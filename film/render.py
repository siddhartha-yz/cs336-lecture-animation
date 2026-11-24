"""Lossless vector stage -> per-beat H.264 -> one MP4 with continuous score and chapter navigation."""
from __future__ import annotations
import argparse,bisect,concurrent.futures,importlib,json,os,subprocess,time
from pathlib import Path
import cairo
from visual import Canvas,background,step,INK
R=Path(__file__).resolve().parent
FPS=30
FF='/usr/bin/ffmpeg'
    
def paint_packet(g,r,t):
    g.cues_text=r.get('cues_text','');g.cues=r.get('cues',[])
    mod=importlib.import_module('act'+str(r['act']))
    mod.draw(g,r['beat'],t,r['duration'])
def caption(g,cap):
    if not cap:return
    size=33
    while g.measure(cap,size,weight='medium')>1160 and size>26:size-=1.4
    g.text(cap,800,831,size,INK,1.,weight='medium')
    
def cross_allowed(r,prev):
    if prev is None or r['beat']==0:return False # matching anchor between acts
    # Animate within a scene first. A few intentionally matched cuts stay crisp.
    return r['id'] not in {'1-01','1-02','1-05','1-08','1-15','2-01','2-09','2-10','3-02','3-07','3-08','4-01','4-05','4-11'}

def frame_stamp(r,prev,w,h):
    if not cross_allowed(r,prev):return None
    sf=cairo.ImageSurface(cairo.FORMAT_RGB24,w,h)
    cg=Canvas(cairo.Context(sf),w,h); background(cg)
    paint_packet(cg,prev,prev['duration']-1/FPS)
    return sf
    
def render_piece(args):
    r,prev,dest,w,h,draft,enc,start,end=args
    dest=Path(dest)
    st=time.monotonic()
    count=r['frames']
    e=min(count,end if end is not None else count)
    progress=(e-start)
    if progress<=0:raise ValueError(r['id'])
    canvas=cairo.ImageSurface(cairo.FORMAT_RGB24,w,h)
    g=Canvas(cairo.Context(canvas),w,h)
    sf=frame_stamp(r,prev,w,h)
    cue=r['captions']
    begins=[x['in'] for x in cue]
    ffargs=[FF,'-v','error','-y','-nostdin','-f','rawvideo','-pixel_format','bgra','-s',f'{w}x{h}',
       '-framerate',str(FPS),'-i','pipe:0','-filter_threads','1','-an','-pix_fmt','yuv420p']
    if enc=='nv':
        ffargs+=['-c:v','h264_nvenc','-preset','p5','-tune','hq','-rc','vbr','-cq','17','-b:v','0','-g','90','-bf','3']
    else:
        ffargs+=['-c:v','libx264','-preset','ultrafast' if draft else 'veryfast','-crf','22' if draft else '17','-g','90','-threads','2']
    tmp=dest.with_name(dest.stem+'.part.mp4')
    with subprocess.Popen(ffargs+['-color_range','tv','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709',str(tmp)],stdin=subprocess.PIPE) as proc:
        assert proc.stdin
        for i in range(start,e):
            t=i/FPS
            g.c.save();background(g);paint_packet(g,r,t);g.c.restore()
            if sf is not None and t<.26:
                alpha=1.-step(t,0,.26)
                c=g.c;c.save();c.identity_matrix()
                c.set_source_surface(sf,0,0);c.paint_with_alpha(alpha);c.restore()
            ix=bisect.bisect_right(begins,t)-1
            if ix>=0 and t<cue[ix]['out']:caption(g,cue[ix]['text'])
            canvas.flush();proc.stdin.write(canvas.get_data())
        proc.stdin.close()
        if proc.wait()!=0:raise RuntimeError(f'ffmpeg failed at beat {r["id"]}')
    tmp.replace(dest)
    return r['id'],progress,time.monotonic()-st

def mtime(p):return Path(p).stat().st_mtime
def main():
    q=argparse.ArgumentParser()
    q.add_argument('--timeline',default='timeline')
    q.add_argument('--dest',default='film_chunks')
    q.add_argument('--width',type=int,default=1920)
    q.add_argument('--workers',type=int,default=5)
    q.add_argument('--encoder',choices=['cpu','nv'],default='cpu')
    q.add_argument('--draft',action='store_true')
    q.add_argument('--pick',nargs='+')
    q.add_argument('--start',type=int,default=0)
    q.add_argument('--end',type=int)
    q.add_argument('--all',action='store_true')
    a=q.parse_args()
    rows=json.loads((R/f'{a.timeline}.json').read_text())
    out=R/a.dest;out.mkdir(exist_ok=True)
    n=0;done=0;elapsed=0; jobs=[]
    for j,r in enumerate(rows):
        if a.pick and r['id'] not in a.pick:continue
        outp=out/f'{r["id"]}.mp4'
        newest=max(mtime(R/k) for k in ('render.py','visual.py',f'act{r["act"]}.py',f'{a.timeline}.json'))
        if not a.all and outp.exists() and mtime(outp)>=newest:continue
        jobs.append((r,rows[j-1] if j else None,str(outp),a.width,a.width*9//16,a.draft,a.encoder,a.start,a.end))
        n+=1
    if n:
        with concurrent.futures.ProcessPoolExecutor(max_workers=a.workers) as pool:
            futures=[pool.submit(render_piece,j) for j in jobs]
            for f in concurrent.futures.as_completed(futures):
                beat,count,sec=f.result(); done+=1;elapsed+=sec
                print(f'{done:02d}/{n:02d} · {beat} · {count} frames in {sec:.1f}s ({count/sec:.0f}fps)',flush=True)
    if not a.pick and a.start==0 and a.end is None:
        for r in rows:
            if not (out/f'{r["id"]}.mp4').exists():raise FileNotFoundError(r['id'])
        (out/'concat.ffconcat').write_text('ffconcat version 1.0\n'+''.join(f"file '{r['id']}.mp4'\n" for r in rows))
if __name__=='__main__':main()
