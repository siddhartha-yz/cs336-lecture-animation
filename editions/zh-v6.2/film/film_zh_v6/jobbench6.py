"""An answer mark cannot carry a job; the geometry picks up actual constraints."""
from rig4 import *
from studio_field import reel

def fixture_sheet(g,c,gdp):
 t=c.t;a=c.at
 # First approach the real sheet, then start turning it on "夹具". The
 # orthographic view still completes on the actual dimensions, not before.
 earlier=.38*easepos(t,a('夹具设计')-.36,1.23);to=earlier+.62*c.u('尺寸约束',1.05)
 eye=phase(t,gdp+.69,a('一位制造工程师')+.61)*(1-phase(to,.08,.60))
 u=enter(t,gdp-.61,.64);theta=-.035+.013*to+.027*eye
 x,y=mix(773,495,to)-23*eye,mix(464,446,to)-21*eye;w=mix(929,669,to)*(.86+.14*u)*(1+.079*eye)
 actual=theta-.072*(1-u)
 photo(g,AS/'gdp-delivery.png',x,y,w,tilt=actual,op=u)
 return to,actual,u,(x,y,w)

def details(g,c,x,y,w,theta,op):
 t=c.t
 cue_=(c.at('有物件'),c.at('尺寸约束'),c.at('检查的图纸'))
 sf=img(AS/'gdp-delivery.png');ar=sf.get_height()/sf.get_width()
 ctx=g.c;ctx.save();ctx.translate(x,y);ctx.rotate(theta);ctx.scale(w,w)
 # Annotation follows actual features on the unaltered engineering plate:
 # the drum, the fastener callout, and the frame itself.
 regions=((-.17,-.28,.22,.29,O),(.21,-.36,.21,.19,C),(-.38,.20,.55,.13,T))
 for j,(xx,cy,ww,hh,co) in enumerate(regions):
  at=cue_[j];life=during(t,at-.21,at+1.46,.43)*op
  if not life:continue
  r=easepos(t,at-.17,.66);cy*=ar;hh*=ar
  # Trace a corner bracket only, leaving the underlying paper and typeset dimensions legible.
  pts=((xx,cy+.04),(xx,cy),(xx+ww,cy),(xx+ww,cy+hh))
  path(g,pts,r,inkcol(co,.63),.0045,life)
  dot(g,xx+ww,cy+hh,.007,inkcol(co,.71),life*r)
 ctx.restore()

def work(g,c,last):
 t=c.t;a=c.at
 scissors=a('孤立小题');context=a('上下文');needs=a('模糊需求')
 desk=a('真实职场');answer=a('圈对一个字母');result=a('交出一份别人')
 collect=a('方便批改');cut=a('切成干干净净')
 snap=easepos(t,scissors-.26,1.18);q=phase(t,desk-.25,desk+.73)
 gather=easepos(t,collect-.20,.82);separate=easepos(t,cut-.15,1.22)
 dock=easepos(t,desk-.46,.73)
 rise=easepos(t,result-.15,1.61);turn_phase=easepos(t,context-.32,1.41)
 light=enter(t,answer-.17,.62)
 hand=1-phase(t,last-.92,last-.28)
 frame=enter(t,collect-.19,.61)*(1-separate)*hand
 if frame:
  # The four answers start on one sheet. The cut can then be seen in the
  # widening gaps, instead of four new disconnected boxes fading in.
  sx=mix(168,480,gather);sy=mix(369,309,gather)
  w=mix(378,620,gather);h=mix(104,195,gather)
  rect(g,sx,sy,w,h,inkcol(C,.25),frame*.89)
  path(g,[(sx,sy+h),(sx,sy),(sx+w,sy),(sx+w,sy+h),(sx,sy+h)],gather,C,2.7,frame)
  for j in range(3):
   bx=mix(260+99*j,635+155*j,gather)
   s=easepos(t,cut-.29+.11*j,.59)
   if s:path(g,[(bx,sy),(bx,sy+h)],s,Y,2.9,frame*.93)
 # Enter from the actual four letters left at the end of the interlude.
 for j,ch in enumerate('ABCD'):
  x=mix(211+99*j,800+(j-1.5)*(155+25*separate),gather)
  y=mix(423,405+(1 if j%2 else -1)*38*separate,gather)
  x=mix(x,211+99*j,dock);y=mix(y,423,dock)
  remove=easepos(t,result-.13+.10*j,1.09)
  bx=mix(x,268+(j-1.5)*43,remove);by=mix(y,492,remove)
  ws=mix(155,128,separate);w=mix(ws,78,dock);wo=mix(w,66,remove)
  hs=mix(93-19*separate,53,dock);h=mix(hs,53,remove)
  sph=1-(.78*remove if j!=2 else .68*remove)
  op=hand*sph
  if separate and op:
   br=mix(.83*separate,1.,snap)
   co=(C,T,Y,V)[j]
   g.poly([(bx-wo/2,by-h),(bx+wo/2-8,by-h),(bx+wo/2,by-h+9),(bx+wo/2,by+h-5),
           (bx-wo/2,by+h-5)],co,2.,br*op,True,inkcol(co,mix(.44,.35,q)),br*op)
  label(g,ch,bx,by,mix(53+17*gather*(1-dock),34,remove),Y if j==2 and light else F,op)
 if light and hand:
  bx=mix(409,268+.5*43,rise)
  path(g,[(bx-30,487),(bx+29,487)],easepos(t,answer-.19,.68),Y,3.8,hand*light*(1-.54*rise))
  label(g,'一个选项',bx,591,28,M,hand*light*(1-rise))
 if q and hand:
  # The illustration is the same fixture visible in the next real drawing.
  cx=mix(1062,1033,rise);cy=mix(410,334,rise)
  angular=1.47-.74*turn_phase-.18*rise+.052*sin((t-desk)*.63)
  main=1.14+.35*rise+.11*q;op=hand*q
  # A desk line widens with the job; it does not become a black slide.
  xs=[(714,641),(1331,641),(1486,678),(830,679),(714,641)]
  path(g,xs,easepos(t,desk-.27,1.18),M,1.8,op*.83)
  reel(g,cx,cy,main,angular,op)
  for j,(word,col,when,source,tip) in enumerate((
   ('需求',O,needs,(929,257),(762,207)),
   ('环境',C,context,(1205,343),(1384,268)),
   ('可检查的交付物',T,result,(1074,545),(1155,706)),
  )):
   er=enter(t,when-.19,.57)
   if er:
    vx,vy=tip;sp0=source;sp1=(mix(vx,sp0[0],.47),mix(vy,sp0[1],.52))
    path(g,[sp0,sp1,tip],er,col,2.2,op*.83)
    point(g,*sp0,4.7,col,op*er)
    st=27 if j<2 else 30
    label(g,word,vx,vy+(-27 if j<2 else +26),st,col,op*er)
 if t>=last-.61:
  fixture_sheet(g,c,last)
