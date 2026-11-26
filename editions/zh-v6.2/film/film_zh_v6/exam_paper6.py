"""Three changes to the exam, phrased by the objects rather than by a slide header."""
from rig4 import *
from motion6 import ArcLength

def options(g,c,end):
    t=c.t
    judge=c.at('第二刀')
    difficulty=c.at('第三刀')
    if t<judge-.08:
        repairs(g,c,judge)
    elif t<difficulty-.08:
        distractors(g,c,judge,difficulty)
    else:
        reasoning(g,c,difficulty,end)


def repairs(g,c,leave):
    t=c.t
    first=c.at('第一刀')
    unclear=c.at('表述不清')
    wrong=c.at('标错答案')
    only=c.at('要求只选一个')
    tie=c.at('两种解释都成立')
    unfit=c.at('机器判出来')
    span=c.at('清理出局')
    hold=1-phase(t,.55,1.30)
    if hold:
        if t<.08:
            endpaper(g,'3-1',op=1.)
        else:
            endpaper(g,'3-1',dx=-16*(1-hold),sc=1.+.029*(1-hold),op=hold)
    p=easepos(t,.72,1.35)
    sep=easepos(t,first-.12,.82)
    retire=1-phase(t,leave-.68,leave-.12)
    if p and retire:
        tag=enter(t,c.at('MMLU-Pro')-.12,.51)
        X=237
        y=220+18*(1-sep)
        # The ceiling from the old paper has become the two active lanes.
        for i,(a,b,col) in enumerate(((X,754,C),(902,1419,V))):
            tick=transit((X-12,218),(a,y),sep,16+11*i)
            pts=[tick,(b,y)]
            path(g,pts,p,col,2.4,retire*p*(.69+.25*i))
            if tag and not i:mark(g,'MMLU-Pro',X,178,33,t-c.at('MMLU-Pro')+.10,C,'left','pen',.55,retire*p)
        if t<unclear-.13:
            # Folding a holder is a moving prop, not yet another text box.
            for j,col in enumerate((C,V)):
                b=enter(t,first-.19+.13*j,.53)
                x=X+493+670*j
                path(g,[(x-45,y-9),(x,y-9),(x+18,y-27)],b,col,2.4,b*retire)
    z=enter(t,unclear-.20,.61)*retire
    first_dx=34*easepos(t,only-.19,.84)
    if z:
        xx=480+first_dx
        yy=463
        label(g,'从 2、4 里挑一个离 3 最近的',xx,315,39,F,z,limit=642)
        xs=[xx-171,xx,xx+171]
        path(g,[(xs[0]-40,yy),(xs[-1]+40,yy)],easepos(t,unclear-.10,.82),M,2.65,z)
        for i,nn in enumerate('234'):
            X0=xs[i]
            bold=enter(t,only-.15,.56)*float(i!=1)
            co=Y if i==1 else (T if i==0 else C)
            if i==1:
                # Three is the reference, never one of the two available choices.
                ring(g,X0,yy,8.7,Y,z,2.1)
                line(g,(X0,yy-8),(X0,yy-29),Y,1.8,z)
                mark(g,nn,X0,yy-61,43,t-unclear+.10,Y,mode='wave',dur=.45,op=z)
            else:
                point(g,X0,yy,7.7,co,z)
                line(g,(X0,yy+10),(X0,yy+30),co,1.8,z)
                mark(g,nn,X0,yy+69,55,t-unclear+.14-.07*i,co,mode='wave',dur=.45,op=z)
                if bold:ring(g,X0,yy,14.,co,z*bold,2.03)
        compare=enter(t,tie-.22,.58)
        if compare:
            for i in (0,1):
                x,y=xs[i:i+2];Y_=yy+139
                p0=phase(t,tie-.22+.20*i,tie+.58+.20*i)
                path(g,[(x,Y_-8),(x,Y_),(y,Y_),(y,Y_-8)],p0,T if not i else C,2.37,z)
                label(g,'1',mix(x,y,.5),Y_+35,32,F,compare*z)
        bad=enter(t,unfit-.17,.58)
        if bad:
            # Sweep gently over the "choose one" position; both equal distances stay true.
            point(g,xs[1]-80,663,4.8,O,z*bad)
            label(g,'两项同样近',xs[1],663,29,O,z*bad)
    z=enter(t,wrong-.23,.58)*retire
    if z:
        Y0=366
        x=1099
        u=enter(t,wrong-.18,.52)
        label(g,'2²',x-8,302,69,F,z)
        for j in range(4):
            xx=x-89+j%2*92
            yy=Y0+j//2*88
            w=enter(t,wrong-.12+.09*j,.54)
            if w:
                rect(g,xx,yy,80,75,inkcol(V,.62+.21*w),z*w)
                if j==3 and w>.3:
                    path(g,[(xx,yy),(xx+80,yy),(xx+80,yy+75),(xx,yy+75),(xx,yy)],w,T,2.35,z*.84)
        lab=enter(t,wrong+.38,.53)
        label(g,'标答 3',x+216,430,37,O,z*lab)
        bl=enter(t,span-.18,.56)
        if bl:
            path(g,[(x+155,466),(x+266,394)],bl,R,4.9,z)
            mark(g,'4',x+218,509,53,t-span+.15,T,mode='pen',dur=.55,op=z*bl)
    if t>=span-.08 and retire:
        # A single stamp highlights bad material rather than erasing the example
        # before the voice has finished explaining it.
        a=enter(t,span-.10,.52)*(1-phase(t,tie-.36,tie+.34))
        if a:
            path(g,[(910,616),(976,657)],a,R,2.55,retire*.80)


def opts_pos(i,move):
    x=475+158*(i%5)
    if i<4:
        return (mix(390+230*i,x,move),382-33*sin(pi*move)*(-1 if i%2 else 1))
    return (x,382 if i<5 else 512)


def piece(g,ch,x,y,span,col,op):
    # Large readable faces. Sharp colour edges carry party and rank, not decoration.
    if not op:return
    rect(g,x-span/2,y-45,span,90,inkcol(col,.43+.15*op),op*.94)
    path(g,[(x-span/2,y+45),(x-span/2,y-45),(x+span/2,y-45),(x+span/2,y+45),(x-span/2,y+45)],1,col,2.5,op)
    label(g,ch,x,y+1,48,F,op)


def distractors(g,c,begin,leave):
    t=c.t;i_at=c.at('这四个选项')
    open_=c.at('位置拉开')
    add=c.at('补上新的')
    enter_=enter(t,begin-.07,.70)
    u=easepos(t,open_-.26,1.21)
    for i in range(10):
        # The fifth slot cannot reveal under the outgoing D tile.
        at=begin-.03+.081*i if i<4 else max(add-.18,open_+.66)+.089*(i-4)
        f=enter(t,at,.52)
        if not f:continue
        # Existing four seats move along crossed but disjoint arcs.
        px,py=opts_pos(i,u)
        if i<4:
            arrive=easepos(t,at,.68)
            x=px-(i-1.5)*16*(1-arrive)
            py=py-167*(1-arrive)
        else:
            x=px+17*(1-f);py+=53*(1-f)
        piece(g,chr(65+i),x,py,mix(117,98,u) if i<4 else 98,C if i<4 else O,f)
        if i<4:
            wave=during(t,i_at-.13+i*.28,i_at+.77+i*.28,.33)
            if wave>0:path(g,[(x-29,py+58),(x+29,py+58)],wave,T,2.5,enter_*wave)
    luck(g,c,1.)


def luck(g,c,fade):
    t=c.t
    n4=c.at('百分之二十五')
    n10=c.at('百分之十')
    n0=enter(t,n4-.19,.58);n1=enter(t,n10-.18,.55)
    if n0 and fade:
        # A full equally weighted unit, cut again into ten. The highlighted
        # interval is one slot's exact share, not a gauge moving at random.
        x=381;w=843;y=664
        r=easepos(t,n10-.19,.70);j0=4 if r<.50 else 10
        path(g,[(x,y),(x+w,y)],n0,M,2.0,n0*fade)
        for i in range(j0+1):
            xx=x+w*i/j0;line(g,(xx,y-9),(xx,y+10),M,1.45,n0*fade*(.58+.42*abs(2*r-1)))
        end=mix(x+w/4,x+w/10,r)
        rect(g,x,y-11,(end-x)*n0,23,inkcol(Y,.75),n0*fade)
        mark(g,'25%',x+240,714,36,t-n4+.15,F,'left',op=n0*fade)
        if n1:mark(g,'→ 10%',x+431,714,36,t-n10+.16,Y,'left',op=n1*fade)


def reasoning(g,c,begin,end):
    t=c.t
    n=c.at('需要走好几步')
    s=c.at('只交一个字母')
    r=c.at('先把推理做完')
    o=1-phase(t,end-.57,end-.05)
    gather=easepos(t,begin-.08,.83)
    final=(1285,429)
    for i in range(10):
        x,y=opts_pos(i,1.)
        col=C if i<4 else O
        if i==1:
            flight=easepos(t,begin+.18,.83)
            px,py=transit((x,y),final,flight,117.)
            piece(g,'B',px,py,98,blend(C,Y,flight),o)
        elif gather<1:
            px,py=transit((x,y),(x-171+41*(i%5),y+105+57*(i//5)),gather,28.+2*i)
            piece(g,chr(65+i),px,py,98*(1-.19*gather),col,(1-gather)**1.35)
    srcs=((277,488),(557,326),(849,500),(1052,421),(1223,428))
    luck(g,c,1.-phase(t,n-.58,n+.25))
    hz=easepos(t,n-.18,1.16)
    uptake=easepos(t,r-.12,1.16)
    if hz:
        spirit=enter(t,n-.20,.51)
        for j,p in enumerate(srcs[:-1]):
            u=enter(t,n-.15+.16*j,.48)
            if u:
                col=(C,T,V,Y)[j]
                point(g,*p,11.+2*j,col,o*u)
                path(g,[p,lerp(p,srcs[j+1],.90)],u,col,2.74,o*u)
        if uptake:
            coords=(*srcs,final)
            vx,vy=ArcLength(coords).at(uptake)
            if uptake<1:point(g,vx,vy,9.,Y,o*spirit)
            if uptake>.78:ring(g,*final,74+.14*15*uptake,Y,o*(uptake-.78)*3.,2.3)
    h=enter(t,s-.19,.54)
    if h:path(g,[(1237,491),(1334,491)],h,Y,3.8,o*h)
    if uptake:
        label(g,'过程',303,596,29,T,o*uptake)
        label(g,'交 B',final[0],596,28,Y,o*uptake)
