#!/usr/bin/env python3
"""Prepare a lecture intake and a native Remotion project; no GPU work is started."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import sys

from score import read, validate as check_score, MODEL

ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / "production/cs336-lecture-animation"
EXAMPLE = ROOT / "pipeline/example-intake"
IDENT = re.compile(r"l([1-9]\d*)(?:-(upper|lower))?\Z")
FORMATS = {"engineering": (16, 20), "derivation": (22, 26)}


def lecture_number(ident):
    m = IDENT.fullmatch(ident)
    if not m:
        raise ValueError("讲次号使用 l16、l15-upper 或 l15-lower")
    return int(m[1])


def script(name, *args):
    subprocess.run([sys.executable, str(KIT / "scripts" / name), *map(str, args)], check=True)


def put(dir, name, content):
    with (dir / name).open("x", encoding="utf-8") as f:
        f.write(content if isinstance(content, str) else json.dumps(content,ensure_ascii=False,indent=2)+"\n")


def new(ident, dir, title, format):
    k = lecture_number(ident)
    if not title.strip():
        raise ValueError("片名不能为空")
    dir.mkdir(exist_ok=False)
    put(dir,"brief.json",{"id":ident,"lecture":k,"title":title,"format":format,
        "fps":60,"voice":"科普声音","status":"draft"})
    put(dir,"narration.json",[])
    put(dir,"storyboard.md","# 分镜\n\n按意群号写真实物件、动作、停顿、切点与来源。\n")
    put(dir,"sources.md","# 资料来源\n\n记原讲义、论文、数据和素材许可。\n")
    put(dir,"music.json",{"model":MODEL,"global_musical_key":"","tracks":[]})
    print(dir)


def check(ident, dir, draft_ok=False):
    k = lecture_number(ident)
    b = read(dir/"brief.json")
    if (b.get("id")!=ident or b.get("lecture")!=k or not str(b.get("title","")).strip()
        or b.get("format") not in FORMATS or b.get("fps")!=60 or b.get("voice")!="科普声音"):
        raise ValueError(f"{ident}: 检查 brief 的讲次、片名、类型、60fps 与音色")
    for name in ("narration.json","storyboard.md","sources.md","music.json"):
        if not (dir/name).is_file():
            raise ValueError(f"{ident}: 缺 {name}")
    if b.get("status")=="draft" and draft_ok:
        print(f"{ident}: 待交稿，不制作")
        return None
    if b.get("status")!="ready":
        raise ValueError(f"{ident}: 先完成资料并标 brief 的 status 为 ready")
    for name in ("storyboard.md","sources.md"):
        doc=(dir/name).read_text(encoding="utf-8")
        if not any(x.strip() and not x.lstrip().startswith("#") for x in doc.splitlines()[1:]):
            raise ValueError(f"{ident}: {name} 没有正文")
    check_score(read(dir/"music.json"))
    script("prepare_narration.py", dir/"narration.json")
    print(f"{ident}: 源稿准备完成")
    return b


def main():
    p=argparse.ArgumentParser(description=__doc__)
    rs=p.add_subparsers(dest="action",required=True)
    for act in ("new","check","bootstrap","voice-queue","check-all"):
        c=rs.add_parser(act)
        if act!="check-all":
            c.add_argument("id")
        if act=="new":
            c.add_argument("--title",required=True)
            c.add_argument("--format",choices=FORMATS,required=True)
        if act=="voice-queue":
            c.add_argument("--out",required=True,type=Path)
    a=p.parse_args()
    try:
        if a.action=="check-all":
            check(read(EXAMPLE/"brief.json")["id"],EXAMPLE)
            for d in sorted((ROOT/"intake").iterdir()):
                if d.is_dir():
                    check(d.name,d,draft_ok=True)
            return
        lecture_number(a.id)
        intake=ROOT/"intake"/a.id
        if a.action=="new":
            new(a.id,intake,a.title,a.format)
            return
        brief=check(a.id,intake)
        if a.action=="bootstrap":
            target=ROOT/"lectures"/a.id
            script("init_lecture.py",target,"--renderer","remotion","--lecture",brief["lecture"],"--title",brief["title"])
            print(f"项目已生成。把示范换成本讲实际内容；{brief['format']} 成片目标 {FORMATS[brief['format']]} 分钟。")
        elif a.action=="voice-queue":
            script("prepare_narration.py",intake/"narration.json","--out",a.out)
            script("drama3_takes.py","check",a.out)
    except (ValueError,KeyError,TypeError,OSError,subprocess.CalledProcessError) as e:
        p.exit(1,f"{e}\n")


if __name__=="__main__":
    main()
