from termnotes import hint
from ink import *
from motion import guide,transit,emphasize
from itertools import combinations
def network(g,x,y,rx,ry,t,op=1,cycle=0,collapse=0,num=16):
 pt=[]
 for i in range(num):
  a=tau*i/num-.7
  rr=.72+.28*((i*7)%11)/10
  xx=x+rx*rr*cos(a+.035*sin(t*.16+i));yy=y+ry*rr*sin(a+.028*cos(t*.19+i))
  pt.append((mix(xx,x+rx*.78,collapse),mix(yy,y-ry+2*ry*i/(num-1),collapse)))
 for i in range(num):
  for m in (1,4):
   if m==4 and i%3:continue
   j=(i+m)%num;p=(t*.095+i*.171+m*.12)%1
   line(g,pt[i],pt[j],E,1.5,op*.70)
   if i%3==1:dot(g,*lerp(pt[i],pt[j],p),3,T,op*(1-collapse))
 for i in range(num):dot(g,*pt[i],5 if i not in (0,6,11) else 8,(C,T,V)[i%3],op)
 if cycle:
  tri=(0,6,11,0)
  for j,(i,k) in enumerate(zip(tri,tri[1:])):
   a=pt[i];b=pt[k];arrow(g,a,lerp(a,b,.92),phase(cycle,.19*j,.19*j+.57),Y,op,2.8)
  for j,i in enumerate(tri[:3]):
   xx,yy=pt[i];txt(g,'ABC'[j],xx+(-22 if j==1 else 19),yy-17,25,Y,op*cycle)
def arena(g,c):
 t=c.t;blind=on(c,'两个匿名模型',1.7);vote=on(c,'投票',1.0);wide=on(c,'模型有上百个',2.3);edge=on(c,'A 赢过 B',2.3);lad=on(c,'统一的能力天梯',2.2)
 title(g,'Chatbot Arena',104,sub='一张选票，约束一对模型')
 # Anonymous paired answers travel apart into two nodes of the very network they create.
 for i,col in enumerate((C,V)):
  x=mix(570+i*455,440+i*678,wide);sw=mix(265,28,wide);h=mix(178,28,wide)
  grow=phase(t,1.1+i*.65,c.at('匿名模型')+1.7+i*.3)
  docs(g,x-sw/2,337,sw,h,col,(1-wide),0,i)
  for j in range(5):
   z=phase(grow,.115*j,.53+.115*j);xx=x-sw*.375;yy=337+h*(.20+j*.145)
   tar=sw*(.39+.36*((j*11+i*3)%13)/12)
   line(g,(xx,yy),(xx+tar*z,yy),Y if i and j==2 and vote>.55 else col,2.7,(1-wide)*z)
  txt(g,'回答 '+('A','B')[i],x,300,32,col,1-wide)
 if 0<blind<1:
  # Candidate colour follows the answer; neither author is revealed before the vote.
  for i in range(2):
   x=570+i*455;line(g,(x-65,548),(x+65,548),E,1.3,sin(pi*blind))
 if vote and wide<1:
  x,y=curve((1027,524),(795,617),vote,60);dot(g,x,y,10,Y,(1-wide));txt(g,'偏好 B',800,680,30,Y,vote*(1-wide))
 if wide:
  network(g,800,450,510,200,t,wide,edge,lad*.54)
  txt(g,'两两胜负可以成环',799,699,32,Y,edge*(1-lad*.45))
def bias(g,c):
 t=c.t;pos=on(c,'位置偏见',1);swap=on(c,'互换位置',2.1);selfp=on(c,'自我偏好',1.5);long=on(c,'长度偏见',1.7);ext=on(c,'更长',2.7)
 same=phase(t,c.at('写法相近')-.33,c.at('写法相近')+.57);reword=phase(t,c.at('换一种措辞')-.20,c.at('内容没变')+.12)
 style=same*(1-phase(t,c.at('长度偏见')-.74,c.at('长度偏见')-.22))
 generic=1-phase(t,c.at('三个偏差')-.65,c.at('三个偏差')-.22)
 mention=c.at('GPT-4');judge=phase(t,mention-.20,mention+.64);ready=c.at('低成本自动化打分')
 if generic:
  title(g,'还要等多少张选票？',110,generic*(1-phase(t,mention-.68,mention-.20)),sub='两份回答已经写好')
  title(g,'LLM-as-a-Judge',110,generic*judge,sub=hint('LLM-as-a-Judge'))
 if generic<1:title(g,'同一位裁判，三种偏差',110,phase(t,c.at('三个偏差')-.16,c.at('三个偏差')+.44),sub='答案的身份用颜色追踪')
 lx,rx=461,1139;yy=410
 # The reader's eye stays on the judge. Lift the two signed pages into disjoint
 # lanes before passing it; an ordinary pair of shallow arcs masks the judge at midpoint.
 lift=phase(swap,0,.29)*(1-phase(swap,.71,1));cross=phase(swap,.11,.89)
 scale=mix(1,.55,lift)
 for i,col in enumerate((C,V)):
  xx=mix(lx,rx,cross) if i==0 else mix(rx,lx,cross);y0=yy+(-165 if i==0 else 178)*lift
  g.c.save();g.c.translate(xx,y0);g.c.scale(scale,scale);g.c.translate(-xx,-y0)
  h=143+(85*ext if i==0 else 0)
  docs(g,xx-135,y0-60,270,h,col,1,0,i)
  for n in range(4):
   lx1=xx-135+270*.12;yy1=y0-60+143*(.21+n*.62/3);lng=270*(.39+.37*((11*n+3*i)%13)/12)
   focus=selfp*(1-long) if i==1 and n==2 else 0
   # The third sentence can be rephrased; the other assertions stay put.
   if i==1 and n==2 and style:
    seam=.52-.17*reword
    line(g,(lx1,yy1),(lx1+lng*(seam-.03*style),yy1),blend(col,Y,focus),2.8,.56+.44*focus)
    line(g,(lx1+lng*(seam+.03*style),yy1),(lx1+lng,yy1),blend(col,Y,focus*(1-.32*style)),2.8,.56+.44*focus)
    dot(g,lx1-10,yy1,3.5,T,style)
   else:line(g,(lx1,yy1),(lx1+lng,yy1),blend(col,Y,focus),2.8,.56+.44*focus)
  txt(g,'回答 '+('A','B')[i],xx,y0-105+(10*lift if i==0 else 0),29,col)
  if i==0 and ext:
   for j in range(4):
    le=phase(ext,j*.14,.5+j*.12);line(g,(xx-95,y0+85+j*15),(xx-95+160*le,y0+85+j*15),R,2.5,le)
  g.c.restore()
 # Time to acquire a human preference is different from the time to emit an answer.
 # Each ballot crosses the midpoint only once; arrivals feed a visibly unfinished tally.
 human=1-judge
 if human:
  start=c.at('今天改了模型');until=c.at('几万张选票')
  for j in range(7):
   voter(g,605+j*64,598,T,human*phase(t,.26+.12*j,.73+.12*j),.67)
   p=phase(t,start+.60*j,until+.64+.49*j);a=human*phase(t,start-.30,start+.21)
   if a:
    dest=(704+j*32,485);xx,yy=transit((605+j*64,573),dest,p,16)
    box(g,xx-8,yy-5,16,10,Y,a,fill=inkcol(Y,.14),sw=1.45)
  txt(g,'等真人投票',800,682,27,T,human)
  line(g,(691,502),(914,502),M,1.4,human*phase(t,start,start+.54))
 prism=judge
 if prism:
  g.poly([(800,301),(841,369),(800,425),(759,369)],V,2.6,prism,True,inkcol(V,.13),1)
  txt(g,'裁判',800,461,30,V,prism)
  txt(g,'GPT-4',800,270,24,V,prism*generic)
  if style:
   line(g,(780,369),(800,369),Y,2.6,style);line(g,(804,369),(820,369),Y,2.6,style)
  for j,px in enumerate((461,1139)):
   p=phase(t,mention-.06+j*.18,mention+1.08+j*.18)
   if 0<p<1:guide(g,[(px+(151 if j==0 else -151),398),(px+(192 if j==0 else -192),398),(758 if j==0 else 842,369)],p,Y,1,2.6,.48)
 if judge*generic:
  bench=1-phase(t,c.at('把两份答案一换')-.32,c.at('把两份答案一换')+.21)
  for j,(name,gloss,px,col,word) in enumerate((('AlpacaEval','单轮开放回答',575,C,'AlpacaEval'),('MT-Bench','多轮对话',1025,V,'MT-Bench'))):
   tm=c.at(word);k=phase(t,tm-.19,tm+.52)
   if k:
    path(g,[(800,487),(800,523),(px,523),(px,551)],k,col,1.45,.72*bench)
    txt(g,name,px,604,31,col,k*bench);txt(g,gloss,px,655,24,M,k*bench)
    rect(g,px-37,571,74*k,2,col,k*bench)
  tick=phase(t,ready-.12,ready+.64)
  if 0<tick<1:emphasize(g,800,370,85,125,tick,Y)
 if pos:
  oldvote=1-phase(t,c.at('自我偏好')-.48,c.at('自我偏好')-.10)
  if oldvote:arrow(g,(lx,660+22*lift),(lx,610+40*lift),pos,Y,oldvote,3)
  # Length cannot have won a vote before there is a longer reply. Release a
  # new mark from the judge only on the spoken verdict, after the extra lines.
  vote=phase(t,c.at('更容易给高分')-.12,c.at('更容易给高分')+.83)
  if vote:
   vx,vy=transit((843,369),(rx+105,615),vote,59)
   dot(g,vx,vy,5.5,Y,phase(vote,0,.14))
   if vote>.55:check(g,rx+105,615,12,True,phase(vote,.55,1))
  label='位置偏见' if selfp<.5 else '自我偏好' if long<.5 else '长度偏见'
  txt(g,label,800,696,35,(O,V,R)[0 if selfp<.5 else 1 if long<.5 else 2])
 if selfp and not long>=1:
  pts=[(774,367),(702,367),(635,407),(576,407)];k=(t*.26)%1
  path(g,pts,1,V,2,selfp*(1-long));dot(g,*lerp(pts[1],pts[2],k),5,V,selfp*(1-long))

from judge_lens import rating,length
