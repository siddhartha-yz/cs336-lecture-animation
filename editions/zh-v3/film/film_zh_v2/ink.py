"""A small blackboard vocabulary. White is a reading, blue is an object, gold is a selected observation."""
from math import sin,cos,pi,tau,sqrt,exp,log,hypot
import math,random,json,bisect,re
from pathlib import Path
from functools import lru_cache,partial
from cut_common import SERIF,World,token_stage as _token_stage
from visual import blend
W=Path(__file__).resolve().parent
# The two sides of the Beat 1 → 2 cut use the same filmed probability readout.
# At a 390px display height, 32 board points gives even 0.0449% a readable face.
measured_token_stage=partial(_token_stage,probability_size=32)
C='#58C4DD';Y='#FFFF00';O='#F0AC5F';T='#5CD0B3';V='#C58AF9';G='#83C167';R='#FC6255';F='#FFFFFF';M='#C0C5CB';E='#626262';D='#333333';BLACK='#000000'
seq=(C,T,Y,V,O,G,R)
def clip(a):return min(1.,max(0.,a))
def ease(a):a=clip(a);return a*a*(3-2*a)
def mix(a,b,p):return a+(b-a)*p
def phase(x,a,b):return ease((x-a)/max(.0001,b-a))
def on(c,s,n=1.2,early=.15):return c.u(c.t,s,n,early)
def flow(t,start,end):return phase(t,start,end)
def pulse(t):return .5-.5*cos(t*tau)
def lerp(a,b,k):return (mix(a[0],b[0],k),mix(a[1],b[1],k))
def curve(a,b,p,bend=40):
 x,y=lerp(a,b,p); return x,y-bend*sin(pi*p)
def title(g,s,y=125,a=1,col=F,sub=None,size=47):
 txt(g,s,800,y,size,col,a)
 if sub:txt(g,sub,800,y+56,24,M,a)
def txt(g,s,x,y,fs=32,col=F,a=1,align='center',width=None,font=SERIF):
 if not s or a<.003:return
 s=str(s)
 if width:fs=min(fs,fs*width/max(1,g.measure(s,fs,font=font)))
 g.text(s,x,y,fs,col,min(1,a),align=align,font=font)
def note(g,label,x,y,col=C,align='left',a=1):
 txt(g,label,x,y,26,col,a,align)
def source(g,s,a=1):txt(g,s,1430,753,20,M,a,'right',1100)
def line(g,a,b,col=E,sw=2,op=1):g.line(*a,*b,col,sw,op)
def dot(g,x,y,r=5,col=C,a=1):g.circle(x,y,r,col,alpha=a)
def ring(g,x,y,r,col=C,a=1,sw=2):g.circle(x,y,r,None,col,sw,a)
def box(g,x,y,w,h,col=E,a=1,fill=None,sw=1.6):g.rect(x,y,w,h,fill,col,sw,0,a)
def rect(g,x,y,w,h,col=C,a=1):g.rect(x,y,w,h,col,alpha=a)
def inkcol(col,v):return blend(BLACK,col,clip(v))
def path(g,pts,k=1,col=C,sw=3,a=1):
 if len(pts)<2 or a<.003 or k<=0:return
 k=clip(k)*(len(pts)-1);i=int(k)
 q=list(pts[:i+1])
 if i+1<len(pts):q.append(lerp(pts[i],pts[i+1],k-i))
 if len(q)>1:g.poly(q,col,sw,a)
 return q[-1]
def arc(g,x,y,r,a0,a1,col=C,sw=3,op=1):
 if a1<=a0:return
 c=g.c;c.save();c.new_path();c.arc(x,y,r,a0,a1);g.source(col,op);c.set_line_width(sw);c.stroke();c.restore()
def arrow(g,a,b,k=1,col=C,a0=1,width=2):
 if k>.001:g.arrow(*a,*lerp(a,b,clip(k)),col,width,a0,10)
def check(g,x,y,r=14,ok=True,a=1):
 if ok:g.poly([(x-r,y),(x-.18*r,y+.72*r),(x+r,y-.84*r)],G,3,a)
 else:
  line(g,(x-r,y-r),(x+r,y+r),R,3,a);line(g,(x+r,y-r),(x-r,y+r),R,3,a)
def frac(g,x,y,num,den,size=33,op=1):
 ww=max(g.measure(num,size,font=SERIF),g.measure(den,size,font=SERIF))+24
 txt(g,num,x,y-size*.66,size,F,op);line(g,(x-ww/2,y),(x+ww/2,y),F,1.65,op);txt(g,den,x,y+size*.73,size,F,op);return ww
def ticks(g,x,y,w,n,col=E,op=1):
 line(g,(x,y),(x+w,y),col,1.6,op)
 for j in range(n):line(g,(x+j*w/(n-1),y-6),(x+j*w/(n-1),y+6),col,1.6,op)
def docs(g,x,y,w,h,col,op=1,lines=6,signature=0,active=-1):
 if op<.003:return
 fold=min(22,w*.11);g.poly([(x,y),(x+w-fold,y),(x+w,y+fold),(x+w,y+h),(x,y+h)],col,2,op,True,inkcol(col,.035),1)
 g.poly([(x+w-fold,y),(x+w-fold,y+fold),(x+w,y+fold)],col,1,op)
 for j in range(lines):
  size=w*(.39+.37*((11*j+3*signature)%13)/12)
  xx=x+w*.12;yy=y+h*(.21+j*(.62/max(lines-1,1)))
  line(g,(xx,yy),(xx+size,yy),Y if active==j else col,2.8 if w>150 else 1.8,op*(1 if active==j else .55))
def pins(g,x,y,w,h,n,m,col,t,a=1):
 for j in range(n*m):
  xx=x+(j%n)*w/(n-1 or 1);yy=y+(j//n)*h/(m-1 or 1)
  dot(g,xx,yy,2.9,col,a*(.36+.64*pulse(t*.2-j*.085)))
def voter(g,x,y,col=C,a=1,scale=1):
 ring(g,x,y-13*scale,9*scale,col,a,2)
 pts=[(x-18*scale,y+19*scale),(x-15*scale,y+6*scale),(x,y+2*scale),(x+15*scale,y+6*scale),(x+18*scale,y+19*scale)]
 g.poly(pts,col,2,a)
def polycube(g,x,y,rad,t,op=1,dims=(1.17,.88,.82)):
 # One tilted wireframe; the long and short edges are the axes introduced in Beat 0.
 az=.51+.20*sin(t*.16);el=.27+.09*sin(t*.13)
 def point(a,b,c):
  xx=a*cos(az)+c*sin(az);z=-a*sin(az)+c*cos(az)
  return x+rad*xx,y-rad*(b*cos(el)-z*sin(el)),b*sin(el)+z*cos(el)
 pts=[point(dims[0]*a,dims[1]*b,dims[2]*c) for a in [-1,1] for b in [-1,1] for c in [-1,1]]
 for face in [(0,1,3,2),(1,3,7,5),(2,3,7,6)]:
  g.poly([pts[j][:2] for j in face],C,0,op,True,inkcol(C,.11),1)
 for i,p in enumerate(pts):
  for bit in (1,2,4):
   j=i^bit
   if i<j:line(g,p[:2],pts[j][:2],C,2.5,op*(.49+.43*clip((p[2]+pts[j][2]+3)/6)))
 for p in pts:dot(g,*p[:2],3.3,C,op)
 return pts
def bracket(g,x,y,w,col=C,op=1):
 g.poly([(x,y-8),(x,y),(x+w,y),(x+w,y-8)],col,2,op)
