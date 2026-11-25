"""A single prompt, two recorded answers. A street lamp and the mall leave the written excerpts legible."""
from ink import *
from motion import transit
from ink_words import swish
from studio_examples import pstep,silk,area,symbol,works,arena as network,VIO,BLUE
from mounting import etch
def caretaker(g,x,y,k,col,op,s=1):
 # A small maintenance robot with one articulated hand and two rolling wheels.
 ctx=g.c;ctx.save();ctx.translate(x,y);ctx.scale(s,s)
 area(g,[(-25,-22),(15,-25),(23,-9),(20,7),(-26,7)],inkcol(col,.68),op)
 path(g,[(-25,5),(-25,-20),(14,-25),(23,-9),(20,7)],1,col,2.2,op)
 dot(g,13,-14,3.4,F,op)
 for xx in(-17,14):
  dot(g,xx,11,7.0,col,op);line(g,(xx-5*cos(k),11-5*sin(k)),(xx+5*cos(k),11+5*sin(k)),F,1.35,op)
 q=(30+17*cos(k*.45),-24+14*sin(k*.45))
 path(g,[(13,-5),(36,-8),q],1,col,2.7,op);dot(g,*q,4,O,op)
 ctx.restore()
def vignette(g,i,x,y,s,t,a,words):
 if a<.001:return
 ctx=g.c;ctx.save();ctx.translate(x,y);ctx.scale(s,s);co=(C,VIO)[i]
 # Cropped setting, not a border. A few perspective lines belong to the text that we are reading.
 if i==0:
  # Brass lamps recede down the actual cobbled street in reply A.
  for j,(xx,yy,sz)in enumerate(((-258,36,1.82),(-421,7,.91),(-519,-14,.50))):
   symbol(g,'A',xx,yy,sz,a*(1-.24*j),.88+.10*math.sin(t*.42+j))
  path(g,[(-546,-7),(-457,22),(-231,199),(123,244)],1,BLUE,2.3,a*.43)
  for j in range(7):
   x0=-491+j*40;yy=32+.19*(x0+491);path(g,[(x0,yy),(x0+15,yy-8),(x0+38,yy+2)],1,BLUE,1.4,a*.45)
 else:
  # A single plant is part of response B. Behind it, shutters and the receding concourse.
  symbol(g,'B',-143,104,1.45,a,.72+.28*phase(t,1.3,4.7))
  for j in range(3):
   xx=148+j*61;yy=26-13*j;path(g,[(xx,yy),(xx+44,yy-10),(xx+44,yy+63-j*8)],1,VIO,2.2,a*(.55-.11*j))
  path(g,[(-146,213),(75,177),(333,101)],1,VIO,2.1,a*.68)
 # Each character carries out a different action from the recorded story.
 walk=phase(t,1.0,7.32);read=phase(t,7.32,13.7)
 if i==0:
  bx=mix(-325,-203,walk);by=144;caretaker(g,bx,by,4.4*walk+2.2*read,C,a,1.04)
  polish=phase(t,3.1,7.45)
  if polish and t<12.2:
   m0=clip((t-3.5)/2.6);px=-245;py=-39
   arc(g,px,py,11+5*m0,-2.5,-2.5+tau*m0,O,2.2,a*(1-phase(t,8.3,10.1)))
 else:
  bx=mix(134,-52,phase(t,1.95,9.9));caretaker(g,bx,142+(bx-110)*.06,5.7*walk+2.8*read,VIO,a,1.04)
 xx=-141 if i==0 else -72; yy=-93 if i==0 else -120
 rows=(('734 号的唯一职责，','是擦亮城里的黄铜路灯。'),('老维修机器人驶过','空无一人的购物中心。'))[i]
 etch(g,'AB'[i],xx,yy-51,36,co,a)
 for j,word in enumerate(rows):
  r=pstep(t,words+.18*j,.42);silk(g,word,xx,yy+j*48,37,t-words-.18*j,F,a,'wave','left',.42)
 if i==1 and t>.9:
  at=phase(t,words,words+.9);x0=xx;y0=yy+82;line(g,(x0,y0),(x0+302*at,y0),co,1.8,a*.75)
 ctx.restore()
def arena(g,c):
 t=c.t;a=c.at;anon=a('两个匿名');think=a('先给更');vote=a('投票谁更好');lead=a('把这一票留下');source=a('真实问题');bt=phase(t,lead-.25,lead+.75)
 if t<.76:
  # Match the old mail strip, but just its type and ink, not an entire frozen screen of labels.
  r=phase(t,0,.74);ctx=g.c;ctx.save();ctx.translate(0,(-554)*r);ctx.scale(1+.03*r,1+.03*r);works(g,8,1);ctx.restore()
 if bt<1:
  op=(1-bt);overview=phase(t,.20,1.55);op1=pstep(t,.32,.53);op2=pstep(t,.92,.55)
  drift=phase(t,think-.23,think+.71);q=phase(t,source-.37,source+.55);r=phase(t,anon-.20,anon+.40);decl=pstep(t,vote-.11,.51)
  # Deliberately stagger depth, baseline and area like two scenes of the same story, not two columns on a slide.
  x0=mix(493,457,overview)+31*drift; y0=mix(302,335,overview); x1=mix(1227,1129,overview)-12*drift; y1=mix(603,513,overview)
  vignette(g,0,x0,y0,1.05,t,op*op1,.45);vignette(g,1,x1,y1,1.14,t,op*op2,.98)
  if drift:
   # The two empty ballot marks stay unfilled throughout the viewer's own silent choice.
   for xx,yy,co in ((x0-114,370,C),(x1-57,601,VIO)):
    cc=phase(t,think-.16,think+.38);ring(g,xx,yy,14.6,co,op*cc*(1-decl),2.4)
  if q:
   # This is the translated original user prompt, connected to both responses. It is not a title.
   pos=(807,172);col=O;etch(g,'“写一个关于机器人的短篇故事。”',pos[0],pos[1],29,col,op*q,'center')
   for j,(px,py)in enumerate(((575,204),(1064,316))):
    z=pstep(t,source-.15+j*.12,.61);path(g,[(802+(j-.5)*202,198),(px,py-16),(px,py)],z,VIO if j else C,1.7,op*q)
   if r and not decl:etch(g,'匿名对战',857,196,22,M,op*r,'center')
  if decl:
   px0=x1-57;py0=601
   xy=transit((799,693),(px0,py0),decl,79);dot(g,*xy,9,Y,op*decl)
   etch(g,'原记录：B 获选',px0+34,py0,26,Y,op*decl)
  if q:etch(g,'Chatbot Arena · 真实回答节译',407,690,23,M,op*q)
 if bt:
  network(g,c,True)
