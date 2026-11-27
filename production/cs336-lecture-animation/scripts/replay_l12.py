#!/usr/bin/env python3
"""Conform v6.2 from its archived shots, with the matching local dual-track master if supplied."""
import argparse
from contextlib import contextmanager
import json
from pathlib import Path, PurePosixPath
import stat
import subprocess
import sys
import tempfile
from zipfile import ZipFile

HERE = Path(__file__).resolve().parent
PACKAGE = "能力的影子-v6.2-复剪工程"
STEM = "CS336-L12-能力的影子-v6.2"
FRAMES = 114330

@contextmanager
def project(kit, extracted):
    if extracted is not None:
        yield extracted.resolve(strict=True)
        return
    with tempfile.TemporaryDirectory(prefix="cs336-l12-") as name, ZipFile(kit) as z:
        target = Path(name)
        used = set()
        for m in z.infolist():
            n = PurePosixPath(m.filename)
            invalid = n.is_absolute() or ".." in n.parts or not n.parts or n.parts[0] != PACKAGE
            if invalid or n in used or stat.S_ISLNK(m.external_attr >> 16):
                raise ValueError(f"分镜包路径不合法：{m.filename}")
            used.add(n)
            z.extract(m, target)
        yield target / PACKAGE

def verify_project(root, assemble):
    v6 = root / "film/film_zh_v6"
    rows = json.loads((v6 / "book/scenes.json").read_text(encoding="utf-8"))
    if len(rows) != 35 or sum(round(x["duration"] * 60) for x in rows) != FRAMES:
        raise ValueError("需要 v6.2.0 的 35 镜工程")
    if not (v6 / "edition" / (STEM + ".srt")).is_file():
        raise ValueError("缺 v6.2 字幕")
    if assemble and not (v6 / "shots").is_dir():
        raise ValueError("源代码可画封面；重组视频需 Release 的 35 个无声切片")

def verify_movie(path, with_audio):
    d = json.loads(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_streams", "-show_chapters", "-of", "json", str(path)]))
    v = next(s for s in d["streams"] if s["codec_type"] == "video")
    audio = [s["channels"] for s in d["streams"] if s["codec_type"] == "audio"]
    sub = [s for s in d["streams"] if s["codec_type"] == "subtitle"]
    assert (v["width"], v["height"], v["avg_frame_rate"], int(v["nb_frames"])) == (1920, 1080, "60/1", FRAMES)
    assert audio == ([2, 1] if with_audio else []) and len(sub) == 1 and len(d["chapters"]) == 9
    print(f"{FRAMES:,} 帧 · 31:45.5 · 9 章 · 可切换中文字幕 · {len(audio)} 条音轨")

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    inputs = ap.add_mutually_exclusive_group(required=True)
    inputs.add_argument("--kit", type=Path, help="v6.2.0 Release ZIP")
    inputs.add_argument("--project", type=Path, help="解压后的复剪工程根目录")
    ap.add_argument("--out", type=Path, help="重组成片 MP4")
    ap.add_argument("--master", type=Path, help="本地匹配的双音轨 v6.2 母版")
    ap.add_argument("--cover", type=Path, help="重画已定版封面 PNG")
    a = ap.parse_args()
    if not (a.out or a.cover) or (a.master and not a.out):
        ap.error("指定 --out 和/或 --cover；--master 与 --out 一起用")
    for p, ext in ((a.out, ".mp4"), (a.cover, ".png")):
        if p and (p.exists() or p.suffix.lower() != ext):
            ap.error(f"输出需要新的 {ext} 文件：{p}")
    with project(a.kit, a.project) as root:
        verify_project(root, a.out is not None)
        if a.out:
            mode = ["--assemble", str(a.master.resolve(strict=True))] if a.master else ["--assemble-silent"]
            subprocess.run([sys.executable, str(root / "复剪.py"), *mode,
                            "--out", str(a.out.resolve())], check=True)
            verify_movie(a.out, a.master is not None)
        if a.cover:
            subprocess.run([sys.executable, str(HERE / "cover_l12.py"), str(root), str(a.cover.resolve())], check=True)

if __name__ == "__main__":
    main()
