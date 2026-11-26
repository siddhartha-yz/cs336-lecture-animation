"""A test score becomes a steering signal before a single explanatory word is added."""
from rig4 import *
from motion import curtain,guide

YVAL=(36,41,47,57,64,71,78,82)
TV=(40,46,53,59,55,51,46,41)
N=len(YVAL)
@lru_cache(4)
def cues(c):
 return [0.,c.at('评测榜单')-.29,c.at('用户面前')+.51,c.at('反而比上个月')+.49,
         c.at('盯住右边')+.22,c.at('改动就被留下')+.38,c.at('下一轮从这里')+.47,
         c.at('训练后的例行')+.48]
def draw(g,c):
 t=c.t;A=c.at;chart=FlowClock(cues(c),(1.3,2.12,2.88,4.6,4.96,5.4,6.35,7.0))
 begin=enter(t,-.10,.65)
 explain=A('盯住右边');keep=A('改动就被留下');no=A('没投票权');ret=A('下一轮从这里')
 place=A('评测排在最前面');action=A('训练就朝哪儿');where=A('把尺子画成')
 # Dolly the chart to the side as the same samples enter the accept/reject mechanism.
 shift=phase(t,explain-.71,explain+.38)
 lens=phase(t,place-.21,place+.73);end=phase(t,c.d-.83,c.d-.10)
 old=(1-lens)*(1-end);letters=old*(1-phase(t,place-.47,place-.14));sc=mix(1,.718,shift)
 xl=144.;xr=mix(1393,1104,shift);bottom=mix(663,644,shift);height=mix(460,397,shift)
 X=lambda i:xl+(xr-xl)*i/(N-1)
 Yf=lambda v:bottom-height*v/100
 a=chart(t);n=min(N-2,int(a));u=a-n
 if old:
  path(g,[(xl,bottom-height-23),(xl,bottom),(xr+27,bottom)],begin,M,2.05,old*.76)
  for v in (0,50,100):
   y=Yf(v);line(g,(xl-9,y),(xl+2,y),M,1.6,begin*old)
   label(g,str(v),xl-18,y,25,M,old*begin,'right')
  lab=enter(t,A('评测榜单')-.51,.72)
  for j,(val,co) in enumerate(((YVAL,Y),(TV,C))):
   seq=[(X(k),Yf(v))for k,v in enumerate(val)];actual=lerp(seq[n],seq[n+1],u)
   pts=seq[:n+1]+[actual]
   if j and len(seq)>4 and n>=3:
    q=1-old*.16
    path(g,pts[:4],1,C,3.6,old*q)
    path(g,pts[3:],1,R,3.65,old*q)
   else:path(g,pts,1,co,3.8,old*.97)
   if j and n>=3:co=R
   point(g,*actual,8.6,co,old)
   # Fixed lanes keep curve labels independent of changing data heights.
   cx,cy=actual;px=mix(80,-81,phase(a,4.39,5.50));end0=(cx+px*.58,cy+(-53 if not j else 53))
   path(g,[actual,(mix(cx,end0[0],.48),mix(cy,end0[1],.73)),end0],lab,co,1.6,old*lab*.76)
   label(g,('基准分数','未见题目')[j],cx+1.33*px,end0[1]-16*(1-abs(px)/81),37*mix(1,.80,shift),co,lab*letters)
   if keep-.38<t<place and ((j==0 and ret-.23<t<ret+.48) or (j==1 and no-.35<t<no+.56)):
    q=math.exp(-((t-(ret if not j else no))/.32)**2)
    ring(g,*actual,13.8+9*q,co,old*q,2.6)
  label(g,'训练更新 · 示意',xr,bottom+44,26,M,old*begin,'right')
  if shift:
   lab=c.u('黄线一抬头',.55);vv=old*lab
   gx=1197;yy=213;w=274
   line(g,(gx,yy+103),(gx+w,yy+103),Y,2.0,vv*.85)
   line(g,(gx,yy+309),(gx+w,yy+309),M,1.7,vv*.65)
   label(g,'计入筛选',gx,yy+10,27,Y,lab*letters,'left');label(g,'不投票',gx,yy+270,27,R,lab*letters*c.u('没投票权'),'left')
   gate=enter(t,keep-.14,.67);gg=enter(t,no-.13,.64)
   for j in range(5):
    prog=enter(t,keep-.31+j*.48,.44);rx=gx+27+j*47;hh=(21,32,25,45,39)[j]
    # The five thumbnails are trend evidence, not another model or decimal series.
    if prog:rect(g,rx,yy+102-hh*prog,20,hh*prog,Y,vv*prog*.94)
    ll=enter(t,no-.27+j*.22,.46)
    if ll:rect(g,rx,yy+311,20,(35,16,30,24,38)[j]*ll,R,old*ll*.86)
    if gate:check(g,rx+9,yy+108+34,7,True,old*prog*gate)
   route=(lerp((X(5),Yf(YVAL[5])),(X(7),Yf(YVAL[-1])),enter(t,ret-.32,.55)),(1176,Yf(YVAL[-1])),(1176,315),(1190,315))
   if keep-.1<t<place-.32:
    e=easepos(t,keep-.12,.70)
    path(g,route,e,Y,2.3,old*e*.66)
    q=phase(t,keep-.12,ret+.52)
    if 0<q<1:guide(g,route,q,Y,old*.93,3,.20)
   if gg:
    x=1155;y=yy+309;line(g,(x-18,y-21),(x+18,y+15),R,3.,old*gg)
    line(g,(x-18,y+15),(x+18,y-21),R,3.,old*gg)
   # From the existing score, one accepted update crosses the routine check.
   # Its later position becomes the same gold input of the feedback loop.
   before=A('训练后的例行');loop=A('工程闭环')
   u=enter(t,before-.43,.83);progress=easepos(t,before-.41,1.14)
   if before-.43<=t<=loop+.39:
    p2=(1195,342);finish=(1466,342)
    path(g,[p2,finish],progress,Y,2.3,u*old*.69)
    if progress<.999:point(g,*lerp(p2,finish,progress),5.65,Y,u*old)
    v=enter(t,A('例行检查')-.16,.59)
    if v:check(g,1475,342,12,True,v*old)
 if lens:
  # Turn a check at the end of a line into feedback at its input. Position and
  # direction are the explanation; just the two actors keep their short names.
  x1,y1=447,432;x2,y2=1118,430;f=lens*(1-end)
  a0=enter(t,place-.21,.52)
  rect(g,x1-129,y1-45,258,90,inkcol(C,.48),f*a0);label(g,'训练',x1,y1,43,C,f*a0)
  rect(g,x2-121,y2-45,242,90,inkcol(Y,.27),f*a0);label(g,'评测',x2,y2,43,Y,f*a0)
  pts=[(x1+131,y1),(x1+250,y1),(x2-121,y2)]
  route=[(x2+3,y2-45),(x2+3,268),(x1+12,268),(x1+12,y1-44)]
  path(g,pts,a0,T,3.43,f*.87)
  back=phase(t,where-.23,action+.32);path(g,route,back,Y,3.55,f)
  if back:guide(g,route,back,Y,f,5.6,.27)
  halo=phase(t,action-.11,c.d-1.04)
  if halo:ring(g,x1,y1,90+29*halo,C,f*sin(pi*halo)**.55,2.45)
 loop=A('工程闭环')
 if loop-.03<t<place+.46:
  r=easepos(t,loop-.03,place-loop+.46);a=during(t,loop-.03,place+.46,.31)
  xx,yy=transit((1475,342),(1118,430),r,57.5)
  point(g,xx,yy,7.6,Y,a)
 if end:
  # Start the next measuring apparatus at its true first camera, with the same scale.
  from v4_act0 import projection
  c0=cue('0-2');held=c0.t
  try:
   c0.t=0.
   curtain(g,end,lambda:projection(g,c0))
  finally:c0.t=held
