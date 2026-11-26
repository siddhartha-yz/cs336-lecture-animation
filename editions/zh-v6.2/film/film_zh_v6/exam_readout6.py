"""First hold the model fixed; then hold the answering protocol fixed."""
from rig4 import *
from motion6 import ArcLength

# MMLU-Pro paper, Table 3. Compare only CoT on both papers after the turn.
MODEL=(('GPT-4o',88.7,72.6,C),('GPT-4 Turbo',86.5,63.7,V))
RAW=(53.5,72.6)
XL,XR=456,1144
def vertical(v):return 679-(v-50)*9.15


def draw(g,c,read,turn):
    t=c.t
    same=c.at('模型没换')
    old=c.at('把旧卷')
    spread=c.at('区分度')
    on=enter(t,read,.62)
    q=easepos(t,turn+.05,1.16)
    oldLabels=1-phase(t,turn-.31,turn+.24)
    oldCards=1-phase(t,turn-.22,turn+.51)
    settle=enter(t,turn+.61,.61)
    label(g,'GPT-4o',239,167,47,C,on*oldLabels,'left')
    path(g,[(238,207),(389,207),(484,242)],on,C,2.2,on*oldLabels)
    label(g,'MMLU-Pro',505,167,34,F,on*oldLabels,'left')
    write=(c.at('五十三点五'),c.at('七十二点六'))
    ex=enter(t,same-.16,.55)
    for j,(tag,v,col,go) in enumerate(zip(('直接交选项','分步推理后选'),RAW,(O,C),write)):
        yy=355+160*j
        grow=easepos(t,go-.22,.83)
        label(g,tag,465,yy,35,col,on*oldLabels,'right')
        line(g,(517,yy+39),(1287,yy+39),E,1.8,on*oldLabels)
        if not grow:continue
        tip=517+v*7.7*grow
        lift=q if j==1 else 0.
        source=(tip,yy)
        x,y=transit(source,(XR,vertical(v)),lift,83.)
        a=oldCards if not j else 1.
        w=mix(tip-517,13.,lift)
        h=mix(32.,13.,lift)
        if a:
            # The cyan bar's actual 72.6% endpoint is the datum on the new seat.
            rect(g,x-w,y-h/2,w,h,inkcol(col,.82+.17*lift),on*a*(1-.65*lift))
            if lift>.61:point(g,x,y,mix(5,8,lift),col,phase(lift,.61,.99))
            name_x=x+29;move=enter(t,go-.10,.44)
            label(g,f'{v:.1f}%',name_x,y,39-5*lift,col,move*a,'left',160)
    if ex and oldCards:
        a0=517+53.5*7.7;b0=517+72.6*7.7
        p=[(a0,625),(a0,640),(b0,640),(b0,625)]
        path(g,p,easepos(t,same-.16,.74),Y,2.2,oldCards*ex)
        label(g,'相差 19.1 个百分点',(a0+b0)/2,693,31,Y,oldCards*ex)
    if not settle:return
    axis=enter(t,old-.10,.68)
    hint=enter(t,old+.62,.61)
    for j,(x,name) in enumerate(((XL,'MMLU'),(XR,'MMLU-Pro'))):
        lo,hi=vertical(50),vertical(100)
        label(g,name,x,159,40,F,hint)
        path(g,[(x,hi),(x,lo)],axis,M,1.65,settle*.68)
        for v in (60,80,100):
            yy=vertical(v);line(g,(x-5,yy),(x+6,yy),M,1.3,settle*.52)
            if not j:label(g,str(v),x-27,yy,24,M,settle*.78,'right')
    for j,(name,a,b,col) in enumerate(MODEL):
        at=turn+.70+.14*j
        cy=vertical(a);end_y=vertical(b)
        arrive=enter(t,at,.52)
        if arrive:
            point(g,XL,cy,7.6,col,arrive)
            rail=easepos(t,at+.07,.97)
            route=[(XL,cy),(XR,end_y)]
            path(g,route,rail,col,3.9,arrive*.93)
            if 0<rail<.99:point(g,*ArcLength(route).at(rail),4.4,col,arrive)
            dx=29;stagger=(-33,39)[j]
            label(g,name,XL-dx,cy+stagger,29,col,arrive,'right')
            path(g,[(XL-10,cy),(XL-dx-4,cy+stagger*.56)],arrive,col,1.6,arrive)
            label(g,f'{a:.1f}%',XL+92,cy+stagger*.69,27,col,arrive)
            src_op=phase(rail,.45,.99)
            if j and src_op:
                point(g,XR,end_y,7.,col,src_op)
                label(g,f'{b:.1f}%',XR+29,end_y,34,col,src_op,'left')
    if settle:
        foot=enter(t,old+.88,.52)
        label(g,'同为分步作答',799,742,30,M,foot)
    for j,(right,gap)in enumerate(((False,2.2),(True,8.9))):
        at=(old+.88,spread-.39)[j]
        v=enter(t,at,.61)
        if not v:continue
        dy=[vertical(row[1+j])for row in MODEL]
        bx=(565,1287)[j]
        # Same y scale. The open jaw has exactly the two positions in the data.
        k=easepos(t,at,.71)
        path(g,[(bx-12,dy[0]),(bx,dy[0]),(bx,mix(dy[0],dy[1],k)),(bx-12,mix(dy[0],dy[1],k))],
             1.,Y,2.25,settle*v)
        label(g,f'{gap:.1f}',bx+21,sum(dy)*.5,31,Y,settle*v,'left')
    d=enter(t,spread-.21,.55)
    if d:label(g,'百分点',1376,vertical(63.7)+38,24,M,d)


def lookup(g,c):
    """A harder exam doesn't remove the shortcut when the key is indexed."""
    from exam_paper6 import opts_pos,piece
    t=c.t
    key=c.at('一搜就有');look=c.at('量的还是检索');handoff=c.at('GPQA')-.20
    carry=easepos(t,.025,.66)
    exit_=easepos(t,look+.19,.87)
    left=easepos(t,c.at('依然防不住')-.09,1.02)
    weights=(1-phase(t,handoff-.62,handoff),1-phase(t,handoff-.45,handoff+.36))
    if carry<1:
        endpaper(g,'3-2',dx=-226*carry,dy=-128*carry,sc=1-.105*carry,op=(1-carry)**.78)
    for j,ch in enumerate('ABCDEFGHIJ'):
        a=easepos(t,.25+.034*j,.66)
        if not a:continue
        x0,y0=opts_pos(j,1.)
        x=mix(x0,190+127*(j%5),left)-563*exit_
        y=y0+93*(1-a)+112*exit_+left*19
        hit=enter(t,look-.24,.44) if j==1 else 0.
        co=blend(C if j<4 else O,Y,hit)
        piece(g,ch,x,y,92,co,a*weights[0]*(.92+.08*hit))
    q=enter(t,key-.57,.63)*weights[1]
    if not q:return
    # The matching letter passes straight from the index to the answer slot;
    # no step of the test's reasoning path runs in this exposure.
    x,y=1157+19*(1-q),345;rr=41.
    shadow=(1-exit_*.57)*q
    ring(g,x,y,rr,T,shadow,3.75)
    line(g,(x+29,y+29),(x+71,y+71),T,5.,shadow)
    label(g,'检索',x+1,y-80,30,T,shadow)
    a=enter(t,key-.07,.44);z=easepos(t,key+.20,.66)
    route=[(x,y),(1052,269),(464,271),(317,347)]
    if a:
        label(g,'B',x,y,45,Y,shadow*a*(1-z));path(g,route,z,Y,2.4,shadow*.73*(1-exit_))
        if 0<z<1:
            px,py=ArcLength(route).at(z)
            label(g,'B',px,py,35,Y,shadow*a)
