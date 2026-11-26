"""Fixed stream, machine and finish line for the NanoGPT wall-clock experiment."""
from rig4 import *
from motion6 import ArcLength
from speed6 import watch,goldrail

LOSS=((943,311),(1005,348),(1051,341),(1105,382),(1165,374),(1213,414),
      (1293,420),(1363,454),(1419,450),(1495,494))
TRACE=ArcLength(LOSS)


def h100(g,x,y,op,under):
    if op<.002:return
    # The eight modules occupy identical seats throughout the controlled task.
    a=[(x-44,y-24),(x+35,y-24),(x+46,y-13),(x+46,y+24),(x-44,y+24)]
    g.poly(a,T,1.95,op,True,inkcol(T,.42+.39*under),op)
    rect(g,x-17,y-10,34,20,inkcol(C,.72),op*.89)
    for j in range(5):
        u=x-34+j*14
        line(g,(u,y-24),(u,y-30),T,1.15,op*.85)
        line(g,(u,y+24),(u,y+30),T,1.15,op*.85)


def draw(g,c,ns):
    t=c.t;a=c.at
    fine=a('把语料锁');stream=a('从同一条网页词元流');ordering=a('顺序固定');stops=a('可以停在不同位置')
    hard=a('八张');finish=a('三点二八');origin=a('这条线来自');model=a('网络结构');stub=a('终点不挪')
    open_=enter(t,ns,.59);jump=easepos(t,ns,1.19);park=easepos(t,fine-.74,1.53)
    u=enter(t,fine-.16,.56);trail=enter(t,stream-.16,.70)
    wx,wy=mix(1213+97*jump,1405,park),mix(354-24*jump,153,park)
    wr=mix(108,36,park);pend=phase(t,finish+.16,stub+.48)
    watch(g,wx,wy,wr,open_,pend)
    x=wx-wr-43;y=wy-11+17*park
    close=a('全场比拼的')-.14
    tag=enter(t,ns+.03,.62)*(1-phase(t,close-.48,close-.10))
    mark(g,'NanoGPT',x,y,mix(63,45,park),t-ns-.02,O,'right','pen',.63,tag)
    path(g,[(x-106,y+26),(x+33,y+26),(wx-wr-7,wy+8)],tag,O,2.1,tag*.76)
    label(g,'实际用时',x,y+56,28,M,tag,'right')
    if t>ns+.25 and park<.99:
        edge=enter(t,ns+.18,1.21);src=(180.,264.)
        pts=[src,(314.,270.),(589,366),(730,478),(wx-31,wy+wr+24),(wx-27,wy+wr*.93)]
        a0=.8*edge*(1-park);path(g,pts,edge,Y,2.55,a0)
        if .01<edge<.999:point(g,*ArcLength(pts).at(edge),6.1,Y,a0)
    if u:
        mark(g,'FineWeb',182,174,43,t-fine+.14,C,'left','pen',.49,u)
        label(g,'公开网页预训练语料',184,218,26,M,u,'left')
        q=easepos(t,stream-.18,.93);cut=phase(t,hard-.39,hard+.37)
        n=26
        for j,y in enumerate((264,336)):
            b=trail if j else u
            sec=phase(t,stops-.28+.18*j,stops+.55+.18*j)
            kept=(.91,.57)[j];stop=mix(.99,kept,sec)
            cy=mix(y,278+46*j,cut);span=528.
            for i in range(n):
                a0=enter(t,fine-.14+.045*i+.10*j,.45)*b
                col=(C,T,O,V)[(i*7+(i//4)*5)%4]
                x1=178+i*(span/n);xx=x1+44*(1-q)*j
                # Two training runs read the same exactly ordered colours.
                # The shorter cursor stops without reversing that stream.
                val=1-.75*phase(i/(n-1),stop,stop+.07)
                rect(g,xx,cy-7,14,14,inkcol(col,.89),a0*val)
            if sec:
                x1=178+span*stop
                line(g,(x1,cy-19),(x1,cy+19),Y,2.55,sec)
                point(g,x1,cy+18,4.9,Y,sec)
        r=enter(t,ordering-.15,.61)
        if r:
            path(g,[(177,358),(177,365),(684,365)],r,T,1.8,r*(1-cut))
            label(g,'同一顺序',751,363,29,T,r*(1-cut),'right')

    machine=enter(t,hard-.20,.72);meter=easepos(t,finish-.29,1.17)
    if machine:
        # Count once, then let a batch pulse from the unchanged stream into a device row.
        for j in range(8):
            x=290+118*(j%4);y=425+(j//4)*88
            b=enter(t,hard-.20+.061*j,.55)
            flash=0.
            for start in (hard+.13,finish-.17,origin+.79,model-.31):
                v=enter(t,start+.06*(j%4),.22)*(1-phase(t,start+.27+.06*(j%4),start+.59+.06*(j%4)))
                flash=max(v,flash)
            h100(g,x,y,b,flash)
            v=easepos(t,hard+.11+.055*j,.76)
            p=[(178+j%4*118,323),(178+j%4*118,359),(x,y-33)]
            if 0<v<.999:point(g,*ArcLength(p).at(v),5.65,T,math.sin(pi*v)**.65)
        label(g,'8 × H100',467,574,38,T,machine)
        test=enter(t,finish-.20,.55)
        for j in range(13):
            progress=enter(t,finish-.26+.055*j,.40)
            rect(g,213+37*j,632,24,15,Y,test*progress*.89)
        link=[(687,639),(770,639),(803,591),(896,591),(929,508)]
        if test:
            label(g,'留出验证',231,687,28,Y,test,'left')
            s=easepos(t,finish-.13,1.34)
            path(g,link,s,Y,2.5,test*.85)
            if s<1:point(g,*ArcLength(link).at(s),5.25,Y,test)

    axes=enter(t,hard-.08,.89);ytitle=220
    if axes:
        path(g,[(931,276),(931,647),(1495,647)],axes,M,2.35,axes)
        label(g,'验证损失',916,ytitle,33,F,axes,'left')
        label(g,'单次运行示意',1496,271,24,M,axes,'right')
        label(g,'用时',1493,687,27,M,axes,'right')
    if meter:
        goldrail(g,(931,494),(1495,494),meter,1.)
        v=enter(t,finish+.19,.61)
        label(g,'3.28 · 留出验证目标',962,535,33,Y,v,'left')
        q=easepos(t,finish-.45,max(.92,origin-finish+1.85));path(g,LOSS,q,C,4.10,axes)
        if q:point(g,*TRACE.at(q),7.3,Y if q>.96 else C,axes)
        if q>.92:ring(g,*TRACE.at(1.),17.8,Y,phase(q,.92,1.),2.4)
    names=enter(t,a('卡帕西')-.20,.57)
    if names:
        mark(g,'llm.c',953,757,30,t-a('卡帕西')+.15,O,'left','pen',.51,names)
        label(g,'GPT-2 small 复现',1066,757,27,M,names,'left')
    net=enter(t,a('选手可以')-.15,.57)
    if net:
        u=easepos(t,model-.24,.79)
        for j in range(4):
            x=267+78*j;y=752+26*sin(pi*u)*(-1 if j%2 else 1)
            box(g,x-18,y-12,36,24,blend(T,V,u),net,inkcol(blend(T,V,u),.46),1.65)
            if j<3:line(g,(x+18,y),(x+59,752-26*sin(pi*u)*(-1 if j%2 else 1)),T,1.8,net*.70)
        label(g,'结构可改',549,752,28,T,net,'left')
    if t>=stub-.14:
        w=enter(t,stub-.14,.48)
        swish(g,1327,1467,494,t-stub+.14,Y,.66,3.20)
        if w:ring(g,1495,494,14.7,Y,w,2.)
