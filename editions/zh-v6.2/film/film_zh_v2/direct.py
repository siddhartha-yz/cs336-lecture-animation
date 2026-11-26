"""Draw the entire film against one Mandarin word clock. Geometry is sampled at output fps."""
from termnotes import hint,TERMS
import sys,os,json,math,re,argparse,subprocess,time,importlib
from pathlib import Path
from functools import lru_cache
W=Path(__file__).resolve().parent
sys.path[:0]=list(map(str,[W,W/'art0',W/'art2',W.parent/'beats_zh',W.parent/'beat2',W.parent/'v2',W.parent]))
from cut_common import ShotCanvas,stage,cairo,SERIF,CJK,flatkey
from localize2 import C as C2,tr
from localize_script import C as C0
from visual import ease,mix
from export_codec import encoder,h264,worker_options
IDS=[s['id'] for s in json.loads((W/'script.json').read_text())]
OPEN={'0-1':('a','opening',0),'0-2':('b','opening',1),'1-1':('c','middle',0),'1-2':('d','middle',1),'1-3':('e','tail',0),'1-4':('f','tail',1)}
SPLIT={'a':['可训练会','你选哪把尺'],'b':['多步推理','可到打分时','看这两个盒子','等大家','光去优化影子'],'c':['先把成本','把智能指数','预算一落下来','可要是连标准答案'],'d':['这时候','先把模型名字','把这些两两对比','现在盯着','每换一把尺','与其问谁最好'],'e':['我们评的是','传统机器学习','拿 ImageNet','其余条件固定','可换成两个','训练集里有什么','它拿了第一'],'f':['NanoGPT','FineWeb','硬件统一','那比什么','少花一分钟','顺着这条终点线','这个损失背后'],'2-1':['把概率连乘','换个算法','这个数怎么看','把它降到十'],'2-3':['先想一个理想情况','真实模型没到这一步','看这条算术题序列'],'2-4':['Paloma','如果榜单只收','所以要在受控沙箱']}
REPLACE={'2-1':{'取负对数概率':'取负对数','再取指数':'最后取指数','等效的候选数':'这个数怎么看'},'2-3':{'把它降下去':'降到最低'}}
def canon(t):return re.sub(r'[^a-z0-9\u3400-\u9fff]','',t.lower())
# Mobile landscape proofs at 844px left several first-use definitions only 12px tall.
# Only the definitional line gets a wider type size. Its factor is fixed in board space,
# so neither zooms nor text hinting can make it walk relative to a chart.
_term_lines={canon(v)for k,v in TERMS.items() if k not in ('FineWeb','BPB','六域等权 PPL')}
@lru_cache(maxsize=1536)
def first_use(s):return canon(s) in _term_lines
class Ink(ShotCanvas):
 loc=False;no_text=False;prefix_blend=None
 def text(self,s,x,y,size=36,color='#FFFFFF',alpha=1,align='center',font='sans',weight='normal'):
  if self.no_text:return
  if s=='| prefix)':
   # Pango's ink bounds intentionally ignore external whitespace. Place the mathematical
   # separator and its two breathing spaces explicitly; do not widen either glyph.
   bar=super().measure('∣',size,font,weight);dx=.23*size
   super().text('∣',x+dx,y,size,color,alpha,'left',font,weight)
   super().text('前文)',x+dx+bar+.16*size,y,size,color,alpha,'left',font,weight)
   return
  label=tr(str(s)) if self.loc else str(s)
  if first_use(label):
   size*=1.13
   if color in ('#C0C5CB','#CDCDCD','#B0B8C4'):color='#D4D7DC'
  return super().text(label,x,y,size,color,alpha,align,font,weight)
 def measure(self,s,size=36,font='sans',weight='normal'):
  if s=='| prefix)':
   return .39*size+super().measure('∣',size,font,weight)+super().measure('前文)',size,font,weight)
  label=tr(str(s)) if self.loc else str(s)
  return super().measure(label,size*(1.13 if first_use(label) else 1),font,weight)

class Clock:
 def __init__(self,s):self.s=s;self.d=s['duration'];self.ch=s['chars'];self.loc={}
 def at(self,q):
  if q not in self.loc:
   k=self.ch.find(canon(q))
   if k<0:raise ValueError((self.s['id'],'missing cue',q))
   self.loc[q]=self.s['starts'][k]
  return self.loc[q]
 def u(self,t,q,span=1.15,early=.12):
  a=self.at(q)-early;v=max(0,min(1,(t-a)/span));return v*v*(3-2*v)
 def clock(self,t):self.t=t;return self
@lru_cache(None)
def state(id):
 s=json.loads((W/'scenes'/f'{id}.json').read_text());z=Clock(s)
 if id in OPEN or id in ('2-1','2-3','2-4'):
  key=OPEN[id][0] if id in OPEN else id
  cues=C0[key] if id in OPEN else C2[key]
  s['zh_cue_override']={flatkey(en):z.at(REPLACE.get(id,{}).get(zh,zh))/z.d for en,zh in cues}
  s['parts_at']=[0.]+[z.at(q)/z.d for q in SPLIT[key]]
 return s,z
def raw(g,id,t):
 s,c=state(id);g.clock=c.clock(t);stage(g);g.c.save();g.prefix_blend=None;g.packet(s);g.loc=id.startswith('2-')
 if id in OPEN:
  _,module,index=OPEN[id];importlib.import_module(module).draw(g,index,t,s['duration'])
 elif id=='2-2':
  from ppl_chalk import tokenizer
  tokenizer(g,c)
 elif id.startswith('2-'):
  g.prefix_blend=ease(max(0,min(1,(t-.13)/1.03))) if id=='2-1' else None
  m={'2-1':'opening2','2-3':'tradeoff','2-4':'domains'}[id];importlib.import_module(m).draw(g,0,t,s['duration'])
 else:
  import boards
  boards.draw(g,id,c)
 if id in ('1-4','2-1'):
  from ink import txt,F,M,T,phase
  op=phase(t,c.at('最基本的指标')-.52,c.at('最基本的指标')+.22) if id=='1-4' else 1-phase(t,4.62,5.09)
  if op:
   txt(g,'困惑度（PPL）',800,62,34,T,op)
   txt(g,hint('困惑度（PPL）'),800,114,25,M,op)
 g.c.restore()
def surface(width):
 h=width*9//16;sf=cairo.ImageSurface(cairo.FORMAT_RGB24,width,h);return sf,Ink(cairo.Context(sf),width,h)
def paint(g,id,t):
 raw(g,id,t)
 if int(id[0])>=3:
  import bridges
  bridges.bridge(g,id,t,state,raw,surface,IDS)
def shot(id,width=1920,mode='nvenc',fps=60,aa=1920,out=None):
 x,c=state(id);sf,g=surface(aa);h=aa*9//16;dest=Path(out or W/'shots')/f'{id}.mp4';dest.parent.mkdir(parents=True,exist_ok=True);part=dest.with_suffix('.part.mp4');exe,codec=encoder(mode);ts=time.monotonic()
 filt='format='+('nv12' if codec=='nvenc' else 'yuv420p')
 if aa!=width:filt+=f',hwupload_cuda,scale_cuda=w={width}:h={width*9//16}:interp_algo=lanczos' if codec=='nvenc' else f',scale={width}:{width*9//16}:flags=lanczos'
 cmd=[exe,'-v','error','-nostdin','-y','-f','rawvideo','-pix_fmt','bgra','-s',f'{aa}x{h}','-r',str(fps),'-threads','1','-i','pipe:0','-an','-filter_threads','1','-vf',filt,*h264(codec,16 if width>=1920 else 20),'-g',str(2*fps),'-profile:v','high','-video_track_timescale','15360','-color_range','tv','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709',str(part)]
 n=x['frames']*fps//30
 with subprocess.Popen(cmd,stdin=subprocess.PIPE,**worker_options()) as proc:
  for f in range(n):
   paint(g,id,f/fps);sf.flush();proc.stdin.write(sf.get_data())
  proc.stdin.close()
  if proc.wait():raise RuntimeError(id)
 part.replace(dest);print(id,n,round(time.monotonic()-ts,2),flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('ids',nargs='*');p.add_argument('--width',type=int,default=1920);p.add_argument('--aa',type=int);p.add_argument('--fps',type=int,default=60,choices=(30,60));p.add_argument('--out');p.add_argument('--stills',action='store_true');p.add_argument('--second',type=float);p.add_argument('--encoder',choices=['auto','nvenc','cpu'],default='nvenc')
 a=p.parse_args()
 for id in a.ids or IDS:
  if a.stills or a.second is not None:
   s,_=state(id);sf,g=surface(a.width)
   for i,t in enumerate(([a.second] if a.second is not None else [s['duration']*u for u in [.04,.16,.35,.52,.72,.89,.98]])):
    paint(g,id,t);sf.write_to_png(str(W/'stills'/f'{id}_{i}.png'))
  else:shot(id,a.width,a.encoder,a.fps,a.aa or a.width,a.out)
