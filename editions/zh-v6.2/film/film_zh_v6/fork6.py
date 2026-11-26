"""One keyed answer opens into several kinds of work, without a new title."""
from rig4 import *
from motion import guide
from motion6 import ArcLength

PORT=(799,465)
ARMS=((-453,-117,C),(3,-238,T),(440,-100,V))


def bezier(a,b,c,u):
 return tuple((1-u)**2*x+2*(1-u)*u*y+u*u*z for x,y,z in zip(a,b,c))


def terminal(g,x,y,r,co,op,phase_,typ):
 if op<.002:return
 n=(4,6,5)[typ];phi=.31-.38*phase_+.13*typ
 pts=[(x+r*math.cos(j*tau/n+phi),y+.68*r*math.sin(j*tau/n+phi))for j in range(n)]
 g.poly(pts,co,2.55,op,True,inkcol(co,.48),op)
 point(g,x,y,4.6,co,op)


def arm(g,where,co,a,u=1.):
 x,y=PORT;dx,dy=where[0]-x,where[1]-y;control=(x+.48*dx,y+.09*dy)
 full=[bezier(PORT,control,where,h/42)for h in range(43)]
 track=ArcLength(full)
 if not a:return full,track
 n=max(2,round(35*u));pts=[track.at(u*i/n)for i in range(n+1)]
 side=[];opposite=[]
 for i,(xx,yy) in enumerate(pts):
  last=pts[max(0,i-1)];after=pts[min(n,i+1)];mx=after[0]-last[0];my=after[1]-last[1];L=math.hypot(mx,my)
  k=(.5+7.6*u*i/n);vx,vy=-my*k/max(.01,L),mx*k/max(.01,L)
  side.append((xx+vx,yy+vy));opposite.append((xx-vx,yy-vy))
 g.poly(side+list(reversed(opposite)),None,0,a,True,inkcol(co,.41),a*.94)
 g.poly(pts,co,1.8,a*.75)
 return full,track


def draw(g,c,end):
 t=c.t;branch=c.at('许多任务');open_=c.at('开放式回答')
 lift=easepos(t,end-.08,.91);solo=enter(t,end-.12,.48)
 if solo:
  x,y=PORT;yy=mix(649,y,lift)
  if lift<.95:
   path(g,[(x,649),(x,y)],lift,Y,1.9,solo*(1-lift)*.93)
  point(g,x,yy,10.1,Y,solo)
 for j,(dx,dy,co)in enumerate(ARMS):
  st=branch-.12+.24*j;u=easepos(t,st,1.06)
  if not u:continue
  a=enter(t,st,.43);x,y=PORT;where=(x+dx,y+dy)
  full,track=arm(g,where,co,a,u);endpt=track.at(u);dot(g,*endpt,4.9,co,a)
  if u>.68:
   r=19+17*phase(u,.69,1.)
   terminal(g,*endpt,r,co,a*phase(u,.69,1.),u,j)
  second=easepos(t,open_-.16+.16*j,1.02)
  if .01<second<.995:
   guide(g,full,second,co,a*.94,6.25,.13)
   px,py=track.at(second);point(g,px,py,7,co,a*.92)
