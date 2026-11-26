"""Long-cut exposure at 60 FPS from native glyph and data paths; NVIDIA-only master encoding."""
from rig4 import *
from argparse import ArgumentParser
import importlib,subprocess,time
from export_codec import encoder,h264,worker_options
from press3 import ass
from edition import captions,width as caption_width
W=Path(__file__).resolve().parent
RUN={'0-1':('v4_act0','cold'),'0-2':('v4_act0','projection'),'opening':('v4_act0','front'),'inter':('v4_act0','doors'),'8-2':('v4_act0','closing'),
'1-1':('v4_act1','cost'),'1-2':('v4_act1','pools'),'1-3':('v4_act1','attrib'),'2-1':('v4_act2','tokens'),'2-2':('v4_act2','byte'),'2-3':('v4_act2','reversal'),'2-4':('v4_act2','domains'),
'3-1':('v4_act3','saturation'),'3-2':('v4_act3','pro'),'3-3':('v4_act3','gpqa'),'3-4':('v4_act3','hle'),
'4-1':('v4_act4','letterdesk'),'4-2':('v4_act4','elo'),'4-3':('v4_act4','biases'),'4-4':('v4_act4','factor'),
'5-1':('v4_act5','sandbox'),'5-2':('v4_act5','chances'),'6-1':('v4_act6','grids'),'6-2':('v4_act6','conduct'),
'7-1':('v4_act7','workshop'),'7-2':('v4_act7','order'),'7-3':('v4_act7','windows'),'7-4':('v4_act7','calendar'),'8-1':('v4_act7','orbit')}
for k in BOOK:
 if k.startswith('door'):RUN[k]=('v4_act0','doors')
@lru_cache(None)
def drawfn(k):m,n=RUN[k];return getattr(importlib.import_module(m),n)
def drawclean(g,k,t,guide=False):
 c=cue(k,guide);was=c.t;c.t=t
 g._attached=True;g.loc=False;g.legacy=False;g.no_text=False;g.editor_id='edition4';stage(g)
 g.c.save()
 try:drawfn(k)(g,c)
 finally:
  c.t=was
  g.c.restore()
from splice4 import seam
def draw(g,k,t,guide=False):
 drawclean(g,k,t,guide);seam(g,k,t,guide,drawclean)
@lru_cache(1)
def frozen_cards():return json.loads((W/'book/captions.json').read_text())
def caprows(s):
 if s.get('caption_mode')=='v6-cards':return frozen_cards()[s['id']]
 if not s['groups_meta']:return []
 # Segment per acoustic take so a subtitle never stretches across a real audience pause.
 out=[]
 for j,gr in enumerate(s['groups_meta']):
  off=sum(len(norm(r['text']))for r in s['groups_meta'][:j]);n=len(norm(gr['text']));a,b=gr['from'],gr['spoken_end']
  p={**s,'id':'take','text':gr['text'],'chars':norm(gr['text']),'starts':s['starts'][off:off+n],'ends':s['ends'][off:off+n],'duration':b+.10}
  rows=captions(p)
  # A half-beat instruction is a lead-in, not its own flashing subtitle. Merge only
  # within this take; an audience reading interval can never be bridged by a caption.
  for j0 in range(len(rows)-2,-1,-1):
   st,en,word=rows[j0];ss,ee,nex=rows[j0+1]
   if en-st<.96 and ss-en<.06 and word in ('盯住右边。','先看整行。','看这几根柱子。','现在往下读。','注意这个反例。') and caption_width(word+nex)<=27:
    rows[j0:j0+2]=[[st,ee,word+nex]]
  out.extend([max(a,x),min(b+.10,y),l]for x,y,l in rows)
 # Two meaning groups can share a take. Clear the old caption precisely when the next starts.
 for i in range(len(out)-1):out[i][1]=min(out[i][1],out[i+1][0])
 return out
def clipshot(k,src,directory=None):
 s=cue(k).s;sf,g=prev.surface(src);n=s['frames'];w,h=src,src*9//16
 root=Path(directory).expanduser().resolve()if directory else W;[p.mkdir(parents=True,exist_ok=True)for p in (root/'shots',root/'shots-sub',root/'edits/ass',root/'review/exposures')]
 ass(caprows(s),root/'edits/ass'/(k+'.ass'));dest=[root/d/(k+'.mp4')for d in ('shots','shots-sub')];tmp=[p.with_suffix('.part.mp4')for p in dest]
 exe,enc=encoder('nvenc');pix='scale=iw:ih:in_range=full:out_range=limited:out_color_matrix=bt709:flags=accurate_rnd+full_chroma_int,format=nv12,hwupload_cuda'
 if src!=1920:pix+=',scale_cuda=w=1920:h=1080:interp_algo=lanczos'
 graph=f'[0:v]{pix},split=2[c][b];[b]hwdownload,format=nv12,ass=filename=edits/ass/{k}.ass,hwupload_cuda[l]'
 cmd=[exe,'-v','error','-nostdin','-y','-f','rawvideo','-pix_fmt','bgra','-s',f'{w}x{h}','-r','60','-threads','1','-i','pipe:0','-filter_complex_threads','1','-filter_complex',graph]
 for lab,path in zip(('[c]','[l]'),tmp):cmd+=['-map',lab,'-an',*h264(enc,15),'-g','120','-profile:v','high','-video_track_timescale','15360','-color_range','tv','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709',str(path)]
 tm=time.monotonic()
 with subprocess.Popen(cmd,stdin=subprocess.PIPE,**worker_options(),cwd=root)as pp:
  for i in range(n):draw(g,k,i/60);sf.flush();pp.stdin.write(sf.get_data())
  pp.stdin.close()
  if pp.wait():raise RuntimeError('encoder failure: '+k)
 for a,b in zip(tmp,dest):a.replace(b)
 (root/'review/exposures'/(k+'.json')).write_text(json.dumps(dict(scene=k,pixels=src,output=[1920,1080],frames=n,fps=60,clock=s['clock_source'],created=time.strftime('%Y-%m-%d %H:%M:%S')),indent=2))
 print(k,n,src,round(time.monotonic()-tm,1),flush=True)
def contacts(ids,guide,sz,n):
 from PIL import Image,ImageDraw,ImageFont
 gd=W/'review/contact';gd.mkdir(parents=True,exist_ok=True);dest=gd/('guide'if guide else 'voice');dest.mkdir(exist_ok=True)
 for k in ids:
  s=cue(k,guide);sf,g=prev.surface(sz);cols=3;thumbw=480;hh=thumbw*9//16;out=Image.new('RGB',(cols*thumbw,((n+cols-1)//cols)*(hh+24)),(31,32,33));pen=ImageDraw.Draw(out)
  for j in range(n):
   t=(j+.52)/n*s.d;draw(g,k,t,guide);sf.flush();im=Image.frombytes('RGB',(sz,sz*9//16),bytes(sf.get_data()),'raw','BGRX',0,1);im.thumbnail((thumbw,hh));x=j%cols*thumbw;y=j//cols*(hh+24);out.paste(im,(x,y));pen.text((x+5,y+hh+3),f'{k}    {t:.2f}s',fill='#DEDEDE')
  out.save(dest/(k+'.jpg'),quality=89);print('checked',k,flush=True)
if __name__=='__main__':
 p=ArgumentParser();p.add_argument('ids',nargs='+');p.add_argument('--src',type=int,default=2560);p.add_argument('--guide',action='store_true');p.add_argument('--contacts',type=int);p.add_argument('--at',action='append',type=float);p.add_argument('--out',type=Path);p.add_argument('--sweep',type=float);a=p.parse_args()
 ids=list(BOOK) if a.ids==['all']else a.ids
 if a.contacts:contacts(ids,a.guide,a.src,a.contacts)
 elif a.sweep:
  for k in ids:
   c=cue(k,a.guide);sf,g=prev.surface(a.src)
   for i in range(math.ceil(c.d/a.sweep)):draw(g,k,i*a.sweep,a.guide)
   print('sweep',k,flush=True)
 elif a.at:
  for k in ids:
   sf,g=prev.surface(a.src)
   for t in a.at:draw(g,k,t,a.guide);sf.write_to_png(str(a.out or W/'review'/f'{k}-{t:.2f}.png'))
 else:
  if a.guide:raise SystemExit('Refusing to expose against a guide clock.')
  for k in ids:clipshot(k,a.src)
