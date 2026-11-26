"""A black canvas, opaque pigments. Grade the ink *before* alpha compositing.
Photographs, captured documents, subtitles, white formulae and pure black keep their own values.
Neutral geometry remains neutral; an expressly retired mark at 20% stays in the background.
"""
from visual import rgb
from functools import lru_cache
import bisect,math
INK_EDITION="ink-3.1"
RANGE=((0.,0.),(.055,.06),(.11,.17),(.20,.37),(.32,.58),(.48,.76),(.67,.88),(.84,.956),(1.,1.))
NEUTRAL=((0,0),(.12,.12),(.27,.30),(.44,.50),(.64,.73),(.81,.885),(1.,1.))
def curve(x,ks):
 for (a,b),(c,d)in zip(ks,ks[1:]):
  if x<c:return b+(x-a)*(d-b)/(c-a)
 return ks[-1][1]
def blendat(x,a,b):
 f=max(0,min(1,(x-a)/(b-a)));return f*f*(3-2*f)
@lru_cache(maxsize=16384)
def chalk(color):
 r,g,b=rgb(color);v=max(r,g,b);lo=min(r,g,b)
 if v<=.0001:return(0.,0.,0.),0.
 sat=(v-lo)/v;ch=blendat(sat,.09,.41)
 # Scale all channels together so a model keeps its colour on both sides of a cut.
 y=curve(v,NEUTRAL)*(1-ch)+curve(v,RANGE)*ch;u=y/v
 return (min(1,r*u),min(1,g*u),min(1,b*u)),ch
def visibility(a,ch):
 if a<=.22 or a>=1:return a
 # Bring ambiguous mid-opacity ink forward, but do not revive retired objects.
 return min(1,a+(.155*ch+.046*(1-ch))*blendat(a,.22,.51)*(1-blendat(a,.64,1)))
