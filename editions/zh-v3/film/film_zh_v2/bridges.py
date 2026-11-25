"""Seams exchange one identity. A departing caption is erased before incoming type is drawn."""
from ink import *
from motion import *
from cut_common import stage
cache={}
# Visible anchor, destination, colour, motif: each pair refers to the adjacent objects.
ports={
 '3-1':((1128,426),(1080,411),T,'equal'),'3-2':((1171,331),(1225,434),Y,'options'),
 '3-3':((935,445),(390,425),C,'diamond'),'3-4':((1260,486),(230,444),Y,'sieve'),
 '4-2':((948,437),(750,451),V,'curve'),'4-3':((1394,283),(800,369),V,'diamond'),
 '4-4':((1139,410),(576,459),V,'curve'),'5-1':((1230,571),(314,443),C,'patch'),
 '5-2':((1070,479),(747,429),T,'patch'),'5-3':((1093,485),(496,371),G,'sample'),
 '5-4':((492,460),(346,365),C,'patch'),'6-2':((800,590),(317,452),Y,'grid'),
 '6-3':((1370,399),(432,411),V,'doc'),'6-4':((979,642),(459,448),R,'sample'),
 '7-1':((829,426),(270,411),T,'doc'),'7-2':((901,411),(431,413),C,'doc'),
 '7-3':((1418,496),(521,387),Y,'window'),'7-4':((1132,581),(337,427),Y,'window'),
 '7-5':((1232,433),(335,469),C,'date'),'8-1':((1125,462),(800,288),Y,'curve'),
 '8-2':((800,471),(800,405),C,'volume')}
def frames(old,width,state,raw,surface):
 key=(old,width)
 if key not in cache:
  if len(cache)>2:cache.clear()
  dur=state(old)[0]['duration'];pair=[]
  for blank in (False,True):
   sf,other=surface(width);other.no_text=blank;raw(other,old,dur-1/60);sf.flush();pair.append(sf)
  cache[key]=pair
 return cache[key]
def raster(g,s,w,a=1,scale=1,dx=0,dy=0,anchor=(800,450)):
 if a<.002:return
 ctx=g.c;ctx.save();ctx.translate(anchor[0]+dx,anchor[1]+dy);ctx.scale(scale,scale);ctx.translate(-anchor[0],-anchor[1]);ctx.scale(1600/w,1600/w);ctx.set_source_surface(s,0,0)
 if a>=.999:ctx.paint()
 else:ctx.paint_with_alpha(a)
 ctx.restore()
def motif(g,tag,a,b,k,op,col):
 if op<.002:return
 x,y=transit(a,b,k,36 if tag in ('patch','window','equal') else 67);r=11+10*sin(pi*k)
 if tag in ('doc','patch','date'):docs(g,x-r*.82,y-r*1.20,1.64*r,2.40*r,col,op,2,2)
 elif tag=='diamond':g.poly([(x,y-r),(x+r,y),(x,y+r),(x-r,y)],col,1.9,op,True,inkcol(col,.16),1)
 elif tag in ('window','options','grid'):
  for j in range(3 if tag=='options' else 4):
   w=(r*.75 if tag!='window' else 11);xx=x+(j-1.5)*(w+3);box(g,xx,y-r*.55,w,r*1.1,col,op*(1-j*.08),sw=1.6)
 elif tag=='curve':
  pts=[(x+(j/20-.5)*r*3.2,y-r*(1/(1+exp(-6*(j/20-.5)))-.5)*1.7) for j in range(21)];path(g,pts,1,col,2.1,op);dot(g,x,y,3,col,op)
 elif tag=='equal':
  line(g,(x-r,y-4),(x+r,y-4),col,2,op);line(g,(x-r,y+4),(x+r,y+4),col,2,op)
 else:ring(g,x,y,r*.72,col,op,2);dot(g,x,y,3.7,col,op)
def bridge(g,id,t,state,raw,surface,ids):
 duration=1.27 if id[2]=='1' else .99
 if id=='8-2':return  # the same seven instruments continue their orbit inside finale.return_home
 if id in ('4-1','6-1'):
  if t<2.20:
   from boards import carry
   carry(g,id,t)
  return
 if id in ('3-2','5-2','7-4'):
  from wetjoins import exam,repository,match
  fn,cap={'3-2':(exam,1.35),'5-2':(repository,1.91),'7-4':(match,1.46)}[id]
  if t<cap:
   old=ids[ids.index(id)-1];width=g.c.get_target().get_width()
   prev,_=frames(old,width,state,raw,surface);fn(g,t,prev,width,raster,raw)
  return
 if t>=duration:return
 old=ids[ids.index(id)-1];width=g.c.get_target().get_width();prev,wire=frames(old,width,state,raw,surface)
 a,b,col,tag=ports[id];u=t/duration
 # At t=0 the outgoing actual last pose is intact; no inter-title or inserted black frame.
 if u<.18:
  raster(g,prev,width);raster(g,wire,width,phase(u,.012,.18));return
 # The new structure may start arriving before the old stroke is gone; neither has text.
 ctx=g.c;stage(g)
 k=phase(u,.17,.81);v=phase(u,.44,.90)
 if k<1:raster(g,wire,width,1-k,.997-.052*k,5*k,-5*k,a)
 if v>0:
  ctx.save();ctx.push_group();g.no_text=True
  try:raw(g,id,t)
  finally:g.no_text=False
  ctx.pop_group_to_source();ctx.paint_with_alpha(v);ctx.restore()
 if u>.79:
  opacity=phase(u,.79,1.);ctx.save();ctx.push_group();raw(g,id,t);ctx.pop_group_to_source();ctx.paint_with_alpha(opacity);ctx.restore()
 p=phase(u,.16,.91);op=phase(u,.14,.30)*(1-phase(u,.77,.96))
 motif(g,tag,a,b,p,op,col)
