import json
from pathlib import Path
from shutil import copytree
import sys
import tempfile
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import lecture
import score
sys.path.insert(0,str(lecture.KIT/"scripts"))
from prepare_narration import voice_budget
from locate_feedback import to_frame, locate


class IntakeTests(unittest.TestCase):
    def test_intake_produces_real_voice_candidates(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            data=root/"intake"
            copytree(lecture.EXAMPLE,data)
            self.assertEqual(lecture.check("l16",data)["voice"],"科普声音")
            queue=root/"queue.json"
            lecture.script("prepare_narration.py",data/"narration.json","--out",queue)
            lecture.script("drama3_takes.py","check",queue)
            rows=json.loads(queue.read_text())
            self.assertEqual(len(rows),5)
            self.assertEqual(sum(r["cue"]=="ask" for r in rows),4)

    def test_native_pace_budget_excludes_reserved_time_and_duplicate_takes(self):
        cue={"sub":"0.7","tts":"零点七","kind":"question","N":4}
        count, capacity, (fast, slow)=voice_budget([cue],2,60)
        self.assertEqual((count,capacity),(3,250))
        self.assertAlmostEqual(fast,60.72)
        self.assertAlmostEqual(slow,60+180/230)
        with self.assertRaisesRegex(ValueError,"预留"):
            voice_budget([cue],1,60)

    def test_bootstrap_from_actual_kit_uses_remotion(self):
        with tempfile.TemporaryDirectory() as temp:
            dest=Path(temp)/"next"
            lecture.bootstrap({"lecture":17,"title":"实际新讲","format":"derivation"},dest)
            state=json.loads((dest/"src/data/cut.json").read_text())
            self.assertEqual((state["lecture"],state["fps"],state["title"],state["demo"],state["format"]),
                             (17,60,"实际新讲",True,"derivation"))
            self.assertTrue((dest/"VISUAL_CONSTITUTION_v2.md").is_file())

    def test_draft_cannot_begin_production(self):
        with tempfile.TemporaryDirectory() as temp:
            d=Path(temp)/"draft"
            lecture.new("l15-lower",d,"片名","derivation")
            self.assertIsNone(lecture.check("l15-lower",d,draft_ok=True))
            with self.assertRaisesRegex(ValueError,"ready"):
                lecture.check("l15-lower",d)


class ScoreTests(unittest.TestCase):
    def test_three_unique_seeds_and_native_cap(self):
        plan=score.read(lecture.EXAMPLE/"music.json")
        self.assertEqual(len(score.validate(plan)),1)
        plan["tracks"][0]["preview_seeds"]=[1,1,2]
        with self.assertRaisesRegex(ValueError,"种子"):
            score.validate(plan)
        plan["tracks"][0].update(preview_seeds=[1,2,3],duration_seconds=440)
        with self.assertRaisesRegex(ValueError,"拆"):
            score.validate(plan)

    def test_revised_prompt_cannot_reuse_old_audio(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)
            cues=score.validate(score.read(lecture.EXAMPLE/"music.json"))
            score.remember(path,cues)
            cues[0]["duration_seconds"]=100
            score.remember(path,cues)
            cues[0]["prompt"]+=" More piano."
            with self.assertRaisesRegex(ValueError,"输出目录"):
                score.remember(path,cues)


class ReviewTests(unittest.TestCase):
    def test_feedback_clock_uses_inclusive_start_and_exclusive_end(self):
        cut={"fps":60, "scenes":[
            {"id":"a","frames":60,"captions":[[0,59,"口播"]],"cues":{"move":59}},
            {"id":"b","frames":30,"captions":[]},
        ]}
        self.assertEqual(to_frame("00:00.999",60),59)
        self.assertEqual(locate(cut,59),("a",59,60,None,(59,"move"),None))
        self.assertEqual(locate(cut,to_frame("00:01",60)),("b",0,30,None,None,None))
        with self.assertRaisesRegex(ValueError,"超出"):
            locate(cut,to_frame("#90",60))
