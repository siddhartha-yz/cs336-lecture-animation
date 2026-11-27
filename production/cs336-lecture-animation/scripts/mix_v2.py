"""V2 mix from three already aligned stems. No sound generation or networking."""
import json
import math
from pathlib import Path
import re
import statistics
import subprocess as sp
import tempfile

def run(exe,args):
    return sp.run([exe,"-hide_banner","-nostdin",*args],check=True,capture_output=True,text=True)

def meter(exe,path):
    log=run(exe,["-i",str(path),"-vn","-af","loudnorm=print_format=json","-f","null","-"]).stderr
    p=re.search(r'\{\s*"input_i"[^}]+\}',log)
    if not p:
        raise ValueError(f"FFmpeg 未返回 LUFS: {path}")
    m=json.loads(p[0])
    level=float(m["input_i"])
    if not math.isfinite(level):
        raise ValueError(f"无法归一化空音轨：{path}")
    return level,float(m["input_tp"])

def integrated(exe,path):
    return meter(exe,path)[0]

def short_lufs(exe,path):
    # EBU short term = 3 s. Use the centre of each measurement window.
    log=run(exe,["-i",str(path),"-vn","-af","ebur128=metadata=1,ametadata=mode=print:key=lavfi.r128.S",
                 "-f","null","-"]).stderr
    rows=[]
    for p in re.finditer(r"pts_time:([\d.]+)\s*\n[^\n]*lavfi\.r128\.S=(-?[\d.]+)",log):
        t,v=map(float,p.groups())
        if t>=3 and v>-80:
            rows.append((t-1.5,v))
    if not rows:
        raise ValueError("无法读取音乐短时响度")
    return rows

def merge(ranges):
    out=[]
    for a,b in sorted(ranges):
        if out and a<=out[-1][1]+.001:
            out[-1][1]=max(b,out[-1][1])
        else:
            out.append([a,b])
    return out

def inspect(exe,file,movements,duration):
    data=short_lufs(exe,file);report=[];cuts=[]
    for item in movements:
        a,b=map(float,(item["start"],item["end"]))
        first=float(item.get("measureFrom",a))
        if not 0<=a<=first<b<=duration+.002:
            raise ValueError(f"乐章区间错误：{item}")
        z=first;base=None
        while b-z>=8:
            e=min(z+30,b)
            vals=[v for t,v in data if z+.5<=t<e-.5]
            if vals:
                m=statistics.median(vals)
                if base is None:
                    base=m
                drift=m-base
                report.append({"start":z,"end":e,"shortLUFS":round(m,2),"risesBy":round(drift,2)})
                if drift>2.5:
                    cuts.append([z,e])
            z=e
    return report,merge(cuts)

def ramp(a,b):
    return f"(0.5-0.5*cos(PI*clip((t-({a:.6f}))/({b-a:.6f}),0,1)))"

def window(a,b,attack=2,release=2):
    return f"({ramp(a-attack,a)}*(1-{ramp(b,b+release)}))"

def maximum(xs):
    p="0"
    for q in xs:
        p=f"max({p},{q})"
    return p

def stage_mix(exe,out,dialogue,score,sfx,n,pcm48,plan):
    duration=n/48000
    plan=plan or {}
    if "lastVoice" in plan and not 3.5<=duration-float(plan["lastVoice"])<=4.0:
        raise ValueError("用实测末字后留 3.5–4.0s，而不是追加空音频")
    speech_input=integrated(exe,dialogue)
    speech_db=-16-speech_input
    use=[dialogue]
    filters=[f"[0:a]volume={speech_db:.6f}dB,asplit=2[key][voice]" if score else
             f"[0:a]volume={speech_db:.6f}dB[voice]",
             "[voice]pan=stereo|c0=0.70710678*c0|c1=0.70710678*c0[speech]"]
    labels=["[speech]"]
    results={"seconds":duration,"dialogueInputLUFS":speech_input,"dialogueTrimDB":speech_db}
    if score:
        use.append(score)
        movements=plan.get("movements") or [{"start":0,"end":duration}]
        windows,auto=inspect(exe,score,movements,duration)
        applied=[(a,b,-3.5) for a,b in auto]
        for row in plan.get("cuts",[]):
            a,b,db=map(float,(row["start"],row["end"],row["db"]))
            if not 0<=a<b<=duration or not -4<=db<=-2.5:
                raise ValueError("人工 BGM 窗要在成片内、-2.5 至 -4 dB")
            applied.append((a,b,db))
        gain=-33.5-integrated(exe,score)
        low=maximum([window(a,b) for a,b,_ in applied])
        local=maximum([f"({-db:.4f}*{window(a,b)})" for a,b,db in applied])
        ducks=[]
        for q in plan.get("questions",[]):
            a,b=map(float,(q["start"],q["end"]))
            if not 0<=a<b<=duration or b+.15>duration:
                raise ValueError("提问窗时间错误")
            ducks.append(window(a,b+.15,2,2.5))
        qgain=maximum(ducks)
        filters.extend([
            "[1:a]equalizer=f=2500:t=q:w=1:g=-3,asplit=2[direct][lowin]",
            "[lowin]bass=f=120:t=q:w=0.7:g=-2[bass]",
            f"[direct]volume='1-({low})':eval=frame[d]",
            f"[bass]volume='{low}':eval=frame[l]",
            f"[d][l]amix=inputs=2:normalize=0,volume='pow(10,({gain:.6f}-({local})-6*({qgain}))/20)':eval=frame[bed]",
            # 22% wet bounds peak reduction of the score to about 2.16 dB.
            "[bed][key]sidechaincompress=threshold=0.022:ratio=3:attack=30:release=250:mix=0.22[score]",
        ])
        labels.append("[score]")
        results.update(scoreTrimDB=gain,windows=windows,autoLowShelfCuts=auto,applied=applied)
    if sfx:
        idx=len(use);use.append(sfx)
        filters.append(f"[{idx}:a]volume=-12dB[sfx]")
        labels.append("[sfx]")
    mix="".join(labels)
    mix+=(f"amix=inputs={len(labels)}:normalize=0:duration=first," if len(labels)>1 else "")
    filters.append(mix+"alimiter=limit=0.89:level=false:latency=true[out]")
    args=[]
    for f in use:
        args+=["-i",str(f.resolve())]
    out.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(dir=out.parent,prefix="v2-mix-") as d:
        temp=Path(d)/"screening.wav"
        sp.run([exe,"-v","error","-nostdin",*args,"-filter_complex_threads","1","-filter_complex",";".join(filters),
                "-map","[out]","-c:a","pcm_s24le",str(temp)],check=True)
        if pcm48(temp,2)!=n:
            raise ValueError("v2 混音改变了采样数")
        results["mixLUFS"],results["mixTruePeakDBTP"]=meter(exe,temp)
        temp.replace(out)
    return results
