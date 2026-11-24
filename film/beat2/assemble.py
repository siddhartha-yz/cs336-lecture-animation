"""Join the locked 0–1 sequence to Beat 2 without a picture cut at the shared pose."""
from pathlib import Path
import json,re,subprocess
R=Path(__file__).resolve().parent
old=R.parent/'beats_final'
new_rows=json.loads((R/'timeline.json').read_text())
old_rows=json.loads((old/'timeline.json').read_text())
n0=old_rows[-1]['end'];n1=new_rows[-1]['end']
s0,s1=n0/30,n1/30
raw=R/'complete.ffconcat'
raw.write_text(f"ffconcat version 1.0\nfile '{old/'master.mp4'}'\nduration {s0:.9f}\nfile '{R/'master.mp4'}'\nduration {s1:.9f}\n")
def parse(text):
    seg=[]
    for para in re.split(r'\n\s*\n',(text.strip())):
        _,tc,*lines=para.splitlines()
        u,v=tc.split(' --> ')
        seg.append((ms(u),ms(v),'\n'.join(lines)))
    return seg
def ms(tc):
    a,b,c,d=[int(x) for x in re.split('[:,]',tc)]
    return 1000*(3600*a+60*b+c)+d
def fmt(t):
    h,t=divmod(t,3600000);m,t=divmod(t,60000);s,t=divmod(t,1000)
    return f'{h:02d}:{m:02d}:{s:02d},{t:03d}'
subs=parse((old/'zh.srt').read_text())
delta=round(s0*1000)
subs.extend((a+delta,b+delta,z) for a,b,z in parse((R/'zh.srt').read_text()))
f_s=R/'complete.srt'
f_s.write_text('\n\n'.join(f'{i}\n{fmt(a)} --> {fmt(b)}\n{z}' for i,(a,b,z) in enumerate(subs,1))+'\n')
meta=(old/'meta.ffmeta').read_text().rstrip()
meta+=f'\n[CHAPTER]\nTIMEBASE=1/30\nSTART={n0}\nEND={n0+n1}\ntitle=Beat 2 — What perplexity can see\n'
f_m=R/'complete.ffmeta';f_m.write_text(meta)
opts=['ffmpeg','-v','error','-y','-nostdin','-f','concat','-safe','0','-i',str(raw),
      '-i',str(old/'audio/mix.wav'),'-i',str(R/'audio/mix.wav'),'-i',str(f_m),'-i',str(f_s),
      '-filter_complex','[1:a:0][2:a:0]concat=n=2:v=0:a=1[a]',
      '-map','0:v:0','-map','[a]','-map','4:s:0','-map_metadata','3','-map_chapters','3',
      '-c:v','copy','-c:a','aac','-b:a','160k','-c:s','mov_text','-metadata:s:a:0','language=eng',
      '-metadata:s:s:0','language=zho','-metadata:s:s:0','title=简体中文','-disposition:s:0','default',
      '-movflags','+faststart','-t',str(s0+s1),str(R/'complete.mp4')]
subprocess.run(opts,check=True)
print(f'0–2: {s0+s1:.3f} s; {len(subs)} cues; Beat 2 starts at {s0:.3f} s.')
