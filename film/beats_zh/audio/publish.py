#!/usr/bin/env python3
"""Promote an explicitly approved candidate and matching word marks."""
import argparse
import json
import shutil
import soundfile as sf
from common import AUDIO, CANDIDATE, candidate_spoken, script_row

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("candidate",nargs="+")
    p.add_argument("--verified-note",help="Explain only a checked, genuine ASR-vs-waveform difference.")
    a=p.parse_args()
    for k in a.candidate:
        if not CANDIDATE.fullmatch(k):p.error(f"invalid id {k}")
        key=k[0]
        stem=AUDIO/"staging"/k
        qsrc=AUDIO/"staging_qa"/f"{k}.qa.json"
        meta=json.loads(stem.with_suffix('.json').read_text())
        qa=json.loads(qsrc.read_text())
        _, original, phonetic, target, _=script_row(key)
        phonetic=candidate_spoken(k,phonetic)
        if original!=meta["text"] or phonetic!=meta["raw"] or target!=meta["target_seconds"]:
            raise ValueError(f"{k}: source script has changed, use a new take")
        if qa["word_changes"] and not (a.verified_note or qa.get("verified_note")):
            raise ValueError(f"{k}: not approved: {qa['word_changes']}")
        w=stem.with_suffix('.wav')
        sec=sf.info(w).duration
        assert abs(sec-qa["seconds"])<2/24000 and qa["words"] and qa["words"][-1]["end"]<=sec+.06
        final=AUDIO/"takes"/key
        cache=AUDIO/"history"/key/str(k)
        if final.with_suffix('.wav').exists():
            # Preserve the most recently approved prior delivery for late script changes.
            prev=json.loads(final.with_suffix(".json").read_text())["candidate"]
            cache=cache.parent/str(prev)
            cache.mkdir(parents=True,exist_ok=True)
            for src in [final.with_suffix('.wav'),final.with_suffix('.json'),AUDIO/'qa'/f'{key}.qa.json']:
                dst=cache/src.name
                if not dst.exists():shutil.copy2(src,dst)
        for src,dst in [(stem.with_suffix('.json'),final.with_suffix('.json')),
                        (qsrc,AUDIO/'qa'/f'{key}.qa.json'),(w,final.with_suffix('.wav'))]:
            pending=dst.with_suffix(dst.suffix+'.approve')
            shutil.copy2(src,pending); pending.replace(dst)
        print(f"{key} approved from {k}: {sec:.2f}s, {meta['wpm']:.0f} CPM",flush=True)

if __name__=="__main__":
    main()
