#!/usr/bin/env python3
"""Mix already timed stems without changing their common 48 kHz sample clock."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess as sp
import tempfile

def pcm48(path,channels):
    m=json.loads(sp.check_output(["ffprobe","-v","error","-show_streams","-of","json",str(path)]))
    if len(m["streams"])!=1:
        raise ValueError(f"一文件一条 PCM 音轨：{path}")
    a=m["streams"][0]
    if (a.get("channels"),a.get("sample_rate"),a.get("time_base"))!=(channels,"48000","1/48000") or not a["codec_name"].startswith("pcm_"):
        raise ValueError(f"需要 {channels} 声道的 48 kHz PCM WAV：{path}")
    return int(a["duration_ts"])

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dialogue",required=True,type=Path)
    p.add_argument("--score",type=Path)
    p.add_argument("--sfx",type=Path)
    p.add_argument("--music-db",type=float,help="旧混音的 BGM dB（默认 -19）")
    p.add_argument("--profile",choices=("legacy","v2"),default="legacy")
    p.add_argument("--plan",type=Path,help="v2：已对齐的乐章、局部 BGM 窗和提问时刻 JSON")
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args()
    out=a.out.resolve()
    if out.exists() or out.suffix.lower()!=".wav":
        p.error("指定一个新的 WAV")
    n=pcm48(a.dialogue,1)
    files=[a.dialogue,*[p for p in (a.score,a.sfx) if p]]
    if any(pcm48(f,2)!=n for f in files[1:]):
        p.error("人声、连续配乐及音效 stem 都要从 0 起，样本数相同")
    if a.plan and a.profile!="v2":
        p.error("--plan 仅用于 --profile v2")
    if a.profile=="v2" and a.music_db is not None:
        p.error("v2 用固定响度基准与 --plan cuts；--music-db 只用于旧版")
    music_db=-19 if a.music_db is None else a.music_db
    if a.profile=="v2":
        from mix_v2 import stage_mix
        plan=json.loads(a.plan.read_text(encoding="utf-8")) if a.plan else {}
        exe="/usr/bin/ffmpeg" if Path("/usr/bin/ffmpeg").is_file() else shutil.which("ffmpeg")
        print(json.dumps(stage_mix(exe,out,a.dialogue,a.score,a.sfx,n,pcm48,plan),ensure_ascii=False,indent=2))
        return
    args=[]
    for f in files:args+=["-i",str(f.resolve())]
    if a.score:
        graph=("[0:a]asplit=2[v][key];[v]pan=stereo|c0=c0|c1=c0[speech];"
               f"[1:a]volume={music_db}dB[bed];"
               "[bed][key]sidechaincompress=threshold=0.035:ratio=2.6:attack=36:release=580[score];")
        inputs="[speech][score]"
    else:
        graph="[0:a]pan=stereo|c0=c0|c1=c0[speech];"
        inputs="[speech]"
    if a.sfx:
        inputs+=f"[{len(files)-1}:a]"
    filters=(f"amix=inputs={len(files)}:normalize=0:duration=first," if len(files)>1 else "")
    graph+=inputs+filters+"alimiter=limit=0.94:level=false:latency=true[a]"
    exe="/usr/bin/ffmpeg" if Path("/usr/bin/ffmpeg").is_file() else shutil.which("ffmpeg")
    out.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(dir=out.parent,prefix="mix-") as d:
        temp=Path(d)/"screening.wav"
        sp.run([exe,"-v","error","-nostdin",*args,"-filter_complex_threads","1",
                "-filter_complex",graph,"-map","[a]","-c:a","pcm_s24le",str(temp)],check=True)
        if pcm48(temp,2)!=n:
            raise ValueError("混音滤镜改了样本长度；检查 FFMpeg 延迟补偿")
        temp.replace(out)
    print(f"{out} · 样本数 {n} · {n/48000:g} 秒")

if __name__=="__main__":
    main()
