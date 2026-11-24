"""Restore the archived production audio at its original sample rate and bit depth."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]

def restore(archive, group, root=ROOT):
    entries = json.loads((ROOT / "tools/audio-packs.json").read_text())[group]
    with zipfile.ZipFile(archive) as z:
        expected = {Path(name).with_suffix(".flac").as_posix() for name in entries}
        if expected != set(z.namelist()):
            raise SystemExit(f"The selected archive does not match the {group} edit.")
        restored = kept = 0
        for name, meta in entries.items():
            out = root / name
            if out.exists():
                kept += 1
                continue
            out.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.TemporaryDirectory(dir=out.parent) as tmp:
                wav = Path(tmp) / "decoded.wav"
                with z.open(Path(name).with_suffix(".flac").as_posix()) as src:
                    with subprocess.Popen(
                        ["ffmpeg", "-nostdin", "-v", "error", "-xerror", "-i", "pipe:0",
                         "-map", "0:a:0", "-map_metadata", "-1", "-c:a", meta["codec_name"], str(wav)],
                        stdin=subprocess.PIPE,
                    ) as proc:
                        with proc.stdin:
                            shutil.copyfileobj(src, proc.stdin)
                        if proc.wait():
                            raise SystemExit(f"Could not decode {name}")
                stream = json.loads(subprocess.check_output(
                    ["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries",
                     "stream=codec_name,sample_rate,channels,duration_ts", "-of", "json", str(wav)]
                ))["streams"][0]
                if stream != {key: meta[key] for key in ('codec_name', 'sample_rate', 'channels', 'duration_ts')}:
                    raise SystemExit(f"Format or sample count changed for {name}")
                # Keep verified word clocks newer than the original take after a fresh clone.
                os.utime(wav, (meta["source_mtime"], meta["source_mtime"]))
                wav.rename(out)
            restored += 1
    print(f"{group}: restored {restored} WAV files; kept {kept} existing files.")

if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("group", choices=["beats", "full"])
    p.add_argument("archive", type=Path)
    args = p.parse_args()
    restore(args.archive, args.group)
