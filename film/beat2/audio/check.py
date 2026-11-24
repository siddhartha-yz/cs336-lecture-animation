#!/usr/bin/env python3
"""Rolling ASR and source QA for dry whole-scene audio."""
import argparse
from difflib import SequenceMatcher
import json
from math import gcd
from pathlib import Path
import re
import time

from faster_whisper import WhisperModel
import numpy as np
import soundfile as sf
from scipy.signal import resample_poly
from common import AUDIO, CANDIDATE, SCENES, write_json

STOP=AUDIO/"control"/"stop-qa"
ASR_MODEL=AUDIO.parent.parent/"asr_model"
ONES="zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
TENS="zero ten twenty thirty forty fifty sixty seventy eighty ninety".split()
ALIASES=[
   (r"\bnano\s*(?:gpt|g p t)\b","nanogpt"),
   (r"\bg p t\b","gpt"),
   (r"\bopen\s*router\b","openrouter"),
   (r"\bfine\s*web\b","fineweb"),
   (r"\bimage\s*net\b","imagenet"),
   (r"\bweb\s*text\b","webtext"),
   (r"\bpre[-\s]training\b","pretraining"),
   (r"\bfine[-\s]tuning\b","finetuning"),
   (r"\bmodels'\b|\bmodel's\b","models"), # Same phone sequence.
   (r"\bhere's\b","here is"),
   (r"\bwhat's\b","what is"),
   (r"\bthat's\b","that is"),
   (r"\bit's\b","it is"),
   (r"\bcannot\b|\bcan't\b","can not"),
   (r"\bdon't\b","do not"),
   (r"\bdoesn't\b","does not"),
   (r"\bdidn't\b","did not"),
]
def integer(n):
    if n<20: return ONES[n]
    if n<100: return TENS[n//10]+(" "+integer(n%10) if n%10 else "")
    if n<1000: return ONES[n//100]+" hundred"+(" "+integer(n%100) if n%100 else "")
    if 2000<=n<=2099: return "twenty"+(" "+integer(n%100) if n%100 else " hundred")
    if n<1000000: return integer(n//1000)+" thousand"+(" "+integer(n%1000) if n%1000 else "")
    return " ".join(ONES[int(x)] for x in str(n))

def lexical(s):
    s=s.lower().replace("’","'").replace("–","-").replace("‑","-").replace(","," ")
    s=re.sub(r"(\d+)\.(\d+)",lambda m:" "+integer(int(m[1]))+" point "+" ".join(ONES[int(x)] for x in m[2])+" ",s)
    s=re.sub(r"\d+",lambda m:" "+integer(int(m[0]))+" ",s)
    s=s.replace("%"," percent ").replace("@"," at ")
    for pattern,r in ALIASES: s=re.sub(pattern,r,s)
    return re.findall(r"[a-z]+(?:'[a-z]+)?",s)

def pitch_wav(x,sr):
    # Objective continuity check, not an assertion that a person has auditioned it.
    div=gcd(sr,8000)
    y=resample_poly(x,8000//div,sr//div)
    n,hop=440,96
    f=np.lib.stride_tricks.sliding_window_view(y,n)[::hop].copy()
    f-=f.mean(axis=1,keepdims=True)
    rms=np.sqrt((f*f).mean(axis=1)); f*=np.hanning(n)
    ac=np.fft.irfft(abs(np.fft.rfft(f,1024))**2)[:,:151]
    ac/=np.maximum(ac[:,:1],1e-9)
    peak=(ac[:,26:144]>=ac[:,25:143]) & (ac[:,26:144]>ac[:,27:145])
    c=np.where(peak,ac[:,26:144],-1)
    score=c.max(axis=1)
    lag=(c>=score[:,None]*.94).argmax(axis=1)+26
    h=8000/lag[(score>.52)&(rms>max(.003,np.percentile(rms,75)*.14))]
    q=np.percentile(h,(12.5,50,87.5)) if len(h)>=6 else [0,0,0]
    return {"median_hz":float(q[1]),"central_range_st":float(12*np.log2(q[2]/q[0])) if q[0]>0 else 0}

def asr(model,signal,offset=0,beam=3):
    rs,_=model.transcribe(signal,language="en",beam_size=beam,word_timestamps=True,
                         condition_on_previous_text=False,no_repeat_ngram_size=5)
    rs=list(rs)
    return ("".join(s.text for s in rs).strip(),[dict(word=w.word.strip(),start=round(float(w.start)+offset,3),end=round(float(w.end)+offset,3))
           for s in rs for w in (s.words or [])])

def compare(raw,heard):
    expected,actual=lexical(raw),lexical(heard)
    m=SequenceMatcher(autojunk=False,a=expected,b=actual)
    return m.ratio(),[dict(action=tag, expected=expected[i:j], observed=actual[k:l], observed_index=k)
                     for tag,i,j,k,l in m.get_opcodes() if tag!="equal"]

def check(candidate,model):
    base=AUDIO/"staging"/candidate
    meta=json.loads(base.with_suffix(".json").read_text())
    w=base.with_suffix(".wav")
    info=sf.info(w)
    x,sr=sf.read(w,dtype="float32")
    if sr!=24000 or info.subtype!="PCM_24" or x.ndim!=1 or not np.isfinite(x).all() or not .005<abs(x).max()<.99999:
        raise ValueError("invalid dry candidate PCM")
    div=gcd(sr,16000)
    y=resample_poly(x,16000//div,sr//div).astype("float32")
    heard,words=asr(model,y)
    sim,edits=compare(meta["raw"],heard)
    pauses=[{"seconds":round(b["start"]-a["end"],3),"after":a["word"],"before":b["word"],"start":a["end"]}
           for a,b in zip(words,words[1:]) if b["start"]-a["end"]>=.30]
    out={"id":meta["id"],"candidate":candidate,"heard":heard,"words":words,"seconds":len(x)/sr,
         "wpm":meta["wpm"],"target_seconds":meta["target_seconds"],"fit_ratio":meta["fit_ratio"],
         "normalized_word_match":sim,"word_changes":edits,
         "peak":float(abs(x).max()),"rms":float(np.sqrt(np.mean(x*x))),
         "pitch":pitch_wav(x,sr),"pauses":pauses,"script":meta["script"]}
    write_json(AUDIO/"staging_qa"/f"{candidate}.qa.json",out)
    print(f"{candidate}: {out['seconds']:.2f}s / {out['target_seconds']:.2f}, {out['wpm']:.0f} WPM, {out['pitch']}, "
          f"ASR {sim:.3f} {edits}",flush=True)


def crop_request(path,model):
    r=json.loads(path.read_text())
    k=r["candidate"]
    if not CANDIDATE.fullmatch(k):
        raise ValueError("out-of-scope context request")
    stem=AUDIO/"staging"/k
    x,sr=sf.read(stem.with_suffix(".wav"),dtype="float32")
    a,b=float(r["start"]),float(r["end"])
    if not 0<=a<b<=len(x)/sr+.001 or b-a>28:
        raise ValueError("context check must be bounded inside the candidate")
    d=gcd(sr,16000)
    y=resample_poly(x[int(a*sr):int(b*sr)],16000//d,sr//d).astype("float32")
    want=lexical(r["expected"])
    proof=[]
    for beam in (1,3):
        heard,w=asr(model,y,a,beam=beam)
        got=lexical(heard)
        yes=any(got[i:i+len(want)]==want for i in range(len(got)-len(want)+1))
        proof.append(dict(beam=beam,heard=heard,words=w,verified=yes))
        print(f"{path.stem}: beam{beam} {'PASS' if yes else 'CHECK'} {heard}",flush=True)
    write_json(AUDIO/"staging_qa"/f"{path.stem}.context.json",dict(r,proof=proof))

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--only",nargs="+")
    p.add_argument("--device",choices=["cuda","cpu"],default="cuda")
    p.add_argument("--idle-timeout",type=float,default=1800)
    a=p.parse_args()
    (AUDIO/"staging_qa").mkdir(exist_ok=True)
    if a.only and any(not CANDIDATE.fullmatch(k) for k in a.only):p.error("invalid take id")
    last=time.monotonic(); model=None
    while not STOP.exists() and time.monotonic()-last<a.idle_timeout:
        eligible=(a.only if a.only else [p.stem for p in sorted((AUDIO/"staging").glob("*.wav"))])
        ready=[k for k in eligible if CANDIDATE.fullmatch(k)
               and (AUDIO/"staging"/f"{k}.wav").exists()
               and not (AUDIO/"staging_qa"/f"{k}.qa.json").exists()]
        requests=[p for p in sorted((AUDIO/"control").glob("ctx-*.json"))
            if not (AUDIO/"staging_qa"/f"{p.stem}.context.json").exists()] if not a.only else []
        if not ready and not requests:
            if a.only:break
            time.sleep(3);continue
        if model is None:
            model=WhisperModel(str(ASR_MODEL),device=a.device,compute_type="float16" if a.device=="cuda" else "int8",
                cpu_threads=6,local_files_only=True)
        for k in ready:
            check(k,model)
            last=time.monotonic()
        for r in requests:
            try:
                crop_request(r,model)
            except Exception as e:
                print(f"{r.stem}: {type(e).__name__}: {e}",flush=True)
                write_json(AUDIO/"staging_qa"/f"{r.stem}.context.json",dict(error=str(e)))
            last=time.monotonic()

if __name__=="__main__":
    main()
