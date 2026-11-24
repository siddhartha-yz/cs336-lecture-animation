"""Assemble the film clock, align the authored captions, and build narration/chapter tracks."""
from __future__ import annotations
import argparse,difflib,json,math,re,subprocess,unicodedata
from pathlib import Path
import numpy as np
import soundfile as sf
from opencc import OpenCC
from scipy import signal

R=Path(__file__).resolve().parent
FPS=30; SR=24000; N=SR//FPS; TARGET=1200*FPS
CN=OpenCC('t2s')
def read(p):return json.loads(p.read_text())
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
def normalized(s):
    s=CN.convert(unicodedata.normalize('NFKC',s)).casefold()
    return re.sub(r'[^\u3400-\u9fff\da-z]+','',s)
def linear_marks(script,seconds):
    n=len(script)
    return np.linspace(.09,max(.11,seconds-.14),n+1)
def quantile_curve(matches,n,seconds):
    m={0:.085,n:seconds-.11}
    for k,v in matches:
        if 0<=k<n and 0<=v<seconds:m[k]=v
    xp=sorted(m)
    yp=np.maximum.accumulate([m[i] for i in xp])
    return np.interp(np.arange(n+1),xp,yp)
def text_marks(orig,heard,seconds):
    src=normalized(orig); seq=[]; times=[]
    for w in heard.get('words',[]):
        s=normalized(w['word'])
        for j,c in enumerate(s):
            seq.append(c);times.append(w['start']+(w['end']-w['start'])*j/max(1,len(s)))
    found=''.join(seq)
    blocks=difflib.SequenceMatcher(None,src,found,autojunk=False).get_matching_blocks()
    coverage=sum(b.size for b in blocks)/max(1,len(src))
    hits=[]
    for a,b,n in blocks:
        for i in range(n):hits.append((a+i,times[b+i]))
    return src,quantile_curve(hits,len(src),seconds) if coverage>.54 else linear_marks(src,seconds),coverage

def display_len(s):
    return sum(1 if ord(c)>=0x2e80 else .54 for c in s)
def captions(text):
    """Short semantic phrases; punctuation is the break hierarchy, not a word-wrap width alone."""
    text=re.sub(r'\s+',' ',text).strip()
    allparts=re.findall(r'[^，。！？；：、…]+[，。！？；：、…]*|[，。！？；：、…]+',text)
    groups=[]; buf=''
    for piece in allparts:
        piece=piece.strip()
        if not piece:continue
        if buf and (buf.endswith('……') or display_len(buf+piece)>21.8 or (buf[-1] in '。！？' and display_len(buf)>=9)):
            groups.append(buf);buf=''
        if display_len(piece)>23:
            # Keep Latin words intact. Long unpunctuated Chinese clauses split near a natural connector.
            while display_len(piece)>23:
                cut=19
                for sep in ('还是','然后','可以','我们','把','又','就','也','再'):
                    for idx in range(17,min(len(piece)-3,23)):
                        if piece.startswith(sep,idx):
                            cut=idx;break
                    if cut!=19:break
                while cut<len(piece) and re.match(r'[A-Za-z0-9\-]',piece[cut]) and re.match(r'[A-Za-z0-9\-]',piece[cut-1]):cut+=1
                if buf:groups.append(buf);buf=''
                groups.append(piece[:cut]);piece=piece[cut:]
        buf+=piece
    if buf:groups.append(buf)
    if len(groups)>1 and display_len(groups[-1])<5 and display_len(groups[-2]+groups[-1])<=24:
        groups[-2:]=[''.join(groups[-2:])]
    return [s.strip('，；：、 ').replace('…… ','……') for s in groups if normalized(s)]

def timeline(native=True):
    rows=[]
    for ac in range(1,5):
        for beat,b in enumerate(read(R/f'act{ac}.json')):
            ident=f'{ac}-{beat:02d}'
            wave=R/'voice'/f'{ident}.wav'
            ref=R/'voice_marks'/f'{ident}.json'
            if not wave.exists():
                if native:raise FileNotFoundError(wave)
                n=max(1,len(normalized(b['text'])))
                dur=.6+n/3.85
            else:
                info=sf.info(wave);dur=info.duration
            rows.append({**b,'act':ac,'beat':beat,'id':ident,'wave':str(wave.relative_to(R)),'natural_s':dur,'hold':b.get('hold',.45),
                'asr':str(ref.relative_to(R)) if ref.exists() and (not wave.exists() or ref.stat().st_mtime>=wave.stat().st_mtime) else ''})
    # Keep the hook on its own cadence. Rounding is distributed by cumulative absolute time.
    coda=3.3
    seconds_speech=sum(r['natural_s'] for r in rows[1:])
    seconds_hold=sum(r['hold'] for r in rows)
    opening=rows[0]['natural_s']/1.045
    need=TARGET/FPS-seconds_hold-coda-opening
    # Give a cold open its own delivery, and redistribute a little time from the
    # naturally slow takes to the quick ones; hold lengths never enter atempo.
    lett=lambda s:len(re.findall(r'[㐀-鿿\d]',s))+.61*len(re.findall(r'[A-Za-z]',s))
    local=[lett(r['text'])/(max(1.0,r['natural_s']-.3)) for r in rows[1:]]
    mid=np.median(local)
    shape=[(mid/max(1.,x))**.57 for x in local]
    lo,hi=.79,1.60
    for _ in range(40):
        scale=(lo+hi)/2
        rs=[float(np.clip(scale*f,1.01,1.37)) for f in shape]
        span=sum(r['natural_s']/f for f,r in zip(rs,rows[1:]))
        if span>need:lo=scale
        else:hi=scale
    rates=[1.045,*rs]
    print(f'native narration {seconds_speech+rows[0]["natural_s"]:.1f}s; authored pauses {seconds_hold:.2f}s; tempo {min(rates):.3f}…{max(rates):.3f}',flush=True)
    at=0.
    for j,r in enumerate(rows):
        rate=rates[j]
        ts=at
        speech=r['natural_s']/rate
        at+=speech+r['hold'] + (coda if j==len(rows)-1 else 0)
        start=round(ts*FPS);end=round(at*FPS)
        if j==len(rows)-1:end=TARGET
        r.update(rate=rate,start=start,end=end,frames=end-start,duration=(end-start)/FPS,speech=speech)
        heard=read(R / r['asr']) if r['asr'] else {}
        idx,tm,score=text_marks(r['text'],heard,r['natural_s'])
        tm=tm/rate
        # This question has a manually timed suspense beat. Anchor the answer
        # to the measured voiced onset (7.590s in the edited master), not the
        # recognizer's fuzzy word boundary inside the preceding silence.
        if r['id']=='3-08' and '对刚好贴上' in idx:
            tm[idx.index('对刚好贴上')]=7.645
            tm=np.maximum.accumulate(tm)
        caps=captions(r['text']); offset=0; raw=[]
        for s in caps:
            k=len(normalized(s))
            a=float(tm[min(len(tm)-1,offset)]);offset+=k
            raw.append((s,max(0,a-.052),float(tm[min(len(tm)-1,offset)])))
        line=[]
        for k,(s,a,b) in enumerate(raw):
            e=(raw[k+1][1] if k+1<len(raw) else speech-.03)
            # Make real breathing gaps subtitle-free, without strobing a semicolon.
            if k+1<len(raw) and b-a>.6 and e-b>.42:e=b+.13
            line.append({'in':round(a,4),'out':round(max(a+.12,e),4),'text':s})
        r.update(cues_text=idx,cues=[round(x/r['duration'],5) for x in tm],captions=line,match=round(score,4))
    assert rows[-1]['end']==TARGET and all(r['frames']>0 for r in rows)
    return rows

def subtitle_clock(seconds):
    m=round(seconds*1000)
    h,m=divmod(m,3600000);minute,m=divmod(m,60000);sec,m=divmod(m,1000)
    return f'{h:02d}:{minute:02d}:{sec:02d},{m:03d}'
def srt(rows,p):
    out=[];index=0
    for r in rows:
        offs=r['start']/FPS
        for w in r['captions']:
            index+=1
            out.append(f'{index}\n{subtitle_clock(offs+w["in"])} --> {subtitle_clock(offs+w["out"])}\n{w["text"]}\n')
    p.write_text('\n'.join(out),encoding='utf-8')
def meta(rows,p):
    t=[';FFMETADATA1','title=好分数，量的是哪一格？','artist=CS336 第12讲 · 动画讲解','comment=普通话旁白 · 简体中文字幕 · 原创配乐']
    names=['猜下一格：困惑度','同一张卷子：考试与裁判','得亲手做：智能体与推理','试卷从哪来：污染与生态效度']
    for a,name in enumerate(names,1):
        first=next(r for r in rows if r['act']==a)
        last=next(r for r in rows[::-1] if r['act']==a)
        t.extend(('[CHAPTER]','TIMEBASE=1/30',f'START={first["start"]}',f'END={last["end"]}',f'title={name}'))
    p.write_text('\n'.join(t)+'\n',encoding='utf-8')

def voice_master(rows,dest):
    filt=signal.butter(2,[67,9800],btype='bandpass',fs=SR,output='sos')
    with sf.SoundFile(dest,'w',samplerate=SR,channels=1,subtype='PCM_24') as f:
        for r in rows:
            arr=subprocess.check_output(['ffmpeg','-nostdin','-v','error','-i',str(R / r['wave']),'-af',f'atempo={r["rate"]:.8f}','-ac','1','-ar',str(SR),'-f','f32le','pipe:1'])
            x=np.frombuffer(arr,dtype='<f4')
            x=signal.sosfilt(filt,x).astype('float32')
            # Normalize clip-to-clip recording level by active syllables, preserving intra-phrase dynamics.
            nf=min(len(x),round(r['speech']*SR))
            x=x[:nf]
            p95=float(np.percentile(np.abs(x),95))
            gain=min(2.3,.255/max(.01,p95))
            x=x*gain
            x=.88*np.tanh(x/.88)
            x[:min(240,len(x))]*=np.linspace(0,1,min(240,len(x)))
            x[-min(420,len(x)):]*=np.linspace(1,0,min(420,len(x)))
            f.write(x)
            f.write(np.zeros(r['frames']*N-len(x),dtype=np.float32))

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--estimate',action='store_true')
    p.add_argument('--skip-voice',action='store_true')
    p.add_argument('--name',default='timeline')
    a=p.parse_args()
    rows=timeline(not a.estimate)
    dump(R/f'{a.name}.json',rows)
    srt(rows,R/f'{a.name}.srt')
    meta(rows,R/f'{a.name}.ffmeta')
    if not a.skip_voice and not a.estimate:voice_master(rows,R/'voice_master.wav')
    for ac in range(1,5):
        arows=[r for r in rows if r['act']==ac]
        print(f'Act {ac}: {arows[0]["start"]/FPS:.2f} → {arows[-1]["end"]/FPS:.2f} / median ASR {np.median([r["match"] for r in arows]):.3f}')
