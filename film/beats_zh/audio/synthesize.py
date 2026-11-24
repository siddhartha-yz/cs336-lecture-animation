#!/usr/bin/env python3
"""Persistent whole-scene Mandarin synthesis; stage WAVs for word QA before publishing."""
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
from common import AUDIO, CANDIDATE, SCENES, SCRIPT, VOICE, candidate_spoken, script_row, write_json

WEIGHTS=os.environ["QWEN_TTS_MODEL"]
STOP=AUDIO/"control"/"stop-synthesis"

def generate(model,candidate):
    key=candidate[0]
    obj, text, spoken, target, direction=script_row(key)
    spoken=candidate_spoken(candidate,spoken)
    suffix=0 if candidate==key else int(candidate.split("-r",1)[1])
    seed=20249 + (ord(key)-ord("a"))*127 + 1229*suffix
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    full_direction=VOICE + (" " + direction if direction else "")
    selection = AUDIO / "control" / "speaker.txt"
    if not selection.is_file():
        raise ValueError("speaker is not selected")
    speaker = selection.read_text().strip()
    override = AUDIO/"control"/f"speaker-{candidate}.txt"
    if override.is_file():
        speaker = override.read_text().strip()
    direction_override=AUDIO/"control"/f"direction-{candidate}.txt"
    if direction_override.is_file():
        full_direction += " " + direction_override.read_text().strip()
    started=time.monotonic()
    max_new_tokens=min(1800, round((target+32)*12.5))
    print(f"{candidate}: synthesizing {len([x for x in spoken if x.isalnum()])} characters for a {target:.2f}s speech slot",flush=True)
    waves, rate=model.generate_custom_voice(
        text=spoken,speaker=speaker,language="Chinese",instruct=full_direction,
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
    m={"engine":"Qwen3-TTS 12Hz 1.7B CustomVoice (local)", "character":speaker, "original_preset":True,
       "id":key, "candidate":candidate, "script":f"script_{key}.json", "text":text,"raw":spoken,
       "seconds":elapsed,"target_seconds":target,"fit_ratio":elapsed/target,
       "wpm":len([x for x in spoken if x.isalnum()])*60/elapsed,"sample_rate":rate,"seed":seed,
       "direction":full_direction,"synthesis_seconds":time.monotonic()-started}
    write_json(stem.with_suffix(".json"),m)
    pending.replace(w)
    print(f"{candidate}: {elapsed:.2f}s / {target:.2f}s ({m['wpm']:.0f} CPM, {m['synthesis_seconds']:.1f}s generation)",flush=True)
    return m

def tasks(only):
    if only:
        return only
    requested=[p.stem for p in sorted((AUDIO/"control").glob("?-r*.request"))]
    return list(dict.fromkeys(requested+list(SCENES)))

def take_sample(model, sample, done):
    for speaker in sample["speakers"]:
        if speaker in done or (AUDIO/"staging"/f"sample-{speaker}.wav").is_file(): continue
        torch.manual_seed(42917)
        torch.cuda.manual_seed(42917)
        t=time.monotonic()
        wav, rate=model.generate_custom_voice(text=sample["text"],speaker=speaker,language="Chinese",
            instruct=VOICE,max_new_tokens=180,temperature=.70,repetition_penalty=1.08)
        x=np.asarray(wav[0],dtype="float32")
        take=AUDIO/"staging"/f"sample-{speaker}.wav"
        sf.write(take.with_suffix(".tmp.wav"),x,rate,subtype="PCM_24")
        take.with_suffix(".tmp.wav").replace(take)
        done.add(speaker)
        print(f"{speaker} audition: {len(x)/rate:.2f}s in {time.monotonic()-t:.1f}s",flush=True)

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
    print("Loading local Mandarin CustomVoice weights on CUDA …",flush=True)
    model=FasterQwen3TTS.from_pretrained(
        WEIGHTS,device="cuda:0",dtype=torch.bfloat16,attn_implementation="sdpa",local_files_only=True)
    print("Mandarin model loaded; awaiting final scene JSON",flush=True)
    last=time.monotonic()
    failed=set()
    auditions_done=set()
    while not STOP.exists() and time.monotonic()-last<a.idle_timeout:
        audition_path=AUDIO/"control"/"audition.json"
        if audition_path.is_file():
            sample=json.loads(audition_path.read_text())
            take_sample(model,sample,auditions_done)
        if not (AUDIO/"control"/"speaker.txt").is_file():
            time.sleep(.6)
            continue
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
            time.sleep(.65)
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
