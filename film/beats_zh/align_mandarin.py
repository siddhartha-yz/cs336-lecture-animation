"""Fit whole Mandarin takes to the original six shots and lock animation to the new word clock."""
from bisect import bisect_right
from math import ceil
from difflib import SequenceMatcher
from pathlib import Path
import argparse,json,re,subprocess,unicodedata
import numpy as np
import soundfile as sf
from scipy import signal
from localize_script import P,C

R=Path(__file__).resolve().parent
SR=24000; FPS=30
REST={'c':(1,2.0),'e':(2,2.3)}
RE_PUNCT=re.compile(r'[^a-z0-9\u3400-\u9fff]+')
def canon(s):
    s=unicodedata.normalize('NFKC',s).lower()
    for pat,val in ((r'h\s*(?:100|一百)','h一百'),(r'3\.28','三点二八'),(r'\be[ -]*lo[w]?\b','elo')):
        s=re.sub(pat,val,s)
    return RE_PUNCT.sub('',s)

def eng(s):
    return re.sub(r'[^a-z0-9]+','',unicodedata.normalize('NFKC',s).lower())

def wordtimes(parts,qa):
    text=canon(''.join(parts))
    records=qa['words']
    seen=''; starts=[]; ends=[]
    for w in records:
        s=canon(w['word'])
        if not s:continue
        a,b=w['start'],max(w['start'],w['end'])
        grid=np.linspace(a,b,len(s)+1)
        starts.extend(grid[:-1]);ends.extend(grid[1:]);seen+=s
    matcher=SequenceMatcher(a=text,b=seen,autojunk=False)
    keyed={}
    for a,b,n in matcher.get_matching_blocks():
        for j in range(n):keyed[a+j]=(starts[b+j],ends[b+j])
    if matcher.ratio()<.92:
        raise ValueError((qa['id'],'Mandarin word clock matched too little',matcher.ratio(),qa['heard']))
    ix=sorted(keyed)
    q=np.arange(len(text))
    left=np.interp(q,ix,[keyed[j][0] for j in ix])
    right=np.interp(q,ix,[keyed[j][1] for j in ix])
    return text,np.maximum.accumulate(left),np.maximum.accumulate(right),matcher.ratio()

def trim(y):
    block=192
    f=np.sqrt(np.mean(y[:(len(y)//block)*block].reshape(-1,block)**2,axis=1))
    hi=np.flatnonzero(f>max(.004,np.quantile(f,.90)*.058))
    assert len(hi)
    return max(0,int(hi[0]*block)-int(.053*SR)),min(len(y),int((hi[-1]+1)*block)+int(.075*SR))

def tempo(samples,ratio):
    if abs(ratio-1)<.004:return samples.copy()
    return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-nostdin','-f','f32le','-ar',str(SR),
         '-ac','1','-i','-','-af',f'atempo={ratio:.9f}','-f','f32le','-'],
         input=np.asarray(samples,dtype='<f4').tobytes()),dtype='<f4').copy()

def fit(old,parts,path,qa):
    sid=old['id']
    y,s=sf.read(path,dtype='float32')
    assert s==SR and y.ndim==1
    total=len(y)/s
    words,starts,ends,score=wordtimes(parts,qa)
    part_ix=np.r_[0,np.cumsum([len(canon(p)) for p in parts])]
    assert len(words)==part_ix[-1]
    lo,hi=trim(y)
    y=y[lo:hi].copy()
    starts=np.clip(starts-lo/SR,0.,len(y)/SR)
    ends=np.clip(ends-lo/SR,0.,len(y)/SR)
    native=len(y)/SR
    target=old['speech']
    gap=need=0.
    rest=None
    if sid in REST:
        pn,need=REST[sid]
        ix=part_ix[pn]
        g0,g1=ends[ix-1],starts[ix]
        gap=max(0.,g1-g0)
    speed=(native-gap)/(target-need) if gap<need else native/target
    if speed>1.22:
        # Give a slower whole take a few more frames rather than forcing
        # an unnaturally fast explanation to match the English timing.
        wanted=(native-gap)/1.197+need if gap<need else native/1.197
        grow=max(0,ceil((wanted-target)*FPS))
        old['frames']+=grow
        old['duration']=old['frames']/FPS
        target+=grow/FPS
        old['speech']=target
        speed=(native-gap)/(target-need) if gap<need else native/target
    rc=tempo(y,speed)
    rk=len(rc)/len(y)
    starts*=rk;ends*=rk
    if need:
        p,q=float(ends[ix-1]),float(starts[ix])
        cut_lo=max(132,round((min(p,q)-.14)*SR))
        cut_hi=min(len(rc)-133,round((max(p,q)+.08)*SR))
        env=np.sqrt(np.convolve(rc[cut_lo-132:cut_hi+133]**2,np.ones(264)/264,mode='same'))[132:-132]
        ii=int(np.argmin(env));cut=cut_lo+ii
        if env[ii]>.036:
            raise RuntimeError((sid,'A quiet split could not be found at the reflection',p,q,float(env[ii])))
        if p>q or cut/SR<p-.018 or cut/SR>q+.018:
            # The end returned by ASR may span room tone; get the room
            # edges from the signal on the two sides of the same trough.
            hop=120; block=round(.008*SR)
            def room(k):
                return np.sqrt(np.mean(rc[k-block//2:k+block//2]**2))<.012
            k=cut
            while k>block+hop and cut-k<SR*.7 and room(k-hop):k-=hop
            p=k/SR
            k=cut
            while k+block+hop<len(rc) and k-cut<SR*.7 and room(k+hop):k+=hop
            q=k/SR
            ends[ix-1]=min(ends[ix-1],p)
            starts[ix]=max(starts[ix],q)
        ext=round(max(0,need-(q-p))*SR)
        if ext:
            n=80
            rc[cut-n:cut]*=np.linspace(1,0,n,dtype='float32')
            rc[cut:cut+n]*=np.linspace(0,1,n,dtype='float32')
            rc=np.r_[rc[:cut],np.zeros(ext,dtype='float32'),rc[cut:]]
            starts[ix:]+=ext/SR;ends[ix:]+=ext/SR
        rest=(p,q+ext/SR)
    final_n=round(target*SR)
    corr=len(rc)/final_n
    if abs(corr-1)>.0009:
        before=len(rc);rc=tempo(rc,corr)
        q=len(rc)/before
        starts*=q;ends*=q
        if rest:rest=tuple(x*q for x in rest)
    # A final maximum ±35ms is at the already trimmed breath tail.
    if abs(len(rc)-final_n)>round(.036*SR):raise ValueError((sid,'audio fit length',len(rc),final_n))
    if len(rc)<final_n:rc=np.pad(rc,(0,final_n-len(rc)))
    else:rc=rc[:final_n]
    if not .76<=speed<=1.26:
        print(f'{sid} editorial check: tempo ×{speed:.3f}',flush=True)
    b=signal.butter(2,[68,10600],fs=SR,output='sos',btype='bandpass')
    rc=signal.sosfilt(b,rc).astype('float32')
    pp=np.percentile(abs(rc),95)
    rc*=min(2.55,.209/max(.006,pp))
    ha=abs(rc)>.72
    rc[ha]=np.sign(rc[ha])*(.72+.16*np.tanh((abs(rc[ha])-.72)/.16))
    rc[:192]*=np.linspace(0,1,192,dtype='float32')
    rc[-384:]*=np.linspace(1,0,384,dtype='float32')
    print(f'{sid} {total:.2f}s native → {target:.2f}s at ×{speed:.3f}; clock {score:.3f}'+
          (f'; reflection {rest[1]-rest[0]:.2f}s' if rest else ''),flush=True)
    return rc,words,starts,ends,part_ix,rest

def make_cues(r,words,starts):
    old=r['cues_text']; legacy=np.asarray(r['cues']);d=r['duration']
    pts={0:0.,len(old):r['speech']/d}
    for i,(en,_) in enumerate(r['parts']):
        ii=sum(len(eng(x[0])) for x in r['parts'][:i])
        jj=sum(len(canon(s)) for s in P[r['id']][:i])
        if i and ii<len(old):pts[ii]=starts[jj]/d
    resolved={}
    for english,zh in C[r['id']]:
        x,y=old.find(eng(english)),words.find(canon(zh))
        if y<0:raise ValueError((r['id'],zh))
        t=float(starts[y]/d)
        # Allow exact-key override for source alternatives that do not occur
        # literally (e.g. written 3.28 vs the spoken Three point two eight).
        resolved[eng(english)]=t
        if x<0 or x in pts:continue
        ix=sorted(pts)
        n=bisect_right(ix,x)
        if pts[ix[n-1]]<=t<=pts[ix[n]]:
            pts[x]=t
    ix=np.array(sorted(pts))
    xx=legacy[ix]
    yy=np.array([pts[i] for i in ix])
    assert np.min(np.diff(yy))>=-1e-9,(r['id'],pts)
    return np.interp(legacy,xx,yy).tolist(),resolved

def lines(s,limit=25.5):
    w=lambda p:sum(.56 if ch.isascii() else 1. for ch in p)
    out=[]
    s=s.strip()
    while w(s)>limit+2:
        options=[i for i in range(1,len(s)) if s[i-1] in '，、。；：？！' and 8<=w(s[:i])<=limit+2 and w(s[i:])>=5]
        if options:j=min(options,key=lambda i:abs(w(s[:i])-limit))
        else:
            j=min(range(1,len(s)),key=lambda i:abs(w(s[:i])-limit))
            while j>6 and s[j-1].isascii() and s[j].isascii() and s[j-1].isalnum() and s[j].isalnum():
                j-=1
        out.append(s[:j].strip());s=s[j:].strip()
    if s:out.append(s)
    return out

def fmt(t):
    ms=round(t*1000)
    h,mm=divmod(ms,3600000); m,mm=divmod(mm,60000);s,ms=divmod(mm,1000)
    return f'{h:02}:{m:02}:{s:02},{ms:03}'

def main():
    par=argparse.ArgumentParser()
    par.add_argument('--partial',nargs='+')
    args=par.parse_args()
    source=json.loads((R/'english_timeline.json').read_text())
    result=[]; dry=[]; subs=[]; at=0
    for r in source:
        k=r['id'];parts=P[k]
        r['start']=at
        if args.partial and k not in args.partial:
            at+=r['frames'];r['end']=at
            result.append(r);continue
        aud=R/f'audio/takes/{k}.wav'
        qa=json.loads((R/f'audio/qa/{k}.qa.json').read_text())
        pcm,words,starts,ends,pi,rest=fit(r,parts,aud,qa)
        at+=r['frames'];r['end']=at;d=r['duration']
        r['cues'],r['zh_cue_override']=make_cues(r,words,starts)
        r['parts_at']=[float(starts[i]/d) for i in pi[:-1]]
        if rest:r['pause_at']=rest
        r['captions']=[]
        draft=[]
        for i,p in enumerate(parts):
            cursor=pi[i]
            for label in lines(p):
                after=cursor+len(canon(label))
                draft.append((cursor,after,label))
                cursor=after
            assert cursor==pi[i+1],(k,p)
        for j,(a,b,label) in enumerate(draft):
            t0=max(0,float(starts[a])-.045)
            t1=min(float(ends[b-1])+.20,r['speech'])
            if j+1<len(draft):t1=min(t1,max(t0+.10,float(starts[draft[j+1][0]])-.056))
            if rest and b==pi[REST[k][0]]:t1=min(t1,rest[0]+.13)
            assert t1-t0>=.1,(k,label)
            r['captions'].append(dict(a=t0,b=t1,text=label))
            shift=r['start']/FPS;subs.append((shift+t0,shift+t1,label))
        r['parts']=[[en[0],zh] for en,zh in zip(r['parts'],parts)]
        dry.append(np.pad(pcm,(0,r['frames']*(SR//FPS)-len(pcm))))
        result.append(r)
    (R/('partial.json' if args.partial else 'timeline.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    if args.partial:return
    sf.write(R/'audio'/'dry.wav',np.concatenate(dry),SR,'PCM_24')
    (R/'zh.srt').write_text('\n'.join(f'{i}\n{fmt(t0)} --> {fmt(t1)}\n{x}\n' for i,(t0,t1,x) in enumerate(subs,1)))
    meta=(R/'meta.ffmeta').read_text()
    anchors=iter((result[0]['start'],result[1]['end'],result[2]['start'],result[-1]['end']))
    meta=re.sub(r'^(START|END)=\d+',lambda m:f'{m[1]}={next(anchors)}',meta,flags=re.M)
    (R/'meta.ffmeta').write_text(meta)
    print(f'{at/FPS:.3f}s · {len(subs)} captions')
if __name__=='__main__':main()
