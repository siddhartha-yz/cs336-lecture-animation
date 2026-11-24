"""An up/down test, then the three-dimensional object the test leaves out."""
from cut_common import *

O=(-4.45,-1.57,0.)
LX=6.46
LY=3.08
LZ=3.34
A0=(-4.45,-1.84,0.)
AX=(-4.45,2.37,0.)
XR=(4.56,-1.84,0.)
GOOD=(82,80,78)
OTHER=(82,28,20)
RACE=(98,15,10)
TI=(0,.14,.31,.48,.61,.74,.87,1)
GOLD_SEQ=(35,40,46,56,63,69,76,82)
NEW_SEQ=(39,46,56,66,65,60,53,46)

def T(g,t,d,name,when):
    if isinstance(name,int):return g.part(name,when/d)*d
    return g.cue(name,when/d)*d

def ramp(v,a,b):
    return step(v,a,max(b,a+.035))

def sl(t,a,b,span=.8):
    return ramp(t,a,a+span)*(1-ramp(t,b,b+span))

def fmt(n):return str(round(n))

def roto(g,t,yaw=0,pitch=0,zoom=1,target=(0,0,0),z=13):
    return World(g,yaw,pitch,zoom,target,distance=z)

def led(w,s,p,c=WHITE,a=1,sz=25,align='left'):
    w.text(str(s),p,sz,c,a,align=align,font=SERIF)

def demo_badge(w,s,al=1,x=-4.44,y=2.66):
    if al<=.002:return
    led(w,s,(x,y,.044),AXIS,al,21)

def smoothed(seq):
    def cubic(a,b,c,d,u):
        return .5*((2*b)+(-a+c)*u+(2*a-5*b+4*c-d)*u*u+(-a+3*b-3*c+d)*u*u*u)
    rs=[]
    for j in range(len(TI)-1):
        for i in range(12):
            r=i/12
            x=mix(TI[j],TI[j+1],r)
            y=cubic(seq[max(0,j-1)],seq[j],seq[j+1],seq[min(len(TI)-1,j+2)],r)
            rs.append((mix(A0[0],XR[0]-.72,x),A0[1]+(AX[1]-A0[1])*y/100,.10))
    rs.append((XR[0]-.72,A0[1]+(AX[1]-A0[1])*seq[-1]/100,.10))
    return tuple(rs)

BENCH=smoothed(GOLD_SEQ)
NEW=smoothed(NEW_SEQ)
KINK=36
def draw_curve(w,points,idx,c,a=1,from_idx=0):
    if a<.004 or idx<=from_idx:return
    nx=int(idx)
    b=points[:nx+1]
    if nx<len(points)-1 and idx>nx:
        b=(*b,vlerp(points[nx],points[nx+1],idx-nx))
    b=b[from_idx:]
    if len(b)<2:return
    lit_path(w,b,c,3.13,a)
    pin(w,b[-1],c,.056,a,8)
    return b[-1]

def old_axis(w,alpha=1):
    w.path((A0,XR),AXIS,1.76,alpha*.92,arrow=True)
    w.path((A0,AX),AXIS,1.76,alpha*.92,arrow=True)
    for v in (0,25,50,75,100):
        y=mix(A0[1],AX[1],v/100)
        w.segment((A0[0]-.065,y,0),(A0[0]+.07,y,0),AXIS,1.26,alpha)
        if v%50==0:led(w,v,(A0[0]-.12,y,.015),AXIS,alpha,20,'right')
    led(w,'训练更新',(XR[0],XR[1]-.33,.02),MILD,alpha,22,'right')

def x_ruler(w,al=1,labels=1,markpos=None,y=None,lx=LX):
    o=O if y is None else (O[0],y,O[2])
    w.path((o,add(o,(lx+.15,0,0))),GOLD,2.28,al,arrow=True)
    for j in range(6):
        p=add(o,(j*lx/5,0,0))
        w.segment(p,add(p,(0,-.112,0)),GOLD,1.46,al)
        led(w,j*20,add(p,(0,-.30,.045)),MILD,al*labels,19,'center')
    if labels>.002:
        led(w,'基准标尺',(o[0]+lx*.46,o[1]-.66,o[2]+.05),GOLD,al*labels,25,'center')
    if markpos is not None:
        q=add(o,(lx*markpos/100,0,.047))
        pin(w,q,GOLD,.064,al,10)
        led(w,fmt(markpos),add(q,(0,score_label_y(markpos),.034)),GOLD,al*labels,30,'center')

def score_label_y(value):
    # Near the end tick, the score gets a dedicated lower text lane.
    return -.47-.23*ramp(value,92,98)

def xpose(g):
    w=World(g)
    x_ruler(w,markpos=82)
    return w

def blink(t,start,dur=1.4):
    if not start<=t<=start+dur:return 0
    return ramp(t,start,start+.17)*(1-ramp(t,start+.36,start+dur))

TRIAL_HEIGHTS=((.62,.41,.74,.55,.91),(.37,.64,.43,.79,.96))
TRIAL_BASIS=(352,475)

def trial_beat(t,anchor,i,j):
    # One retained update, with its unchecked out-of-domain result following.
    release=anchor+.43+i*.57+j*.19
    raise_bar=ramp(t,release-.22,release+.25)
    commit=ramp(t,release+.10,release+.61)
    return raise_bar,commit,release+.27

def panel_sweep(g,t,anchor,x,xp,yp,i,j,col,alpha):
    _,_,hit=trial_beat(t,anchor,i,j)
    q=(t-hit)/.57
    if not 0<q<1:return
    # The short return impulse couples the bar and the plotted endpoint.
    u=1-(1-q)**2
    base=TRIAL_BASIS[j]
    h=19+TRIAL_HEIGHTS[j][i]*34
    sx=x+43+64*i; sy=base+(-h if j==0 else h)
    xend=x-46; yend=yp
    vx=mix(sx,xp,u);vy=mix(sy,yend,u)+26*math.sin(math.pi*u)*(-1 if j==0 else 1)
    vis=alpha*math.sin(math.pi*q)**.57
    g.line(xend,yp,xp,yp,col,1.5,vis*.62)
    g.circle(vx,vy,5.1+1.6*math.sin(math.pi*q),fill=col,alpha=vis)

def update_trials(g,t,anchor,out,steering,endpoints,labels=1):
    dr=step(t,anchor,anchor+.40)*out
    if dr<.002:return
    x=1110
    g.text('训练更新',x,181,35,WHITE,dr*labels,align='left',font=SERIF)
    g.line(x,210,1455,210,EDGE,1.25,dr)
    for j,(base,v,col,label,header) in enumerate(zip(TRIAL_BASIS,(1,-1),(GOLD,CORAL),('测评分数 Δ','未见题目 Δ'),(239,424))):
        al=ramp(t,anchor+.08+j*.23,anchor+.54+j*.26)*out
        g.text(label,x,header,26,col,al*labels,align='left',font=SERIF)
        g.line(x,base,1455,base,EDGE,1.3,al)
        for i,n in enumerate(TRIAL_HEIGHTS[j]):
            xx=x+43+64*i
            z,_,moment=trial_beat(t,anchor,i,j)
            h=(19+n*34)*z
            bar_y=base-(h if v==1 else 0)
            g.rect(xx-12,bar_y,24,h,fill=col,alpha=z*al)
            q=blink(t,moment,.44)*al
            if j==0:
                g.line(xx,base-2-h,xx,base-20-h,WHITE,1.55,z*al*.60)
                g.circle(xx,base-20-h,6.6+2.5*q,fill=GOLD,alpha=min(1,.28*z*al+.82*q))
                hit=blink(t,steering+.075+i*.31,1.13)*out
                if hit>.002:
                    g.circle(xx,base-20-h,8+6*(1-hit),stroke=GOLD,width=2.35,alpha=hit)
            if q>0:
                yy=base-v*h
                g.line(xx+18,yy,xx+27,yy,col,1.6,q)
            if endpoints[j]:
                panel_sweep(g,t,anchor,x,*endpoints[j],i,j,col,al)
    gate=ramp(t,anchor+.44,anchor+1.03)*out
    g.text('保留',1447,239,27,GOLD,gate*labels,align='right',font=SERIF)
    g.line(x+30,TRIAL_BASIS[0]-77,x+303,TRIAL_BASIS[0]-77,GOLD,2.0,gate*.64)
    z=ramp(t,anchor+1.96,anchor+3.30)*out
    g.text('不作筛选',1447,558,26,CORAL,z*labels,align='right',font=SERIF)

def extract_score(g,t,w,u,timing,ruler):
    """Keep exactly one scalar: erase the training-time dimension, not its value."""
    # Pull the gate back behind its own leftmost edge.
    fold=ramp(u,.075,.52)
    if fold<1:
        ctx=g.c
        ctx.save()
        right=mix(1490,1107,fold)
        ctx.rectangle(1098,0,right-1098,900)
        ctx.clip()
        update_trials(g,t,timing,1,ruler-.06,(None,None),1-ramp(u,.008,.105))
        ctx.restore()
        if .025<fold<.975:
            g.line(right,210,right,570,EDGE,1.35,math.sin(math.pi*fold)*.7)

    # The unmeasured answer trace runs backwards into its origin.
    cut=ramp(u,.00,.61)
    n=(len(NEW)-1)*(1-cut)
    last=draw_curve(w,NEW,n,CYAN,1) if n<=KINK else draw_curve(w,NEW,KINK,CYAN,1)
    if n>KINK:last=draw_curve(w,NEW,n,CORAL,1,from_idx=KINK) or last
    if last and cut<.18:
        x,y,z=last
        led(w,'未见题目',(x-.13,y-.33,z+.07),CORAL,1-ramp(cut,.01,.18),28,'right')
    # The skeletal axes retract at the same time; a single line survives
    # the operation. The graphic is drawn, not composited as two fading scenes.
    chop=ramp(u,.065,.66)
    a,x,y=w.pos(A0),w.pos(XR),w.pos(AX)
    if chop<1:
        qx=(mix(x[0],a[0],chop), mix(x[1],a[1],chop))
        qy=(mix(y[0],a[0],chop), mix(y[1],a[1],chop))
        g.arrow(*a,*qx,AXIS,1.76,.92,11)
        g.arrow(*a,*qy,AXIS,1.76,.92,11)
        for value in (0,25,50,75,100):
            at=value/100
            if at>(1-chop):continue
            pt=(A0[0],mix(A0[1],AX[1],at),.0)
            w.segment(add(pt,(-.065,0,0)),add(pt,(.07,0,0)),AXIS,1.26,1)
            if value%50==0:led(w,value,add(pt,(-.12,0,.015)),AXIS,1,20,'right')
        led(w,'训练更新',add(XR,(0,-.33,.02)),MILD,1-ramp(chop,0,.15),22,'right')
    demo_badge(w,'示意数据',1-ramp(chop,.13,.47))
    old_tip=BENCH[-1]
    guide=1-ramp(u,.02,.37)
    if guide:
        w.path((old_tip,(A0[0],old_tip[1],.09)),GOLD,1.84,.84,dash=[5,5],progress=guide)
    w.draw()

    k=ramp(u,.19,.86)
    tgt=World(g)
    source=[(w.pos(p),p[0]) for p in BENCH]
    # The end of the surviving path is still the 82 point, not the 100 tick.
    left=BENCH[0][0]; extent=BENCH[-1][0]-left
    points=[]
    for (x,y),qx in source:
        target=tgt.pos(add(O,(LX*.82*(qx-left)/extent,0,0)))
        points.append((mix(x,target[0],k),mix(y,target[1],k)))
    tip=points[-1]
    g.poly(points,GOLD,mix(3.13,2.28,k),1)
    g.circle(*tip,mix(6.8,8.25,k),fill=GOLD)
    if k<.37:
        x,y,z=old_tip
        led(w,'基准分数',(x-.13,y+.31,z+.07),GOLD,1-ramp(k,.02,.37),28,'right')
        w.draw()
    # Once flat, the tip stays at 82 and an unmarked continuation draws to 100.
    rule=ramp(u,.71,.96)
    if rule:
        endpoint=tgt.pos(add(O,(LX+.15,0,0)))
        mid=(mix(tip[0],endpoint[0],rule),mix(tip[1],endpoint[1],rule))
        g.arrow(*tip,*mid,GOLD,2.28,1,10)
    for i in range(6):
        reach=.82+(1+.15/LX-.82)*rule
        tick=ramp(u,.50+i*.046,.63+i*.051)*ramp(k,.89,.99)
        if i==5:tick*=ramp(reach,.993,1.014)
        if tick<=0:continue
        q=add(O,(i*LX/5,0,0))
        tgt.segment(q,add(q,(0,-.112*tick,0)),GOLD,1.46,tick)
        led(tgt,i*20,add(q,(0,-.30,.045)),MILD,tick,19,'center')
    led(tgt,'基准标尺',add(O,(LX*.46,-.66,.05)),GOLD,ramp(u,.72,.96),25,'center')
    pos=tgt.pos(add(O,(LX*.82,-.47,.081)))
    g.text('82',mix(tip[0]+22,pos[0],ramp(u,.70,.95)),mix(tip[1]-17,pos[1],ramp(u,.70,.95)),
           30,GOLD,ramp(u,.31,.45),font=SERIF)
    tgt.draw()

def first(g,t,d):
    exam=T(g,t,d,"final exam",4.4)
    debate=T(g,t,d,"But evaluation",8.9)
    drive=T(g,t,d,"optimization target",12.8)
    ruler=T(g,t,d,"Whatever ruler",16.0)
    end=ramp(t,max(ruler+.45,d-3.4),d-.19)
    if end>=.99998:
        xpose(g).draw();return
    w=World(g,pitch=-.022*math.sin(t*.37),zoom=.91,center=(635,381))
    if end>.002:
        extract_score(g,t,w,end,debate-.12,ruler-.06)
        return
    bright=1
    old_axis(w,bright)
    apex=T(g,t,d,"who won",7.0)
    turn_at=min(exam+.36,T(g,t,d,"opening hook",exam+.58)-.22)
    chart_tip=len(BENCH)-1
    cold=KINK*ramp(t,.30,turn_at)+(59-KINK)*ramp(t,turn_at,min(apex+.73,debate+.03))
    timing=debate-.12
    pidx=cold+(chart_tip-59)*sum(trial_beat(t,timing,i,0)[1] for i in range(5))/5
    qidx=cold+(chart_tip-59)*sum(trial_beat(t,timing,i,1)[1] for i in range(5))/5
    p=draw_curve(w,BENCH,pidx,GOLD,bright)
    q=draw_curve(w,NEW,min(qidx,KINK),CYAN,bright)
    q=draw_curve(w,NEW,qidx,CORAL,bright,from_idx=KINK) or q
    if p and q:
        focus=ramp(t,turn_at,turn_at+1.13)
        for j,(pt,txt,col) in enumerate(((p,'基准分数',GOLD),(q,'未见题目',blend(CYAN,CORAL,focus)))):
            x,y,z=pt
            edge=ramp(x,-2.85,-2.31)
            side='right' if edge>=.40 else 'left'
            offset=.13 if side=='left' else -.13
            if t<timing-.14:
                split=1-ramp(t,timing-1.03,timing-.14)
                offset=mix(offset,1.04 if j==0 else -.18,split)
                side='right'
            above=(j==0)
            # The two Chinese labels stay outside the interval between
            # the end points, including when the curves cross.
            high=max(p[1],q[1]);low=min(p[1],q[1])
            label=(x+offset,high+.31 if above else low-.33,z+.07)
            br=bright*ramp(t,.5+j*.75,1.2+j*.75)
            w.segment(pt,(x+offset*.61,label[1]+(-.1 if above else .105),z+.02),col,1.65,br)
            led(w,txt,label,col,br,28,side)
        for j,pt in enumerate((p,q)):
            b=blink(t,apex-.15+.20*j,1.55)*bright
            if b>.002:
                x,y=w.pos(pt);g.circle(x,y,12+13*(1-b),stroke=GOLD if j==0 else CORAL,width=2.15,alpha=b)
    votes=ramp(t,drive-.24,drive+.84)*bright
    if p and votes:
        high=(A0[0],p[1],.09)
        w.path((p,high),GOLD,1.84,votes,dash=[5,5],progress=ramp(t,drive-.23,drive+.63))
        k=blink(t,drive,.98)
        pin(w,high,GOLD,.052+.027*k,votes)
    demo_badge(w,'示意数据',bright*ramp(t,0,.75))
    w.draw()
    update_trials(g,t,timing,1,ruler-.06,
                  (w.pos(p) if p else None,w.pos(q) if q else None))
    feed=ramp(t,drive+.04,ruler+.43)
    if p and 0<feed<1:
        px,py=w.pos(p)
        # The selected score sends the only visible control signal to the update gate.
        # Both dashed traces are still measurements; only yellow feeds back to training.
        g.line(px+9,py,1088,py,GOLD,1.8,.74)
        g.line(1088,py,1088,352,GOLD,1.8,.74)
        g.line(1088,352,1140,352,GOLD,1.8,.74)
        hops=((px+9,py),(1088,py),(1088,352),(1140,352))
        for j in range(3):
            f=clamp(feed*3-j)
            if .001<f<.999:
                x=mix(hops[j][0],hops[j+1][0],f)
                y=mix(hops[j][1],hops[j+1][1],f)
                g.circle(x,y,7.3,fill=GOLD)

def coords(ln,n):
    return (LX*n[0]/100,LY*n[1]/100,LZ*n[2]/100)

def outer(w,n,primary,t,replace=0,al=1):
    dx,dy,dz=coords(0,n)
    x,y,z=O
    cs=((x,y,z),(x+dx,y,z),(x+dx,y+dy,z),(x,y+dy,z),
        (x,y,z-dz),(x+dx,y,z-dz),(x+dx,y+dy,z-dz),(x,y+dy,z-dz))
    for idx,c,v in (((0,1,2,3),primary,.105),((3,2,6,7),primary,.185),((1,5,6,2),primary,.224)):
        w.face(tuple(cs[i] for i in idx),c,al*.72,fill=v,edge=0)
    for a,b,j in ((0,1,0),(1,2,1),(2,3,0),(3,0,1),(4,5,0),(5,6,1),(6,7,0),(7,4,1),
                  (0,4,2),(1,5,2),(2,6,2),(3,7,2)):
        c=(GOLD,CYAN,GREEN)[j] if primary==CYAN and a in (0,3) else primary
        c=blend(c,CORAL,replace) if replace else c
        w.segment(cs[a],cs[b],c,2.6,al*(1 if a in (0,1,2,3) else .74))
    return cs[2],cs[6]

def project(w,p,c,a,lock=0,which=0):
    if a<.002:return
    x,y,z=p
    p1=(x,O[1],z)
    p2=(x,O[1],O[2])
    w.path((p,p1,p2),c,1.72,a*.84,dash=[4,6],progress=ramp(a,0,.9))
    pin(w,p2,GOLD,.059,a*lock,8)

def dimension_axes(w,al):
    o=O
    if al<.002:return
    y1=add(o,(0,LY+.19,0));z1=add(o,(0,0,-LZ-.32))
    w.path((o,y1),CYAN,2.25,al,arrow=True)
    w.path((o,z1),GREEN,2.22,al,arrow=True)
    led(w,'对话',add(y1,(-.01,.29,.085)),CYAN,al,25)
    # Label on the depth arrow, lifted enough to separate from the ground ruler.
    for j in (1,2,3,4):
        v=j/4
        y=o[1]+LY*v
        w.segment((o[0]-.059,y,0),(o[0]+.061,y,0),CYAN,1.23,al*.73)
        z=-LZ*v
        w.segment(add(o,(0,0,z)),add(o,(-.10,0,z)),GREEN,1.26,al*.66)

def comparison(w,n,other,shrink,a=1):
    if a<.002:return
    g=w.g
    x0,y0=1050,236
    g.text('模型 A',1335,y0,29,WHITE,a,font=SERIF)
    if other>.002:
        g.text('模型 B',1455,y0,29,PURPLE,a*other,font=SERIF)
    for j,(name,c,v) in enumerate(zip(('Benchmark','对话','自主规划'),(GOLD,CYAN,GREEN),n)):
        y=y0+57+54*j
        g.text(name,x0,y,27,c,a,align='left',font=SERIF)
        active=blend(c,CORAL,shrink) if j else c
        g.text(fmt(v),1335,y,33,active,a,font=SERIF)
        if other>.002:g.text(fmt(OTHER[j]),1455,y,31,PURPLE,a*other,font=SERIF)

def turning(w,u,mark):
    # Rotate the very same baseline on its left endpoint, including the
    # measured point and the notches. Register it with the next chart at 90°.
    phi=ramp(u,.0,1)
    root=vlerp(O,AX0,ramp(phi,.23,.99))
    angle=math.pi*.5*phi
    axis=(math.cos(angle),math.sin(angle),0)
    normal=(math.sin(angle),-math.cos(angle),0)
    length=mix(LX+.15,AXT[1]-AX0[1],phi)
    c=blend(GOLD,AXIS,ramp(phi,.51,1))
    w.path((root,add(root,mul(axis,length))),c,mix(2.28,2.25,phi),1,arrow=True)
    label=1-ramp(phi,.01,.41)
    for j in range(6):
        extent=mix(LX,length-.08,phi)*j/5
        q=add(root,mul(axis,extent))
        w.segment(add(q,mul(normal,-.065*phi)),add(q,mul(normal,mix(.112,.065,phi))),
                  c,mix(1.46,1.49,phi),mix(1,.82,phi))
        led(w,j*20,add(q,(0,-.30,.045)),MILD,label,19,'center')
    led(w,'基准标尺',add(root,(LX*.46,-.66,.05)),GOLD,label,25,'center')
    m=mix(LX*mark/100,length-.18,phi)
    pin(w,add(add(root,mul(axis,m)),(0,0,mix(.047,.05,phi))),GOLD,mix(.064,.057,phi),1)
    led(w,fmt(mark),add(add(root,mul(axis,m)),(0,score_label_y(mark),.081)),GOLD,label,30,'center')

def corners(n):
    dx,dy,dz=coords(0,n)
    x,y,z=O
    return ((x,y,z),(x+dx,y,z),(x+dx,y+dy,z),(x,y+dy,z),
            (x,y,z-dz),(x+dx,y,z-dz),(x+dx,y+dy,z-dz),(x,y+dy,z-dz))

def edge_map(w,n,phase,col,which):
    if phase<.002:return
    v=corners(n)
    l=((0,1),(1,2),(3,7))[which]
    p,q=v[l[0]],v[l[1]]
    q=vlerp(p,q,phase)
    w.segment(add(p,(0,0,.03)),add(q,(0,0,.03)),col,5.55,phase,sort_depth=.117)
    pin(w,add(q,(0,0,.043)),col,.060,phase)

def shadow_tracks(w,n,t,anchor,col,al):
    if al<.002:return
    for j,p in enumerate(corners(n)):
        x,y,z=p
        if abs(y-O[1])+abs(z-O[2])<.001:continue
        start=anchor+.31*j
        reach=2.35+.10*(j%3)
        u=ramp(t,start,start+reach)
        stay=.39+.61*(1-ramp(t,start+reach,start+reach+.90))
        q=(x,O[1],O[2]+.024)
        # Parallel motion in the kernel of the projection: X never changes.
        w.segment(p,q,col,2.05,al*u*stay,dash=[4,4])
        if .002<u<.998:pin(w,vlerp(p,q,u),col,.060+.022*math.sin(math.pi*u),al*.96)
        elif u>.997:pin(w,q,GOLD,.047,al*.88)

def scale_comparison(w,n,other,shrink,vis,hi,selection):
    g=w.g; x0,y0=1093,216
    if vis<.002:return
    g.text('模型 A',x0,y0,32,CYAN,vis,align='left',font=SERIF)
    g.text('模型 B',1393,y0,30,PURPLE,vis*other,align='right',font=SERIF)
    for j,(name,c,v) in enumerate(zip(('推理','对话','自主规划'),(GOLD,CYAN,TEAL),n)):
        y=y0+57+98*j; h=hi[j]
        c2=blend(c,CORAL,shrink*.87 if j else 0)
        row=vis*(1-.62*selection*other if j else 1)
        g.text(name,x0,y,28,c,row,align='left',font=SERIF)
        g.line(x0,y+30,x0+258,y+30,EDGE,2,row)
        g.line(x0,y+30,x0+v*2.58,y+30,c2,5+2.6*h,row)
        g.circle(x0+v*2.58,y+30,4.5+2*h,fill=c2,alpha=row)
        if other:
            g.line(x0,y+46,x0+OTHER[j]*2.58,y+46,PURPLE,3.8,row*other)
            g.circle(x0+OTHER[j]*2.58,y+46,4.3,fill=PURPLE,alpha=row*other)
        if j==0:
            g.text(str(round(v)),x0+279,y+30,27,c,vis,align='left',font=SERIF)
            if selection>0 and other>.04:
                target=x0+OTHER[0]*2.58
                mark=mix(x0+.09,target,selection)
                g.line(x0,y+20,mark,y+20,GOLD,1.8,vis*.86)
                g.circle(mark,y+20,5.2,fill=GOLD,alpha=vis)
                g.line(target,y+18,target,y+49,GOLD,2.4,ramp(selection,.71,1)*vis)
                # One open pulse marks the shared score as the two rows align.
                pulse=ramp(selection,.33,.73)*(1-.52*ramp(selection,.82,1))
                arrive=ramp(selection,.70,1)
                g.circle(mark,mix(y+20,y+30,arrive),8+6*arrive,
                         stroke=GOLD,width=1.9,alpha=vis*other*pulse*.80)
        elif shrink>.02:
            g.text(str(round(v)),x0+279,y+30,24,c2,vis*shrink,align='left',font=SERIF)

def second(g,t,d):
    if t<=0:xpose(g).draw();return
    seq=('multi-step reasoning','nuanced dialogue','autonomous planning')
    keys=tuple(T(g,t,d,n,4+i*2) for i,n in enumerate(seq))
    approach=T(g,t,d,'high-dimensional space',9)
    stepin=T(g,t,d,"project that entire space",12.8)
    same=T(g,t,d,'exact same shadow',19)
    gt=T(g,t,d,"Goodhart's law",25.5)
    squeeze=T(g,t,d,'optimizing directly',27)
    end=ramp(t,d-2.16,d-.073)
    if end>=.99998:vertical(g).draw();return
    emerge=ramp(t,.06,2.1)
    present=1-ramp(end,.045,.72)
    yaw=(.40*emerge+.125*ramp(t,keys[2],approach+1.02)-.073*ramp(t,stepin,stepin+1.7)+
         .089*ramp(t,same,same+3)-.110*ramp(t,squeeze,d-1.48))*(1-end)
    ph=(.12*emerge+.073*ramp(t,keys[2]-.22,approach+.83)
        -.13*ramp(t,approach+.37,stepin+.60))*(1-end)
    zoom=(1+.046*ramp(t,stepin-.3,stepin+1.1)-.018*ramp(t,same,same+1.8))*(1-end)+end
    w=roto(g,t,yaw=yaw,pitch=ph,zoom=zoom,target=(emerge*.06*(1-end),0,0))
    mark=mix(82,98,ramp(t,squeeze+.12,d-2.16))
    if end:turning(w,end,mark)
    else:x_ruler(w,markpos=mark)
    dimension_axes(w,emerge*present)
    for j,((x,y,z),key,col) in enumerate(zip((add(O,(LX+.35,.27,.04)),add(O,(-.19,LY+.33,.04)),
                                                add(O,(.03,.46,-LZ-.53))),keys,(GOLD,CYAN,TEAL))):
        al=(.24+.76*ramp(t,key-.06,key+.50))*emerge*present
        if j==2 and al:
            # Paint this axis name in front of the cuboid, not behind its faces.
            px,py=w.pos(add(O,(-.11,-.20,-LZ-.51)))
            w.items.append((10.,3,'自主规划',px+7,py-12,26,TEAL,al,'left',SERIF,'normal'))
    build=ramp(t,.055,.42)*present
    alt=ramp(t,same-2.25,same+.54)*(1-ramp(t,squeeze-.12,squeeze+.78))*present
    melt=ramp(t,squeeze+.085,d-2.16)
    # The baseline splits into the front outline, then opens in depth.
    # Its measured length is invariant while the other dimensions unfold.
    assemble=(1,ramp(t,.09,keys[1]+.55),ramp(t,.27,approach+.44))
    n=tuple(mix(a*q,b,melt) for a,b,q in zip(GOOD,RACE,assemble))
    emphasis=tuple(blink(t,h-.08,2.25) for h in keys)
    if build>.002:
        _,q=outer(w,n,CYAN,t,melt,build*(1-.11*alt))
        for j,h in enumerate(emphasis):edge_map(w,n,h*present,(GOLD,CYAN,TEAL)[j],j)
        shadow_tracks(w,n,t,stepin,GOLD,build*(1-.6*melt))
        if t>=stepin:
            k=ramp(t,stepin+.14,same-.92)
            a=add(O,(.0,.028,.027));b=add(O,(LX*n[0]/100*k,.028,.027))
            strength=.46+.54*(1-ramp(t,same-.60,same+.90))
            w.segment(a,b,GOLD,3.4+2.55*strength,build*present*strength)
            pin(w,b,GOLD,.055,build*present*strength)
        if alt>.002:
            outer(w,OTHER,PURPLE,t,0,alt)
            shadow_tracks(w,OTHER,t,same-.60,PURPLE,alt)
        rows=ramp(t,keys[0]-.05,keys[0]+.63)*present
        target=ramp(t,T(g,t,d,"the moment the community",21),gt+.66)
        scale_comparison(w,n,alt,melt,rows,emphasis,target)
    if gt<=t<d-1.39:
        aa=ramp(t,gt-.03,gt+.69)*present
        note(w,(2.63,-1.27,.16),"Goodhart’s law",('指标成了目标，','就可能偏离原本要测的东西。'),CORAL,aa)
    demo_badge(w,'几何示意',present*emerge,x=-4.55,y=2.68)
    w.draw()
    shared=alt*ramp(t,same-.10,same+.56)*(1-ramp(melt,.012,.092))
    if shared>.002:
        x82,y82=w.pos(add(O,(LX*.82,-.47,.081)))
        g.text('投影等长',x82+22,y82+44,28,WHITE,shared,font=SERIF)
    if gt<=t<d-1.39:
        xx,yy=w.pos(add(O,(LX*n[0]/100,.0,.051)))
        h=blink(t,squeeze-.045,1.81)
        if h>.002:g.circle(xx,yy,12+8*(1-h),stroke=GOLD,width=2.3,alpha=h)

def draw(g,i,t,duration):
    (first,second)[i](g,t,duration)
