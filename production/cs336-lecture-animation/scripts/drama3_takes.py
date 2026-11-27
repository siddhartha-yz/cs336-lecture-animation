#!/usr/bin/env python3
"""Validate a locked narration queue, or render it on an authorized local Drama 3 runtime."""
import argparse
import json
import os
from pathlib import Path
import re

CUE = re.compile(r"\[[^\[\]\r\n]+\]")
TAKE_ID = re.compile(r"[a-zA-Z0-9][a-zA-Z0-9_-]{0,79}\Z")

def read_queue(path):
    rows = json.loads(path.read_text(encoding="utf-8"))
    seen = set()
    for r in rows:
        k = r["id"]
        if not TAKE_ID.fullmatch(k) or k in seen:
            raise ValueError(f"取样名不合法或重复：{k}")
        seen.add(k)
        text, say = r["text"], r["say"]
        expected = text
        for a,b in r.get("pronunciation",{}).items():
            if not a or a not in expected:
                raise ValueError(f"{k}: 注音原词不在稿内：{a}")
            expected = expected.replace(a,b)
        spoken = CUE.sub("",say)
        if not text.strip() or CUE.search(expected) or "[" in spoken or "]" in spoken or spoken != expected:
            raise ValueError(f"{k}: 去掉表演指令后必须逐字等于原稿（含显式注音别名）")
        if type(r["seed"]) is not int or not 0 < r["top_p"] <= 1 or not 0 < r["temperature"] <= 2:
            raise ValueError(f"{k}: 检查 seed、top_p 和 temperature")
    if not seen:
        raise ValueError("没有意群")
    return rows

def render(rows,a):
    import numpy as np
    import soundfile as sf
    import torch
    from fish_speech.models.text2semantic.inference import (
        decode_to_audio, encode_audio, generate_long, init_model, load_codec_model,
    )
    if json.loads((a.weights/"config.json").read_text())["model_type"]!="fish_omni":
        raise ValueError("只接受 Drama 3 的 fish_omni checkpoint")
    if not torch.cuda.is_available():
        raise ValueError("在有授权 GPU 的 Drama 3 环境内运行")
    transcript=a.ref_text.read_text(encoding="utf-8").strip()
    if not transcript:
        raise ValueError("参考逐字文本不能为空")
    out=a.out.resolve()
    os.umask(0o077)
    out.mkdir(parents=True, exist_ok=False, mode=0o700)
    with torch.inference_mode():
        requested="cuda:0"
        model,decoder=init_model(a.weights,requested,torch.bfloat16,compile=False)
        device=str(model.device)
        codec=load_codec_model(a.codec,device,model.dtype)
        codes=(torch.from_numpy(np.load(a.ref_tokens,allow_pickle=False)) if a.ref_tokens
               else encode_audio(a.ref_audio,codec,device).cpu())
        for r in rows:
            k=r["id"]; text=r["say"]; seed=r["seed"]
            torch.manual_seed(seed)
            torch.cuda.manual_seed(seed)
            max_tokens=max(650,min(1800,200+len(text)*7))
            seq=[]
            for response in generate_long(model=model,device=requested,decode_one_token=decoder,text=text,
                prompt_text=[transcript],prompt_tokens=[codes],num_samples=1,max_new_tokens=max_tokens,
                temperature=r["temperature"],top_p=r["top_p"],top_k=30,single_chunk=True,compile=False):
                if response.action=="sample":
                    seq.append(response.codes)
            if not seq:
                raise ValueError(f"{k}: 未返回语音")
            sample=torch.cat(seq,dim=1)
            if not 2<sample.shape[1]<max_tokens-1:
                raise ValueError(f"{k}: 生成过短或撞到生成上限；检查意群长度")
            audio=decode_to_audio(sample.to(device),codec).float().cpu().numpy()
            if audio.ndim!=1 or not np.isfinite(audio).all() or not audio.size:
                raise ValueError(f"{k}: WAV 样本异常")
            temp=out/(k+".part.wav")
            sf.write(temp,audio,codec.sample_rate,subtype="PCM_16")
            temp.replace(out/(k+".wav"))
            print(k,round(len(audio)/codec.sample_rate,3),"s",flush=True)
    (out/"takes.json").write_text(json.dumps(rows,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

def main():
    p=argparse.ArgumentParser(description=__doc__)
    s=p.add_subparsers(dest="command",required=True)
    ck=s.add_parser("check");ck.add_argument("queue",type=Path)
    run=s.add_parser("render");run.add_argument("queue",type=Path)
    for flag in ("weights","codec","ref-text","out"):
        run.add_argument("--"+flag,required=True,type=Path)
    refs=run.add_mutually_exclusive_group(required=True)
    refs.add_argument("--ref-audio",type=Path);refs.add_argument("--ref-tokens",type=Path)
    a=p.parse_args()
    rows=read_queue(a.queue)
    if a.command=="check":
        print(f"{len(rows)} 个 Drama 3 意群：原稿锁和读音别名通过")
    else:
        for x in (a.codec,a.ref_text,a.ref_audio or a.ref_tokens):
            if not x.is_file():p.error(f"缺本地输入：{x}")
        render(rows,a)

if __name__=="__main__":
    main()
