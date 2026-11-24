"""Verify the two playable deliveries and the inherited opening frame."""
from pathlib import Path
import json,subprocess,re,math
from io import BytesIO
from PIL import Image, ImageChops
from film import canvas,paint,R
T=json.loads((R/'timeline.json').read_text())
ED=json.loads((R.parent/'beats_final'/'timeline.json').read_text())
n0=ED[-1]['end'];n1=T[-1]['end']
assert n1==7650
def run(*c):return subprocess.check_output(c)
def desc(p,expected,chapters,expected_captions):
 a=json.loads(run('ffprobe','-v','error','-show_streams','-show_format','-show_chapters','-of','json',str(p)))
 v=next(x for x in a['streams'] if x['codec_type']=='video')
 s=next(x for x in a['streams'] if x['codec_type']=='subtitle')
 assert (int(v['width']),int(v['height']))==(1920,1080)
 assert int(v['nb_frames'])==expected,(p,v.get('nb_frames'),expected)
 assert abs(float(a['format']['duration'])-expected/30)<.033
 assert s['codec_name']=='mov_text' and s['tags']['language']=='zho'
 assert s['disposition']['default']==1
 assert len(a['chapters'])==chapters
 out=run('ffmpeg','-v','error','-i',str(p),'-map','0:s:0','-f','srt','-').decode()
 assert len(re.findall(r'^\d+\s*$',out,re.M))==expected_captions
 print(p.name,expected/30,expected,expected_captions,'subtitles')
nsub=sum(len(r['captions']) for r in T)
nold=sum(len(r['captions']) for r in ED)
desc(R/'master.mp4',n1,1,nsub)
desc(R/'complete.mp4',n0+n1,3,nold+nsub)

def frame(r,t):
 s,g=canvas(768);paint(g,r,t)
 with BytesIO() as b:
  s.write_to_png(b);b.seek(0);return Image.open(b).convert('RGB')
for a,b in zip(T,T[1:]):
 im=ImageChops.difference(frame(a,a['duration']-1/30),frame(b,0))
 assert not im.getbbox(),(a['id'],b['id'],im.getbbox())
 print(a['id'],b['id'],'identical pose')
prev=Image.open(R/'qa'/'beat1-last-source.png').convert('RGB')
s,g=canvas(960);paint(g,T[0],0);b=BytesIO();s.write_to_png(b);b.seek(0)
f=Image.open(b).convert('RGB')
assert not ImageChops.difference(prev,f).getbbox()
print('Beat 1 → Beat 2 same 960px opening pose')
p=json.loads((R/'verified-data.json').read_text())
m=p['opening']; probs=m['probabilities']
assert abs(math.exp(sum(-math.log(x) for x in probs)/len(probs))-m['ppl'])<1e-10
for r in p['tokenizers']['models']:
 assert len(''.join(r['raw_tokens']).encode())==p['tokenizers']['bytes']
 assert 2**(sum(r['bits'])/len(r['bits']))==r['ppl']
 assert sum(r['bits'])/p['tokenizers']['bytes']==r['bpb']
print('PPL/BPB and common raw-byte denominator recomputed.')
