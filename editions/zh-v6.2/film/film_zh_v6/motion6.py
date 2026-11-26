"""Interpolate an anchored clock without a change of velocity at every spoken word."""
from bisect import bisect_right
from math import hypot
from functools import lru_cache

def _bound(n,d):
 return max(0.,min(1.,n/d))
@lru_cache(maxsize=256)
def slopes(x,y):
 """Shape-preserving cubic Hermite slopes, including plateaus and endpoints."""
 h=[b-a for a,b in zip(x,x[1:])];d=[(b-a)/k for a,b,k in zip(y,y[1:],h)]
 if len(d)==1:return (d[0],d[0])
 def edge(h0,h1,d0,d1):
  v=((2*h0+h1)*d0-h0*d1)/(h0+h1)
  if v*d0<=0:return 0.
  if d0*d1<=0 and abs(v)>3*abs(d0):return 3*d0
  return v
 m=[edge(h[0],h[1],d[0],d[1])]
 for i in range(1,len(d)):
  a,b=d[i-1],d[i]
  if a*b<=0:m.append(0.);continue
  w0=2*h[i]+h[i-1];w1=h[i]+2*h[i-1];m.append((w0+w1)/(w0/a+w1/b))
 m.append(edge(h[-1],h[-2],d[-1],d[-2]))
 return tuple(m)

class FlowClock:
 """A shared monotonic time map; proposed local events stay on their words."""
 def __init__(self,x,y):
  self.x,self.y=tuple(x),tuple(y)
  if len(self.x)!=len(self.y) or len(self.x)<2 or any(b<=a for a,b in zip(self.x,self.x[1:])) or any(b<a-1e-8 for a,b in zip(self.y,self.y[1:])):
   raise ValueError(('motion needs ordered knots',self.x,self.y))
  self.m=slopes(self.x,self.y)
 def __call__(self,t):
  x,y,m=self.x,self.y,self.m
  j=max(0,min(len(x)-2,bisect_right(x,t)-1));dt=x[j+1]-x[j];u=_bound(t-x[j],dt);v=1-u
  # Two Bernstein endpoint contributions and their tangents. Avoid jumps
  # from using a different eased animation independently in every interval.
  return (1+2*u)*v*v*y[j]+(3-2*u)*u*u*y[j+1]+dt*u*v*(v*m[j]-u*m[j+1])

class ArcLength:
 """Keep the speed independent of the layout's aspect ratio."""
 def __init__(self,xy):
  self.xy=tuple(xy);d=[0.]
  for (x,y),(xx,yy) in zip(self.xy,self.xy[1:]):d.append(d[-1]+hypot(xx-x,yy-y))
  if len(d)<2 or d[-1]==0:raise ValueError('empty camera rail')
  self.d=tuple(d);self.length=d[-1]
 def at(self,p):
  dist=_bound(p,1.)*self.length;d=self.d;j=max(0,min(len(d)-2,bisect_right(d,dist)-1))
  f=(dist-d[j])/max(1e-10,d[j+1]-d[j]);x,y=self.xy[j];xx,yy=self.xy[j+1]
  return (x+(xx-x)*f,y+(yy-y)*f)
 def fraction(self,index):return self.d[index]/self.length
