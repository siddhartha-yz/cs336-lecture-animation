#!/usr/bin/env python3
"""Read back a selected take with a supplied offline faster-whisper checkpoint."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess

def validate_model(directory,language):
    names=("tokenizer.json","vocabulary.json","preprocessor_config.json")
    missing=[name for name in names if not (directory/name).is_file()]
    if missing:
        raise ValueError("本地 ASR 检查点不完整：缺 "+", ".join(missing)+"；从同一模型修订补齐")
    try:
        vocabulary=json.loads((directory/"vocabulary.json").read_text(encoding="utf-8"))
        added=json.loads((directory/"tokenizer.json").read_text(encoding="utf-8"))["added_tokens"]
        ids={x["content"]:x["id"] for x in added}
    except (ValueError, TypeError, KeyError) as exc:
        raise ValueError("不能读取本地 ASR tokenizer / vocabulary") from exc
    controls=["<|translate|>","<|transcribe|>","<|notimestamps|>","<|0.00|>"]
    if language=="zh":
        controls.append("<|zh|>")
    for mark in controls:
        i=ids.get(mark)
        if not (isinstance(vocabulary,list) and isinstance(i,int) and 0<=i<len(vocabulary) and vocabulary[i]==mark):
            raise ValueError(f"ASR tokenizer 与模型词表不匹配：{mark}；不可用 tiny 的 tokenizer 补 large-v3")

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("wav",type=Path)
    p.add_argument("--model",required=True,type=Path,help="已装的 CTranslate2 模型目录")
    p.add_argument("--language",choices=("zh","en"),default="zh")
    p.add_argument("--device",choices=("cpu","cuda"),default="cpu")
    p.add_argument("--strict-model",action="store_true",help="拒绝不完整或词表不匹配的本地模型，禁止隐式回退到 tiny tokenizer")
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args()
    if not a.wav.is_file() or not (a.model/"model.bin").is_file() or a.out.exists():
        p.error("需要本地 take、已有模型目录，以及一个新输出路径")
    if a.strict_model:
        try:
            validate_model(a.model,a.language)
        except ValueError as e:
            p.error(str(e))
    import numpy as np
    from faster_whisper import WhisperModel
    from opencc import OpenCC
    # Decode explicitly, as in the original waveform-first readback. This
    # keeps the ASR's transient PyAV API from being part of the edit contract.
    ff="/usr/bin/ffmpeg" if Path("/usr/bin/ffmpeg").is_file() else shutil.which("ffmpeg")
    data=subprocess.check_output([ff,"-v","error","-nostdin","-threads","1","-i",str(a.wav),
            "-map","0:a:0","-ac","1","-ar","16000","-c:a","pcm_f32le","-f","f32le","pipe:1"])
    audio=np.frombuffer(data,dtype="<f4")
    if not audio.size:
        raise ValueError("输入没有采样")
    model=WhisperModel(str(a.model),device=a.device,
                       compute_type="int8" if a.device=="cpu" else "float16",
                       cpu_threads=3,local_files_only=True)
    lines,_=model.transcribe(audio,language=a.language,beam_size=5,word_timestamps=True,
          temperature=0,condition_on_previous_text=False,vad_filter=False)
    convert=OpenCC("t2s").convert if a.language=="zh" else str
    words=[dict(word=convert(w.word),start=round(w.start,3),end=round(w.end,3))
        for s in lines for w in s.words or []]
    if not words:
        raise ValueError("未读出词；检查长静音、采样或所选 take")
    a.out.parent.mkdir(parents=True,exist_ok=True)
    with a.out.open("x",encoding="utf-8") as f:
        json.dump(dict(words=words,heard="".join(r["word"]for r in words)),f,ensure_ascii=False,indent=2)
        f.write("\n")
    print(f"{len(words)} 个有时间戳的词段 · {a.out}")

if __name__=="__main__":
    main()
