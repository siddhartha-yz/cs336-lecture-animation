"""Carry vote geometry into the rating ruler. Motion carries the relation."""
from rig4 import *
from studio_votes import wedge

def screenplate(g, paint, shift=(0,0), scale=1., opacity=1., pivot=(800,424)):
 if opacity<.002:return
 ctx=g.c;ctx.save();ctx.translate(*shift);ctx.translate(*pivot);ctx.scale(scale,scale);ctx.translate(-pivot[0],-pivot[1])
 if opacity<.995:
  ctx.push_group()
  paint()
  ctx.pop_group_to_source();ctx.paint_with_alpha(opacity)
 else:paint()
 ctx.restore()

def scores_ribbon(g,c,st,glass):
 # Indices refer to the two displayed illustrative scores, never the real ranking.
 t=c.t;take=c.at('两把尺的差距');draw=easepos(t,st-.12,.82)
 retire=easepos(t,take-.25,.83);a=draw*(1-retire)
 if a<.004:return
 h=mix(504,424,glass);x0=616;x1=1027
 marks=((.28,V,'乙'),(.52,T,'丙'),(.74,C,'甲'))
 path(g,[(x0,h),(x1+3,h),(x1-13,h-9)],draw,F,2.,a)
 for i,(p,co,lab) in enumerate(marks):
  w=enter(t,st+.23+i*.13,.51);x=mix(x0,x1,p)
  if w:
   line(g,(x,h-16),(x,h+15),co,2.7,w*a);dot(g,x,h,8,co,w*a)
   label(g,lab,x,h-43,29,co,w*a)
 z=enter(t,take-.69,.55);a*=z
 if a:
  lo,hi=(mix(x0,x1,k)for k in (.28,.74))
  path(g,[(lo,h+25),(lo,h+34),(hi,h+34),(hi,h+25)],z,Y,2.1,a)
  label(g,'实力分差',.5*(lo+hi),h+64,28,Y,a)

def beats(g,c):
 """An actual 11-sector fan, tied to the score difference in the projector."""
 t=c.t
 # Linearly advance the clock only inside each semantic detent, not between
 # syllables. Both the point and the proportion have the same instantaneous p.
 turn=c.at('给每个模型')-.23;take=c.at('两把尺的差距')
 neutral=c.at('分差为零');s400=c.at('往上推四百分')
 other=c.at('另一头');fit=c.at('反过来')-.13;return_=c.at('领先四百分');upset=c.at('爆冷翻车')
 dv=(-190*easepos(t,take-.10,1.91)+190*easepos(t,c.at('代两个')-.19,max(.8,neutral-c.at('代两个')+.37))
     +400*easepos(t,s400-.08,1.23)-800*easepos(t,other-.13,1.46)+800*easepos(t,return_-.11,1.0))
 prob=1/(1+10**(-dv/400))
 a=easepos(t,take-.11,.79);r=easepos(t,fit-.38,.63)
 if a<.003:return
 graph_form=easepos(t,take-.21,1.09)
 def chart():
  from motion import formula
  mid,bot,top,width=560,637,289,726
  def xy(x,y):return mid+x/600*width/2,bot-(bot-top)*y
  pos=lambda x:xy(x,1/(1+10**(-x/400)))
  x0=mid-width*.5;xf=mid+width*.5
  path(g,[(x0,top-14),(x0,bot),(xf,bot)],graph_form,M,1.65)
  for v in (.5,10/11):
   y=xy(0,v)[1];line(g,(x0-5,y),(xf,y),E,1.3,graph_form*.77)
   label(g,'½' if v==.5 else '10/11',x0-17,y,25,M,graph_form,'right')
  for x in (-400,0,400):
   px,_=pos(x);line(g,(px,bot),(px,bot+9),M,1.55,graph_form);label(g,f'{x:+g}' if x else '0',px,bot+38,25,F,graph_form)
  p0=pos(dv)
  path(g,[pos(i)for i in range(-600,601,8)],easepos(t,take+.11,1.22),C,4.2)
  line(g,(p0[0],bot),p0,Y,2.25,graph_form);point(g,*p0,10,Y,graph_form)
  tag=c.at('指数分母');f=enter(t,tag-.23,.60)
  label(g,'分差  A − B',mid,732,27,M,graph_form)
  formula(g,'elo',550,154,583,f)
  if f and t<neutral+.71:
   reveal=during(t,tag-.14,neutral+.65,.46)
   label(g,'Δ = '+f'{dv:+.0f}',909,215,30,Y,reveal)
  # This sector belongs to the SAME variable as the dot, not a second animation.
  cx,cy,rad=1212,423,170.;ang=-pi/2
  wipe=enter(t,take+.04,.94);pie=rad*(.92+.08*wipe)
  wedge(g,cx,cy,pie,ang,ang+tau*prob,C,wipe)
  wedge(g,cx,cy,pie,ang+tau*prob,ang+tau,V,wipe)
  ring(g,cx,cy,pie,F,wipe,1.85)
  q0=enter(t,neutral-.19,.55)*(1-easepos(t,s400-.15,.40))
  if q0:
   # The vertical cut through equal areas fixes what '对半' means.
   line(g,(cx,cy-pie),(cx,cy+pie),F,1.9,q0)
  eleven=c.at('一共十一份');ten=c.at('占十份')
  odds=enter(t,eleven-.13,.76)*(1-easepos(t,other-.18,.61))
  if odds:
   for i in range(11):
    f=enter(t,eleven-.16+i*.037,.37);an=ang+tau*i/11
    line(g,(cx,cy),(cx+pie*cos(an)*f,cy+pie*sin(an)*f),BLACK,2.7,f*odds)
   f=easepos(t,ten-.18,.68);arc(g,cx,cy,pie+9,ang,ang+tau*(10/11)*max(.001,f),Y,3.9,odds)
  word=c.at('小块紫色')
  if word-.18<t<return_-.12:
   op=during(t,word-.18,return_-.12,.40)
   arc(g,cx,cy,pie+9,ang+prob*tau,ang+tau-.003,V,3.35,op)
  if upset-.44<t<fit-.26:
   # A single B win is possible with A still +400. This sweep illustrates a
   # point landing in the small sector; it doesn't move the score anymore.
   op=during(t,upset-.44,fit-.26,.37);s=easepos(t,upset-.44,.85)
   ca=ang+tau*mix(.07,prob+.50*(1-prob),s)
   x,y=cx+pie*.77*cos(ca),cy+pie*.77*sin(ca)
   line(g,(cx,cy),(x,y),F,1.8,op*.87);point(g,x,y,7.9,F,op)
   if s>.73:
    b=phase(s,.73,.99)*op
    arc(g,cx,cy,pie+8,ang+prob*tau,ang+tau-.003,V,3.6,b)
    path(g,[(cx-33,cy-pie-8),(cx-73,cy-pie-47),(cx-175,cy-pie-47)],b,V,2.2,b)
    label(g,'小概率的 B 胜',cx-180,cy-pie-48,26,V,b,'right')
  label(g,f'{prob:.1%}',cx,cy+rad+62,64,F,wipe)
  label(g,'A 在下一场获胜',cx,cy+rad+119,27,C,wipe)
  ten=c.at('十比一');hold=during(t,ten-.10,other-.05,.36)
  if hold:
   label(g,'10 : 1',cx,165,43,Y,hold);underline(g,cx-64,204,128,t-ten+.12,Y)
 screenplate(g,chart,(-105*r,27*r),1-.16*r,a*(1-r))
 if r:
  # One illustrative rail and three next-match opponents, not new observations.
  at=fit-.28
  coords=((265,344),(430,244),(589,353))
  for j,(xx,yy) in enumerate(coords):
   k=easepos(t,at+.045*j,.75)
   x,y=transit((602+68*j,500),(xx,yy),k,49+11*j)
   f=during(t,at+.045*j,fit+.56,.31)*k
   if f:point(g,x,y,5.4,(C,V,T)[j],f*.83)

def draw(g,c,oldvotes,rank):
 t=c.t;turn=c.at('给每个模型')-.23;tag=c.at('布拉德利')-.16;take=c.at('两把尺的差距')
 lay=easepos(t,tag-.18,max(.8,turn-tag+.12));compact=easepos(t,turn-.16,.97)
 if compact<.999:
  prior=cue('4-1',c.s['clock_source']=='rough')
  def votes():
   oldvotes(g,c,prior.at('现在先别')-prior.d)
   nodes=((403,488),(820,232),(1199,535))
   for j,(key,co) in enumerate((('甲赢过乙',C),('乙赢过丙',T),('丙偶尔',V))):
    start=c.at(key);q=during(t,start-.14,start+1.64,.44)
    if q:
     a,b=nodes[j],nodes[(j+1)%3];startp=lerp(a,b,.10);endp=lerp(a,b,.90)
     beam=easepos(t,start-.16,1.12);x,y=lerp(startp,endp,beam)
     tail=lerp(startp,endp,max(0,beam-.21))
     line(g,tail,(x,y),co,3.4,q);point(g,x,y,6.7,co,q)
     ring(g,*b,43+3*beam,co,q*beam,1.75)
   when=c.at('绕了一圈');focus=during(t,when-.17,when+3.7,.52)
   if focus:
    pts=((403,488),(820,232),(1199,535),(403,488))
    from motion6 import ArcLength
    rail=ArcLength(pts)
    x,y=rail.at(easepos(t,when-.11,3.23));ring(g,x,y,12,Y,focus,2.4)
  screenplate(g,votes,(-268*lay+52*compact,-8*lay),1-.36*lay-.14*compact,1-compact)
  if lay>0 and compact<.999:
   col=Y
   for k,(xx,yy,co) in enumerate(((749,552,C),(798,413,V),(858,570,T))):
    tick=enter(t,turn-.18+.08*k,.41)
    if tick:
     target=(729+71*k,503);x,y=transit((xx,yy),target,compact,20+13*k)
     point(g,x,y,5,co,tick*(1-compact))
 topic=enter(t,tag,.51)*(1-easepos(t,take-.36,.61))
 if topic:
  mark(g,'Bradley–Terry',1074,265,46,t-tag,T,mode='pen',op=topic)
  label(g,'把成对选择放到同一把尺上',1074,324,27,F,topic)
 scores_ribbon(g,c,turn,compact)
 fit=c.at('反过来')-.13
 if t<fit+.24:beats(g,c)
 if t>=fit:rank(g,c)
