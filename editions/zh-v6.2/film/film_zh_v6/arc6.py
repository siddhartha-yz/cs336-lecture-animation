"""Place real tiles under a candidate transform; check the same three examples."""
from rig4 import *
from studio_tests import AR,arcboard,PAL,tile
from motion6 import ArcLength
from functools import lru_cache
SYMS=('原样','上下翻转','转半圈','左右翻转')
COL=(C,V,O,T)
def _result(a,i):
 if not i:return a
 if i==1:return a[::-1]
 if i==2:return [r[::-1]for r in a[::-1]]
 return [r[::-1]for r in a]
@lru_cache(1)
def outcomes():
 return tuple(tuple(_result(r['input'],i)==r['output']for r in AR['train'])for i in range(4))
def hypothesis(g,c,op):
 r=AR['train'][0];t=c.t;roll=c.at('不妨盯住同一行');wrong=c.at('那一格颜色')
 st=c.at('旋转半圈');snag=c.at('合理的猜法');other=[a[::-1]for a in r['input'][::-1]]
 xx,xx2,y,sz=992,1300,415,207
 turn=easepos(t,roll-.14,.96);see=enter(t,roll+.22,.60)*op
 mark(g,'转半圈',xx,613,29,t-roll+.08,O,op=op)
 mark(g,'例 I 的输出',xx2,613,29,t-roll-.10,C,op=see)
 ctx=g.c;ctx.save();ctx.translate(xx,y);ctx.rotate(turn*pi)
 arcboard(g,r['input'],0,0,sz,op)
 # This specific original corner was at the top. Its screen location is
 # rotated with the original tile, not rounded to the closest target cell.
 q=enter(t,roll-.11,.54);k=sz*.375;f=sz*.25
 box(g,-k-f*.5+3,-k-f*.5+3,f-6,f-6,Y,op*q,sw=3.15)
 ctx.restore()
 arcboard(g,r['output'],xx2,y,sz,see)
 q=enter(t,snag-.16,.50)
 if q:
  # This very cell should stay on the top row under the real rule.
  box(g,xx2+k-f*.5+3,y-k-f*.5+3,f-6,f-6,Y,op*q,sw=3.15)
 wrong0=enter(t,wrong-.19,.61)
 if wrong0:
  cx,cy=xx+k,y+k;dx=xx2+k;dy=y-k
  ride=during(t,wrong-.19,wrong+2.15,.47)
  pts=[(cx+26,cy-13),(cx+58,cy-30),(dx-50,dy+73),(dx-12,dy+29)]
  if ride:path(g,pts,wrong0,R,2.6,op*ride)
  ring(g,xx2+k,y-k,8,R,op*ride*.8,2.1)
  label(g,'跑到了下面',xx,696,27,R,op*wrong0)
 
def branch(g,c,st,limit):
 t=c.t
 a=enter(t,st,.64);grow=easepos(t,st-.22,1.12)
 expand=c.at('展开搜索');choose=c.at('提出几种候选变换')
 verify=c.at('前面几个示例');prune=c.at('不合的枝条');time_=c.at('时间和算力')
 cx,cy,sz=mix(560,382,grow),mix(425,446,grow),mix(353,298,grow)
 r=AR['test'][0]
 arcboard(g,r['input'],cx,cy,sz)
 cap=1-easepos(t,st,.74)
 label(g,'候选规则演算',cx+sz*.68,cy-37,33,T,cap,'left')
 label(g,'把猜想拿回三个例子去验',cx+sz*.68,cy+15,25,M,cap,'left')
 lab_op=a*enter(t,expand-.13,.56)
 if lab_op:
  label(g,'同一张新输入',cx,cy+sz*.55+37,27,C,lab_op)
  bar=enter(t,expand-.11,.54);path(g,[(cx+sz/2+12,cy),(659,cy),(686,414)],bar,C,2.4,lab_op*.75)
  dot(g,686,414,4.5,C,lab_op*bar)
 xpos=909;yy=(204,352,499,647);guesses=outcomes()
 for i,(y,col,lab) in enumerate(zip(yy,COL,SYMS)):
  launch=choose-.31+i*.182
  f=enter(t,launch,.64);dead=easepos(t,prune-.02+i*.12,.69) if not all(guesses[i]) else 0
  if f<.001:continue
  sem=f*(1-.78*dead)
  pts=[(686,414),(734,414+(y-414)*.33),(795,y),(xpos-49,y)]
  path(g,pts,easepos(t,launch,.85),col,2.8,sem)
  h=clip((t-launch)/1.11)
  if .02<h<.96:
   bx,by=ArcLength(pts).at(easepos(t,launch,1.11));point(g,bx,by,4.9,col,sem)
  rect(g,xpos-24,y-20,48,41,inkcol(col,.74),sem)
  # Tiny preview of each candidate on the target; validation below is only from
  # examples, so the result is not used as evidence for the selected branch.
  motion=easepos(t,launch+.31,.65)
  arcboard(g,_result(r['input'],i),xpos,y,45,sem*motion)
  label(g,lab,xpos+61,y,30,col,sem,'left')
  if dead:
   x0=xpos+41;x1=xpos+207
   path(g,[(x0,y+16),(x1,y+10)],dead,R,2.25,dead*.76)
  if t>verify-.26:
   tri=enter(t,verify-.24,.66)
   for j,ok in enumerate(guesses[i]):
    check(g,1209+j*81,y,12,ok,enter(t,verify-.05+i*.084+j*.125,.39)*tri*(1-.50*dead))
 # Each column is one visible observation. Keep its width the same when the
 # branches retire, while the surviving rule gains physical weight.
 colop=enter(t,verify-.29,.54)
 for j,row in enumerate(AR['train']):
  x=1209+j*81
  if colop:
   arcboard(g,row['output'],x,113,38,colop*.67)
   label(g,('I','II','III')[j],x,158,22,M,colop)
 if t>time_-.15:
  beam=easepos(t,time_-.20,1.56)
  pts=[(686,414),(734,491),(795,647),(1090,647),(1161,683),(1390,683)]
  path(g,pts,beam,T,4.1,.92)
  if 0<beam<.99:point(g,*ArcLength(pts).at(beam),6.8,T)
  label(g,'三组都通过',1270,731,27,T,enter(t,time_+.74,.52))

def actual_output(g,t,begin,x0,y0,side0,x1,y1,side1,opacity=1.):
 """Bring the original cells to their exact mirrored destinations after the guess."""
 raw=AR['test'][0];inp=raw['input'];out=raw['output']
 n=len(inp);m=len(inp[0]);u0=side0/max(n,m);u1=side1/max(n,m)
 x0,y0=x0-u0*(m-1)/2,y0-u0*(n-1)/2
 x1,y1=x1-u1*(m-1)/2,y1-u1*(n-1)/2
 # Only outlines show at the first reveal frame. Every saturated tile that
 # arrives is attached to an already visible cell in the original input.
 if t<begin+1.55:arcboard(g,out,x1+u1*(m-1)/2,y1+u1*(n-1)/2,side1,open_=0,op=opacity)
 for i,row in enumerate(inp):
  for j,co in enumerate(row):
   assert co==out[i][m-j-1]
   at=begin+.035+.17*i+.11*j
   tpx,tpy=x1+(m-1-j)*u1,y1+i*u1
   start=(x0+j*u0,y0+i*u0)
   v=easepos(t,at,.74)
   if not v:continue
   if v<1:
    xx,yy=transit(start,(tpx,tpy),v,23+(j-1)*31.)
    r=mix(14.,u1-3.,clip(v*1.21-.21))
    tile(g,xx-r*.5,yy-r*.5,r,PAL[co],opacity*enter(t,at,.21))
   else:
    r=u1-3.
    tile(g,tpx-r*.5,tpy-r*.5,r,PAL[co],opacity)
