#!/usr/bin/env python3
"""Create a fresh editable CS336 cut; keep the v6.2 project as a separate baseline."""
import argparse
import json
from pathlib import Path
import shutil

SKILL = Path(__file__).resolve().parents[1]

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("project", type=Path)
    ap.add_argument("--lecture", type=int)
    ap.add_argument("--title")
    ap.add_argument("--renderer", choices=("cairo", "remotion"), default="cairo",
                    help="新讲按技能用 remotion；不传参数保留旧 Cairo 调用")
    args = ap.parse_args()
    dest = args.project.expanduser().resolve()
    if dest.exists():
        ap.error(f"工程目录已存在：{dest}")
    if args.lecture is not None and args.lecture < 1:
        ap.error("讲次用正整数")
    starter = "remotion-starter" if args.renderer == "remotion" else "starter"
    shutil.copytree(SKILL / "assets" / starter, dest,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "node_modules", "build"))
    cut = dest / "cut.json"
    if args.renderer == "remotion":
        cut = dest / "src/data/cut.json"
        shutil.copy2(SKILL / "references/VISUAL_CONSTITUTION_v2.md", dest / "VISUAL_CONSTITUTION_v2.md")
    plan = json.loads(cut.read_text(encoding="utf-8"))
    if args.lecture is not None:
        plan["lecture"] = args.lecture
    if args.title:
        plan["title"] = args.title
    cut.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(dest)

if __name__ == "__main__":
    main()
