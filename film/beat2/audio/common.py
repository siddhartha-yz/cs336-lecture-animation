from pathlib import Path
import json
import re

AUDIO=Path(__file__).resolve().parent
SCRIPT=AUDIO.parent
SCENES="ghijk"
CANDIDATE=re.compile(r"^[g-k](?:-r[1-9][0-9]*)?$")
VOICE=(
    "Warm adult American English male speaking to a few students, not projecting into a hall. Begin "
    "conversationally, and let an unexpected fact change the voice naturally: brief curiosity, "
    "then a lucid explanation. Use distinct logical stresses and connected sentences. Maintain an easy, measured teaching pace, brisk but unhurried. "
    "Keep momentum through sentences with ordinary breathing room around the main question; about 165 words per minute. "
    "Thoughtful rather than an announcer."
)
ALIASES=(
    (r"\bUTF(?:[-‑–]eight|[-‑–]?8)\b", "you tee eff eight"),
    (r"\bWikiText[‑–-]?103\b", "Wiki Text one oh three"),
    (r"\bWikiText\b", "Wiki Text"),
    (r"\blogits\b", "low-jits"),
    (r"\bGPT[‑–-]?2\b", "G P T two"),
    (r"\bBPB\b", "B P B"),
    (r"\bPPL\b", "P P L"),
)

def write_json(path, data):
    p=path.with_suffix(path.suffix+".partial")
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n")
    p.replace(path)

def script_row(key):
    p=SCRIPT/f"script_{key}.json"
    obj=json.loads(p.read_text())
    if not isinstance(obj,dict) or obj.get("id",key)!=key:
        raise ValueError(f"{p.name}: expected one object for {key}")
    parts=obj["parts"]
    if not parts or any(len(part)!=2 or not all(isinstance(t,str) and t.strip() for t in part) for part in parts):
        raise ValueError(f"{p.name}: each part must have English and Chinese")
    en=" ".join(part[0].strip() for part in parts)
    originally_spoken=en
    for pattern, replacement in ALIASES:
        en=re.sub(pattern,replacement,en,flags=re.I)
    duration=float(obj["duration"])
    hold=float(obj.get("hold",0))
    direction=obj.get("voice_direction",obj.get("direction","")) or ""
    if not isinstance(direction,str):
        raise ValueError(f"{p.name}: voice direction must be text")
    if not (3<=duration-hold<=105 and 0<=hold<duration):
        raise ValueError(f"{p.name}: unusable duration / hold")
    return obj, originally_spoken, en, duration-hold, direction.strip()
