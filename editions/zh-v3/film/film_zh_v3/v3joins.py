"""Match cuts, moving apertures, and edges attached to the departing subject.
The matte is applied to the previous exposure: no new text is ever mixed through the old ink."""
from timeline3 import IDS,S
from ink import *
from motion import out3
from cut_common import cairo
CACHE={}
def link(g,k,t,raw,surface):
 j=IDS.index(k)
 if not j or t>=.78 or k in ('3-2','4-1','5-1','6-1','6-2','7-4','8-2'):return
 old=IDS[j-1];wd=g.c.get_target().get_width();sig=(old,wd)
 if sig not in CACHE:
  CACHE.clear();sf,oldg=surface(wd);raw(oldg,old,S[old]['duration']-1/60);sf.flush();CACHE[sig]=sf
 image=CACHE[sig];ctx=g.c;ctx.save()
 # Looking through the specimen and three paired score transitions require different optics.
 # The iris is shape-matched to the jewel, vote dot, commit or aperture, not a visual overlay.
 holes={'3-4':(570,421,'facet'),'4-2':(998,705,'circle'),'5-3':(1117,449,'hex'),'7-3':(1262,436,'lens'),'8-1':(1116,455,'circle')}
 if k in holes:
  x,y,shape=holes[k];q=clip(t/.73);r=1920*(.12*q+.88*q*q)
  ctx.new_path();ctx.rectangle(-5,-5,1610,910)
  if shape in ('circle','lens'):
   ctx.new_sub_path();ctx.arc(x,y,r,0,tau)
  else:
   n=6 if shape=='hex' else 4;tilt=.09 if shape=='facet' else .52
   pts=[(x+r*(1.15 if shape=='facet'else 1)*cos(i*tau/n-pi/2+tilt),y+r*sin(i*tau/n-pi/2+tilt))for i in range(n)]
   ctx.move_to(*pts[0])
   for xy in pts[1:]:ctx.line_to(*xy)
   ctx.close_path()
  ctx.set_fill_rule(cairo.FILL_RULE_EVEN_ODD);ctx.clip()
 else:
  p=out3(t/.64)
  if k in ('4-4','5-2'):coords=[(-300,0),(1880*(1-p)-130,0),(1880*(1-p)+140,900),(-300,900)]
  elif k in ('7-1','6-3'):coords=[(0,-60),(1600,-60),(1600,1090*(1-p)-40),(0,1090*(1-p)-205)]
  else:coords=[(1840*p-200,0),(1800,0),(1800,900),(1840*p-60,900)]
  ctx.new_path();ctx.move_to(*coords[0])
  for xy in coords[1:]:ctx.line_to(*xy)
  ctx.close_path();ctx.clip()
 ctx.scale(1600/wd,1600/wd);ctx.set_source_surface(image,0,0);ctx.paint();ctx.restore()
