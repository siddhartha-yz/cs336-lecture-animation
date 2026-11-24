"""One shared 20-minute timebase, mapped from the actual English performance."""
from pathlib import Path
import argparse,difflib,json,math,re,subprocess,unicodedata
import numpy as np
import soundfile as sf
from scipy import signal
R=Path(__file__).resolve().parent
FPS=30;SR=24000;N=SR//FPS;FRAMES=36000
def flat(s):return re.sub('[^a-z0-9]','',unicodedata.normalize('NFKC',s).lower())
def read(p):return json.loads(p.read_text())
def dump(p,data):p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def words(s):return len(re.findall(r"[A-Za-z0-9]+(?:[’'][A-Za-z]+)?",s))
def wordclock(text,heard,dur):
    src=flat(text)
    xs=[];ts=[]
    for w in heard.get('words',[]):
        a=flat(w['word'])
        xs.extend(a);ts.extend(np.linspace(w['start'],w['end'],len(a),endpoint=False))
    alt=''.join(xs);n=len(src)
    seq=difflib.SequenceMatcher(None,src,alt,autojunk=False).get_matching_blocks()
    match=sum(x.size for x in seq)/max(n,1)
    m={0:.07,n:dur-.08}
    if match>.52:
        for a,b,q in seq:
            for j in range(q):
                if 0<=ts[b+j]<dur:m[a+j]=float(ts[b+j])
    xp=sorted(m);yp=np.maximum.accumulate([m[x] for x in xp])
    return src,np.interp(np.arange(n+1),xp,yp),match
def timeline(estimate=False):
    rows=[]
    for act in range(1,5):
        for i,b in enumerate(read(R/f'act{act}.json')):
            text=' '.join(p[0].strip() for p in b['parts'])
            key=f'{act}-{i:02d}'
            path=R/'voice'/f'{key}.wav'; mark=R/'marks'/f'{key}.json'
            if not path.exists() and not estimate:raise FileNotFoundError(path)
            dur=sf.info(path).duration if path.exists() else words(text)/2.11+.35
            valid=mark.exists() and path.exists() and mark.stat().st_mtime>=path.stat().st_mtime
            rows.append(dict(**b,text=text,nwords=words(text),act=act,beat=i,id=key,
                             take=str(path.relative_to(R)),native_s=dur,marks=str(mark.relative_to(R)) if valid else '',
                             pause=float(b.get('hold',.62))))
    intro=.99;tail=3.1
    remaining=FRAMES/FPS-tail-sum(r['pause'] for r in rows)-rows[0]['native_s']/intro
    pace=[r['nwords']/max(1,r['native_s']-.41) for r in rows[1:]]
    ref=np.median(pace)
    shape=[(ref/max(.65,x))**.52 for x in pace]
    lo,hi=.53,1.43
    for _ in range(42):
        mid=(lo+hi)/2
        rates=[float(np.clip(mid*x,.72,1.29)) for x in shape]
        got=sum(r['native_s']/q for r,q in zip(rows[1:],rates))
        if got>remaining:lo=mid
        else:hi=mid
    if abs(got-remaining)>.05:raise RuntimeError(f'Unreachable time: {got:.2f} vs {remaining:.2f}')
    at=0.
    for i,(r,rate) in enumerate(zip(rows,[intro]+rates)):
        st=round(at*FPS)
        dur=r['native_s']/rate
        at+=dur+r['pause']+(tail if i==len(rows)-1 else 0)
        end=round(at*FPS) if i<len(rows)-1 else FRAMES
        shot=(end-st)/FPS
        heard=read(R / r['marks']) if r['marks'] else {}
        text,marks,match=wordclock(r['text'],heard,r['native_s'])
        tm=marks/rate
        r.update(start=st,end=end,frames=end-st,duration=shot,rate=rate,speech=dur,
                 cues_text=text,cues=[round(float(a/shot),6) for a in tm],match=round(match,4))
        offset=0;heads=[];tails=[]
        for e,z in r['parts']:
            here=int(min(len(text),offset));offset+=len(flat(e))
            after=int(min(len(text),offset))
            heads.append(min(dur-.16,max(0,float(tm[here]))))
            tails.append(float(tm[after]))
        for q in range(1,len(heads)):
            # Some recognizers time two very short words on the same Mark.
            # Preserve the reading order and give a Chinese line a real frame span.
            if heads[q]-heads[q-1]<.43:heads[q]=heads[q-1]+.43
        if heads[-1]>=dur-.10:heads[-1]=dur-.12
        r['parts_at']=[round(t/shot,6) for t in heads]
        caps=[]
        for j,((e,z),u,v) in enumerate(zip(r['parts'],heads,tails)):
            begin=max(0,u-.025)
            finish=heads[j+1]-.025 if j<len(heads)-1 else dur-.025
            if finish-v>.7 and v-begin>1.1:finish=v+.16
            if finish>begin+.053:
                caps.append(dict(text=z.strip(),en=e.strip(),a=round(begin,4),b=round(finish,4)))
        r['captions']=caps
    for j in range(1,5):
        rr=[r for r in rows if r['act']==j]
        print(f'{j}: {rr[0]["start"]/FPS:.2f} → {rr[-1]["end"]/FPS:.2f}, median ASR={np.median([r["match"] for r in rr]):.3f}, {sum(r["nwords"] for r in rr)/(sum(r["speech"] for r in rr)/60):.0f} wpm',flush=True)
    print(f'Voice source {sum(r["native_s"] for r in rows):.1f}s; paced {sum(r["speech"] for r in rows):.1f}s; rate {min(x["rate"] for x in rows):.3f}–{max(x["rate"] for x in rows):.3f}')
    return rows
def clock(t):
    ms=round(t*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000)
    return f'{h:02d}:{m:02d}:{s:02d},{ms:03d}'
def subs(rows):
    en=[];zh=[];i=1
    for r in rows:
        p=r['start']/FPS
        for q in r['captions']:
            qe=f'{i}\n{clock(p+q["a"])} --> {clock(p+q["b"])}\n'
            en.append(qe+q['en']+'\n');zh.append(qe+q['text']+'\n');i+=1
    (R/'en.srt').write_text('\n'.join(en),encoding='utf-8')
    (R/'zh.srt').write_text('\n'.join(zh),encoding='utf-8')
def metadata(rows):
    names=('The missing tile','The exam and the judge','The system has to act','Where did the test come from?')
    l=[';FFMETADATA1','title=The Missing Tile: Evaluation and Benchmarks','comment=CS336 Lecture 12 · Spatial edition · English narration · Chinese subtitles']
    for a,s in enumerate(names,1):
        rs=[r for r in rows if r['act']==a]
        l+=['[CHAPTER]','TIMEBASE=1/30',f'START={rs[0]["start"]}',f'END={rs[-1]["end"]}',f'title={s}']
    (R/'chapters.ffmeta').write_text('\n'.join(l)+'\n')
def voice(rows):
    filt=signal.butter(2,[63,10400],btype='bandpass',fs=SR,output='sos')
    with sf.SoundFile(R/'dry.wav','w',samplerate=SR,channels=1,subtype='PCM_24') as f:
        for r in rows:
            raw=subprocess.check_output(['/usr/bin/ffmpeg','-nostdin','-v','error','-i',str(R / r['take']),'-af',f'atempo={r["rate"]:.9f}','-ac','1','-ar',str(SR),'-f','f32le','pipe:1'])
            x=np.frombuffer(raw,dtype='<f4')[:round(r['speech']*SR)]
            x=signal.sosfilt(filt,x).astype('float32')
            g=np.percentile(np.abs(x),95)
            x=.88*np.tanh((x*min(2.45,.243/max(.01,g)))/.88)
            x[:160]*=np.linspace(0,1,160);x[-420:]*=np.linspace(1,0,420)
            f.write(x);f.write(np.zeros(r['frames']*N-len(x),dtype=np.float32))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--estimate',action='store_true');p.add_argument('--skip-voice',action='store_true');a=p.parse_args()
    rows=timeline(a.estimate);dump(R/'timeline.json',rows)
    if not a.estimate:
        subs(rows);metadata(rows)
        if not a.skip_voice:voice(rows)
