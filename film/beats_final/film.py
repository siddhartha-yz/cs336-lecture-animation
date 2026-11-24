"""Render Beat 0–1 with switchable subtitles and the exact recorded narration clock."""
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor,as_completed
from functools import lru_cache
import argparse,bisect,importlib,json,subprocess,sys,time
R=Path(__file__).resolve().parent
sys.path.insert(1,str(R.parent/'v2'))
from cut_common import ShotCanvas,cairo,stage
FPS=30
FF='/usr/bin/ffmpeg'

@lru_cache
def scene(module):
    return importlib.import_module(module)
def paint(g,r,t):
    g.packet(r)
    stage(g)
    g.c.save()
    scene(r['module']).draw(g,r['beat'],t,r['duration'])
    g.c.restore()

def canvas(w):
    h=w*9//16
    s=cairo.ImageSurface(cairo.FORMAT_RGB24,w,h)
    return s,ShotCanvas(cairo.Context(s),w,h)

def encode(r,width,dest,draft=False):
    t0=time.monotonic()
    w=width;h=w*9//16
    out=dest/(r['id']+'.mp4')
    tmp=out.with_suffix('.part.mp4')
    s,g=canvas(w)
    cmd=[FF,'-nostdin','-v','error','-y','-f','rawvideo','-pixel_format','bgra','-s',f'{w}x{h}',
         '-framerate','30','-i','-','-an','-pix_fmt','yuv420p','-filter_threads','1','-c:v','libx264',
         '-preset','ultrafast' if draft else 'veryfast','-crf','23' if draft else '17','-threads','2',
         '-g','90','-color_range','tv','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709',str(tmp)]
    with subprocess.Popen(cmd,stdin=subprocess.PIPE) as p:
        for f in range(r['frames']):
            paint(g,r,f/FPS)
            s.flush();p.stdin.write(s.get_data())
        p.stdin.close()
        if p.wait():raise RuntimeError(f'Encoding failed: {r["id"]}')
    tmp.replace(out)
    return r['id'],r['frames'],time.monotonic()-t0

def mux(dest,out):
    rows=json.loads((R/'timeline.json').read_text())
    f=dest/'film.ffconcat'
    f.write_text('ffconcat version 1.0\n'+''.join(f"file '{r['id']}.mp4'\nduration {r['duration']}\n" for r in rows))
    end=rows[-1]['end']/30
    subprocess.run([FF,'-v','error','-y','-nostdin','-f','concat','-safe','0','-i',str(f),'-i',str(R/'audio'/'mix.wav'),
      '-i',str(R/'meta.ffmeta'),'-i',str(R/'zh.srt'),'-map','0:v:0','-map','1:a:0','-map','3:s:0',
      '-map_metadata','2','-map_chapters','2','-c:v','copy','-c:a','aac','-b:a','160k','-c:s','mov_text',
      '-metadata:s:a:0','language=eng','-metadata:s:s:0','language=zho','-metadata:s:s:0','title=简体中文',
      '-disposition:s:0','default',
      '-movflags','+faststart','-t',f'{end:.7f}',str(out)],check=True)

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--pick',nargs='+');p.add_argument('--width',type=int,default=1920)
    p.add_argument('--workers',type=int,default=5);p.add_argument('--estimate',action='store_true');p.add_argument('--clock')
    p.add_argument('--dest',default='shots');p.add_argument('--still',nargs=3,metavar=('ID','TIME','FILE'))
    p.add_argument('--mux',metavar='FILE')
    a=p.parse_args()
    dst=R/a.dest;dst.mkdir(exist_ok=True)
    if a.mux:mux(dst,R/a.mux);sys.exit()
    rows=json.loads((R/(a.clock or ('draft.json' if a.estimate else 'timeline.json'))).read_text())
    if a.still:
        id_,t,fn=a.still
        r=next(x for x in rows if x['id']==id_)
        s,g=canvas(a.width)
        paint(g,r,float(t))
        out=Path(fn);out.parent.mkdir(exist_ok=True,parents=True);s.write_to_png(str(out))
    else:
        rows=[r for r in rows if not a.pick or r['id'] in a.pick]
        with ProcessPoolExecutor(a.workers) as pool:
            futures=[pool.submit(encode,r,a.width,dst,a.estimate) for r in rows]
            for j,f in enumerate(as_completed(futures),1):
                i,n,sec=f.result()
                print(f'{j}/{len(rows)} {i} {n} frames in {sec:.2f}s',flush=True)
