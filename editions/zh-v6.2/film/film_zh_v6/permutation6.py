"""The same 23 reorderings become the 23 points in the teaching example."""
from rig4 import *


def location(j):
 return (793+252*(j%3),238+48*(j//3))


def pair(g,x,y,col,alpha=1,ch=None):
 w=36;h=31
 for j in (0,1):
  xx=x+(-24 if not j else 24);box(g,xx-w/2,y-h/2,w,h,col,alpha,inkcol(col,.38 if not j else .18),1.6)
  if ch:label(g,ch[j],xx,y,19,F,alpha)
 line(g,(x-6,y),(x+6,y),col,2.65,alpha)


def group(g,x,y,perm,col,alpha=1,scale=1):
 for i,v in enumerate(perm):
  x0=x+(i-1.5)*37*scale;w=13.6*scale;h=13*scale;co=col[v]
  rect(g,x0-w-3*scale,y-h/2,w,h,co,alpha*.95)
  rect(g,x0+3*scale,y-h/2,w*.77,h,inkcol(co,.57),alpha)
  line(g,(x0-4*scale,y),(x0+4*scale,y),co,1.62,alpha)


def gather(g,c,perms,col,at):
 t=c.t;vis=enter(t,at-.13,.56)
 if not vis:return
 for j,p in enumerate(perms):
  x,y=location(j);f=enter(t,at+.038*j,.55);xx=mix(1044,x,p5(f));yy=mix(373,y,p5(f))-25*sin(pi*f)
  group(g,xx,yy,p,col,f*vis,.60+.40*f)
 title=enter(t,at+.16,.49)*(1-phase(t,c.at('把这些分数排开')-.78,c.at('把这些分数排开')-.21))
 label(g,'其余 23 种排列 · 示意',1034,174,29,C,title)


def score(g,c,perms,col,scored,X,at,ready):
 """Morph the banks, then keep the coordinates/readouts the same as the plain chart."""
 t=c.t;where={p:location(i)for i,p in enumerate(perms)};by={};placed=[]
 for i,(p,v) in enumerate(scored):
  x=X(v);snap=round((x-224)/26);level=by.get(snap,0);by[snap]=level+1;y=530-31*level
  z=easepos(t,at+.029*i,.93);sx,sy=where[p];xx,yy=transit((sx,sy),(x,y),z,25)
  k=1-phase(z,.35,.87);alpha=enter(t,ready+.038*perms.index(p),.55)
  if k:group(g,xx,yy,p,col,k*alpha,clip(1-.81*z))
  if z:dot(g,xx,yy,9.3,inkcol(C,.84),alpha*phase(z,.32,1))
  placed.append((x,y))
 return placed
