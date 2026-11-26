"""A measured bar becomes an aperture on the next, entirely different evidence."""
from rig4 import *

# The rectangle is the exact 87.5% bar from sample_readout; the later aperture
# refers to the reading process, and carries neither the score nor its label.
LENGTH=87.5*3.91
HALF=647-LENGTH*.5
CUT=(801,290)
HEIGHT=10.5
WIDTH=1021


def fold(g,q,op=1.):
    ctx=g.c;ctx.save()
    xy=transit((1289,HALF),CUT,q,73.)
    ctx.translate(*xy);ctx.rotate(pi/2*q)
    w=mix(102.,HEIGHT,q);h=mix(LENGTH,WIDTH,q)
    rect(g,-w/2,-h/2,w,h,C,op)
    ctx.restore()


def out(g,c):
    edge=easepos(c.t,c.d-.75,.75-1/60)
    if edge:
        shade(g,edge)
        fold(g,edge,edge)


def in_(g,t):
    u=1-phase(t,.13,.82)
    if u:
        fold(g,1.,u)
