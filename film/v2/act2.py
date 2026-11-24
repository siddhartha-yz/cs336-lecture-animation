"""Act II. The same exam slip moves from a score ceiling to a decision about the calendar."""
from math import pi, sin, cos, exp
from pathlib import Path
import json
from spatial import *

CAM_HOME=(0,0,1,(0,0,0))
CAM_QUIZ=(.25,.18,.98,(0,.37,0))
CAM_QUIZ_END=(.035,.123,1.04,(0,.41,0))
CAM_CHOICE=(0,.27,1.02,(0,.31,0))
CAM_CHOICE_END=(0,.43,1.02,(0,.33,0))
CAM_EXPERT=(-.22,.16,.98,(0,.33,0))
CAM_PAIR=(.10,.12,.98,(0,.20,0))
CAM_NETWORK=(.36,.43,.99,(0,.09,0))
CAM_SCORE=(0,.10,1.00,(0,.19,0))
CAM_JUDGE=(.05,.205,.94,(0,.28,0))
CAM_JUDGE_NEAR=(.032,.225,1.075,(.02,.20,.16))
CAM_CHART=(0,.07,.98,(0,.31,0))
CAM_CHART_DEPTH=(.31,.21,.91,(0,.39,0))
CAM_CAL=(.20,.16,.99,(0,.31,0))


def stage(u,a,b,c,d):
    return step(u,a,b)*(1-step(u,c,d))


def camera(g,a=CAM_HOME,b=None,u=0):
    b=b or a
    return World(g,yaw=mix(a[0],b[0],u),pitch=mix(a[1],b[1],u),zoom=mix(a[2],b[2],u),
                 target=vlerp(a[3],b[3],u))


def cam_mix(a,b,u):
    return (mix(a[0],b[0],u),mix(a[1],b[1],u),mix(a[2],b[2],u),vlerp(a[3],b[3],u))


def cubic(p0,p1,p2,p3,q):
    p=1-q
    return tuple(p**3*a+3*p*p*q*b+3*p*q*q*c+q**3*d for a,b,c,d in zip(p0,p1,p2,p3))


def brush(w,points,c=MUTED,alpha=1,lo=.8,hi=2.8,progress=1):
    """A tapered pen mark, in world space so it follows an actual trace."""
    if alpha<=0 or progress<=0:
        return
    n=len(points)-1
    m=min(n,max(1,int(n*progress+.999)))
    for j in range(m):
        a,b=points[j],vlerp(points[j],points[j+1],clamp(progress*n-j))
        t=(j+.5)/n
        pressure=sin(pi*t)**.72
        w.segment(a,b,c,mix(lo,hi,pressure),alpha*(.50+.50*pressure))


def ribbon(w,p0,p1,p2,p3,c=MUTED,alpha=1,lo=.75,hi=2.4,progress=1,n=16):
    brush(w,[cubic(p0,p1,p2,p3,j/n) for j in range(n+1)],c,alpha,lo,hi,progress)


def fly(w,p0,p1,p2,p3,u,color=GOLD,r=.10,alpha=1):
    if alpha<=0 or u<=0:
        return
    ribbon(w,p0,p1,p2,p3,color,alpha*.65,.8,2.25,u)
    w.dot(cubic(p0,p1,p2,p3,u),color,r,alpha)


def branch(w,p,q,n,c=MUTED,alpha=1):
    y=(p[1]+q[1])/2
    ribbon(w,p,(p[0],y,p[2]),(q[0],y,q[2]),q,c,alpha,.75,2.65,n)


def local(p,angle=(0,0,0)):
    m=rotation(angle)
    def f(x,y,z=0):
        return add(p,trans((x,y,z),m))
    return f


def sketch(w,loc,pts,c,a,lo=.82,hi=1.7,progress=1):
    brush(w,[loc(*v) for v in pts],c,a,lo,hi,progress)


def bottom_ticks(w,p0,p1,c=MUTED,alpha=1,width=1.15,h=.08):
    for p in (p0,p1):
        w.segment((p[0],p[1]-h,p[2]),(p[0],p[1]+h,p[2]),c,width,alpha)
    w.segment(p0,p1,c,width,alpha)


def sheet(w,p,c=MUTED,s=1,angle=(0,0,0),alpha=1,image=0,ink=1):
    """A folded folio: a stable document silhouette even at icon scale."""
    if alpha<=0 or s<=0:
        return
    m=local(p,angle)
    def f(x,y,z=0):return m(x*s,y*s,z*s)
    outline=((-0.59,-.74),(.59,-.74),(.60,.49),(.35,.75),(-.59,.75))
    w.face([f(x,y,-.035) for x,y in outline],c,alpha*.85,.19,1.13)
    w.face([f(x,y,.029) for x,y in outline],c,alpha,.225,1.13)
    w.face((f(.35,.75,.034),f(.35,.49,.034),f(.60,.49,.034)),c,alpha*.91,.39,1.12)
    w.path((f(-.39,-.61,.044),f(-.39,-.08,.044),f(-.39,.62,.044)),c,.87,alpha*.37)
    for j,span in enumerate((.54,.66,.41)):
        y=.43-.157*j
        w.curve(f(-.25,y,.047),f(-.14,y+.013,.047),f(-.09+span*.7,y-.011,.047),
                f(-.25+span,y,.047),c,1.2+min(1.,s),alpha*ink*(.71-.12*j))
    if image:
        coords=[f(x,y,.050) for x,y in ((-.275,-.57),(.43,-.57),(.43,-.09),(-.275,-.09),(-.275,-.57))]
        w.path(coords,c,1.12,image*alpha*.77)
        w.path([f(x,y,.052) for x,y in ((-.23,-.49),(-.06,-.24),(.11,-.45),(.26,-.22),(.39,-.45))],
               c,1.8,image*alpha*.96)
        w.dot(f(.316,-.204,.054),GOLD,.033*s,image*alpha)


def question(w,p,a=1,t=1):
    """Pen writes a naked formula while the source tile opens into a binding."""
    if a<=0:
        return
    x,y,z=p
    if t<1:
        w.tile(p,'',GOLD,(mix(.96,2.27,t),mix(.67,.49,t),.14),alpha=a*(1-t),fill=.33)
    if t:
        w.text('3 + 4 = ?', (x,y,z+.16),57,GOLD,a*t,font='math')
        p0=(x-1.13,y-.34,z+.15); p3=(x+1.16,y-.31,z+.15)
        ribbon(w,p0,(x-.63,y-.42,z+.16),(x+.57,y-.30,z+.154),p3,
               GOLD,a*t*.76,.86,2.21,step(t,.24,1))


def _exam(w,u,leave=0):
    expand=step(u,.015,.19)
    miss=step(u,.56,.76)
    s=1-leave
    # This common slab sits directly above both score stacks. Its thickness
    # and rear face become legible only as the camera rises.
    slab=step(u,.26,.47)
    if slab and leave<1:
        drop=step(leave,.24,1)
        sp=(0,mix(1.215,-.67,drop),.12*drop)
        slab_size=(mix(7.64,8.,drop),.083,mix(1.63,1.31,drop))
        w.box(sp,slab_size,blend(GOLD,MUTED,drop),slab*mix(.93,.76,drop),
              fill=mix(.16,.10,drop),edge=1.47)
        if drop<1:
            rim=slab*(1-drop)*.94
            x0,x1=-3.82,3.82
            yy=sp[1]+.042
            z=sp[2]+slab_size[2]/2+.007
            w.segment((x0,yy,z),(x1,yy,z),GOLD,2.39,rim)
            for j,xv in enumerate((-3.24,0,3.24)):
                w.segment((xv,yy+.026,z),(xv,yy-.155,z),GOLD,1.42,rim*(1 if j==1 else .58))
        w.text('10',(-.02,1.38,.975),31,GOLD,slab*s*s,font='math')
    y=mix(0,1.99,expand)
    if s:
        question(w,(0,y,-.16*expand),s,expand)
    for side,(c,loss) in enumerate(((BLUE,3),(PURPLE,1))):
        sign=2*side-1
        x=sign*mix(2.45,6.13,step(leave,0,.90))
        f=step(u,.125,.24)
        label='A' if side==0 else 'B'
        w.disk((x,mix(0,-1.50,expand),mix(0,-.72,leave)),c,label,
               r=mix(.42,.34,expand),alpha=1-.91*leave)
        # Dark binding boards and side punches make these scored pages, not bars.
        # A scored stack keeps the spacing of its ten paper strips, without
        # specular faces: flat ink on the front, a faint fold only at the edge.
        a0=f*s*.86
        w.face(((x-.88,-.974,-.48),(x+.88,-.974,-.48),
                (x+.88,-.974,.61),(x-.88,-.974,.61)),c,a0,.23,1.04)
        w.segment((x-.84,-.971,.621),(x+.84,-.971,.621),c,1.61,a0*.65)
        for j in range(10):
            ready=step(u,.087+.026*side+.023*j,.16+.025*side+.024*j)
            if not ready and not leave:
                continue
            height=-.856+.217*j
            z=mix(-.75,0,ready)
            kicked=step(miss,.05+(9-j)*.10,.76+(9-j)*.11) if j>=10-loss else 0
            jitter=(sin(j*2.42+side)*.036)*(1-kicked)
            pos=(x+sign*1.22*kicked+jitter,height-1.05*kicked*kicked,z+1.47*kicked)
            col=blend(c,RED,kicked*.92)
            ang=(kicked*.66,kicked*.21*sign,kicked*sign*.12)
            a=ready*s*(1-.70*kicked)
            m=local(pos,ang)
            front=((-0.691,-.076,.41),(.684,-.071,.41),(.694,.076,.407),
                   (.62,.080,.407),(-.674,.076,.412))
            w.face([m(*q) for q in front],col,a,.56+.04*(j%3),.96)
            w.face((m(-.674,.076,.412),m(.694,.076,.407),
                    m(.67,.079,-.418),m(-.671,.077,-.412)),col,a,.24,.77)
            w.segment(m(-.573,.031,.417),m(.530,.033,.417),col,1.26,a*.58)
            w.dot(m(-.511,-.025,.426),col,.025,a*.67)
        before=(1-step(u,.58,.70))*step(u,.34+side*.03,.43+side*.03)*s
        if before:
            w.text('10 / 10',(x,-2.02,.78),39,c,before,font='math')
        after=step(u,.64,.79)*s
        if after:
            w.text(f'{10-loss} / 10',(x,-2.02,.78),39,c,after,font='math')
            w.mark((x+1.05,-.856+.217*(9-loss),.49),True,.14,after*.84)
    if u>.729 and leave<1:
        vv=step(u,.735,.984)
        fade=1-step(leave,.005,.34)
        top_y_a=-.856+.217*6+.082
        top_y_b=-.856+.217*8+.082
        for j,(y0,x,c) in enumerate(((top_y_a,-2.45,BLUE),(top_y_b,2.45,PURPLE))):
            p=(x+(.653 if j==0 else -.653),y0,.71)
            q=(0,y0,.71)
            w.path([p,q],c,1.45,fade*vv*.79,dash=[5,6],progress=step(vv,.037+.15*j,.55+.15*j))
        compare=step(vv,.51,.93)
        if compare:
            w.segment((0,top_y_a,.72),(0,mix(top_y_a,top_y_b,compare),.72),
                      GOLD,1.9,fade*compare*.91)
            for j,y0 in enumerate((top_y_a,top_y_b)):
                w.segment((-.060,y0,.72),(.060,y0,.72),GOLD,1.58,fade*compare*(1 if j==0 else compare))


def exam_scene(g,u):
    c=cam_mix(CAM_HOME,CAM_QUIZ,step(u,.03,.40))
    w=camera(g,c,CAM_QUIZ_END,step(u,.753,.982))
    if u<=1e-6:
        w.anchor()
    else:
        _exam(w,u)
    w.draw()


def _choice(w,e,alpha=1,depart=0,stand=1,joined=1):
    """Lottery width is genuinely an area on the same floor—not a bar label."""
    if not alpha:
        return
    s=1-depart
    under=step(joined,.24,1)
    yfloor=mix(1.215,-.67,under)
    zfloor=.12*under
    visible=step(joined,.43,1)
    x0=-4.0
    width=8.0
    h=.081
    # Old 4-stripe seat positions slide right as six places are made on the left.
    for j in range(10):
        old=-3+2*(j-6)
        new=x0+(j+.5)*width/10
        if j>=6:
            x=mix(old,new,e)
            p=1
        else:
            x=new
            after=clamp((mix(-3,1.2,e)-x-.56)/.21)
            # The last new tile has precisely one final pitch of clearance.
            p=step(e,.08+.059*j,.28+.102*j)*ease(after)
        yy=.30+(.25*(1-p))
        aa=alpha*s*p*visible
        if j==7 and aa:
            # An isolated wax-colored answer marker; the other numerals are simply ink.
            w.disk((x,yy,.53),GOLD,'7',.245,.105,
                   rot=(.16,0,-.055),alpha=aa,fill=.63,label_size=37)
        else:
            w.text(str(j),(x,yy,.545),37,MUTED,aa*.92,font='math')
            w.segment((x,yy-.24,.545),(x,yy-.31,.545),MUTED,1.5,aa*.66)
    w.box((0,-.67,.12),(width,h,1.31),MUTED,alpha*s*.76*stand,fill=.10,edge=1.4)
    goldx=mix(-1,2,e)
    goldw=mix(2,.8,e)
    w.box((goldx,yfloor+.052,zfloor),(goldw,.055,1.31),GOLD,
          alpha*s*step(joined,.38,1),fill=.70,edge=1.45)
    seams=alpha*s*step(joined,.40,1)
    w.segment((-4,yfloor+.046,zfloor+.663),(4,yfloor+.046,zfloor+.663),
              MUTED,2.25,seams*.82)
    for n,k in ((4,1-e),(10,e)):
        for j in range(1,n):
            x=x0+j*width/n
            w.segment((x,yfloor+.057,zfloor-.655),(x,yfloor+.057,zfloor+.655),
                      MUTED,1.02,k*alpha*s*step(joined,.44,1)*.64)
            w.segment((x,yfloor+.050,zfloor+.664),(x,yfloor-.017,zfloor+.664),
                      MUTED,1.62,k*seams*.86)
    x7=mix(-1,2,e)
    w.segment((x7,-.56,.61),(x7,-.016,.56),GOLD,1.5,alpha*s*visible*.77,dash=[4,5])
    w.text('1 / 4',(-1,-1.25,.86),43,GOLD,alpha*s*step(joined,.72,1)*(1-step(e,0,.38)),font='math')
    w.text('1 / 10',(2,-1.25,.86),43,GOLD,alpha*s*step(e,.55,1),font='math')
    y=mix(1.99,1.78,depart)
    question(w,(0,y,-.16),alpha,1)


def choice_scene(g,u):
    join=step(u,0,.15)
    c=cam_mix(CAM_QUIZ_END,CAM_CHOICE,join)
    closer=step(u,.685,.977)
    w=camera(g,c,CAM_CHOICE_END,closer)
    if join<1:
        _exam(w,1,join)
    e=step(u,.39,.69)
    _choice(w,e,join,stand=step(join,.95,1),joined=join)
    # Fly the unchanged correct choice down into its smaller equal-area slot.
    p=step(u,.682,.856)
    a=stage(u,.673,.726,.90,.998)
    if a:
        fly(w,(2,.23,.64),(2,-.09,.70),(2,-.35,.63),(2,-.548,.64),
            p,GOLD,.077,a*.92)
        ratio=step(u,.806,.892)
        w.segment((1.61,-.533,.779),(mix(1.61,2.39,ratio),-.533,.779),GOLD,2.08,a*ratio*.86)
    w.draw()


TASK="Cancel today's appointment."
RESP_A="Let's cancel today."
RESP_B='Cancel today. Another day?'
LEFT=(-2.50,-.05,.45)
RIGHT=(2.50,-.05,.45)
JUDGE=(0,.835,-.72)
VOTE1=(-2.50,-.91,.62)
VOTE2=(2.50,-.91,.62)
TASKPOS=(0,1.95,-.19)
NETWORK=((-2.73,.23,.15),(2.69,.23,.15),(0,-.77,2.05))
GREY_NODE='#A6A6A6'


HAND='Z003'
IVORY='#FFF4D9'


def appointment(w,p=TASKPOS,alpha=1,s=1, ink=1):
    x,y,z=p
    sheet(w,p,GOLD,.31*s,alpha=alpha,ink=ink)
    if ink:
        w.text(TASK,(x+.04,y-.44*s,z+.12),43*s,GOLD,alpha*ink,font=HAND)


def reply(w,p,label,color,alpha=1,mask=0,width=None,angle=(0,0,0),height=.56,length=1):
    """Move the actual calligraphed paper, rather than moving a text panel."""
    if alpha<=0:
        return
    wid=width or (3.71 if label==RESP_B else 3.25)
    L=wid*length/2
    H=.38*height/.56
    cc=blend(color,MUTED,mask)
    loc=local(p,angle)
    # Both strips come from the same pad; unequal hand-cut ends let the eye
    # keep an identity even when the modeled name is masked.
    off=.047 if color==PURPLE else -.026
    dim=.92 if mask>.75 else 1.
    outline=[(-L,-H),(-L+.091,-H+.052),(-L+.036,-.8*H),
             (-L+.066,-.50*H),(-L-.009,-.23*H),(-L+.012,.01*H),
             (-L-.03,.41*H),(-L+.075,.73*H),(-L+.04,H*.93),
             (-L+.18,H),(L-.14,H+off),(L-.018,.88*H+off),
             (L-.055,.62*H+off),(L+.023,.31*H+off),(L-.026,-.04*H+off),
             (L+.006,-.28*H+off),(L-.053,-.58*H+off),(L-.02,-.88*H+off),
             (L-.20,-H+off),(-L+.07,-H+.016)]
    # Back paper edge is slightly offset and thin; the front remains matte.
    w.face([loc(x,y-.035,-.038) for x,y in outline],cc,alpha*.70,.11,.73)
    w.face([loc(x,y,.027) for x,y in outline],cc,alpha*.95,mix(.235,.13,mask),.88)
    ink=(IVORY if mask<.78 else '#FFFDF6')
    if length>.39:
        l=-L+.15
        r=L-.14
        ribbon(w,loc(l,-.196,.047),loc(l+(r-l)*.33,-.211,.047),
               loc(r-(r-l)*.34,-.204+off,.047),loc(r,-.184+off,.047),cc,
               alpha*dim*.52,1.1,2.45)
    if label:
        at=loc(0,.026,.081)
        normal=trans((0,0,1),rotation(angle))
        facing=step(dot(normal,w.depth),.30,.82)
        w.text(label,at,43*min(1,length+.14),ink,alpha*facing*step(length,.39,.88),font=HAND)
    if mask<1 and length>.22:
        pin=loc(-L+.036,.216,.061)
        w.face((loc(-L-.045,.11,.055),loc(-L+.148,.095,.062),
                loc(-L+.113,.323,.061),loc(-L-.065,.309,.051)),
               color,alpha*(1-mask)*.93,.75,1.1)
        w.dot(pin,BG,.016,alpha*(1-mask)*.82)


def _benchmark_options(w,u,alpha):
    if alpha<=0:
        return
    n0=(-2.55,.43,-.12)
    n1=(2.55,.43,.18)
    ang=step(u,.09,.27)
    for pos,n,wid,name in ((n0,4,.64,'MMLU'),(n1,10,.38,'MMLU-Pro')):
        z=pos[2]
        ain=alpha*(1 if n==4 else ang)
        w.text(name,(pos[0],1.06,z),40,INK,ain)
        for j in range(n):
            a=step(u,.035+.008*j,.13+.008*j)
            xx=pos[0]+(j-(n-1)/2)*(wid+.032)
            sel=j==(1 if n==4 else 7)
            w.tile((xx,mix(-.36,pos[1],a),z), '',GOLD if sel else MUTED,
                   (wid,.28,.11),alpha=ain*a,fill=.24 if sel else .11)
    w.path([(-.73,.43,.14),(.45,.43,.14)],MUTED,1.4,alpha*.77,arrow=True,progress=ang)


def benchmark_scene(g,u):
    start=step(u,0,.16)
    reveal=step(u,.52,.71)
    nextq=step(u,.868,1)
    c=cam_mix(CAM_CHOICE_END,CAM_EXPERT,reveal)
    w=camera(g,c,CAM_PAIR,nextq)
    if start<1:
        _choice(w,1,1-start,depart=.69*start)
    _benchmark_options(w,u,stage(u,0,.13,.32,.49))
    ambiguous=stage(u,.225,.310,.385,.497)
    if ambiguous:
        remove=step(u,.36,.488)
        q=(mix(0,-2.14,remove),mix(1.67,1.20,remove),.66+remove*.15)
        w.text('3 + ? = 7',q,46,GOLD,ambiguous,font='math')
        w.tile((-.66,mix(-.37,-1.15,remove),.98+remove*.68),'4',GOLD,(1.05,.60,.13),
               (0,remove*.6,-remove*.3),alpha=ambiguous)
        w.tile((.66,mix(-.37,-1.15,remove),.98+remove*.68),'4.0',GOLD,(1.05,.60,.13),
               (0,-remove*.6,remove*.3),alpha=ambiguous)
        w.mark((0,-.93,.93),False,.17,ambiguous*step(u,.33,.40))
    # The sample does real work: order-of-operations becomes visible.
    work=stage(u,.421,.494,.582,.650)
    if work:
        fold=step(u,.594,.655)
        c0=step(u,.445,.512); c1=step(u,.486,.559); c2=step(u,.553,.610)
        if fold:
            w.text('3 + 4 × 2',(mix(0,1.18,fold),mix(1.55,.26,fold),.03),
                   mix(52,23,fold),GOLD,work,font='math')
        else:
            w.text('3 + 4 × 2',(0,1.55,.03),52,GOLD,work,font='math')
        branch(w,(0,1.20,0),(-2.25,.20,0),c0,MUTED,work*(1-fold)*.71)
        branch(w,(0,1.20,0),(2.25,.20,0),c0,MUTED,work*(1-fold)*.71)
        w.text('11',(-2.25,-.36,0),48,GOLD,work*c0*(1-fold),font='math')
        if c1<1:
            w.text('4 × 2',(mix(.63,2.28,c0),mix(1.30,-.33,c0)+.45*c1,.10),
                   45,GOLD,work*c0*(1-c1),font='math')
        if c1:
            w.text('3 + 8',(2.25,mix(-.69,-.34,c1)+c2*.48,.10),45,INK,work*c1*(1-c2),font='math')
        if c2:
            w.text('11',(2.25,mix(-.81,-.36,c2),.10),48,GOLD,work*c2*(1-fold),font='math')
    gp=stage(u,.590,.658,.738,.837)
    if gp:
        w.text('GPQA',(-3.02,1.25,.20),43,INK,gp)
        m=step(u,.641,.722)
        # A chain representing one quick lookup stops short of the expert item.
        w.segment((-3.58,-.38,-.23),(-1.55,-.38,-.23),MUTED,1.7,gp*.66,dash=[5,8])
        w.mark((-1.55,-.38,-.16),False,.15,gp*m)
        search=(mix(-3.40,-1.72,m),-.38,-.20)
        w.dot(search,MUTED,.074,gp*m)
        # Three disciplines fan toward the expert item.
        for j,letter in enumerate(('P','C','B')):
            origin=(.05+.38*j,-.89+(.23*j),-1.05+.77*j)
            w.disk(origin,MUTED,letter,.20,.075,alpha=gp*m,label_size=20)
            w.segment(origin,(1.72,.01,-.10),MUTED,1.28,gp*m*.51)
    hle=step(u,.737,.822)*(1-nextq)
    if hle:
        w.text('HLE',(0,1.38,.17),45,INK,hle)
        for k in range(3):
            sheet(w,(-3.78+.23*k,.12+.08*k,-.88+.39*k),MUTED,.58,alpha=hle*(.59+.15*k))
        screen=step(u,.755,.875)
        w.path([(-2.69,-.04,-.29),(-1.03,-.04,-.29)],MUTED,1.5,hle*.78,
               arrow=True,progress=screen)
        for j,z in enumerate((-.94,.0,.88)):
            w.disk((-.45+.47*j,-.17,z),MUTED,'',.25,.11,alpha=hle*column_reveal(j,screen),fill=.2)
        w.path([(1.20,-.02,.32),(2.76,-.02,.32)],MUTED,1.55,hle,arrow=True,progress=screen)
        w.path([(0,-.20,.62),(0,-1.04,1.23)],MUTED,1.50,hle*.64,arrow=True,progress=screen)
        w.mark((0,-1.24,1.28),False,.15,hle*screen)
    active=step(u,.603,.674)
    pivot=step(u,.733,.858)
    origin=vlerp((2.43,-.02,-.11),(3.18,.08,.15),pivot)
    p=cubic(origin,(3.45,1.16,.59),(.30,2.41,.17),TASKPOS,nextq)
    sheet(w,p,GOLD,mix(.92,.31,nextq),alpha=active,image=step(u,.812,.87)*(1-nextq))
    w.text(TASK,(TASKPOS[0]+.04,TASKPOS[1]-.44,TASKPOS[2]+.12),43,GOLD,
           step(nextq,.82,1),font=HAND)
    w.draw()


def column_reveal(j,u):
    return step(u,.12*j,.66+.08*j)


def receiver(w,p,alpha=1,look=0,human=False):
    """One deliberate gaze, on a pale outline instead of a network icon."""
    if alpha<=0:
        return
    f=local(p,(.16,0,0)) if not human else local(p,(-.12,0,0))
    span=.48 if not human else .405
    up=.285 if not human else .233
    cornea=[cubic(f(-span,0,0),f(-.22,up,.01),f(.22,up,.01),f(span,0,0),j/18) for j in range(19)]
    cornea+= [cubic(f(span,0,0),f(.21,-up,.025),f(-.21,-up,.025),f(-span,0,0),j/18) for j in range(1,19)]
    w.face(cornea,MUTED,alpha*.85,.075,.68)
    brush(w,cornea[:19],IVORY,alpha*.94,1.08,3.29)
    brush(w,cornea[18:],MUTED,alpha*.88,.65,1.63)
    x=.17*look
    w.disk(f(x,-.025,.054),GOLD,'',.132 if not human else .102,.063,
           alpha=alpha*.91,fill=.52)
    w.dot(f(x+.005,-.034,.100),BG,.053 if not human else .040,alpha)
    w.dot(f(x-.032,.015,.112),IVORY,.023 if not human else .016,alpha)
    if not human:
        # Tiny registration marks distinguish the fixed automatic eye from the people.
        for k in (-1,1):
            w.segment(f(k*.61,-.08,.02),f(k*.61,.07,.02),MUTED,1.35,alpha*.71)


def seat(w,p,alpha=1):
    if alpha<=0:
        return
    x,y,z=p
    w.segment((x-1.91,y-.021,z-.26),(x+1.91,y-.021,z-.26),MUTED,1.42,alpha*.64)
    for j in (-1,1):
        a=(x+1.91*j,y-.021,z-.26)
        b=(a[0]+.18*j,a[1],z+.19)
        w.segment(a,b,MUTED,1.20,alpha*.60)
        w.segment((x+.14*j,y+.016,z+.24),(x+.22*j,y+.016,z+.24),GOLD,1.55,alpha*.61)
    w.face(((x-.12,y+.007,z+.23),(x,y-.005,z+.31),(x+.12,y+.007,z+.23)),
           GOLD,alpha*.89,.41,1.1)


def _pair_open(w,u,alpha=1,drift=0):
    if alpha<=0:
        return
    appointment(w,alpha=alpha*(1-.82*drift))
    a=step(u,.08,.29)
    b=step(u,.16,.34)
    blind=step(u,.48,.62)
    pp=(0,1.26,-.02)
    eye_in=step(u,.43,.66)
    for j,(q,c,body,e) in enumerate(((LEFT,BLUE,RESP_A,a),(RIGHT,PURPLE,RESP_B,b))):
        xx,y,z=vlerp(pp,q,e)
        if e:
            branch(w,pp,(q[0],q[1]+.44,q[2]),e,MUTED,e*alpha*(1-blind)*.71)
            p=vlerp((xx,y,z),NETWORK[j],drift)
            reply(w,p,body,c,e*alpha,blind,width=None,
                  angle=(.11*sin(pi*e),(-1)**j*.23*sin(pi*e),0),
                  length=mix(mix(.25,1,e),.20,drift))
    # The optional follow-up is a second piece of work, not a new grade.
    # Reveal it from the purple slip as the lecturer compares preferences.
    optional=stage(u,.242,.313,.555,.671)
    under=step(u,.263,.391)
    if optional:
        extra=cubic((3.1,-.095,.58),(3.36,-.28,.78),(3.53,-.57,.92),(2.83,-.82,.66),under)
        w.segment((2.84,-.363,.56),(mix(2.84,3.90,under),-.363,.56),
                  PURPLE,1.9,optional*.86)
        w.tile(extra,'',GOLD,(mix(.22,.62,under),mix(.13,.42,under),.094),
               (0,under*.15,under*-.17),alpha=optional*under,fill=.48)
        w.curve((3.75,-.29,.62),(3.81,-.64,.89),(3.31,-.88,.87),extra,
                MUTED,1.5,optional*.71,progress=under)
    direct=stage(u,.34,.41,.541,.64)
    if direct:
        p=step(u,.376,.542)
        w.path([(-3.36,-.45,.57),(-2.45,-.45,.57),(-1.57,-.45,.57)],BLUE,1.5,direct*.69,
               progress=p)
        w.dot((-1.57,-.45,.57),BLUE,.064,direct*step(p,.70,1)*.82)
    v0=stage(u,.60,.71,.835,.98)
    v1=stage(u,.72,.82,.94,1)
    v2=stage(u,.82,.90,.97,1)
    eye=(0,-1.22,.40)
    if eye_in:
        receiver(w,eye,alpha*eye_in,clamp(v1-v0,-1,1),human=True)
        for j,(hit,target) in enumerate(((v0,(-2.5,-.60,.54)),(v1,(2.5,-.60,.53)),(v2,(0,-.43,.55)))):
            if hit:
                fly(w,(0,-1.22,.49),((j-1)*.47,-.78,1.05),(target[0],-1.28,.89),
                    target,step((u-(.60+.10*j))/.15,0,1),GOLD,.077,alpha*hit)
    # Keep a last vote on the eye's pupil. It becomes a graph edge marker.
    w.dot((0,-1.22,.57),GOLD,.075,alpha*step(u,.86,.98))


def pair_scene(g,u):
    w=camera(g,CAM_PAIR)
    _pair_open(w,u)
    w.draw()


def _match_graph(w,u,alpha,flatten):
    if not alpha:
        return
    end=[(0,.03,1.12),(0,-.31,1.46),(0,-.64,1.87)]
    positions=[vlerp(a,b,flatten) for a,b in zip(NETWORK,end)]
    for k,(a,b) in enumerate(((1,0),(2,1),(0,2))):
        move=step(u,.135+.085*k,.29+.09*k)
        if flatten<1:
            p,q=positions[a],positions[b]
            mid=(p[0]+q[0])/2
            y=(p[1]+q[1])/2
            z=(p[2]+q[2])/2
            p1=(mid,y+.24,z-.34)
            p2=(mid,y+.24,z-.34)
            w.curve(p,p1,p2,q,MUTED,1.65,alpha*(1-flatten)*(.62+.32*move),arrow=True)
            fly(w,p,p1,p2,q,move,GOLD,.083,alpha*(1-flatten)*.92)
    for j,(p,c,label) in enumerate(zip(positions,(BLUE,PURPLE,GREY_NODE),('A','B','C'))):
        a=step(u,.02+.026*j,.145+.036*j)
        w.disk(p,c,label if flatten<.74 else '',mix(.35,.15,flatten),.11,alpha=alpha*a)
    if flatten:
        w.segment((-4.06,-.19,1.14),(4.06,-.19,1.14),MUTED,1.45,alpha*flatten*.64)
        for k in range(-4,5):
            pp=(k*.79,-.19,1.14)
            w.segment((pp[0],pp[1]-.055,pp[2]),(pp[0],pp[1]+.055,pp[2]),
                      GOLD if k==0 else MUTED,1.5,alpha*flatten*.65)
        w.text('½',(0,.99,.77),55,GOLD,alpha*step(flatten,.65,1),font='math')


def network_scene(g,u):
    build=step(u,.0,.22)
    flatten=step(u,.405,.66)
    pivot=step(u,.755,1)
    first=cam_mix(CAM_PAIR,CAM_NETWORK,step(u,0,.24))
    c=cam_mix(first,CAM_SCORE,flatten)
    w=camera(g,c,CAM_JUDGE,pivot)
    if build<1:
        _pair_open(w,1,1-build,build)
    _match_graph(w,u,build*(1-pivot),flatten)
    if pivot:
        sensor_src=(0,.03,1.12)
        receiver(w,vlerp(sensor_src,JUDGE,pivot),pivot)
        p=vlerp((0,.03,1.12),TASKPOS,pivot)
        appointment(w,p,pivot,.6+.4*pivot,step(pivot,.72,.96))
        for j,(q,col,txt) in enumerate(((LEFT,BLUE,RESP_A),(RIGHT,PURPLE,RESP_B))):
            side=2*j-1
            p=vlerp((side*.03,-.31,1.46),q,pivot)
            reply(w,p,txt,col,pivot,.92,length=mix(.24,1,pivot))
            seat(w,((VOTE1,VOTE2)[j]),pivot*step(pivot,.40,1))
    w.draw()


def _judge_core(w,task=1,sensor=1,seats=1):
    if task:appointment(w,alpha=task)
    receiver(w,JUDGE,sensor)
    for pos in (VOTE1,VOTE2):
        seat(w,pos,seats)


def _judge_replies(w,swap=0,mask=0,alpha=1,bad=0,length=1,fold=0):
    # Opposite z signs give a physical over/under crossing. Their y offsets
    # separate perspective projections near the intersection, not the slots.
    ss=sin(pi*swap)
    ax=mix(LEFT[0],RIGHT[0],swap)
    bx=mix(RIGHT[0],LEFT[0],swap)
    pa=(ax,LEFT[1]-.06*ss-.31*fold,LEFT[2]+1.83*ss-.09*fold)
    pb=(bx,RIGHT[1]+.11*ss-.31*fold,RIGHT[2]-1.80*ss+.1*fold)
    if .003<swap<.997:
        for c,sign in ((BLUE,1),(PURPLE,-1)):
            path=[(mix(LEFT[0]*sign,RIGHT[0]*sign,q/24),
                   LEFT[1]-.27+(-.06 if sign==1 else .11)*sin(pi*q/24),
                   LEFT[2]-.18+sign*1.8*sin(pi*q/24)) for q in range(25)]
            brush(w,path,c,alpha*ss*.80,.81,3.05,progress=swap)
    reply(w,pb,RESP_B,PURPLE,alpha*(1-bad),mask,angle=(.045*ss+1.48*fold,.25*ss,0),length=length)
    if bad:
        reply(w,pb,'I moved it to tomorrow.',PURPLE,alpha*bad,mask,width=3.55)
    reply(w,pa,RESP_A,BLUE,alpha,mask,angle=(.06*ss+1.48*fold,-.30*ss,0),length=length)
    return pa,pb


def underline(w,p,text,needle,color,amount,a):
    """The pen travels under the exact words the rubric checks."""
    if amount<=0 or a<=0:
        return
    j=text.index(needle)
    fx=(w.zoom**.5)/w.scale
    text_w=w.g.measure(text,43,font=HAND)
    left=p[0]+(w.g.measure(text[:j],43,font=HAND)-text_w/2)*fx
    width=w.g.measure(needle,43,font=HAND)*fx
    right=left+width
    y,z=p[1]-.168,p[2]+.055
    ribbon(w,(left,y,z),(left+.22*width,y-.02,z),(right-.20*width,y+.025,z),(right,y+.012,z),
           color,a,.81,3.47,amount)
    w.mark(((left+right)/2,p[1]-.62,p[2]+.11),color==GREEN,.139,a*step(amount,.70,1)*.93)


def judge_scene(g,u):
    close=stage(u,.363,.493,.714,.89)
    w=camera(g,CAM_JUDGE,CAM_JUDGE_NEAR,close)
    glance=stage(u,.307,.375,.405,.44)+stage(u,.61,.679,.90,1)
    _judge_core(w,sensor=0)
    receiver(w,JUDGE,look=-glance)
    bad=stage(u,.075,.158,.25,.31)
    swap=step(u,.42,.615)
    mask=.92*(1-step(u,.35,.42))
    _judge_replies(w,swap,mask,bad=bad)
    evidence=stage(u,.065,.138,.245,.307)
    if evidence:
        underline(w,LEFT,RESP_A,'cancel',GREEN,step(u,.058,.127),evidence)
        underline(w,RIGHT,'I moved it to tomorrow.','moved it to tomorrow',RED,
                  step(u,.137,.216),evidence*bad)
    pick1=step(u,.307,.384)
    pick2=step(u,.614,.683)
    seatpos=(VOTE1[0],-.77,.72)
    p0=(JUDGE[0],JUDGE[1]-.24,JUDGE[2]+.12)
    p1=(-.34,.34,-.14)
    p2=(-2.83,-.60,.51)
    if pick1:
        fly(w,p0,p1,p2,seatpos,pick1,GOLD,.10,(1-step(u,.417,.465))*.94)
    if pick2:
        fly(w,p0,p1,p2,seatpos,pick2,GOLD,.10,(1-step(u,.69,.86))*.94)
    if u>.67:
        reveal=step(u,.69,.79)
        end=step(u,.925,1)
        base=(seatpos[0],-1.16,.93)
        w.segment(seatpos,base,RED,1.36,reveal*(1-end)*.58,dash=[4,7])
        for j,c in enumerate((BLUE,PURPLE)):
            origin=base
            dest=(-.75+1.5*j,-1.49,.87)
            q=step(u,.724+.085*j,.83+.095*j)
            bu=cubic(origin,(-1.94,-1.52,-.38-.93*j),(-1.45,-1.60,-.55-1.12*j),dest,q)
            if q:
                w.disk(bu,c,('A','B')[j] if q>.75 else '',.165,.095,alpha=step(u,.72+.085*j,.79+.09*j)*(1-end))
        w.segment((-.50,-1.49,.87),(.50,-1.49,.87),RED,1.42,(1-end)*step(u,.865,.92)*.75,dash=[4,6])
    if u>.93:
        w.dot(seatpos,GOLD,.10,step(u,.93,1))
    w.draw()


def _extrawords(w,p,q,dup=0,a=1):
    if a<=0:
        return
    x,y,z=p
    for j,wide in enumerate((2.48,1.97,2.26,2.39)):
        expand=step(q,.09*j,.41+.15*j) if j<3 else dup
        if expand:
            p=(x-.11,y-.34-.179*j,z-.075+.125*j)
            f=local(p,(expand*.16,0,0))
            d=wide*expand/2
            c=blend(MUTED,RED,.50)
            w.face((f(-d,-.045),f(-d+.048,.045),f(d-.030,.042),f(d,-.016),f(d-.041,-.039)),
                   c,a*expand,.24,.94)
            if d>.2:
                w.segment(f(-d+.065,0,.008),f(d-.091,.003,.008),c,1.39,a*expand*.56)


def verbosity_scene(g,u):
    leave=step(u,.88,1)
    w=camera(g,CAM_JUDGE,CAM_CHART,leave)
    s=1-leave
    if s:
        _judge_core(w,s,s,s)
        pa,pb=_judge_replies(w,1,0,s,fold=leave)
        grow=step(u,.12,.31)
        repeat=step(u,.52,.67)
        _extrawords(w,pa,grow,repeat,s)
        move=step(u,.29,.427)
        a=(VOTE1[0],-.77,.72)
        b=(VOTE2[0],-.77,.72)
        fly(w,a,(-.70,-1.54,1.54),(.54,-1.61,1.94),b,move,GOLD,.10,s)
        if move<.015:
            w.dot(a,GOLD,.10,s*(1-move))
        feed=stage(u,.41,.51,.648,.755)
        if feed:
            p=(2.5,-.79,.72)
            c1=(4.77,-1.19,1.81)
            c2=(4.92,.27,1.48)
            dest=(3.75,.10,.55)
            fly(w,p,c1,c2,dest,step(u,.428,.61),BLUE,.066,feed*.94)
        slicing=stage(u,.733,.805,.889,.945)
        if slicing:
            # A hypothetical cut approaches the long tail, then turns aside.
            w.box((4.54,-.50,1.09),(0.055,.95,1.52),RED,slicing*.68,
                  (0,-.19,.18*step(u,.82,.92)),fill=.17,edge=1.25)
    if leave:
        _rulers(w,1-leave,1,step(leave,.43,1),1)
    w.draw()


def _rulers(w,source=0,extra=1,alpha=1,gap=1):
    """Two strips line up on their left ends; the uncovered interval is x."""
    if alpha<=0:
        return
    x0=-2.81
    for j,(c,d,prior) in enumerate(((PURPLE,2.11,LEFT),(BLUE,2.11+1.56*extra,RIGHT))):
        y=.59-.49*j
        p=vlerp((x0+d/2,y,.69),(prior[0],prior[1]-.31,.55-.19*j),source)
        w.box(p,(d,.089,.18),c,alpha,fill=.61,edge=1.23)
    if gap and extra:
        q=1-source
        b=x0+2.11
        e=b+1.56*extra
        bottom_ticks(w,(b,-.19,.82),(e,-.19,.82),GOLD,alpha*extra*gap*q,1.42,.06)
        w.segment((b,-.115,.80),(b,.55,.80),MUTED,1.1,alpha*extra*q*.53,dash=[3,5])


CX=3.80
FY=-1.37
TOP=1.58
ZDEFAULT=.03
Q_LEVELS=((-1.14,-.61),(0,-.06),(1.17,.55))
SAMPLE_X=(-3.21,-2.69,-2.16,-1.54,-.98,-.44,.06,.54,1.14,1.70,2.13,2.70,3.15,3.60)
SAMPLE_D=(.024,-.071,.045,-.021,.016,-.051,.018,.047,-.051,.016,.035,-.026,-.011,.029)


def win(x,delta=0):
    return 1/(1+exp(-(.75*x+delta)))


def fy(f):
    return mix(FY,TOP,f)


def wc(x,delta=0,z=.03):
    return (x,fy(win(x,delta)),z)


def gaxis(w,h=1,v=1,a=1):
    if a<=0:
        return
    xo=(-CX,FY,ZDEFAULT)
    w.path([xo,(CX+.18,FY,ZDEFAULT)],MUTED,1.75,a*.92,arrow=True,progress=h)
    w.path([xo,(-CX,TOP+.19,ZDEFAULT)],MUTED,1.75,a*.92,arrow=True,progress=v)
    w.text('Length gap',(3.38,FY-.35,.05),27,MUTED,a*step(h,.80,1))
    w.text('Win rate',(-CX+.30,TOP+.41,.04),29,MUTED,a*step(v,.82,1))
    for y,label,n in ((FY,'0%',.02),(fy(.5),'50%',.5),(TOP,'100%',.95)):
        z=step(v,max(0,n-.06),min(1,n+.09))
        w.segment((-CX-.059,y,.043),(-CX+.038,y,.043),MUTED,1.15,a*z*.73)
        w.text(label,(-CX-.12,y,.07),24,MUTED,a*z,align='right',font='math')
        if n>.1:
            w.segment((-CX+.06,y,.028),(CX,y,.028),GRID,1.02,a*z*.77)
    s=step(h,.41,.68)
    w.segment((0,FY-.055,.044),(0,FY+.055,.044),GOLD,1.45,a*s*.80)
    w.text('0',(0,FY-.26,.05),24,GOLD,a*s,font='math')


def _chart(w,u,alpha=1):
    ax=step(u,.012,.168)
    ay=step(u,.133,.291)
    gaxis(w,ax,ay,alpha)
    detect=1-step(u,.147,.245)
    if detect:
        _rulers(w,0,1,detect*alpha,gap=1)
        if ax:
            a=step(u,.01,.164)
            lift=(mix(-.70,.85,a),mix(-.19,FY,a),mix(.82,.03,a))
            w.dot(lift,GOLD,.073,alpha*detect*a)
            w.segment((lift[0],FY,lift[2]),lift,GOLD,1.2,alpha*detect*.59,dash=[4,6])
    dots=step(u,.219,.524)
    line=step(u,.375,.583)
    depth=step(u,.479,.713)
    zero=step(u,.606,.771)
    avg=step(u,.739,.831)
    raw=(2.58,fy(win(2.58,-.06)),.05)
    pp=step(u,.533,.656)
    if pp:
        q=wc(mix(raw[0],0,zero),-.06,raw[2])
        # The one observed x collapses to the x=0 condition. At the same
        # moment the 3D cross section exposes one prediction for each question.
        w.segment((q[0],FY,q[2]),q,RED,1.33,alpha*pp*(1-zero)*.79,dash=[5,7])
        w.dot(q,blend(RED,GOLD,zero),.075,alpha*pp*(1-step(avg,.22,.71)))
    for j,(x,d) in enumerate(zip(SAMPLE_X,SAMPLE_D)):
        a=step(dots,j*.041,j*.041+.21)
        if a:
            z=.031
            w.dot((x,fy(clamp(win(x,-.06)+d)),z),MUTED,.044,alpha*a*.77)
    for j,(z,delta) in enumerate(Q_LEVELS):
        openlayer=step(depth,0,1) if j!=1 else 1
        z=z*depth
        p=.42+.44*(1-abs(z)/1.17)
        if openlayer and line:
            w.path([wc(-3.75+k*7.50/44,delta,z) for k in range(45)],MUTED,
                   2.0 if j==1 else 1.48,alpha*openlayer*p,progress=line)
    if zero:
        plane=zero*(1-.66*avg)
        z=.15+1.39*depth
        w.face([(0,FY,-z),(0,TOP,-z),(0,TOP,z),(0,FY,z)],GOLD,alpha*plane*.40,.07,1.18)
        w.segment((0,FY,.05),(0,TOP,.05),GOLD,1.65,alpha*plane*.63,dash=[5,7])
        target=(0,fy(sum(win(0,d) for _,d in Q_LEVELS)/3),1.40)
        for j,(z,d) in enumerate(Q_LEVELS):
            q=step(avg,.04+.075*j,.68+.09*j)
            pos=vlerp(wc(0,d,z*depth),target,q)
            r=.075+.016*(j==2)
            w.dot(pos,GOLD,r,alpha*zero*(1-step(avg,.87,1)*.66))
        if avg:
            w.dot(target,GOLD,.128,alpha*step(avg,.72,1))
            w.segment((-CX,target[1],target[2]),target,GOLD,1.3,alpha*step(avg,.73,1)*.49,
                      dash=[4,7])


CAL_START=(.32,-.24,-1.59)
CAL_TEXT=(-.05,.02,.90)
CAL_PROMPT=(.26,1.93,-1.24)
CAL_DATE=(1.70,-.96,1.18)


class MoveGraph:
    """A single spatial transform for the outgoing plot and its labeled axes."""
    def __init__(self,w,offset,scale):
        self.w,self.o,self.s=w,offset,scale
    def p(self,q):
        return tuple(a+self.s*b for a,b in zip(self.o,q))
    def segment(self,a,b,*args,**kw):
        self.w.segment(self.p(a),self.p(b),*args,**kw)
    def path(self,points,*args,**kw):
        self.w.path([self.p(p) for p in points],*args,**kw)
    def face(self,points,*args,**kw):
        self.w.face([self.p(p) for p in points],*args,**kw)
    def box(self,p,size,*args,**kw):
        self.w.box(self.p(p),tuple(self.s*q for q in size),*args,**kw)
    def text(self,s,p,size,*args,**kw):
        self.w.text(s,self.p(p),self.s*size,*args,**kw)
    def dot(self,p,c,r,*args,**kw):
        self.w.dot(self.p(p),c,self.s*r,*args,**kw)


def length_scene(g,u):
    lift=step(u,.577,.769)
    bridge=step(u,.842,1)
    first=cam_mix(CAM_CHART,CAM_CHART_DEPTH,lift)
    w=camera(g,first,CAM_CAL,bridge)
    if bridge<1:
        depart=step(bridge,.005,.82)
        slide=MoveGraph(w,(-9.38*depart,.27*depart,-2.06*depart),mix(1,.77,depart))
        _chart(slide,u,1-step(bridge,.56,.88))
    if bridge:
        # The marker on the section turns into real extra information.
        c=(0,fy(sum(win(0,d) for _,d in Q_LEVELS)/3),1.40)
        p=vlerp(c,CAL_DATE,bridge)
        w.tile(p,'Thu 2 pm' if bridge>.55 else '',GOLD,
               (mix(.23,1.57,bridge),mix(.13,.43,bridge),.117),
               alpha=step(bridge,0,.52),fill=mix(.53,.38,bridge),label_size=mix(17,27,bridge))
        _cal_stage(w,step(bridge,.34,1),0,bridge,show_date=False)
        # The human vote from the Arena returns once the new line has
        # operational content. It is placed on the appointment time, not
        # attributed to the fact that the line is longer.
        h=stage(bridge,.60,.75,.915,1)
        if h:
            pupil=(3.83,-.90,.63)
            receiver(w,pupil,h,-.72,human=True)
            fly(w,pupil,(3.13,-1.01,.36),(2.55,-.92,.78),
                (CAL_DATE[0]+.72,CAL_DATE[1]+.11,CAL_DATE[2]+.07),
                step(bridge,.716,.916),GOLD,.064,h*.88)
    w.draw()


def _cal_shape(w,center,alpha=1):
    """One bound page; its ruled cells sit behind the writing, not inside a UI."""
    if alpha<=0:
        return
    x,y,z=center
    f=local(center)
    board=((-1.91,-1.07),(1.64,-1.07),(1.88,-.83),(1.88,1.04),(-1.91,1.04))
    paper=((-1.78,-1.02),(1.59,-1.02),(1.81,-.80),(1.81,.985),(-1.78,.985))
    w.face([f(j,k,-.031) for j,k in board],MUTED,alpha*.82,.10,1.2)
    w.face([f(j,k,.044) for j,k in paper],'#C3B9AB',alpha*.88,.16,1.23)
    w.face((f(1.59,-1.02,.047),f(1.59,-.80,.059),f(1.81,-.80,.047)),
           MUTED,alpha*.73,.21,1.12)
    ribbon(w,f(-1.76,.58,.06),f(-.62,.59,.06),f(.68,.58,.06),f(1.77,.59,.06),
           MUTED,alpha*.74,1.11,2.56)
    for j in (-1,1):
        xx=j*1.02
        ring=(f(xx,.86,.074),f(xx+.066,.98,.171),f(xx+.035,1.27,.211),f(xx,1.13,-.058))
        ribbon(w,*ring,MUTED,alpha*.91,1.35,3.12,n=18)
        w.dot(f(xx,.864,.083),MUTED,.041,alpha*.67)
    x0=-1.56
    y0=-.869
    for j in range(6):
        xx=x0+j*.629
        w.segment(f(xx,y0,.063),f(xx,y0+1.30,.063),MUTED,
                  1.44 if j in (0,5) else 1.17,alpha*(.59 if j in (0,5) else .46))
    for j in range(4):
        yy=y0+j*.436
        w.segment(f(x0,yy,.064),f(x0+3.145,yy,.064),MUTED,
                  1.42 if j in (0,3) else 1.18,alpha*(.72 if j in (0,3) else .54))


def _event_p(c):
    return (c[0]-.008,c[1]-.236,c[2]+.14)


def _cal_stage(w,amount,look,arrived=1,show_text=1,leave=0,show_date=True,touch=0):
    if amount<=0:
        return
    # Reply in foreground at z≈1 and a true separate surface at z≈−1.6.
    # A sideways peek makes the projected separation grow.
    p=(mix(CAL_TEXT[0],-3.45,look)-.32*touch,mix(CAL_TEXT[1],.31,look)+.16*touch,
       mix(CAL_TEXT[2],1.24,look)+.27*touch)
    if show_text:
        reply(w,p,RESP_A,BLUE,amount*(1-leave),.17,width=3.58,
              angle=(.10*touch,.21*touch,-.075*touch),length=1)
    center=(mix(CAL_START[0],1.31,look),CAL_START[1]+.12*look,CAL_START[2])
    _cal_shape(w,center,amount*(1-leave))
    pos=_event_p(center)
    s=step(look,.12,.91)
    p=vlerp(pos,(0,0,0),leave)
    w.tile(p,'',GOLD,(mix(.544,.96,leave),mix(.389,.67,leave),.14),
           alpha=amount,fill=mix(.66,.33,leave))
    if s:
        w.dot((pos[0],pos[1],pos[2]+.10),GOLD,.069,s*amount*(1-leave))
    badge=vlerp(CAL_DATE,(4.39,-1.18,1.09),look)
    if show_date and 1-look:
        w.tile(badge,'Thu 2 pm',GOLD,(1.57,.43,.117),alpha=amount*arrived*(1-look),fill=.38,label_size=27)


def calendar_scene(g,u):
    look=step(u,.215,.535)
    collect=step(u,.715,1)
    focus=cam_mix(CAM_CAL,(.39,.13,.95,(.02,.26,-.13)),look)
    w=camera(g,focus,CAM_HOME,collect)
    reach=stage(u,.009,.143,.24,.365)
    _cal_stage(w,1,look,1,leave=collect,touch=reach)
    if collect:
        for j,(x,c) in enumerate(((-2.45,BLUE),(2.45,PURPLE))):
            side=2*j-1
            p=vlerp((side*5.18,-.48,-.74),(x,0,0),collect)
            w.disk(p,c,('A','B')[j],r=mix(.29,.42,collect),depth=.15,
                   alpha=step(collect,0,.58),label_size=34)
    w.draw()


SCENES=(exam_scene,choice_scene,benchmark_scene,pair_scene,network_scene,
        judge_scene,verbosity_scene,length_scene,calendar_scene)
HOLDS=tuple(b.get('hold',.55) for b in json.loads(Path(__file__).with_suffix('.json').read_text(encoding='utf-8')))
# Choreographic landmarks of the subtitled phrase pairs. Values are positions
# on the speech clock, so measured narration can lead the motion without
# changing its final held state or the cross-beat camera match.
MARKS=(
    (.0,.155,.246,.402,.557,.737,.836),
    (.0,.112,.272,.389,.568,.680,.829),
    (.0,.130,.257,.387,.521,.600,.748,.866),
    (.0,.170,.292,.406,.582,.724,.865),
    (.0,.148,.286,.398,.589,.739,.866),
    (.0,.145,.311,.422,.611,.686,.852),
    (.0,.127,.293,.419,.557,.674,.774),
    (.0,.136,.299,.413,.575,.735,.820,.922),
    (.0,.112,.247,.452,.560,.735),
)


def phase(g,i,t,duration):
    length=getattr(g,'speech',0.) or duration-HOLDS[i]
    length=max(length,duration*.67)
    u=clamp(t/length)
    if u>=1 or not getattr(g,'parts',None):
        return u
    points=[(0.,0.)]
    for j,target in enumerate(MARKS[i][1:],1):
        heard=clamp(g.part(j,target*length/duration)*duration/length)
        if points[-1][0]+.025<heard<.988:
            points.append((heard,target))
    points.append((1.,1.))
    for (a,p),(b,q) in zip(points,points[1:]):
        if u<=b:
            return mix(p,q,(u-a)/(b-a))
    return 1.


def draw(g,i,t,duration):
    SCENES[i](g,phase(g,i,t,duration))
