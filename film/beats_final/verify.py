from pathlib import Path
import json,subprocess,sys,re
from PIL import Image,ImageChops,ImageDraw
from io import BytesIO
from film import R,paint,canvas
rows=json.loads((R/'timeline.json').read_text())
(R/'qa').mkdir(exist_ok=True)
p=R/'master.mp4'
js=lambda a:json.loads(subprocess.check_output(a))
meta=js(['ffprobe','-v','error','-show_format','-show_streams','-show_chapters','-of','json',str(p)])
v,a,c=[next(x for x in meta['streams'] if x['codec_type']==k) for k in ('video','audio','subtitle')]
assert (v['width'],v['height'],int(v['nb_frames']))==(1920,1080,rows[-1]['end'])
assert a['tags']['language']=='eng'
assert (c['codec_name'],c['tags']['language'],c['disposition']['default'])==('mov_text','zho',1)
srt=subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-map','0:s:0','-f','srt','-']).decode()
n=len(re.findall(r'^\d+$',srt,re.M));assert n==sum(len(r['captions']) for r in rows)
assert len(meta['chapters'])==2 and abs(float(meta['format']['duration'])-rows[-1]['end']/30)<.022
def pic(r,t):
    s,g=canvas(640);paint(g,r,t)
    with BytesIO() as b:
        s.write_to_png(b);b.seek(0);return Image.open(b).convert('RGB')
for x,y in zip(rows,rows[1:]):
    diff=ImageChops.difference(pic(x,x['duration']-1/30),pic(y,0))
    n_chg=sum(diff.convert('L').histogram()[18:])
    assert n_chg<220,(x['id'],y['id'],n_chg)
    print(f'{x["id"]}→{y["id"]}: {n_chg} materially changed pixels')
for k,subclip in (('first','abc'),('last','def')):
    w,h=400,225
    s=Image.new('RGB',(w*3,(h+20)*3),'#1D2025');labels=ImageDraw.Draw(s)
    for j,r in enumerate(x for x in rows if x['id'] in subclip):
        st=r['start']/30; t=r['duration']
        indices={'a':[0,1,2],'b':[1,3,5],'c':[2,3,4],
                 'd':[2,3,5],'e':[3,5,7],'f':[1,3,7]}[r['id']]
        for i,ind in enumerate(indices):
            at=min(t-.12,r['parts_at'][ind]*t+1.85)
            if r['id']=='f' and i==2:at=t-.25
            raw=subprocess.check_output(['ffmpeg','-v','error','-threads','2','-ss',f'{at+st:.3f}','-i',str(p),
              '-frames:v','1','-vf',f'scale={w}:{h}','-f','image2pipe','-c:v','png','-'])
            im=Image.open(BytesIO(raw)).convert('RGB')
            assert max(im.getpixel((1,1)))==0,(r['id'],i,im.getpixel((1,1)))
            s.paste(im,(w*i,(h+20)*j))
            labels.text((w*i+8,(h+20)*j+h+3),f'{r["id"].upper()}  {int((at+st)//60):02}:{(at+st)%60:05.2f}',fill='#FFFFFF')
    s.save(R/'qa'/f'{k}-encoded.jpg',quality=93)
print(f'{v["width"]}×{v["height"]}, {v["nb_frames"]} frames, {n} Chinese captions, 2 chapters')
