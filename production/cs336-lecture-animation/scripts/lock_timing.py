#!/usr/bin/env python3
"""Map accepted take readback to the cut's original subtitle strings and named animation cues."""
import argparse
from difflib import SequenceMatcher
import json
import math
from pathlib import Path
import re
import unicodedata

def canonical(s):
    return re.sub(r"[^a-z0-9\u3400-\u9fff]","",unicodedata.normalize("NFKC",s).casefold())

def word_spans(words):
    text=[]; starts=[]; ends=[]; last=0.0
    for item in words:
        chars=canonical(item["word"])
        a,b=float(item["start"]),float(item["end"])
        if not math.isfinite(b) or not math.isfinite(a) or a < last or b < a:
            raise ValueError("ASR words 需要按发声区间排序，单位是秒、相对于该 take")
        last=a
        for j,c in enumerate(chars):
            text.append(c)
            starts.append(a+(b-a)*j/len(chars))
            ends.append(a+(b-a)*(j+1)/len(chars))
    return "".join(text), starts, ends

def find_cue(text,phrase,n):
    pos=-1
    if n<1 or not phrase:
        raise ValueError("锚词不能为空；occurrence 从 1 开始")
    for _ in range(n):
        pos=text.find(phrase,pos+1)
        if pos<0:
            raise ValueError(f"锁定字幕里找不到锚词：{phrase}（第 {n} 次）")
    return pos

def spoken_texts(cards, spoken):
    if not isinstance(spoken,list) or len(spoken)!=len(cards):
        raise ValueError("送读表与本镜字幕必须逐条对应，且顺序相同")
    result=[]
    for i,(sub,item) in enumerate(zip(cards,spoken),1):
        if not isinstance(item,dict) or item.get("sub")!=sub:
            raise ValueError(f"送读表第 {i} 条 sub 与本镜字幕不一致")
        tts=item.get("tts")
        heard=item.get("read",tts)
        if not all(isinstance(s,str) and canonical(s) for s in (tts,heard)):
            raise ValueError(f"送读表第 {i} 条缺可对齐的 tts 或 read")
        result.append(heard)
    return result

def lock(book,row,asr,anchors,offset,spoken=None):
    cards=[x[2] for x in row["captions"]]
    chunks=list(map(canonical,cards if spoken is None else spoken_texts(cards,spoken)))
    if not chunks or any(not s for s in chunks):
        raise ValueError("先给本镜写可读的逐字字幕")
    expected="".join(chunks)
    heard,a,b=word_spans(asr["words"])
    matched={}
    for i,j,n in SequenceMatcher(None,expected,heard,autojunk=False).get_matching_blocks():
        matched.update({i+p:j+p for p in range(n)})
    coverage=len(matched)/len(expected)
    if coverage<.9:
        raise ValueError(f"实际读回只对齐 {coverage:.0%}；先核对读音、漏词和 ASR")
    fps=book["fps"]; total=row["frames"]
    def boundary(i,t,rounder):
        if i not in matched:
            raise ValueError(f"字幕/关键帧边界“{expected[i]}”没在读回里可靠对齐；请听查")
        return offset+rounder(t[matched[i]]*fps)
    at=0; result=[]
    for s,n in zip(cards,chunks):
        start=boundary(at,a,math.floor);end=boundary(at+len(n)-1,b,math.ceil)
        if start>=end or start<0 or end>total:
            raise ValueError(f"本次录音不合锁定时槽：{s} [{start}, {end}) / {total}")
        if result:
            result[-1][1]=min(result[-1][1],start)
            if result[-1][1]<=result[-1][0]:
                raise ValueError("字幕时间重叠，检查读回边界")
        result.append([start,end,s]);at+=len(n)
    cues=dict(row.get("cues",{}))
    measured={}
    for key,mark in anchors.items():
        phrase,n=(mark,1) if isinstance(mark,str) else (mark["phrase"],mark.get("occurrence",1))
        cue=canonical(phrase)
        i=find_cue(expected,cue,n)
        if spoken is not None:
            j=matched.get(i)
            if j is None or any(matched.get(i+k)!=j+k for k in range(len(cue))):
                raise ValueError(f"锚词未完整读回：{key}（{phrase}）；请听核词尾和数字")
        t=boundary(i,a,round)
        if not 0<=t<total:raise ValueError(f"锚点超出本镜：{key}")
        cues[key]=t
        measured[key]=t
    row.update(captions=result,cues=cues)
    if spoken is not None and "beats" in row:
        row["beats"]=[
            {**beat,"wordFrame":measured[beat["cue"]]} if beat["cue"] in measured else beat
            for beat in row["beats"]
        ]
    return coverage

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--cut",required=True,type=Path)
    ap.add_argument("--scene",required=True)
    ap.add_argument("--asr",required=True,type=Path)
    ap.add_argument("--anchors",type=Path,help='镜内锚点，如 {"move":"同时加二"}')
    ap.add_argument("--spoken-cues",type=Path,help="按本镜字幕顺序列出的 sub/tts（可选 read）JSON")
    ap.add_argument("--offset-frames",type=int,default=0,help="录音在镜内的实际入点")
    ap.add_argument("--out",required=True,type=Path)
    a=ap.parse_args()
    if a.out.exists():ap.error("输出用新路径；试听后再采用")
    if a.offset_frames<0:ap.error("镜内入点不能为负")
    read=lambda p:json.loads(p.read_text(encoding="utf-8"))
    data=read(a.cut)
    row=next((s for s in data["scenes"] if s["id"]==a.scene),None)
    if row is None:ap.error(f"镜号不存在：{a.scene}")
    spoken=read(a.spoken_cues) if a.spoken_cues else None
    if a.spoken_cues and not isinstance(spoken,list):ap.error("送读表必须是数组")
    rate=lock(data,row,read(a.asr),read(a.anchors) if a.anchors else {},a.offset_frames,spoken)
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"{row['id']}: {rate:.1%} 字位匹配 · {len(row['captions'])} 条字幕 · 帧数不动")

if __name__=="__main__":
    main()
