"""The observed next word gets one real conditional probability and one magnification."""
from rig4 import *
from motion6 import ArcLength


def condition(g,c,xs,yrow,p0,op):
    t=c.t;a=c.at;read=a('语言模型逐个');each=a('每一步都给');actual=a('真实出现');cond=a('条件概率')
    gold=a('金色那根');small=a('很短的柱子');say=a('押给 cat');look=a('沿原文')
    # The pre-existing The and small join the prefix, so the gold result is
    # visibly conditional on the words already exposed above it.
    band=during(t,read-.15,actual+1.36,.33)*op
    for j in range(2):
        xx=xs[j];st=read-.17+.31*j;u=easepos(t,st,1.08)
        if u:
            aa=(xx,yrow+41);bb=(438,316);coords=[aa,(xx,305),(353+35*j,328),bb]
            path(g,coords,u,T,2.45,band*.87)
            if .01<u<.99:point(g,*ArcLength(coords).at(u),5.55,T,band)
    q=during(t,each-.20,cond+.55,.48)*op
    if q:
        x=xs[2];r=enter(t,actual-.22,.58)
        pts=[(xs[0]-62,195),(xs[0]-62,186),(xs[1]+62,186),(xs[1]+62,195)]
        path(g,pts,enter(t,each-.18,.62),T,2.46,q)
        if r:
            ring(g,x,yrow+1,31+4*r,Y,r*q*.85,2.28)
            swish(g,x-52,x+52,yrow+51,t-actual+.17,Y,.64,3.0)
    ca=during(t,cond-.19,look-.12,.44)*op
    if not ca:return
    fade=enter(t,cond-.16,.60);x0=1262;base=566
    if fade:
        label(g,'p(cat | … The small)',1266,392,32,Y,ca*fade)
    lens=enter(t,small-.25,.72);start=(1006,590);fork=(1167,566)
    reel=during(t,gold-.13,look-.21,.44)*op
    if reel:
        u=easepos(t,gold-.23,1.24)
        coords=[start,(1068,603),(1121,603),fork]
        path(g,coords,u,Y,2.35,reel)
        if 0<u<.998:point(g,*ArcLength(coords).at(u),6.1,Y,reel)
        if u>.81:ring(g,*start,10.8,Y,reel*phase(u,.81,.998),2.3)
    a0=ca*lens
    if a0:
        height=128*(p0/.001);top=base-128;col=Y
        path(g,[(1171,top),(1171,base),(1419,base)],lens,M,1.9,a0)
        line(g,(1171,top),(1419,top),E,1.4,a0*.84)
        label(g,'0.1%',1430,top,23,M,a0,'left');label(g,'0',1430,base,23,M,a0,'left')
        rect(g,x0-22,base-height*lens,44,height*lens,inkcol(col,.92),a0)
        u=enter(t,say-.17,.57);point(g,x0,base-height*lens,4.85,col,u*a0)
        label(g,'近零处放大',1291,622,27,M,a0)
