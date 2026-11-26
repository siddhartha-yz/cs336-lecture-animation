"""Letterpress and TeX use the very same frozen vector outlines at t=0.99 and t=1."""
from functools import lru_cache
from pathlib import Path
import xml.etree.ElementTree as ET,re,math,bisect
from ink import *
from cut_common import cairo,SERIF
import ink_words as old
def letter5(g,s,x,y,sz,t,mode='wave',col=F,op=1,align='center',font=SERIF,dur=.56):
 if op<=.002 or t<0 or g.no_text or (hasattr(g,'outside') and g.outside(s,x,y,sz)):return
 if t<dur:return old.letter(g,s,x,y,sz,t,mode,col,op,align,font,dur)
 raw,(le,top,ww,h),_=old._l(g,s,sz,font);q=g.c;q.save();q.translate(x,y);q.scale(sz/g.EM,sz/g.EM);q.translate(-le-{'center':ww*.5,'right':ww}.get(align,0),-top-h*.5)
 q.new_path();q.append_path(raw);g.source(col,op);q.fill();q.restore()
W=Path(__file__).resolve().parent
@lru_cache(None)
def outlines(tag):
 f=W/'art/formula'/(tag+'.svg')
 if not f.is_file():f=W.parent/'film_zh_v2/math'/(tag+'.svg')
 svg=ET.parse(f).getroot();vb=list(map(float,svg.attrib['viewBox'].split()));ns='{http://www.w3.org/2000/svg}';defs={u.attrib['id']:u.find(ns+'path').attrib['d'] for u in svg.findall('.//'+ns+'defs//'+ns+'g')if 'id'in u.attrib and u.find(ns+'path') is not None}
 surf=cairo.RecordingSurface(cairo.CONTENT_COLOR_ALPHA,None);ctx=cairo.Context(surf);pieces=[]
 def shape(d,matrix,stroke=False,sw=0):
  def point(x,y):
   a,b,c,d,e,f=matrix;return a*x+c*y+e,b*x+d*y+f
  it=iter(re.findall(r'[A-Za-z]|[-+]?(?:\d*\.\d+|\d+\.?\d*)(?:[eE][-+]?\d+)?',d));q=ctx;q.new_path();q.set_tolerance(.045)
  for cmd in it:
   if cmd=='Z' or cmd=='z':q.close_path();continue
   n={'M':2,'L':2,'C':6}[cmd];p=[float(next(it))for _ in range(n)]
   pts=[point(p[i],p[i+1])for i in range(0,n,2)]
   if cmd=='M':q.move_to(*pts[0])
   if cmd=='L':q.line_to(*pts[0])
   if cmd=='C':q.curve_to(*[f for pair in pts for f in pair])
  full=q.copy_path();flat=q.copy_path_flat();segs=[];total=0.;at=None;orig=None
  for ty,pt in flat:
   if ty==cairo.PATH_MOVE_TO:at=orig=pt
   else:
    end=orig if ty==cairo.PATH_CLOSE_PATH else pt
    if at is None or end is None:continue
    ll=math.dist(at,end)
    if ll>0:segs.append((at,end,total,ll));total+=ll
    at=end
  if total:
   x0,y0,x1,y1=q.path_extents();pieces.append((.5*(x0+x1),full,segs,total,stroke,sw))
 def visit(node):
  kind=node.tag.split('}')[-1]
  if kind=='defs':return
  if kind=='use':
   k=node.attrib['{http://www.w3.org/1999/xlink}href'][1:];shape(defs[k],(1,0,0,1,float(node.get('x',0)),float(node.get('y',0))))
  elif kind=='path':
   m=re.search(r'matrix\(([^)]+)\)',node.get('transform',''));mm=tuple(map(float,re.findall(r'[-+.\deE]+',m[1])))if m else(1,0,0,1,0,0)
   shape(node.attrib['d'],mm,node.get('fill')=='none',float(node.get('stroke-width',0)))
  else:
   for f in node:visit(f)
 visit(svg);return vb,sorted(pieces,key=lambda p:p[0])
def texwrite(g,tag,x,y,w,t,d=.70,col=F,op=1):
 if t<0 or op<.002:return
 (x0,y0,vw,vh),pieces=outlines(tag);cc=g.c;cc.save();sc=w/vw;cc.translate(x-w*.5,y-vh*sc*.5);cc.scale(sc,sc);cc.translate(-x0,-y0)
 progress=min(1,t/d);lag=.60
 for i,(_,raw,segments,total,line_only,sw)in enumerate(pieces):
  z=clip((progress-lag*i/max(1,len(pieces)-1))/(1-lag))
  if z<=0:continue
  fill=phase(z,.37,1) if z<1 else 1.
  if fill:
   cc.new_path();cc.append_path(raw);g.source(col,op*fill)
   if line_only:cc.set_line_width(sw);cc.stroke()
   else:cc.fill()
  if z<.9999:
   length=total*min(1,z/.69);cc.new_path()
   for a,b,start,ll in segments:
    if start>=length:break
    kk=min(1,(length-start)/ll);cc.move_to(*a);cc.line_to(mix(a[0],b[0],kk),mix(a[1],b[1],kk))
   g.source(col,op*(1-fill));cc.set_line_width(max(.18,1.22/sc));cc.set_line_cap(cairo.LINE_CAP_ROUND);cc.stroke()
 cc.restore()
