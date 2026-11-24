#!/usr/bin/env python3
"""Persistent whole-scene Aiden synthesis; stage WAVs for word QA before publishing."""
import argparse
import os
import json
from pathlib import Path
import time

os.environ["HF_HUB_OFFLINE"]="1"
os.environ["TOKENIZERS_PARALLELISM"]="false"
import numpy as np
import soundfile as sf
import torch
from faster_qwen3_tts import FasterQwen3TTS
from common import AUDIO, CANDIDATE, SCENES, SCRIPT, VOICE, script_row, write_json

WEIGHTS=os.environ["QWEN_TTS_MODEL"]
STOP=AUDIO/"control"/"stop-synthesis"

def generate(model,candidate):
    key=candidate[0]
    obj, text, spoken, target, direction=script_row(key)
    suffix=0 if candidate==key else int(candidate.split("-r",1)[1])
    seed=20249 + (ord(key)-ord("a"))*127 + 1229*suffix
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    full_direction=VOICE + (" " + direction if direction else "")
    if candidate == "h-r1":
        full_direction += (" Pronounce the encoding name as the four distinct sounds you, tee, eff, eight. "
            "Continue at an active natural pace; lightly stress only the cuts move and same denominator, with short connected pauses.")
    if candidate == "j-r1":
        full_direction += (" Pronounce Paloma as puh-LOH-muh, flowing as a single name, and low-jits as a single term. "
            "Build momentum toward the actual model line with distinct thought groups but connected sentences.")
    started=time.monotonic()
    max_new_tokens=min(1800, round((target+22)*12.5))
    print(f"{candidate}: synthesizing {len(spoken.split())} words for a {target:.2f}s speech slot",flush=True)
    waves, rate=model.generate_custom_voice(
        text=spoken,speaker="Aiden",language="English",instruct=full_direction,
        max_new_tokens=max_new_tokens,temperature=.72,repetition_penalty=1.08,
    )
    if len(waves)!=1:
        raise RuntimeError(f"{candidate}: engine yielded more than one take")
    x=np.asarray(waves[0],dtype="float32")
    if x.ndim!=1 or not np.isfinite(x).all():
        raise RuntimeError(f"{candidate}: unexpected waveform")
    if len(x)/rate > (max_new_tokens-8)/12.5:
        raise RuntimeError(f"{candidate}: may have hit its speech-token limit")
    nz=np.flatnonzero(abs(x)>.007)
    if not len(nz):
        raise RuntimeError(f"{candidate}: silent take")
    # Trim only the leading/trailing dead edges, not any gap within the take.
    x=x[max(0,nz[0]-round(.04*rate)):min(len(x),nz[-1]+round(.10*rate))]
    peak=float(abs(x).max())
    if peak>.99:
        x=x*(.97/peak)
    stem=AUDIO/"staging"/candidate
    w=stem.with_suffix(".wav")
    pending=w.with_suffix(".pending.wav")
    sf.write(pending,x,rate,subtype="PCM_24")
    elapsed=len(x)/rate
    m={"engine":"Qwen3-TTS 12Hz 1.7B CustomVoice (local)", "character":"Aiden", "original_preset":True,
       "id":key, "candidate":candidate, "script":f"script_{key}.json", "text":text,"raw":spoken,
       "seconds":elapsed,"target_seconds":target,"fit_ratio":elapsed/target,
       "wpm":len(spoken.split())*60/elapsed,"sample_rate":rate,"seed":seed,
       "direction":full_direction,"synthesis_seconds":time.monotonic()-started}
    write_json(stem.with_suffix(".json"),m)
    pending.replace(w)
    print(f"{candidate}: {elapsed:.2f}s / {target:.2f}s ({m['wpm']:.0f} WPM, {m['synthesis_seconds']:.1f}s generation)",flush=True)
    return m

def tasks(only):
    if only:
        return only
    requested=[p.stem for p in sorted((AUDIO/"control").glob("?-r*.request"))]
    return list(dict.fromkeys(requested+list(SCENES)))

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--only",nargs="+",help="process specific draft or retake IDs and exit")
    p.add_argument("--idle-timeout",type=float,default=1800)
    a=p.parse_args()
    (AUDIO/"staging").mkdir(exist_ok=True)
    if a.only and any(not CANDIDATE.fullmatch(k) for k in a.only):
        p.error("invalid take identifier")
    if a.only and any(not (SCRIPT/f"script_{k[0]}.json").is_file() for k in a.only):
        p.error("a requested script is missing")
    torch.set_num_threads(4)
    print("Loading local Aiden weights on CUDA …",flush=True)
    model=FasterQwen3TTS.from_pretrained(
        WEIGHTS,device="cuda:0",dtype=torch.bfloat16,attn_implementation="sdpa",local_files_only=True)
    print("Aiden loaded; awaiting final scene JSON",flush=True)
    last=time.monotonic()
    failed=set()
    while not STOP.exists() and time.monotonic()-last<a.idle_timeout:
        ready=[]
        for k in tasks(a.only):
            if not CANDIDATE.fullmatch(k) or k in failed or (AUDIO/"staging"/f"{k}.wav").exists():
                continue
            if (SCRIPT/f"script_{k[0]}.json").is_file():
                try:
                    script_row(k[0])
                except (FileNotFoundError,json.JSONDecodeError):
                    continue
                except Exception as e:
                    print(f"{k}: script rejected: {type(e).__name__}: {e}",flush=True)
                    failed.add(k); continue
                ready.append(k)
        if not ready:
            if a.only:
                break
            time.sleep(3)
            continue
        for k in ready:
            try:
                generate(model,k)
            except Exception as e:
                if a.only: raise
                print(f"{k}: synthesis failed: {type(e).__name__}: {e}",flush=True)
                failed.add(k)
            last=time.monotonic()

if __name__=="__main__":
    main()
