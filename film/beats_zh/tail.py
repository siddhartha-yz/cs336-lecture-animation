"""Chunks E/F: open one score, control the experiment, then keep its finish line."""
from cut_common import *
from datetime import date
from pathlib import Path
import json

LFINAL=(-2.45,.30,.13)
RFINAL=(2.44,.30,.08)
LRX,LRY,LPOWER=1.975,1.275,.076
FREEZE=(.33,1.70)
SOURCE=(Path(__file__).resolve().parent.parent/'beats_real'/'data'/
        'nanogpt_main_track_2024_2025.json')
DATA=json.loads(SOURCE.read_text(encoding='utf-8'))
RECORDS=tuple((date.fromisoformat(r['date']),r['minutes']) for r in DATA['records'])
VAL=f"{DATA['cross_entropy_target']:.2f}"
BOX_BG=BOX
AX_BLUE=CYAN
ALT_BLUE=PURPLE

def a(u,l,h):return step(u,l,h)
def off(u,l,h):return 1-a(u,l,h)
def pulse(u,l,h,s,t):return a(u,l,h)*off(u,s,t)

def phase(g,i,t,duration):
    cues=(
      ((("single scoreboard",),.024),(("evaluating a method",),.117),
       (("in classical machine learning","give the two methods"),.181),
       (("on imagenet or squad","imagenet and squad"),.257),
       (("if model a won","once the rest stays fixed"),.377),
       (("in modern foundation models","now compare two finished systems"),.523),
       (("training sets","their training mixtures"),.603),
       (("brilliant new attention","maybe its attention"),.794),
       (("or simply ingested","maybe it saw"),.866)),
      ((("great for procurement",),.010),
       (("fundamental algorithmic progress",),.025),
       (("nanogpt speedrun",),.049),
       (("training token stream in a fixed order","fixed one billion tokens","one stream of tokens"),.151),
       (("eight h one hundred","eight h100"),.246),
       (("three point two eight","3.28"),.365),
       (("wall clock time","the training logs"),.477),
       (("every single minute","forty-five minutes"),.552),
       (("about eleven",),.634),
       (("genuine algorithmic","just under three"),.711),
       (("notice what sits","now follow the finish line"),.783),
       (("driving down validation loss","real probabilities"),.864),
       (("foundational metric","that average sets"),.956)),
    )[i]
    s=getattr(g,'speech',0.)
    end=clamp((s if s>0 else duration-FREEZE[i])/duration,.64,.998)
    u=clamp(t/duration)
    if u<=0:return 0.
    if u>=end:return 1.
    t0=v0=0.
    for k,(phrases,v) in enumerate(cues):
        default=end*v
        x=next((q for q in (g.cue(p,-1.) for p in phrases) if q>=0),default)
        x=clamp(x,t0+.004,end-(len(cues)-k)*.006)
        if u<=x:return mix(v0,v,(u-t0)/(x-t0))
        t0,v0=x,v
    return mix(v0,1,(u-t0)/(end-t0))

def outline(p,rx,ry,power=.25,N=76):
    x,y,z=p
    pts=[]
    for j in range(N+1):
        ang=-math.pi/2+j*math.tau/N
        v,q=math.cos(ang),math.sin(ang)
        # Snap the four analytic quadrants to zero before exponentiating.
        # At near-square exponents float epsilon would otherwise open the rim.
        vx=0. if abs(v)<1e-12 else math.copysign(abs(v)**power,v)
        vy=0. if abs(q)<1e-12 else math.copysign(abs(q)**power,q)
        pts.append((x+rx*vx,y+ry*vy,z))
    return tuple(pts)

def inktrace(w,pts,c,vis=1,width=2.11,progress=1,flourish=.30,dash=None):
    if vis<=.002:return
    w.path(pts,c,width,vis,progress=progress,dash=dash)

def flight(w,p0,p1,p2,p3,k,c=GOLD,al=1,line=MILD,tip=True):
    if al<=.002 or k<=0:return
    w.curve(p0,p1,p2,p3,line,1.75,al*.89,progress=k,arrow=tip)
    if .006<k<.993:
        z=1-k
        p=add(add(mul(p0,z**3),mul(p1,3*z*z*k)),add(mul(p2,3*z*k*k),mul(p3,k**3)))
        pin(w,p,c,.030,al*.90,5.5)

def lpos(u):
    # Once detached from the opening rank pin, the first panel is the object
    # that stays put while everything else is compared with it.
    return LFINAL

def method_outline(w,u,p,vis=1):
    g=a(u,.076,.234);m=a(u,.123,.236)
    geom=(mix(RING_RADIUS,LRX,g),mix(RING_RADIUS,LRY,g),mix(1,LPOWER,m))
    rim=outline(p,*geom)
    inktrace(w,rim,CYAN,vis*(.78+.17*a(u,.801,.965)),2.0,flourish=.43)
    k=off(u,.145,.23)*vis
    pin(w,p,GOLD,mix(.057,.040,g),k)

def process(w,p,variant,al=1,grow=1):
    if al<=.002:return
    c=AX_BLUE if not variant else ALT_BLUE
    w.path(outline(p,.361,.361,1,N=44),c,1.66,al*.89,progress=grow)
    coords=((-.13,-.11),(0,.148),(.132,-.11)) if not variant else (
        (-.14,-.112),(-.14,.112),(.125,.112),(.146,-.112))
    nodes=[add(p,(x,y,.077)) for x,y in coords]
    links=((0,1),(1,2),(0,2)) if not variant else ((0,1),(1,2),(2,3),(0,2),(0,3))
    for k,(i,j) in enumerate(links):
        w.path((nodes[i],nodes[j]),c,1.37,al*.82,
               progress=a(grow,.031*k,.65+.030*k))
    for j,pt in enumerate(nodes):w.dot(pt,c,.029,al*a(grow,.038*j,.35+.07*j))

def rect(w,x,y,z,ww,hh,c,al=1,fill=1.,stroke=0):
    if al<=.002 or min(ww,hh)<=.0002:return
    w.face(((x-ww/2,y-hh/2,z),(x+ww/2,y-hh/2,z),
            (x+ww/2,y+hh/2,z),(x-ww/2,y+hh/2,z)),c,al,fill,stroke)

def streams(w,p,al=1,sweep=-1,c=GOLD):
    # Each pipeline uses the same ordered stream, not two independent draws.
    for j,n in enumerate((.14,.18,.14,.19,.16,.14,.20)):
        x=p[0]+(j-3)*.158;y=p[1]
        bump=max(0,1-abs(sweep-j)/1.2) if sweep>=0 else 0
        rect(w,x,y+(n-.11)/2+.063*bump,p[2],.106,n,c,al*(.70+.28*bump))

def bezier_at(p0,p1,p2,p3,s):
    v=1-s
    return add(add(mul(p0,v**3),mul(p1,3*v*v*s)),add(mul(p2,3*v*s*s),mul(p3,s**3)))

def runner(w,p0,p1,p2,p3,s,c=GOLD,op=1,r=.032):
    s=clamp(s)
    if op<=.002 or not 0<s<1:return
    w.dot(bezier_at(p0,p1,p2,p3,s),c,r,op*a(s,0,.09)*off(s,.93,1))

def runner_train(w,p0,p1,p2,p3,u,c,vis,k=3):
    for j in range(k):
        runner(w,p0,p1,p2,p3,(u+j/k)%1.,c,vis)

def scores(w,loc,y,v,c,j,vis=1,reveal=1,system=False):
    if vis<=.002:return (loc,y,.17)
    x,z=loc,.164
    span=2.58
    for q,color,al in ((span,EDGE,vis*.31),(span*v*reveal,c,vis*.99)):
        if q>.001:
            w.face(((x,y-.041,z),(x+q,y-.041,z),(x+q,y+.041,z),(x,y+.041,z)),
                   color,al,1.,0)
    w.text(('系统 ' if system else '方法 ')+('A','B')[j],
           (x-.17,y,.24),23,c,vis,align='right',font=SERIF)
    return (x+span*v*reveal,y,z+.051)

def control_side(w,u,p,vis=1,rim=True):
    if vis<=.002:return
    if rim:method_outline(w,u,p,vis)
    x,y,z=p
    method=a(u,.128,.203);data=a(u,.164,.255);same=a(u,.231,.315)
    tests=a(u,.252,.326);gap=a(u,.335,.433)
    w.text('方法',(x,y+1.850,.19),39,WHITE,vis*method)
    w.text('ImageNet · SQuAD',(x,y+1.423,.21),25,WHITE,
           vis*a(u,.231,.289),font=SERIF)
    train=(x,y+.700,.16)
    spool=pulse(u,.168,.214,.440,.540)
    streams(w,train,vis*data,(u*69)%8.1 if spool>.10 else -1,CYAN)
    w.text('同一训练集',(x,y+.985,.21),23,WHITE,vis*data)
    held=y-.734
    w.segment((x-1.61,held,.14),(x+1.61,held,.14),GOLD,1.85,vis*tests*.91)
    w.text('同一留出测试集',(x,held-.204,.23),23,WHITE,vis*tests)
    bars=[]
    for j,d in enumerate((-.76,.76)):
        c=AX_BLUE if not j else ALT_BLUE
        op=(x+d,y-.028,.192)
        arrive=a(u,.188+j*.021,.307+j*.018)
        path=(add(train,(0,-.122,.021)),(x+d*.20,y+.39,.16),
              (x+d*.85,y+.45,.173),add(op,(0,.359,.024)))
        flight(w,*path,arrive,CYAN,vis*data)
        if u<.99:runner_train(w,*path,u*19.8+j*.12,CYAN,vis*spool*arrive)
        opvis=a(u,.150+j*.027,.203+j*.035)
        sw=a(u,.234,.331) if j else 0
        process(w,op,0,vis*opvis*(1-sw),opvis)
        if sw:process(w,op,1,vis*opvis*sw,sw)
        out=(x+d,held,.14)
        run=a(u,.254+j*.020,.380+j*.025)
        path2=(add(op,(0,-.359,0)),add(op,(0,-.45,0)),add(out,(0,.201,.017)),out)
        flight(w,*path2,run,c,vis*same)
        if u<.99:runner_train(w,*path2,u*15.8+j*.11,GOLD,vis*tests*run*spool,2)
        w.dot(out,GOLD,.038,vis*tests)
        hg=a(u,.336+j*.017,.430+j*.025)
        bars.append(scores(w,x-.904,y-1.625-j*.35,(.73,.51)[j],c,j,vis*gap,hg))
    extra=a(u,.329,.370)*vis
    w.text('其余条件固定',(x,held-.402,.23),21,TEAL,extra)
    proof=pulse(u,.355,.410,.518,.626)*vis
    if proof:
        ep=bars[0]
        proofpath=(add(ep,(0,.080,.023)),(x+1.92,y-1.72,.18),(x+1.71,y+.185,.276),
                   (x-.408,y+.050,.262))
        flight(w,*proofpath,a(u,.373,.494),AX_BLUE,proof*.63,AX_BLUE,tip=True)
        runner_train(w,*proofpath,u*15,AX_BLUE,proof,2)
    clamp=pulse(u,.924,.956,.997,1.)
    for j in (-1,1):
        if clamp:
            dx=mix(2.16,LRX-.052,clamp)*j
            w.path(((x+dx-j*.085,y-.87,z+.05),(x+dx,y-.87,z+.05),
                    (x+dx,y+.83,z+.05),(x+dx-j*.085,y+.83,z+.05)),TEAL,3.2,vis*clamp)

def blackbox(w,p,c,al=1,stage=0,*,shell=True,ink=True):
    if al<=.002:return
    x,y,z=p
    W,H=.59,.50
    poly=((-W,-H),(W,-H),(W,H-.093),(W-.093,H),(-W,H))
    if shell:
        for dx,dy,dz,aa in ((-.073,.056,-.098,.57),(0,0,0,1)):
            q=tuple((x+dx+xx,y+dy+yy,z+dz) for xx,yy in poly)
            w.face(q,BOX_BG,al*aa,1.,0)
            w.path((*q,q[0]),c,1.89 if aa==1 else 1.1,al*aa*.94)
    if not ink:return
    X=W-.067;Y=H-.090
    for j in range(-8,8):
        i=j*.125
        x0=max(-X,-Y-i);x1=min(X,Y-i)
        if x0<x1:
            peak=clamp(1-abs(j-(-8+(stage%1.)*16))/2)
            w.segment((x+x0,y+x0+i,z+.027),(x+x1,y+x1+i,z+.027),
                      c,.98,al*(.27+.37*peak))
    w.dot((x,y-.284,z+.052),GOLD,.037,al*.97)

def system_side(w,u,p,vis=1,*,shell=True):
    if vis<=.002:return
    intro=a(u,.517,.592)
    data=a(u,.575,.662)
    rank=a(u,.625,.732)
    cause=a(u,.738,.802)
    x,y,z=p
    w.text('系统',(x,y+1.850,.22),39,WHITE,vis*intro)
    held=y-.734
    bars=[]
    figs=pulse(u,.556,.599,.721,.774)
    for k,(dx,label) in enumerate(zip((-1.13,.0,1.13),('数据配比','训练方案','算力'))):
        f=figs*a(u,.565+k*.017,.593+k*.021)*vis
        if not f:continue
        src=(x+dx,y+1.159,.158)
        w.text(label,add(src,(0,.183,.05)),22,WHITE,f)
        w.dot(src,WHITE,.024,f*.8)
        for j,d in enumerate((-.746,.749)):
            dst=(x+d+(k-1)*.18,y+.488,.191+j*.078)
            points=(src,add(src,(.19*d,-.29,.013)),add(dst,(-.09*d,.20,-.012)),dst)
            col=(AX_BLUE,ALT_BLUE)[j]
            w.curve(*points,col,1.10,f*.91,progress=a(u,.575+k*.016,.624+k*.018))
            runner(w,*points,(u*12+k*.15+j*.28)%1.,col,f,.043)
    for j,d in enumerate((-.746,.749)):
        col=AX_BLUE if not j else ALT_BLUE
        op=(x+d,y-.016,z+.078*j)
        blackbox(w,op,col,vis*intro,u*16+j*.35 if u<.998 else 0,shell=shell)
        o=(op[0],held,z+.048)
        tip=a(u,.591+j*.017,.683+j*.025)
        lead=add(op,(0,-.50,0))
        w.path((lead,o),MILD,1.63,vis*data,arrow=True,progress=tip)
        glint=pulse(u,.592,.625,.733,.776)
        for jj in range(2):
            w.dot(vlerp(lead,o,(13*u+jj*.50)%1),GOLD,.034,vis*glint*tip)
        w.dot(o,GOLD,.037,vis*data)
        val=a(u,.658+j*.017,.742+j*.018)
        bars.append(scores(w,x-.900,y-1.625-j*.35,(.51,.841)[j],col,j,
                           vis*rank,val,system=True))
    w.segment((x-1.68,held,z+.033),(x+1.69,held,z+.033),GOLD,1.85,vis*data*.89)
    if cause:
        ranktip=bars[-1]
        # Carry the causal question outside the right box, then bend inward
        # above its top; the untouched box interior is part of the argument.
        elbow=(x+1.94,y-.52,z+.17)
        shoulder=(x+1.92,y+.670,z+.192)
        pivot=(x+.18,y+.880,z+.200)
        flight(w,add(ranktip,(.019,.074,.01)),(x+1.57,y-1.84,z+.22),
               (x+1.98,y-1.00,z+.18),elbow,a(u,.728,.766),CORAL,
               vis*cause,CORAL,tip=False)
        flight(w,elbow,(x+1.95,y-.16,z+.175),(x+1.96,y+.40,z+.186),
               shoulder,a(u,.761,.793),CORAL,vis*cause,CORAL,tip=False)
        flight(w,shoulder,(x+1.53,y+.790,z+.198),(x+.87,y+.877,z+.204),
               pivot,a(u,.784,.812),CORAL,vis*cause,CORAL,tip=False)
        for j,d in enumerate((-1,1)):
            p1=add(pivot,(.31*d,.18,0));p2=add(pivot,(.62*d,.26,.012))
            end=add(pivot,(1.04*d,.42,.041))
            cue=(.792,.849)[j]
            w.curve(pivot,p1,p2,end,CORAL,2.55,vis*cause,progress=a(u,cue-.011,cue+.041))
            pin(w,end,CORAL,.052,vis*a(u,cue+.025,cue+.044))
            w.text(('注意力更好？','代码和数学数据更多？')[j], add(end,(.104*d,.242,.082)),
                   25,CORAL,vis*a(u,cue+.005,cue+.055),font=SERIF)

def experiment(w,u,vis=1,la=1,ra=1,rim=True):
    p=lpos(u)
    control_side(w,u,p,vis*la,rim)
    system_side(w,u,RFINAL,vis*ra)
    shared=a(u,.582,.728)
    w.segment((p[0]+1.60,p[1]-.734,.13),(RFINAL[0]-1.60,RFINAL[1]-.734,.13),
              GOLD,1.60,vis*shared*min(la,ra)*.46,dash=[4.1,4.2])

def sense_camera(g,zoom=1,x=0,y=0):
    return World(g,zoom=zoom,target=(x,y,0))

def folded_rulers(g,stage,u):
    """Spine-fold the three unselected measurements, then slide the sheet off."""
    if u<=.025:
        stage(g).draw();return
    offstage=a(u,.048,.079)
    if offstage>=1:return
    right=a(u,.026,.059)
    lower=a(u,.031,.063)
    title=a(u,.042,.065)
    x0,hy,hy0=800.,378.,132.
    dx=-824*offstage
    def panel(x,y,ww,hh,sx,sy,ax,ay):
        if min(sx,sy)<.018:return
        c=g.c;c.save()
        c.translate(dx+ax,ay);c.scale(sx,sy);c.translate(-ax,-ay)
        c.rectangle(x,y,ww,hh);c.clip()
        stage(g).draw()
        c.restore()
    panel(0,0,1600,hy0,1,1-title,x0,hy0)
    panel(0,hy0,x0,hy-hy0,1,1,x0,hy)
    panel(x0,hy0,800,hy-hy0,1-right,1,x0,hy)
    panel(0,hy,x0,900-hy,1,1-lower,x0,hy)
    panel(x0,hy,800,900-hy,1-right,1-lower,x0,hy)

def method(g,u,t,dur):
    from middle import SELECTED, selection_stage
    if t==0:
        selection_stage(g).draw();return
    if u>=.999:
        w=sense_camera(g);experiment(w,1.);w.draw();return
    folded_rulers(g,selection_stage,u)
    front=pulse(u,.187,.284,.436,.574)
    w=sense_camera(g,zoom=1+.21*front)
    release=.042
    base=SELECTED
    emerge=a(u,release,.163)
    p=vlerp(base,LFINAL,emerge)
    methodalpha=a(u,.079,.103)
    if u<.176:
        lead=a(u,.034,.052)*off(u,.143,.176)
        if u>release:
            c1=add(base,(.30,.28,0));c2=add(LFINAL,(-.19,.31,0))
            p=bezier_at(base,c1,c2,LFINAL,emerge)
            w.curve(base,c1,c2,LFINAL,GOLD,1.92,
                    a(u,.048,.064)*off(u,.119,.159),progress=emerge)
        w.dot(p,GOLD,.058+lead*.017,lead)
    else:
        # Keep the controlled experiment in front while it runs; then make
        # room for the finished systems on the right.
        p=add(LFINAL,(1.47*front,.045*front,0))
    early=pulse(t,.04,.38,1.99,2.73)
    if early:
        # Select this particular ruler before the chosen score detaches.
        q=a(t,.10,2.41)
        r=mix(.102,.215,q)
        w.path(outline(base,r,r,1.,N=36),GOLD,2.25,early*.92,progress=q)
        w.dot(base,GOLD,.034+.017*q,early*.83)
    control_side(w,u,p,methodalpha)
    q=pulse(u,.091,.119,.177,.220)
    if q:
        q0=(.56,1.073,.288);q1=(2.76,1.073,.288)
        for j,(pt,c,label) in enumerate(((q0,CYAN,'方法'),(q1,PURPLE,'系统'))):
            vis=q*a(u,.094+j*.009,.133+j*.010)
            w.text(label,pt,35,c,vis)
            w.segment(add(pt,(-.45,-.236,0)),add(pt,(.45,-.236,0)),c,2.2,vis)
            lens=add(pt,(0,-.805,-.09))
            if not j:
                process(w,lens,0,vis*.90,clamp(1.15*vis))
                for k in range(4):
                    xx=lens[0]+(k-1.5)*.153
                    rect(w,xx,lens[1]-.502,.203,.093,.071,GOLD,vis*.88)
            else:
                blackbox(w,lens,PURPLE,vis*.79,a(u,.100,.177))
    sr=a(u,.514,.573)
    if sr:
        system_side(w,u,RFINAL,sr)
        shared=a(u,.582,.728)
        w.segment((LFINAL[0]+1.60,LFINAL[1]-.734,.13),
                  (RFINAL[0]-1.60,RFINAL[1]-.734,.13),
                  GOLD,1.70,sr*shared*.69,dash=[4.1,4.2])
    w.draw()

# Time-to-target records, not within-run loss traces. Each step takes its
# height and date from the official main-track ledger through record #20.
X0=-4.18
X1=4.31
D0,D1=RECORDS[0][0],RECORDS[-1][0]
Y0=-1.005
Y45=1.080
RAIL=-1.88
TITLE_Y=2.55

def days_to_x(d):
    return mix(X0,X1,(d-D0).days/(D1-D0).days)

def minutes_to_y(v):
    return mix(Y0,Y45,v/45)

def place(d,min_):
    return days_to_x(d),minutes_to_y(min_),.073

POINTS=tuple(place(d,m) for d,m in RECORDS)
JOGS=[POINTS[0]]
for prev,p in zip(POINTS,POINTS[1:]):
    JOGS.extend(((p[0],prev[1],.073),p))
STAIRS=tuple(JOGS)

def data_badge(w,al):
    if al>.002:
        w.text('modded-nanogpt · 2024.05–2025.01',(4.48,TITLE_Y,.217),24,
               MILD,al,align='right',font=SERIF)

def wall_axes(w,alpha):
    if alpha<=.002:return
    o=(X0,Y0,0)
    w.path((o,(X1+.187,Y0,0)),MILD,1.65,alpha*.89,arrow=True)
    w.path((o,(X0,Y45+.204,0)),MILD,1.65,alpha*.89,arrow=True)
    for min_ in (0,15,30,45):
        y=minutes_to_y(min_)
        w.segment((X0-.056,y,.01),(X0+.063,y,.01),MILD,1.32,alpha*.89)
        w.text(str(min_),(X0-.126,y,.094),23,MILD,alpha,align='right',font=SERIF)
    for date_,label in ((D0,'2024年5月'),(date(2024,8,1),'8月'),
                         (date(2024,11,1),'11月'),(D1,'2025年1月')):
        x=days_to_x(date_)
        w.segment((x,Y0-.047,.03),(x,Y0+.057,.03),MILD,1.17,alpha*.85)
        w.text(label,(x,Y0-.191,.123),22,MILD,alpha,font=SERIF)
    w.text('实际耗时（分钟）',(X0,1.440,.13),25,WHITE,alpha,font=SERIF,align='left')

def small_labels(w,i,alpha):
    if alpha<=.002:return
    p=POINTS[i]
    if i==0:
        pin(w,p,GOLD,.062,alpha,9.5)
        end=(p[0]+.52,p[1]-.256,.132)
        q=(p[0]+.071,p[1]-.052,.145)
        w.segment(q,end,GOLD,1.37,alpha)
        w.text('45 分钟 · 基线',add(end,(.098,-.004,.039)),27,GOLD,alpha,
               font=SERIF,align='left')
        w.text('2024.05.28',add(end,(.098,-.265,.038)),23,MILD,alpha,
               font=SERIF,align='left')
    elif i==7:
        pin(w,p,GOLD,.053,alpha,9)
        q=add(p,(-.39,.402,.046));end=add(q,(-.45,.06,0))
        w.path((add(p,(-.055,.087,.042)),q,end),GOLD,1.43,alpha)
        w.text('10.8 分钟 · 2024.11.03',add(end,(-.093,.09,.034)),25,GOLD,alpha,
               font=SERIF,align='right')
        w.text('嵌入层与输出头不再共享权重',add(end,(-.093,-.148,.034)),22,MILD,alpha,
               font=SERIF,align='right')
    else:
        pin(w,p,GOLD,.066,alpha,10.0)
        q=add(p,(-.30,.463,.048));end=add(q,(-.426,.063,0))
        w.path((add(p,(-.045,.072,.029)),q,end),GOLD,1.47,alpha)
        w.text('2.992 分钟',add(end,(-.091,.084,.029)),29,GOLD,alpha,font=SERIF,align='right')
        w.text('2025.01.16',add(end,(-.091,-.183,.032)),22,MILD,alpha,font=SERIF,align='right')

def record_progress(u):
    # Place the three narrative milestones at their real positions in history.
    if u<=.526:return 0.
    marks=((.526,0.),(.648,14/38),(.738,1.))
    for (u0,q0),(u1,q1) in zip(marks,marks[1:]):
        if u<u1:return mix(q0,q1,a(u,u0,u1))
    return 1.

def record_chart(w,u,vis=1):
    axes=a(u,.411,.503)*vis
    k=a(u,.476,.518)*vis
    w.text('NanoGPT 速训挑战',(X0,TITLE_Y,.14),42,WHITE,a(u,.425,.490)*vis,align='left')
    data_badge(w,a(u,.439,.497)*vis)
    wall_axes(w,axes)
    q=record_progress(u)
    if k:
        stroke=3.54+1.8*a(u,.50,.60)
        lit_path(w,STAIRS,CYAN,stroke,k*.99,progress=q)
        at=(len(STAIRS)-1)*q
        j=int(at);p=vlerp(STAIRS[j],STAIRS[min(j+1,len(STAIRS)-1)],at-j)
        pin(w,p,CYAN,.063,k*a(u,.492,.524)*off(u,.729,.767))
        for j,p in enumerate(POINTS):
            if 2*j<=at and j not in (0,7,len(POINTS)-1):w.dot(p,CYAN,.023,k*.83)
    small_labels(w,0,k*a(u,.494,.537))
    small_labels(w,7,k*a(u,.615,.655))
    small_labels(w,len(POINTS)-1,k*a(u,.710,.752))

# The small first plot is a schema of one run only. It deliberately has no
# numerically graduated loss/time axes beyond its real stopping threshold.
WX0=.57;WX1=4.99
WY0=-1.57;WY1=1.36
WRAIL=-.73
LOSS=(
    (.59,1.21,.14),(1.29,.78,.14),(2.01,.86,.14),(2.72,.29,.14),
    (3.45,.36,.14),(4.17,-.31,.14),(4.89,WRAIL,.14),
)
TRAIN_START=.233
LOSS_STOP=.372
TRAIN_BATCHES=len(LOSS)-1
ARRIVALS=(.115,.160,.205,.250,.272,.314,.355,.397)

def update_state(u):
    """One schematic cycle: feed → compute → measure → plot new loss."""
    k=clamp((u-TRAIN_START)/(LOSS_STOP-TRAIN_START))*TRAIN_BATCHES
    if k>=TRAIN_BATCHES:return 1.,0.,False
    i=int(k);f=k-i
    return (i+a(f,.675,1.))/TRAIN_BATCHES,f,u>=TRAIN_START

def clock_kick(u):
    """A self-settling mechanical response, beginning at the crossing."""
    d=max(0.,(u-LOSS_STOP)/.015)
    if not 0<d<3:return (0.,0.)
    decay=math.exp(-2.15*d)*off(d,2.3,3.)
    return math.sin(11.8*d)*decay,math.sin(8.4*d)*decay

def poly_at(pts,v):
    x=clamp(v)*(len(pts)-1)
    i=int(x)
    return vlerp(pts[i],pts[min(i+1,len(pts)-1)],x-i)

def path_clock(w,p,r,q,al=1,finish=0):
    if al<=.002:return
    x,y,z=p
    w.path(outline(p,r,r,1.,N=44),WHITE,2.14,al*.91)
    for j in range(12):
        t=j*math.tau/12
        u,v=math.sin(t),math.cos(t)
        rr=r*(.79 if j%3==0 else .86)
        w.segment((x+rr*u,y+rr*v,z+.011),(x+r*.951*u,y+r*.951*v,z+.011),
                  WHITE,1.66 if j%3==0 else .95,al*.90)
    top=y+r
    w.path(((x-.063,top+.068,z),(x-.063,top+.125,z),(x+.065,top+.125,z),
            (x+.065,top+.067,z)),WHITE,1.7,al)
    th=q*math.tau
    hand=(x+r*.74*math.sin(th),y+r*.74*math.cos(th),z+.029)
    w.segment((x,y,z+.026),hand,blend(CYAN,GOLD,finish),2.89,al)
    w.dot((x,y,z+.041),GOLD if finish>.55 else WHITE,.029,al)

def fixed_tape(w,u,x0,x1,y,c,name,vis,rail):
    if vis<=.002:return
    w.text(name,(x0,y+.263,.27),27,WHITE,vis,align='left')
    if rail:w.segment((x0,y-.160,.101),(x1,y-.160,.101),c,1.7,vis*.87)
    N=14
    space=(x1-x0)/N
    motion=off(u,.382,.456)
    p=min(u,.445)*34.7
    for j in range(N):
        f=(j+(p%1)*motion)/N
        x=mix(x0,x1,f)
        ink=a(f,0,.045)*off(f,.963,1)
        n=(j-int(p))%8
        hh=(.102,.173,.123,.142,.177,.111,.134,.158)[n]
        rect(w,x,y+(hh-.14)/2,.126,min(.146,space*.72),hh,c,vis*ink*.92)
    w.path(((x1-.103,y-.211,.139),(x1,y-.160,.139),(x1-.103,y-.116,.139)),
           c,1.65,vis)

def chip(w,x,y,u,idx,vis,cycle,active):
    gain=a(u,.207+idx*.006,.235+idx*.009)
    if gain<=.001:return
    z=.193
    p=(x,y,z)
    # Actual devices are counted by identical faces, not by animated billboards.
    xw=.242
    when=ARRIVALS[idx]
    heat=pulse(cycle,when-.008,when+.028,when+.129,when+.278) if active else 0.
    rect(w,x,y,z,.489,.313,TEAL,vis*gain,.115+.22*heat,1.44)
    rect(w,x,y,z+.028,.190,.134,TEAL,vis*gain*(.56+.40*heat),.51+.35*heat,1.12)
    if heat:
        rect(w,x,y,z+.043,.165,.105,CYAN,vis*gain*heat,.55+.41*heat,0)
    for side in (-1,1):
        for v in (-.102,0,.102):
            w.segment((x+side*(xw+.047),y+v,z+.008),(x+side*xw,y+v,z+.008),
                      TEAL,1.39,vis*gain*(.78+.22*heat))
    if heat>.35: w.dot(add(p,(0,0,.054)),WHITE,.017,vis*gain*heat)

def workbench(w,u,vis=1):
    if vis<=.002:return
    pipe=a(u,.092,.183)*vis
    second=a(u,.137,.214)*vis
    chamber=a(u,.171,.254)*vis
    w.text('NanoGPT 速训挑战',(-4.93,2.437,.176),48,WHITE,
           a(u,.038,.086)*vis,align='left')
    w.text('FineWeb · 词元顺序固定，用量可变',(-4.9,1.763,.142),27,WHITE,
           a(u,.119,.168)*vis,align='left')
    fixed_tape(w,u,-4.90,-.61,1.071,CYAN,'训练词元',pipe,u>=.132)
    fixed_tape(w,u+.025,-4.90,-.61,-1.030,GOLD,'留出验证',second,u>=.132)
    q,cycle,active=update_state(u)
    # Training executes at the rack. The held-out tape has an independent
    # route to the measurement; it never enters the weight-update path.
    hub=(-2.751,.911,.108)
    top=(-2.751,.643,.115)
    eval_pin=(.407,-.390,.139)
    train_out=((-1.55,.01,.133),(-.61,.01,.133),(-.61,.31,.133),
               (.145,.31,.133),(.145,-.310,.133),eval_pin)
    valid_in=((-.61,-1.19,.092),(-.33,-1.19,.092),(-.33,-.89,.092),
              (.145,-.89,.092),(.145,-.474,.104),eval_pin)
    if pipe:
        w.path((hub,top),CYAN,1.94,pipe,arrow=True,progress=a(u,.137,.233))
        if active and .003<cycle<.17:
            inpos=poly_at((hub,top),a(cycle,0.,.17))
            w.dot(inpos,CYAN,.052,pipe*pulse(cycle,.004,.033,.128,.17))
    for col in range(4):
        cx=-3.79+col*.716
        branching=a(u,.208+col*.007,.260+col*.008)
        path=(top,(cx,top[1],.116),(cx,.522,.118))
        lowerpath=(top,(cx+.31,top[1],.116),(cx+.31,-.215,.116),(cx+.244,-.215,.120))
        if branching:
            w.path(path,CYAN,1.22,chamber*.66,progress=branching)
            w.path(lowerpath,CYAN,1.14,chamber*.43,progress=a(u,.222+col*.007,.271+col*.008))
            for row,route in enumerate((path,lowerpath)):
                idx=row*4+col
                end=ARRIVALS[idx]
                begin=.040+.011*col+.090*row
                current=pulse(cycle,begin,begin+.042,end-.018,end+.006) if active else 0.
                if current:
                    w.dot(poly_at(route,a(cycle,begin,end)),CYAN,.042,chamber*current)
    t=a(u,.238,.301)
    if t:
        w.path(train_out,TEAL,1.82,chamber,progress=t,arrow=True)
        flow=pulse(cycle,.432,.479,.615,.669) if active else 0.
        if flow: w.dot(poly_at(train_out,a(cycle,.432,.669)),TEAL,.048,chamber*flow)
    for row in range(2):
        for col in range(4):
            chip(w,-3.79+col*.716,.365-row*.580,u,row*4+col,chamber,cycle,active)
    w.text('8 × H100',(-2.72,-.584,.152),25,TEAL,a(u,.220,.269)*vis)
    case=a(u,.226,.292)
    if case:
        w.path(valid_in,GOLD,1.81,second,progress=case,arrow=True)
        result=pulse(cycle,.409,.454,.621,.669) if active else 0.
        if result:w.dot(poly_at(valid_in,a(cycle,.409,.669)),GOLD,.044,second*result)
        judge=pulse(cycle,.638,.672,.704,.770) if active else 0.
        if judge:w.dot(eval_pin,WHITE,.046,judge*case*vis)
    graph=a(u,.207,.303)*vis
    if graph:
        w.path(((WX0,WY0,.083),(WX1,WY0,.083)),WHITE,1.61,graph,arrow=True)
        w.path(((WX0,WY0,.083),(WX0,WY1,.083)),WHITE,1.61,graph,arrow=True)
        w.text('验证损失',(WX0,1.588,.15),28,WHITE,graph,align='left')
        w.text('时间',(WX1,WY0-.204,.15),23,MILD,graph,align='right')
        w.text('单次运行示意',(WX0,2.405,.15),25,MILD,graph,align='left')
        if u>.229:
            w.path(LOSS,CYAN,4.07,graph,progress=q)
            p=poly_at(LOSS,q)
            w.dot(p,blend(CYAN,GOLD,a(q,.91,1.0)),.060,graph)
        reach=a(u,LOSS_STOP,LOSS_STOP+.010)
        needle,body=clock_kick(u)
        spin=1.61*clamp((u-.229)/(LOSS_STOP-.229))
        cp=(4.676+.031*body,1.942+.042*body,.149)
        path_clock(w,cp,.325*(1+.062*body),spin+.044*needle,graph,reach)
        w.text('停表',(4.676,1.381,.15),24,GOLD,graph*reach)
        hit=pulse(u,LOSS_STOP,LOSS_STOP+.008,LOSS_STOP+.019,LOSS_STOP+.040)
        if hit:
            spread=a(u,LOSS_STOP,LOSS_STOP+.039)
            w.path(outline(LOSS[-1],.070+.127*spread,.070+.127*spread,1.,N=28),
                   GOLD,1.96,graph*hit)

def strip_layout(u):
    shift=a(u,.406,.492);spread=a(u,.772,.896)
    return (mix(mix(WX0,X0,shift),TOKEN_LEFT,spread),
            mix(mix(WX1-.08,X1,shift),TOKEN_RIGHT,spread),
            mix(mix(WRAIL,RAIL,shift),TOKEN_Y,spread))

def line_to_strip(w,u,vis=1):
    amt=a(u,.300,.355)*vis
    if amt<=.002 or u>=.963:return
    x0,x1,y=strip_layout(u)
    n=len(token_data())
    if u<=.782:
        w.segment((x0,y,.105),(x1,y,.105),GOLD,2.24,amt,dash=[5.2,4.2])
    else:
        d=(x1-x0)/n
        slot=min(TOKEN_WIDTH*.5,d*.439)
        for j in range(n):
            x=x0+d*(j+.5)
            k=a(u,.797+j*.004,.885+j*.004)
            half=mix(d*.499,slot,k);h=TOKEN_HEIGHT*.50*k;z=.105
            if k<.055:
                w.segment((x-half,y,z),(x+half,y,z),GOLD,2.24,amt,dash=[5.2,4.2])
            else:
                # The two lips of each segment separate; short vertical
                # connectors close that segment into its own token slot.
                poly=((x-half,y-h,z),(x+half,y-h,z),(x+half,y+h,z),
                      (x-half,y+h,z),(x-half,y-h,z))
                w.path(poly,GOLD,mix(2.24,1.37,k),amt*mix(1.,.79,k))
    label=off(u,.771,.806)*amt
    gutter=.123  # ~19px at 1920-wide; keep ink away from the axis.
    # Do not drag the text through either axis while the chalk rule migrates.
    before=off(u,.406,.426)
    after=a(u,.446,.480)
    w.text('3.28 · 留出验证目标',(WX0+gutter,WRAIL+.170,.248),26,GOLD,
           label*before,align='left')
    w.text('3.28 · 留出验证目标',(x0+gutter,y+.170,.248),26,GOLD,
           label*after,align='left')

def token_ink(g,u,t,hold_start):
    if u<=.853:return
    _,_,rail=strip_layout(u)
    w=token_stage(g,center=(0,TOKEN_Y-rail,0))
    if u<.963:
        # Register the numbers in the exact slots. A geometric mask admits
        # the canonical lettering and vertical bars, not another overlay.
        c=g.c;c.save();c.new_path()
        def aperture(x0,y0,x1,y1,z=.134):
            ax,ay=w.pos((x0,y0,z));bx,by=w.pos((x1,y1,z))
            if bx>ax and by>ay:c.rectangle(ax,ay,bx-ax,by-ay)
        for j,x in enumerate(token_positions()):
            k=a(u,.850+j*.003,.920+j*.003)
            if k<=.001:continue
            span=.438
            if k>.44:
                aperture(x-span,TOKEN_Y+.156,x+span,TOKEN_Y-.156)
            aperture(x-span,TOKEN_BASELINE+.83*k,x+span,TOKEN_BASELINE-.049)
            if k>.66:
                aperture(x-span,TOKEN_Y-.25,x+span,TOKEN_Y-.574)
        c.clip();w.draw();c.restore()
        title=a(u,.951,.963)
        if title:
            whole=token_stage(g,alpha=title)
            c.save();c.new_path()
            aperture(-5.16,2.23,5.16,1.28)
            aperture(-5.16,-1.49,5.16,-1.77)
            c.clip();whole.draw();c.restore()
    else:w.draw()
    scan_w=sense_camera(g,y=TOKEN_Y-rail)
    n=len(token_data());late=a(t,hold_start-2.4,hold_start-.10)
    scan=mix(n*.22*a(u,.859,.940),n*.975,late)
    for j,x in enumerate(token_positions()):
        al=clamp(1-abs(scan-j-.45)/1.10)*a(u,.863,.900)*off(t,hold_start-.17,hold_start)
        if al:
            scan_w.segment((x-.42,TOKEN_Y-TOKEN_HEIGHT*.50-.048,.264),
                           (x+.42,TOKEN_Y-TOKEN_HEIGHT*.50-.048,.264),GOLD,2.84,al)
    scan_w.draw()

def retained_history(g,u):
    vis=a(u,.409,.498)*off(u,.883,.955)
    if vis<=.002:return
    dock=a(u,.783,.919)
    sc=mix(1.,.34,dock);dx=mix(0,28,dock);dy=mix(0,-17,dock)
    follow=pulse(u,.501,.553,.738,.782)
    cursor=poly_at(STAIRS,record_progress(u))
    # The frame bends towards the measured cursor, not away from the data.
    # Keep the same coordinate system and all three numeric marks inside.
    w=sense_camera(g,1+.044*follow,
                   x=.385*math.tanh(cursor[0]/4)*follow,
                   y=.092*cursor[1]*follow)
    g.c.save();g.c.translate(dx,dy);g.c.scale(sc,sc)
    record_chart(w,u,vis*(1-.68*dock));w.draw()
    g.c.restore()

def unfolding_bench(g,u):
    """The comparison shuts down, but its method frame becomes the two rails."""
    c=g.c
    # Readable ink releases from the unchanged pose before any metal bends.
    # Only the bare covers are passed through the anisotropic projection.
    ink=off(u,.043,.059)
    fold=a(u,.059,.125)
    sx=1-fold
    if sx>.016:
        c.save();c.translate(1358+186*a(u,.079,.125),0)
        c.scale(sx,1);c.translate(-1358,0)
        sheet=sense_camera(g)
        x,y,z=RFINAL
        for j,dx in enumerate((-.746,.749)):
            blackbox(sheet,(x+dx,y-.016,z+.078*j),(AX_BLUE,ALT_BLUE)[j],ink=False)
        sheet.draw()
        c.restore()
    w=sense_camera(g)
    if ink>.002:
        control_side(w,1.,LFINAL,ink,rim=False)
        system_side(w,1.,RFINAL,ink,shell=False)
    old0=(LFINAL[0]+1.60,LFINAL[1]-.734,.13)
    old1=(RFINAL[0]-1.60,RFINAL[1]-.734,.13)
    y=a(u,.043,.082)
    if y<1:
        w.segment(old0,vlerp(old1,old0,y),GOLD,1.60,.46,dash=[4.1,4.2])
    flat=a(u,.059,.132)
    if flat<1:
        rim=outline(LFINAL,LRX,LRY,LPOWER)
        strips=(tuple(reversed(rim[19:58])),(*rim[57:76],*rim[:20]))
        origin=LFINAL[0]-LRX
        for j,side in enumerate(strips):
            def pnew(p):
                k=(p[0]-origin)/(2*LRX)
                return vlerp(p,(mix(-4.90,-.61,k),(.911,-1.190)[j],.101),flat)
            tin=CYAN if not j else blend(CYAN,GOLD,a(u,.072,.132))
            coords=tuple(pnew(p) for p in side)
            w.path(coords,tin,mix(2.,1.7,flat),mix(.95,.87,flat))
    elif u<.214:
        # Once straight, each rail stays put; the tape's own identical ink
        # takes over the line as the tokens arrive.
        for yy,tin,k in ((.911,CYAN,a(u,.092,.183)),
                         (-1.19,GOLD,a(u,.137,.214))):
            if k<.999:
                need=(.87-.87*k)/(1.-.87*k)
                w.segment((-4.90,yy,.101),(-.61,yy,.101),tin,1.7,need)
    w.draw()

def race(g,u,t,dur):
    if t==0:
        w=sense_camera(g);experiment(w,1.);w.draw();return
    hold_start=min(dur-FREEZE[1],g.speech if g.speech>0 else dur)
    if t>=hold_start:
        token_stage(g).draw();return
    if u<=.043:
        prev=1.
        old=sense_camera(g);experiment(old,1.)
        # Procurement can pick the winning output. Moving backward from that
        # point still meets a fork, rather than a single explanatory path.
        k=pulse(t,.20,.78,4.71,5.93)
        if k:
            winner=(3.710,-1.679,.245)
            p=(mix(1.61,winner[0],a(t,.36,1.62)),winner[1],winner[2])
            old.path(outline(p,.094,.094,1.,N=30),GOLD,2.75,prev*k)
            old.segment(add(p,(-.245,0.,0)),add(p,(-.096,0.,0)),GOLD,3.52,prev*k)
            # Follow the score to the box one could actually buy, leaving
            # the separate coral fork unanswered.
            p0=add(winner,(.080,.065,.045));p1=(4.33,-1.55,.291)
            p2=(4.17,-.26,.291);p3=(3.81,-.086,.291)
            pick=a(t,1.48,3.55)
            if pick:
                old.curve(p0,p1,p2,p3,GOLD,3.48,prev*k,progress=pick,arrow=True)
                runner(old,p0,p1,p2,p3,pick,GOLD,prev*k,.063)
            box=(3.19,.28,.313)
            lock=a(t,3.36,4.82)
            if lock:
                old.path(outline(box,.635,.548,.22,N=40),GOLD,2.94,prev*k,progress=lock)
        f=pulse(u,.015,.023,.072,.140)
        if f:
            p0=(3.71,-1.60,.247);p1=(5.02,-.75,.25)
            p2=(4.51,1.11,.268);p3=(2.62,1.18,.285)
            runner(old,p0,p1,p2,p3,a(u,.018,.065),CORAL,prev*f,.058)
        old.draw()
    else:
        unfolding_bench(g,u)
    w=sense_camera(g)
    workbench(w,u,off(u,.407,.443))
    w.draw()
    retained_history(g,u)
    hand=sense_camera(g)
    line_to_strip(hand,u);hand.draw()
    token_ink(g,u,t,hold_start)

SCENES=(method,race)
def draw(g,i,t,duration):
    SCENES[i](g,phase(g,i,t,duration),t,duration)
