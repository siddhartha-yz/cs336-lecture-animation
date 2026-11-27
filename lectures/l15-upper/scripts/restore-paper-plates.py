#!/usr/bin/env python3
"""Recreate the four Ouyang et al. citations from the official v1 PDF."""
import argparse
from pathlib import Path
import struct
import subprocess
import tempfile
import urllib.request

URL = "https://arxiv.org/pdf/2203.02155v1"
ROOT = Path(__file__).resolve().parents[1]
# Rectangles already checked against the master: figure 2 at 600dpi, Eq. (2) at 480dpi.
PLATES = (
    ("instruct-prompt", 3, 600, 1464, 980, 446, 236, False),
    ("instruct-example", 3, 600, 1464, 1315, 446, 388, False),
    ("instruct-sft", 3, 600, 1464, 1779, 446, 438, False),
    ("instruct-eq2", 9, 480, 871, 2676, 2586, 417, True),
)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    loc = p.add_mutually_exclusive_group(required=True)
    loc.add_argument("--pdf", type=Path, help="arXiv:2203.02155v1 PDF")
    loc.add_argument("--fetch", action="store_true", help="从固定的 arXiv 官方地址下载")
    a = p.parse_args()
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        pdf = a.pdf.resolve() if a.pdf else d / "ouyang-v1.pdf"
        if a.fetch:
            with urllib.request.urlopen(URL, timeout=45) as response:
                buf = response.read(8_000_001)
            if len(buf) > 8_000_000:
                p.error("论文文件超过预期上限")
            pdf.write_bytes(buf)
        if not pdf.is_file():
            p.error("找不到 PDF")
        # A different version or generic PDF can return plausible empty crops.
        for n, anchors in ((3, ("Figure 2:", "supervised fine-tuning")), (9, ("log(", "(2)"))):
            s = subprocess.check_output(["pdftotext","-f",str(n),"-l",str(n),str(pdf),"-"],text=True)
            if any(x not in s for x in anchors):
                p.error(f"第 {n} 页和 arXiv:2203.02155v1 不符")
        pending = []
        for key, page, dpi, x, y, w, h, alpha in PLATES:
            out = ROOT/"public"/"plates"/(key+".png")
            if out.is_file():
                with out.open("rb") as f:
                    header = f.read(24)
                if len(header) == 24 and header.startswith(b"\x89PNG\r\n\x1a\n") and struct.unpack(">II", header[16:]) == (w,h):
                    continue
                p.error(f"{out.name} 不是这版的尺寸；请先移走旧图板")
            cmd = ["pdftocairo","-transp"] if alpha else ["pdftoppm"]
            subprocess.run([*cmd,"-q","-png","-singlefile","-f",str(page),"-l",str(page),
                "-r",str(dpi),"-x",str(x),"-y",str(y),"-W",str(w),"-H",str(h),
                str(pdf),str(d/key)],check=True)
            candidate = d/(key+".png")
            with candidate.open("rb") as f:
                header=f.read(24)
            if struct.unpack(">II",header[16:]) != (w,h):
                p.error(f"{key} 裁切尺寸不符")
            pending.append((candidate,out))
        for src,out in pending:
            # Stage on the destination filesystem for a complete PNG on rename.
            with tempfile.NamedTemporaryFile(dir=out.parent,delete=False) as f:
                f.write(src.read_bytes())
                dest=Path(f.name)
            dest.replace(out)
        print(f"原论文 4 个图板就绪；本次恢复 {len(pending)} 个")


if __name__ == "__main__":
    main()
