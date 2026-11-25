"""Publication dates drawn on one reel: two actual AtCoder examples, then two distinct protections."""
from ink import *
from ink_words import swish
from studio_examples import pstep,area,BLUE,VIO
from mounting import etch
from studio_corpus import HIST,dx
from motion import transit
P1,P2=HIST['contest_examples']
PRODUCTS=[i*j for i in range(1,10)for j in range(1,10)]
assert sum(x for x in PRODUCTS if x!=24)==1929 and PRODUCTS.count(24)==4
def seal(g,xx,yy,b,open_,op=1):
 # An actual shutter with overlapping opaque leaves: the held-out pattern is hidden, not merely labelled private.
 pts=[(xx+cos(i*tau/6)*b,yy+sin(i*tau/6)*b)for i in range(6)]
 g.poly(pts,C,3,op,True,'#103442',1)
 for i in range(6):
  a=i*tau/6;v=a+.72;tip=(xx+open_*.72*b*cos(v),yy+open_*.72*b*sin(v));j=(i+1)%6
  area(g,[pts[i],pts[j],tip],('#227B91','#165769')[i%2],op)
  line(g,pts[i],tip,C,2.4,op)
 if open_>.02:
  inner=[(xx+b*.51*open_*cos(i*tau/6+.72),yy+b*.51*open_*sin(i*tau/6+.72))for i in range(6)];area(g,inner,BLACK,op)
  for i,v in enumerate([.31,.87,.56,.71,.37,.93,.53]):
   o=b*.38*open_;x=xx+(i-3)*o*.245;rect(g,x-2.9,yy-v*o*.5,5.8,v*o,T,op)
def newtests(g,c):
 t=c.t;a=c.at;train=a('训练结束以后');new=a('再把新题');name=a('LiveCodeBench');dates=a('竞赛日期');aug=a('八月出的');jan=a('隔年一月');cut=a('九月底停止');pick=a('右边这题');secret=a('机构内部');hold=a('最终校验');audit=a('专家二次审计');refine=a('高可信度')
 yy=594;dx0=dx(HIST['example_cutoff']);sec=phase(t,secret-.70,secret+.14);op=1-sec
 if op>.001:
  # A row of old material becomes a spine; the fixed place on the spine distinguishes 'came before'.
  m=phase(t,.29,new+.33);older=1-phase(t,new-.17,new+.48)
  if older:
   # Material from the previous shot still has readable words, rather than a new diagram of bars.
   tokens=('permission','is','hereby','granted','free','of','charge')
   for j,ss in enumerate(tokens):
    u=clip((t-.15-j*.22)/2.15)
    if 0<u<1:
     xx,yt=transit((215+156*j,299+37*(j%2)),(236+j*93,yy-74),u,47)
     etch(g,ss,xx,yt,31,C,older*op*.89*sin(pi*u)**.45,'center')
   l1=173;l2=dx0-40
   for j in range(27):
    xx=mix(l1,l2,j/26);target=xx-118*phase(t,.38+j*.024,train+.15)
    size=30+13*((j*5)%7);rect(g,target,yy-size-31,11,size,BLUE,op*older*(.53+.45*j/26))
   etch(g,'训练语料',226,yy-200,35,C,op*older)
   path(g,[(235,yy-159),(235,yy-125),(267,yy-105)],1,C,1.7,op*older)
  p=pstep(t,.09,.91);path(g,[(131,yy),(1470,yy)],p,M,2.2,op)
  moved=phase(t,new-.18,name+.25);shutter=phase(t,train-.18,train+.53)*(1-phase(t,name-.32,dates+.21)) + phase(t,cut-.31,cut+.39)
  h=mix(126,333,phase(t,cut-.55,cut+.58))
  if shutter:
   line(g,(dx0,yy-h),(dx0,yy+55),Y,3.1,op*shutter)
   area(g,[(dx0-9,yy-h-2),(dx0+9,yy-h-2),(dx0,yy-h+13)],Y,op*shutter)
   if t<name:etch(g,'训练结束',dx0-17,yy-h-9,30,Y,op*shutter,'right')
   else:etch(g,'2024-09-30',dx0-15,yy-111,26,Y,op*shutter,'right')
  if moved:
   etch(g,'2023.05',145,yy+34,22,M,op*moved)
   if t<aug-.23:
    vis=pstep(t,new+.14,.59)*(1-phase(t,aug-.90,aug-.23))
    etch(g,'累计收题',787,356,34,C,op*vis,'right')
    path(g,[(791,381),(824,402),(dx('2024-05'),yy-72)],vis,C,1.6,op*vis)
   # The six cumulative releases contribute different real heights, not six repeated cards.
   points=[]
   for j,(tag,day,n)in enumerate(HIST['releases']):
    x=dx(day);q=pstep(t,new+.17+j*.26,.60);ht=104*n/1055
    if q:
     rect(g,x-10,yy-ht*q,20,ht*q,BLUE,op*q*.95)
     if j in (0,5) or t<aug-.60:
      etch(g,str(n),x,yy-ht*q-21,26,C,op*q,'center')
     etch(g,tag,x,yy+35,20,M,op*q,'center')
   live=pstep(t,name-.16,.65);xx=dx(HIST['releases'][0][1])
   if live:
    path(g,[(xx-5,yy+45),(xx-45,yy+77),(xx-167,yy+77)],live,C,1.6,op*live)
    etch(g,'LiveCodeBench',xx-177,yy+73,32,C,op*live,'right')
    etch(g,'按竞赛日期收录编程题',xx-178,yy+110,24,M,op*live,'right')
   # Before examples appear, a pair of holes is punched in the tape at their precise dates.
   showdates=pstep(t,dates-.13,.57)
   for j,d in enumerate((P1,P2)):
    co=(O,T)[j];xx=dx(d['day']);ev=(aug,jan)[j];focus=pstep(t,ev-.19,.55)
    bright=op*showdates*(1-.76*phase(t,cut-.20,cut+.60) if not j else 1)
    if not bright:continue
    dot(g,xx,yy,7,co,bright)
    if not focus:continue
    opt=bright*focus
    # Actual dates stay on the spine as the samples grow out of them.
    xp=(547,1206)[j];yp=425 if not j else 422
    path(g,[(xx,yy-8),(xx,yy-100),(xp,yp+47)],focus,co,2.3,opt)
    etch(g,d['day'],xp,yp+24,30,co,opt,'center')
    etch(g,d['title'],xp,217 if not j else 172,31,F,opt,'center')
    if not j:
     coords=(369,541,719)
     for i,(x0,value)in enumerate(zip(coords,(1,6,26))):
      f=pstep(t,aug-.19+i*.34,.45)
      if f:
       dot(g,x0,336,34*f,O,opt*.32);ring(g,x0,336,34*f,O,opt,2)
       etch(g,str(value),x0,336,34,O,opt*f,'center')
      if i:
       arrow(g,(coords[i-1]+42,336),(x0-45,336),f,O,opt,2.5)
       etch(g,('x + 5','4x + 2')[i-1],(x0+coords[i-1])/2,286,23,F,opt*f,'center')
    else:
     filter_=phase(t,pick-.13,pick+.76);mx=1114;my=224;cw=20.5
     for i,v in enumerate(PRODUCTS):
      row,col=divmod(i,9);f=pstep(t,jan-.17+row*.034+col*.012,.37)
      if f:
       x0=mx+cw*col;y0=my+cw*row;excluded=v==24
       if excluded:
        box(g,x0-8,y0-8,16,16,O,opt*f,inkcol(O,.67*(1-filter_)),1.6)
        etch(g,'24',x0,y0,12,F,opt*f*(1-filter_),'center')
        if filter_:line(g,(x0-5,y0+5),(x0+5,y0-5),O,1.7,opt*filter_)
       else:rect(g,x0-8,y0-8,16,16,T,opt*f*.59)
     if filter_:
      etch(g,'Σ = 1929',1406,334,28,T,opt*filter_,'right')
      etch(g,'去掉 4 个 24',1406,373,21,M,opt*filter_,'right')
 if sec:
  # Change scale here, and start with an unrelated sample. These are independent policies,
  # not a claim that the public AtCoder case belongs in a private benchmark.
  op=sec;x,y=390,442;close=phase(t,secret-.04,secret+1.17);reopen=phase(t,hold-.23,hold+.88);rr=phase(t,audit-.31,audit+.49)
  g.c.save();zoom=1.53-.53*rr;g.c.translate(mix(780,x,rr),mix(414,y,rr));g.c.scale(zoom,zoom);g.c.translate(-x,-y)
  seal(g,x,y,131,1-close+.94*reopen,op*(1-.65*rr))
  etch(g,'私有题库',x,633,33,C,op*(1-.48*rr),'center')
  if close>.91 and reopen<.99:
   etch(g,'封存',x,yy-80,25,'#FFFFFF',op*close*(1-reopen),'center')
  if reopen:
   q=pstep(t,hold-.08,.83);px,py=transit((x+13,y),(678,364),q,-39)
   if q<.99:dot(g,px,py,9,T,op*q)
   path(g,[(x+134,y),(566,y),(640,369)],q,T,2.2,op)
   etch(g,'最终校验',657,365,30,T,op*q)
  g.c.restore()
  # One damaged item, actually repaired: 'round 2.5' admits two distinct readings.
  if rr:
   x2=1101;cy=434;w=phase(t,audit+.20,a('清洗残次题')+.51);fix=phase(t,a('打磨出')-.18,refine+.59)
   etch(g,'复核示例',x2-208,283,23,M,op*rr)
   etch(g,'2.5',x2-114,cy,62,F,op*rr,'center')
   for j,val in enumerate(('2','3')):
    sy=(356,527)[j];bz=op*rr*(1-.86*fix if j else 1)
    path(g,[(x2-48,cy),(x2+26,cy),(x2+99,sy),(x2+160,sy)],w,T if j==0 else O,2.8,bz)
    etch(g,val,x2+183,sy,42,T if j==0 else O,bz*w)
   etch(g,'取整',x2-118,cy+81,31,O,op*rr*(1-fix),'center')
   if fix:
    etch(g,'向下取整',x2-117,cy+81,34,T,op*fix,'center');swish(g,x2-187,x2-46,cy+108,t-refine+.12,T,.60)
    check(g,x2+252,356,13,True,op*fix)
