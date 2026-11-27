#!/usr/bin/env python3
"""Run the standard source and frame checks for additional Remotion projects changed in a PR."""
import argparse
import json
import subprocess
import sys

from film_pr import COMMIT, matches
from lecture import IDENT, ROOT


def changed_ids(paths):
    ids = set()
    for p in paths:
        parts = p.split("/")
        if len(parts) >= 3 and parts[0] == "lectures" and IDENT.fullmatch(parts[1]):
            ids.add(parts[1])
    return sorted(ids)


def checks(scripts):
    names = ["typecheck", "lint:visuals"]
    if "check:frames" in scripts and scripts["check:frames"] != scripts.get("lint:visuals"):
        names.append("check:frames")
    if "qa:dpo" in scripts:
        names.append("qa:dpo")
    return names


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("base")
    a = p.parse_args()
    if not matches(COMMIT, a.base):
        p.error("expected the full PR base SHA")
    names = subprocess.check_output(
        ["git", "diff", "--name-only", "-z", a.base, "HEAD", "--", "lectures/"], cwd=ROOT
    ).decode().split("\0")
    for lecture in changed_ids(names):
        # The existing production job already checks the upper episode.
        if lecture == "l15-upper":
            continue
        project = ROOT / "lectures" / lecture
        pkg = project / "package.json"
        if not pkg.is_file():
            continue
        scripts = json.loads(pkg.read_text(encoding="utf-8"))["scripts"]
        print(f"Checking actual PR project: lectures/{lecture}", flush=True)
        subprocess.run(["npm", "ci", "--no-audit", "--no-fund"], cwd=project, check=True)
        for name in checks(scripts):
            subprocess.run(["npm", "run", name], cwd=project, check=True)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError) as e:
        sys.exit(str(e))
