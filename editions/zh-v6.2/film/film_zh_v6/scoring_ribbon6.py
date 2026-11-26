"""The same two measured texts yield a length condition and an intact pair."""
from rig4 import *
from studio_preference import material
from motion6 import ArcLength


@lru_cache(maxsize=1)
def measured():
    return tuple(map(len, material()))


def strips(g,c,ticket,op):
    t=c.t
    n=measured()
    trim=c.at('一刀剪短')
    bonus=c.at('单靠长度')
    quiet=c.at('原文钉住')
    start=enter(t,.17,.58)
    if not start:return
    collect=easepos(t,c.at('长度差等信息')-.49,1.01);fold=easepos(t,ticket-.35,1.08)
    retire=1-phase(t,c.at('裁判胜负')-.60,c.at('裁判胜负')-.09)
    v=op*start*retire*(1-collect)
    X=791;unit=.692;max_len=max(n);base=(402,541)
    # The two rows share word scale. Each broad mark groups 10 *actual* words
    # from the two complete archived responses; last partial marks are shorter.
    for j,(words,col) in enumerate(zip(n,(C,V))):
        yy=base[j]
        step=unit*10
        gap=1.65
        h=29
        first=phase(t,.22+.24*j,2.06+.31*j)
        lifted=(j-.5)*28*fold
        y=yy-lifted
        if first and v:
            for i in range((words+9)//10):
                drawn=enter(t,.19+.18*j+.020*i,.38)
                if not drawn:break
                x=X+i*step;wi=unit*min(10,words-i*10)-gap
                if wi<.4:wi=.4
                is_excess=j==0 and i*10>=n[1]
                warm=phase(t,bonus-.18,bonus+.51)*(1-phase(t,quiet-.60,quiet))
                shade_=.63+.27*((i*11+j*7)%11)/11
                co=blend(col,O,.91*warm)if is_excess else col
                rect(g,x,y-h*.5+1.5*(1-drawn),wi,h*(.55+.45*drawn),co,v*drawn*shade_)
            text_op=enter(t,1.05+.26*j,.51)*v
            label(g,f'{words} 词',X+unit*words+21,y,28,col,text_op,'left')
            label(g,('A','B')[j],X-19,y,32,col,v,'right')
            # An animated transfer picks from the original word
            # trace; the incoming particle never consumes a word in the left.
            for i,(sx,sy)in enumerate(((546,348),(565,606)) if j==0 else ((548,537),(584,568))):
                ts=.16+.29*j+.17*i;u=easepos(t,ts,.94)
                if 0<u<1:
                    dst=(X+45+i*106,y);hl=sin(pi*u)**.52
                    xx,y1=transit((sx,sy),dst,u,-34.+15*i)
                    path(g,[(sx,sy),(642,sy-7),dst],u,col,1.6,v*hl*.50)
                    point(g,xx,y1,5.3+j,col,v*hl)
    if not v:return
    cut=during(t,trim-.18,bonus+.18,.46)
    width_short=unit*min(n);width_long=unit*max_len
    if cut:
        x0=X+width_short
        yy0=base[0]-29;yy1=base[1]+25
        draw=phase(t,trim-.19,trim+.38)
        # A common vertical yardstick probes the difference, while both rows remain intact.
        lim=mix(yy0,yy1,draw)
        for y0 in range(round(yy0),round(yy1),14):
            if y0<lim:line(g,(x0,y0),(x0,min(lim,y0+6)),F,1.8,v*cut*.84)
        xx=x0-6
        path(g,[(xx,yy0),(x0,yy0-8),(x0+6,yy0)],draw,M,2.0,v*cut)
    comparison=phase(t,bonus-.17,bonus+.52)*(1-phase(t,quiet-.18,quiet+.45))
    if comparison:
        y=base[0]+48
        x=X+width_short
        b=X+width_long
        u=easepos(t,bonus-.15,.76)
        path(g,[(x,y-9),(x,y),(b,y),(b,y-9)],u,O,2.4,comparison*v)
        mark(g,'长度差',.5*(x+b),y+30,29,t-bonus+.07,O,op=comparison*v)
    hold=enter(t,quiet-.20,.62)
    if hold and not fold:
        # Registration corners, not copy scissors.
        for j,yy in enumerate(base):
            len_=unit*n[j];x=X+len_+13
            path(g,[(x-9,yy-20),(x-16,yy-20),(x-16,yy+20),(x-9,yy+20)],hold,Y,2.,v*hold)


def ticket_spine(g,c,ticket,fit,op):
    t=c.t
    n=measured()
    pop=enter(t,ticket-.10,.63)
    fold=easepos(t,fit-.40,1.00)
    if not pop or fold>=1:return
    # A gold vote crease extends from the two response marks. Three features
    # attach to it *when spoken*, before fanning into the conditional plot.
    cx=1099-163*fold;origin=(cx,271+199*fold)
    data=((879,419,Y,'裁判胜负'),(1099,454,T,'哪两个模型'),(1319,473,V,'长度差等信息'))
    lead=[(625,542),(701,500),(748,337),origin]
    lo=during(t,ticket-.21,fit+.42,.43)*op
    flow=easepos(t,ticket-.25,1.06)
    path(g,lead,flow,Y,2.30,lo*.85)
    if flow<1:point(g,*ArcLength(lead).at(flow),7.,Y,lo)
    o=op*pop*(1-fold)
    if o:
        X,Y_=origin
        pts=((X,Y_-22),(X+23,Y_),(X,Y_+21),(X-23,Y_))
        g.poly(pts,Y,2.3,o,True,inkcol(Y,.37),.70*o)
        label(g,'偏好票',X+35,Y_-1,29,F,o,'left')
    for i,(xx,yy,co,tag) in enumerate(data):
        at=c.at(tag)
        u=enter(t,at-.18,.55)
        if not u:continue
        pts=[origin,(origin[0],mix(origin[1],yy,.48)),(xx,yy)]
        w=op*u*(1-fold)
        path(g,pts,easepos(t,at-.21,.68),co,2.2,w*.86)
        # Intentionally no count or model identity: each arm is a predictor, not
        # an empirical demonstration of the paper's exact fitted coefficients.
        if i==0:check(g,xx,yy,19,True,w)
        elif i==1:
            point(g,xx-16,yy,9,C,w);point(g,xx+18,yy,9,V,w)
            line(g,(xx-6,yy),(xx+8,yy),T,2.5,w)
        else:
            unit=.18
            x=xx-65
            for j in range(2):
                line(g,(x,yy+(j-.5)*17),(x+unit*n[j],yy+(j-.5)*17),(C,V)[j],5.,w)
        label(g,('哪份获选','谁和谁比','长度差')[i],xx,yy+49,28,co,w)

