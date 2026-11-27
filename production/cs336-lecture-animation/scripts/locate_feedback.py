#!/usr/bin/env python3
"""Locate review timestamps in the corresponding Remotion cut, without modifying it."""
import argparse
import json
from pathlib import Path
import re

TIME = re.compile(r"(?:(\d+):)?(\d+):([0-5]\d)(?:\.(\d{1,3}))?\Z")


def to_frame(mark, fps):
    if re.fullmatch(r"#[0-9]+", mark):
        return int(mark[1:])
    found = TIME.fullmatch(mark)
    if not found or (found[1] is not None and int(found[2]) >= 60):
        raise ValueError(f"{mark}: 用 MM:SS[.mmm]、HH:MM:SS[.mmm] 或 #全片帧号")
    h, m, s = (int(found[i] or 0) for i in range(1, 4))
    millis = int((found[4] or "").ljust(3, "0"))
    return ((h * 3600 + m * 60 + s) * 1000 + millis) * fps // 1000


def locate(cut, frame):
    start = 0
    for row in cut["scenes"]:
        stop = start + row["frames"]
        if start <= frame < stop:
            local = frame - start
            caption = next((text for a, b, text in row["captions"] if a <= local < b), None)
            cues = sorted((v, k) for k, v in row.get("cues", {}).items())
            previous = next((x for x in reversed(cues) if x[0] <= local), None)
            following = next((x for x in cues if x[0] > local), None)
            return row["id"], local, row["frames"], caption, previous, following
        start = stop
    raise ValueError(f"全片帧 #{frame} 超出本版镜表 [0, {start})")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("cut", type=Path, help="与审片文件同一版本的 src/data/cut.json")
    p.add_argument("marks", nargs="+", help="时间码或 #帧，写帧号时给 shell 加引号")
    a = p.parse_args()
    try:
        cut = json.loads(a.cut.read_text(encoding="utf-8"))
        fps = cut["fps"]
        if type(fps) is not int or fps < 1:
            raise ValueError("镜表需要整数 fps")
        for mark in a.marks:
            frame = to_frame(mark, fps)
            name, local, total, caption, prev, nxt = locate(cut, frame)
            print(f"{mark} → 全片 #{frame} · {name} +{local} / {total} 帧")
            if caption is not None:
                print("  字幕："+caption.replace("\n", " / "))
            cues = "；".join(f"{label} {v[1]} @{v[0]}" for label, v in
                           (("上一锚", prev), ("下一锚", nxt)) if v is not None)
            if cues:
                print("  "+cues)
    except (KeyError, TypeError, OSError, ValueError) as exc:
        p.exit(1, f"{exc}\n")


if __name__ == "__main__":
    main()
