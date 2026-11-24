"""Project the new spatial shots and the authored Chinese caption track onto H.264 frames."""
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor,as_completed
import argparse,bisect,importlib,json,subprocess,time,os
from spatial import ShotCanvas,cairo,background,INK
R=Path(__file__).resolve().parent
FF='/usr/bin/ffmpeg';FPS=30
def paint(g,r,t,subs=True):
    g.packet(r);background(g)
    mod=importlib.import_module('act'+str(r['act']))
    g.c.save()
    mod.draw(g,r['beat'],t,r['duration'])
    g.c.restore()
    if subs:
        caps=r['captions'];ix=bisect.bisect_right(r['_begins'],t)-1
        if ix>=0 and t<caps[ix]['b']:
            text=caps[ix]['text']
            size=33
            while size>25 and g.measure(text,size,weight='medium')>1150:size-=1.33
            g.text(text,800,827,size,INK,weight='medium')
def piece(r,dst,w,h,enc,lo,hi,caption):
    started=time.monotonic()
    out=Path(dst);tmp=out.with_suffix('.part.mp4')
    s=cairo.ImageSurface(cairo.FORMAT_RGB24,w,h);g=ShotCanvas(cairo.Context(s),w,h)
    last=min(r['frames'],hi if hi is not None else r['frames'])
    cmd=[FF,'-nostdin','-v','error','-y','-f','rawvideo','-pixel_format','bgra','-s',f'{w}x{h}','-framerate',str(FPS),'-i','-',
        '-an','-pix_fmt','yuv420p','-filter_threads','1']
    if enc=='nv':
        cmd+=['-c:v','h264_nvenc','-preset','p5','-tune','hq','-rc','vbr','-cq','17','-b:v','0','-bf','3','-g','90']
    else:
        cmd+=['-c:v','libx264','-preset','ultrafast' if enc=='draft' else 'veryfast','-crf','22' if enc=='draft' else '17','-threads','2','-g','90']
    cmd+=['-color_range','tv','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709',str(tmp)]
    r['_begins']=[x['a'] for x in r['captions']]
    with subprocess.Popen(cmd,stdin=subprocess.PIPE) as p:
        assert p.stdin
        for j in range(lo,last):
            paint(g,r,j/FPS,caption)
            s.flush();p.stdin.write(s.get_data())
        p.stdin.close()
        if p.wait():raise RuntimeError('encoding failed '+r['id'])
    tmp.replace(out)
    return r['id'],last-lo,time.monotonic()-started
def main():
    p=argparse.ArgumentParser();p.add_argument('--timeline',default='timeline')
    p.add_argument('--dest',default='shots');p.add_argument('--width',type=int,default=1920);p.add_argument('--workers',type=int,default=5)
    p.add_argument('--pick',nargs='+');p.add_argument('--act',type=int);p.add_argument('--encoder',choices=['cpu','nv','draft'],default='cpu')
    p.add_argument('--start',type=int,default=0);p.add_argument('--end',type=int);p.add_argument('--no-text',action='store_true')
    a=p.parse_args();r=json.loads((R/f'{a.timeline}.json').read_text())
    out=R/a.dest;out.mkdir(parents=True,exist_ok=True)
    sel=[q for q in r if (not a.pick or q['id'] in a.pick) and (not a.act or q['act']==a.act)]
    with ProcessPoolExecutor(a.workers) as pool:
        fs=[pool.submit(piece,q,out/f'{q["id"]}.mp4',a.width,a.width*9//16,a.encoder,a.start,a.end,not a.no_text) for q in sel]
        for j,f in enumerate(as_completed(fs),1):
            ident,n,sec=f.result();print(f'{j:02d}/{len(sel):02d} · {ident} · {n} f / {sec:.1f}s ({n/sec:.0f} fps)',flush=True)
if __name__=='__main__':main()
