"""Build an editable cut from continuous performances. Only room-tone pauses are trimmed."""
from pathlib import Path
import argparse,json,re,subprocess,sys
import numpy as np
import soundfile as sf
from scipy import signal
from scipy.ndimage import gaussian_filter1d
R=Path(__file__).resolve().parent
sys.path[:0]=[str(R.parent/'v2'),str(R.parent)]
from timing import wordclock,flat,clock
SR=48000
VS,FPS=24000,30
p=argparse.ArgumentParser()
p.add_argument('--estimate',action='store_true')
p.add_argument('--partial',nargs='+',metavar='ID',help='fit selected verified takes and estimate the remaining edit slots')
a=p.parse_args()
rows=[json.loads((R/f'script_{k}.json').read_text()) for k in 'ghijk']
def read(k):return json.loads(k.read_text())
def ts_for(n):
    c=n//FPS
    return f'{c//60:02}:{c%60:02}.{round(n%FPS/30*100):02}'
def align_aliases(words):
    anchors={('100000',):'a hundred thousand',('10',):'ten',('gpt2',):'GPT two',
             ('wikitext103',):'WikiText one oh three',('wikitext','103'):'WikiText one oh three',
             ('utf8',):'UTF eight',('you','tee','eff','eight'):'UTF eight'}
    out=[];i=0
    while i<len(words):
        for seq,spelling in anchors.items():
            if tuple(flat(q['word']) for q in words[i:i+len(seq)])==seq:
                out.append(dict(word=spelling,start=words[i]['start'],end=words[i+len(seq)-1]['end']))
                i+=len(seq)
                break
        else:out.append(words[i]);i+=1
    return out

def reflection(r,heard,source,retime,rate,tm,y):
    plan=r.get('thinking')
    if not plan:return tm,y,None
    idx=sum(len(flat(x[0])) for x in r['parts'][:plan['after_part']+1])
    next_raw=source[idx]
    words=heard['words']
    prev=max((w for w in words if w['start']<next_raw-.042),key=lambda w:w['start'])
    p=min(tm[idx],float(retime([prev['end']])[0]/rate))
    q=float(tm[idx])
    # Insert room tone at the quiet trough across the verbatim question seam.
    lo=max(96,round((max(p,q-.25)-.022)*VS)); hi=min(len(y)-96,round((q+.008)*VS))
    if hi<lo:hi=lo
    short=y[max(0,lo-96):hi+97]
    rms=np.convolve(short*short,np.ones(128,dtype=np.float32)/128,mode='same')
    a0=max(0,lo-96)
    k=lo+int(np.argmin(rms[lo-a0:hi-a0+1]))
    if np.sqrt(rms[k-a0])>.045:raise RuntimeError((r['id'],'question seam is not between words',p,q))
    ext=max(0.,plan['seconds']-(q-p))
    n=round(ext*VS)
    y[k-64:k]*=np.linspace(1,0,64)
    y[k:k+64]*=np.linspace(0,1,64)
    y=np.concatenate([y[:k],np.zeros(n,dtype=np.float32),y[k:]])
    tm[idx:]+=n/VS
    return tm,y,(p,q+n/VS)

def pause_trim(path,marks):
    x,sr=sf.read(path,dtype='float32',always_2d=True)
    x=np.mean(x,axis=1)
    if sr!=VS:x=signal.resample_poly(x,VS,sr).astype('float32')
    # Tail breaths stay unless long inaudible room tone. Preserve a 35 ms
    # buffer on each side of word landmarks for consonants.
    size=round(VS*.008)
    rms=np.sqrt(np.mean(x[:len(x)//size*size].reshape(-1,size)**2,axis=1))
    ex=np.flatnonzero(rms>max(.003,.055*np.quantile(rms,.9)))
    if len(ex):
        low=max(0,ex[0]*size-round(.051*VS))
        high=min(len(x),(ex[-1]+1)*size+round(.083*VS))
    else:low,high=0,len(x)
    words=marks.get('words',[])
    drops=[]
    for p,q in zip(words,words[1:]):
        ga,gb=float(p['end']),float(q['start'])
        if gb-ga<=.32:continue
        lo=max(low//size,round((ga+.027)*VS/size))
        hi=min(high//size,round((gb-.027)*VS/size))
        mask=(rms[lo:hi]<max(.008,.105*np.quantile(rms,.9)))
        edge=np.diff(np.r_[False,mask,False].astype(int))
        zz=list(zip(np.flatnonzero(edge==1)+lo,np.flatnonzero(edge==-1)+lo))
        if not zz:continue
        s,e=max(zz,key=lambda v:v[1]-v[0])
        can=min((e-s)*size-round(VS*.026),round((gb-ga-.252)*VS))
        if can<round(VS*.028):continue
        center=(e+s)*size//2
        start=center-can//2
        drops.append((start,start+can))
    def remap(times):
        u=np.asarray(times)*VS
        out=u-low
        for s,e in drops:out-=np.clip(u-s,0,e-s)
        return np.maximum(0,out)/VS
    y=[];last=low
    for s,e in drops:
        # 2.2 ms fades entirely inside room tone at the splice.
        x[s-54:s]*=np.linspace(1,0,54,dtype='float32')
        x[e:e+54]*=np.linspace(0,1,54,dtype='float32')
        y.append(x[last:s]);last=e
    y.append(x[last:high])
    return np.concatenate(y),remap,drops

def rate_change(samples,rate):
    if abs(rate-1)<.007:return samples
    pcm=np.asarray(samples,dtype='<f4').tobytes()
    args=['ffmpeg','-nostdin','-v','error','-f','f32le','-ar',str(VS),'-ac','1','-i','-',
          '-af',f'atempo={rate:.9f}','-f','f32le','-']
    return np.frombuffer(subprocess.check_output(args,input=pcm),dtype='<f4').copy()

def splits(z,maxlen=26):
    if '\n' in z:return z.splitlines()
    todo=z;result=[]
    while len(todo)>maxlen+6:
        cand=[i+1 for i,c in enumerate(todo[:maxlen+8]) if c in '，。；：！？、' and 12<=i+1<=min(len(todo)-9,maxlen+6)]
        j=min(cand,key=lambda i:abs(i-maxlen)) if cand else maxlen
        if not cand:
            while j>12 and todo[j-1].isascii() and todo[j].isascii() and todo[j-1].isalnum() and todo[j].isalnum():j-=1
        result.append(todo[:j]);todo=todo[j:]
    if todo:result.append(todo)
    return result

at=0;all_audio=[];full=[];holds=[]
for r in rows:
    k=r['id'];text=' '.join(e for e,z in r['parts']);wanted=flat(text)
    path=R/f'audio/takes/{k}.wav'
    anchored=R/f'audio/verified-marks/{k}.json'
    qa=anchored if anchored.exists() else R/f'audio/qa/{k}.qa.json'
    nominal=round(r['duration']*FPS)
    fit=not a.estimate and (not a.partial or k in a.partial) and path.exists() and qa.exists()
    if not (a.estimate or a.partial or fit):raise FileNotFoundError(f'{path}, {qa}')
    if fit:
        heard=read(qa)
        heard['words']=align_aliases(heard['words'])
        n=sf.info(path).duration
        key,source,match=wordclock(text,heard,n)
        y,retime,dropped=pause_trim(path,heard)
        raw=len(y)/VS
        # Let a take keep its own cadence. Planned shot time is a guide;
        # leave the edit slightly shorter instead of inserting sentence gaps.
        target=nominal/FPS-r['hold']
        wordcount=len(text.split())
        extra=r.get('thinking',{}).get('seconds',0)
        natural_rate=max(.80,min(1.28,raw/max(1.,target-extra)))
        y=rate_change(y,natural_rate)
        tm=retime(source)/natural_rate
        tm,y,pause_at=reflection(r,heard,source,retime,natural_rate,tm,y)
        fine_rate=len(y)/VS/target
        if abs(fine_rate-1)>.003:
            before=len(y)
            y=rate_change(y,fine_rate)
            ratio=len(y)/before
            tm=tm*ratio
            if pause_at:pause_at=tuple(t*ratio for t in pause_at)
        if pause_at:r['pause_at']=pause_at
        # ffmpeg's overlap window can leave an extra ~20 ms; end of file is
        # already beyond the last voiced sample, so retain the intended rest.
        max_len=nominal*(VS//FPS)-round((r['hold']-.05)*VS)
        y=y[:max_len]
        support=len(y)/VS
        frames=nominal
        b=signal.butter(2,[66,10600],fs=VS,btype='bandpass',output='sos')
        y=signal.sosfilt(b,y).astype('float32')
        pp=np.percentile(abs(y),95)
        gain=min(2.5,.232/max(.006,pp))
        y*=gain
        # Stay linear through the speaker's normal dynamic range; round off
        # only rare peaks, preserving expressive phrase-to-phrase contrast.
        high=np.abs(y)>.72
        y[high]=np.sign(y[high])*(.72+.16*np.tanh((np.abs(y[high])-.72)/.16))
        for q,sl in ((1,y[:240]),(-1,y[-300:])):sl*=np.linspace(0,1,len(sl))[::q]
        all_audio.append(np.pad(y,(0,frames*(VS//FPS)-len(y))))
        holds.append((at/FPS+support, (at+frames)/FPS, k))
        print(k,ts_for(at),f'native {n:.2f}s; {len(dropped)} room gaps shortened; tempo ×{natural_rate:.3f}; speech {support:.2f}s; ASR {match:.3f}',flush=True)
    else:
        frames=nominal
        support=frames/FPS-r['hold']
        tm=np.linspace(0,support-r.get('thinking',{}).get('seconds',0)-.07,len(wanted)+1)
        if plan:=r.get('thinking'):
            ix=sum(len(flat(v[0])) for v in r['parts'][:plan['after_part']+1])
            r['pause_at']=(float(tm[ix]),float(tm[ix]+plan['seconds']))
            tm[ix:]+=plan['seconds']
    duration=frames/FPS
    r.update(start=at,end=at+frames,frames=frames,duration=duration,speech=support,cues_text=wanted,
             cues=[float(q/duration) for q in tm])
    at+=frames
    ends=[];n=0
    for e,z in r['parts']:
        ends.append(float(tm[n]));n+=len(flat(e))
    r['parts_at']=[float(q/duration) for q in ends]
    cc=[]
    for j,((e,z),t) in enumerate(zip(r['parts'],ends)):
        t=max(0,t-.034)
        u=max(t+.25,(ends[j+1] if j+1<len(ends) else support)-.053)
        u=min(u,support)
        if 'pause_at' in r and j==r.get('thinking',{}).get('after_part'):
            u=min(u,float(r['pause_at'][0]+.12))
        tt=splits(z);wgt=[sum(.53 if c.isascii() else 1 for c in q) for q in tt]
        acc=np.r_[0,np.cumsum(np.asarray(wgt)/sum(wgt))]
        for i,caption in enumerate(tt):
            x=float(t+(u-t)*acc[i]);y=float(t+(u-t)*acc[i+1])
            cc.append(dict(a=x,b=y,text=caption))
            full.append((r['start']/FPS+x,r['start']/FPS+y,caption))
    r['captions']=cc

(R/('draft.json' if a.estimate else 'partial.json' if a.partial else 'timeline.json')).write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
if a.estimate or a.partial:sys.exit()
T=at/FPS
print(f'Total {T:.3f}s · {at}f · {len(full)} subtitles')
(R/'zh.srt').write_text('\n'.join(f'{i}\n{clock(t)} --> {clock(u)}\n{y}\n' for i,(t,u,y) in enumerate(full,1)),encoding='utf-8')
meta=[';FFMETADATA1','title=What Perplexity Can See — CS336 Lecture 12',
      'comment=English narration · Chinese subtitles · Music by Blue Dot Sessions · Edited excerpts, CC BY-NC 4.0 (https://creativecommons.org/licenses/by-nc/4.0/)']
for title,rr in [('Beat 2 — What perplexity can see',rows)]:
    meta+=['[CHAPTER]','TIMEBASE=1/30',f'START={rr[0]["start"]}',f'END={rr[-1]["end"]}',f'title={title}']
(R/'meta.ffmeta').write_text('\n'.join(meta)+'\n')
dry=np.concatenate(all_audio)
sf.write(R/'dry.wav',dry,VS,subtype='PCM_24')
print("Narration clock ready.")
