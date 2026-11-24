"""Act III: from an answer, to an intervention, to proof of an intervention.

Geometry keeps its job across changes of scale. The order becomes a test case,
the patch becomes an object that can be sampled, and the sampling tetrahedron
hands one of its cells to the lattice puzzle.
"""
from spatial import *
from pathlib import Path
from itertools import combinations
import json

NEUTRAL='#DDDDDD'
LATTICE='#454545'
DARK='#262626'
CX=(-2.25,0,2.25)
FEES=(8,8,0)
WANT=(8,0,0)
ORDER=(99,100,101)
CAM=((0,0,1),(-.13,.10,1.04),(.02,.11,.98),(.25,.18,1.01),
     (-.40,.23,1.04),(-.26,.19,1.00),(.075,.07,1.01),(0,0,1.0),
     (-.24,.17,.99),(0,0,1))
SCRIPT=json.loads(Path(__file__).with_suffix('.json').read_text())
HOLD=tuple(b.get('hold',.42) for b in SCRIPT)
PART_FRAME=(
    (0,.12,.27,.44,.60,.70,.86),
    (0,.22,.38,.54,.60,.66,.77,.87),
    (0,.11,.21,.34,.45,.58,.72,.84,.94),
    (0,.20,.44,.60,.77),
    (0,.16,.30,.40,.47,.58,.68,.79,.88),
    (0,.12,.23,.36,.48,.62,.74,.86),
    (0,.36,.66),
    (0,.12,.27,.40,.56,.66,.86),
    (0,.13,.23,.35,.47,.57,.69,.79,.89),
)

def a(u,l,r):return step(u,l,r)
def gone(u,l,r):return 1-a(u,l,r)
def window(u,l,r,s,t):return a(u,l,r)*gone(u,s,t)

def keypose(u,*knots):
    for (left,ka),(right,kb) in zip(knots,knots[1:]):
        if u<=right:return vlerp(ka,kb,a(u,left,right))
    return knots[-1][1]

def film_phase(g,i,t,duration):
    speech=g.speech if g.speech>0 else duration-HOLD[i]
    finish=clamp(speech/duration,.58,.997)
    x=clamp(t/duration)
    if x==0:return 0.
    if x>=finish:return 1.
    j0=y0=0.
    parts=PART_FRAME[i]
    words=[len(en.split()) for en,_ in SCRIPT[i]['parts']]
    for j,y in enumerate(parts[1:],1):
        pol=finish*sum(words[:j])/sum(words)
        jj=clamp(g.part(j,pol),j0+.002,finish-(len(parts)-j)*.002)
        if x<=jj:return mix(y0,y,(x-j0)/(jj-j0))
        j0,y0=jj,y
    return mix(y0,1,(x-j0)/(finish-j0))

def world(g,pose):
    return World(g,yaw=pose[0],pitch=pose[1],zoom=pose[2],distance=13)

def bez(p0,p1,p2,p3,q):
    q=clamp(q);f=1-q
    return add(add(mul(p0,f**3),mul(p1,3*f*f*q)),add(mul(p2,3*f*q*q),mul(p3,q**3)))

def stream(w,p0,p1,p2,p3,prog,opacity=1,c=MUTED,spark=GOLD):
    if opacity<=0:return
    w.curve(p0,p1,p2,p3,c,1.7,opacity*.75,progress=max(.03,prog),arrow=True)
    if .008<prog<.988:
        w.dot(bez(p0,p1,p2,p3,prog),spark,.056,opacity)

def receipt_card(w,p,k,alpha=1,high=False):
    c=GOLD if high else '#C7BBA2'
    w.paper(p,1.13,.72,c,alpha,fill=.82 if high else .67,cut=.17)
    w.text(str(k),add(p,(.032,.023,.061)),45,'#332814',alpha,font='math',weight='medium')
    w.segment(add(p,(-.31,-.219,.048)),add(p,(.365,-.219,.048)),
              '#3E3423',1.0,alpha*.49,dash=[2.5,3.2])

def order_tile(w,p,k,dims=(1.04,.64,.15),alpha=1,high=False):
    # In the runner an invoice becomes an indexed input, not a second postcard.
    color=GOLD if high else INK
    y=-dims[1]*.455
    w.text(str(k),add(p,(0,.020,.061)),41,color,alpha,font='math',weight='medium')
    w.segment(add(p,(-dims[0]*.40,y,.050)),add(p,(dims[0]*.40,y,.050)),
              color,1.39,alpha*.61)
    w.dot(add(p,(0,y,.061)),color,.032,alpha)

def fee(w,p,n,color,alpha=1,sz=1):
    # Equal-size sockets keep fee magnitude separate from pass/fail.
    w.disk(p,color,'',.228*sz,.061*sz,alpha=alpha,fill=.21)
    w.text(('+' if n else '')+str(n),add(p,(0,0,.048*sz)),30*sz,
           blend(color,INK,.30),alpha,font='math',weight='medium')

def packet(w,p,alpha=1,col=GOLD,s=.50,rot=(0,0,0),plain=False):
    w.tile(p,'',col,(s,s*1.27,.12),rot,alpha,fill=.42 if col==GOLD else .31)
    if alpha<.01:return
    R=rotation(tuple(rot))
    def f(x,y,z=.075):return add(p,trans((x*s,y*s,z),R))
    if plain:
        for j,L in enumerate((.28,.2,.26,.09)):
            yy=.22-.14*j
            w.segment(f(-.29,yy),f(L,yy),col,1.30,alpha*.64)
    else:
        w.segment(f(-.29,.19),f(-.11,.19),RED,1.85,alpha*.87)
        w.segment(f(-.04,.19),f(.24,.19),RED,1.45,alpha*.68)
        w.segment(f(-.29,-.16),f(-.11,-.16),GREEN,1.85,alpha*.87)
        w.segment(f(-.20,-.25),f(-.20,-.08),GREEN,1.85,alpha*.87)
        w.segment(f(-.04,-.16),f(.26,-.16),GREEN,1.45,alpha*.68)

# 1. A threshold is a plane, and an exact boundary case lands on it.
PATCH=(1.92,-1.40,.24)
YORDER=.69
YFEE=.04

def checkout_stage(w,u,opacity=1):
    if opacity<=0:return
    intro=a(u,0,.29)
    bmove=a(u,.21,.48)
    axis=a(u,.13,.26)
    w.path(((-4.04,-.45,0),(4.02,-.45,0)),MUTED,1.8,axis*opacity*.67,arrow=True)
    qplane=a(u,.14,.32)
    fence=[(0,-.45,-1.4),(0,1.56,-1.4),(0,1.56,1.07),(0,-.45,1.07)]
    w.face(fence,GOLD,qplane*opacity*.37,.22,1.45)
    w.segment((0,-.45,-1.4),(0,-.45,1.08),GOLD,2.1,qplane*opacity*.73)
    w.text('≥ 100',(0,1.88,-.15),30,GOLD,qplane*opacity,font='math')
    for j,x in enumerate(CX):
        reveal=a(u,(.215,.12,.25)[j],(.34,.23,.40)[j])
        cy=mix(0,YORDER,intro) if j==1 else YORDER
        z=.04 if j==1 else mix(-.65,.04,bmove)
        xx=x if j==1 else mix(x*.72,x,bmove)
        if j==1:
            w.tile((0,cy,z*intro),'',GOLD, (.96+.08*intro,.67-.03*intro,.14),alpha=(1-reveal)*opacity)
        receipt_card(w,(xx,cy,z),ORDER[j],reveal*opacity,high=(j==1))
        val=a(u,(.29,.43,.36)[j],(.37,.52,.44)[j])
        col=(MUTED,RED,GREEN)[j]
        w.segment((xx,cy-.34,z),(xx,YFEE+.20,z),col,1.4,val*opacity*.53)
        fee(w,(xx,YFEE,z+.015),FEES[j],col,val*opacity)
    vis=(a(u,.455,.53)*gone(u,.68,.81))*opacity
    end=(0,YFEE-.235,.11)
    w.curve((0,-.46,1.08),(0,-.39,.70),(0,-.28,.38),end,GOLD,1.79,vis,arrow=True)
    w.dot(end,GOLD,.027,vis)
    split=a(u,.48,.61)
    w.disk(vlerp((-2.45,0,0),(-2.93,-1.40,.05),split),BLUE,'A',.42,.15,
           alpha=opacity*gone(u,.80,.96))
    w.disk(vlerp((2.45,0,0),(2.93,-1.40,.05),split),PURPLE,'B',.42,.15,alpha=opacity)
    s=a(u,.585,.681)*gone(u,.88,.97)
    packet(w,vlerp((-2.93,-1.40,.10),(-1.91,-1.40,.23),s),s*opacity,BLUE,.48,plain=True)
    h=a(u,.705,.82)
    packet(w,vlerp((2.93,-1.40,.10),PATCH,h),h*opacity,GOLD,.58)
    e=a(u,.75,.85)*gone(u,.91,.99)
    w.text('>   →   ≥',(1.91,-2.03,.27),34,INK,e*opacity,font='math')

def checkout(g,u):
    p=keypose(u,(0,CAM[0]),(.18,(-.40,.18,1.04)),(.49,(-.34,.13,1.06)),
               (.74,CAM[1]),(1,CAM[1]))
    w=world(g,p);checkout_stage(w,u);w.draw()

BTEST=(0,1.71,.10)
TEST_PATCH=(0,-1.89,.25)

def test_stage(w,u,visibility=1):
    # Reuse the three price tiles. Their ideal outcomes sit deeper, the observed rows nearer.
    transi=a(u,.02,.23)*visibility
    checkout_stage(w,1,visibility*(1-a(u,.025,.23)))
    move=a(u,.018,.23)
    enter=a(u,.022,.165)
    receipt=a(u,.206,.305)
    repo=(0,-.07,-1.06)
    phases=(PATCH,(1.45,-1.40,.79),(.55,-.44,-.40),repo)
    patch=vlerp(bez(*phases,enter),TEST_PATCH,receipt)
    packet(w,patch,visibility*max(move,enter),GOLD,.58,
           rot=(.08*move+.39*math.sin(math.pi*enter),-.25*move-.30*math.sin(math.pi*enter),0))
    if .02<enter<.99:
        stream(w,*phases,enter,visibility*.78,MUTED,GOLD)
    fill=a(u,.073,.23)*visibility
    # Only the two depth rails and three paths are constructed. The y separation
    # is for reading; the depth still distinguishes specification and execution.
    for z,y in ((-.92,.207),(.78,-.609)):
        ends=((-3.02,y,z),(3.07,y,z))
        w.segment(*ends,MUTED,1.30,fill*.39)
        for dx in (-2.74,2.74):
            w.segment((dx,y-.055,z-.13),(dx,y-.055,z+.13),MUTED,1.22,fill*.36)
    w.disk(vlerp((2.93,-1.40,.05),BTEST,move),PURPLE,'B',.42,.15,alpha=transi)
    free=a(u,.23,.34)
    reg=a(u,.36,.48)
    expect=a(u,.46,.60)
    fix=a(u,.75,.84)
    ytop=1.02
    for j,x in enumerate(CX):
        fy=a(u,.13+j*.019,.29+j*.018)*visibility
        order_tile(w,vlerp((x,YORDER,.04),(x,ytop,-.22),move),ORDER[j],(.96,.51,.13),fy,(j==1))
        top=(x,.42,-.92); front=(x,-.39,.78)
        expose=(free if j==1 else reg)*visibility
        zeta=.96 if j==1 else .79
        start=(x,ytop-.27,-.22)
        v=norm(sub(top,start));b=norm(sub(front,top))
        w.segment(start,add(top,mul(v,-.27)),MUTED,1.36,expose*.63)
        w.path((add(top,mul(b,.263)),add(front,mul(b,-.27))),MUTED,1.43,expose*.59,arrow=True)
        fee(w,top,WANT[j],GOLD,expect*visibility,.81)
        fail_free=(j==0)
        fee(w,front,0,RED if fail_free else GREEN,expose*(1-fix),zeta*.99)
        fee(w,vlerp((x-.35,-.39,.78),front,fix),WANT[j],GREEN,expose*fix,zeta)
        markp=(x,-.98,.84)
        w.mark(markp,not fail_free,.14,expose*(1-fix))
        w.mark(markp,True,.14,expose*fix)
        if j==0 and expose:
            w.curve((0,-1.6,.25),(-1.3,-1.41,.40),(-2.25,-1.36,.57),(-2.25,-1.10,.82),
                    RED,1.65,expose*.62*(1-fix),progress=expose,arrow=True)
    if u>.15:
        trace=a(u,.25,.41)
        w.curve(TEST_PATCH,(2.0,-1.74,.52),(3.20,-.76,.77),(2.69,-.35,.76),
                GOLD,1.75,visibility*.68,progress=trace,arrow=True)
    a0=window(u,.21,.31,.70,.82)
    w.text('shipping = 0',(0,-2.42,0),27,INK,a0*visibility,font='math')
    a1=window(u,.74,.83,.91,.99)
    w.text('>   →   ≥',(0,-2.44,0),33,GOLD,a1*visibility,font='math')
    test=a(u,.876,.969)
    w.text('SWE-bench',(-3.78,-1.87,.10),34,INK,test*visibility)
    # A resolved target and the two still-good cases feed the same verdict.
    # Their actual outcomes travel, rather than just stamping a check over them.
    left=(-2.25,-.98,.84);middle=(0,-.98,.84);right=(2.25,-.98,.84)
    unchanged=(2.86,-1.48,1.15)
    repaired=(2.81,-.91,1.20)
    join=(3.66,-.71,1.16)
    lanes=(
      (middle,(.68,-.90,1.46),(1.66,-.98,1.29),repaired),
      (left,(-1.15,-1.57,1.19),(1.58,-1.67,1.46),unchanged),
      (right,(2.42,-1.07,1.32),(2.51,-1.45,1.29),unchanged),
    )
    for k,curve in enumerate(lanes):
        q=a(u,.868+k*.008,.933+k*.012)
        light=a(u,.857+k*.009,.89+k*.013)*visibility
        if q:
            stream(w,*curve,q,light*.91,GREEN,GREEN)
            if .02<q<.992:
                w.dot(bez(*curve,q),GREEN,.061,light)
    verdict=a(u,.934,.992)
    for k,p0 in enumerate((repaired,unchanged)):
        q=a(u,.932+k*.012,.976+k*.01)
        if q:
            p1=add(p0,(.28,.02,.17));p2=add(join,(-.56,-.16,.10))
            stream(w,p0,p1,p2,join,q,.91*verdict*visibility,GREEN,GREEN)
    mark=a(u,.965,.999)
    w.disk(join,GREEN,'',.282,.074,alpha=mark*visibility,fill=.19)
    w.mark(add(join,(0,0,.091)),True,.16,mark*visibility)

def tests(g,u):
    p=keypose(u,(0,CAM[1]),(.31,(-.37,.25,.99)),(.62,(-.29,.24,1.02)),
              (.89,CAM[2]),(1,CAM[2]))
    w=world(g,p);test_stage(w,u);w.draw()

# 2. Mirrors of the same purple model, only one of which has a tool loop.
CORES=((-2.1,.15,0),(2.1,.15,0))
TASKS=((-2.1,1.67,-.14),(2.1,1.67,-.14))
OUTS=((-2.1,-1.46,.14),(2.1,-1.46,.14))
STORE=(2.93,.81,-1.72)
RUNNER=(3.22,-.38,1.51)

def tool_unit(w,p,alpha=1,test=False):
    if test:
        w.box(p,(.88,.56,.49),MUTED,alpha,rot=(.07,-.18,0),fill=.36,edge=1.8)
        x,y,z=p
        for d,ok in ((-.17,False),(.17,True)):
            w.dot((x+d,y,z+.25),GREEN if ok else RED,.062,alpha)
    else:
        for k in range(3):
            w.box(add(p,(-k*.075,k*.085,-k*.115)),(.82,.55,.105),MUTED,alpha*(1-k*.16),
                  rot=(.08,-.16,0),fill=.19,edge=1.2)
        x,y,z=p
        for d in (-.12,0,.12):
            w.segment((x-.25,y+d,z+.07),(x+.18,y+d,z+.07),MUTED,1.25,alpha*.62)

def scaffold_stage(w,u,vis=1):
    enter=a(u,.00,.205)
    test_stage(w,1,vis*(1-a(u,.006,.17)))
    for j,p in enumerate(CORES):
        x,y,z=p; c=vlerp(BTEST,p,enter)
        swap=window(u,.713,.787,.839,.897) if j else 0
        w.disk(c,PURPLE,'B',.42,.22,alpha=enter*(1-swap)*vis)
        w.disk(c,BLUE,'A',.42,.22,alpha=enter*swap*vis)
        q=vlerp((0,1.67,-.14),TASKS[j],enter)
        w.tile(q,'',GOLD,(.72,.46,.13),alpha=enter*vis,fill=.34)
        w.path((add(q,(0,-.27,0)),(x,y+.44,z)),MUTED,1.65,enter*vis*.74,arrow=True)
        if enter>.14:
            w.dot(vlerp(add(q,(0,-.26,0)),(x,y+.44,z),enter),GOLD,.042,
                  math.sin(math.pi*enter)*vis)
        drawout=a(u,.11,.24) if j==0 else a(u,.40,.58)
        output=OUTS[j]
        p0=(x,y-.44,z);p1=(x,y-.75,z+.04);p2=add(output,(0,.64,0));p3=add(output,(0,.34,0))
        stream(w,p0,p1,p2,p3,drawout,drawout*vis)
        packet(w,vlerp(add(p,(0,-.57,.12)),output,drawout),drawout*vis,GOLD,.52)
        w.mark(add(output,(.45,-.02,.12)),j==1,.13,a(u,.42,.56)*drawout*vis*(1-swap*.77))
    tool=a(u,.198,.38)*vis
    tool_unit(w,STORE,tool)
    tool_unit(w,RUNNER,tool,test=True)
    R=CORES[1];f=(R[0]+.38,R[1]+.12,R[2]-.15)
    # Away into stored state, forward to execution, then back to the same core.
    stream(w,f,(2.34,.48,-.80),(2.54,.67,-1.48),add(STORE,(-.49,0,0)),
           a(u,.19,.34),tool,MUTED)
    stream(w,add(STORE,(.24,-.25,.04)),(4.16,.36,-1.26),(4.28,-.18,.62),RUNNER,
           a(u,.285,.448),tool,MUTED)
    feedback=(add(RUNNER,(-.40,-.04,0)),(2.56,-.99,1.37),(1.48,-.71,.83),
              add(R,(-.23,-.29,.10)))
    err=a(u,.34,.51)
    stream(w,*feedback,err,tool,MUTED,RED)
    if .014<err<.991:
        w.box(bez(*feedback,err),(.165,.165,.13),RED,tool,rot=(.26,.38+2*err,.13),fill=.68)
    meter=a(u,.926,.99)*vis
    for x in (-2.10,2.10):
        for k in range(4):
            w.box((x+(k-1.5)*.22,-2.19,-.04),(.14,.15,.18),GOLD,meter*.82,fill=.11)
        w.segment((x-.57,-2.33,-.08),(x+.57,-2.33,-.08),MUTED,1.3,meter*.52)

def scaffolds(g,u):
    p=keypose(u,(0,CAM[2]),(.20,(-.11,.19,1.02)),(.46,(.52,.27,1.01)),
              (.68,(.41,.22,1.02)),(.95,CAM[3]),(1,CAM[3]))
    w=world(g,p);scaffold_stage(w,u);w.draw()

# 3. The four attempts are points in space. Each bowed filament is one pair,
# whether the camera sees it in front of the mobile or behind it.
TET=((-1.66,-.84,.56),(1.66,-.84,.56),(0,1.35,.56),(.33,-.10,-2.22))
PAIRS=tuple(combinations(range(4),2))
GOOD=2
TET_CENTER=(0,.05,0)
BOW={
    (0,1):(0,-.48,.08),
    (0,2):(-.39,.11,.14),
    (1,2):(.39,.13,.09),
    (0,3):(-.34,.00,-.09),
    (1,3):(.32,-.17,-.24),
    (2,3):(.32,.23,-.13),
}

def vertices(center=TET_CENTER,scale=1.20):
    return tuple(add(center,mul(p,scale)) for p in TET)

def candidate_tile(w,p,j,alpha=1,scale=1,known=0,number=True,rot=(0,.1,0),correct=None):
    good=j==GOOD if correct is None else correct
    status=GREEN if good else RED
    ink=blend(GOLD,status,.55*known if good else .17*known)
    # The four discs stay the same size. The small attached test pin carries
    # the result, so highlighting the successful draw changes no weight.
    r=.239*scale
    w.disk(p,ink,'',r,.065*scale,rot=rot,alpha=alpha,fill=.19 if number else .33)
    if number:
        w.text(str(j+1),add(p,(0,0,.056*scale)),32*scale,INK,alpha,font='math',weight='medium')
    if known:
        stem=add(p,(.16*scale,.12*scale,.049*scale))
        bead=add(p,(.256*scale,.202*scale,.104*scale))
        w.segment(stem,bead,status,1.42*scale,known*alpha*.84)
        w.dot(bead,status,(.077 if good else .050)*scale,known*alpha)
        if good:
            w.dot(add(bead,(0,0,.006)),GREEN,.102*scale,known*alpha*.078)

def pair_color(ij,winners):
    return GREEN if any(j in winners for j in ij) else RED

def braided_edge(points,ij,scale=1):
    p,q=[points[j] for j in ij]
    v=norm(sub(q,p));trim=.274*scale
    p=add(p,mul(v,trim));q=add(q,mul(v,-trim))
    bend=mul(BOW[tuple(sorted(ij))],scale)
    return p,add(vlerp(p,q,.316),bend),add(vlerp(p,q,.692),bend),q

def filament(w,curve,col,alpha=1,width=2.,progress=1,halo=0):
    if halo:
        w.curve(*curve,col,width+3.0,alpha*halo*.18,progress=progress)
    w.curve(*curve,col,width,alpha,progress=progress)

def set_wire(w,points,ij,vis=1,version=0,scale=1,progress=1,wash=0):
    ok=GOOD in ij
    col=blend(MUTED,GREEN,.46*version) if ok else blend(MUTED,RED,.79*wash)
    filament(w,braided_edge(points,ij,scale),col,vis*(.78 if ok else .68),2.2 if ok else 1.65,
             progress=progress,halo=version*.37 if ok else 0)

def ratio_pair(w,p,up,down,alpha=1,size=39,top=GOLD,bottom=INK):
    x,y,z=p
    w.text(str(up),(x,y+.22,z),size,top,alpha,font='math',weight='medium')
    w.segment((x-.188,y,z),(x+.188,y,z),MUTED,1.70,alpha*.92)
    w.text(str(down),(x,y-.24,z),size,bottom,alpha,font='math')

def attempts_stage(w,u,opacity=1):
    scaffold_stage(w,1,opacity*gone(u,.016,.196))
    points=vertices()
    for j,p in enumerate(points):
        r=a(u,.035+j*.034,.17+j*.039)
        pos=vlerp(OUTS[1],p,r)
        alpha=r*opacity
        candidate_tile(w,pos,j,alpha,mix(.94,1.08,r),a(u,.277,.414),
                       rot=(.18*r,-.25*r+.06*j,.06*(j-1.5)*r))
        if r<.985:
            w.curve(OUTS[1],(1.99,-.72,.52),(1.32,.38,.16),pos,MUTED,1.2,
                    alpha*.60*(1-r),progress=1)
    rate=window(u,.426,.514,.60,.72)
    ratio_pair(w,(-3.11,-1.03,.36),1,4,rate*opacity)
    glow=a(u,.774,.925)
    for j,ij in enumerate(PAIRS):
        r=a(u,.56+j*.018,.74+j*.021)
        if r:
            set_wire(w,points,ij,opacity,glow,progress=r)

def attempts(g,u):
    p=keypose(u,(0,CAM[3]),(.30,(.29,.32,1.10)),(.46,(.34,.34,1.10)),
               (.77,CAM[4]),(1,CAM[4]))
    w=world(g,p);attempts_stage(w,u);w.draw()

def tiny_tetra(w,center,scale,winners,alpha):
    points=vertices(center,scale)
    for ij in PAIRS:
        filament(w,braided_edge(points,ij,.57),pair_color(ij,winners),alpha*.66,1.56)
    for j,p in enumerate(points):
        candidate_tile(w,p,j,alpha,.60,1,number=False,correct=j in winners)

def proof_stage(w,u,opacity=1):
    hits=((2,0),(2,1),(2,3))
    pooled=window(u,.59,.652,.735,.782)
    base=vertices((0,.05+.12*pooled,.17*pooled),1.20-.63*pooled)
    scale=1-.28*pooled
    miss=a(u,.155,.279)
    for j,p in enumerate(base):
        candidate_tile(w,p,j,opacity,scale*1.08,1,rot=(.18,-.25+.06*j,.06*(j-1.5)))
    for ij in PAIRS:
        set_wire(w,base,ij,opacity,1,scale,wash=miss)
    for k,ij in enumerate(hits):
        curve=braided_edge(base,ij,scale)
        s=a(u,.018+k*.023,.083+k*.025)
        if s:
            filament(w,curve,GREEN,opacity,2.86,progress=s,halo=.84)
        if .006<s<.992:
            w.dot(bez(*curve,s),GREEN,.068,opacity)
    mathcue=window(u,.235,.315,.596,.662)*opacity
    retry=window(u,.45,.518,.752,.82)
    ratio_pair(w,(-.64,-1.99,.47),3,6,mathcue,39,GREEN)
    w.text('=',(0,-1.99,.47),38,MUTED,mathcue,font='math')
    ratio_pair(w,(.66,-1.99,.47),1,2,mathcue,39,GOLD)
    w.text('pass@k',(-2.88,1.68,.19),31,INK,retry*opacity)
    if pooled>.002:
        left=(-3.12+.55*(1-pooled),.18,-.84)
        right=(3.12-.55*(1-pooled),.18,-.84)
        tiny_tetra(w,left,.49,{0,2},pooled*opacity)
        tiny_tetra(w,right,.49,{0,1,2},pooled*opacity)
        merge=a(u,.676,.747)
        for p,s in zip((left,(0,.13,.17),right),(5,3,6)):
            x,y,z=p
            bar(w,(mix(x,0,merge),mix(-1.14,-1.67,merge),mix(z,.33,merge)),
                mix(s,14/3,merge),pooled*opacity*(1-merge*.77),scale=.8)
        if merge:
            bar(w,(0,-1.67,.33),14/3,merge*pooled*opacity,scale=.91)
    choose=a(u,.86,.958)
    if choose:
        p=base[0];target=(3.19,-1.43,1.05)
        curve=(p,(-.91,-1.64,.88),(2.12,-1.54,1.21),target)
        w.curve(*curve,RED,1.78,choose*.63*opacity,progress=choose,arrow=True)
        x=bez(*curve,choose)
        candidate_tile(w,x,0,choose*opacity,1.18,a(u,.914,.97),rot=(.13,-.13,0))

def bar(w,p,success,alpha,scale=1):
    left=add(p,(-.72*scale,0,0));right=add(p,(.72*scale,0,0))
    w.segment(left,right,MUTED,1.7,alpha*.57)
    w.segment(left,vlerp(left,right,clamp(success/6)),GREEN,3.11,alpha)
    for j in range(6):
        q=vlerp(left,right,(j+.5)/6)
        w.dot(q,blend(MUTED,GREEN,clamp(success-j)),.031*scale,alpha)

def proof(g,u):
    p=keypose(u,(0,CAM[4]),(.26,(-.22,.10,1.10)),(.57,(-.14,.16,1.07)),
              (.72,(-.17,.26,.96)),(.89,CAM[5]),(1,CAM[5]))
    w=world(g,p);proof_stage(w,u);w.draw()

# 4. The evidence is now a lattice. A board is a solid thin plane; cells sit on its face.
DEMO=(
    (((1,1),(1,2)),(4,1),2),
    (((0,2),(1,2)),(4,2),2),
    (((0,1),(0,2),(1,2)),(5,2),3),
)
QUERY=(((0,0),(1,0),(0,1)),(3,0),1)
EXTRA=(((0,1),(0,2)),(5,1),4)
DROWS=(1.44,.00,-1.44)
DS=.315
DL=-1.49
DR=1.49

def board_cell(c,s,j,k,rot=0,depth=.10):
    return add(c,trans(((j-2.5)*s,(1.5-k)*s,depth),rotation((0,rot,0))))

def outline_cells(shape):
    # Oriented boundary of an edge-connected polyomino in grid coordinates.
    edges=set()
    for x,y in shape:
        r=((x,y),(x+1,y),(x+1,y+1),(x,y+1))
        for i in range(4):
            edge=(r[i],r[(i+1)%4])
            if edge[::-1] in edges:edges.remove(edge[::-1])
            else:edges.add(edge)
    nxt=dict(edges)
    start=min(nxt);cur=start;out=[]
    while True:
        out.append(cur);cur=nxt[cur]
        if cur==start:break
    simple=[]
    for i,b in enumerate(out):
        a0=out[i-1];c0=out[(i+1)%len(out)]
        left=(b[0]-a0[0],b[1]-a0[1]);right=(c0[0]-b[0],c0[1]-b[1])
        if left[0]*right[1]-left[1]*right[0]:simple.append(b)
    return simple

def silhouette(w,p,s,shape,shift,depth,vis,ghost=0):
    if vis<=0:return
    body=set(shape)
    contour=outline_cells(shape)
    rim=[]
    bevel=.055
    for i,(x,y) in enumerate(contour):
        xa,ya=contour[i-1];xb,yb=contour[(i+1)%len(contour)]
        sa=abs(x-xa)+abs(y-ya);sb=abs(xb-x)+abs(yb-y)
        ix=x-bevel*((y-ya)/sa+(yb-y)/sb)
        iy=y+bevel*((x-xa)/sa+(xb-x)/sb)
        rim.append(((ix+shift-3)*s,(2-iy)*s))
    if ghost:
        w.path(tuple(p(x,y,depth+.005) for x,y in (*rim,rim[0])),NEUTRAL,
               1.05,vis*.57,dash=[2.0,3.4])
        return
    dz=max(.023,.098*s)
    # Joint top, true boundary sidewalls. Shared edges leave no cube seams.
    for i,(x,y) in enumerate(rim):
        xx,yy=rim[(i+1)%len(rim)]
        p0,p1=p(x,y,depth),p(xx,yy,depth)
        q0,q1=p(x,y,depth-dz),p(xx,yy,depth-dz)
        n=cross(sub(p1,p0),sub(q0,p0))
        if dot(n,w.depth)>.0:
            w.face((p0,p1,q1,q0),NEUTRAL,vis*.93,fill=.30,edge=.53)
    for x,y in shape:
        v=(x+shift-2.5)*s;h=(1.5-y)*s
        left=v-(.504 if (x-1,y) in body else .445)*s
        right=v+(.504 if (x+1,y) in body else .445)*s
        top=h+(.504 if (x,y-1) in body else .445)*s
        bot=h-(.504 if (x,y+1) in body else .445)*s
        w.face((p(left,bot,depth),p(right,bot,depth),p(right,top,depth),p(left,top,depth)),
               NEUTRAL,vis,fill=.90,edge=0)
    w.path(tuple(p(x,y,depth+.007) for x,y in (*rim,rim[0])),INK,1.12,vis*.79)

def plate(w,c,s,data=None,shift=0,alpha=1,tiles=1,ghost=0,rot=0,depth=None):
    if alpha<=0:return
    depth=.033+.065*s if depth is None else depth
    M=rotation((0,rot,0))
    def p(x,y,d=depth/2+.007):return add(c,trans((x,y,d),M))
    width,height=6*s,4*s
    # Quiet tilework is cut into the base, not raised into another layer.
    edge='#424242'
    w.box(c,(width,height,depth),edge,alpha*.83,rot=(0,rot,0),fill=0,edge=.96)
    # Matte graphite rails: depth on the edges, barely-there lines on the face.
    for x,side in ((-width/2,1),(width/2,-1)):
        wall=(p(x,-height/2,depth/2),p(x,height/2,depth/2),
              p(x,height/2,-depth/2),p(x,-height/2,-depth/2))
        if dot(cross(sub(wall[1],wall[0]),sub(wall[2],wall[0])),w.depth)*side>0:
            w.face(wall,edge,alpha,fill=.41,edge=.54)
    seam=depth/2+.016
    for j in range(1,6):
        x=(j-3)*s
        w.segment(p(x,-height/2,seam),p(x,height/2,seam),edge,.92,alpha*.82)
    for k in range(1,4):
        y=(k-2)*s
        w.segment(p(-width/2,y,seam),p(width/2,y,seam),edge,.92,alpha*.82)
    if not data:return
    shape,(gx,gy),_=data
    contact_z=depth/2+.054
    brush=tiles*alpha
    loc=board_cell(c,s,gx,gy,rot,contact_z)
    w.tile(loc,'',GOLD,(s*.89,s*.89,.052),rot=(0,rot,0),alpha=brush,fill=.80)
    w.dot(add(loc,trans((0,0,.033),M)),'#30260a',s*.050,brush*.91)
    if ghost:
        silhouette(w,p,s,shape,0,contact_z+.048,brush*ghost*.62,ghost=1)
        if shift>.31:
            tx,ty=shape[0]
            q=(tx-2.5)*s;t=(1.5-ty)*s
            w.segment(p(q,t,contact_z+.051),p(q+shift*s,t,contact_z+.051),MUTED,
                      1.05,brush*ghost*.38,dash=[3,5])
    silhouette(w,p,s,shape,shift,contact_z+.041,brush)

def highlight_gap(w,p,s,alpha):
    x,y,z=p
    bits=.408*s;short=.142*s
    for sx,sy in ((-1,-1),(-1,1),(1,1),(1,-1)):
        q=(x+sx*bits,y+sy*bits,z+.009)
        w.path(((q[0]-sx*short,q[1],q[2]),q,(q[0],q[1]-sy*short,q[2])),
               RED,2.0,alpha)

def contact_mark(w,c,s,data,vis,rot=0):
    if vis<=0:return
    mx,my=data[1]
    p=board_cell(c,s,mx-.5,my,rot,.164)
    w.segment(add(p,(0,-s*.35,0)),add(p,(0,s*.35,0)),GOLD,3.26,vis*.27)
    w.segment(add(p,(0,-s*.22,0)),add(p,(0,s*.30,0)),GOLD,1.69,vis*.88)
    w.dot(add(p,(0,s*.27,.011)),GOLD,s*.054,vis)

def arc_link(w,L,R,s,opacity,trace=1,move=False):
    if opacity<=0:return
    v=norm(sub(R,L))
    P=add(L,mul(v,s*3+.10));Q=add(R,mul(v,-s*3-.10))
    if dot(sub(Q,P),v)<=0:
        P=add(L,(s*.73,-s*1.85,.11));Q=add(R,(-s*.73,-s*1.85,.11))
    C=add(vlerp(P,Q,.37),(0,.03,.12));D=add(vlerp(P,Q,.65),(0,.04,.12))
    stream(w,P,C,D,Q,trace,opacity,spatial_line(),GOLD) if move else w.curve(P,C,D,Q,MUTED,1.7,opacity*.70,progress=trace,arrow=True)

def spatial_line():return MUTED

def arc_examples(w,u,opacity=1):
    proof_stage(w,1,opacity*gone(u,.011,.161))
    expansion=a(u,.205,.401)
    lift=a(u,.424,.552)
    re_evaluate=window(u,.710,.754,.817,.871)
    for i,example in enumerate(DEMO):
        # First pair starts as a stack in depth; a camera turn uncovers both
        # surfaces before they fan out into a directly comparable elevation.
        if not i:
            y=mix(.13,DROWS[0],lift)
            L=(mix(-.16,DL,expansion),y,mix(-1.81,-.14,expansion))
            R=(mix(.16,DR,expansion),y,mix(1.83,.19,expansion))
            viv=a(u,.061,.201)
            output=a(u,.157,.236)
            shift=2*a(u,.337,.456)
            angle=mix(.08,0,expansion)
            tracks=window(u,.341,.381,.445,.469)*.65
        elif i==1:
            y=DROWS[i]
            L=(DL,y,mix(-1.90,-.14,a(u,.439,.515)))
            R=(DR,y,mix(-1.41,.19,a(u,.449,.530)))
            viv=a(u,.437,.532);output=a(u,.465,.547)
            shift=2*a(u,.495,.615)
            angle=0
            tracks=window(u,.494,.539,.614,.654)*.64
        else:
            y=DROWS[i]
            L=(DL,y,mix(-1.77,-.14,a(u,.575,.654)))
            R=(DR,y,mix(1.05,.19,a(u,.579,.661)))
            viv=a(u,.571,.669);output=a(u,.584,.655)
            shift=2*a(u,.601,.690)+a(u,.864,.954)
            angle=0
            tracks=window(u,.626,.682,.862,.951)*.70
        plate(w,L,DS,example,alpha=viv*opacity,rot=angle)
        plate(w,R,DS,example,shift,output*opacity,ghost=tracks,rot=angle)
        if not i:
            # Follow one gold face out of the candidate solid and down into
            # the first input lattice instead of changing the subject in place.
            joined=a(u,.028,.195)
            ride=window(u,.023,.058,.175,.224)*opacity
            if ride:
                end=board_cell(L,DS,*example[1],rot=angle)
                src=vertices()[2]
                flight=bez(src,(-.97,1.30,-.37),(-1.07,.04,-1.13),end,joined)
                s=mix(.52,DS*.88,joined)
                w.box(flight,(s,s,mix(.145,.08,joined)),GOLD,ride,
                      rot=(.17*(1-joined),.11+1.2*joined*(1-joined),.17*(1-joined)),
                      fill=.72,edge=1.59)
        march=(a(u,.117,.278) if not i else a(u,.436+i*.042,.49+i*.07))
        arc_link(w,L,R,DS,min(viv,output)*opacity,march,.02<march<.99)
        if i==2:
            red=window(u,.644,.714,.867,.941)
            ghost=window(u,.705,.750,.862,.928)
            gap=board_cell(R,DS,4,2,0,.159)
            highlight_gap(w,gap,DS,red*opacity)
            w.segment(add(gap,(0,-DS*.5,0)),add(gap,(0,-DS*.78,0)),RED,1.6,red*opacity)
            # Actual output is shown as a faint nearby hypothesis until the final slide.
            for j,k in example[0]:
                if (j+3,k) not in {(x+2,y) for x,y in example[0]}:
                    gp=board_cell(R,DS,j+3,k,0,.121)
                    w.box(gp,(DS*.86,DS*.86,.05),NEUTRAL,ghost*opacity*.54,fill=0,edge=1.4)
        contact_mark(w,R,DS,example,
                     (a(u,.932,.985) if i==2 else max(a(u,.932,.985),re_evaluate))*opacity,angle)
    bias=window(u,.475,.53,.675,.725)
    w.text('+2',(0,.24,.52),33,GOLD,bias*opacity,font='math')

def grids(g,u):
    p=keypose(u,(0,CAM[5]),(.19,(-.68,.28,1.07)),(.33,(-.74,.20,1.08)),
               (.53,(-.24,.17,1.04)),(.76,(.10,.12,1.02)),(1,CAM[6]))
    w=world(g,p);arc_examples(w,u);w.draw()

QL=(-1.94,-.34,.30)
QR=(1.94,-.34,.52)
QS=.514

def mini_demos(w,amount=1,alpha=1):
    # Preserve all six boards and their ordering as they recede into context.
    for i,dat in enumerate(DEMO):
        xmain=(-3.44,0,3.44)[i]
        L=vlerp((DL,DROWS[i],-.14),(xmain-.73,1.57,-.70),amount)
        R=vlerp((DR,DROWS[i],.19),(xmain+.73,1.57,-.43),amount)
        s=mix(DS,.181,amount)
        plate(w,L,s,dat,alpha=alpha)
        plate(w,R,s,dat,dat[-1],alpha)
        arc_link(w,L,R,s,alpha)
        contact_mark(w,R,s,dat,alpha*gone(amount,.05,.98))

def mystery_stage(w,u,opacity=1):
    hint=a(u,.023,.402)
    mini_demos(w,hint,opacity*mix(1,.58,hint))
    influx=a(u,.152,.435)
    pull=(0,-.21,-1.88)
    ll=vlerp(pull,QL,influx); rr=vlerp(pull,QR,influx)
    s=mix(.237,QS,influx)
    plate(w,ll,s,QUERY,alpha=influx*opacity)
    plate(w,rr,s,alpha=influx*opacity*.82)
    arc_link(w,ll,rr,s,influx*opacity)
    qt=a(u,.562,.706)*opacity
    w.text('?',add(QR,(0,0,.10)),52,MUTED,qt)

def mystery(g,u):
    p=keypose(u,(0,CAM[6]),(.29,(-.19,.14,1.03)),(.64,CAM[7]),(1,CAM[7]))
    w=world(g,p);mystery_stage(w,u);w.draw()

EVIDENCE_C=(0,-1.17,.69)
EVIDENCE_S=.258

def rule_stamp(w,p,j,vis=1):
    if j==0:
        w.path((add(p,(-.47,0,0)),add(p,(.14,0,0))),MUTED,1.90,vis,arrow=True)
        w.text('2',add(p,(.38,0,.03)),30,INK,vis,font='math')
    else:
        o=(-.44 if j==2 else -.20)
        w.box(add(p,(o,0,.04)),(.258,.258,.08),NEUTRAL,vis,fill=.64)
        w.box(add(p,(o+.278,0,.04)),(.258,.258,.08),GOLD,vis,fill=.68)
        if j==2:w.text('≤ 3',add(p,(.30,0,.025)),29,INK,vis,font='math')

def search_stage(w,u,opacity=1):
    center=a(u,.294,.465)
    vis=opacity*(1-center)
    mini_demos(w,1,vis*.58)
    answer=a(u,.003,.066)
    move=a(u,.029,.111)
    plate(w,QL,QS,QUERY,alpha=vis)
    plate(w,QR,QS,QUERY,move,vis*mix(.82,1,answer),tiles=answer,
          ghost=window(u,.027,.057,.126,.182)*.82)
    arc_link(w,QL,QR,QS,vis)
    w.text('?',add(QR,(0,0,.10)),52,MUTED,vis*(1-answer))
    contact_mark(w,QR,QS,QUERY,a(u,.116,.186)*vis)
    grade=a(u,.225,.347)
    if grade:
        # Trace the actual checked boundary rather than floating a verdict.
        width,height=6*QS/2,4*QS/2
        frame=((width,height),(width,-height),(-width,-height),(-width,height),(width,height))
        w.path(tuple(add(QR,(x,y,.085)) for x,y in frame),GREEN,2.0,grade*vis*.74,progress=grade)
        w.mark(add(QR,(1.82,0,.10)),True,.15,grade*vis)
    if center<.002:return
    xlist=(-2.85,0,2.85)
    join=(0,1.57,-.59)
    w.tile(join,'',GOLD,(.55,.43,.16),alpha=center*opacity,fill=.35)
    for j,x0 in enumerate(xlist):
        z=(-.84,.60,-.37)[j]
        dest=(x0,.59,z)
        lev=a(u,.346+j*.025,.429+j*.025)
        p=vlerp(join,dest,lev)
        path=(join,(.44*x0,1.45,-.58),(.86*x0,1.06,z-.13),add(p,(0,.27,0)))
        stream(w,*path,lev,lev*center*opacity,MUTED)
        rule_stamp(w,p,j,lev*center*opacity)
        for k,ex in enumerate(DEMO):
            pin=a(u,.408+.034*k+j*.012,.482+.040*k+j*.013)
            ok=j>0 or k<2
            v=(x0+(k-1)*.24,.138,z+.08)
            w.dot(v,GREEN if ok else RED,.050,opacity*pin)
        w.mark((x0,-.18,z),j>0,.14,opacity*a(u,.514+j*.015,.57+j*.028))
        feel=a(u,.676,.806)
        if j>0 and feel:
            c=(x0,EVIDENCE_C[1],z+.09)
            k=4 if j==1 else 3
            sh=k*a(u,.689+j*.026,.824+j*.016)
            plate(w,c,EVIDENCE_S,EXTRA,sh,feel*opacity,ghost=window(u,.706,.747,.836,.901)*.62)
            verdict=a(u,.829+j*.013,.875+j*.010)*opacity
            w.mark(add(c,(.98,0,.10)),j==1,.128,verdict)
            if j==1:contact_mark(w,c,EVIDENCE_S,EXTRA,a(u,.841,.897)*opacity)
            if j==2:
                gap=board_cell(c,EVIDENCE_S,4,1,depth=.131)
                highlight_gap(w,gap,EVIDENCE_S,verdict)
        # Spend another turn on the bounded rule; old evidence does not change.
        if j==2:
            again=a(u,.861,.97)
            if .01<again<.997:
                p0=(x0+.50,.65,z-.08);p1=(x0+1.01,1.13,z-.88)
                p2=(x0-.40,1.18,z-.67);p3=(x0-.63,.64,z-.09)
                stream(w,p0,p1,p2,p3,again,opacity*.63,GOLD,GOLD)

def search(g,u):
    p=keypose(u,(0,CAM[7]),(.25,(0,0,1)),(.48,(-.48,.23,1.01)),
               (.75,(-.54,.21,1)),(.93,CAM[8]),(1,CAM[8]))
    w=world(g,p);search_stage(w,u);w.draw()

# 5. Ordinary utility and protected access are two separate observations.
T_REQ=((-3.15,.85,-.65),(-3.15,-.78,.40))
T_OUT=((2.87,.85,-.65),(2.87,-.78,.40))

def clock_icon(w,p,alpha,c=GOLD):
    if alpha<=0:return
    w.disk(p,c,'',.208,.047,alpha=alpha,fill=.10)
    x,y,z=p
    w.path(((x,y+.115,z+.033),(x,y,z+.035),(x+.098,y-.064,z+.035)),
           c,1.57,alpha)
    w.dot((x,y,z+.043),c,.020,alpha)

def lock_icon(w,p,alpha,c=GOLD):
    if alpha<=0:return
    x,y,z=p
    w.box((x,y-.062,z),(.31,.24,.061),c,alpha,fill=.21,edge=1.35)
    pts=tuple((x+.107*math.cos(k*math.pi/10),y+.048+.13*math.sin(k*math.pi/10),z+.045)
               for k in range(11))
    w.path(pts,c,1.45,alpha)
    w.dot((x,y-.061,z+.034),c,.019,alpha)

def shutters(w,p,alpha,col):
    if alpha<=0:return
    x,y,z=p
    for q in (-1,1):
        w.box((x+q*.17,y,z),(.295,.37,.105),col,alpha,fill=.18,edge=1.25)
        w.dot((x+q*.073,y,z+.058),col,.015,alpha)

def response(w,p,j,alpha,col=GREEN):
    if alpha<=0:return
    x,y,z=p
    w.tile(p,'',col,(1.38,.65,.13),alpha=alpha,fill=.19)
    if j==0:
        clock_icon(w,(x-.36,y,z+.086),alpha,col)
        w.text('19:30',(x+.21,y,z+.082),32,INK,alpha,font='math')
    else:packet(w,(x,y,z+.084),alpha,col,.37,rot=(0,0,-.13),plain=True)

def reject_station(w,p,alpha,ok):
    if alpha<=0:return
    x,y,z=p
    c=GREEN if ok else RED
    shutters(w,(x,y,z+.13),alpha,c)
    w.mark((x+.63,y,z+.116),ok,.14,alpha)

def outcome_samples(w,p,which,vis):
    if vis<=0:return
    # Small controlled, invented counts, kept as individual outputs.
    misses=(2,) if not which else (1,4)
    x,y,z=p
    for j in range(6):
        q=(x+(j-2.5)*.30,y,z+.055*(j%2))
        c=RED if j in misses else GREEN
        w.box(q,(.216,.225,.11),c,vis,fill=.44,edge=1.13)
    w.segment((x-.95,y-.21,z),(x+.95,y-.21,z),MUTED,1.24,vis*.59)

def theater_stage(w,u):
    advance=a(u,0,.145)
    search_stage(w,1,1-advance)
    join=a(u,.017,.165)
    origin=board_cell(EVIDENCE_C,EVIDENCE_S,*EXTRA[1],depth=.10)
    carry=gone(u,.12,.212)*window(u,0,.024,.90,.92)
    incoming=bez(origin,(.15,-.65,1.07),(-1.49,.51,.58),T_REQ[0],join)
    if carry:
        w.tile(incoming,'',GOLD,(mix(.22,.79,join),mix(.22,.59,join),.11),alpha=carry,fill=.62)
    exit_now=a(u,.790,.953)
    base=1-exit_now
    bpos=vlerp((-.04,.44,-1.07),(0,.04,.06),a(u,.064,.203))
    w.disk(bpos,PURPLE,'B',.42,.21,alpha=base*a(u,.049,.188)*gone(u,.561,.722))
    all_closed=a(u,.317,.441)
    measure=a(u,.465,.599)
    for j,(request,outcome) in enumerate(zip(T_REQ,T_OUT)):
        show=a(u,.11+j*.085,.216+j*.087)*base
        # Curved paths live at genuinely different depths, one of which
        # comes in front of the model and one behind it.
        x,y,z=request
        w.tile(request,'',GOLD,(1.0,.67,.17),alpha=show*gone(u,.489,.671),fill=.32)
        ico=clock_icon if not j else lock_icon
        ico((w),(x,y,z+.121),show*gone(u,.488,.655))
        m=(bpos[0]-.40,bpos[1]+(j*-.18+.10),bpos[2]-.02+j*.21)
        q=a(u,.142+j*.085,.251+j*.055)
        stream(w,add(request,(.54,0,0)),(-1.96,y,z),(m[0]-.42,m[1]+.10,z),m,
               q,show*gone(u,.45,.56),MUTED,GOLD)
        rx,ry,rz=outcome
        p0=(bpos[0]+.44,bpos[1]+(.11 if j==0 else -.11),bpos[2]+.02+j*.18)
        p3=(rx-.74,ry,rz)
        out=a(u,.217+j*.068,.335+j*.037)
        stream(w,p0,(.96,p0[1]+.14,rz),(.93+1.26,ry,rz),p3,out,
               out*show*gone(u,.47,.585),MUTED)
        normal=out*base*(1-all_closed)*gone(u,.44,.61)
        response(w,outcome,j,normal)
        w.mark(add(outcome,(.94,0,.09)),True,.127,normal)
        gate=out*base*all_closed*gone(u,.463,.605)
        shut=vlerp(add(outcome,(0,.68,0)),outcome,all_closed)
        reject_station(w,shut,gate,j==1)
    metric_y=.015
    harm=(-2.10,.11,-.56)
    util=(2.11,-.29,.53)
    part2=a(u,.668,.776)
    harm_a=measure*base
    w.text('HarmBench',(harm[0],harm[1]+1.46,harm[2]),34,INK,harm_a*gone(u,.799,.884))
    # The left probe judges generated items. The right independently tests
    # normal requests; a protected item is never the definition of harm.
    for j,p in enumerate((harm,util)):
        vr=(harm_a if not j else part2*base)
        x,y,z=p
        origin=(x,y+.35,z-.61)
        end=(x,y,z)
        w.path((origin,vlerp(origin,end,.9),end),MUTED,1.4,vr*.62,arrow=True)
        outcome_samples(w,end,j,vr)
        gate=window(u,.566,.627,.702,.774)*base
        if not j:packet(w,(x,y-.63,z+.11),gate,RED,.30,rot=(0,0,.13),plain=True)
        else:lock_icon(w,(x,y-.71,z+.12),gate*.76,MUTED)
    green=a(u,.774,.841)
    for j,endpoint in enumerate(((-2.45,0,0),(2.45,0,0))):
        p=vlerp((harm,util)[j],endpoint,exit_now)
        w.dot(p,GREEN,.134,green*base*.83)
    q=vlerp(incoming,(0,0,0),exit_now)
    if exit_now:
        carry_mid=window(u,.786,.834,.899,.966)
        w.tile(q,'',GOLD,(mix(.48,.96,exit_now),mix(.43,.67,exit_now),.14),
               alpha=carry_mid,fill=.43)
    w.anchor(exit_now)

def theater(g,u):
    p=keypose(u,(0,CAM[8]),(.19,(-.46,.22,1.02)),(.38,(-.28,.16,1.03)),
               (.61,(.31,.23,1.06)),(.79,(.20,.12,1.02)),(.97,CAM[9]),(1,CAM[9]))
    w=world(g,p);theater_stage(w,u);w.draw()

SCENES=(checkout,tests,scaffolds,attempts,proof,grids,mystery,search,theater)

def draw(g,i,t,duration):
    SCENES[i](g,film_phase(g,i,t,duration))
