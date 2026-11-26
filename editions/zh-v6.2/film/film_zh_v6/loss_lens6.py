"""One measured token, two losses, then the same answer space at a larger scale."""
from rig4 import *


def slots(g,c,labels,first,dx,y,ai,op):
    t=c.t
    start=c.at('每个标点');fill=c.at('每个铺垫词');final=c.at('最后的答案')
    each=c.at('各占一个位置');worth=c.at('给同样的权重');cost=c.at('每一步吃的亏')
    reveal=easepos(t,each-.35,1.47)
    emphasis=enter(t,worth-.11,.55)*(1-phase(t,cost-.3,cost+.29))
    active=1-phase(t,c.at('前面许多')-.19,c.at('前面许多')+.68)
    leave=float(t<c.at('收起整行平均数')-.16)
    arrive=phase(t,c.at('把题干')+.75,c.at('把题干')+1.15)
    for i,ss in enumerate(labels):
        x=first+i*dx
        v=op*(arrive*leave if i==ai else 1.)
        if ss in (':','.'):
            pulse=during(t,start-.12+.081*i,start+1.20,.28)*.92
        elif i==ai:pulse=during(t,final-.17,each+1.17,.46)
        else:pulse=during(t,fill-.15+.045*i,final+.12,.37)*.66
        p=phase(reveal,i/22,.53+i/31)
        stroke=v*(.62*p*active+.38*emphasis)
        co=Y if i==ai else T
        if stroke or pulse:
            box(g,x-36,y-27,72,55,blend(M,co,min(1.,1.4*pulse+emphasis)),max(stroke,v*pulse),
                inkcol(co,.11+.46*pulse) if pulse else None,1.65)
        a=emphasis*enter(t,worth-.23+.037*i,.42)
        if a:point(g,x,y+54,4.9,co,a*v)
        lab=Y if i==ai else blend(F,T,.59*pulse)
        label(g,ss,x,y+1,27,lab,v*enter(t,c.at('把题干')+.045*i,.49),limit=71)


def live_losses(g,c,models,labels,li,dx,op):
    t=c.t;entry=c.at('给原词');exit_=c.at('前面许多');w=c.at('损失就越大')
    ix=0;col0,col1=C,V;xx=li+ix*dx
    ui=during(t,entry-.3,exit_-.08,.44)
    z=during(t,entry-.19,exit_-.09,.41)*op
    if z:
        for j,(y,model,co) in enumerate(zip((302,591),models,(col0,col1))):
            nh=model['nll'][ix];pa=exp(-nh);y1=y-9.7*nh
            a=enter(t,entry-.18+.14*j,.57)
            pulse=enter(t,w-.17+.11*j,.61)
            path(g,[(xx-40,y),(xx-49,y),(xx-49,y1),(xx-40,y1)],pulse,co,2.55,z)
            if pulse:rect(g,xx-22,y1,44,9.7*nh,inkcol(co,.98),z*pulse*.72)
            v=(f'{pa:.2%}' if pa>=.0001 else f'{pa:.4%}')
            if j:label(g,v,xx-53,y1+19,27,co,a*z,'right',108)
            else:label(g,v,xx,y1-32,28,co,a*z)
        path(g,[(xx,394),(xx,405)],ui,T,2.5,z)
        path(g,[(xx,474),(xx,493)],ui,T,2.5,z)
    elif exit_-.13<t<c.at('先看整行')-.17:
        # Keep the prompt tokens themselves visible. An expanding bracket adds
        # actual summands to the same side of the eventual comparison.
        a=easepos(t,exit_-.16,1.36)
        b=c.at('盖过答案词');u=enter(t,b-.17,.56)
        y=488
        path(g,[(li-36,y-8),(li-36,y),(li-36+(13*dx+72)*a,y)],1,T,2.05,op*a*.83)
        if a>.97:line(g,(li+13*dx+36,y),(li+13*dx+36,y-8),T,2.05,op*a*.83)
        if u:
            sx=li+14*dx
            path(g,[(sx-35,y-9),(sx-35,y),(sx+36,y),(sx+36,y-9)],u,Y,2.6,op*u)


def take_focus(g,c,front_y,old_x):
    t=c.t;pick=c.at('收起整行平均数');landing=c.at('最后那一格');out_=c.at('比较候选答案')
    if t<pick-.17 or t>out_+.51:return
    q=easepos(t,pick-.16,max(.95,landing-pick+.25))
    film=1-phase(t,out_-.15,out_+.51);a=enter(t,pick-.16,.49)*film
    x,y=transit((old_x,front_y),(800,326),q,75.)
    ww=mix(70,176,q);hh=mix(55,113,q)
    box(g,x-ww/2,y-hh/2,ww,hh,Y,a,inkcol(Y,.28),mix(1.9,3.4,q))
    label(g,'two',x,y+1-q,mix(27,59,q),Y,film)
    if q>.35:
        for side,j in ((C,-1),(V,1)):
            u=phase(q,.4,.97)
            path(g,[(x+j*ww*.52,y),(x+j*129,y),(x+j*239,y+38)],u,side,2.5,a*.83)
