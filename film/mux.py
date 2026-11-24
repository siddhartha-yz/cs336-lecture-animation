"""Mux the approved picture and mixed sound. Keep each beat on the master frame clock."""
import argparse,json,subprocess
from pathlib import Path
R=Path(__file__).resolve().parent
p=argparse.ArgumentParser()
p.add_argument('--chunks',default='film_chunks')
p.add_argument('--out',default='cs336-review.mp4')
p.add_argument('--timeline',default='timeline')
p.add_argument('--audio',default='mixed.wav')
a=p.parse_args()
rows=json.loads((R/f'{a.timeline}.json').read_text())
dst=R/a.chunks
fc=dst/'final.ffconcat'
fc.write_text('ffconcat version 1.0\n'+''.join(
    f"file '{r['id']}.mp4'\nduration {r['frames']/30:.6f}\n" for r in rows))
cmd=['/usr/bin/ffmpeg','-v','error','-y','-nostdin','-f','concat','-safe','0','-i',str(fc),'-i',str(R/a.audio),
     '-i',str(R/f'{a.timeline}.ffmeta'),'-map','0:v:0','-map','1:a:0','-map_metadata','2','-map_chapters','2',
     '-c:v','copy','-c:a','aac','-b:a','160k','-metadata:s:a:0','language=zho','-movflags','+faststart','-t','1200',str(R/a.out)]
subprocess.run(cmd,check=True)
