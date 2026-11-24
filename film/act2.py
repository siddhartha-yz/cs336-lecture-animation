"""CS336 / Evaluation: chapter 2. Vector animation in the shared logical stage."""
from math import cos, exp, pi, sin
from pathlib import Path
import json
from visual import *


def window(u, a, b, c, d):
    return step(u, a, b) * (1 - step(u, c, d))


def bez(g, p0, p1, p2, p3, color=MUTED, width=2, alpha=1, portion=1):
    c = g.c
    if portion < 1:
        q0 = tuple(mix(a,b,portion) for a,b in zip(p0,p1))
        q1 = tuple(mix(a,b,portion) for a,b in zip(p1,p2))
        q2 = tuple(mix(a,b,portion) for a,b in zip(p2,p3))
        r0 = tuple(mix(a,b,portion) for a,b in zip(q0,q1))
        r1 = tuple(mix(a,b,portion) for a,b in zip(q1,q2))
        p1,p2,p3=q0,r0,tuple(mix(a,b,portion) for a,b in zip(r0,r1))
    g.source(color, alpha)
    c.set_line_width(width)
    c.move_to(*p0)
    c.curve_to(*p1,*p2,*p3)
    c.stroke()


def halo(g, x, y, r, color=GOLD, alpha=1):
    for j in range(4):
        g.circle(x,y,r+6*j,None,color,1.25,alpha*(.44 - .091*j))


def pill(g, s, x, y, color=GOLD, alpha=1, width=None, size=31, h=61):
    if alpha <= 0:
        return
    font='math' if any(mark in s for mark in (' = ', ' + ', ' × ')) else 'sans'
    w=max(width or 72,g.measure(s,size,font=font,weight='medium')+28)
    g.rect(x-w/2,y-h/2,w,h,blend(BG,color,.09),color,1.65,11,alpha*.94)
    g.text(s,x,y,size,color,alpha,font=font,weight='medium')


def link(g, a, b, animate, color=MUTED, alpha=1, width=2.05):
    if animate<=0 or alpha<=0:
        return
    ex, ey = mix(a[0],b[0],animate), mix(a[1],b[1],animate)
    g.arrow(a[0],a[1],ex,ey,color,width,alpha,head=9)


def packet(g, x, y, w=113, h=136, color=MUTED, a=1, detail=0, dz=.52):
    """A document icon; the internal lines indicate data, never semantic labels."""
    if a <= 0:
        return
    g.rect(x-w/2,y-h/2,w,h,blend(BG,color,.064),color,1.45,9,a)
    if not detail:
        return
    for j,z in enumerate((.63,.52,.35)):
        yy=y-h/2+29+j*15
        g.line(x-w/2+16,yy,x-w/2+16+(w-25)*z,yy,color,2,a*dz)
    if detail>=2:
        g.rect(x-w/2+17,y+12,w-34,h/3,None,color,1,2,a*.55)
        g.poly([(x-w/2+24,y+12+h/4),(x-2,y+17),(x+11,y+28),(x+w/2-23,y+19)],color,1.5,a*.75)


def _exam(g, i, u):
    """The same two answer sheets first collide at 10, then diverge."""
    intro = step(u,.015,.18) if i==0 else 1
    switch = step(u,.04,.19) if i==1 else 0
    out = step(u,.89,1.0) if i==1 else 0
    zero_case = window(u,.55,.66,.74,.86) if i==1 else 0
    weight=(1-out)*(1-.83*zero_case)
    # The transition is driven by the same card and model identity disks.
    if i==0 and intro < 1:
        g.tile(800,mix(420,198,intro),mix(68,179,intro),mix(62,61,intro),'',GOLD,1,True)
        g.text('3 + 4 = ?',800,mix(420,198,intro),41,GOLD,step(intro,.35,1),font='math')
    else:
        pill(g,'3 + 4 = ?',800,198,GOLD,1-switch*(1-out),190,39,65)
        pill(g,'3 + 4 × 2 = ?',800,198,GOLD,switch*(1-out),268,39,65)
    g.disk(mix(530,276,intro),mix(420,361,intro),BLUE,mix(53,46,intro),'A',weight)
    g.disk(mix(1070,276,intro),mix(420,508,intro),PURPLE,mix(53,46,intro),'B',weight)
    for k, (y,color,miss) in enumerate(((361,BLUE,(3,6,9)),(508,PURPLE,(6,)))):
        for j in range(10):
            x = 432+j*82
            visible=step(intro,.18+.05*j,.68+.034*j)*weight
            if i==0:
                done=step(u,.18+.030*k+j*.024,.232+.030*k+j*.024)
                g.rect(x-27,y-28,54,56,blend(BG,color,.075),blend(GRID,color,.25),1.5,7,visible)
                g.check(x,y,True,14,visible*done)
            else:
                verify = step(u,.10+j*.012,.19+j*.015) if j in miss else 1
                inspect = sin(pi*step(u,.02+.008*j,.19+.009*j)) if j in (3,6,9) else 0
                accent=blend(blend(GRID,color,.25),GOLD,inspect)
                g.rect(x-27,y-28,54,56,blend(BG,accent,.21),accent,1.5,7,visible)
                if j in miss:
                    g.check(x,y,True,14,visible*(1-verify))
                    g.check(x,y,False,14,visible*verify)
                else:
                    g.check(x,y,True,14,visible)
        rank_in = step(u,.43+.032*k,.52+.034*k) if i==0 else 1
        g.text('/ 10',1371,y,44,color,rank_in*weight,font='math',weight='bold')
        phase = step(u,.234,.37) if i==1 else 0
        if i==1 and phase:
            g.c.save()
            g.c.rectangle(1230,y-28,111,56)
            g.c.clip()
            g.text('10',1322,y-48*phase,44,color,(1-phase)*weight,align='right',font='math',weight='bold')
            g.text(str(10-len(miss)),1322,y+48*(1-phase),44,color,phase*weight,align='right',font='math',weight='bold')
            g.c.restore()
        else:
            g.text('10',1322,y,44,color,rank_in*weight,align='right',font='math',weight='bold')
    if i==0:
        roof=step(u,.60,.78)
        g.line(534,622,1130,622,MUTED,1.5,roof*.63)
        g.line(534,613,534,631,MUTED,2,roof*.74)
        g.line(1130,593,1130,646,GOLD,2.9,roof*.96)
        g.text('0',534,664,24,MUTED,roof,font='math')
        g.text('10',1130,664,25,GOLD,roof,font='math')
        hit = step(u,.65,.84)
        g.disk(mix(666,1130,hit),622,BLUE,13,'',roof)
        g.disk(mix(754,1130,hit),622,PURPLE,7,'',roof)
        halo(g,1130,622,26,GOLD,roof*step(hit,.76,1)*.45)
    else:
        a=1-out
        g.line(534,622,1130,622,MUTED,1.5,a*.63)
        g.line(534,613,534,631,MUTED,2,a*.74)
        g.line(1130,593,1130,646,GOLD,2.9,a*.96)
        g.text('0',534,664,24,MUTED,a,font='math')
        g.text('10',1130,664,25,GOLD,a,font='math')
        separate=step(u,.26,.46)
        g.disk(mix(1130,951,separate),622,BLUE,13,'',a*(1-.58*zero_case))
        g.disk(mix(1130,1070,separate),622,PURPLE,mix(7,13,separate),'',a*(1-.58*zero_case))
        if zero_case:
            arrival=step(u,.57,.69)
            g.disk(mix(951,534,arrival),622,BLUE,13,'',zero_case)
            g.disk(mix(1070,534,arrival),622,PURPLE,mix(13,7,arrival),'',zero_case)
            halo(g,534,622,26,RED,zero_case*arrival*.63)


def _choice(g, expand, seen=1, graph=1, alpha=1, morph=0):
    """One correct tile stays the same while additional choices split the measure."""
    if alpha<=0:
        return
    qx = mix(800,1110,morph)
    qy = mix(198,181,morph)
    pill(g,'3 + 4 = ?',qx,qy,GOLD,alpha,mix(190,164,morph),mix(39,29,morph),mix(65,51,morph))
    y= mix(377,437,morph)
    scl = mix(1,41/77,morph)
    for j in range(10):
        before=482+(j-6)*212
        after=370+j*95
        x=mix(before,after,expand) if j>=6 else after
        cleared=(mix(482,940,expand)-x-83)/12
        opening=step(expand,.08+j*.06,.27+j*.10)*ease(cleared) if j<6 else 1
        x=mix(x,1110+(j-4.5)*43,morph)
        yy=y-29*scl*(1-opening)
        col=GOLD if j==7 else MUTED
        a=alpha*seen*opening
        g.tile(x,yy,77*scl,76*scl,'',col,a,j==7)
        g.text(str(j),x,yy,min(76*scl*.52,34),col,a*(1-morph),weight='medium')
    if graph<=0:
        return
    top=482
    x0,x1=372,1228
    bw=x1-x0
    w = mix(bw/4,bw/10,expand)
    g.rect(x0,top,bw,44,blend(BG,GRID,.46),GRID,1.8,7,graph*alpha)
    xg = mix(x0+bw*.25,x0+bw*.7,expand)
    g.rect(xg,top,w,44,blend(BG,GOLD,.3),GOLD,1.6,5,graph*alpha)
    for n,opacity in ((4,1-expand),(10,expand)):
        for j in range(1,n):
            x=x0+j*bw/n
            g.line(x,top,x,top+44,MUTED,1.4,graph*alpha*opacity*.48)
    qpos=mix(694,1035,expand)
    bez(g,(qpos,y+43),(qpos,455),(xg+w/2,450),(xg+w/2,top),GOLD,1.45,graph*alpha*.71)
    g.text('1 / 4 = 25%',xg+w/2,609,35,GOLD,graph*alpha*(1-step(expand,.08,.52)),font='math')
    g.text('1 / 10 = 10%',xg+w/2,609,35,GOLD,graph*alpha*step(expand,.49,1),font='math')


def _mmlu(g,u):
    # The literal tile first shrinks beside the benchmark; new examples then grow from it.
    first = 1-step(u,.18,.33)
    move=step(u,.02,.14)
    _choice(g,1,1,1-move,first,move)
    names=window(u,.035,.15,.45,.64)
    pro=window(u,.13,.23,.48,.64)
    g.text('MMLU',445,263,41,INK,names,weight='medium')
    g.text('MMLU-Pro',1110,263,41,INK,pro,weight='medium')
    for side,x,n in ((0,445,4),(1,1110,10)):
        a=pro if side else names
        for j in range(n):
            xx=x+(j-(n-1)/2)*(58 if n==4 else 43)
            y=437
            selected=j==(1 if n==4 else 7)
            g.tile(xx,y,41,41,'',GOLD if selected else MUTED,a*(.92 if selected else .65),selected)
    link(g,(664,436),(856,436),move,MUTED,pro*.7,2.2)
    discard=step(u,.514,.695)
    bad=step(u,.29,.42)*(1-discard)
    if bad:
        g.text('3 + ? = 7',800,191-75*discard,46,GOLD,bad,font='math')
        for j,(x,label) in enumerate(((714,'4'),(886,'4.0'))):
            g.tile(x+(j*2-1)*113*discard,552+43*discard,93,72,label,GOLD,bad,True)
        bracket=step(u,.43,.52)*bad
        g.rect(641-113*discard,502+43*discard,318+226*discard,99,None,RED,2.3,12,bracket)
        g.check(971+113*discard,500+43*discard,False,15,bracket)
    reveal=step(u,.586,.718)
    if reveal:
        _worked_example(g,step(u,.69,.97),reveal)


def _worked_example(g,stage,alpha,heading=True):
    """One expression, two physical paths to the same answer."""
    if alpha<=0:
        return
    if heading:
        g.text('3 + 4 × 2',800,191,51,GOLD,alpha,font='math')
    l,r=506,1094
    bez(g,(800,232),(800,294),(l,267),(l,331),MUTED,2,alpha*.68)
    bez(g,(800,232),(800,294),(r,267),(r,331),MUTED,2,alpha*.68)
    g.text('直答',l,497,28,MUTED,alpha*.87)
    g.text('先推理',r,497,28,MUTED,alpha*.87)
    direct=step(stage,.05,.31)
    g.text('11',l,mix(365,395,direct),57,GOLD,alpha*direct,font='math')
    g.line(l-34,428,l+34,428,GOLD,1.6,alpha*direct*.65)

    # Carry the multiplication (not an explanation card) into the working line.
    fall=step(stage,.03,.31)
    collapse=step(stage,.30,.52)
    bring=step(stage,.48,.70)
    final=step(stage,.73,.99)
    if collapse<1:
        xx=mix(853,r,fall)
        yy=mix(201,395,fall)-62*collapse
        g.text('4 × 2',xx,yy,51,GOLD,alpha*fall*(1-collapse),font='math')
        g.line(xx-60*(1-collapse),yy+32,xx+60*(1-collapse),yy+32,
               GOLD,1.7,alpha*fall*(1-collapse)*.77)
    if collapse and final<1:
        xx=mix(r,r+50,bring)
        yy=mix(451,395,collapse)-61*final
        g.text('8',xx,yy,52,GOLD,alpha*collapse*(1-final),font='math')
        g.text('3 +',mix(777,r-27,bring),mix(204,395,bring)-61*final,52,INK,
               alpha*bring*(1-final)*.90,font='math')
    if final:
        g.text('11',r,mix(459,395,final),57,GOLD,alpha*final,font='math')
        g.line(r-34,428,r+34,428,GOLD,1.6,alpha*step(final,.7,1)*.65)


def _search(g,x,y,alpha,query):
    g.rect(x-247,y-33,494,66,blend(BG,MUTED,.066),MUTED,1.65,13,alpha)
    g.circle(x-211,y-3,10,None,GOLD,2.1,alpha)
    g.line(x-204,y+4,x-195,y+13,GOLD,2.1,alpha)
    if query:
        g.text(query,x-173,y,27,INK,alpha,'left',font='math')


def _expert(g,x,y,stroke=MUTED,alpha=1,s=1):
    g.circle(x,y-12*s,13*s,None,stroke,2,alpha)
    g.arc(x,y+22*s,26*s,pi*1.10,pi*1.90,stroke,2,alpha)
    g.line(x-25*s,y+14*s,x-25*s,y+22*s,stroke,2,alpha*.78)
    g.line(x+25*s,y+14*s,x+25*s,y+22*s,stroke,2,alpha*.78)


def _filter_icon(g,x,y,alpha):
    g.poly([(x-46,y-37),(x+46,y-37),(x+11,y+1),(x+11,y+29),(x-11,y+38),(x-11,y+1)],MUTED,2,alpha,True,blend(BG,MUTED,.07),alpha*.85)
    g.line(x-31,y-24,x+31,y-24,MUTED,1.2,alpha*.55)


def _expert_tests(g,u):
    # Search result A is literally the query. Then the item survives without that shortcut.
    early = 1-step(u,.11,.22)
    device = window(u,.13,.24,.53,.66)
    g.text('3 + 4 × 2',800,mix(191,172,step(u,.0,.1)),51,GOLD,early,font='math')
    _worked_example(g,1,1-step(u,0,.14),False)
    xx=mix(800,645,step(u,.19,.40))
    search_a=window(u,.055,.18,.42,.55)
    _search(g,xx,337,search_a,'3 + 4 × 2 = ?' if u<.24 else '…')
    for j,w in enumerate((335,273,205)):
        a = window(u,.14+j*.015,.23+j*.02,.43,.54)
        y=416+51*j
        g.rect(xx-240,y-14,w,27,blend(BG,MUTED,.07),GRID,1,4,a)
        g.line(xx-223,y,xx-242+w*.9,y,GOLD if j==0 and u<.27 else MUTED,2.5,a*.65)
        if j==0:
            g.text('11',xx+153,y,33,GOLD,a*(1-step(u,.20,.28)),font='math')
    if device:
        g.text('GPQA',1167,309,53,INK,device,weight='medium')
        for j,(cx,s) in enumerate(((1111,'物'),(1167,'化'),(1223,'生'))):
            a=step(u,.26+.025*j,.39+.029*j)
            g.tile(cx,433,49,49,s,GOLD,device*a,j==1)
        g.line(956,269,956,563,GRID,2,device*.78)
    stage=window(u,.49,.60,.93,.995)
    arrive=step(u,.925,1)
    if stage:
        g.text('HLE',800,191,52,INK,stage,weight='medium')
        for j in range(3):
            a=step(u,.48+.034*j,.59+.025*j)
            packet(g,410+22*j,405-21*j,89,116,MUTED,stage*a,1)
        a=step(u,.55,.64)
        link(g,(519,387),(627,387),a,MUTED,stage*.75)
        _expert(g,673,387,MUTED,a*stage,1.24)
        link(g,(717,387),(834,387),step(u,.61,.71),MUTED,stage*.75)
        _filter_icon(g,894,387,stage*step(u,.62,.72))
        link(g,(958,382),(1090,382),step(u,.68,.78),MUTED,stage*.75)
        fall=step(u,.73,.84)
        link(g,(894,446),(894,543),fall,MUTED,stage*.68)
        g.check(894,574,False,17,stage*fall)
    # Keep the accepted document onstage. It draws close, then becomes the
    # paper marker beside the next concrete task; the diagram is left behind.
    x=mix(1192,652,arrive)
    y=mix(382,195,arrive)-56*sin(pi*arrive)
    v=step(u,.74,.86)
    _answer_sheet(g,x,y,mix(1,.225,arrive),v,
                  window(u,.87,.94,.96,1))
    _prompt(g,step(arrive,.952,1),195,False)

TEXT_A='今天先取消吧。'
TEXT_B='今天先取消，下周再约？'
SLOT_L=483
SLOT_R=1117


def _answer(g,x,y,color,text,alpha=1,identity=1,extra=0,h=113,w=441):
    """An utterance lives on a narrow ruled slip, not in a UI card."""
    if alpha<=0:
        return
    c=blend(MUTED,color,identity)
    scale=min(35,35*(w-42)/max(g.measure(text,35),1))
    span=g.measure(text,scale)
    x0=x-span/2
    yline=y+29*h/113
    g.text(text,x,y-1,scale,INK,alpha)
    g.line(x0-15,yline,x0+span+15,yline,c,1.55,alpha*(.36+.33*identity))
    if identity>0:
        g.disk(x0-26,y-2,color,10,'',alpha*identity*.95)
    for j,part in enumerate((1.,.81,.9)):
        a=step(extra,.02+j*.17,.33+j*.19)
        yy=yline+23+(j+.45)*25*extra
        g.line(x0,yy,x0+span*part,yy,blend(MUTED,RED,.21),2.7,alpha*a*.68)


def _answer_sheet(g,x,y,s,alpha=1,picture=0):
    if alpha<=0:
        return
    w,h=142*s,174*s
    g.rect(x-w/2,y-h/2,w,h,blend(BG,GOLD,.06),GOLD,1.45,9*s,alpha)
    for j,q in enumerate((.63,.52,.35)):
        xx=x-w/2+16*s
        yy=y-h/2+29*s+j*15*s
        g.line(xx,yy,xx+(w-25*s)*q,yy,GOLD,max(1,2*s),alpha*.52)
    g.rect(x-54*s,y+14*s,108*s,48*s,None,GOLD,1.3,3*s,picture*.76)
    g.poly([(x+dx*s,y+dy*s) for dx,dy in ((-48,52),(-23,33),(3,54),(26,29),(47,54))],
           GOLD,1.6,picture*.88)


def _prompt(g,alpha=1,y=195,with_sheet=True):
    if with_sheet:
        _answer_sheet(g,652,y,.225,alpha)
    g.text('取消今天的预约',822,y,35,GOLD,alpha,font='serif',weight='medium')


def _evidence(g,x,y,line,word,color,alpha):
    whole=g.measure(line,35)
    offset=g.measure(line[:line.index(word)],35)
    span=g.measure(word,35)
    p=x-whole/2+offset
    q=step(alpha,.02,.9)
    g.line(p,y+29,p+span*q,y+29,color,2.95,alpha*.93)
    return p+span/2


def _ballot(g,x,y,alpha=1,color=GOLD):
    if alpha<=0:
        return
    g.poly([(x,y-19),(x+18,y),(x,y+19),(x-18,y)],color,2.05,alpha,True,blend(BG,color,.24),.92)
    g.line(x-5,y,x+5,y,color,2,alpha*.82)


def _eye(g,x,y,alpha=1):
    if alpha<=0:
        return
    bez(g,(x-46,y),(x-22,y-35),(x+22,y-35),(x+46,y),MUTED,2.4,alpha)
    bez(g,(x-46,y),(x-22,y+35),(x+22,y+35),(x+46,y),MUTED,2.4,alpha)
    g.circle(x,y,11,None,GOLD,2.05,alpha)
    g.circle(x,y,3,fill=GOLD,alpha=alpha)


def _judge(g,x,y,alpha=1):
    if alpha<=0:
        return
    g.circle(x,y,45,blend(BG,MUTED,.07),MUTED,2.05,alpha)
    for i in range(5):
        li = pi/2 + 2*pi*i/5
        x1,y1 = x+24*cos(li),y+24*sin(li)
        x2,y2 = x+24*cos(li+4*pi/5),y+24*sin(li+4*pi/5)
        g.line(x1,y1,x2,y2,MUTED,1.1,alpha*.44)
        g.circle(x1,y1,3.9,fill=MUTED,alpha=alpha*.84)
    g.circle(x,y,5,None,GOLD,2,alpha)


def _open_task(g,u):
    _prompt(g)
    a=step(u,.13,.35)
    b=step(u,.27,.44)
    start_x=800
    if a:
        bez(g,(800,227),(800,275),(SLOT_L,267),(SLOT_L,370),MUTED,2,a*.68,a)
        _answer(g,mix(start_x,SLOT_L,a),mix(380,424,a),BLUE,TEXT_A,a,1,w=mix(130,441,a))
    if b:
        bez(g,(800,227),(800,275),(SLOT_R,267),(SLOT_R,370),MUTED,2,b*.68,b)
        _answer(g,mix(start_x,SLOT_R,b),mix(380,424,b),PURPLE,TEXT_B,b,1,w=mix(130,441,b))
    understood=window(u,.35,.51,.76,.94)
    g.check(SLOT_L,559,True,20,understood)
    g.check(SLOT_R,559,True,20,understood)
    # A single-answer key literally opens until the two outputs can coexist.
    single=window(u,.69,.77,.89,.99)
    openness=step(u,.79,.97)
    edge=mix(SLOT_L+232,SLOT_R+232,openness)
    left=SLOT_L-232
    g.poly([(left,461),(left,513),(left+26,513)],GOLD,2.05,single*.68)
    g.poly([(edge,461),(edge,513),(edge-26,513)],GOLD,2.05,single*.68)
    _eye(g,800,573,step(u,.87,1)*.98)


A_POS=(406,360)
B_POS=(1194,360)
C_POS=(800,657)
ARENA=((A_POS,BLUE,'A'),(B_POS,PURPLE,'B'),(C_POS,MUTED,'C'))
EDGE_ORDER=((0,1),(1,2),(2,0))


def _edge(g, i,j, a=1, arrow_amount=0, mode='neutral'):
    p0,col0,_=ARENA[i]
    p1,col1,_=ARENA[j]
    vx,vy=p1[0]-p0[0],p1[1]-p0[1]
    v=(vx*vx+vy*vy)**.5
    x0,y0=p0[0]+vx*66/v,p0[1]+vy*66/v
    x1,y1=p1[0]-vx*66/v,p1[1]-vy*66/v
    g.line(x0,y0,x1,y1,MUTED,2.25,a*.38)
    if arrow_amount:
        x= mix(x1,x0,arrow_amount)
        y= mix(y1,y0,arrow_amount)
        g.circle(x,y,7.2,fill=GOLD,alpha=a*.96)
        if mode=='direction':
            g.arrow(mix(x1,x0,.42),mix(y1,y0,.42),mix(x1,x0,.62),mix(y1,y0,.62),GOLD,2.15,a*arrow_amount,10)


def _arena(g,u):
    cards=1-step(u,.59,.83)
    anonymous=1-step(u,.06,.23)
    _prompt(g,1-step(u,.57,.78))
    p=1-step(u,0,.14)
    for x in (SLOT_L,SLOT_R):
        bez(g,(800,227),(800,275),(x,267),(x,370),MUTED,2,p*.68)
    shifted=step(u,.64,.86)
    _answer(g,mix(SLOT_L,A_POS[0],shifted),mix(424,A_POS[1],shifted),BLUE,TEXT_A,cards,anonymous,w=mix(441,172,shifted))
    _answer(g,mix(SLOT_R,B_POS[0],shifted),mix(424,B_POS[1],shifted),PURPLE,TEXT_B,cards,anonymous,w=mix(441,172,shifted))
    _eye(g,800,573,cards)
    for k,target in enumerate((SLOT_L,800,SLOT_R)):
        phase = step(u,.25+k*.094,.38+k*.095)
        opacity=window(u,.22+k*.092,.26+k*.094,.47+k*.055,.56+k*.071)
        _ballot(g,mix(800,target,phase),mix(573,518,phase),opacity)
        if k==1:
            g.text('平',800,508,26,MUTED,opacity*.8)
    chart=step(u,.61,.79)
    for k,(i,j) in enumerate(EDGE_ORDER):
        a=step(u,.64+k*.034,.83+k*.04)
        _edge(g,i,j,chart*a,a)
    for k,(p,col,label) in enumerate(ARENA):
        a=chart if k<2 else step(u,.64,.86)
        start=(SLOT_L,424) if k==0 else ((SLOT_R,424) if k==1 else (800,577))
        q=(mix(start[0],p[0],shifted),mix(start[1],p[1],shifted))
        g.disk(*q,col,mix(30,52,a),label,a)


def _rating(g,u):
    squeeze=step(u,.39,.69)
    collapse=step(u,.82,.975)
    for k,(i,j) in enumerate(EDGE_ORDER):
        a=step(u,.052+k*.092,.17+k*.075)
        _edge(g,i,j,1-squeeze,a,'direction')
    for k,(p,col,label) in enumerate(ARENA):
        q=(mix(p[0],800,squeeze),mix(p[1],492+(k-1)*49,squeeze))
        g.disk(*q,col,mix(52,17,squeeze),label,1-collapse)
    if squeeze:
        x0,x1,y=411,1189,492
        span=389*squeeze
        yy=mix(525,y,squeeze)
        g.line(800-span,yy,800+span,yy,MUTED,1.6,squeeze*(1-collapse)*.69)
        for k in (-3,-2,-1,0,1,2,3):
            x=800+span*k/3
            a=squeeze*(1-collapse)
            g.line(x,yy-7,x,yy+7,GOLD if k==0 else MUTED,2.3 if k==0 else 1.4,a*.82)
        g.line(800,469,800,520,GOLD,2.25,squeeze*(1-collapse)*.8)
        g.text('½',800,343,48,GOLD,window(u,.56,.69,.80,.97),font='math')
        halo(g,800,492,29,GOLD,window(u,.59,.73,.78,.94)*.56)
    transfer=step(u,.87,1)
    if transfer:
        _prompt(g,transfer,mix(343,195,transfer))
        _answer(g,mix(800,SLOT_L,transfer),424,BLUE,TEXT_A,transfer*.95,0,w=mix(190,441,transfer))
        _answer(g,mix(800,SLOT_R,transfer),424,PURPLE,TEXT_B,transfer*.95,0,w=mix(190,441,transfer))
        _eye(g,800,573,transfer)


def _auto_judge(g,u):
    _prompt(g)
    a=step(u,.18,.37)
    _eye(g,800,573,1-a)
    _judge(g,800,mix(573,339,a),a)
    _answer(g,SLOT_L,424,BLUE,TEXT_A,1,0)
    pretend = window(u,.34,.49,.78,.93)
    _answer(g,SLOT_R,424,PURPLE,TEXT_B,1-pretend,0)
    _answer(g,SLOT_R,424,PURPLE,'已帮您改到明天。',pretend,0)
    good=window(u,.35,.52,.82,.96)
    red=pretend*window(u,.51,.63,.84,.96)
    a=_evidence(g,SLOT_L,424,TEXT_A,'取消',GREEN,good)
    b=_evidence(g,SLOT_R,424,'已帮您改到明天。','已帮您改到明天',RED,red)
    g.check(a,501,True,18,good)
    g.check(b,501,False,18,red)
    check=window(u,.63,.75,.84,.95)
    bez(g,(772,379),(754,482),(640,477),(589,525),GOLD,1.65,check*.72,check)
    _ballot(g,589,525,check)


def _swap(g,u):
    phase=step(u,.20,.365)
    focus=sin(pi*phase)
    _prompt(g,1,195-23*focus)
    _judge(g,800,339,1-.85*focus)
    ax = mix(SLOT_L,SLOT_R,phase)
    bx = mix(SLOT_R,SLOT_L,phase)
    dy = sin(pi*phase)
    ay = 424-149*dy
    by = 424+116*dy
    names=step(u,.13,.21)
    w=mix(441,344,dy)
    if dy>0:
        bez(g,(SLOT_L,424),(659,270),(947,270),(SLOT_R,424),BLUE,1.65,.57*dy)
        bez(g,(SLOT_R,424),(946,613),(660,613),(SLOT_L,424),PURPLE,1.65,.57*dy)
    id_alpha=.77*names
    _answer(g,bx,by,PURPLE,TEXT_B,1,id_alpha,h=mix(113,88,dy),w=w)
    _answer(g,ax,ay,BLUE,TEXT_A,1,id_alpha,h=mix(113,88,dy),w=w)
    v1=window(u,.035,.12,.17,.25)
    v2=step(u,.34,.43)
    label_a=1-step(u,.71,.84)
    for hit, label in ((v1,'①'),(v2,'②')):
        x=SLOT_L
        _ballot(g,x,mix(500,554,hit),hit*.82)
        g.text(label,x,608,31,MUTED,hit*label_a,font='math')
    # Both votes arrive at the same physical slot. Write their identities
    # into two records, then connect the conflicting results.
    pin=window(u,.46,.56,.88,.98)
    if pin:
        height=106*step(u,.49,.65)
        g.line(SLOT_L,554,SLOT_L,554+height,RED,1.45,pin*.49,dash=[5,8])
        for j,(c,cap) in enumerate(((BLUE,'A'),(PURPLE,'B'))):
            skim=step(u,.58+j*.105,.72+j*.128)
            a=step(u,.57+j*.098,.61+j*.107)*(1-step(u,.947,1))
            if not a:
                continue
            xx=mix(SLOT_L,703+190*j,skim)
            yy=mix(655,675,skim)-(24+28*j)*sin(pi*skim)
            g.disk(xx,yy,c,mix(12,24,skim),cap if skim>.62 else '',a)
            g.text(('①','②')[j],xx-43,yy,28,MUTED,a*skim,font='math')
        compare=step(u,.806,.925)
        g.line(756,675,mix(756,842,compare),675,RED,2.1,pin*compare*.91,dash=[5,8])


def _verbosity(g,u):
    _prompt(g,1-step(u,.91,1))
    _judge(g,800,339,1-step(u,.91,.99))
    extension=step(u,.105,.26)
    dissolve=step(u,.91,1)
    length_color=blend(MUTED,RED,.2)
    _answer(g,mix(SLOT_L,383,dissolve),mix(424,465,dissolve),PURPLE,TEXT_B,1-dissolve,.77)
    _answer(g,mix(SLOT_R,1193,dissolve*.5),mix(424,340,dissolve),BLUE,TEXT_A,1-dissolve,.77,extension)
    move=step(u,.265,.39)
    jump=sin(pi*move)
    _ballot(g,mix(SLOT_L,SLOT_R,move),mix(554,625,move)+47*jump,(1-dissolve)*(.82+.18*move))
    if extension>0:
        a=extension*(1-dissolve)*.85
        l=81*extension
        g.poly([(1354,480),(1368,480),(1368,480+l),(1354,480+l)],length_color,1.7,a)
    cut=window(u,.71,.80,.94,.99)
    if cut:
        sx,sy=1344,520
        for q in (-1,1):
            g.circle(sx+q*10,sy+20,7,None,MUTED,1.9,cut)
            g.line(sx+q*4,sy+14,sx-q*17,sy-18,MUTED,2.25,cut)
        g.circle(sx,sy+6,2.4,fill=MUTED,alpha=cut)
        g.line(1313,482,1375,554,RED,1.6,cut*.78)
    # This is the training signal returning to the same model, followed by
    # one more redundant line; the proposition on the slip never changes.
    feed=window(u,.405,.46,.59,.71)
    up=step(u,.423,.565)
    if feed:
        bez(g,(SLOT_R+72,618),(1370,596),(1371,438),(SLOT_R+123,414),
            BLUE,2.05,feed*.68,up)
        if .02<up<1:
            a,b=up,1-up
            x=b**3*(SLOT_R+72)+3*b*b*a*1370+3*b*a*a*1371+a**3*(SLOT_R+123)
            y=b**3*618+3*b*b*a*596+3*b*a*a*438+a**3*414
            g.circle(x,y,5,fill=BLUE,alpha=feed*.87)
    duplicate=window(u,.525,.64,.89,.99)
    if duplicate:
        g.line(SLOT_R-118,559,SLOT_R+111*duplicate,559,
               blend(MUTED,RED,.38),2.75,duplicate*.69)
    points=step(u,.91,1)
    _plot(g,points,appear=0,activate=0,average=0,ax=.08,ay=0)


def _plot(g,alpha=1,appear=1,activate=1,average=1,ax=1,ay=1):
    if alpha<=0:
        return
    x0,x1,zero=388,1212,800
    bottom,top=638,227
    yr=lambda p: mix(bottom,top,p)
    curve=lambda x: 1/(1+exp(-2.35*(x-.04)))
    g.arrow(x0,bottom,mix(x0,x1,ax),bottom,MUTED,1.9,alpha*.86)
    g.arrow(x0,bottom,x0,mix(bottom,top,ay),MUTED,1.9,alpha*ay*.86)
    g.text('长度差',x1,668,29,MUTED,alpha*step(ax,.74,1),'right')
    g.text('胜率',x0,193,29,MUTED,alpha*step(ay,.78,1),'left')
    for j,p in enumerate((0,.5,1)):
        y=yr(p)
        a=step(ay,max(0,p-.15), min(1,p+.07))
        g.line(x0-8,y,x0+2,y,MUTED,1.55,alpha*a*.59)
        g.text(f'{int(100*p)}%',x0-24,y,24,MUTED,alpha*a*.82,'right',font='math')
        if j>0:
            g.line(x0+2,y,x1-2,y,GRID,1.1,alpha*a*.68)
    g.line(zero,227,zero,bottom,GOLD,1.5,alpha*step(ax,.55,1)*ay*(.21+.35*activate),dash=[7,8])
    g.text('0',zero,667,25,GOLD,alpha*step(ax,.49,.79)*(.62+.38*activate),font='math')
    for k,(j,r) in enumerate(((-.81,.16),(-.68,.12),(-.55,.27),(-.38,.31),(-.22,.32),(-.10,.43),(.13,.60),(.26,.61),(.40,.68),(.56,.73),(.69,.81),(.80,.86),(.91,.87),(.95,.94))):
        a=step(appear,.031*k,.38+.038*k)
        g.circle(zero+386*j,yr(r),5.4,fill=MUTED,alpha=alpha*a*.69)
    line=step(appear,.38,1)
    if line:
        pts=[]
        for k in range(49):
            d=-1+2*k*line/48
            pts.append((zero+386*d,yr(curve(d))))
        g.poly(pts,MUTED,2.6,alpha*line*.92)
    if activate:
        q=mix(.64,0,activate)
        x,y=zero+386*q,yr(curve(q))
        g.line(x,bottom,x,y,RED,1.8,alpha*(1-activate)*.79,dash=[7,7])
        g.circle(x,y,8.1,fill=GOLD,alpha=alpha*activate)
        g.circle(x,y,8.1,fill=RED,alpha=alpha*(1-activate))
        g.line(x0,y,x,y,GOLD,1.3,alpha*activate*.48,dash=[6,7])
    if average:
        for j,d in enumerate((-44,0,51)):
            a=step(average,.14*j,.58+.11*j)
            y=yr(curve(0))+d*(1-step(average,.57,.98))
            g.circle(zero,y,10+5*(j==2),None,GOLD,1.6,alpha*a*(1-.5*step(average,.68,.99)))
        halo(g,zero,yr(curve(0)),24,GOLD,alpha*step(average,.68,1)*.54)


def _length_curve(g,u):
    ax=mix(.08,1,step(u,.01,.165))
    ay=step(u,.14,.288)
    _plot(g,1,step(u,.255,.61),step(u,.65,.86),step(u,.88,.99),ax,ay)
    amount=window(u,.017,.063,.172,.25)
    if amount:
        j=step(u,.033,.121)
        bx0,bx1=617,841
        y0,y1=411,471
        longer=mix(bx1,986,j)
        g.line(bx0,y0,bx1,y0,PURPLE,3.2,amount*.86)
        g.line(bx0,y1,longer,y1,BLUE,3.2,amount*.86)
        if j:
            g.line(bx1,y1+27,longer,y1+27,GOLD,1.6,amount*j)
            g.line(bx1,y1+21,bx1,y1+33,GOLD,1.6,amount*j)
            g.line(longer,y1+21,longer,y1+33,GOLD,1.6,amount*j)
            g.line(bx1,y0,bx1,y1+21,MUTED,1.35,amount*j*.42,dash=[5,7])
    pulse=window(u,.50,.56,.69,.78)
    if pulse:
        x,y=1047,yr_for(.805)
        g.circle(x,y,12,None,RED,2,pulse*.65)


def yr_for(p):
    return mix(638,227,p)


def _length_limit(g,u):
    enter = step(u,0,.13)
    if enter<1:
        _plot(g,1-enter)
    calendar=step(u,.89,1)
    _prompt(g,enter*(1-calendar))
    _answer(g,800,mix(381,322,step(u,.08,.22)),BLUE,TEXT_A,enter*(1-calendar),.77,w=486)
    a=window(u,.105,.235,.84,.98)
    if a:
        bez(g,(800,379),(800,452),(505,400),(505,498),MUTED,1.8,a*.78,a)
        bez(g,(800,379),(800,452),(1095,400),(1095,498),MUTED,1.8,a*.78,a)
        for j,w in enumerate((150,132)):
            yy=544+j*22
            g.line(505-w/2,yy,505+w/2,yy,RED,2.55,a*(.79-.30*j))
        g.text('周四 14:00',1095,553,37,GOLD,a,font='serif')
        g.line(1016,577,1174,577,GOLD,1.6,a*.64)
    check=window(u,.49,.59,.87,.98)
    _eye(g,800,664,check)
    for j,x in enumerate((505,1095)):
        q=window(u,.55+j*.08,.63+j*.08,.76+j*.04,.83+j*.05)
        g.line(800,642,mix(800,x,q),mix(642,591,q),MUTED,1.5,q*.57,dash=[5,8])
    if calendar:
        _calendar(g,800,428,mix(155,255,calendar),calendar,1)


def _calendar(g,x,y,w,a=1,called=1):
    h=w*.82
    g.rect(x-w/2,y-h/2,w,h,blend(BG,MUTED,.07),MUTED,1.65,12,a)
    cap=y-h/2+w*.17
    g.line(x-w/2,cap,x+w/2,cap,MUTED,1.1,a*.74)
    for ang in (.2,.8):
        gx=x-w/2+ang*w
        g.line(gx,y-h/2-11,gx,y-h/2+16,MUTED,2.45,a)
    boxw=(w-30)/5
    boxh=(h-w*.17-21)/4
    for j in range(5):
        gx=x-w/2+15+boxw*(j+.5)
        for k in range(4):
            gy=cap+10+boxh*(k+.5)
            if j==2 and k==1:
                g.tile(gx,gy,boxw-5,boxh-5,'',GOLD,a*called,True)
            else:
                g.rect(gx-boxw/2+2,gy-boxh/2+2,boxw-4,boxh-4,None,GRID,1,4,a*.82)


def _calendar_end(g,u):
    mark=step(u,.26,.53)
    gather=step(u,.77,.94)
    w=mix(mix(255,402,mark),170,gather)
    y=mix(mix(428,457,mark),420,gather)
    _calendar(g,800,y,w,1-gather,0)
    inner_w=(w-30)/5-5
    inner_h=(w*.65-21)/4-5
    cap=y-w*.24
    cell_y=cap+10+((w*.65-21)/4)*1.5
    anchor_y=mix(cell_y,420,gather)
    g.tile(800,anchor_y,mix(inner_w,68,gather),mix(inner_h,62,gather),'',GOLD,1,True)
    text=window(u,.04,.18,.40,.62)
    if text:
        leftx=mix(800,497,step(u,.11,.35))
        _answer(g,leftx,256,BLUE,TEXT_A,text,.76,w=395)
        bez(g,(leftx+192,271),(708,288),(744,299),(770,315),MUTED,1.25,text*.63,text)
    halo(g,800,anchor_y,29+17*mark,GOLD,mark*(1-gather)*.66)
    if gather:
        g.disk(mix(530-107,530,gather),420,BLUE,mix(30,53,gather),'A',gather)
        g.disk(mix(1070+107,1070,gather),420,PURPLE,mix(30,53,gather),'B',gather)


HOLDS=tuple(b.get('hold',.45) for b in json.loads(Path(__file__).with_suffix('.json').read_text(encoding='utf-8')))
# These are perceptual landmarks, not subtitle lines. Retiming preserves the
# same drawing, while the card lands before the second vote and the fitted dot
# hits the center as the lecturer says what to hold fixed.
CUES={
    1: (('答案一比', .15, .227),
        ('两排勾这才错开', .19, .317),
        ('原来那张卷子', .25, .409),
        ('这就叫基准饱和', .52, .529),
        ('全班都拿零分', .67, .669),
        ('好题得落在', .80, .784)),
    9: (('挑了左边', .058, .074),
        ('只交换顺序', .262, .252),
        ('它又挑左边', .332, .367),
        ('这次赢了', .495, .458)),
    11: (('横着走', .052, .041),
         ('纵着走', .179, .152),
         ('用回归估计', .420, .450),
         ('往中线看', .691, .651),
         ('模型相对基线', .810, .862),
         ('最后在题目上平均', .931, .891)),
}


def speech_phase(g,i,t,duration):
    spoke=max(duration-HOLDS[i],duration*.68)
    u=clamp(t/spoke)
    if i not in CUES or u>=1:
        return u
    knots=[(0.,0.)]
    for phrase, expect, phase in CUES[i]:
        when=clamp(g.cue(phrase,expect*spoke/duration)*duration/spoke)
        if when>knots[-1][0]+.024 and when<.98:
            knots.append((when,phase))
    knots.append((1.,1.))
    for (x,a),(y,b) in zip(knots,knots[1:]):
        if u<=y:
            return mix(a,b,(u-x)/(y-x))
    return 1.


def draw(g,i,t,duration):
    u=speech_phase(g,i,t,duration)
    if i<2:
        _exam(g,i,u)
    elif i==2:
        _choice(g,step(u,.39,.67),step(u,.04,.18),step(u,.14,.32))
    else:
        (_mmlu,_expert_tests,_open_task,_arena,_rating,_auto_judge,_swap,
         _verbosity,_length_curve,_length_limit,_calendar_end)[i-3](g,u)
