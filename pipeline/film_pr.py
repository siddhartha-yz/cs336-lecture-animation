#!/usr/bin/env python3
"""Record the source commit and private viewing copy of a film PR."""
import argparse
from decimal import Decimal
import json
import os
from pathlib import Path
import re
import subprocess

from lecture import ROOT, lecture_number

PR_MARK = "<!-- cs336-film-pr:v1 -->"
REVIEW_MARK = "<!-- cs336-film-review:v1 -->"
COMMIT = re.compile(r"[a-f0-9]{40}")
VERSION = re.compile(r"R[0-9]{2,}")
SIZE = (1920, 1080)
FPS = 60
NEXT = {
    "plain": "普通 PR：走 Production check。",
    "plan": "把原始材料交给 Gemini。核准后将 PR 的 plan 改为 ready。",
    "implement": "把 PR 交给 ChatGPT：从分镜、字幕/送读和验收点实现到可审片。先提交源码，再导出候选。",
    "stale": "PR 已有新提交。用当前提交导出下一版，再换 candidate；旧回执不迁移。",
    "gemini": "把这版私有 MP4、镜表和 PR 链接交给 Gemini，随后由仓库所有者贴 Gemini 回执。",
    "revise": "保留 Draft，把这一版的时间码问题交给 ChatGPT；新版提交后换 candidate，再审新版。",
    "owner": "Gemini 已通过。请仓库所有者亲看这版，随后贴本人回执。",
    "approved": "两次回执都对应当前提交。Draft 可转 Ready for review；由用户决定合并。",
}


def block(body, marker):
    lines = (body or "").splitlines()
    starts = [i for i, line in enumerate(lines) if line == marker]
    if not starts:
        return None
    if len(starts) != 1:
        raise ValueError("同一个交接标记只能出现一次")
    tail = lines[starts[0] + 1:]
    if not tail or tail[0] != "```json" or "```" not in tail[1:]:
        raise ValueError("交接标记下方需要紧接 json 代码块")
    try:
        doc = json.loads("\n".join(tail[1:tail.index("```")]))
    except json.JSONDecodeError as e:
        raise ValueError(f"交接 JSON 无法读取：第 {e.lineno} 行") from e
    if not isinstance(doc, dict):
        raise ValueError("交接块必须是 JSON 对象")
    return doc


def fields(obj, *names):
    if not isinstance(obj, dict) or obj.keys() != set(names):
        raise ValueError("交接字段必须是 " + "、".join(names))


def matches(pattern, value):
    return isinstance(value, str) and pattern.fullmatch(value)


def identity(revision, commit):
    if not matches(VERSION, revision) or not matches(COMMIT, commit):
        raise ValueError("版号使用 R01、R02 等；commit 必须是完整的 40 位提交号")


def candidate_record(c):
    fields(c, "version", "commit", "video", "frames")
    identity(c["version"], c["commit"])
    file = c["video"]
    if (not isinstance(file, str) or not file.lower().endswith(".mp4") or len(file) > 180
            or re.search(r'[\\/:<>`\[\]\x00-\x1f\x7f]', file)
            or not re.search(r"(?<![0-9A-Za-z])"+c["version"]+r"(?![0-9A-Za-z])", file)):
        raise ValueError("video 只填含该版号的 MP4 文件名，不填路径或链接")
    if type(c["frames"]) is not int or c["frames"] < 1:
        raise ValueError("frames 必须是同版审片文件的总帧数")


def run(*args):
    p = subprocess.run(args, cwd=ROOT, check=True, capture_output=True, text=True)
    return p.stdout


def cut_frames(lecture, commit):
    path = f"lectures/{lecture}/src/data/cut.json"
    try:
        cut = json.loads(run("git", "show", f"{commit}:{path}"))
    except subprocess.CalledProcessError as e:
        raise ValueError(f"此提交缺正式 Remotion 镜表：{path}") from e
    if cut.get("demo") is not False or cut.get("fps") != FPS:
        raise ValueError("候选镜表必须是 60fps 的正式片（demo: false）")
    lengths = [scene["frames"] for scene in cut["scenes"]]
    if not lengths or any(type(x) is not int or x <= 0 for x in lengths):
        raise ValueError("候选镜表缺有效的镜长")
    return sum(lengths)


def review(role, verdict, candidate):
    candidate_record(candidate)
    if role not in ("gemini", "owner") or verdict not in ("pass", "changes"):
        raise ValueError("回执须标明 gemini/owner 和 pass/changes")
    return {"role": role, "verdict": verdict, "candidate": candidate}


def assess(pr, reviews, owner, expected_head, read_frames=cut_frames):
    plan = block(pr.get("body"), PR_MARK)
    if plan is None:
        return "plain", None
    fields(plan, "lecture", "work", "plan", "candidate")
    lecture = plan["lecture"]
    lecture_number(lecture)
    if plan["work"] not in ("new", "revision") or plan["plan"] not in ("draft", "ready"):
        raise ValueError("work 使用 new/revision；plan 使用 draft/ready")
    candidate = plan["candidate"]
    if candidate is not None:
        candidate_record(candidate)
    head = pr["head"]["sha"]
    if head != expected_head:
        raise ValueError("此次检查的提交已过期；以最新 PR 提交的检查为准")
    if plan["plan"] == "draft":
        if candidate is not None:
            raise ValueError("先核准制作范围，再登记候选")
        return "plan", plan
    if candidate is None:
        return "implement", plan
    if candidate["commit"] != head:
        return "stale", plan
    actual = read_frames(lecture, head)
    if actual != candidate["frames"]:
        raise ValueError(f"候选为 {candidate['frames']} 帧，当前提交镜表为 {actual} 帧")

    # The owner relays Gemini's private media review; only that GitHub account
    # can record either decision. PR authorship alone never counts as approval.
    latest = {}
    signed = [
        item for item in reviews
        if item.get("state") in ("COMMENTED", "DISMISSED")
        and item.get("commit_id") == head
        and (item.get("user") or {}).get("login", "").casefold() == owner.casefold()
    ]
    for item in sorted(signed, key=lambda r: (r["submitted_at"], r["id"])):
        data = block(item.get("body"), REVIEW_MARK)
        if data is None:
            continue
        fields(data, "role", "verdict", "candidate")
        row = review(data["role"], data["verdict"], data["candidate"])
        if row["candidate"] == candidate:
            order = (item["submitted_at"], item["id"])
            decision = None if item["state"] == "DISMISSED" else row["verdict"]
            latest[row["role"]] = (order, decision)
    g, o = latest.get("gemini"), latest.get("owner")
    if not g or g[1] is None:
        return "gemini", plan
    if g[1] == "changes" or (o and o[1] == "changes"):
        return "revise", plan
    if o and o[1] == "pass" and o[0] > g[0]:
        return "approved", plan
    return "owner", plan


def probe(lecture, revision, video):
    lecture_number(lecture)
    commit = run("git", "rev-parse", "HEAD").strip()
    identity(revision, commit)
    if run("git", "status", "--porcelain", "--untracked-files=all").strip():
        raise ValueError("先提交该讲的源稿和工程，再从这个版本导出审片")
    frames = cut_frames(lecture, commit)
    info = json.loads(run("ffprobe", "-v", "error", "-show_streams", "-of", "json", str(video.resolve())))
    streams = info["streams"]
    pictures = [s for s in streams if s["codec_type"] == "video"]
    if len(pictures) != 1 or sum(s["codec_type"] == "audio" for s in streams) != 1:
        raise ValueError("请选择一个画面轨、一个混音轨的带字幕审片版")
    v = pictures[0]
    if ((v["width"], v["height"]) != SIZE or v["avg_frame_rate"] != "60/1"
            or v.get("nb_frames") != str(frames)
            or abs(Decimal(v["duration"]) - Decimal(frames)/FPS) >= Decimal(1)/FPS):
        raise ValueError(f"审片须为 1080p60、{frames} 帧，且对上当前镜表时长")
    item = {"version": revision, "commit": commit, "video": video.name, "frames": frames}
    candidate_record(item)
    return item


def emit(data, marker=""):
    if marker:
        print(f"{marker}\n```json")
    print(json.dumps(data, ensure_ascii=False, indent=2))
    if marker:
        print("```")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    pack = sub.add_parser("candidate", help="从当前提交与本地 MP4 生成 candidate 对象")
    pack.add_argument("lecture")
    pack.add_argument("version")
    pack.add_argument("video", type=Path)
    reply = sub.add_parser("receipt", help="生成在 PR 中以 Comment 提交的审片回执")
    reply.add_argument("role", choices=("gemini", "owner"))
    reply.add_argument("verdict", choices=("pass", "changes"))
    reply.add_argument("candidate", type=Path, help="制作端对实际审片导出的候选 JSON")
    gate = sub.add_parser("check")
    for name in ("event", "pr", "reviews"):
        gate.add_argument(f"--{name}", required=True, type=Path)
    gate.add_argument("--owner", required=True)
    a = parser.parse_args()
    try:
        if a.action == "candidate":
            emit(probe(a.lecture, a.version, a.video))
            return
        if a.action == "receipt":
            candidate = json.loads(a.candidate.read_text(encoding="utf-8"))
            emit(review(a.role, a.verdict, candidate), REVIEW_MARK)
            return
        event, pr, reviews = (json.loads(p.read_text(encoding="utf-8"))
                               for p in (a.event, a.pr, a.reviews))
        stage, meta = assess(pr, reviews, a.owner, event["pull_request"]["head"]["sha"])
        ready = stage in ("plain", "approved")
        lines = ["## 制片 PR 交接", NEXT[stage]]
        if meta is not None:
            lines += [f"讲次：`{meta['lecture']}` · 当前提交：`{pr['head']['sha']}`"]
            c = meta["candidate"]
            if c and stage != "stale":
                lines += [f"候选：`{c['version']}` · `{c['video']}` · {c['frames']:,} 帧"]
        if not ready:
            lines += ["等待同版验收。草稿保留为 Draft；可继续制作和提交。"]
        report = "\n\n".join(lines) + "\n"
        print(report)
        summary = os.environ.get("GITHUB_STEP_SUMMARY")
        if summary:
            with open(summary, "a", encoding="utf-8") as f:
                f.write(report)
        if not ready:
            parser.exit(1)
    except (ValueError, KeyError, TypeError, OSError, ArithmeticError, subprocess.CalledProcessError) as e:
        parser.exit(1, f"制片交接：{e}\n")


if __name__ == "__main__":
    main()
