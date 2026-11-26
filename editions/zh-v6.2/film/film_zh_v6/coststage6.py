"""A rank, a receipt, then a scatter plot: the same measured configurations."""
from rig4 import *
from gates6 import bar_in
from motion6 import ArcLength


def set_cost(g,c,models,front,X,Yf):
    t=c.t
    paper=c.at('账单')-.16;until=c.at('把每个模型')
    bend=easepos(t,until-.24,2.05);seat=easepos(t,paper-.16,.57)
    retire=easepos(t,until-.34,.72);receipt=seat*(1-phase(retire,.62,.96))
    rows=sorted(models,key=lambda p:p['index']);rank={r['slug']:j for j,r in enumerate(rows)}
    last=rows[-1];oldx,y0,pitch=209,590,46.5
    if bend<1:
        edge=1-bend
        a=enter(t,.04,.76)*edge*(1-.86*seat)
        line(g,(oldx-18,y0),(oldx+25*pitch+47,y0),M,2.3,edge*(1-.80*receipt))
        label(g,'26 个默认配置',oldx+2,y0+57,31,M,a,'left')
        label(g,'智能指数',oldx+2,197,36,F,a,'left')
    cut=c.at('依次拿走');bads=[r for r in models if r not in front]
    budget=c.u('一美元的线',.50)
    first=enter(t,c.at('只看成绩')-.2,.61)
    for r in models:
        j=rank[r['slug']];promoted=r is last
        x0=oldx+j*pitch+15.15
        rise=bar_in(t,j)
        if not rise:continue
        x=mix(x0,X(r['cost']),bend)
        yy=mix(y0-r['index']*5.25*rise,Yf(r['index']),bend)
        y=mix(y0,yy,bend)
        rest=0. if r in front else enter(t,cut-.10+.071*bads.index(r),.52)
        visible=(1-.86*rest)*(1-(.61*budget if r['cost']>1 else 0.))
        chosen=C if r not in front else O
        col=blend(blend(C,O,first)if promoted else C,chosen,bend)
        seen=visible*(1-(.83 if not promoted else .67)*receipt)
        width=mix(30.3,16. if r in front else 12.,bend)
        if bend<1:
            ht=max(0.,y-yy);rounding=phase(bend,.30,1.)
            if ht>.001:
                p=inkcol(col,mix(.68+.23*j/25,1.,bend))
                rect(g,x-width/2,yy,width,ht,p,seen*(1-rounding))
            if rounding:dot(g,x,yy+width*.25*(1-bend),width/2,col,seen*rounding)
        else:dot(g,x,yy,8. if r in front else 6.,col,seen)
        if promoted and first and bend<.8:
            a=first*(1-seat)*(1-phase(bend,.10,.80));py=yy-59
            if a:
                path(g,[(x,yy-8),(x-43,py+3),(x-140,py+3)],first,O,2.15,a)
                label(g,'Claude Fable 5.2',x-150,py-5,32,O,a,'right')
                label(g,f"{r['index']:.1f}",x,py+15,29,O,a)

    q=enter(t,c.at('给你每道题')-.26,.47)*(1-bend)
    if q:
        label(g,'$1 / 题',438-81*seat,309,56,Y,q)
        if not seat:swish(g,358,516,354,t-c.at('给你每道题')+.15,Y)
    if receipt:
        # The original evidence rides on the receipt. It is inset so the far
        # column, the $1 budget and the camera motion remain visible together.
        x=mix(1368,880,seat)+1108*retire;y=mix(429,403,seat)-132*retire
        width=735*(.16+.84*seat)*(1-.10*retire)
        paint=.995*phase(seat,.06,.57)
        photo(g,AS/'aa-scatter.png',x,y,width,tilt=.08*(1-seat)-.021-.12*retire,op=paint)
        a=receipt*phase(seat,.57,.94)*(1-phase(retire,.02,.32))
        label(g,'Artificial Analysis · 实际每题平均开销',x-6,y+width*.27+41,27,O,a)
        tail=enter(t,paper+.25,.51)*(1-phase(t,until-.35,until-.06))
        label(g,'$26.54',1372,y-16,62,O,tail)
        path(g,[(1287,y+25),(1464,y+25)],tail,O,2.3,tail)
        label(g,'第一名 · 每题美元',1372,y+73,27,M,tail)


def constraint(g,c,top,X,Yf):
    t=c.t;intro=c.at('真实预算');pick=c.at('挑这个点');highest=c.at('纵轴最高点')
    q=enter(t,intro-.13,.57)*(1-phase(t,pick-.40,pick-.08))
    if q:
        x,y=X(top['cost']),Yf(top['index']);p=easepos(t,highest-.50,.73)
        a=enter(t,highest-.51,.58)*q
        if a:
            path(g,[(x,y),(x,658)],p,O,2.5,a*.76)
            ring(g,x,y,14.6,O,a,2.3)
            label(g,'$26.54',x-16,631,27,O,a*p,'right')
        cap=enter(t,intro-.14,.56)
        bx=X(1)
        line(g,(X(.1)+3,642),(mix(X(.1)+3,bx,cap),642),T,2.5,q)
        line(g,(bx,635),(bx,648),T,2.3,q*cap)


def exchange(g,c,rows,X,Yf):
    t=c.t;left=c.at('再省点钱');right=c.at('再往上挪');wall=c.at('一美元的线')
    # From Terra, move to the closest cheaper and the closest higher measured
    # configurations on this frontier. Each endpoint is an observed model.
    back,mid,next_=rows[1:4]
    origin=(X(mid['cost']),Yf(mid['index']))
    for j,(owner,start,stop,zcol)in enumerate(((back,left,right-.13,T),(next_,right,wall-.12,C))):
        a=during(t,start-.15,stop,.29)
        if not a:continue
        to=(X(owner['cost']),Yf(owner['index']))
        d=easepos(t,start-.15,.94)
        # Use the plotted stairs themselves. The arrowhead follows both legs,
        # so that there is no apparent diagonal bargain with both gains.
        route=[origin,(origin[0],to[1]),to] if j==0 else [origin,(to[0],origin[1]),to]
        rail=ArcLength(route);dotxy=rail.at(d)
        path(g,route,d,zcol,4.25,a)
        ring(g,*origin,13,Y,a*.77,2.)
        if d>.002:point(g,*dotxy,6.7,zcol,a)
        b=enter(t,start+.21,.58)
        if b:
            dc=owner['cost']-mid['cost'];di=owner['index']-mid['index']
            tag=f'{"+" if dc>0 else "−"}${abs(dc):.2f}'
            if j:
                xx,yy=to[0]+101,to[1]-36
                label(g,f'+{di:.1f} 指数',xx,yy,29,zcol,b*a)
                label(g,tag,xx-41,to[1]+39,28,O,b*a)
            else:
                xx,yy=to[0]+11,to[1]+56
                label(g,tag,xx,yy,29,zcol,b*a)
