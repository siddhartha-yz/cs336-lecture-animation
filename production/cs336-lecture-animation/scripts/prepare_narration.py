#!/usr/bin/env python3
"""Check a v2 sub/tts cue sheet and compile local Drama 3 takes without changing the script."""
import argparse
import json
import math
from pathlib import Path
import re

DIRECTION = {
    "E1": "悬念慢慢抬起来，问句留给观众想一下",
    "E2": "像给同行指一眼黑板，轻快，笑意很浅",
    "E3": "讲清因果和数值，别抢，留自然断句",
    "E4": "转折利落，落在看见的变化上",
    "E5": "沉静收住，让最后几个字落稳",
}
ID = re.compile(r"[a-zA-Z0-9][a-zA-Z0-9_-]{0,69}\Z")
LATEX = re.compile(r"\\[a-zA-Z]+|\$|\b[prv]\([^)]*_[^)]*\)")
META = re.compile(r"教学示意|教学算例|教学例|读图约值|不按比例|核心结论|本节小结|关键洞察|示意图形|来源口径|复剪包|讲义|课程幻灯|课堂举例|\bSlide\b")
RISK = {
    "估抖": "估不准，或估值容易抖动",
    "拒答": "拒绝回答",
    "老实给出": "干脆给出，或老老实实给出",
    "卡在": "拦在或堵在",
}
HAN = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\U00020000-\U0002ffff\U00030000-\U000323af]")
NATIVE_HAN_PER_MIN = (230, 250)

def prepare(rows):
    if not isinstance(rows,list) or not rows:
        raise ValueError("需要非空的意群数组")
    ids=set()
    for r in rows:
        name,sub,tts,emotion=(r[k] for k in ("id","sub","tts","emotion"))
        n,kind=r.get("N",1),r.get("kind","prose")
        if not ID.fullmatch(name) or name in ids:
            raise ValueError(f"{name}: 意群 id 重复或不能用于文件名")
        ids.add(name)
        if not sub.strip() or not tts.strip() or any(c in tts for c in "[]；;_") or LATEX.search(sub) or LATEX.search(tts):
            raise ValueError(f"{name}: sub/tts 要有正文，送读不用括注、分号、下划线或公式源码")
        if META.search(sub) or META.search(tts):
            raise ValueError(f"{name}: 删除制作标签")
        if kind not in ("prose","number","question","reveal") or emotion not in DIRECTION:
            raise ValueError(f"{name}: 检查意群类型与 E1–E5")
        if type(n) is not int or not 1<=n<=4 or (kind in ("question","reveal") and n!=4):
            raise ValueError(f"{name}: 普通 1–4 遍；核心问句/大反转 4 遍后人工取")
        if kind=="question" and not sub.endswith("？"):
            raise ValueError(f"{name}: 屏幕问句用全角问号")
        for word,better in RISK.items():
            if word in tts:
                raise ValueError(f"{name}: tts「{word}」改读「{better}」")
        if re.search(r"(?:^|[，。！？“])沸水(?:[，。！？”]|$)(?!这个词)",tts):
            raise ValueError(f"{name}: 孤立词元用「沸水这个词」")
        if "π" in sub and ("派" not in tts or "π" in tts):
            raise ValueError(f"{name}: π 写作派")
        if re.search(r"G\s*[-–—]\s*V",sub,re.I) and not re.search(r"G[，,]\s*V[，,。]",tts,re.I):
            raise ValueError(f"{name}: G-V 拆成「G，V，」")
        if "前缀和" in tts and re.search(r"前缀和\s*(?:C U|cu)",tts,re.I):
            raise ValueError(f"{name}: 前缀和后补逗号和「也就是」")
        seed=r.get("seed")
        if type(seed) is not int or not 0<=seed<2**31-4:
            raise ValueError(f"{name}: 用明确的非负整数 seed 记录复选")
        for k in range(n):
            yield {
                "id":f"{name}-t{k+1}","text":tts,"say":f"[{DIRECTION[emotion]}。]{tts}",
                "seed":seed+k,"temperature":r.get("temperature",0.80),
                "top_p":r.get("top_p",0.85),"sub":sub,"cue":name,"emotion":emotion,
            }

def voice_budget(rows, max_minutes, reserved_seconds):
    limit = max_minutes * 60
    if not (math.isfinite(limit) and math.isfinite(reserved_seconds)
            and 0 <= reserved_seconds < limit):
        raise ValueError("片长上限必须大于已预留的非旁白秒数，两者都用有限值")
    # Budget the delivery text once per cue, never once per candidate.
    count = sum(len(HAN.findall(row["tts"])) for row in rows)
    slow, fast = NATIVE_HAN_PER_MIN
    capacity = math.floor((limit - reserved_seconds) * fast / 60)
    return count, capacity, (reserved_seconds + count * 60 / fast,
                              reserved_seconds + count * 60 / slow)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("script",type=Path)
    p.add_argument("--out",type=Path)
    p.add_argument("--max-minutes",type=float,help="按 v2 原生语速估算，输入成片时长上限（分钟）")
    p.add_argument("--reserve-seconds",type=float,help="其中留给片头、章门、净切、思考与片尾的非旁白秒数")
    a=p.parse_args()
    if (a.max_minutes is None) != (a.reserve_seconds is None):
        p.error("--max-minutes 与 --reserve-seconds 一起使用")
    narration=json.loads(a.script.read_text(encoding="utf-8"))
    rows=list(prepare(narration))
    if a.max_minutes is not None:
        try:
            count, capacity, (fast, slow) = voice_budget(narration,a.max_minutes,a.reserve_seconds)
        except ValueError as e:
            p.error(str(e))
        print(f"送读 {count} 汉字 · 预留 {a.reserve_seconds:g} 秒 · 230–250 字/分对应 {fast/60:.2f}–{slow/60:.2f} 分钟")
        print(f"250 字/分时最多 {capacity} 汉字；"
              + (f"需去掉至少 {count-capacity} 个汉字才合上限。" if count > capacity else "汉字账面在上限以内。")
              + "仅计送读汉字，数字请先展开；实录后重算。")
    if a.out:
        a.out.parent.mkdir(parents=True,exist_ok=True)
        with a.out.open("x",encoding="utf-8") as f:
            json.dump(rows,f,ensure_ascii=False,indent=2)
            f.write("\n")
    print(f"{len(rows)} 个已校验候选 · {len({r['cue'] for r in rows})} 个意群")

if __name__=="__main__":
    main()
