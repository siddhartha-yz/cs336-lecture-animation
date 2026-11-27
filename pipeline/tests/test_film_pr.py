import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import check_lectures
import film_pr as gate


A, B = "1" * 40, "2" * 40
OWNER = "creator"
REVIEW = dict(version="R02", commit=A)
CANDIDATE = dict(**REVIEW, video="审片-R02.mp4", frames=79254)
SETUP = dict(lecture="l15-lower", work="revision", plan="ready", candidate=CANDIDATE)


def marked(mark, obj):
    return f"{mark}\n```json\n{json.dumps(obj)}\n```\n"


def current(status=SETUP, head=A, draft=True):
    return {"head": {"sha": head}, "draft": draft, "body": marked(gate.PR_MARK, status)}


def receipt(role, seq, verdict="pass", actor=OWNER, **changed):
    data = dict(role=role, verdict=verdict, candidate={**CANDIDATE, **changed})
    return {"id": seq, "user": {"login": actor}, "body": marked(gate.REVIEW_MARK, data)}


class FilmPR(unittest.TestCase):
    def stage(self, p, *reviews, frames=79254):
        return gate.assess(p, reviews, OWNER, p["head"]["sha"], lambda *_: frames)[0]

    def test_unrelated_pr_and_draft_lifecycle(self):
        self.assertEqual(self.stage({**current(), "body": "update the PR workflow"}), "plain")
        self.assertEqual(self.stage(current({**SETUP, "plan": "draft", "candidate": None})), "plan")
        self.assertEqual(self.stage(current({**SETUP, "candidate": None})), "implement")
        self.assertEqual(self.stage(current()), "gemini")
        self.assertEqual(self.stage(current(), receipt("gemini", 1)), "owner")
        self.assertEqual(self.stage(current(), receipt("gemini", 1), receipt("owner", 2)), "approved")

    def test_new_commit_and_copy_approval_do_not_reopen(self):
        notes = (receipt("gemini", 1), receipt("owner", 2))
        self.assertEqual(self.stage(current(head=B), *notes), "stale")
        p = current({**SETUP, "candidate": {**CANDIDATE, "commit": B}}, head=B)
        self.assertEqual(self.stage(p, *notes), "gemini")
        other_cut = {"version": "R03", "video": "审片-R03.mp4"}
        self.assertEqual(self.stage(current({**SETUP, "candidate": {**CANDIDATE, **other_cut}}), *notes), "gemini")
        renamed = {**CANDIDATE, "video": "另一个审片-R02.mp4"}
        self.assertEqual(self.stage(current({**SETUP, "candidate": renamed}), *notes), "gemini")
        with self.assertRaisesRegex(ValueError, "过期"):
            gate.assess(p, notes, OWNER, A)

    def test_only_owner_can_relay_gemini_and_sign_off_in_order(self):
        r = current()
        self.assertEqual(self.stage(r, receipt("gemini", 1), receipt("owner", 2, actor="contributor")), "owner")
        self.assertEqual(self.stage(r, receipt("gemini", 1, actor="contributor"), receipt("owner", 2)), "gemini")
        self.assertEqual(self.stage(r, receipt("owner", 1), receipt("gemini", 2)), "owner")
        self.assertEqual(self.stage(r, receipt("gemini", 1), receipt("owner", 2, "changes")), "revise")
        self.assertEqual(self.stage(r, receipt("gemini", 1), receipt("owner", 2), receipt("gemini", 3, "changes")), "revise")
        self.assertEqual(self.stage(r, receipt("gemini", 1), receipt("owner", 2), receipt("gemini", 3)), "owner")

    def test_public_candidate_fields_and_real_frame_contract(self):
        for value in ("https://private.invalid/片-R02.mp4", "/data/片-R02.mp4", "审片-R01.mp4"):
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, "文件名"):
                self.stage(current({**SETUP, "candidate": {**CANDIDATE, "video": value}}))
        for value in (True, 0, "79254"):
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, "帧数"):
                self.stage(current({**SETUP, "candidate": {**CANDIDATE, "frames": value}}))
        with self.assertRaisesRegex(ValueError, "当前提交镜表"):
            self.stage(current(), frames=79000)
        with self.assertRaisesRegex(ValueError, "核准"):
            self.stage(current({**SETUP, "plan": "draft"}))

    def test_contract_marker_errors_are_actionable(self):
        r = current()
        r["body"] += r["body"]
        with self.assertRaisesRegex(ValueError, "只能出现一次"):
            self.stage(r)
        r["body"] = gate.PR_MARK + "\n\n没有 JSON"
        with self.assertRaisesRegex(ValueError, "紧接 json"):
            self.stage(r)

    def test_template_itself_is_a_runnable_draft(self):
        p = gate.ROOT / ".github/PULL_REQUEST_TEMPLATE/film.md"
        self.assertEqual(self.stage({**current(), "body": p.read_text(encoding="utf-8")}), "plan")


class SourceChecks(unittest.TestCase):
    def test_select_changed_native_lectures_only(self):
        self.assertEqual(check_lectures.changed_ids([
            "lectures/l15-lower/src/film.ts", "lectures/l15-lower/README.md", "lectures/l16/src/data/cut.json",
            ".github/workflows/film-pr.yml", "film/check.sh", "lectures/l16-fiction/fake",
        ]), ["l15-lower", "l16"])

    def test_avoid_redundant_frame_alias_and_keep_project_gate(self):
        self.assertEqual(check_lectures.checks({
            "typecheck": "tsc --noEmit", "lint:visuals": "same", "check:frames": "same", "qa:dpo": "true",
        }), ["typecheck", "lint:visuals", "qa:dpo"])
        self.assertEqual(check_lectures.checks({
            "lint:visuals": "lint", "check:frames": "different",
        }), ["typecheck", "lint:visuals", "check:frames"])
