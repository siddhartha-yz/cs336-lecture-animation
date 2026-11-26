"""One drawing, two elevations. Dimensions derive from the same reel mesh as the perspective view."""
from ink import *
from ink_words import swish
from studio_examples import pstep,area,VIO,BLUE
from studio_field import reel
from studio_encounter import medical
from mounting import etch
def elevation(g,x,y,sc,side,q,a):
 ctx=g.c;ctx.save();ctx.translate(x,y);ctx.scale(sc,sc)
 def l(p1,p2,co=T,w=2):path(g,[p1,p2],q,co,w,a)
 if side=='end':
  for r in (96,51,7.4):arc(g,0,0,r,-pi/2,-pi/2+tau*q,C,2.3,a)
  for sgn in(-1,1):
   l((0,0),(sgn*104,135),O);l((sgn*104,135),(sgn*118,139),O)
  l((-118,139),(118,139),O)
 else:
  for xx in(-86,86):
   for sx in(-4,4):l((xx+sx,-96),(xx+sx,96),T,1.6)
   l((xx-4,96),(xx+4,96),T);l((xx-4,-96),(xx+4,-96),T)
  for h in(-51,51):l((-80,h),(80,h),C)
  for h in(-7.4,7.4):l((-163,h),(163,h),O,1.7)
  for sx in(-127,127):l((sx,0),(sx,139),O,2.8)
 ctx.restore()
def industry(g,c):
 t=c.t;a=c.at;node=a('圈对一个字母');draw=a('交上一张');src=a('一堆材料');eco=a('生态效度');data=a('GDPval');re=a('卷筒参数');jig=a('夹具的设计图');med=a('斯坦福')
 if t>=med-.34:medical(g,c)
 if t>=med-.12:return
 pull=phase(t,node-.19,node+.68);spin=phase(t,draw-.45,src+.93);dock=phase(t,data-.24,re+.31);guide=phase(t,src-.3,src+.68);out=1-phase(t,med-.64,med-.27)
 if spin<1:
  op=1-spin;xx=340+19*pull;yy=391
  for j,ch in enumerate('ABCD'):
   xx0=130+j*107;txt(g,ch,xx0,yy,54,Y if j==2 else M,op*(1-phase(t,draw-.68,draw-.12)))
  arc(g,344,yy,42,-.85*pi,-.85*pi+tau*max(.001,pull),Y,3.6,op)
 # The circled C and the emerging end face align momentarily; engineering drawing takes over the screen.
 a0=pstep(t,draw-.37,.62);cx=mix(344,840,spin)-250*dock;cy=mix(391,379,spin)+37*dock
 if a0:
  q=phase(t,draw+.27,src+2.09);th=1.53-.91*q+.31*phase(t,eco,eco+2.92)-.32*dock
  mag=mix(1.34,2.11,spin)-.49*dock
  reel(g,cx,cy,mag,th,out*a0)
  # Project the same two flange rims as the mesh. Carry their separation into the
  # open space above-left, rather than writing across the brass legs or caption lane.
  if guide:
   def rim(x):
    by,cz=32.,-90.51
    return (cx+mag*(x*cos(th)+cz*sin(th)),cy+mag*(-.89*by+(-x*sin(th)+cz*cos(th))*.43))
   near,far=rim(-86),rim(86);dx=far[0]-near[0];dy=far[1]-near[1];ll=hypot(dx,dy)or 1;nx,ny=dy/ll,-dx/ll
   po=lambda v,r:(v[0]+nx*r,v[1]+ny*r)
   n1,n2=po(near,35*mag),po(far,35*mag);fade=out*guide*(1-dock)
   for v in (near,far):
    path(g,[po(v,5),po(v,35*mag+8)],guide,O,1.15,fade*.75)
   path(g,[n1,n2],guide,O,2.3,fade)
   if guide>.55:
    for v in (n1,n2):line(g,po(v,-6),po(v,6),O,1.65,fade)
    etch(g,'卷筒宽度',n1[0]-17,n1[1]+7,26,O,fade,'right')
  if t>=eco-.12 and dock<.97:
   xx,yy=cx+mag*117,max(160.,cy-96*mag)
   line(g,(xx-46,yy+67),(xx,yy),T,1.7,out*(1-dock))
   etch(g,'生态效度',xx+12,yy-9,29,T,out*(1-dock))
   etch(g,'图纸能用来加工，才算交付',xx+13,yy+31,24,M,out*(1-dock))
 if dock:
  # Two elevations are close and linked by construction lines because aligned edges are the evidence.
  xx=1130;top=288;bot=584;sc=.90;bb=out*dock
  elevation(g,xx,top,sc,'end',dock,bb);elevation(g,xx,bot,sc,'side',dock,bb)
  for i in(-1,1):line(g,(xx+i*sc*96,top+sc*124),(xx+i*sc*96,bot-sc*99),E,.96,bb)
  k=pstep(t,jig-.21,.59)
  path(g,[(xx+91,top),(xx+127,top-33),(xx+224,top-33)],k,C,1.7,bb)
  if k:etch(g,'直径',xx+154,top-56,25,C,bb)
  etch(g,'GDPval · 制造工程交付物',xx+180,715,28,O,bb,'right')
  path(g,[(cx-65,cy-91),(251,214),(135,214)],dock,T,1.45,bb*.85)
  etch(g,'卷盘支架 · 结构示意',131,187,25,M,bb)
