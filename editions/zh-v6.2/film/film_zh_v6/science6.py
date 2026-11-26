"""Keep the real bibliographic record clear of the observer's moving silhouette."""
from rig4 import *
from studio_examples import pstep, VIO
from mounting import etch
from studio_gesture import scholar,scribe,library,workbench
from studio_science import field,helix,diene,polycurve,smooth_travel

def draw(g,c):
 from studio_exam import crystal
 t=c.t;a=c.at;start=a('GPQA');search=a('搜索引擎');diamond=a('Diamond');r1=a('两位同领域博士');proof=a('核对解析');other=a('三位其他学科');mi=a('至少十五分钟');av=a('平均三十七');one=a('一人答对');end=a('两道关都过')
 cut=phase(t,diamond-.64,diamond+.36)
 if cut<1:
  op=1-cut
  # The near plane moves most. The charge arcs can leave the frame: the viewer never needs
  # to hold three little thumbnails in mind. The second glance is at the actual counting problem.
  v=phase(t,1.56,5.20);f=phase(t,search-.62,search+.93);tg=phase(t,.05,.69)
  xc,yc,rv=smooth_travel(t,[(0,559,377,296),(1.9,566,364,302),(5.32,309,171,182),(search+.7,200,62,150),(diamond,153,45,132)])
  # Farther disciplines move less when we approach the chemical specimen.
  xb=mix(1470,1277,v)+341*f;yb=mix(248,408,v)-110*f
  helix(g,xb,yb,mix(70,102,v),mix(632,619,v),.38-.14*v,t,op*(.26+.72*v)*(1-.90*f))
  field(g,xc,yc,rv,-.10-.18*v,t,op*(1-.13*v)*(1-.72*f),pstep(t,.05,1.02))
  if tg:
   q=(xc-.10*rv,yc+.85*rv);etch(g,'物理',*q,41-.03*(296-rv),C,op*(1-.62*f),'center')
  chemx=mix(1293,689,v)+(-153)*f;chemy=mix(627,468,v)+3*f;rad=mix(150,188,v)+f*34
  diene(g,chemx,chemy,rad,-.24+.11*v-.14*f,op*(.53+.47*v),pstep(t,.38,1.0))
  xx=chemx+rad*.85;yy=chemy+rad*.62
  etch(g,'化学',xx,yy,38+5*v,'#F6BC69',op*(.52+.48*v)*(1-.91*f))
  if v>.09:
   bx=xb+55;by=yb-186
   etch(g,'生物',bx,by,37,T,op*v*(1-.83*f)*(1-phase(bx,1488,1532)))
  intro=phase(t,start-.18,start+.45)
  if intro:
   # An accession inscription, immediately below the bond it names; moves with the molecular skeleton.
   px,py=chemx+.05*rad,chemy+rad+43
   etch(g,'GPQA',px,py,33,F,op*intro,'center')
   etch(g,'博士出题，跨学科验证' if f<.50 else '甲基环戊二烯 · 公开样题',px,py+39,24,M,op*intro,'center')
  author=a('博士');intro2=phase(t,author-.09,author+.35)*(1-phase(t,search-.14,search+.40))
  if intro2:
   x,y=chemx-rad*1.86,chemy+rad*.51;stroke=phase(t,a('出题')-.11,a('出题')+.81)
   scholar(g,x,y,O,op*intro2,1.66,theta=-.1,tassel=sin(t*3))
   etch(g,'出题人 · PhD',x-2,y+62,26,O,op*intro2,'center')
   pts=((x+39,y-8),(x+66,y-56),(chemx-rad*.77,chemy+rad*.72),(chemx-rad*.55,chemy+rad*.72))
   tip=polycurve(g,pts,O,2.6,op*intro2,stroke);scribe(g,*tip,O,op*intro2,-.7,1.1)
  outsider=phase(t,a('外行')-.09,a('外行')+.42)*(1-phase(t,search+.09,search+.78))
  if outsider:
   h=phase(t,a('外行')-.10,search+.52);xx,yy=transit((xb+3,yb-96),(982,203),h,81)
   scholar(g,xx,yy,T,outsider*op,1.35,-.1,tassel=sin(t*2))
   # The hand holding the magnifier never crosses its target's letters.
   if op*outsider>.06:
    pivot=(xx+61,yy+10)
    ring(g,*pivot,12,C,op*outsider,2.5)
    path(g,[(xx+35,yy+15),(xx+54,yy+17)],1,C,2.39,op*outsider)
  if f:
   # Finding the compound and solving a new question are two genuinely different operations.
   opn=phase(t,search-.12,search+.85);xx=971;yy=332
   library(g,xx,yy,opn,op*opn,1.18)
   pre=phase(t,a('搜一搜')-.12,a('搜一搜')+.44)
   if pre:
    x3=chemx+rad*.92;y3=chemy+rad*.12
    points=[(xx-41,yy+137),(xx-85,yy+137),(x3+58,y3),(x3,y3)];path(g,points,pre,C,2.3,op*.9)
    etch(g,'产物有几种？',xx+24,yy+232,34,O,op*pre)
 if cut:
  u=cut;p=phase(t,diamond-.40,diamond+.87);r=phase(t,other-1.0,other+.42);z=phase(t,end-.34,end+.50)
  pp=phase(t,r1-.50,r1+.66);xx=mix(700,713,p)-15*pp-143*r;yy=mix(483,401,p)+30*pp-9*r
  approach=phase(t,diamond-.27,diamond+.83)*(1-phase(t,a('两道校验')-.24,r1+.12));rad=132+42*p-42*r+19*z+74*approach;ev=phase(t,proof+.05,proof+.57);expert_dim=1-.70*r
  # Two faint plane-crossings arrive on “两道校验”, then each becomes its own observable test.
  gates=phase(t,a('两道校验')-.10,a('两道校验')+.63);only=1-phase(t,r1-.30,r1+.18)
  # The two review paths resolve out of the facets, before the reviewers get the question.
  if p and not gates:
   for j,col in enumerate((C,VIO)):
    q=phase(t,diamond+.18+j*.20,diamond+1.18+j*.20);dx=(-1 if j==0 else 1)
    startp=(xx+dx*rad*.70,yy-22);endp=(xx+dx*230,yy-75+149*j)
    if q:path(g,[startp,(xx+dx*182,yy-31+85*j),endp],q,col,2.15,u*.66)
  if gates*only>.002:
   for j,col in enumerate((C,VIO)):
    x=xx+(-1 if j==0 else 1)*237
    arc(g,x,yy,91,(-.48 if not j else .52)*pi,(.48 if not j else 1.48)*pi,col,4,gates*only*u)
  crystal(g,xx,yy,rad,'#FFDB58',u,.23+.22*phase(t,diamond,r1)+.28*phase(t,proof,other)+.34*phase(t,one,end+.65))
  if ev:
   etch(g,'16',xx,yy+2,64,BLACK,u*ev,'center')
  elif p:
   diene(g,xx,yy+3,rad*.34,-.13,u*.95,col='#45350E')
  etch(g,'GPQA Diamond',xx,yy+rad*1.13+24,33,Y,u*p,'center')
  # A initially chose A, B chose B. The two check marks appear only *after reading the solution*.
  blind=a('盲做');agree=a('认同答案')
  for j,((sx,sy),col)in enumerate([((183,239),C),((297,660),T)]):
   q=pstep(t,r1-.16+j*.21,.54)
   if not q:continue
   xe,ye=xx-rad*.79,yy+(-53 if not j else 47);points=((sx+37,sy),(sx+218,sy-40),(xe-122,ye+30),(xe,ye))
   tip=polycurve(g,points,col,3.9,u*q*expert_dim,q)
   if .02<q<.98:dot(g,*tip,5.7,F,u)
   scholar(g,sx,sy,col,u*q*expert_dim,1.23,theta=(.08,-.05)[j],tassel=sin(t*2))
   etch(g,('同领域 · 甲','同领域 · 乙')[j],sx,sy+55,25,col,q*u*expert_dim,'center')
   b=pstep(t,blind-.1+j*.17,.48);agr=pstep(t,agree-.22+j*.19,.45)
   if b:
    etch(g,('初答 A','初答 B')[j],sx+48,sy-52,25,F,b*u*expert_dim)
   if ev:
    if not r>.97:
     check(g,sx+74,sy+17,10,True,agr*u*expert_dim);etch(g,'同意 B',sx+99,sy+21,24,T,agr*u*expert_dim)
  if ev and r<1:
   # A geometrical reading of the source's 4 × 4; the answer is withheld during the blind attempt.
   for i in range(16):
    row,col=divmod(i,4);zz=pstep(t,proof-.11+row*.064+col*.032,.34);x=1034+col*49-row*7;y=272+row*50+col*3
    if zz:dot(g,x,y,11.7,(T,C,O,VIO)[row],u*zz*(1-r))
   etch(g,'4 × 4 = 16',1102,509,42,F,u*ev*(1-r),'center')
   etch(g,'核对解析',1102,558,25,M,u*ev*(1-r),'center')
  if r>.0001:
   # Three trained researchers enter from OUTSIDE the subject. Their badges keep their identity
   # when borrowing the same book, writing on scratch paper and finally turning in C/B/A.
   sm=a('聪明');ne=a('非专家');web=a('谷歌');ret=a('结果三人')
   req=phase(t,ne-.10,ne+.51);look=phase(t,a('放开')-.05,web+.48)*(1-phase(t,ret+1.45,ret+2.04));res=phase(t,ret-.04,ret+.76)
   people=((1048,154),(1390,370),(1123,621));colors=(VIO,T,O)
   for j,((px,py),co) in enumerate(zip(people,colors)):
    q=pstep(t,other-.12+.16*j,.51)
    if not q:continue
    src=((1530,44),(1630,355),(1462,737))[j];px,py=transit(src,(px,py),q,22*(j-1))
    scholar(g,px,py,co,u*q,1.64,theta=(-.13,.08,-.06)[j],tassel=sin(t*2+j))
    note=phase(t,sm-.10+j*.045,sm+.56+j*.10)*(1-res)
    if note:workbench(g,px+2,py+61,j,note,t,u*note,co)
    if req:
     dest=(xx+rad*.70,yy+(-58+j*56));points=((px-47,py),(px-169,py+(32-j*31)),(dest[0]+176,dest[1]),dest)
     tip=polycurve(g,points,co,3.0,req*u*(.60+.40*res),req)
     if req<.999:dot(g,*tip,6,F,u)
     if .02<look and not res:
      b=phase(t,web-.12+j*.09,web+.66+j*.09);s=transit((px-39,py),(400,382),b,170+35*j)
      if 0<b<1:dot(g,*s,7,co,u)
    if res:
     ch=('C','B','A')[j];etch(g,ch,px+58,py-6,52,co,u*res,'center')
     d=pstep(t,one-.12+.12*j,.45);check(g,px+96,py-16,11,j==1,u*d)
   # Non-expert here means *outside this subject*, not underqualified. Bring back the field/helix
   # dialects of the opening as one mixed strand, before the three independent scratches begin.
   home=phase(t,other-.09,other+.40)*(1-phase(t,mi+.08,mi+.72))
   if home:
    xh,yh=1213,228;am=29
    for fi,cc in enumerate((C,T)):
     v0=[(xh-101+z*4.1,yh+(z/50-.5)*19+am*sin(z*.15+fi*pi))for z in range(51)]
     path(g,v0,home,cc,3.05,u*home)
    etch(g,'跨学科',xh,yh-55,29,F,u*home,'center')
   if req and not res:
    h=phase(t,ne-.1,ne+.50);gg=(xx+rad*.72,yy-2);rr=18+11*h
    arc(g,*gg,rr,-.5*pi,1.33*pi,O,3.3,h*u)
   # The same book the question-writer consulted reopens on the Google cue.
   if look:
    library(g,83,335,phase(t,web-.19,web+.48),u*look,1.09)
    etch(g,'Google',81,288,29,T,u*look)
   timer=phase(t,mi-.18,mi+.46);m=phase(t,av-.1,av+.50)
   if timer:
    x=820;y=193;rad2=48
    ring(g,x,y,rad2,M,u*timer,1.9);angle=-pi/2+tau*(15*timer+22*m)/60
    arc(g,x,y,rad2,-pi/2,angle,O,5,u*timer);line(g,(x,y),(x+34*cos(angle),y+34*sin(angle)),O,3.1,u*timer);dot(g,x,y,4,F,u*timer)
    etch(g,'平均 37 分钟' if m>.5 else '至少 15 分钟',x,y+75,26,O,u*timer,'center')
   if z:
    etch(g,'2 / 2',361,405,41,T,u*z,'center');etch(g,'1 / 3',1292,537,43,VIO,u*z,'center')
