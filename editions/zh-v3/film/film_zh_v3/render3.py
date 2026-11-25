"""Native 60 fps, single supersampled exposure, NVENC clean and subtitled outputs."""
from timeline3 import W,OLD,S,IDS
from stage3 import paint,surface
from press3 import ass
from edition import captions
from export_codec import encoder,h264,worker_options
import math,argparse,subprocess,time,os
from pathlib import Path
import json
from pigments import INK_EDITION
def render(k,src,fps=60,*,outroot=None):
 root=W if outroot is None else Path(outroot).resolve()
 for d in ('shots','shots-sub','notes/exposures'):(root/d).mkdir(parents=True,exist_ok=True)
 (W/'ass').mkdir(exist_ok=True)
 s=S[k];n=s['frames']*2;w,h=src,src*9//16;dest=[root/d/(k+'.mp4')for d in ('shots','shots-sub')];tmp=[q.with_suffix('.part.mp4')for q in dest]
 ass(captions(s),W/'ass'/(k+'.ass'));exe,enc=encoder('nvenc');pix='scale=iw:ih:in_range=full:out_range=limited:out_color_matrix=bt709:flags=accurate_rnd+full_chroma_int,format=nv12,hwupload_cuda'
 if src!=1920:pix+=',scale_cuda=w=1920:h=1080:interp_algo=lanczos'
 graph=f'[0:v]{pix},split=2[c][b];[b]hwdownload,format=nv12,ass=filename=ass/{k}.ass,hwupload_cuda[l]'
 cmd=[exe,'-v','error','-nostdin','-y','-f','rawvideo','-pix_fmt','bgra','-s',f'{w}x{h}','-r',str(fps),'-threads','1','-i','pipe:0','-filter_complex_threads','1','-filter_complex',graph]
 for lab,path in zip(('[c]','[l]'),tmp):
  cmd+=['-map',lab,'-an',*h264(enc,15),'-g','120','-profile:v','high','-video_track_timescale','15360','-color_range','tv','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709',str(path)]
 sf,g=surface(src);tm=time.monotonic()
 with subprocess.Popen(cmd,stdin=subprocess.PIPE,**worker_options(),cwd=W)as p:
  for i in range(n):
   paint(g,k,i/fps);sf.flush();p.stdin.write(sf.get_data())
  p.stdin.close()
  if p.wait():raise RuntimeError(k)
 for a,b in zip(tmp,dest):a.replace(b)
 cert=root/'notes'/'exposures'
 (cert/(k+'.json')).write_text(json.dumps({'edition':INK_EDITION,'scene':k,'supersample':src,'frames':n,'finished':time.strftime('%Y-%m-%d %H:%M:%S')},indent=2))
 print(k,n,src,round(time.monotonic()-tm,2),flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('ids',nargs='+');p.add_argument('--src',type=int,default=2880);p.add_argument('--at',type=float,action='append');p.add_argument('--out',type=Path);args=p.parse_args()
 for k in args.ids:
  if args.at:
   sf,g=surface(args.src)
   for t in args.at:
    paint(g,k,t);out=args.out or W/'stills'/f'{k}-{t:06.2f}.png';sf.write_to_png(str(out))
  else:render(k,args.src)
