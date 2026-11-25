"""Identity-driven chalk motion. Timing is in recorded syllables; positions are in board units."""
from math import pi,sin,cos,hypot,exp
from pathlib import Path
from functools import lru_cache
import xml.etree.ElementTree as ET
from ink import *
def out3(p):p=clip(p);return 1-(1-p)**3
def settle(p):
 # A slightly overdamped arrival with one small overshoot; never applied to glyph shape.
 p=clip(p);return 1+(p-1)**2*((1+1.19)*(p-1)+1.19)
def itinerary(t,start,duration,b=0.):
 return (out3 if b==0 else settle)((t-start)/duration)
def transit(a,b,u,lift=0):
 return mix(a[0],b[0],u),mix(a[1],b[1],u)-lift*sin(pi*clip(u))
def reletter(p):
 # Two distinct inscriptions sharing one piece of blackboard must never
 # occupy it at the same time. The geometry beneath can move continuously.
 return 1-phase(p,0,.43),phase(p,.52,1)
def guide(g,pts,p,c=Y,op=1,sw=2.3,tail=.22):
 # Fixed-length passing segment, measured by arc length. No halo.
 L=[0.]
 for a,b in zip(pts,pts[1:]):L.append(L[-1]+hypot(b[0]-a[0],b[1]-a[1]))
 if L[-1]<.01:return
 p=clip(p);lo=max(0.,(p-tail)*L[-1]);hi=p*L[-1];out=[]
 for j,(a,b) in enumerate(zip(pts,pts[1:])):
  aa=max(lo,L[j]);bb=min(hi,L[j+1])
  if bb<=aa:continue
  if not out:out.append(lerp(a,b,(aa-L[j])/(L[j+1]-L[j])))
  out.append(lerp(a,b,(bb-L[j])/(L[j+1]-L[j])))
 if len(out)>1:g.poly(out,c,sw,op);dot(g,*out[-1],2.35,c,op)
def emphasize(g,x,y,w,h,p,col=Y):
 # Mark the actual reading; a moving stroke is easier to follow than flashing a region.
 if 0<p<1:
  chain=[(x-w/2,y+h/2),(x+w/2,y+h/2),(x+w/2,y-h/2),(x-w/2,y-h/2),(x-w/2,y+h/2)]
  guide(g,chain,p,col,sin(pi*p)**.5,2.6,.34)
@lru_cache(None)
def formula_asset(name):
 import cairo,gi
 gi.require_version('Rsvg','2.0')
 from gi.repository import Rsvg
 p=Path(__file__).with_name('math')/(name+'.svg')
 vb=ET.fromstring(p.read_bytes()).attrib['viewBox'].split()
 ratio=float(vb[2])/float(vb[3]);ww=900.;hh=ww/ratio
 surf=cairo.RecordingSurface(cairo.CONTENT_COLOR_ALPHA,(0,0,ww,hh));ctx=cairo.Context(surf)
 box=Rsvg.Rectangle();box.x=0;box.y=0;box.width=ww;box.height=hh
 Rsvg.Handle.new_from_file(str(p)).render_document(ctx,box)
 return surf,ww,hh
def formula(g,name,x,y,w,alpha=1):
 if alpha<=.002 or getattr(g,"no_text",False):return
 sf,base,h=formula_asset(name);ctx=g.c;ctx.save();ctx.translate(x-w*.5,y-h*w/base*.5);ctx.scale(w/base,w/base);ctx.set_source_surface(sf,0,0);ctx.paint_with_alpha(clip(alpha));ctx.restore()
def curtain(g,k,draw):
 if k<=.001:return
 if k>=.999:draw();return
 c=g.c;c.save();c.push_group();draw();c.pop_group_to_source();c.paint_with_alpha(k);c.restore()
