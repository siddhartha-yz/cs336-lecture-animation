"""A repeated passage in two independent streams, then the door to one of them closes.
The observable data are scores of the four items, not alleged recoveries of training records."""
from ink import *
from motion import transit
from studio_examples import area,pstep,VIO
from mounting import etch
from timeline3 import remap
from studio_field import shuf
from validity import QNAME,QC
def glyph(g,j,xx,yy,r,co,u,a):
 if a<.001:return
 # A few specific objects from the four published topic examples.
 ctx=g.c;ctx.save();ctx.translate(xx,yy);ctx.scale(r,r)
 if j==0:
  area(g,[(-20,4),(-10,-11),(9,-11),(20,4),(6,15),(-13,12)],inkcol(co,.75),a)
  for x in(-10,10):g.circle(x,-10,6,co,alpha=a);dot(g,x+1,-11,2,BLACK,a)
  arc(g,1,3,7,.1*pi,.91*pi,F,1.2,a)
 elif j==1:
  etch(g,'E',0,-4,36,co,a,'center');arc(g,0,0,25,-.4*pi,1.30*pi,co,2,a)
 elif j==2:
  g.rect(-22,-17,44,33,inkcol(co,.64),co,1.8,0,a)
  for y in(-13,12):
   for x in(-16,-6,4,14):rect(g,x,y,4,3,BLACK,a)
  area(g,[(-5,-8),(8,0),(-5,8)],F,a)
 else:
  area(g,[(-26,3),(-15,-8),(1,-12),(12,-8),(22,0),(29,5),(27,13),(-26,13)],co,a)
  for x in(-16,18):g.circle(x,11,5,BLACK,co,1.6,a)
 ctx.restore()
def shuffle(g,c):
 a=c.at;t=c.t;ta=a('公开试题');meet=a('混进训练语料');concept=a('数据污染');score=a('高分');hide=a('训练集不公开');key=a('题序的可交换性');take=a('取一组');orig=a('原始顺序')
 # Physical items go into the permutation apparatus on the phrase which introduces it.
 hand=phase(t,take-.27,take+.73)
 if hand>=1:
  from direct import state
  b=state('7-2')[1];shuf()(g,b.clock(remap('7-2',c.t)));return
 choose=phase(t,ta-.15,ta+.54);m=phase(t,meet-.09,meet+.85);h=phase(t,hide-.10,hide+.82);k=phase(t,key-.21,key+.65)
 x0=198;y0=217;ww=542;bs=(235,338,441,544);sel=1
 # The left ink survives the shutter, then each coloured item goes to its actual order position.
 for j,(ss,col)in enumerate(zip(QNAME,QC)):
  z=pstep(t,.14+.10*j,.48);x,y=transit((x0+28*j,bs[j]),(301,252+j*57),hand,23+j*6)
  glyph(g,j,x,y,1.12-.43*hand,col,1,z);etch(g,ss,x+54,y,38-12*hand,F,z)
  if j==sel and m:
   w=phase(t,concept-.34,concept+.39);line(g,(x+47,y+32),(x+47+m*206,y+32),R,3.2,w*(1-hand))
 if choose:etch(g,'公开试题',x0-24,635,30,C,choose*(1-hand))
 if hand<1:
  # A real piece of repeated content: it is the same colour, term and shape before and after crossing.
  col=QC[sel];ctx=g.c;ctx.save();ctx.translate(1102,391);ctx.rotate(-.095)
  for i in range(12):
   y=-195+i*30;st=-228+((i*23)%77)
   for j in range(6+(i%3)):
    if i==5:continue
    x=st+j*54;w=21+(19*j+31*i)%29;rect(g,x,y,w,7,('#438DAD','#5A8C83','#8C75A2')[i%3],(1-h)*(.65 if i in (3,4,6,7)else .41)*(1-hand))
  ctx.restore()
  f=phase(t,meet-.1,concept+.03)
  if f and h<1:
   xp,yp=transit((x0+28*sel,bs[sel]),(961,356),f,69);glyph(g,sel,xp,yp,1.13,col,1,(1-h)*(1-hand))
   etch(g,QNAME[sel],xp+49,yp,39,F,f*(1-h)*(1-hand))
  q0=phase(t,concept-.14,concept+.58)
  if q0 and h<1:
   path(g,[(954,388),(1240,388),(1298,420)],q0,R,2.6,(1-h)*(1-hand))
   etch(g,'数据污染',1297,449,31,R,q0*(1-h)*(1-hand),'right')
  if h:
   for j in range(9):
    p=clip(h*1.36-j*.045);x=853+j*63;up=179-11*cos(j*.7);bot=567+17*sin(j*.6)
    g.poly([(x,up),(x+57,up-6),(x+57,up+p*(bot-up)-5),(x,up+p*(bot-up))],'#67879B',1.2,(1-hand)*p,True,inkcol('#587C91',.41+.09*(j%3)),1)
   etch(g,'训练集不可读',1121,374,42,F,h*(1-hand),'center')
   if k:
    path(g,[(1120,518),(1120,574),(993,616)],k,C,2.25,1-hand)
    etch(g,'仍能读 log P',986,644,31,C,k*(1-hand),'center')
  else:etch(g,'训练语料 · 示意',1180,635,27,M,choose*(1-hand),'center')
