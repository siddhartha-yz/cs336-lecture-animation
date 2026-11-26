"""Cut on an actual edge. The two sets of letters never share a pixel at a cut.
A question is allowed to finish in the old world: no hint of its answer before the chapter door."""
from rig4 import *
IDS=list(BOOK);CACHE={};KINDS={
 '1-2':('budget',.71,0),
 '2-3':('oblique',.63,-1),'2-4':('iris',.78,(442,339)),
 '3-2':('leaf',.73,0),
 '4-3':('leaf',.70,1),'4-4':('part',.80,794),
 '7-3':('iris',.82,(1383,538)),
 '8-1':('iris',.82,(773,425)),'8-2':('socket',.88,(806,417))}
def seam(g,k,t,guide,drawclean):
 if k not in KINDS:return
 kind,d,anchor=KINDS[k]
 if t>=d:return
 j=IDS.index(k);old=IDS[j-1];wd=g.c.get_target().get_width();sig=(old,wd,guide)
 if sig not in CACHE:
  # Snapshot is a short exposure of the real outgoing picture. Never use a cached old
  # full frame as translucent foreground over the new labels.
  CACHE.clear();sf,og=prev.surface(wd);drawclean(og,old,BOOK[old]['duration']-1/60,guide);sf.flush();CACHE[sig]=sf
 ctx=g.c;ctx.save();img=CACHE[sig];q=p5(t/d);ctx.new_path()
 if kind in ('socket','facet','iris'):
  x,y=anchor;r=(q*.22+q*q*.78)*2100;ctx.rectangle(-8,-8,1616,916)
  if kind=='iris':ctx.new_sub_path();ctx.arc(x,y,max(.001,r),0,tau)
  else:
   n=6 if kind=='socket'else 4;theta=-pi/2+.15-.12*q
   vertices=[(x+r*cos(j*tau/n+theta)*(1.09 if n==4 else 1.14),y+r*sin(j*tau/n+theta))for j in range(n)]
   ctx.move_to(*vertices[0]);[ctx.line_to(*v)for v in vertices[1:]];ctx.close_path()
  ctx.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
 elif kind=='part':
  l=anchor-(anchor+12)*q;r=anchor+(1612-anchor)*q;ctx.rectangle(-8,-8,l+8,916);ctx.rectangle(r,-8,1616,916)
 elif kind=='strip':
  # The edge tracks the underlined unit or a mask. It never draws another horizontal title.
  y=-105+1118*q
  xy=[(-4,y-75),(1604,y+53),(1604,907),(-4,907)] if not anchor else [(-4,-7),(1604,-7),(1604,1004-y+51),(-4,1004-y-92)]
  ctx.move_to(*xy[0]);[ctx.line_to(*v)for v in xy[1:]];ctx.close_path()
 elif kind=='leaf':
  start=1910*(1-q)-60
  coords=[(-5,-5),(start+84,-5),(start-92,900),(-5,905)]
  if anchor:coords=[(1600-x,y)for x,y in coords]
  ctx.move_to(*coords[0]);[ctx.line_to(*v)for v in coords[1:]];ctx.close_path()
 else:
  x=-210+2006*q;sign=1 if anchor in(0,1)else -1
  xy=[(x-100*sign,-5),(1605,-5),(1605,905),(x+100*sign,905)]
  ctx.move_to(*xy[0]);[ctx.line_to(*v)for v in xy[1:]];ctx.close_path()
 ctx.clip();ctx.scale(1600/wd,1600/wd);ctx.set_source_surface(img,0,0);ctx.paint();ctx.restore()
