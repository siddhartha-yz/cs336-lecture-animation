"""Act I — take a probability chip from a sentence, through two kinds of ruler."""
import math
from spatial import *

TILES=('Two','plus','two','is','exactly','four')
XS=tuple(-4.40+i*1.76 for i in range(6))
PROBS=((.9,.9,.9,.9,.9,.4),(.6,.6,.6,.6,.6,.8))
MODELS=(BLUE,PURPLE)
ZLANE=(.74,-.86)
YLANE=(-.09,-1.47)
HOLD=(1.6,1.55,1.75,1.9,1.7,1.85,1.6,1.75,1.85)
PI=math.pi
# yaw, elevation, focal scale, tracked world origin:
C0=(.055,.095,1.57,(3.37,.45,.18))
CW=(-.13,.18,.93,(-.06,.10,.12))
C1=(.12,.179,.99,(.57,.043,.12))
CF=(.14,.255,.92,(.08,.06,.10))
CA=(.17,.25,.81,(0,.28,.08))
CS=(.04,.075,.97,(.05,.22,.10))
CV=(-.14,.245,1.00,(.16,.02,.08))
CL=(-.38,.255,.97,(0,.10,.08))
CR=(.05,.20,.94,(0,.03,.12))
CY=(.37,.14,1.07,(2.61,-.03,.09))
CD=(-.22,.28,.91,(.12,.02,.10))
CC=(-.13,.22,.93,(.06,.04,.08))
CE=(.03,.14,.99,(0,.04,0))
END=(0,0,1,(0,0,0))


def ep(u,a,b,c,d):
    return step(u,a,b)*(1-step(u,c,d))


def interp(ca,cb,u):
    return tuple(mix(a,b,u) for a,b in zip(ca[:3],cb[:3]))+(vlerp(ca[3],cb[3],u),)


def cam(g,state,distance=13):
    yaw,pitch,scale,target=state
    return World(g,yaw=yaw,pitch=pitch,zoom=scale,target=target,distance=distance)


def timing(g,t,duration,i):
    voiced=getattr(g,'speech',0) or duration-HOLD[i]
    voiced=max(.01,voiced)
    u=clamp(t/voiced)
    def cue(j,f):
        return clamp(g.part(j,f*voiced/duration)*duration/voiced,0,.998)
    return u,cue


def poly_move(a,b,t,lift=.0):
    x,y,z=vlerp(a,b,t)
    return x,y+lift*math.sin(PI*t),z


def packet(w,a,b,u,color=GOLD,alpha=1,r=.064):
    if .008<u<.996 and alpha>.001:
        w.box(poly_move(a,b,u,.065),(r*1.7,r*1.7,r*1.7),color,alpha=alpha,fill=.63,edge=.8)


def tri(w,x,y,z,color,alpha=1):
    w.face(((x-.2,y-.12,z),(x+.2,y-.12,z),(x,y+.22,z+.14)),
           color,alpha,fill=.32,edge=1.5)


def ink_patch(w,p,dx,dy,c,a=1,rot=(0,0,0),fill=.82,edge=.0):
    if a<.002 or min(dx,dy)<.001:return
    r=rotation(rot)
    corners=tuple(add(p,trans((x*dx/2,y*dy/2,0),r))
                  for x,y in ((-1,-1),(1,-1),(1,1),(-1,1)))
    w.face(corners,c,a,fill,edge)


def prob(w,x,y,z,width,p,c=GOLD,a=1,mass=1,depth=.185):
    """One calibrated ink band, not a case around each probability."""
    if a<.002:return
    z+=depth*.41
    w.segment((x-width/2,y,z),(x+width/2,y,z),MUTED,1.25,a*.46)
    for xx in (x-width/2,x+width/2):
        w.segment((xx,y-.067,z),(xx,y+.067,z),MUTED,1.12,a*.53)
    dx=width*clamp(p)*clamp(mass)
    if dx>.003:
        ink_patch(w,(x-width/2+dx/2,y,z+.023),dx,.069,c,a,fill=.91)


def score_mark(w,x,y,z,model,a=1,pnum=False):
    if a<.002:return
    c=MODELS[model]
    # The response is ink on a trace, not another token-shaped container.
    label='four' if model else 'five'
    w.text(label,(x,y,z+.06),48,c,a,weight='medium')
    left=x-.37
    right=x+.38
    w.segment((left,y-.285,z),(right,y-.285,z),c,1.56,a*.84)
    w.mark((x+.72,y+.039,z+.09),bool(model),.113,a*.97)
    if pnum:
        w.text('0.60' if not model else '0.80',(x,y-.38,z+.1),25,c,a)


def lead_rule(w,a,b,c,alpha=1):
    """The line that indicates the extent of a measured interval."""
    if alpha<.002:return
    w.segment(a,b,c,1.32,alpha)
    for p in (a,b):
        w.segment(add(p,(0,-.075,0)),add(p,(0,.075,0)),c,1.14,alpha*.81)


def prompt_track(w,a=1,shift=(0,0,0),splay=0,only=None,
                 mask=0,fill=1,truth=1,highlight=-1,omit=()):
    sx,sy,sz=shift
    x0=-5.12+sx
    x1=5.12+sx
    yy=.93+sy
    zz=.22+sz
    # Five ordinary words use typography and a single baseline. The thick
    # gold answer slip is the one object with the authority to leave the row.
    if a>.001:
        w.segment((x0,yy-.38,zz-.06),(x1,yy-.38,zz-.06),MUTED,1.08,a*.28)
    for j,x in enumerate(XS):
        if j in omit:continue
        if only is not None and j not in only:
            az=a*.18
        else:
            az=a
        X=x+sx
        if j==highlight:
            target=fill
            label=TILES[j] if target>.51 else '?'
            lz=zz+1.24*(1-target)
            Y=yy+.32*(1-target)
            if mask>.5 and target<.24:label='?'
            w.tile((X,Y,lz),label,GOLD,(1.40,.69,.12),
                   (0,-.58*(1-target),0),az,.67,label_size=41)
        elif j>highlight and highlight>=0 and mask>0.001:
            q=clamp(mask)
            Y=yy-.27*q
            lz=zz-1.56*q
            w.tile((X,Y,lz),TILES[j] if q<.50 else '',GOLD,
                   (1.39,.68,.13),(.87*q,0,0),az*(1-.76*q),.21,label_size=39)
        elif j==5 and truth<.995:
            w.tile((X,yy,zz),'four' if truth>.53 else '?',GOLD,(1.40,.68,.16),
                   (0,-.62*math.sin(PI*truth),0),az,.84,label_size=49)
        elif j==5:
            w.tile((X,yy,zz),TILES[j],GOLD,(1.39,.68,.17),
                   (0,0,0),az,.84,label_size=46)
        else:
            w.text(TILES[j],(X,yy+.044,zz+.035),46,INK,az*.88)
            # Discrete token boundaries stay legible without five identical boxes.
            dv=.60 if j!=3 else .45
            w.segment((X-dv,yy-.285,zz+.022),(X+dv,yy-.285,zz+.022),
                      MUTED,1.26,az*.54)
            w.segment((X-dv,yy-.316,zz+.022),(X-dv,yy-.239,zz+.022),
                      MUTED,1.12,az*.40)
            w.segment((X+dv,yy-.316,zz+.022),(X+dv,yy-.239,zz+.022),
                      MUTED,1.12,az*.40)
        w.segment((X,yy-.39,zz-.055),(X,yy-.48,zz-.055),GOLD if j==5 else MUTED,1.14,az*.47)


def probability_stroke(w,x,y,z,p,c,q,alpha=1):
    if alpha<.002:return
    x0=x-.61
    x1=x+.61
    lead_rule(w,(x0,y,z),(x1,y,z),MUTED,alpha*.30)
    if q>.001:
        b=x0+1.22*p*q
        w.segment((x0,y,z+.075),(b,y,z+.075),c,3.95,alpha)
        w.dot((b,y,z+.088),c,.041,alpha*(.64+.36*q))


def prediction_lanes(w,reveal=(1,1,1,1,1),results=(1,1),alpha=1,zoff=0,yoff=0):
    for j,col in enumerate(MODELS):
        y,z=YLANE[j]+yoff,ZLANE[j]+zoff
        w.segment((-5.1,y,z-.17),(5.18,y,z-.17),col,1.04,alpha*.14)
        w.disk((-5.15,y,z),col,'AB'[j],.245,.145,alpha=alpha,fill=.42,label_size=29)
        for h,x in enumerate(XS[:-1]):
            q=reveal[h]
            probability_stroke(w,x,y,z,PROBS[j][h],col,q,alpha*(.24+.76*q))
        if results[j]>.001:
            q=results[j]
            dz=mix(-.81,0,q)
            score_mark(w,XS[5],y,z+dz,j,alpha*q)


def answer_trace(w,focus=1,a=1,zoff=0):
    for j,(y,z) in enumerate(zip(YLANE,ZLANE)):
        end=(XS[5],y+.21,z+zoff)
        x=XS[5]
        w.curve((x,.55,.23+zoff),(x+.21,.37,.31+zoff),(x+.15,y+.32,z-.09+zoff),end,
                GOLD,1.36,a*focus*.61,focus)
    w.segment((XS[5]-.60,1.41,.22+zoff),(XS[5]+.60,1.41,.22+zoff),
              GOLD,1.3,a*focus*.63)


def hero(w,u,c_blue=.59,c_purple=.82,a=1):
    reveal=[step(u,.018+j*.049,.146+j*.054) for j in range(5)]
    s=step(u,c_blue-.023,c_blue+.12)
    p=step(u,c_purple-.025,c_purple+.108)
    prompt_track(w,a,truth=s)
    prediction_lanes(w,reveal,(s,p),a*step(u,.017,.19))
    answer_trace(w,step(u,c_blue-.08,c_blue+.045),a)


def force(w,u,cu=None,a=1,zoff=0):
    cu=cu or (lambda j,f:f)
    blend_in=step(u,0,.115)
    wrong_clear=step(u,.025,.17)
    prefix=step(u,max(.13,cu(2,.24)-.075),cu(2,.24)+.095)
    mask=step(u,.10,.26)
    slice_open=step(u,cu(3,.38)-.027,cu(3,.38)+.116)
    keep=step(u,cu(4,.51)-.018,cu(4,.51)+.080)
    insert=step(u,cu(5,.63)-.055,cu(5,.63)+.10)
    wrong=ep(u,cu(6,.77)-.038,cu(6,.77)+.06,.917,1)
    forward=step(u,cu(7,.91)-.01,.985)
    if u<=.001:
        hero(w,1,a=a)
        return
    prompt_track(w,a,(0,0,zoff),only=None,mask=mask*(1-forward),fill=insert,
                 truth=1,highlight=4 if blend_in>.25 else -1)
    if blend_in<1:
        prediction_lanes(w,(1,1,1,1,1),(1-wrong_clear,1-wrong_clear),a*(1-blend_in),zoff)
        answer_trace(w,1-wrong_clear,a*(1-blend_in),zoff)
    selected=mix(XS[4],XS[5],forward)
    xprefix=XS[0]- .5
    prev=mix(XS[3],XS[4],forward)
    stem=(prev,.525,.23+zoff)
    trace=(selected,.51,.21+zoff)
    w.segment(trace,(selected,-.03,.21+zoff),GOLD,1.55,a*blend_in*keep*.76)
    w.path(((xprefix,1.49,.11+zoff),(prev+.55,1.49,.11+zoff)),
           GOLD,1.6,a*prefix*.64,progress=prefix)
    w.dot(stem,GOLD,.037,a*prefix*.91)
    for k,c in enumerate(MODELS):
        y,z=YLANE[k],ZLANE[k]+zoff
        w.disk((-5.15,y,z),c,'AB'[k],.245,.145,alpha=a*blend_in,fill=.42,label_size=29)
        rail0=(stem[0]+.41,.38,.27+zoff)
        rail1=(selected-.53,y+.23,z)
        rail_end=(selected,y+.13,z)
        w.curve(stem,rail0,rail1,rail_end,
                MUTED,1.85,a*prefix*.74,prefix,True)
        tap=step(u,cu(2,.24)+.028,cu(3,.38)+.046)
        if tap>.005 and tap<.995:
            rev=1-tap
            pos=tuple(rev**3*xx+3*rev*rev*tap*yy+3*rev*tap*tap*zz+tap**3*ww
                      for xx,yy,zz,ww in zip(stem,rail0,rail1,rail_end))
            w.sphere(pos,GOLD,.047,a*prefix)
        p=mix(PROBS[k][4],PROBS[k][5],forward)
        prob(w,selected,y,z,1.55,p,c,a*blend_in,slice_open)
        if slice_open>.001:
            for b in (.32,.67):
                x=selected-.775+1.55*(p+b*(1-p))
                w.segment((x,y+.063,z-.06),(x,y-.063,z+.11),MUTED,1.05,a*slice_open*.62)
        if keep>.001:
            stayx=XS[4]-.775+1.55*PROBS[k][4]*.5
            record=(XS[4]-.18,y-.34,z+.17)
            saved=poly_move((stayx,y,z+.06),record,keep,.03)
            w.segment((XS[4]-.45,y-.34,z+.11),(XS[4]+.42,y-.34,z+.11),
                      GOLD,1.05,a*keep*.41)
            w.box(saved,(.14,.11,.15),GOLD,alpha=a*keep,fill=.76,edge=1.)
            if forward>.54:
                kx=XS[5]-.775+1.55*PROBS[k][5]*.5
                w.box((kx,y-.23,z+.12),(.14,.11,.15),GOLD,
                      alpha=a*step(forward,.54,.91),fill=.76,edge=1.)
        pnote=a*step(keep,.12,.66)*(1-step(forward,.05,.24)+step(forward,.82,.995))
        if pnote>.001:
            v=PROBS[k][4 if forward<.5 else 5]
            w.text(f'{v:.2f}',(selected-.8+.78*p,y+.28,z+.22),24,c,pnote)
    if wrong>.002:
        x=XS[4]
        y=1.17+wrong*1.02
        path=((x,1.05,.43+zoff),(x+.05,y,.93+zoff),(x+.17,y,1.10+zoff))
        w.path(path,RED,1.35,a*wrong*.56,dash=[4,7])
        w.tile(path[-1],'almost',RED,(1.22,.50,.11),
               rot=(0,.37,-.17),alpha=a*wrong,fill=.22,label_size=24)
        w.mark((x+.99,y,1.21+zoff),False,.10,a*wrong)


SIDE=2.88
AREA_Y=.27
AREA_Z=.19
LEFT=(-2.06,AREA_Y,AREA_Z)
RIGHT=(2.06,AREA_Y,AREA_Z)


def slab_coords(center,theta):
    cs,sn=math.cos(theta),math.sin(theta)
    def pos(dx,dy,h=0):
        x,y,z=center
        return x+dx,y+dy*cs-h*sn,z+dy*sn+h*cs
    return pos


def unit_slab(w,center,s=SIDE,theta=0,half=1,eighth=1,a=1,ad=1,corner=1):
    if a<.002:return
    pos=slab_coords(center,theta)
    q=s/2
    v=lambda x,y:pos(x,y)
    w.face((v(-q,-q),v(q,-q),v(q,q),v(-q,q)),MUTED,a*.67,fill=.028,edge=1.12)
    if corner>.001:
        ww=s*mix(1,.5,half)
        hh=s*mix(1,.125,eighth)
        w.face((pos(-q,q-hh,.019),pos(-q+ww,q-hh,.019),pos(-q+ww,q,.019),pos(-q,q,.019)),
               GOLD,a*corner,fill=mix(.58,.83,eighth),edge=1.72)
    if half>.003:
        w.segment(pos(0,-q,.023),pos(0,q,.023),MUTED,1.16,a*half*.68)
    if eighth>.005:
        for j in range(1,8):
            yy=q-s*j/8
            # The second cut partitions what survived the first cut.
            w.segment(pos(-q,yy,.025),pos(0,yy,.025),MUTED,.97,a*eighth*.50)
    if ad>.001:
        ah=a*half*ad
        ae=a*eighth*ad
        yy=q+.12
        w.path((pos(-q,yy-.054,.025),pos(-q,yy,.025),pos(0,yy,.025),pos(0,yy-.054,.025)),
               GOLD,1.19,ah*.93)
        x=-q-.12
        y1=q-s/8
        w.path((pos(x+.054,y1,.025),pos(x,y1,.025),pos(x,q,.025),pos(x+.054,q,.025)),
               GOLD,1.19,ae*.93)
        w.text('½',pos(-q*.50,q+.33,.064),37,GOLD,ah,font='math')
        w.text('⅛',pos(-q-.24,q-s/16,.07),36,GOLD,ae,align='right',font='math')


def early_cut(w,u,cu=None,a=1):
    cu=cu or (lambda j,f:f)
    minip=step(u,0,.18)
    two_a=ep(u,cu(0,.02),cu(0,.02)+.14,cu(4,.52)-.034,cu(4,.52)+.095)
    reach=step(u,cu(4,.52)-.065,cu(4,.52)+.13)
    half=step(u,cu(1,.15)-.024,cu(1,.15)+.075)
    eighth=step(u,cu(3,.40)-.034,cu(3,.40)+.086)
    moved=step(u,cu(6,.75)-.044,cu(6,.75)+.12)
    if minip<1:
        # The looked-at evidence remains the last object to leave the old rail.
        force(w,1,a=a*(1-minip),zoff=-3.5*minip)
    for j in range(2):
        x=(-.81,.81)[j]
        px=mix((3.01,4.42)[j],x,minip)
        zz=mix(.5,.91,minip)
        w.tile((px,1.33,zz),'',GOLD,(.79,.57,.16),(0,.32*(1-minip),0),
               a*two_a,.36)
        p=(.5,.125)[j]
        k=(half,eighth)[j]
        prob(w,x,.78,.94,1.24,p,GOLD,a*two_a,k)
        if k>.002:
            w.text(('½','⅛')[j],(x,.45,.98),29,GOLD,a*two_a*k)
    center=vlerp((0,AREA_Y,AREA_Z),LEFT,moved)
    theta=mix(.83,0,reach)
    unit_slab(w,center,SIDE,theta,half,eighth,a*reach)
    if moved>.001:
        p=poly_move((.13,AREA_Y,AREA_Z-1.9),RIGHT,moved,.05)
        unit_slab(w,p,SIDE,-.62*(1-moved),half,eighth,a*moved)
        w.text('×',(0,AREA_Y,AREA_Z+.16),49,MUTED,a*moved*.67)
    show=ep(u,cu(5,.65)-.026,cu(5,.65)+.056,cu(6,.75)-.066,cu(6,.75)-.018)
    if show>.001:
        yy=center[1]+SIDE*.429
        xx=center[0]-.06
        sx=1.99+(center[0]*.20)
        w.path(((xx,yy,AREA_Z+.04),(xx+.37,yy,AREA_Z+.04),
                (sx-.12,AREA_Y+.61,AREA_Z+.08)),GOLD,1.19,a*show*.76,progress=show)
        w.text('1 / 16',(sx,AREA_Y+.59,AREA_Z+.14),39,GOLD,a*show,
               align='left',font='math')
    prod=step(u,cu(7,.86)-.03,cu(7,.86)+.079)
    w.text('(1 / 16)²  =  1 / 256',(0,-1.63,.23),34,GOLD,a*prod)


def box_choice(w,cx=1.68,cy=.43,z=.39,a=1,spread=1):
    # One square, four equal alternatives: shared edges do the counting.
    h=.78*spread
    l,r=cx-h,cx+h
    bot,top=cy-h,cy+h
    w.face(((l,bot,z),(r,bot,z),(r,top,z),(l,top,z)),
           MUTED,a*.91,fill=.062,edge=1.50)
    w.face(((l,cy,z+.021),(cx,cy,z+.021),(cx,top,z+.021),(l,top,z+.021)),
           GOLD,a,fill=.84,edge=1.42)
    w.segment((l,cy,z+.025),(r,cy,z+.025),MUTED,1.49,a*.73)
    w.segment((cx,bot,z+.025),(cx,top,z+.025),MUTED,1.49,a*.73)


def n_vocab(w,u,a=1):
    if a<.002:return
    sizes=(.2,.17,.12,.104,.080,.066,.062,.055,.047,.038,.033,.025)
    norm=sum(sizes)
    x=-2.15
    width=3.63
    for j,p in enumerate(sizes):
        ln=width*p/norm
        cc=GOLD if j==7 else MUTED
        land=step(u,.032*j,.45+.047*j)
        dest=(x+ln/2-.006,-1.55,-1.14)
        src=(x+ln/2-.006,.25+.15*math.sin(j),-3.08-.028*j)
        p=poly_move(src,dest,land,.17)
        ink_patch(w,p,max(.005,ln-.014),.238,cc,a*land,
                  rot=(.79*(1-land),0,.21*(1-land)),
                  fill=.90 if j==7 else .16,edge=1.12)
        if j==7:
            w.segment((p[0],p[1]-.13,p[2]+.12),(p[0],p[1]-.3,p[2]+.12),GOLD,1.3,
                      a*step(land,.62,.99))
        x+=ln


def normalized_slab(w,u,cu=None,a=1):
    cu=cu or (lambda j,f:f)
    inward=step(u,.014,.205)
    stretch=step(u,cu(2,.325)-.04,cu(2,.325)+.124)
    metric=step(u,cu(3,.47)-.028,cu(3,.47)+.071)
    reciprocal=step(u,cu(4,.58)-.027,cu(4,.58)+.111)
    dist=step(u,cu(6,.89)-.04,.995)
    start=vlerp(LEFT,(0,AREA_Y,AREA_Z),inward)
    if inward<.999:
        right=poly_move(RIGHT,(.26,.43,-3.3),inward,.16)
        unit_slab(w,right,SIDE,-.79*inward,1,1,a*(1-inward))
        w.text('×',(0,.27,.32),49,MUTED,a*(1-inward)*.67)
        w.text('(1 / 16)²  =  1 / 256',(0,-1.63,.23),34,GOLD,a*(1-inward))
    pitch=.16*math.sin(stretch*PI)
    unit_slab(w,start,SIDE,pitch,1,1,a*(1-stretch),1,corner=0)
    # A 2D face in a 3D room; its exact world-space area is invariant.
    width=.5*SIDE*(.5**stretch)
    height=(SIDE*SIDE/16)/width
    from_ctr=(start[0]-SIDE/4,start[1]+7*SIDE/16,start[2]+.018)
    center=vlerp(from_ctr,(-1.66,.39,.38),stretch)
    tr=.22*math.sin(PI*stretch)
    v=slab_coords(center,tr)
    rect=tuple(v(x*width/2,y*height/2) for x,y in ((-1,-1),(1,-1),(1,1),(-1,1)))
    w.face(rect,GOLD,a,fill=mix(.83,.89,stretch),edge=mix(1.72,2.15,stretch))
    if metric>.001:
        y=-height/2-.18
        w.path((v(-width/2,y+.10),v(-width/2,y),v(width/2,y),v(width/2,y+.10)),
               GOLD,1.45,a*metric)
        w.text('¼',v(0,y-.21,.12),42,GOLD,a*metric,font='math')
    if reciprocal>.001:
        w.path(((-1.12,.39,.36),(-.41,.39,.36),(.65,.43,.36)),
               MUTED,1.65,a*reciprocal*.85,arrow=True,progress=reciprocal)
        box_choice(w,a=a*reciprocal,spread=.34+.66*reciprocal)
    done=step(u,cu(5,.77)-.018,cu(5,.77)+.081)
    w.text('PPL = 4',(1.68,-.65,.62),47,GOLD,a*done,font='math')
    n_vocab(w,dist,a*dist*.92)


BIT_PATHS=((-2.02,-.78,.41),(2.02,-.78,.41))
LIFT=.48
SIZ=.39


def bit_unit(w,p,a=1,rot=(0,0,0),size=SIZ):
    # Equal-area sheets write the integer surprise. Their round trip still
    # happens in world depth, without a specular block around each bit.
    ink_patch(w,p,size,size,GOLD,a,rot,fill=.83,edge=.72)


def book_tail(w,u,cut,a=1):
    q=step(u,.018,cut-.014)
    op=ep(u,.028,.068,cut+.035,cut+.113)
    if op<.002:return
    for j in range(16):
        t=step(q,.035*j,.37+.037*j)
        x=mix(-1.66,-3.57+.47*j,t)
        y=mix(.40,.47+.027*j,t)
        z=mix(.39,.45-.239*j,t)
        w.paper((x,y,z),.38,.52,GOLD,a*op*t,(0,.51*t,0),.31+.38*(1-j/16),.19)
    left=-3.62
    y=-.49
    w.segment((left,y,.32),(left+5.56,y,.32),MUTED,1.35,a*op*.52)
    span=.98*(2.**(-10*q))
    ink_patch(w,(left+span/2,y,.32),span,.074,GOLD,a*op,fill=.88)


def log_room(w,u,cu=None,a=1):
    cu=cu or (lambda j,f:f)
    transfer=step(u,.025,.20)
    if transfer<.999:
        normalized_slab(w,1,a=a*(1-transfer))
    book_tail(w,u,cu(1,.18),a)
    on=step(u,cu(1,.18)-.06,cu(1,.18)+.12)
    lift=step(u,cu(2,.31)-.031,cu(2,.31)+.123)
    merge=step(u,cu(4,.46)+.041,cu(5,.56)+.002)
    spread=step(u,cu(5,.56)+.010,cu(5,.56)+.116)
    exp=step(u,cu(6,.75)-.031,cu(6,.75)+.075)
    rare=step(u,cu(7,.89)-.026,.998)
    for j,(x,y,z) in enumerate(BIT_PATHS):
        p=.5 if not j else .125
        if on>.001:
            prob(w,x,1.15,.22,2.08,p,GOLD,a*on*(1-lift*.73),on)
            w.text(('½','⅛')[j],(x,1.50,.30),33,GOLD,a*on*(1-lift*.7))
        for k in range(1 if not j else 3):
            n=k if not j else k+1
            birth=step(lift,.11*k,.57+.11*k)
            lift_pos=(x,y+LIFT*k,z)
            z0=(x-1.04+p*1.04,1.15,.22)
            p0=poly_move(z0,lift_pos,birth,.16)
            join=(0,-.79+n*LIFT,.44)
            split=(-1.12 if n<2 else 1.12,-.79+LIFT*(n%2),.44)
            p1=poly_move(p0,join,merge,.20)
            p2=poly_move(p1,split,spread,.09)
            bit_unit(w,p2,a*birth*(1-.52*rare),rot=(0,.48*math.sin(PI*merge),0),
                     size=SIZ*(.65+.35*birth))
    w.text('PPL = 2² = 4',(0,-1.48,.39),40,GOLD,a*exp*(1-.43*rare),font='math')
    if rare>.002:
        for i in range(6):
            k=step(rare,.072*i,.47+.09*i)
            yy=-.94+i*.47
            pos=(3.56,yy,-.79)
            bit_unit(w,(pos[0],mix(-1.02,yy,k),pos[2]),a*k,size=.35)
        w.text('p → 0',(3.56,-1.44,-.68),28,GOLD,a*rare,font='math')


LOSS_Y=-1.42
LOSS_SCALE=.558
LOSS_Z=-.42


def loss_points():
    banks=[]
    for j in range(2):
        p=[(-5.09,LOSS_Y,LOSS_Z)]
        loss=0.
        for x,pr in zip(XS,PROBS[j]):
            loss-=math.log2(pr)
            p.append((x,LOSS_Y+LOSS_SCALE*loss,LOSS_Z))
        banks.append(tuple(p))
    return tuple(banks)


LOSSES=loss_points()


def cumulative(w,u,cu=None,a=1):
    cu=cu or (lambda j,f:f)
    enter=step(u,.01,.17)
    burn=step(u,cu(1,.15)-.01,cu(2,.30)-.015)
    last=step(u,cu(2,.30)-.025,cu(2,.30)+.107)
    result=step(u,cu(4,.55)-.022,cu(4,.55)+.070)
    look=step(u,cu(5,.68)-.011,cu(5,.68)+.16)
    pick=step(u,cu(6,.76)-.017,cu(6,.76)+.11)
    if enter<.999:
        log_room(w,1,a=a*(1-enter))
    aa=a*enter
    if aa<.002:return
    yshift=.83*(1-look)
    prompt_track(w,aa,(0,yshift,0),only=(5,) if look>.67 else None)
    plot=aa*(1-look)
    x0=-5.09
    if plot>.001:
        w.path(((x0,1.09,LOSS_Z),(x0,LOSS_Y,LOSS_Z),(4.99,LOSS_Y,LOSS_Z)),MUTED,1.65,plot*.68)
        for j in range(1,5):
            yy=LOSS_Y+LOSS_SCALE*j
            w.segment((x0,yy,LOSS_Z),(4.73,yy,LOSS_Z),GRID,1.03,plot*.56)
        w.text('bits',(x0+.096,.939,LOSS_Z),23,MUTED,plot*.88,align='left')
        w.text('0',(x0-.13,LOSS_Y-.10,LOSS_Z),20,MUTED,plot*.85,align='right')
        lo,hi=cu(3,.34),cu(4,.46)
        trace=1-step(u,hi-.02,hi+.034)
        for n in range(1,6):
            start=mix(lo-.01,hi-.042,(n-1)/5)
            strength=step(u,start,start+.043)*trace
            pa,pb=LOSSES[0][n],LOSSES[1][n]
            if strength>.001:
                w.path((pa,pb),GOLD,1.55,plot*strength*.64,progress=strength)
        # Compare the final heights on the graph's one measurement plane.
        compare=step(u,hi-.024,cu(5,.62)-.019)
        if compare>.001:
            sa,sb=LOSSES[0][-1],LOSSES[1][-1]
            ra=(sa[0]-.16,sa[1],LOSS_Z);rb=(ra[0],sb[1],LOSS_Z)
            for p,q,c in ((sa,ra,BLUE),(sb,rb,PURPLE)):
                w.path((p,q),c,1.53,plot*compare*.73,progress=compare)
            w.path((ra,rb),GOLD,1.65,plot*compare*.82,progress=compare)
    prog=(5*burn+last)/6
    for k,c in enumerate(MODELS):
        pts=LOSSES[k]
        w.path(pts,c,2.75,plot*.95,progress=prog)
        for j,p in enumerate(pts):
            q=step(prog,j/6-.085,j/6)
            if q>.001:
                w.dot(p,c,.047 if j<6 else .075,plot*q)
        end=pts[-1]
        if result>.001:
            at=(end[0]+.14,end[1]-.27,end[2]+.32)
            w.text('1.272' if not k else '1.589',at,34,c,plot*result)
            w.text('PPL',(at[0]-.89,at[1],at[2]),21,MUTED,plot*result)
        # The last path bead turns into its model's answer at that depth.
        dx=3.46
        a0=(x0+.26+.74*k,LOSS_Y-.46,LOSS_Z)
        ad=(dx,YLANE[k],ZLANE[k])
        dp=poly_move(a0,ad,look,.14)
        w.disk(dp,c,'AB'[k],mix(.28,.35,look),.15,alpha=aa*(.87+.13*look),fill=.36,label_size=30)
        if look>.002:
            ay,az=YLANE[k],ZLANE[k]
            w.segment((dx+.39,ay,az),(XS[5]-.56,ay,az),MUTED,1.6,aa*look*.67)
            sz=mix(end[2],az,pick)
            score_mark(w,XS[5],ay,sz,k,aa*look*pick)
    if look>.001:
        w.path(((XS[5],.54,.24),(XS[5],.31,.37),(XS[5],.04,ZLANE[0])),
               GOLD,1.6,aa*look*.64)
        w.path(((XS[5],.54,.19),(XS[5],.31,-.1),(XS[5],-.70,ZLANE[1])),
               GOLD,1.6,aa*look*.58)


WORD='sunrise'
DX=.82
LETTER_X=tuple((j-3)*DX for j in range(7))
MATCH_CUTS=((0,3,7),(0,1,3,5,7))


def letter_rulers(w,u,cu=None,a=1):
    cu=cu or (lambda j,f:f)
    hand=step(u,0,.19)
    dwell=step(u,cu(1,.15)-.04,cu(1,.15)+.125)
    bytes_appear=step(u,cu(3,.37)-.046,cu(3,.37)+.12)
    if hand<.999:
        old=(1-hand)*a
        prompt_track(w,old,omit=(5,),only=(5,))
        w.path(((XS[5],.54,.24),(XS[5],.31,.37),(XS[5],.04,ZLANE[0])),
               GOLD,1.6,old*.64)
        w.path(((XS[5],.54,.19),(XS[5],.31,-.1),(XS[5],-.70,ZLANE[1])),
               GOLD,1.6,old*.58)
        for j,c in enumerate(MODELS):
            w.disk(poly_move((3.46,YLANE[j],ZLANE[j]),(2.74,YLANE[j],ZLANE[j]-2),hand,.23),
                   c,'AB'[j],.35,.15,rot=(0,.9*hand,0),alpha=old,fill=.36,label_size=30)
            w.segment((3.85,YLANE[j],ZLANE[j]),(XS[5]-.56,YLANE[j],ZLANE[j]),
                      MUTED,1.6,old*.67)
            score_mark(w,XS[5],YLANE[j],ZLANE[j]-2*hand,j,old)
    shift=4.40*(1-hand)
    g_y=mix(.93,.92,hand)
    width=mix(1.39,7*DX,hand)
    lift=1-step(bytes_appear,.1,.53)
    strip=step(hand,.26,.85)
    if lift>.001:
        w.tile((shift,g_y-.28*strip,.22),'four' if hand<.49 else '',GOLD,
               (width,mix(.68,.028,strip),mix(.17,.045,strip)),
               (0,.12*math.sin(PI*hand),0),a*lift,mix(.84,.58,hand),label_size=46)
    for j,x in enumerate(LETTER_X):
        # The continuous text plate is wider than the individual letters.
        # Keep its glyphs in the foreground even during the side-on reveal.
        w.text(WORD[j],(x+shift,g_y,.42),47,INK,a*step(hand,.58+.035*j,.76+.032*j),
               font='math',depth_bias=.94)
        if bytes_appear>.001:
            y=g_y-.303
            lead_rule(w,(x+shift-.34,y,.28),(x+shift+.34,y,.28),GOLD,a*bytes_appear*.83)
    unit_a=1-step(bytes_appear,.31,.96)
    for j,col in enumerate(MODELS):
        y=(.18,-.80)[j]
        z=(.55,-.33)[j]
        position=step(u,cu(1,.15)-.086+j*.064,cu(1,.15)+.092+j*.067)
        left=LETTER_X[0]-.5*DX
        bx=mix(2.84,-3.40,position)
        if position>.001:
            w.disk((bx,y,z),col,'AB'[j],.29,.15,alpha=a*position,fill=.37,label_size=27)
        rz=z+.06
        for n,(lo,hi) in enumerate(zip(MATCH_CUTS[j],MATCH_CUTS[j][1:])):
            ww=(hi-lo)*DX
            x=left+lo*DX+ww/2
            yy=mix(g_y-.018,y,position)
            q=a*position*unit_a
            lead_rule(w,(x-(ww-.09)/2,yy,rz),(x+(ww-.09)/2,yy,rz),col,q*.91)
        w.text(str(len(MATCH_CUTS[j])-1),(3.40,y,rz+.08),34,col,a*position*unit_a*dwell)
        if bytes_appear>.001:
            p=(.50,.70)[j]
            for x in LETTER_X:
                prob(w,x,y,z,.74,p,col,a*bytes_appear,bytes_appear)
            w.text(f'{p:.1f}',(3.48,y,rz+.14),34,col,a*bytes_appear)
    if bytes_appear>.001:
        w.text('bits / byte',(3.48,-1.33,.04),22,MUTED,a*bytes_appear,font='math')


def file_tile(w,p,kind='chat',scale=1,a=1,rot=(0,0,0)):
    x,y,z=p
    if a<.002:return
    w.paper(p,.95*scale,1.17*scale,GOLD,a,rot,.69,.20)
    zf=z+.060
    ink='#211C13'
    if kind=='math':
        w.text('∑',(x,y,zf),42*scale,ink,a)
    elif kind=='mail':
        ww=.29*scale
        hh=.18*scale
        pts=((x-ww,y+hh,zf),(x+ww,y+hh,zf),(x,y-.055*scale,zf),(x-ww,y+hh,zf),
             (x-ww,y-hh,zf),(x+ww,y-hh,zf),(x+ww,y+hh,zf))
        w.path(pts,ink,1.35,a*.86)
    else:
        ww=.244*scale
        hh=.137*scale
        pts=((x-ww,y-hh,zf),(x-.14*scale,y-hh,zf),(x-.21*scale,y-.24*scale,zf),
             (x-.035*scale,y-hh,zf),(x+ww,y-hh,zf),(x+ww,y+hh,zf),
             (x-ww,y+hh,zf),(x-ww,y-hh,zf))
        w.path(pts,ink,1.38,a*.86)
        for k in (-1,0,1):
            w.dot((x+.102*scale*k,y,zf+.011),ink,.014*scale,a*.9)


def doc_stack(w,x,y,z,kind,a=1,m=.0,direction=1):
    """Keep two files present; extras advance or retire in depth."""
    if a<.002:return
    for j in range(5,-1,-1):
        extra=(0 if j<2 else m)
        px=x+direction*j*.16*min(1,.53+.47*extra)
        py=y+j*.10
        pz=z-.193*j-(0 if j<2 else 2.32*(1-m))
        file_tile(w,(px,py,pz),kind,.91,a*(1 if j<2 else m))


def domain_points(m):
    chat=mix(.75,.25,m)
    q=(chat+3*(1-chat),2*chat+1-chat)
    return tuple((-2.85+2.81*(val-1),-1.02,(.54,-.26)[j]) for j,val in enumerate(q))


def domains(w,u,cu=None,a=1,draw_models=True):
    cu=cu or (lambda j,f:f)
    mixd=step(u,cu(6,.73)-.028,cu(6,.73)+.11)
    deck=step(u,cu(4,.53)-.04,cu(4,.53)+.125)
    if deck<.998:
        letter_rulers(w,u,cu,a*(1-deck))
    if deck<.002:return
    x1=mix(-.80,-2.63,deck)
    x2=mix(.80,2.60,deck)
    doc_stack(w,x1,.67,.60,'chat',a*deck,1-mixd,-1)
    doc_stack(w,x2,.67,-.23,'math',a*deck,mixd,1)
    axis=step(u,cu(5,.62)-.027,cu(5,.62)+.093)
    w.path(((-3.28,-1.46,0),(-1.44,-1.46,0),(1.18,-1.46,0),(3.37,-1.46,0)),
           MUTED,1.6,a*deck*axis,arrow=True,progress=axis)
    if axis>.001:
        for j in range(3):
            tx=-2.85+j*2.81
            w.segment((tx,-1.52,.015),(tx,-1.38,.015),MUTED,1.45,a*deck*axis)
            w.text(str(1+j),(tx,-1.76,.085),20,MUTED,a*axis*deck)
        w.text('bits / token',(3.44,-1.73,.088),21,MUTED,a*axis*deck)
    if draw_models:
        for j,p in enumerate(domain_points(mixd)):
            w.segment((p[0],-1.44,p[2]),p,MODELS[j],1.35,a*axis*deck*.71)
            w.disk(p,MODELS[j],'AB'[j],.28,.15,alpha=a*axis*deck,fill=.34,label_size=25)
    name=step(u,cu(7,.86)-.013,cu(7,.86)+.081)
    w.text('Paloma',(0,1.64,.10),34,INK,a*name)


COST=( (-3.576,-.07,.03),(2.68,1.07,.01) )
CORE=((-2.45,0,0),(2.45,0,0))


def dial(w,p,a=1):
    x,y,z=p
    w.disk(p,GOLD,'',.234,.095,alpha=a,fill=.10,label_size=17)
    w.path(((x,y+.12,z+.075),(x,y,z+.075),(x+.098,y-.056,z+.075)),GOLD,1.5,a)


def budget(w,u,cu=None,a=1):
    cu=cu or (lambda j,f:f)
    stage=step(u,.015,.172)
    enter=step(u,cu(1,.15)-.04,cu(1,.15)+.082)
    line=step(u,cu(2,.255)-.04,cu(2,.255)+.112)
    lock=step(u,cu(3,.365)-.02,cu(3,.365)+.085)
    open_=step(u,cu(5,.60)-.051,cu(5,.60)+.13)
    inputs=step(u,cu(6,.72)-.034,cu(6,.72)+.09)
    splice=step(u,cu(7,.86)-.023,cu(7,.86)+.12)
    if stage<.999:
        domains(w,1,a=a*(1-stage),draw_models=False)
    if stage>.001:
        for j in range(4):
            xx=mix(-2.63+ .15*j,-.83+.12*j,stage)
            py=mix(.66+.10*j,1.41+.06*j,stage)
            zz=mix(.58-.19*j,.56-.16*j,stage)
            file_tile(w,(xx,py,zz),'mail',.67,a*ep(u,.045,.115,.20,.34))
    aa=a*enter*(1-open_)
    if aa>.001:
        z=-.54
        w.path(((-4.47,-1.48,z),(-4.47,1.59,z)),MUTED,1.7,aa*.88,arrow=True,progress=enter)
        w.path(((-4.47,-1.48,z),(4.40,-1.48,z)),MUTED,1.7,aa*.88,arrow=True,progress=enter)
        w.text('accuracy',(-4.45,1.84,z+.04),23,MUTED,aa,align='left')
        w.text('cost / letter',(4.42,-1.82,z+.08),23,MUTED,aa,align='right')
        for j,(x,y,_) in enumerate(COST):
            cc=MODELS[j]
            f=aa*(1-.5*lock*j)
            w.segment((x,y,z),(x,-1.48,z),cc,1.24,f*.62,dash=[4,7])
            w.segment((-4.47,y,z),(x,y,z),cc,1.24,f*.62,dash=[4,7])
            w.text(('74%','82%')[j],(-4.68,y,z+.04),25,cc,f,align='right',font='math')
            w.text(('¢1','¢8')[j],(x,-1.77,z+.06),24,cc,f,font='math')
        x=mix(4.9,.62,line)
        soft=aa*step(line,0,.21)
        w.face(((x,-1.49,-1.77),(x,-1.49,1.73),(x,1.48,1.73),(x,1.48,-1.77)),
               GOLD,soft*.38,fill=.10,edge=1.52)
        w.segment((x,-1.49,z),(x,1.57,z),GOLD,1.95,soft*.9)
        w.mark((3.29,1.07,.40),False,.135,aa*lock)
    for j,c in enumerate(MODELS):
        p=poly_move(domain_points(1)[j],COST[j],stage,.17)
        p=poly_move(p,CORE[j],open_,.065)
        aa=a*(1-.48*lock*j*(1-open_))
        if open_<.998:
            w.disk(p,c,'AB'[j],mix(.28,.38,stage),.15,
                   rot=(0,(-1+2*j)*.74*open_,0),alpha=aa*(1-open_*.34),fill=.34,
                   label_size=mix(25,31,stage))
        if open_>.001:
            h=(p[0]+(-1+2*j)*.52*open_,p[1]+.21*open_,p[2]-.61*open_)
            w.disk(h,c,'',.39,.12,rot=(0,(-1+2*j)*.84*open_,0),alpha=a*open_*.75,fill=.18)
            loc=(p[0],p[1],p[2]+.09)
            if j:
                tri(w,*loc,c,a*open_)
                w.box((p[0]-.18*splice,.24*splice,.08),(.24,.24,.24),c,
                      alpha=a*splice,rot=(.6*splice,.4*splice,.8*splice),fill=.37)
            else:
                w.box(loc,(.54,.54,.31),c,alpha=a*open_,
                      rot=(.24,.31*splice,.36),fill=.44,edge=1.5)
    if inputs>.001:
        yy=mix(2.08,1.41,inputs)
        for j in (2,1,0):
            file_tile(w,(-.40+.102*j,yy+.073*j,-.08-.105*j),'mail',.55,a*inputs)
        dial(w,(.73,yy+.08,.04),a*inputs)
        src=(0,.69,.07)
        w.path(((-.38,yy-.34,-.03),(-.38,.84,.07),(0,.84,.07),src),
               MUTED,1.5,a*inputs*.91,progress=inputs)
        w.path(((.72,yy-.16,.05),(.72,.84,.07),(0,.84,.07)),MUTED,1.5,a*inputs*.91,progress=inputs)
        w.dot(src,GOLD,.040,a*inputs)
        pulse=step(u,cu(6,.72)+.04,cu(6,.72)+.18)
        for j,goal in enumerate(CORE):
            w.path((src,(goal[0],.69,.07),(goal[0],.35,.07)),MUTED,1.6,a*inputs*.81,progress=inputs)
            packet(w,src,(goal[0],.69,.07),pulse,alpha=a*inputs*.98,r=.073)


def question_planes(w,u,a=1):
    if a<.002:return
    pos=(0,-.24,0)
    extend=step(u,.06,.50)
    for j in range(9,-1,-1):
        q=step(extend,j*.080,.17+j*.089)
        if q<.002:continue
        p=(pos[0]+.055*(j-4.5)*q,pos[1],pos[2]+(j-4.5)*.19*q)
        w.grid(p,10,10,.19,'xy',GOLD,alpha=a*q*(.37+.037*j),width=.90)
        s=.95
        u0=(p[0]-s,p[1]-s,p[2]);u1=(p[0]+s,p[1]-s,p[2])
        u2=(p[0]+s,p[1]+s,p[2]);u3=(p[0]-s,p[1]+s,p[2])
        w.path((u0,u1,u2,u3,u0),GOLD,1.32,a*q*(.50+.05*j))


def terminal(w,u,cu=None,a=1):
    cu=cu or (lambda j,f:f)
    enter=step(u,.008,.185)
    count=step(u,cu(1,.18)-.035,cu(1,.18)+.17)
    check=step(u,cu(2,.39)-.025,cu(2,.39)+.14)
    rise=step(u,cu(3,.59)-.031,cu(3,.59)+.128)
    close=step(u,cu(4,.83)-.017,.996)
    if close>.999:
        w.anchor(a)
        return
    if enter<.999:
        budget(w,1,a=a*(1-enter))
    b=a*enter*(1-close)
    if b>.001:
        question_planes(w,u,b*count*(1-.62*rise))
        if check>.001:
            w.text('10 × 10 × 10',(0,-1.65,1.07),29,GOLD,b*count*check*(1-.82*rise),font='math')
        if rise>.001:
            top=(0,1.66,.08)
            w.path(((-3.57,top[1],.08),(0,top[1],.08),(3.57,top[1],.08)),
                   MUTED,1.65,b*rise*.74,progress=rise)
            for j,c in enumerate(MODELS):
                p=CORE[j]
                yy=mix(-.29,1.66,(.981,.99)[j])
                w.segment((p[0],-.29,.02),(p[0],top[1],.02),MUTED,1.18,b*rise*.46)
                w.dot((p[0],yy,.06),c,.046,b*step(rise,.66,.99))
                w.text(('98.1%','99.0%')[j],(p[0],.19,.13),24,c,b*step(rise,.72,1),font='math')
    k=enter
    for j,c in enumerate(MODELS):
        p=CORE[j]
        yy=mix(0,mix(-.29,1.66,(.981,.99)[j])-.46,rise)
        pos=(p[0],yy*(1-close),0)
        w.disk(pos,c,'AB'[j],mix(.34,.42,k),.15,alpha=a*k,fill=.34,label_size=34)
    anchor_tile=(0,mix(.90,0,step(u,0,.16)),mix(.32,0,step(u,0,.16)))
    w.tile(anchor_tile,'four' if u<.19 else '',GOLD,(.96,.67,.14),
           (0,.49*math.sin(PI*count)*(1-close),0),a*k*(.99-.74*count*(1-close)),.33)


def draw(g,i,t,duration):
    u,cu=timing(g,t,duration,i)
    if i==0:
        open_lens=step(u,.017,.264)
        answer_lens=step(u,cu(1,.38)+.015,.945)
        w=cam(g,interp(interp(C0,CW,open_lens),C1,answer_lens))
        hero(w,u,cu(2,.58),cu(3,.81))
    elif i==1:
        q=step(u,.01,.82)
        w=cam(g,interp(C1,CF,q))
        force(w,u,cu)
    elif i==2:
        q=step(u,.04,.92)
        one=ep(u,.14,.40,cu(6,.75)-.02,cu(6,.75)+.13)
        w=cam(g,interp(interp(CF,CA,q),(.21,.29,1.06,(.08,.25,.12)),one))
        early_cut(w,u,cu)
    elif i==3:
        q=step(u,.031,.72)
        one=ep(u,.222,.36,cu(4,.58)-.091,cu(4,.58)+.081)
        lens=interp(interp(CA,CS,q),(-.06,.11,1.63,(-1.54,.30,.12)),one)
        lens=interp(lens,CV,step(u,cu(6,.80)-.022,.993))
        w=cam(g,lens)
        normalized_slab(w,u,cu)
    elif i==4:
        q=step(u,.065,.945)
        w=cam(g,interp(CV,CL,q))
        log_room(w,u,cu)
    elif i==5:
        q=step(u,.01,.295)
        rr=step(u,cu(5,.68)-.016,.987)
        inspect=ep(u,cu(3,.34)-.028,cu(4,.46)+.016,cu(4,.46)+.036,cu(5,.62)+.029)
        trace=interp(interp(CL,CR,q),(-.06,.32,.93,(.05,.045,.10)),inspect)
        w=cam(g,interp(trace,CY,rr))
        cumulative(w,u,cu)
    elif i==6:
        q=step(u,.024,.45)
        rr=step(u,cu(4,.53)-.04,.96)
        mid=(.05,.12,.97,(.11,.01,.16))
        w=cam(g,interp(interp(CY,mid,q),CD,rr))
        domains(w,u,cu)
    elif i==7:
        q=step(u,.01,.43)
        rr=step(u,cu(5,.60)-.03,.94)
        w=cam(g,interp(interp(CD,CC,q),CE,rr))
        budget(w,u,cu)
    else:
        orbit=step(u,.06,.50)
        close=step(u,cu(4,.83)-.017,.996)
        middle=(.43,.29,.91,(0,.08,.063))
        w=cam(g,interp(interp(CE,middle,orbit),END,close))
        terminal(w,u,cu)
    w.draw()
