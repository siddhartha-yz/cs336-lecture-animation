"""Single prop across each cut. On either side, every prop has one screen pose."""
from rig4 import *
from studio_tests import AR,arcboard

def front_ruler(g,t):
 # The film's one title exits with its other instruments; the measured edge
 # underneath remains to turn into the axis in the first chapter.
 u=phase(t,4.04,4.89)
 if u:
  x=mix(457,340,u);y=mix(649,616,u);w=mix(666,899,u)
  ruler(g,x,y,w,-.105,u,0.)

def opening_aperture(g,t):
 # At the start of the title, the current board withdraws through its own
 # shadow. Only the outgoing contrast remains until the new instruments enter.
 q=easepos(t,.0,.48)
 if q>=1:return
 ctx=g.c;ctx.save()
 left=mix(0,279,q);top=mix(0,599,q);right=mix(1600,963,q);bottom=mix(900,628,q)
 ctx.rectangle(left,top,right-left,bottom-top);ctx.clip()
 endpaper(g,'0-2',0,0,1,1-phase(t,.29,.48))
 ctx.restore()

def ruler(g,x,y,w,theta,op,settle):
 for i in range(13):
  p=i/12;tx=x+w*cos(theta)*p;ty=y+w*sin(theta)*p
  line(g,(tx,ty-4),(tx-9*sin(theta),ty+9*cos(theta)),Y,1.45,op*(1-settle)*(.64+.27*(i%3==0)))
 line(g,(x,y),(x+w*cos(theta),y+w*sin(theta)),blend(Y,M,settle),mix(3.25,2.3,settle),op)
def bar_in(t,i):return enter(t,-.81+.056*i,.61)
def array(g,c):
 from v4_act1 import A
 t=c.t;u=easepos(t,.04,c.d-.11);q=easepos(t,.11,2.20);b=easepos(t,1.04,2.13)
 x=mix(340,191,u);y=mix(616,590,u);w=mix(899,1227.5,u);theta=-.105*(1-q)
 ruler(g,x,y,w,theta,1.,b)
 # Same 26 positioned bars, from the same data as the first plot.
 compare=sorted(A,key=lambda r:r['index']);raw=t-c.d
 for j,r in enumerate(compare):
  z=bar_in(raw,j)
  if z:
   xx=209+j*46.5;h=r['index']*5.25*z;co=C
   rect(g,mix(x+(xx-191)*w/1227.5,xx,b),y-h,30.3,h,inkcol(co,.68+.23*j/25),1.)
def termstrip(g, tokens, t, q0=1., y=244, result=0., lead=False):
 for i,tok in enumerate(tokens):
  x=182+172*i
  factor=easepos(t,-.79+.075*i,.57)if lead else q0
  if not factor:continue
  by=y+19*(1-factor)*sin(i*.52)
  ww=mix(132,140,factor);hh=mix(17,71,factor)
  pop=result if i==2 else 0.
  box(g,x-ww*.5,by-33*(hh/71.),ww,hh,blend(E,Y,pop),factor,inkcol(blend(M,Y,pop),.086+.16*pop),1.65+1.10*pop)
  if lead and factor<.998:
   mark(g,tok,x,by+1,40,t+.67-.075*i,blend(F,Y,pop),dur=.48,op=factor)
  else:label(g,tok,x,by+1,40,blend(F,Y,pop),factor)
def fold_words(g,c):
 from v4_act2 import OP
 t=c.t;q=easepos(t,.10,c.d-.11);r=phase(t,.04,1.22);u=easepos(t,1.12,1.73)
 if r<1:
  # Recede once. Leave just the lowercase words on one narrow lane;
  # the old ruler and formula never repaint over the new labels.
  ctx=g.c;ctx.save();top=mix(0,287,r);bottom=mix(900,532,r)
  ctx.rectangle(0,top,1600,bottom-top);ctx.clip()
  endpaper(g,'1-3',0,0,1.,1-r);ctx.restore()
 if r:
  beta=easepos(t,.84,.85);by=mix(526,244,q)
  for j,(token,p) in enumerate(zip(OP['tokens'],OP['probabilities'])):
   x=182+172*j;w=mix(12+190*p,137,beta);h=mix(67*p+13,22,beta)
   co=Y if j==2 else C;a=beta*enter(t,.31+.065*j,.61)
   if u<.998:
    box(g,x-w/2,by-h*.5,w,h,co,a*(1-u),inkcol(co,.15+.20*beta),2.0)
    top=by-h*.5
    line(g,(x,top),(x,top-91*(1-u)*beta),co,1.9,a*(1-u))
  if u:
   termstrip(g,OP['tokens'],t-c.d,u,y=by,lead=False)
 if t>c.d-1.0:
  lab=enter(t,c.d-.51,.49)
  if lab:
   label(g,'The room was quiet.',153,105,38,M,lab,'left');label(g,'前文',153,154,25,T,lab,'left')
def exam_text(g,a,x=199,y=300):
 label(g,'9 − 7',x,y,80,F,a,'left')
def still_answer(g,vis,co=V):
 ring(g,1281,422,58,co,vis,2.5);dot(g,1281,422,51,inkcol(co,.46),vis);label(g,'2',1281,420,50,F,vis)
def cut_mail(g,t,shape,alpha):
 from v4_act4 import mail
 c=cue('4-1');was=c.t
 # Real envelope lands at its first position in the next frame.
 try:
  c.t=t
  mail(g,shape[0],shape[1],shape[2],alpha,shape[3],c)
 finally:c.t=was
MAIL_RUN=(744,554,.91,-.034)
def filing(g,c):
 from fork6 import PORT,ARMS,terminal,arm
 t=c.t;u=easepos(t,.13,c.d-.13);q=enter(t,1.31,.69)
 t0=phase(t,.07,.69)
 if t0<1:endpaper(g,'3-4',0,0,1.,1-t0)
 if t0:
  reach=easepos(t,.19,1.23)
  outp=1-phase(t,1.48,2.33)
  from_=PORT
  point(g,*from_,10.1,Y,t0*outp*(1-phase(t,.93,1.52)))
  for j,(dx,dy,co) in enumerate(ARMS):
   wait=t0*(1-q if j==1 else 1.);p=easepos(t,.58+.17*j,1.03)
   shape=(from_[0]+dx,from_[1]+dy)
   dest=((536,592),(741,444),(1110,465))[j]
   xx,yy=transit(shape,dest,p,-37.+4*j)
   if p<1:arm(g,(xx,yy),co,wait*outp*(1-phase(p,.59,1.)))
   if wait:
    # The branches acquire material before any specimen text enters.
    r=36+44*reach
    theta=.30- .78*p+.16*j
    shape=phase(p,.15,.50)
    terminal(g,xx,yy,36,co,wait*outp*(1-shape),1.,j)
    ctx=g.c;ctx.save();ctx.translate(xx,yy);ctx.rotate(theta)
    a=shape*wait*outp
    g.poly([(-r,-r*.48),(r,-r*.48),(r,r*.48),(-r,r*.48)],co,1.9,a,True,inkcol(co,.42),a*.86)
    ctx.restore()
 if q:
  f=easepos(t,1.31,c.d-1.36);tilt=mix(-.16,MAIL_RUN[3],f)
  x,y=transit((741,448),MAIL_RUN[:2],f,-41)
  k=mix(.51,MAIL_RUN[2],f);hide=1-.78*phase(t,c.d-1.06,c.d-.01)
  cut_mail(g,0.,(x,y,k,tilt),q*hide)
def issue_pose(q,focus):
 return (mix(803,809,focus)+62*(1-q),mix(392,399,focus)-49*(1-q),
         mix(1070,1242,focus)*(.94+.06*q),-.027+.013*focus+.051*(1-q))
def issue(g,q,focus=0.,opacity=1.):
 x,y,w,theta=issue_pose(q,focus)
 photo(g,AS/'sphinx-issue.png',x,y,w,tilt=theta,op=opacity)
def issues_on_wire(g,c):
 t=c.t;q=easepos(t,.18,2.02);v=easepos(t,1.10,c.d-1.11)
 settle=easepos(t,0,.47)
 if settle<1:
  ctx=g.c;ctx.save();rad=1730*(1-settle)+24
  ctx.arc(1222,465,rad,0,tau);ctx.clip()
  endpaper(g,'4-4',0,0,1.,1-phase(t,.29,.44));ctx.restore()
 if q<1:
  # The sole empty diagnostic lamp at the end of the previous shot grows its
  # measuring wire before any new paper arrives.
  ring(g,1222,465,mix(24,17,q),blend(M,T,q),1-q,2.25)
  pts=[(1222,466),(1120,466),(1040,508),(775,508)]
  path(g,pts,q,T,2.7,1-v)
  for j in range(9):
   px=mix(1222,502+j*81,q);py=mix(465,508,q)
   z=enter(t,.09+j*.063,.52);rect(g,px-12,py-8,24*z,16*z,T,z*q*(1-v))
 if v:
  x,y,w,th=issue_pose(0,0)
  photo(g,AS/'sphinx-issue.png',mix(660,x,v),mix(541,y,v),mix(410,w,v),tilt=mix(-.185,th,v),op=v)
def puzzle_gate(g,c):
 t=c.t
 # The actual three input grids at the end of SWE-bench enter the aperture;
 # first example I becomes the full sensor of ARC-AGI.
 for j,rec in enumerate(AR['train']):
  x=(465,799,1134)[j];y=(465,357,501)[j];w=184
  q=easepos(t,.10+.06*j,c.d-.11-.06*j)
  if j==0:
   x,y=transit((x,y),(506,420),q,-44);w=mix(w,535,q)
  else:
   x,y=transit((x,y),(1570+150*j,y+289),q,91)
  p=1 if not j else 1-q
  if p:arcboard(g,rec['input'],x,y,w,p)
def choices_pose(g,op=1,q=0):
 for j,ch in enumerate('ABCD'):
  x=211+99*j;y=423;h=(31 if j in (0,3)else 29)*q
  if h:rect(g,x-h*1.2,y-h*1.05,h*2.4,h*2.1,C,op*.44*q)
  label(g,ch,x,y,53,F,op)
