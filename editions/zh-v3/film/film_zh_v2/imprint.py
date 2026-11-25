"""A single supersampled vector exposure yields two first-generation H.264 cuts (clean / lettered)."""
from pathlib import Path
from direct import W,IDS,state,paint,surface
from export_codec import encoder,h264,worker_options
from letterpress import ass
from edition import captions
import argparse,os,math,sys,time,subprocess
def render(id,src=3840,fps=60,start=0.,seconds=None,root=None):
 if fps!=60:raise ValueError('master clock is 60 fps')
 s,_=state(id);root=Path(root or W);(root/'shots').mkdir(parents=True,exist_ok=True);(root/'shots-sub').mkdir(parents=True,exist_ok=True);(root/'ass').mkdir(exist_ok=True)
 for f in ('shots','shots-sub'):assert root/f!=W/'shots-edit'
 ss=round(start*fps)/fps;count=s['frames']*2-round(ss*fps) if seconds is None else min(round(seconds*fps),s['frames']*2-round(ss*fps));assert count>0
 coords=[[max(0,a-ss),min(count/fps,b-ss),v] for a,b,v in captions(s) if a<ss+count/fps and b>ss]
 rel=Path('ass')/(id+'.ass');ass(coords,root/rel)
 exe,enc=encoder('nvenc');sh=(src,src*9//16);dest=[root/d/(id+'.mp4') for d in ('shots','shots-sub')];tmp=[q.with_suffix('.part.mp4') for q in dest]
 pix='scale=iw:ih:in_range=full:out_range=limited:out_color_matrix=bt709:flags=accurate_rnd+full_chroma_int,format=nv12,hwupload_cuda'
 if src!=1920:pix+=',scale_cuda=w=1920:h=1080:interp_algo=lanczos'
 graph=f'[0:v]{pix},split=2[c][letter];[letter]hwdownload,format=nv12,ass=filename={rel.as_posix()},hwupload_cuda[l]'
 cmd=[exe,'-v','error','-nostdin','-y','-f','rawvideo','-pix_fmt','bgra','-s',f'{sh[0]}x{sh[1]}','-r',str(fps),'-threads','1','-i','pipe:0','-filter_complex_threads','1','-filter_complex',graph]
 for label,fp in zip(('[c]','[l]'),tmp):
  cmd+=['-map',label,'-an',*h264(enc,15),'-g','120','-profile:v','high','-video_track_timescale','15360','-color_range','tv','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709',str(fp.resolve())]
 sf,g=surface(src);stamp=time.monotonic()
 with subprocess.Popen(cmd,stdin=subprocess.PIPE,**worker_options(),cwd=root) as job:
  for i in range(count):
   paint(g,id,ss+i/fps);sf.flush();job.stdin.write(sf.get_data())
  job.stdin.close()
  if job.wait():raise RuntimeError((id,job.returncode))
 for f,o in zip(tmp,dest):f.replace(o)
 print(id,count,src,'wall',round(time.monotonic()-stamp,2),flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('ids',nargs='*');p.add_argument('--src',type=int,default=3840);p.add_argument('--start',type=float,default=0.);p.add_argument('--seconds',type=float);p.add_argument('--root',type=Path);a=p.parse_args()
 for id in a.ids or IDS:render(id,a.src,60,a.start,a.seconds,a.root)
