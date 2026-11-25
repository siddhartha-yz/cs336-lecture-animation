"""Working deliverables: a cable-reel stand you can rotate, and four named items you can permute."""
from ink import *
from motion import transit,guide
from studio_examples import silk,pstep,area,VIO,AQUA,BLUE,MONO
from ink_words import carryword,swish
from timeline3 import S,W,clock,remap
from termnotes import hint
from types import FunctionType
from functools import lru_cache
def reel(g,cx,cy,scale,theta,op=1,parts=1):
 # Orthographic projections of ONE mesh. In the model, axis X goes through both flanges.
 pt=lambda a,b,c:(cx+scale*(a*math.cos(theta)+c*math.sin(theta)),cy+scale*(-b*.89+(-a*math.sin(theta)+c*math.cos(theta))*.43),-a*math.sin(theta)+c*math.cos(theta)+b*.08)
 faces=[]
 def face(coords,color,light):
  pts=[pt(*v)for v in coords];faces.append((sum(v[2]for v in pts)/len(pts),pts,color,light))
 def beam(a,b,w):
  # A flat, slightly deep steel member in the Y/Z plane at one X.
  x,y,z=a;xx,yy,zz=b;dy=yy-y;dz=zz-z;ll=hypot(dy,dz)or 1;p=-dz*w/ll;q=dy*w/ll
  v0=[(x,y+p,z+q),(x,yy+p,zz+q),(x,yy-p,zz-q),(x,y-p,z-q)]
  face(v0,O,.60);face([(a0+9,b0,c0)for a0,b0,c0 in v0],O,.80)
 for x in(-127,127):
  beam((x,-135,-104),(x,0,0),11);beam((x,-135,104),(x,0,0),11);beam((x,-139,-118),(x,-139,118),8)
 def cylinder(x0,x1,r,col,n=48):
  pts=[(r*sin(k*tau/n),r*cos(k*tau/n))for k in range(n)]
  for k,(yy,zz)in enumerate(pts):
   v,w=pts[(k+1)%n];face([(x0,yy,zz),(x1,yy,zz),(x1,v,w),(x0,v,w)],col,.34+.40*(.5+.5*sin(k*tau/n+.6)))
  face([(x0,y,z)for y,z in pts],col,.43);face([(x1,y,z)for y,z in pts],col,.66)
 cylinder(-80,80,51,BLUE,42)
 for sgn in(-1,1):cylinder(sgn*86-4,sgn*86+4,96,T,52)
 cylinder(-163,163,7.4,O,12)
 for z,pts,col,level in sorted(faces,key=lambda f:f[0]):
  area(g,[p[:2]for p in pts],inkcol(col,level),op)
 for sx in(-86,86):
  front=1 if (sx>=0)==(sin(theta)<0)else .5
  for r in(96,52,12):
   a=[pt(sx,r*sin(j*tau/64),r*cos(j*tau/64))[:2]for j in range(65)]
   path(g,a,1,T if r!=12 else O,2.0 if r==96 else 1.3,op*front)
  for j in range(6):
   an=j*tau/6
   line(g,pt(sx,25*sin(an),25*cos(an))[:2],pt(sx,78*sin(an),78*cos(an))[:2],T,1.7,op*front)
def ortho(g,x,y,z,op=1,q=1):
 ctx=g.c;ctx.save();ctx.translate(x,y);ctx.scale(z,z)
 # Sheet boundary is an engineering title line, not the placeholder's folded corner.
 tt=op
 line(g,(-179,-94),(180,-94),O,1.5,tt);line(g,(-179,106),(180,106),O,1.5,tt)
 for j,rad in enumerate((57,32,8)):
  arc(g,-85,0,rad,-pi/2,-pi/2+tau*max(.001,q),C,2,tt)
 for off in(-1,1):
  path(g,[(-85,-2),(-85+off*67,72),(-85,72)],q,O,2.0,tt)
 for a,b in [((39,-45),(39,52)),((132,-45),(132,52)),((40,-30),(130,-30)),((40,31),(130,31)),((31,0),(143,0))]:path(g,[a,b],q,C,2,tt)
 for j in range(2):
  x0=35+j*98;path(g,[(x0-19,69),(x0,0),(x0+19,69)],q,O,2,tt)
 if q>.8:txt(g,'正视',-84,151,23,M,op);txt(g,'侧视',87,151,23,M,op)
 ctx.restore()
def real_work(g,c,medical_only=False):
 t=c.t;ex=c.at('圈对一个字母');draw=c.at('交上一张');src=c.at('一堆材料');eco=c.at('生态效度');data=c.at('GDPval');reel_=c.at('卷筒参数');jig=c.at('夹具的设计图');med=c.at('斯坦福');rec=c.at('临床工作任务');note=c.at('起草病历');decision=c.at('辅助临床决策');meaning=c.at('真实工作长得越像')
 zone=1-phase(t,med-.56,med-.14);geo=phase(t,eco-.40,eco+.25)
 if zone and not medical_only:
  a=zone
  silk(g,'考卷上的一格，车间里的一件东西',131,102,43,t-.06,F,a*(1-geo),align='left')
  if geo:
   silk(g,'生态效度',130,100,50,t-eco+.24,F,a*geo,align='left')
   silk(g,'考题与实际工作有多像',132,160,25,t-eco-.18,M,a*geo,align='left')
  sq=phase(t,src-.38,src+.52);o=a*(1-sq)
  if o:
   txt(g,'交一个选项',355,307,30,M,o);p=pstep(t,ex-.16,.61)
   for j,le in enumerate('ABCD'):
    xx=190+107*j;txt(g,le,xx,431,48,Y if j==2 else F,o)
    if j==2 and p:arc(g,xx,431,42,-.77*pi,-.77*pi+tau*p,Y,3,o)
   line(g,(124,518),(582,518),E,1.5,o)
  ask=pstep(t,draw-.19,.6)
  if ask:
   pos=phase(t,reel_-.39,jig+.27);theta=.29+.66*phase(t,draw-.2,src+.84)+.52*pos
   xx=mix(1110,797,sq);yy=443
   reel(g,xx,yy,1.05+.14*pos,theta,a*ask);txt(g,'卷盘支架 · 结构示意',xx,682,27,T,a*ask)
  if sq:
   o=sq*a
   txt(g,'卷筒参数',273,331,29,C,o)
   # Dimension witnesses without fabricated numerical tolerances.
   for i,(lab,w0,col)in enumerate((('宽度',135,C),('直径',177,T),('轴径',70,O))):
    y=415+69*i;x=155;txt(g,lab,x,y,24,col,o,'left');p=pstep(t,src-.11+i*.14,.66);line(g,(x+73,y),(x+73+w0*p,y),col,2.4,o)
    if p:line(g,(x+73+w0*p,y-8),(x+73+w0*p,y+8),col,1.6,o)
   xx,yy=1282,437;op=phase(t,src-.28,src+.61)
   ortho(g,xx,yy,.80,op*a,phase(t,src-.05,src+2.06))
   if t>=data-.35:
    silk(g,'GDPval',1267,106,48,t-data+.22,F,o,'pen');silk(g,hint('GDPval'),1267,164,23,t-data-.16,M,o)
   if t>jig-.29:swish(g,1131,1412,586,t-jig+.12,O,.58)
 if not zone>=1:
  op=1-zone;ii=pstep(t,med-.13,.69)
  silk(g,'MedHELM',135,104,51,t-med+.16,F,op,'pen','left');silk(g,hint('MedHELM'),139,163,26,t-med-.18,M,op,align='left')
  txt(g,'一次就诊',291,287,29,T,op*ii)
  for j in range(38):
   p=pstep(t,med-.06+j*.035,.47);u=phase(t,rec-.20,rec+.8);h=16+58*abs(sin(.52*j)*cos(j*.32+t*.73*(1-u)))
   rect(g,139+j*7.9,444-h*.5,4.8,h,T,op*p)
  k0=phase(t,rec-.15,rec+.65);k1=pstep(t,note-.35,.60);k2=pstep(t,decision-.34,.64)
  if k0:
   path(g,[(456,442),(563,442),(563,351),(690,351)],k0,T,2.4,op);path(g,[(564,443),(564,570),(690,570)],k0,VIO,2.4,op)
  if k1:
   silk(g,'病历草稿',752,339,35,t-note+.23,C,op,align='left')
   for j,ss in enumerate(('主诉','就诊经过','随访记录')):
    txt(g,ss,1084+j*119,352,24,F,op*k1)
    if j<2:line(g,(1124+j*119,352),(1146+j*119,352),M,1.4,op*k1)
  if k2:
   silk(g,'辅助决策',752,569,35,t-decision+.27,VIO,op,align='left')
   for j,col in enumerate((T,O)):
    path(g,[(1041,569),(1125,569),(1175,528+j*83),(1375,528+j*83)],pstep(t,decision+.10+j*.08,.61),col,2.3,op);dot(g,1375,528+j*83,5.7,col,op*k2)
  if t>=meaning-.34:silk(g,'任务分开测，交付物也分开看。',802,712,27,t-meaning+.21,M,op)
def item(g,x,y,w,h,col,op=1,lines=6,signature=0,active=-1):
 # Four actual topics carried across the exchangeability example, recognised here by persistent ink.
 lab=('青蛙','能量','电影','捷豹')[signature%4];num=('温度','质量','评分','车型')[signature%4]
 rect(g,x,y+2,w,h-4,inkcol(col,.32),op);line(g,(x,y+h),(x+w,y+h),col,2,op)
 txt(g,lab,x+w/2,y+h*.37,min(25,w*.27),F,op);txt(g,num,x+w/2,y+h*.72,min(17,w*.18),col,op)
@lru_cache(None)
def shuf():
 from validity import shuffle
 gg={**shuffle.__globals__,'docs':item}
 return FunctionType(shuffle.__code__,gg,shuffle.__name__,shuffle.__defaults__,shuffle.__closure__)
def shuffle(g,c):
 from direct import state
 b=state('7-2')[1];shuf()(g,b.clock(remap('7-2',c.t)))
