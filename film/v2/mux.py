from pathlib import Path
import argparse,json,subprocess
R=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--shots',default='shots')
p.add_argument('--out',default='spatial-cut.mp4')
a=p.parse_args();rr=json.loads((R/'timeline.json').read_text());d=R/a.shots
f=d/'film.ffconcat'; f.write_text('ffconcat version 1.0\n'+''.join(f"file '{r['id']}.mp4'\nduration {r['frames']/30:.6f}\n" for r in rr))
subprocess.run(['/usr/bin/ffmpeg','-v','error','-y','-nostdin','-f','concat','-safe','0','-i',str(f),'-i',str(R/'mix.wav'),'-i',str(R/'chapters.ffmeta'),
   '-map','0:v:0','-map','1:a:0','-map_metadata','2','-map_chapters','2','-c:v','copy','-c:a','aac','-b:a','160k','-metadata:s:a:0','language=eng',
   '-movflags','+faststart','-t','1200',str(R/a.out)],check=True)
