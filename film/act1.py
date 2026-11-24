"""Lecture 12 — one paper strip, two different questions."""
import math
from visual import *

TOKEN = ('二','加','二','等','于','四')
X = [363+158*j for j in range(6)]
MODEL = (BLUE, PURPLE)
ROWS = (441, 580)
PROBS = ([.9]*5+[.4],[.6]*5+[.8])
HOLD = [1.65,.55,.75,1.65,1.65,1.75,.65,1.65,1.85,.6,.6,1.8,.65,.75,1.75,1.75]


def gate(u, on, end, ramp=.09):
    return step(u,on,on+ramp)*(1-step(u,end,end+ramp))


def paths(g, coords, color=MUTED, width=2, alpha=1, draw=1):
    """Polyline with length-based write-on."""
    lengths = [math.hypot(b[0]-a[0], b[1]-a[1]) for a,b in zip(coords,coords[1:])]
    remaining = sum(lengths)*clamp(draw)
    for a,b,n in zip(coords,coords[1:],lengths):
        if remaining <= 0: break
        q = min(1,remaining/max(n,1e-9))
        g.line(*a,mix(a[0],b[0],q),mix(a[1],b[1],q),color,width,alpha)
        remaining -= n


def paper(g, x, y, label='', color=GOLD, w=104, h=81, strength=1, a=1):
    if a < .001:
        return
    g.rect(x-w/2, y-h/2, w,h, fill=blend(BG,color,.045+.09*strength),
           stroke=blend(GRID,color,.21+.71*strength), width=2.4,r=5,alpha=a)
    if label:
        g.text(label,x,y-1,42 if h>=65 else 30, blend(INK,color,strength*.75),a,font='serif')


def linebar(g, cx, y, w, p, color, alpha=1, *, split=False, h=8):
    g.rect(cx-w/2,y-h/2,w,h,fill=GRID,r=h/2,alpha=alpha)
    v=w*clamp(p)
    if v>1:
        g.rect(cx-w/2,y-h/2,v,h,fill=color,r=h/2,alpha=alpha)
    if split:
        g.line(cx-w/2+v,y-h*.93,cx-w/2+v,y+h*.93,INK,1.4,alpha*.8)


def result_tile(g,x,y,j,alpha, numbers=0, scale=1):
    if alpha<=.002: return
    c=MODEL[j]; ok=j==1
    paper(g,x,y,'四' if ok else '五',GOLD if ok else c,
          94*scale,73*scale,1,alpha)
    g.check(x+72*scale,y,ok,13*scale,alpha)
    if numbers:
        g.text('0.8' if ok else '0.6',x,y+63*scale,29,c,alpha*numbers,font='math')


def numstrip(g, alpha=1, y=252, focus=-1, fade=0, reveal_end=1, xoff=0, last_x=None):
    if alpha<.002:return
    g.line(X[0]-90+xoff,y,X[-1]+110+xoff,y,GRID,1.5,alpha*.85*(1-fade))
    for j,x in enumerate(X):
        a = alpha*((1-fade)**2 if j<5 else 1)
        if j==5 and last_x is not None:
            x=last_x
        g.line(x+xoff,y+51,x+xoff,y+67,GOLD if j==5 else GRID,1.8,a*.8)
        strength = ((.36 if j<5 else .94) if focus<0 else
                    (.97 if j==focus else .30 if j<focus else .07))
        label = TOKEN[j] if j<5 or reveal_end>=.95 else '？'
        paper(g,x+xoff,y,label,GOLD,104,81,strength,a)


def open_board(g, u, alpha=1, full=False, select=.607):
    # The wrong tile arrives with “选了五”; the second move uses the breath
    # before the actual question.
    targets = (step(u,select,select+.062),step(u,select+.071,select+.143)) if not full else (1,1)
    numstrip(g,alpha,reveal_end=targets[0])
    scan = mix(X[0]-55,X[4]+48,step(u,0,.46))
    for k,(y,c) in enumerate(zip(ROWS,MODEL)):
        target=targets[k]
        g.disk(180,y,c,43,'A' if k==0 else 'B',alpha)
        g.line(230,y,283,y,GRID,1.8,alpha*.9)
        for j,x in enumerate(X[:-1]):
            glow = math.exp(-((x-scan)/156)**2)
            a=alpha*mix(.50,1,max(glow,step(u,.22,.51)))
            linebar(g,x,y,106,PROBS[k][j],c,a,h=9)
            g.line(x,y-11,x,y-24,GRID,1.3,a*.75)
        g.line(1099,y,1174,y,GRID,1.5,alpha*.5*(1-target))
        result_tile(g,X[-1],y,k,alpha*target)
    g.rect(X[-1]-63,187,126,461,stroke=GOLD,width=1.6,r=8,
           alpha=alpha*step(u,.3,.60)*.24)
    for j in range(5):
        g.line(X[j]-34,659,X[j]+34,659,BLUE,2.0,alpha*.53*step(u,j*.044,j*.044+.11))
    g.line(X[5]-34,659,X[5]+34,659,GOLD,2.5,alpha*step(u,.44,.72))


def b0(g,u,select=.607):
    open_board(g,u,select=select)


def choice_board(g,u,a=1):
    # The original prefix gets lit one slot at a time; probability bars change
    # only where the golden cursor is, not on masked targets.
    active=mix(0,5,step(u,.86,.995))
    j=min(5,int(active+.25))
    fr=step(u,.13,.28)
    xr=mix(X[0],X[5],active/5)
    numstrip(g,a,y=252,focus=j,fade=0,reveal_end=1-step(u,.15,.3)+step(u,.83,.94))
    # Occlude future targets while keeping their identity in the strip geometry.
    for k in range(j+1,6):
        xx=X[k]
        close=step(u,.18+(k-1)*.021,.27+(k-1)*.021)
        g.rect(xx-50,215,100,74,fill=BG,r=3,alpha=a*fr*.91*close)
        g.text('·',xx,251,37,MUTED,a*fr*.5*close)
    pending=gate(u,.21,.81,.07)
    if pending>0:
        g.rect(X[j]-50,215,100,74,fill=BG,r=3,alpha=a*pending)
        g.text('?',X[j],251,38,GOLD,a*pending,font='math')
    g.line(xr,313,xr,626,GOLD,1.3,a*fr*.40,dash=[4,8])
    g.arc(xr,322,8,0,math.tau,GOLD,2,a*fr*.80)
    for k,(yy,c) in enumerate(zip(ROWS,MODEL)):
        g.disk(180,yy,c,43,'A' if k==0 else 'B',a)
        for h,xx in enumerate(X):
            if h==j:
                p=PROBS[k][j]
                mass=step(u,.39,.57)
                parts=step(u,.48,.63)
                linebar(g,xx,yy,208,p*mass,c,a,h=18,split=mass>.997)
                for rr in (.44,.73):
                    other=xx-104+208*(p+rr*(1-p))
                    g.line(other,yy-7,other,yy+7,MUTED,1.15,a*parts*.55)
                norm=gate(u,.59,.747,.083)
                bracket(g,xx-104,xx+104,yy+25,-6,MUTED,a*norm*.79)
                label=f'{p:.1f}'
                g.text(label,xx-104+208*p/2,yy-36,26,c,a*step(u,.53,.64),font='math')
                # True token is selected by the text, not chosen by max bar.
                marker=xx-104+208*p/2
                g.circle(marker,yy+39,4.5,fill=GOLD,alpha=a*step(u,.73,.81))
            elif h<j:
                linebar(g,xx,yy,106,PROBS[k][h],c,a*.28)
            else:
                g.line(xx-36,yy,xx+36,yy,GRID,2,a*.7)
    g.text('p(xᵢ | x₁⋯xᵢ₋₁)',800,696,32,GOLD,a*step(u,.74,.87),font='math')


def b1(g,u):
    q=step(u,0,.13)
    g.c.save()
    g.c.translate(-36*gate(u,0,.76,.12),0)
    open_board(g,1,1-q,True)
    pivot=(384,422)
    zoom=1+.145*gate(u,.267,.771,.112)
    g.c.translate(*pivot)
    g.c.scale(zoom,zoom)
    g.c.translate(-pivot[0],-pivot[1])
    choice_board(g,u,q)
    g.c.restore()


def b2(g,u):
    q=step(u,0,.12)
    if q<1:
        choice_board(g,1,1-q)
    panel=q
    focus=4 if u<.57 else 5
    fade=step(u,.57,.82)*.7
    numstrip(g,panel,focus=focus,fade=fade)
    wrong=gate(u,.11,.29,.09)
    if wrong>0:
        xx=X[3]
        b=step(u,.13,.24)
        g.arrow(xx-44,203,xx-44-b*78,203-b*37,RED,2,panel*wrong,9)
        paper(g,xx-83,174,'却',RED,67,53,.7,panel*wrong)
        g.line(xx-27,205,xx-23,302,GOLD,1.8,panel*wrong*.6)
    for k,(y,c) in enumerate(zip(ROWS,MODEL)):
        g.disk(180,y,c,43,'A' if k==0 else 'B',panel)
        for h,xx in enumerate(X[:-1]):
            linebar(g,xx,y,106,PROBS[k][h],c,panel*(1-fade))
        reveal=step(u,.61,.79)
        linebar(g,X[5],y,208,PROBS[k][-1],c,panel*(1-reveal),split=True,h=14)
        if reveal>0:
            result_tile(g,X[5],y,k,panel*reveal,reveal)


def bracket(g,x1,x2,y,depth=10,color=MUTED,alpha=1):
    g.line(x1,y,x2,y,color,1.7,alpha)
    g.line(x1,y,x1,y+depth,color,1.7,alpha)
    g.line(x2,y,x2,y+depth,color,1.7,alpha)


def area_panel(g,x,y,s,alpha=1, half=1, eighth=1, grid=1, labels=1, rectangle=1):
    if alpha<.001:return
    g.rect(x,y,s,s,fill=blend(BG,GRID,.18),stroke=GRID,width=2.0,r=0,alpha=alpha)
    if rectangle:
        g.rect(x,y,s*mix(1,.5,half),s*mix(1,.125,eighth),
               fill=blend(BG,GOLD,.36),stroke=GOLD,width=2.15,alpha=alpha*rectangle)
    for i in range(1,8):
        yy=y+s*i/8
        g.line(x,yy,x+s,yy,GRID,1,alpha*grid*eighth*.9)
    g.line(x+s/2,y,x+s/2,y+s,GOLD,1.3,alpha*half*.8)
    if labels:
        bracket(g,x,x+s/2,y-17,8,GOLD,alpha*labels*half)
        g.text('1/2',x+s/4,y-38,29,GOLD,alpha*labels*half,font='math')
        g.line(x-16,y,x-16,y+s/8,GOLD,1.7,alpha*labels*eighth)
        g.line(x-16,y,x-8,y,GOLD,1.7,alpha*labels*eighth)
        g.line(x-16,y+s/8,x-8,y+s/8,GOLD,1.7,alpha*labels*eighth)
        g.text('1/8',x-64,y+s/16,29,GOLD,alpha*labels*eighth,font='math')


def b3(g,u):
    q=step(u,0,.14)
    layer(g,1-q,b2,1)
    into=step(u,.48,.57)
    tile_a=(1-into)*q
    g.line(636,mix(420,505,into),964,mix(420,505,into),GRID,1.55,tile_a)
    for j,xx in enumerate((690,910)):
        paper(g,xx,mix(420,505,into),'',GOLD,105,83,.64,tile_a)
        a=step(u,(.19,.32)[j],(.30,.43)[j])*tile_a
        linebar(g,xx,494,105,(.5,.125)[j],GOLD,a,h=10,split=True)
    s=480
    h=step(u,.64,.72)
    e=step(u,.72,.83)
    area_panel(g,560,222,s,into,h,e,labels=1)
    w=step(u,.84,.95)
    if w>0:
        g.arrow(801,253,1109,253,MUTED,1.8,w,10)
        g.text('1/16',1199,253,46,GOLD,w,font='math')


def b4(g,u):
    split=step(u,.10,.31)
    back=step(u,.74,.96)
    q=split*(1-back)
    g.arrow(801,253,1109,253,MUTED,1.8,1-step(u,.02,.16),10)
    g.text('1/16',1199,253,46,GOLD,1-step(u,.02,.16),font='math')
    s=mix(480,330,q)
    area_panel(g,mix(560,310,q),mix(222,285,q),s)
    if q>.001:
        area_panel(g,mix(560,964,q),mix(222,285,q),s,q)
        g.text('×',800,447,62,MUTED,q,font='math')
    a=gate(u,.32,.69,.10)
    g.text('1/16   ×   1/16',800,667,41,GOLD,a,font='math')
    # Full pipeline probability scales with the number of pieces.
    g.text('=   1/256',800,722,36,INK,gate(u,.43,.69,.10),font='math')


def boxes(g,x,y,cnt=4,margin=17,size=77,a=1):
    for j in range(cnt):
        c=GOLD if j==0 else MUTED
        paper(g,x+(j%2-.5)*(size+margin),y+(j//2-.5)*(size+margin),
              '',c,size,size,1 if j==0 else .22,a)


def b5(g,u):
    resh=step(u,.07,.23)
    shift=step(u,.51,.65)
    l=480
    g0=1-resh
    area_panel(g,560,222,l,g0,1,1,labels=1,rectangle=0)
    wx=l*.5*2**(-resh); hy=l*l/16/wx
    cx=mix(680,780,resh)-215*shift
    cy=mix(252,420,resh)
    g.rect(cx-wx/2,cy-hy/2,wx,hy,fill=blend(BG,GOLD,.36),
           stroke=GOLD,width=2.2)
    brace=step(u,.25,.35)
    bracket(g,cx-wx/2,cx+wx/2,cy+hy/2+11,-7,GOLD,brace)
    g.line(cx-wx/2-13,cy+hy/2,cx-wx/2-13,mix(cy+hy/2,cy-hy/2,step(u,.30,.43)),GOLD,1.35,brace*.63)
    g.text('1/4',cx,cy+hy/2+42,33,GOLD,brace,font='math')
    d=step(u,.61,.74)
    g.arrow(cx+wx/2+59,420,1002,420,MUTED,1.9,d,11)
    g.text('倒数',mix(cx+wx/2+59,1002,.54),387,25,MUTED,d)
    boxes(g,1165,420,a=d)
    g.text('PPL = 4',1165,582,43,GOLD,step(u,.93,.994),font='math')


DIST=(.22,.16,.12,.095,.08,.07,.018,.052,.045,.035,.028,.022,.02,.015,.013,.007)


def b6(g,u):
    q=step(u,.02,.27)
    boxes(g,mix(1165,408,q),420,a=1)
    g.text('PPL = 4',mix(1165,408,q),582,43,GOLD,1-.46*q,font='math')
    g.rect(505,360,120,120,fill=blend(BG,GOLD,.36),stroke=GOLD,width=2,alpha=1-q)
    g.text('1/4',565,522,33,GOLD,1-q,font='math')
    d=step(u,.20,.42)
    move=step(u,.69,.86)
    masses=list(DIST)
    masses[0]-=.063*(1-move); masses[6]+=.063*(1-move)
    widths=[673*p/sum(masses) for p in masses]
    canon=813
    cur=canon
    yy=mix(420,391,move)
    for i,w in enumerate(widths):
        sel=i==6
        a=d*(1-.55*move if not sel else 1)
        height=95 if sel else 73
        g.rect(cur+1.5,yy-height/2,max(2,w-3),height,
               fill=blend(BG,GOLD,.62) if sel else blend(BG,MUTED,.19+i*.009),
               stroke=GOLD if sel else GRID,width=1.5,alpha=a)
        if sel:
            sx=cur+w/2
        cur+=w
    g.line(785,278,785,562,GRID,1.5,d)
    d2=step(u,.48,.64)
    g.line(sx,yy+48,sx,528,GOLD,1.6,d2)
    g.text('原文词元',sx,558,25,GOLD,d2)
    g.line(sx,yy-50,sx,290,GOLD,1.5,move*.8)
    g.text('p ↓',sx,265,38,GOLD,move,font='math')


def layer(g, alpha, fn, *args, **kw):
    if alpha<=.002:return
    if alpha>=.998:
        fn(g,*args,**kw)
        return
    g.c.push_group()
    fn(g,*args,**kw)
    g.c.pop_group_to_source()
    g.c.paint_with_alpha(alpha)


def bit(g,x,y,alpha=1,color=GOLD,s=60):
    g.rect(x-s/2,y-s/2,s,s,fill=blend(BG,color,.24),stroke=color,width=1.7,r=5,alpha=alpha)
    g.circle(x,y,3.7,fill=color,alpha=alpha*.8)


def formula(g, y=675, alpha=1):
    if alpha<.002:return
    g.text('PPL = exp',595,y,39,INK,alpha,font='math',align='right')
    g.text('(',619,y,54,MUTED,alpha,font='math')
    g.text('−',665,y,41,INK,alpha,font='math')
    g.text('1',710,y-21,28,INK,alpha,font='math')
    g.text('T',710,y+22,28,INK,alpha,font='math')
    g.line(690,y+1,730,y+1,MUTED,1.5,alpha)
    g.text('∑',776,y,57,INK,alpha,font='math')
    g.text('i',776,y+36,16,MUTED,alpha,font='math')
    g.text('ln pᵢ',875,y,39,GOLD,alpha,font='math')
    g.text(')',957,y,54,MUTED,alpha,font='math')


def b7_body(g,u):
    q=step(u,.34,.56)
    z=step(u,.63,.78)
    k=step(u,.78,.90)
    forms = ((495,.5,1),(1005,.125,3))
    for j,(cx,p,n) in enumerate(forms):
        yy=315
        linebar(g,cx,yy,310,p,GOLD,1-q*.87,h=22,split=True)
        g.text('1/2' if j==0 else '1/8',cx,yy-54,40,GOLD,1-q*.60,font='math')
        sw=mix(0,58,q)
        startx=cx-155+155*p
        bit_xy=[]
        for b in range(n):
            # Probability rectangles are converted one-to-one to a stack of
            # surprisal units (bits), rather than copied as ornamental bars.
            bx=mix(startx,cx,q)
            by=mix(yy,486-b*67,q)
            merge_index=b if j==0 else b+1
            bx=mix(bx,800,z)
            by=mix(by,585-merge_index*67,z)
            spread_x=732 if merge_index in (0,1) else 868
            spread_y=535-(merge_index%2)*67
            bx=mix(bx,spread_x,k)
            by=mix(by,spread_y,k)
            if sw>.01:
                bit(g,bx,by,mix(.25,1,q),GOLD,sw)
            bit_xy.append((bx,by))
        if u<.70:
            g.text('1 bit' if j==0 else '3 bits',cx,572,36,INK,gate(u,.47,.65,.05),font='math')
    shown=step(u,.80,.90)
    if shown>.001:
        g.line(690,587,910,587,GRID,1.3,shown)
        g.text('2 bits',800,623,33,GOLD,gate(u,.85,.94,.055),font='math')
    f=step(u,.91,.996)
    formula(g,691,f)
    g.text('= 4',1044,691,40,GOLD,f,font='math')


def b7(g,u):
    q=step(u,0,.14)
    layer(g,1-q,b6,1)
    layer(g,q,b7_body,u)


def cumulative(g,u,alpha=1):
    # Cumulative negative log probability. Y increases up the screen.
    fin=step(u,.49,.64)
    hide=step(u,.76,.94)
    basey=602
    x0=232
    xa=[x0,*X]
    a=alpha*(1-hide)
    numstrip(g,alpha,252,fade=hide,last_x=mix(X[5],964,hide))
    g.line(x0,basey,X[5]+95,basey,GRID,1.4,a)
    g.line(x0,basey,x0,342,GRID,1.4,a)
    ypx=56
    for j in range(1,5):
        g.line(x0,basey-j*ypx,X[5]+18,basey-j*ypx,GRID,1,a*.55)
    g.text('累计损失',x0,basey+41,25,MUTED,a,align='left')
    for j,c in enumerate(MODEL):
        yv=[basey]; total=0
        for p in PROBS[j]:
            total+=-math.log2(p)
            yv.append(basey-total*ypx)
        coords=list(zip(xa,yv))
        d=step(u,.15,.47)
        paths(g,coords,c,3,a,d)
        ll=[0]
        for start,end in zip(coords,coords[1:]):
            ll.append(ll[-1]+math.dist(start,end))
        for n,((xx,yy),traveled) in enumerate(zip(coords,ll)):
            reveal=traveled/ll[-1]
            cf=step(d,reveal-.013,reveal)
            g.circle(xx,yy,5.1 if n<6 else 7.1,fill=c,alpha=a*cf)
            if n==6:
                g.circle(xx,yy,14,stroke=c,width=1.5,alpha=a*cf*.6)
        start=yv[6]
        if (1-hide)*fin>.001:
            g.text('1.272' if j==0 else '1.589',X[5]+108,start,32,c,alpha*(1-hide)*fin,font='math',align='left')
            g.text('PPL',X[5]+111,start-32,20,MUTED,alpha*(1-hide)*fin,font='math',align='left')
    # Camera stops on the one token which can change the outcome.
    if hide>.001:
        for j,c in enumerate(MODEL):
            x=mix(X[5],964,hide)
            y=(409,570)[j]
            g.disk(x-304,y,c,43,'A' if j==0 else 'B',alpha*hide)
            g.arrow(x-240,y,x-80,y,MUTED,1.4,alpha*hide*.62,9)
            result_tile(g,x,y,j,alpha*hide,0,1.08)


def b8(g,u):
    q=step(u,0,.16)
    layer(g,1-q,b7_body,1)
    cumulative(g,u,q)


def letter_strip(g,y,color,indices,alpha=1,cuts=1,allchars=1,r=7):
    letters='sunrise'
    x0=516
    w=81
    for n in range(len(indices)-1):
        l,rr=indices[n:n+2]
        start=x0+w*l
        aw=w*(rr-l)
        g.rect(start+2*cuts,y-41,aw-4*cuts,82,fill=blend(BG,color,.105),
               stroke=blend(GRID,color,.74),width=2.1,r=r*cuts,alpha=alpha)
    for n,ch in enumerate(letters):
        g.text(ch,x0+w*(n+.5),y,51,blend(INK,color,.15),alpha*allchars,font='math')
    return x0,w


def b9_body(g,u,counts=1):
    q=step(u,.61,.74)
    d=step(u,.75,.92)
    letter_strip(g,252,GOLD,(0,7),alpha=.88,cuts=1)
    for j,c in enumerate(MODEL):
        yy=mix(252,(430,590)[j],q)
        a=q
        g.disk(386,yy,c,43,'A' if j==0 else 'B',a)
        ids=((0,3,7),(0,1,3,5,7))[j]
        shape=step(u,.65+j*.083,.77+j*.083)
        letter_strip(g,yy,c,ids if shape>.12 else (0,7),a,shape)
        g.text('2' if j==0 else '4',1177,yy,47,c,a*d*counts,font='math')
    g.line(516,700,1083,700,GRID,1.5,d*.8)
    g.line(516,693,516,707,GRID,1.5,d*.8)
    g.line(1083,693,1083,707,GRID,1.5,d*.8)


def b9(g,u):
    q=step(u,.53,.67)
    measure=step(u,.06,.23)
    strip_y=mix(252,300,measure)
    if q<.999:
        numstrip(g,1-q,strip_y,fade=1-measure,last_x=mix(964,X[-1],measure))
        a0=(1-q)*(1-step(u,.035,.153))
        for j,c in enumerate(MODEL):
            y=(409,570)[j]
            g.disk(660,y,c,43,'AB'[j],a0)
            g.arrow(724,y,884,y,MUTED,1.4,a0*.62,9)
            result_tile(g,964,y,j,a0,0,1.08)
        a=measure*(1-q)
        bracket(g,X[0]-55,X[-1]+55,422,12,BLUE,a*.84)
        bracket(g,X[-1]-54,X[-1]+54,487,13,GOLD,a)
        beamx=mix(X[0]-55,X[-1]+55,step(u,.17,.36))
        g.line(beamx,strip_y+73,beamx,421,BLUE,1.65,a*.65,dash=[3,6])
        g.arrow(X[-1],strip_y+73,X[-1],486,MUTED,1.38,a*.63,9)
    layer(g,q,b9_body,u)


def stackdoc(g,x,y,count,size=1,a=1,color=GOLD,kind='words'):
    w,h=145*size,173*size
    for j in range(count-1,-1,-1):
        xx=x+j*13*size
        yy=y-j*10*size
        g.rect(xx-w/2,yy-h/2,w,h,fill=blend(BG,color,.062),stroke=blend(GRID,color,.51),
               width=1.7,r=5,alpha=a*(1-min(j,7)*.06))
        if j!=0:continue
        if kind=='words':
            for k,row in enumerate((.68,.54,.72,.36)):
                ypos=yy-37*size+k*21*size
                g.line(xx-w*.32,ypos,xx+w*(-.32+row),ypos,color,2*size,a*.78)
        elif kind=='chat':
            pw,ph=w*.58,h*.32
            g.rect(xx-pw/2,yy-ph/2,pw,ph,stroke=color,width=2,r=10,alpha=a*.92)
            g.poly([(xx-w*.16,yy+ph/2),(xx-w*.20,yy+ph*.71),(xx-w*.034,yy+ph/2)],
                   color,1.8,a*.92)
            for k in range(3):
                g.circle(xx+(k-1)*16*size,yy,3.1*size,fill=color,alpha=a*.8)
        else:
            g.text('∑',xx,yy,54*size,color,a,font='math')


def b10(g,u):
    erase=step(u,.27,.58)
    docs=step(u,.67,.96)
    stable=(1-docs)
    a=(1-erase)*stable
    if a>.001: layer(g,a,b9_body,1,1-step(u,.26,.34))
    byte=erase*stable
    if byte>.001:
        letter_strip(g,252,GOLD,tuple(range(8)),alpha=byte,cuts=1)
        for j,(p,c) in enumerate(zip([.5,.7],MODEL)):
            yy=(430,590)[j]
            g.disk(386,yy,c,43,'A' if j==0 else 'B',byte)
            start=516
            for k in range(7):
                xx=start+k*81+.5
                g.rect(xx,yy-13,79,25,fill=GRID,r=4,alpha=byte)
                g.rect(xx,yy-13,79*p*erase,25,fill=c,r=4,alpha=byte)
                g.line(xx+78,yy+18,xx+78,yy+30,GRID,1.5,byte)
            g.text(f'{p:.1f}',1177,yy,44,c,byte*step(u,.46,.60),font='math')
        g.text('bits / byte',1177,684,26,MUTED,byte,font='math')
    if docs>.001:
        stackdoc(g,mix(660,470,docs),mix(442,319,docs),6,.83,docs,GOLD,'chat')
        stackdoc(g,mix(940,1100,docs),mix(442,319,docs),2,.83,docs,GOLD,'math')


def domain_body(g,u):
    swap=step(u,.45,.59)
    doc_a=1-step(u,.43,.61)
    doc_b=step(u,.46,.58)
    stackdoc(g,470,319,6,.83,doc_a,GOLD,'chat')
    stackdoc(g,470,319,2,.83,doc_b,GOLD,'chat')
    stackdoc(g,1100,319,2,.83,doc_a,GOLD,'math')
    stackdoc(g,1100,319,6,.83,doc_b,GOLD,'math')
    k=step(u,.05,.24)
    for j,(x,pair) in enumerate(((470,(2,4)),(1100,(8,2)))):
        for m,c in enumerate(MODEL):
            rx=x+(-1 if m==0 else 1)*64
            g.circle(rx-42,484,5,fill=c,alpha=k)
            g.text(str(pair[m]),rx,484,33,c,k,font='math')
    g.text('PPL',800,484,24,MUTED,k*.77,font='math')
    y=642
    g.arrow(355,y,1230,y,MUTED,1.65,k,10)
    start=420; w=380
    for j in range(3):
        x=start+j*w
        g.line(x,y-9,x,y+9,GRID,1.8,k)
        g.text(str(1+j),x,y+36,25,MUTED,k,font='math')
    pchat=mix(.75,.25,swap)
    xA=start+w*((pchat+3*(1-pchat))-1)
    xB=start+w*((2*pchat+1-pchat)-1)
    for j,(x,c) in enumerate(((xA,BLUE),(xB,PURPLE))):
        yy=y+(-23 if j==0 else 22)
        g.line(x,y,x,yy,c,1.4,k*.72)
        g.disk(x,yy,c,12,'',k)
    g.text('bits / token',1242,y+38,25,MUTED,k,font='math')
    p=step(u,.60,.73)
    if p>.001:
        g.text('Paloma',800,176,45,INK,p,font='serif')


def b11(g,u):
    domain_body(g,u)


def corpus_tile(g,x,y,kind='page',s=1,a=1):
    if a<.002:return
    paper(g,x,y,'',GOLD,84*s,84*s,.64,a)
    if kind=='web':
        g.circle(x,y,24*s,stroke=GOLD,width=1.6,alpha=a)
        g.arc(x-9*s,y,27*s,-1.03,1.03,GOLD,1.4,a)
        g.arc(x+9*s,y,27*s,2.11,4.17,GOLD,1.4,a)
        g.line(x-23*s,y,x+23*s,y,GOLD,1.4,a)
    elif kind=='tree':
        for side in (-1,1):
            g.line(x,y-16*s,x+side*16*s,y+12*s,GOLD,1.7,a)
            g.circle(x+side*16*s,y+12*s,4*s,fill=GOLD,alpha=a)
        g.circle(x,y-16*s,4*s,fill=GOLD,alpha=a)
    else:
        for k in range(3):
            g.line(x-19*s,y+(k-1)*13*s,x+(19-5*k)*s,y+(k-1)*13*s,GOLD,1.6,a)


def corpus(g,x,y,kind='page',s=1,a=1,n=6):
    w=84*s
    for j in range(n-1,0,-1):
        g.rect(x-w/2-j*13*s,y-w/2-j*10*s,w,w,fill=blend(BG,GOLD,.04),
               stroke=blend(GRID,GOLD,.38),width=1.45,r=4,alpha=a*(1-j*.055))
    corpus_tile(g,x,y,kind,s,a)


def model_matrix(g,x,y,alpha,learned,update=0):
    if alpha<.002:return
    g.circle(x,y,76,stroke=INK,width=1,alpha=alpha*.24)
    g.circle(x,y,66,fill=blend(BG,INK,.067),stroke=INK,width=2.4,alpha=alpha)
    for row in range(3):
        for col in range(3):
            rank=(row*5+col*7)%9
            weight=mix(.27,.27+.075*rank,learned)
            cc=blend(MUTED,GOLD,.45*update)
            g.rect(x+(col-1)*19-6,y+(row-1)*19-6,12,12,
                   fill=cc,r=2,alpha=weight*alpha)


def corpus_motion(g,x0,x1,y,kind,send,alpha):
    if alpha<.002 or send<.001:return
    tx=mix(x0,x1,send)
    g.line(x0,y,tx,y,MUTED,1.65,alpha*.74)
    corpus_tile(g,tx,y-13*math.sin(math.pi*send),kind,mix(.54,.34,send),alpha)


def corpus_result(g,u,alpha):
    if alpha<.002:return
    q=step(u,.66,.76)
    paths(g,[(800,454),(800,523),(608,523),(608,578)],MUTED,1.6,alpha*.78,q)
    for j,p in enumerate((.89,.42,.72,.26,.81)):
        f=step(u,.72+.032*j,.79+.032*j)
        x=608+j*96
        paper(g,x,596,'',GOLD,69,58,.21+.55*(j==4),alpha*f)
        linebar(g,x,652,69,p*f,GOLD,alpha*f,h=6)


def b12_body(g,u):
    y=382
    world=step(u,.035,.15)
    split=step(u,.247,.349)
    swap=step(u,.387,.49)
    left=mix(510,421,world)
    test_x=mix(421,1191,split)
    test_y=y-112*math.sin(split*math.pi)
    # A slice of the same stack travels over the model and is held aside.
    # In the cross-domain example the two recognizable page shapes diverge.
    corpus(g,left,y,'page',1.12,world*(1-swap),6)
    corpus(g,test_x,test_y,'page',.90,world*step(u,.247,.283)*(1-swap),3)
    if swap>.001:
        corpus(g,left,y,'web',1.12,world*swap,7)
        corpus(g,test_x,test_y,'tree',.90,world*swap,3)
    for start,end,kind in ((.252,.304,'page'),(.457,.527,'web')):
        send=step(u,start,end)
        corpus_motion(g,486,741,y,kind,send,gate(u,start,end+.003,.024)*world)
    yr=y
    for start,end,kind in ((.351,.393,'page'),(.556,.692,'tree')):
        send=step(u,start,end)
        corpus_motion(g,1140,857,yr,kind,send,gate(u,start,end+.006,.026)*world)
    learn_base=step(u,.255,.308)
    learn_web=step(u,.47,.528)
    trained=learn_base*(1-swap)+learn_web*swap
    pulse=max(gate(u,.27,.305,.03),gate(u,.48,.523,.03))
    model_a=step(u,.158,.247)
    model_matrix(g,800,y,model_a,trained,pulse)
    g.text('GPT-2',800,y-107,35,INK,step(u,.387,.447),font='serif')
    # Each evaluation emits traceable probabilities, while the weight grid
    # in the circle remains immobile; test material never enters a train loop.
    proof1=gate(u,.374,.420,.029)
    if proof1>.001:
        g.arrow(800,454,800,551,MUTED,1.6,proof1,8)
        linebar(g,800,566,176,.74,GOLD,proof1,h=9)
    corpus_result(g,u,step(u,.66,.715))


def b12(g,u):
    layer(g,1-step(u,0,.139),domain_body,1)
    b12_body(g,u)


COST_POINTS=((442,456),(1198,347))


def clock(g,x,y,s=1,a=1,c=MUTED):
    g.circle(x,y,31*s,stroke=c,width=1.9,alpha=a)
    g.line(x,y,x,y-16*s,c,1.8,a)
    g.line(x,y,x+13*s,y+9*s,c,1.8,a)
    g.circle(x,y,3*s,fill=c,alpha=a)


def cost_body(g,u):
    q=step(u,.11,.35)
    budget=step(u,.39,.64)
    fx=step(u,.54,.72)
    due=step(u,.80,.99)
    xbudget=mix(1290,891,budget)
    y0=648
    x0=334
    g.arrow(x0,y0,1328,y0,MUTED,1.7,q,10)
    g.arrow(x0,y0,x0,227,MUTED,1.7,q,10)
    g.text('正确率',x0,190,27,MUTED,q,align='left')
    g.text('单次成本',1327,723,27,MUTED,q,align='right')
    for j,(x,y) in enumerate(COST_POINTS):
        color=MODEL[j]
        a=q if j==0 else q*(1-.49*fx)
        g.line(x,y,x,y0,GRID,2,a,dash=[5,8])
        g.line(x0,y,x,y,GRID,2,a,dash=[5,8])
        g.disk(x,y,color,mix(23,36,q),'A' if j==0 else 'B',a)
        g.text(('¥0.01','¥0.08')[j],x,y0+32,28,color,a,font='math')
        g.text(('74%','82%')[j],x0-26,y,28,color,a,align='right',font='math')
    b=step(u,.34,.46)
    if b>.001:
        g.rect(xbudget,248,1306-xbudget,400,fill=GOLD,alpha=b*.032)
        g.line(xbudget,228,xbudget,y0,GOLD,2.2,b)
        g.circle(xbudget,y0,6,fill=GOLD,alpha=b)
        g.text('预算',xbudget,196,28,GOLD,b)
        g.check(COST_POINTS[1][0]+61,COST_POINTS[1][1],False,16,fx)
    if due>.001:
        clock(g,1255,278,1,due,GOLD)


def b13(g,u):
    q=step(u,.02,.23)
    layer(g,1-q,b12_body,1)
    cost_body(g,u)


def blade(g,x,y,a,c,j,rotate):
    p=((-29,20),(-8,-25),(31,-15),(12,27)) if j==0 else ((-31,11),(-1,-30),(30,13),(2,22))
    cs,sn=math.cos(rotate),math.sin(rotate)
    pts=[(x+cs*xx-sn*yy,y+sn*xx+cs*yy) for xx,yy in p]
    g.poly(pts,c,2,a,close=True,fill=blend(BG,c,.18),fill_alpha=a)
    g.line(x-6*cs+14*sn,y-6*sn-14*cs,x+13*cs-13*sn,y+13*sn+13*cs,c,1.65,a)


def system_body(g,u):
    q=step(u,.035,.22)
    clear=step(u,.51,.65)
    cast=step(u,.405,.522)
    open_in=step(u,.058,.178)
    same=step(u,.555,.652)
    fork=step(u,.621,.754)
    exchange=step(u,.713,.814)
    grounded=step(u,.85,.968)
    for j,(sx,sy) in enumerate(COST_POINTS):
        pos=((530,420),(1070,420))[j]
        x=mix(sx,pos[0],q)
        y=mix(sy,pos[1],q)
        a=.50+.50*q if j else 1
        g.disk(x,y,MODEL[j],mix(36,55,q),'AB'[j],a*(1-.82*cast))
        turn=(.27 if j==0 else -.38)*exchange
        blade(g,x,y,cast,MODEL[j],j,turn)
        at=open_in*(1-clear)
        if at>.001:
            dx=(-1 if j==0 else 1)*83
            off=36*clear-20*(1-open_in)
            stackdoc(g,x+dx*mix(.68,1,open_in), y-165-off,3+j,.49,at,GOLD)
            clock(g,x-dx*mix(.68,1,open_in),y-165-off,.65,at,GOLD)
            paths(g,[(x+dx,y-104-off),(x+dx*.41,y-50)],MUTED,1.6,at,open_in)
            paths(g,[(x-dx,y-131-off),(x-dx*.41,y-51)],MUTED,1.6,at,open_in)
        if fork>.001:
            elbow=(x,330)
            paths(g,[(800,330),elbow,(x,y-52)],MUTED,1.65,.89,fork)
            carry=step(u,.682,.754)
            chip_a=gate(u,.669,.754,.034)
            firstleg=abs(x-800)/(abs(x-800)+max(0,y-52-330))
            if carry<firstleg:
                cx,cy=mix(800,x,carry/firstleg),330
            else:
                cx,cy=x,mix(330,y-52,(carry-firstleg)/(1-firstleg))
            g.rect(cx-5,cy-5,10,10,fill=GOLD,r=1.5,alpha=chip_a*fork)
        if grounded>.001:
            g.line(x,y+53,x,523,GRID,1.5,grounded)
            g.circle(x,523,4.5,fill=MODEL[j],alpha=grounded)
    if same>.001:
        cy=mix(162,226,same)
        stackdoc(g,mix(790,740,same),cy,4,.46,same,GOLD)
        clock(g,mix(810,861,same),cy+8,.70,same,GOLD)
        paths(g,[(740,267),(740,299),(800,299),(800,330)],MUTED,1.6,same,fork)
        paths(g,[(861,258),(861,299),(800,299)],MUTED,1.6,same,fork)
        g.circle(800,330,5,fill=GOLD,alpha=fork)
    if grounded>.001:
        g.line(mix(800,448,grounded),523,mix(800,1152,grounded),523,GRID,1.8,grounded)


def b14(g,u):
    q=step(u,0,.14)
    layer(g,1-q,cost_body,1)
    layer(g,q,system_body,u)


# 1,000 squares, one fixed item order, two different sets of missed items.
MISSES_A={(13+61*k)%1000 for k in range(19)}
MISSES_B={(13+137*k)%1000 for k in range(10)}
GRID_XY=tuple((311+20*(j%50),208+13*(j//50)) for j in range(1000))

def score_grid(g, amount, alpha, model):
    n=int(clamp(amount)*len(GRID_XY))
    misses=MISSES_A|MISSES_B
    c=g.c
    c.new_path()
    for j,(x,y) in enumerate(GRID_XY[:n]):
        if j not in misses:
            c.rectangle(x-4,y-4,8,8)
    g.source(blend(BG,GREEN,.30),alpha*.78); c.fill_preserve()
    g.source(GREEN,alpha*.78); c.set_line_width(1); c.stroke()
    for j in sorted(misses):
        if j>=n:
            break
        x,y=GRID_XY[j]
        red=mix(float(j in MISSES_A),float(j in MISSES_B),model)
        color=blend(GREEN,RED,red)
        g.rect(x-4,y-4,8,8,fill=blend(BG,color,.30+.45*red),
               stroke=color,width=1.0,alpha=alpha*(.78+.22*red))


def b15_body(g,u):
    q=step(u,.15,.32)
    out=step(u,.79,.993)
    fill=step(u,.16,.54)
    aa=(1-out)*q
    hidden=step(u,.46,.64)
    if aa>.001:
        score_grid(g,fill,aa,step(u,.40,.58))
        g.text('1,000',800,510,49,GOLD,aa*step(u,.18,.34),font='math')
        g.line(415,610,1185,610,GRID,2.2,aa*hidden)
        g.text('100%',1194,655,27,MUTED,aa*hidden,font='math')
    for j,c in enumerate(MODEL):
        xpos=415+770*mix(.83,.981+j*.009,hidden)
        yy=610+(-23 if j==0 else 23)
        g.line(xpos,610,xpos,yy,c,1.8,aa*hidden)
        if hidden>.001:
            x=mix(xpos,(530,1070)[j],out)
            y=mix(yy,420,out)
            r=mix(11,53,out)
            g.disk(x,y,c,r,'AB'[j] if out>.48 else '',q*hidden)
    g.tile(800,mix(510,420,out),68*mix(.5,1,out),62*mix(.5,1,out),'',GOLD,out,True)


def b15(g,u):
    q=step(u,0,.19)
    layer(g,1-q,system_body,1)
    # Pull the decisive answer out of the study, then multiply that same
    # evidence tile into an exam's worth of independent outcomes.
    focus=step(u,.036,.174)
    seed=step(u,.035,.128)*(1-step(u,.218,.362))
    if seed>.001:
        y=mix(415,300,focus)
        g.tile(800,y,mix(68,142,focus),mix(62,125,focus),'',GOLD,seed,True)
        g.text('四',800,y,mix(33,61,focus),GOLD,seed,font='serif')
    for j,(x,y) in enumerate(GRID_XY[:7]):
        k=step(u,.16+.009*j,.31+.009*j)
        a=step(u,.17+.009*j,.23+.009*j)*(1-step(u,.27+.01*j,.35+.01*j))
        g.tile(mix(800,x,k),mix(300,y,k),mix(38,9,k),mix(35,9,k),'',GOLD,a,True)
    b15_body(g,u)


# At an important reveal, time is held on the finished layout rather than
# continuing an ambient pan through the audience's thinking time.
BEATS=(b0,b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12,b13,b14,b15)


def draw(g, i, t, duration):
    played=max(duration-HOLD[i],duration*.64)
    u=clamp(t/max(played,.001))
    if i==0:
        select=g.cue('选了五',.607*played/duration)*duration/played
        b0(g,u,clamp(select,.53,.69))
    else:
        BEATS[i](g,u)
