"""Reusable 1600×900 blackboard, one master clock per sequence and one camera per shot."""
from pathlib import Path
from functools import lru_cache
import json,sys,os,bisect,math,re,unicodedata
from math import pi,tau,sin,cos,log,exp,sqrt
W=Path(__file__).resolve().parent;V3=W.parent/'film_zh_v3'
sys.path.insert(0,str(V3))
import stage3 as prev
sys.path.insert(0,str(W/'native5'))
from timeline3 import S as OLDS,clock as oc
from ink import *
from ink_words import swish,out
from outlines5 import letter5 as letter,texwrite
from cut_common import cairo,stage,SERIF,CJK
from mounting import etch
from studio_examples import area
from motion import transit
from motion6 import FlowClock
W=Path(__file__).resolve().parent
V3=W.parent/'film_zh_v3';V2=W.parent/'film_zh_v2';AS=W/'assets'
BOOK={r['id']:r for r in json.loads((W/'book/scenes.json').read_text())}
MARKERS=json.loads((W/'book/visual-cues.json').read_text())
def norm(s):return re.sub(r'[^a-z0-9\u3400-\u9fff]','',unicodedata.normalize('NFKC',s).lower())
class Cue:
 def __init__(self,k,guide=False):
  self.k=k;file=W/('book/guide-clocks'if guide else 'scene-clocks')/(k+'.json');self.s=json.loads(file.read_text());self.d=self.s['duration'];self.gs=self.s['groups_meta'];self.t=0.
 @lru_cache(None)
 def at(self,q):
  if type(q) in (float,int):return float(q)
  if q=='$':return self.d
  if q=='$s':return self.s['speech']
  anchor=MARKERS.get(self.k,{}).get(q,q);offset=0.
  if isinstance(anchor,dict):offset=float(anchor['offset']);anchor=anchor['ref']
  q=anchor
  if q.startswith('g') and re.fullmatch(r'g\d+(e)?',q):return self.gs[int(q[1:].rstrip('e'))-1]['end'if q.endswith('e')else'start']+offset
  word,*nn=q.split('#');p=-1
  for _ in range(1+int(nn[0])if nn else 1):
   p=self.s['chars'].find(norm(word),p+1)
   if p<0:raise ValueError(('new cue absent',self.k,q))
  return self.s['starts'][p]+offset
 def u(self,q,span=.55,lead=.08):
  return phase(self.t,self.at(q)-lead,self.at(q)-lead+span)
 def delta(self,q):return self.t-self.at(q)
 def rest(self,n):return next(x for x in self.s['rests']if x['name']==n)
@lru_cache(None)
def _cue(k,guide):return Cue(k,guide)
def cue(k,guide=False):
 # A call with the default and a call with explicit False must identify the
 # very same clock. functools.lru_cache does not normalize default arguments.
 return _cue(k,bool(guide))
def native(g,c,k,knots):
 # Bind source phrases, not the runtime of a previous MP4. Only motion/layout is inherited.
 tt=legacy_flow(c,k,tuple(knots))(c.t)
 g._attached=False;render_inherited(g,k,max(.001,min(OLDS[k]['duration']-.02,tt)));g._attached=True;g.loc=False;g.legacy=False;g.editor_id='edition4'
@lru_cache(None)
def inherited_time(k):
 from timeline3 import knots
 return FlowClock(*knots(k))
def render_inherited(g,k,t):
 if k=='3-3':
  from science6 import draw
  from lens import seat
  from mounting import place
  previous=oc(k).clk(t);g.editor_id=k;g.loc=False;g.no_text=False;g.legacy=False
  stage(g);g.c.save()
  try:
   seat(g,k,previous);draw(g,previous);place(g,k,previous)
  finally:g.c.restore()
  return
 if k in prev.CUSTOM:return prev.raw(g,k,t)
 # v3 also projects its *own* older response onto a linear word clock. Chain
 # differentiable clocks through both generations, keeping the shots anchored.
 from lens import historical
 g.editor_id=k;g.loc=False;g.no_text=False;g.legacy=True;c=oc(k).clk(t)
 stage(g);g.c.save()
 try:
  historical(g,k,c);prev.v2.raw(g,k,inherited_time(k)(t))
  if k=='2-2':
   from studio_units import compare
   g.loc=False;compare(g,c)
 finally:g.c.restore();g.loc=False
@lru_cache(None)
def legacy_knots(c,k,knots):
 x=[];y=[];o=oc(k)
 for a,b in knots:
  aa=c.at(a);bb=(OLDS[k]['duration']-.025 if b=='$'else o.at(b) if isinstance(b,str) else b)
  if len(x)>0 and (aa<=x[-1] or bb<y[-1]-.02):raise ValueError(('nonmonotonic',c.k,k,a,b,aa,bb,x[-1],y[-1]))
  x.append(aa);y.append(bb)
 assert len(x)>=2;return x,y
@lru_cache(None)
def legacy_flow(c,k,knots):
 x,y=legacy_knots(c,k,knots)
 return FlowClock(x,y)
def mark(g,s,x,y,fs,t,col=F,align='center',mode='wave',dur=.53,op=1):
 letter(g,s,x,y,fs,t,mode,col,op,align,SERIF,dur)
def label(g,s,x,y,fs=31,col=F,op=1,align='center',limit=None):
 txt(g,s,x,y,fs,col,op,align,width=limit)
def panelnote(g,term,ex,x,y,ts,co=C,op=1):
 mark(g,term,x,y,38,ts,co,'left','pen',.48,op);mark(g,ex,x+1,y+42,25,ts-.14,M,'left','wave',.37,op)
def shade(g,av): 
 if av>.0001:rect(g,-30,-30,1660,960,BLACK,clip(av))
def point(g,x,y,r,col=Y,op=1):
 dot(g,x,y,r,col,op);dot(g,x,y,.38*r,F,op*.83)
def p5(v):v=clip(v);return v**3*(v*(6*v-15)+10)
def enter(t,at,span=.58):return out(clip((t-at)/span))
def easepos(t,at,d=.6):return p5((t-at)/d)
def during(t,a,b,d=.48):
 return enter(t,a,d)*(1-phase(t,b-d,b))
def underline(g,x,y,w,t,col=Y):swish(g,x,x+w,y,t,col,.60,3.7)
@lru_cache(maxsize=26)
def img(p):return cairo.ImageSurface.create_from_png(str(p))
def photo(g,p,x,y,w,h=None,tilt=0,op=1):
 if op<.002:return
 sf=img(p);iw,ih=sf.get_width(),sf.get_height();h=w*ih/iw if h is None else h
 ctx=g.c;ctx.save();ctx.translate(x,y);ctx.rotate(tilt);ctx.scale(w/iw,h/ih);ctx.translate(-iw/2,-ih/2);ctx.rectangle(0,0,iw,ih);ctx.clip()
 ctx.set_source_surface(sf,0,0);ctx.get_source().set_filter(cairo.Filter.BILINEAR);ctx.paint_with_alpha(clip(op));ctx.restore()
def page(g,p,x,y,w,t,out_t=1e7,tilt=-.034,read='',warm_col=O):
 u=enter(t,0,.58);v=phase(t,out_t-.57,out_t);s=mix(.88,1,u);h=img(p).get_height()/img(p).get_width()*w
 if u<.001 or v>.999:return
 xx=x+146*(1-u)-88*v;yy=y-100*(1-u)+111*v+2.1*sin(1.19*t+.003*x)*u*(1-v)
 photo(g,p,xx,yy,w*s,tilt=tilt+.064*(1-u)-.055*v,op=u*(1-v))
 if read:
  mark(g,read,x-w*.46,y+h*.5+39,24,t-.16,warm_col,'left','wave',.40,1-v)
def optgrid(g,x,y,w,h,n,k,col=C,active=None,labels=False):
 gap=8;cw=(w-(n-1)*gap)/n
 for j in range(n):
  v=clip(k*1.30-j*.28/max(1,n-1));xx=x+j*(cw+gap);co=col if active is None or active==j else E
  box(g,xx,y,w=cw,h=h,col=co,a=v,fill=inkcol(co,.51 if active is None or active==j else .13),sw=1.8)
  if labels:label(g,chr(65+j),xx+cw/2,y+h*.51,26,F,v)
def satin(g,s,x,y,w,h,theta=0):
 ctx=g.c;ctx.save();ctx.translate(x,y);ctx.rotate(theta);box(g,-w/2,-h/2,w,h,s,1,inkcol(s,.17),2.4);ctx.restore()
@lru_cache(maxsize=4)
def _endpaper(k,width):
 # Immutable single exposure in the same camera and colour pipeline. This is the
 # actual outgoing pose, not a redrawn thumbnail with stale relative positions.
 from shoot4 import drawclean
 surf,gg=prev.surface(width);cc=cue(k);old=cc.t
 try:drawclean(gg,k,cc.d-1/60)
 finally:cc.t=old
 surf.flush();return surf
def endpaper(g,k,dx=0,dy=0,sc=1,op=1):
 if op<.001:return
 ctx=g.c;surf=_endpaper(k,ctx.get_target().get_width());ctx.save()
 ctx.translate(dx,dy);s=sc*1600/surf.get_width();ctx.scale(s,s)
 ctx.set_source_surface(surf,0,0);ctx.get_source().set_filter(cairo.FILTER_BILINEAR);ctx.paint_with_alpha(clip(op));ctx.restore()
