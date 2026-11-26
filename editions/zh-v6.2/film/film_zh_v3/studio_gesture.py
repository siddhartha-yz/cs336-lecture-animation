"""Actors are instruments: the same marked nib writes, reasons and finally submits.
No portraits, role cards, Google-results mockups or labels floating above the film.
"""
from ink import *
from studio_examples import area,pstep
from mounting import etch
def scholar(g,x,y,col,op,scale=1,theta=0,tassel=0):
 # Oblique silhouette, tassel and pen identify the research role, not the person's discipline or gender.
 ctx=g.c;ctx.save();ctx.translate(x,y);ctx.scale(scale,scale);ctx.rotate(theta)
 area(g,[(-22,0),(-11,-7),(0,-3),(13,-8),(24,5),(31,23),(-29,23)],inkcol(col,.63),op)
 g.circle(1,-17,11,inkcol(col,.83),col,1.35,op)
 g.poly([(-26,-32),(0,-42),(26,-33),(2,-22)],col,1.5,op,True,inkcol(col,.58),1)
 path(g,[(23,-32),(27,-25),(26+4*tassel,-13)],1,col,2.4,op);dot(g,26+4*tassel,-11,2.7,col,op)
 ctx.restore()
def scribe(g,x,y,col,op,ang=-.65,scale=1):
 ctx=g.c;ctx.save();ctx.translate(x,y);ctx.rotate(ang);ctx.scale(scale,scale)
 g.poly([(0,0),(-6,-16),(-5,-48),(5,-48),(6,-16)],col,1.25,op,True,inkcol(col,.72),1)
 area(g,[(-6,-16),(6,-16),(0,0)],F,op);ctx.restore()
def library(g,x,y,k,op,s=1):
 # A real record's identifiers; a searchable substance is not its reaction's isomer count.
 if op<.003:return
 m=g.c;m.save();m.translate(x,y);m.scale(s,s)
 k=clip(k);name='methylcyclopentadiene';q=min(len(name),int(k*len(name)*2.1))
 ring(g,-29,0,10,C,op,2.7);line(g,(-21,8),(-12,17),C,3,op)
 etch(g,name[:q],0,0,26,F,op)
 length=max(38,g.measure(name,26,font=SERIF));line(g,(0,23),(length*k,23),C,2.,op)
 a=phase(k,.33,.84);b=phase(k,.55,.98)
 if a:etch(g,'NIST Chemistry WebBook',8,57,25,C,op*a)
 if b:
  etch(g,'C₆H₈',8,107,32,F,op*b);etch(g,'CAS  96-39-9',109,107,22,M,op*b)
 m.restore()
def workbench(g,x,y,i,q,t,op,col):
 # Three distinct scratch marks shared as a visual example of inspection, not individual response logs.
 # No lightbulb for intelligence: compare families of geometric structures and trace a candidate.
 if op<.003:return
 ctx=g.c;ctx.save();ctx.translate(x,y);ctx.rotate((-.16,.12,-.10)[i])
 for j in range(4):
  z=clip(q*4.48-j*.87);rr=9.8;xx=j*27-(3*27)/2
  if z:
   vert=[(xx+rr*cos(-pi/2+l*tau/5),rr*sin(-pi/2+l*tau/5))for l in range(6)]
   path(g,vert,z,col,1.9,op*(.53+.36*z))
   v=vert[(i+j)%5];line(g,v,(xx+1.46*(v[0]-xx),1.46*v[1]),col,1.5,op*z)
 if q>.54:
  a=phase(q,.54,1);d=(t*.66+i*.31)%1;xx=-45+89*d
  path(g,[(-49,22),(-49,29),(mix(-49,51,a),29)],1,F,1.4,op*a)
  dot(g,xx,29,3.5,col,op*a)
 ctx.restore()
