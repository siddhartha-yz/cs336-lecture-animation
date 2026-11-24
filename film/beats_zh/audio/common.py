from pathlib import Path
import json,re

AUDIO=Path(__file__).resolve().parent
SCRIPT=AUDIO.parent
SCENES="abcdef"
CANDIDATE=re.compile(r"^[a-f](?:-r[1-9][0-9]*)?$")
VOICE=(
    "年轻到中年的中文大学老师，普通话清楚，面对几位学生自然地讲。"
    "声线温暖明亮，带着一点好奇。用语气自然突出真正的转折，句内连贯。"
    "像在黑板边讲，不像朗诵、新闻播报或广告。语速自然稍快，别拖尾，不要逐字念。"
)
ALIASES=(
    (r"(?<![a-z0-9])H100(?![a-z0-9])", " H 一百 "),
    (r"(?<![0-9.])3\.28(?![0-9.])", "三点二八"),
    (r"(?<![a-z0-9])Elo(?![a-z0-9])", " E-low "),
    (r"(?<![a-z0-9])OpenRouter(?![a-z0-9])", " Open Router "),
    (r"(?<![a-z0-9])Karpathy(?![a-z0-9])", "卡帕西"),
    (r"(?<![a-z0-9])NanoGPT(?![a-z0-9])", " Nano G P T "),
    (r"(?<![a-z0-9])FineWeb(?![a-z0-9])", " Fine Web "),
    (r"(?<![a-z0-9])SQuAD(?![a-z0-9])", " Squad "),
    (r"(?<![a-z0-9])GPUs?(?![a-z0-9])", " G P U "),
    (r"(?<![a-z0-9])GPT[‑–-]?6(?![a-z0-9])", " G P T 六 "),
)

def write_json(path,data):
    p=path.with_suffix(path.suffix+".partial")
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n")
    p.replace(path)

def script_row(key):
    p=SCRIPT/f"script_{key}.json"
    obj=json.loads(p.read_text())
    if not isinstance(obj,dict) or obj.get("id",key)!=key:
        raise ValueError(f"{p.name}: expected one object for {key}")
    parts=obj["parts"]
    if not parts or any(not isinstance(x,str) or not x.strip() for x in parts):
        raise ValueError(f"{p.name}: expected Chinese text parts")
    text=obj.get("text") or "".join(x.strip() for x in parts)
    raw=obj.get("spoken") or text
    for pattern,replacement in ALIASES:
        raw=re.sub(pattern,replacement,raw,flags=re.I)
    # Text/numbers untouched; suppress visual marker if explicitly present.
    raw=re.sub(r"[\u200b\ufeff]","",raw)
    duration=float(obj["duration"])
    hold=float(obj.get("hold",0))
    direction=obj.get("voice_direction",obj.get("direction","")) or ""
    if not isinstance(direction,str) or not (3<=duration-hold<=105 and 0<=hold<duration):
        raise ValueError(f"{p.name}: invalid direction or timing")
    return obj,text,raw,duration-hold,direction.strip()

def candidate_spoken(key, raw):
    if key == "f-r2":
        raw=raw.replace("Fine Web","Fyne Web").replace("\n"," ")
        raw=raw.replace("条件固定下来。", "条件固定下来，").replace("，由你。", "，由你；")
    return raw
