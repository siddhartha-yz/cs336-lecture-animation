"""Act IV — follow one test item back into the archive, then forward to a real job."""
import math
from spatial import *
from act1 import prompt_track,prediction_lanes,XS,YLANE,ZLANE
PI=math.pi
HOLDS=(1.75,1.65,1.65,1.55,1.80,.70,1.70,1.65,2.0)
CAMS=(
 (0,0,1,(0,0,0)), (.36,.21,1.03,(0,.05,0)),
 (.03,.27,1.05,(0,-.03,0)),(-.42,.27,.91,(.1,.03,-.24)),
 (.32,.16,.98,(0,.02,0)),(.03,.12,.95,(.03,.0,.08)),
 (-.15,.22,.96,(0,.05,0)),(-.35,.28,.93,(.05,0,.17)),
 (.13,.15,1.03,(.12,.0,.03)),(.165,.230,.94,(.53,.035,.12)),
)
# A single archival object passes through each section. Geometry changes shape at the splice.
SEAMS=((0,0,0),(.35,.04,.10),(.15,.31,.19),(-.38,.12,.20),
       (0,.15,.40),(.42,-.12,.22),(2.91,.32,.22),(.24,-.42,.31),
       (3.55,.14,.25),(5.98,.93,.22))
SL0=(1.54,1.91,.19)
def swing(g,i,u,magnitude=0,zoom_bump=0,shift=(0,0,0)):
    a,b=CAMS[i:i+2]
    s=step(u,0,1)
    yaw=mix(a[0],b[0],s)+magnitude*math.sin(PI*s)
    return World(g,yaw,mix(a[1],b[1],s),mix(a[2],b[2],s)+zoom_bump,add(vlerp(a[3],b[3],s),shift),distance=13)
def inout(u,a,b,c,d):return step(u,a,b)*(1-step(u,c,d))
def qcue(g,u,k,f,duration,speech,width=.16):
    actual=g.part(k,f*speech/duration)*duration/speech
    return step(u,max(0,actual-width*.27),max(.015,actual+width*.73))
def passage(g,i,t,duration):
    speech=g.speech or duration-HOLDS[i]
    if i==8 and not g.speech:speech-=3.1
    return clamp(t/max(speech,.01)),lambda k,v,w=.16:qcue(g,clamp(t/max(speech,.01)),k,v,duration,speech,w)

def page(w,p,c=GOLD,alpha=1,scale=1,rot=(0,0,0),kind=0,label=''):
    """The archive receipt is marked differently from an unseen work packet."""
    if alpha<.002:return
    m=rotation(tuple(rot));a=SL0
    def pos(local):return add(p,trans(mul(local,scale),m))
    fill=.83 if c!=MUTED else .76
    w.paper(p,a[0]*scale,a[1]*scale,c,alpha,rot,fill,cut=.24*scale)
    z=.041;dep=w.project(p)[2]+.046
    ink='#262523';rule='#514E48'
    def ln(a,b,color=rule,d=1.10,opacity=1):
        w.segment(pos((*a,z)),pos((*b,z)),color,d,alpha*opacity,sort_depth=dep)
    def words(txt,x,y,size,color=ink,align='center',bold=False):
        w.ink(txt,pos((x,y,z)),m,size*scale,color,alpha,align,
              'bold' if bold else 'medium',sort_depth=dep+.003)
    if kind in (1,2):
        words('Shipping',-.51,.62,32,align='left',bold=True)
        ln((-.51,.43),(.51,.43),ink,1.55)
        words('$100',-.26,.19,25)
        words('$0',.28,.19,25)
        ln((.018,.34),(.018,-.17),rule,.91)
        ln((-.51,-.03),(.51,-.03),rule,.91)
        ln((-.51,-.30),(.51,-.30),'#CD4256' if kind==1 else '#8A6906',2.20)
        ln((-.51,-.52),(.20,-.52),rule,1.13,.84)
    else:
        ln((-.52,.64),(.24,.64),ink,3.1)
        ln((-.52,.44),(.49,.44),rule,1.18)
        for j,ll in enumerate((.91,.68,.84,.55)):
            y=.21-j*.17
            ln((-.52,y),(-.52+ll,y),rule,1.30)
        ln((-.52,-.59),(.24,-.59),'#61542C',2.1)
    if label:w.text(label,pos((0,-1.19,.10)),27,c,alpha)
def pairpage(w,p,c,alpha=1,scale=1):
    for j in range(3):
        q=(p[0]-.17*j*scale,p[1]+.09*j*scale,p[2]+.18*j*scale)
        page(w,q,c,alpha*(.44+.25*j),scale,rot=(.03, -.10, -.02*j))
def spine(w,i,u,kind='tile'):
    """Carry the same evidence baton between cameras; it does not fade through black."""
    z0,z1=SEAMS[i:i+2]
    if i and u<.17:
        p=step(u,0,.17)
        a=1-step(u,.072,.19)
        w.tile(vlerp(z0,add(z0,(-.35,.16,-.08)),p),'',GOLD,(.96,.67,.14),(0,.55*p,0),a,fill=.57)
    if i<8 and u>.82:
        p=step(u,.845 if i==7 else .82,1)
        origin=(2.37,.08,.075) if i==7 else add(z1,(.58,-.53,-.22))
        x=vlerp(origin,z1,p)
        if i==7:x=add(x,(0,.26*math.sin(PI*p),-.68*math.sin(PI*p)))
        opacity=step(u,.82,.99) if i!=7 else step(p,.26,.91)
        if i==7:
            a=step(u,.845,.875)*(1-step(p,.34,.71))
            w.text('$0',x,36,GOLD,a,weight='bold')
        w.tile(x,'',GOLD,(mix(.6,.96,p),mix(.44,.67,p),.14),(0,-.55*(1-p),0),opacity,fill=.56)
def strip(w,a,b,t,c=GOLD,al=1,r=.065):
    if .001<t<.999:
        p=vlerp(a,b,t);w.sphere((p[0],p[1]+.16*math.sin(PI*t),p[2]),c,r,al)

def archive(g,u,cue):
    mid=inout(u,.03,.26,.65,.98)
    w=swing(g,0,u,-.06,.23*mid,(.11*mid,.05*mid,.0))
    open_=cue(0,.04,.23); duplicate=cue(1,.16,.19); same=cue(2,.30,.15); pull=cue(6,.83,.20)
    glow=cue(3,.48,.18)
    dispose=step(u,.82,1)
    p=vlerp((0,0,0),(1.04,.03,.57),open_)
    op=vlerp((0,-.02,-.41),(-.98,.02,-.84),duplicate)
    op=add(op,(-.78*pull,-.65*pull,-1.05*pull))
    fin=1-dispose
    w.disk(vlerp((-2.45,0,0),(-4.10,-.26,.48),open_),A,'A',.42,.15,alpha=fin)
    w.disk(vlerp((2.45,0,0),(4.04,-.31,-.24),open_),B,'B',.42,.15,alpha=fin)
    w.tile((0,0,0),'',GOLD,alpha=1-open_,fill=mix(.33,.62,open_))
    page(w,p,GOLD,open_*fin,1.12,rot=(.08,.18*(-1+open_),.04),kind=2)
    page(w,op,MUTED,duplicate*(1-pull)*fin,1.06,rot=(.07,-.14,-.095),kind=1)
    w.mark(add(p,(.80,.76,.17)),True,.18,open_*fin)
    p1=add(op,(.73,-.20,.12));p2=add(p,(-.82,-.20,.12))
    w.path((p1,p2),RED,2.1,same*(1-pull)*fin,arrow=False,dash=[5,7],progress=same)
    w.curve(p1,(-1.9,-.20,-1.84),(-3.0,-.18,-1),(-3.6,-.23,.25),RED,2.2,glow*(1-pull)*fin,progress=glow,arrow=True)
    t=step(glow,.58,1)
    strip(w,p1,(-3.6,-.23,.25),t,RED,fin*(1-pull),.1)
    spine(w,0,u);w.draw()

def amounts(g,u,cue):
    w=swing(g,1,u,.15)
    a=step(u,.03,.21);old=cue(1,.17);th=cue(2,.31,.28);case=cue(3,.43);basis=cue(4,.55);new=cue(5,.66)
    end=1-step(u,.84,1)
    xx=lambda v:-4.27+(v-90)*.20
    yy=-.38;zz=.06
    mark=mix(xx(100),xx(120),th)
    w.segment((xx(90)-.25,yy,zz),(xx(132),yy,zz),MUTED,2.2,a*end)
    if a:
        w.face([(mark,yy+.06,zz),(xx(132),yy+.06,zz),(xx(132),yy+.06,-.84),(mark,yy+.06,-.84)],GOLD,a*end,.42,1.4)
    for n in (90,100,110,120,130):
        x=xx(n)
        w.segment((x,yy-.075,zz),(x,yy+.07,zz),MUTED,1.45,a*end)
        w.text(str(n),(x,yy-.30,zz+.06),25,MUTED,a*end)
    w.segment((mark,yy,.17),(mark,yy+.98,.17),GOLD,2.7,a*end)
    sign=((mark,yy+1.42,.19),(mark+.91,yy+1.42,.19),(mark+.73,yy+1.20,.19),
          (mark+.91,yy+.99,.19),(mark,yy+.99,.19))
    w.face(sign,GOLD,a*end,.89,1.20)
    w.text('FREE',(mark+.40,yy+1.205,.23),24,'#201903',a*end,weight='bold')
    w.segment((xx(100),yy-.1,-.62),(xx(100),yy+.78,-.62),MUTED,1.8,th*end,dash=[5,6])
    p=(mix(xx(100),xx(119),case),yy,.26)
    w.sphere(p,GOLD,.105,a*end)
    w.text('$119',(p[0],yy-.57,.34),32,GOLD,case*end)
    for j,(color,v,fee,ok,z) in enumerate(((A,basis,'$0',False,.52),(B,new,'$8',True,-.52))):
        y=-1.30-.87*j
        fee_x=2.63+1.17*j
        w.disk((-3.74,y,z),color,'AB'[j],.31,.13,alpha=a*end,label_size=25)
        w.path(((-3.37,y,z),(-1.6,y,z),(.17,y,z),(fee_x-.43,y,z)),color,1.7,a*end*.74,progress=.32+.68*v)
        if v>.003:
            w.text(fee,(fee_x,y+.035,z+.066),53,color,v*end,weight='bold')
            w.mark((fee_x+.68,y+.02,z+.045),ok,.133,v*end)
    if old*(1-th)>0:w.text('$0',(xx(100)+.13,yy+.11,.43),30,GOLD,old*(1-th)*end)
    spine(w,1,u);w.draw()

PHRASE=('Free','shipping','starts','at','$120','today')
def ngrams(g,u,cue):
    w=swing(g,2,u,.19)
    a=step(u,.01,.19);sc=cue(2,.26,.27);found=cue(3,.35,.17)
    long=cue(4,.50,.15);heading=cue(5,.63,.18);rewrite=cue(6,.75,.14)
    z0=.48;y0=1.17;end=1-step(u,.84,1)
    x=lambda j:(j-2.5)*1.23
    along=mix(mix(x(0),x(3),sc),x(1),found)
    gated=step(found,.86,.995)
    pview=(1-long*.73)*(1-heading)
    # This is a word span: the measuring bracket can move independently
    # of the original sentence, while its search result sits deeper in space.
    def token(p,text,col,alpha=1,width=.8,sz=28,base=.23,rule=.70):
        w.text(text,add(p,(0,.03,.01)),sz,col,alpha,weight='medium')
        x,y,z=p;half=width*.5
        w.segment((x-half,y-base,z),(x+half,y-base,z),col,1.6,alpha*rule)
    for k,tok in enumerate(PHRASE):
        keep=clamp(1.-max(0.,abs(x(k)-(along+1.23))-1.22)*3.7)
        co=blend(INK,GOLD,keep)
        token((x(k),y0,z0),tok,co,a*pview*end,.91,33,rule=keep)
    l=along-.49;r=along+2.46+.49;yy=y0+.31
    w.path(((l,yy-.16,z0),(l,yy,z0),(r,yy,z0),(r,yy-.16,z0)),GOLD,2.05,end*a*pview)
    for p in range(3):
        yy=.18-.60*p;z=-1.42+p*.69
        for j in range(12):
            tx=(j-5.5)*.68
            matched=p==1 and 4<=j<=6
            extra=p==0 and 1<=j<=3
            hit=gated*(1-heading)
            false_match=heading*(1-rewrite)
            al=end*a
            if matched and hit>.005:
                tx+=hit*(j-5)*.26
                token((tx,yy,z),('shipping','starts','at')[j-4] if long<.8 else '',RED,al*hit,
                      mix(.57,.78,hit),23,.18)
                w.curve((x(j-3),y0-.234,z0),(x(j-3),.59,.07),(tx,yy+.28,z),(tx,yy+.14,z),GOLD,
                        1.38,hit*.62*end*pview,progress=hit)
            elif extra and false_match>.005:
                w.segment((tx-.22,yy,z),(tx+.21,yy,z),RED,2.1,al*false_match*.72)
            else:
                w.segment((tx-.19,yy,z),(tx+.09+(j*j%5)*.048,yy,z),MUTED,1.61,al*.29*(1-.65*heading))
        w.face(((-4.1,yy-.24,z-.07),(4.1,yy-.24,z-.07),(4.1,yy+.24,z-.07),(-4.1,yy+.24,z-.07)),
               MUTED,a*end*.71*(1-.48*heading),.091,.0)
        w.segment((-4.06,yy-.237,z),(4.06,yy-.237,z),MUTED,1.02,a*end*.34*(1-.48*heading))
    for j in range(13):
        q=step(long,j*.025,.52+j*.022)
        p=((j-6)*.6,-1.63,.90+.27*math.sin(j*.36)*rewrite)
        col=GOLD if j in (4,5,6) else MUTED
        if heading and j in (0,1,2):col=blend(col,RED,heading*(1-rewrite))
        if rewrite and j in (4,5,6):p=add(p,(0,-.24*rewrite,-.48*rewrite))
        xx,yy,z=p
        w.segment((xx-.16,yy,z),(xx+.16+(j%3)*.027,yy,z),col,3.65,end*q*(1-heading*.65))
    w.path(((-3.89,-1.78,1.0),(-3.89,-1.92,1.0),(3.89,-1.92,1.0),(3.89,-1.78,1.0)),
           GOLD,1.55,long*end*.83*(1-heading*.86))
    w.text('13-gram',(0,-2.17,1.02),34,GOLD,long*end*.96*(1-heading*.92))
    # False positive, then false negative. Text aligns to allow the
    # dashed correspondence to appear and actually break.
    for j in range(3):
        xx=(j-1)*1.82
        equal=('Store','help','center')[j]
        old=('Shipping','is','free')[j]
        newer=('Postage','is','waived')[j]
        a1=heading*(1-step(rewrite,.18,.57))*end
        a2=step(rewrite,.53,1)*end
        p1=(xx,1.28,.84);p2=(xx,.13,-.25)
        if a1>.004:
            token(p1,equal,GOLD,a1,1.27,36,rule=.79)
            token(p2,equal,RED,a1,1.27,36,rule=.79)
            w.path((add(p1,(0,-.27,0)),add(p2,(0,.27,0))),RED,1.4,a1*.58,dash=[4,6],progress=heading)
        if a2>.004:
            token(p1,old,GOLD,a2,1.30,36,rule=.79)
            token(add(p2,(0,0,-.40*rewrite)),newer,INK,a2,1.30,36,rule=.44)
    spine(w,2,u);w.draw()

def card(w,p,n,c=MUTED,a=1,rot=(0,0,0),scale=1):
    if a<.002:return
    m=rotation(tuple(rot));f=lambda q:add(p,trans(mul(q,scale),m))
    w.paper(p,1.47*scale,.91*scale,c,a,rot,.73 if c==GOLD else .66,cut=.125*scale)
    dep=w.project(p)[2]+.058
    w.ink(str(n),f((-.43,0,.114)),m,34*min(1.12,scale),'#211D13',a,weight='bold',sort_depth=dep)
    for j in range(3):
        yy=.21-j*.20
        w.segment(f((-.07,yy,.112)),f((.52-(j==1)*.14,yy,.112)),('#7B5D19' if c==GOLD else '#56505C') if j==2 else '#3D3A42',1.67,a*.87,sort_depth=dep)
def shuffle(g,u,cue):
    w=swing(g,3,u,-.15)
    spawn=cue(1,.21,.25);paired=cue(2,.34);change=cue(3,.50,.26);read=cue(4,.67);pub=cue(6,.89)
    end=1-step(u,.85,1)
    for j in range(3):
        p0=SEAMS[3];px=(j-1)*1.92
        p=vlerp(add(p0,(0,0,-j*.13)),(px,.70,.44),spawn)
        card(w,p,j+1,GOLD,spawn,rot=(.01,-.08,0))
        if paired:
            f=j if j==1 else 2-j
            x=mix(px,(f-1)*1.92,change)
            base=mix(.70,-.94,paired)
            angle=math.sin(PI*change)
            lift=(j-1)*angle*.80
            yy=base+lift*.46
            q=(x,yy,-.95+lift)
            card(w,q,j+1,MUTED,paired,rot=(0,-.54*angle*(j-1),.24*angle*(j-1)))
            if f!=j and 0<change<1:
                w.curve((px,base,-.95),(px,base,-.95+lift),((f-1)*1.92,base,-.95+lift),q,MUTED,1.16,angle*.61*end,progress=change)
    w.disk((4.28,.02,.21),A,'A',.42,.15,alpha=read*end)
    for j,y in enumerate((.70,-.94)):
        p0=(2.67,y,.58 if not j else -.75)
        p1=(3.80,.07,.20);progress=pub if not j else read
        w.curve(p0,(3.44,y,.42),(3.80,y*.22,.22),p1,GOLD if not j else MUTED,2,progress*end,progress=progress,arrow=True)
    spine(w,3,u);w.draw()

PERMS=(0,1,1,2,2,2,3,3,3,3,4,4,4,4,4,4,5,5,5,5,5,6,6,6,6,7,7,7,8,8,9)
def ordering(g,u,cue):
    w=swing(g,4,u,.09)
    scatter=cue(0,.08,.39);cloud=cue(1,.18,.29);pub=cue(2,.34,.20)
    known=cue(3,.48,.19);cond=cue(4,.60,.20);cal=cue(5,.76,.25)
    f=step(u,0,.17);end=1-step(u,.86,1)
    for j in range(6):
        x0=(j%3-1)*1.92;y0=.70 if j<3 else -.94
        dest=((-2.9+.27*j),-1.31,-.30)
        q=step(scatter,j*.048,.59+j*.046)
        p=vlerp((x0,y0,.44 if j<3 else -.95),dest,q)
        val=j%3+1 if j<3 else 3-(j%3)
        card(w,p,val,GOLD if j<3 else MUTED,(1-q)*end,
             rot=(mix(.01 if j<3 else 0,.18,q),mix(-.08 if j<3 else 0,.64,q),0),scale=mix(1,.18,q))
    for j in range(3):
        a=step(scatter,.08+j*.08,.27+j*.10)*end
        if a*(1-cloud)>0:card(w,(2.71+.28*j,.93+.17*j,-.75+j*.17),j+4,MUTED,a*(1-cloud),scale=.35)
    y=-1.25;z=.12
    w.path(((-4.67,y,z),(4.83,y,z)),MUTED,2.1,f,arrow=True,progress=f)
    levels={}
    for j,x in enumerate(PERMS):
        levels[x]=levels.get(x,0)+1
        q=step(cloud,j/65,.34+j*.021)
        dz=(j%4-1.5)*.57*(1-step(cloud,.43,.97))
        xx=-3.78+x*.66
        yy=y+.25+(levels[x]-1)*.31
        w.sphere(vlerp((-.25,.25,-1.10),(xx,yy,z+dz),q),MUTED,.075+.021*q,q*end)
    xg=4.06
    w.segment((xg,y+.02,z),(xg,y+1.88,z),GOLD,1.65,pub*end,dash=[5,7])
    w.sphere((xg,y+.26,z),GOLD,.128,pub*end)
    w.text('Published order',(xg,y+2.08,z),27,GOLD,pub*end)
    w.text('Sequence log probability',(0,y-.49,z),28,MUTED,cloud*end)
    for j in range(3):
        xx=1.70+j*.35
        pp=(xx,.77+j*.17,-.96+j*.15)
        po=((-2.55+j*2.5),1.62,-.46)
        a=known*end
        if a:
            card(w,vlerp(pp,po,cal),j+1,blend(GOLD,RED,cal),a,rot=(.25*(1-cal),.20*(1-cal),0),scale=.64)
            w.text(('Mon','Tue','Wed')[j],add(po,(0,.54,.08)),25,RED,cal*end)
            if j:w.path(((-2.55+(j-1)*2.5+.58,1.62,-.46),(po[0]-.60,1.62,-.46)),RED,1.65,cal*.78*end,arrow=True)
    if cond:w.segment((-4.63,y-.05,z),(xg,y-.05,z),RED,1.1,cal*end*.47,dash=[4,10])
    spine(w,4,u);w.draw()

def fresh(g,u,cue):
    w=swing(g,5,u,-.10)
    take=step(u,0,.27);freeze=cue(1,.26,.18);later=cue(2,.38,.19);lc=cue(3,.53,.18);lock=cue(4,.70,.18)
    end=1-step(u,.85,1)
    y=mix(-1.25,-.32,take);z=.12
    w.path(((-4.67,y,z),(4.83,y,z)),MUTED,2.1,end,arrow=True)
    cut=.22
    for j in range(4):
        xx=-3.54+j*.91
        yy=y+.78
        w.paper((xx,yy,-.47),.47,.56,MUTED,end*take*.75,(.04,.08,-.035*j),.39,.108)
        w.segment((xx,yy-.24,-.47),(xx,y,z),MUTED,1.15,end*take*.54)
    for j in range(3):
        xx=1.27+j*.82;zz=.23
        alpha=step(later,j*.14,.74+j*.101)
        w.paper((xx,y+.76,zz),.52,.59,GOLD,alpha*end,(.04,-.09,.035*j),.70,.12)
        w.segment((xx,y+.53,zz),(xx,y,zz),GOLD,1.3,alpha*end*.79)
    w.text('time',(5.04,y+.01,z),25,MUTED,end*take,align='left')
    w.segment((cut,y-.42,z),(cut,y+2.18,z),A,2.04,freeze*end)
    w.disk((cut,y+2.08,z+.04),A,'A',.33,.12,alpha=freeze*end,label_size=27)
    w.text('cutoff',(cut,y-.56,z),24,A,freeze*end)
    w.text('LiveCodeBench',(2.10,y-.58,z),30,GOLD,lc*end)
    if lock:
        for j in range(4):w.tile((3.20+.14*j,-1.56-.09*j,-.83+j*.15),'',GOLD,(.67,.46,.13),alpha=lock*end*(.48+.16*j),fill=.31)
        w.text('Held-out set',(3.66,-2.14,-.04),25,GOLD,lock*end)
    spine(w,5,u);w.draw()

def workday(g,u,cue):
    w=swing(g,6,u,-.21)
    crop=step(u,.015,.23);input_=cue(1,.18,.23);coupons=cue(2,.30,.22)
    valid=cue(3,.45,.29);winner=cue(4,.64,.15);med=cue(5,.77,.17)
    end=1-step(u,.86,1)
    l=vlerp(SEAMS[6],(-3.55,.16,-.37),crop)
    r=vlerp((2.89,.17,-.18),(3.35,.16,.26),valid)
    pairpage(w,l,GOLD,crop*end,.96)
    price=vlerp((-.13,.24,.54),(-1.41,.15,.19),input_)
    w.tile(price,'$0',MUTED,(.82,.59,.17),alpha=crop*end*(1-valid),fill=.24)
    w.text('Coupons',(-1.27,1.00,.61),31,GOLD,coupons*end)
    w.text('Refunds',(-.95,-.19,-.45),31,GOLD,coupons*end)
    for q in ((-1.27,.78,.58),(-.95,-.43,-.50)):
        w.pin(q,GOLD,.066,coupons*end)
    for j,q in enumerate(((-1.27,.78,.58),(-.95,-.43,-.50))):
        w.curve(add(l,(.68,.0,.12)),(-2.47,.12,.18),add(q,(-.73,0,-.66)),q,GOLD,1.79,coupons*.62*end,progress=coupons,arrow=True)
        w.curve(q,(.46,q[1],q[2]),(2.03,.13,.54),add(r,(-.77,.0,.10)),GOLD,1.79,valid*.63*end,progress=valid,arrow=True)
    page(w,r,GOLD,input_*end,1.18,rot=(.01,.04,.03))
    w.mark(add(r,(.80,-.59,.16)),True,.15,valid*end)
    # The existing deliverable moves into the upper lane while a second work packet opens below.
    if winner:
        q=step(med,0,.87)
        w.text('GDPval',(1.36,.98+.62*q,.45),30,INK,winner*end)
        one=add(r,(-.28,.23+.50*q,-.94))
        page(w,one,B,winner*.84*end,.87,rot=(.02,.15,-.07))
    if med:
        y=-1.22
        w.text('MedHELM',(-2.45,y-.45,.34),28,INK,med*end)
        for j,t in enumerate(('Record','Decision')):
            xx=1.32+j*1.94
            w.text(t,(xx+.12,y-.28,.69-.47*j),28,GOLD,med*end)
            w.pin((xx-.41,y-.46,.65-.47*j),GOLD,.066,med*end)
            w.curve((-.88,y-.44,.47),(-.2,y-.50,.68),(xx-.51,y-.57,.74),(xx-.76,y-.44,.65-.47*j),
                    MUTED,1.35,med*.65*end,progress=med,arrow=True)
    spine(w,6,u);w.draw()

def practical(g,u,cue):
    w=swing(g,7,u,.17)
    a=step(u,.0,.19);border=cue(1,.13,.18);refund=cue(2,.28,.20)
    rule=cue(4,.48,.22);trade=cue(5,.63,.23);fail=cue(6,.77,.18);human=cue(7,.86,.22)
    end=1-step(u,.85,1)
    # For the first comparison, the same input packet forks to both systems.
    # The gold packet then becomes the boundary-case receipts below.
    hold=a*(1-step(border,.36,.87))
    ip=vlerp(SEAMS[7],(-.08,1.05,.19),a)
    if hold>.002:
        pairpage(w,ip,GOLD,hold,.61)
        for j,d in enumerate((A,B)):
            xx=-3.21+6.42*j;pos=(xx,.25,.50-.92*j)
            w.disk(pos,d,'AB'[j],.40,.15,alpha=hold,label_size=32)
            dep=.18-.56*j
            p0=add(ip,(-.42+.84*j,-.27,.10))
            p1=add(pos,(.39-.78*j,.03,.04))
            w.curve(p0,(-1.02+2.04*j,.86,dep),(-2.55+5.10*j,.44,dep),p1,GOLD,1.9,hold*.77,progress=step(a,.19,.76),arrow=True)
            q=step(u,.10+.015*j,.22+.022*j)
            strip(w,p0,p1,q,GOLD,hold,.07)
    for j,(p,fee) in enumerate((('$119','$8'),('$120','$0'),('Refund','$8'))):
        yy=1.08-1.0*j
        z=.42-.40*j
        show=border if j==0 else (step(border,.28,1) if j==1 else refund)
        orig=SEAMS[7]
        left=vlerp(orig,(-3.94,yy,z),show)
        right=(2.37,yy,z)
        name=p if j<2 else 'Refund'
        half=.69 if j<2 else 1.03
        paper_depth=w.project(left)[2]+.054
        m=rotation((.075,-.13,0))
        w.paper(left,1.38 if j<2 else 2.20,.55,GOLD,show*end,(.075,-.13,0),
                fill=.83 if j==2 else .72,cut=.15)
        if j==2 and rule>.5:
            name='$120 − $60'
        w.ink(name,add(left,(0,.013,.047)),m,31,'#20180E',show*end,weight='medium',sort_depth=paper_depth)
        w.path(((left[0]+half,yy,z),(-1.44,yy,z),(right[0]-.52,yy,z)),MUTED,1.35,
               show*end*.57,arrow=True,progress=show)
        zfee=show if j<2 else rule
        keep=1-step(u,.845,.875) if j==1 else 1
        w.text(fee,add(right,(0,.015,.055)),37 if j<2 else 43,GOLD,zfee*end*keep,weight='bold')
        w.mark(add(right,(.69,0,.09)),True,.12,zfee*end*(1-trade if j<2 else 1-fail))
        if j<2:
            w.mark((3.57,yy,.86),j==1,.13,trade*border*end)
            w.mark((4.30,yy,-.20),True,.13,trade*border*end)
        elif fail:
            w.mark((3.57,yy,.86),False,.13,fail*end)
            w.mark((4.30,yy,-.20),False,.13,fail*end)
            w.path(((4.48,yy,-.15),(4.92,yy,-.08),(5.21,yy,.10)),MUTED,1.40,human*end,arrow=True,progress=human)
            h=(5.52,yy+.20,.16)
            w.sphere(h,MUTED,.10,human*end)
            w.curve(add(h,(-.20,-.31,0)),add(h,(-.15,-.06,0)),add(h,(.15,-.06,0)),add(h,(.20,-.31,0)),MUTED,1.95,human*end,progress=human)
    w.disk((3.57,1.92,.86),A,'A',.28,.13,alpha=trade*end,label_size=23)
    w.disk((4.30,1.92,-.20),B,'B',.28,.13,alpha=trade*end,label_size=23)
    w.segment((-1.62,-2.10,.44),(-1.62+1.18*trade,-2.10,.44),A,3.6,trade*end)
    w.segment((-1.62,-2.42,.12),(-1.62+2.00*trade,-2.42,.12),B,3.6,trade*end)
    w.text('Time',(-2.33,-2.26,.33),23,MUTED,trade*end)
    spine(w,7,u);w.draw()

def reprise(g,u,cue):
    spread=cue(0,.02,.23);ahead=cue(1,.19,.23);last=cue(2,.38,.19)
    look=cue(4,.72,.27);extra=cue(5,.89,.19)
    w=swing(g,8,u,-.08,.39*look,(2.98*look,.20*look,.12*look))
    first=step(u,0,.19)
    pp=SEAMS[8]
    w.tile(vlerp(pp,(XS[-1],.93,.22),spread),'four' if spread>.32 else '',GOLD,(mix(.96,1.39,spread),mix(.67,.68,spread),.17),alpha=(1-first),fill=.65)
    prompt_track(w,first*(1-look*.51),omit=(5,))
    xl=XS[-1]
    w.tile((xl,.93,.22),'four',GOLD,(1.39,.68,.17),alpha=first*(1-look*.25),fill=.53)
    prediction_lanes(w,tuple(ahead for _ in range(5)),(last,last),first*(1-look*.60))
    for j,z in enumerate(ZLANE):
        w.path(((xl,.55,.22),(xl,.39,z),(xl,YLANE[j]+.33,z)),GOLD,1.47,last*(1-look*.48),progress=last)
    if extra:
        p=vlerp((xl+.24,.93,.24),(5.85,.92,.22),extra)
        w.tile(p,'?',GOLD,(1.31,.72,.18),rot=(0,.66*(1-extra),0),alpha=extra,fill=.57,label_size=39)
        w.segment((xl+.70,.93,.22),(p[0]-.65,.93,.22),GOLD,1.25,extra,dash=[4,7])
        w.sphere((p[0],p[1]-.62,p[2]),GOLD,.043,extra*.85)
    w.draw()

STAGES=(archive,amounts,ngrams,shuffle,ordering,fresh,workday,practical,reprise)
def draw(g,i,t,duration):
    u,cue=passage(g,i,t,duration)
    STAGES[i](g,u,cue)
