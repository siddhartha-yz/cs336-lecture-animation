#!/usr/bin/env python3
"""Create a source-first recut archive without local voice, music or credentials."""
import argparse
import json
import os
from pathlib import Path
import tempfile
from zipfile import ZIP_DEFLATED, ZIP_STORED, ZipFile

ROOT=Path(__file__).resolve().parents[1]
MEDIA={".png",".jpg",".jpeg",".webp",".svg",".otf",".ttf",".woff",".woff2"}
SOURCE={".ts",".tsx",".js",".jsx",".mjs",".cjs",".json",".md",".css",".py",".txt"}
REQUIRED=("README.md","VISUAL_CONSTITUTION_v2.md","sources.md","package.json","package-lock.json","tsconfig.json")
SIDECARS=("captions.srt","captions.ass","chapters.ffmeta","章节.txt","镜表.csv","数值算例.txt")

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("out",type=Path)
    p.add_argument("--shots",type=Path,help="可选：已验证的一整套原生清片目录")
    a=p.parse_args()
    out=a.out.expanduser().resolve()
    if out.exists() or out.suffix.lower()!=".zip":
        p.error("请选择新的 .zip 输出")
    files=[(ROOT/f,Path(f),ZIP_DEFLATED) for f in REQUIRED]
    for folder in ("src","scripts","license","public"):
        suffixes=MEDIA if folder=="public" else SOURCE
        for f in sorted((ROOT/folder).rglob("*")):
            rel=f.relative_to(ROOT)
            if not f.is_file() or f.is_symlink() or f.suffix.lower() not in suffixes:
                continue
            if any(n.startswith(".") or n in ("local","audio","__pycache__","node_modules") for n in rel.parts):
                continue
            files.append((f,rel,ZIP_DEFLATED))
    for name in SIDECARS:
        f=ROOT/"docs"/name
        if f.is_file() and not f.is_symlink():files.append((f,f.relative_to(ROOT),ZIP_DEFLATED))
    if a.shots:
        book=json.loads((ROOT/"src/data/cut.json").read_text(encoding="utf-8"))
        for shot in book["scenes"]:
            shot_id=shot["id"]
            if not isinstance(shot_id,str) or not shot_id or any(c not in "abcdefghijklmnopqrstuvwxyz0123456789-" for c in shot_id):
                p.error(f"不能打包该镜号：{shot_id}")
            name=shot_id+".mp4"
            files.append((a.shots/name,Path("build/native-shots")/name,ZIP_STORED))
    for f,_,_ in files:
        if not f.is_file() or f.is_symlink():
            p.error(f"缺少常规打包文件：{f}")
    out.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(dir=out.parent,prefix=".edit-") as d:
        temp=Path(d)/"editing.zip"
        with ZipFile(temp,"x",compresslevel=5) as z:
            for f,rel,compression in files:
                z.write(f,"cs336-editing/"+rel.as_posix(),compress_type=compression)
        os.link(temp,out)
    print(out,len(files),"files")

if __name__=="__main__":
    main()
