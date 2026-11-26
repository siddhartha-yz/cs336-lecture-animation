"""Intact experimental controls, a 57-spoke field, and letters that keep their identities."""
from rig4 import *
def cuboid(g,x,y,w,h,co,a):
 if a<=0:return
 p=[(x-w/2,y-h/2),(x+w/2,y-h/2),(x+w/2,y+h/2),(x-w/2,y+h/2)]
 dx,dy=26,-23
 for points,ft in ((p,.27),([p[0],p[1],(p[1][0]+dx,p[1][1]+dy),(p[0][0]+dx,p[0][1]+dy)],.45),([p[1],p[2],(p[2][0]+dx,p[2][1]+dy),(p[1][0]+dx,p[1][1]+dy)],.16)):
  g.poly(points,co,2.3,a,True,inkcol(co,ft),a)
def two_benches(g,c,start,stop):
 t=c.t;change=c.at('可到了基础模型')-.22;d=enter(t,start,.58);blend_=phase(t,change-.04,change+.60);method_off=easepos(t,change-.51,.53)
 if method_off<1:
  wide=d*(1-blend_);land=c.at('优化器');rise=easepos(t,land-.94,1.42)
  al=wide*(1-phase(rise,.12,.70));train=enter(t,c.at('同一份公开训练集')-.33,.61);test=enter(t,c.at('隔离测试集')-.27,.69)
  mark(g,'ImageNet · SQuAD',800,118,52,t-start,C,mode='pen',dur=.55,op=al)
  label(g,'同一训练集',340,234,32,T,train*al);label(g,'同一留出测试集',1243,234,32,O,test*al)
  for j,yy in enumerate((392,586)):
   co=(C,V)[j];label(g,('方法 A','方法 B')[j],128,yy,33,co,al,'left')
   for i in range(7):
    u=enter(t,c.at('同一份公开训练集')-.23+.045*i,.43);x=270+24*i;rect(g,x,yy-15,18,30,T,u*al)
   path(g,[(447,yy),(608,yy)],train,T,2.2,al)
   x=765;rr=39;vv=enter(t,start+.24+.12*j,.58);p=[]
   for k in range(5):
    a=-pi/2+k*tau/5;p.append((x+rr*cos(a),yy+rr*sin(a)))
   g.poly(p,co,2.2,al*vv,True,inkcol(co,.36),al*vv)
   path(g,[(884,yy),(1143,yy)],test,O,2.0,al)
   for i in range(6):rect(g,1155+i*26,yy-15,18,30,O,test*al)
   if train:
    lo=c.at('同一份公开训练集');hi=c.at('只改一个环节');p0=clip((t-lo)/max(1,hi-lo));f=(p0*1.999)%1
    if 0<p0<1:point(g,mix(448,607,f),yy,5.1,T,al)
   if test:
    var=enter(t,c.at('训练预算')-.20+.16*j,.48);x0=530;dy=yy+42
    if var:
     line(g,(x0,dy),(x0+105*var,dy),Y,2.35,al*var);point(g,x0+105*var,dy,4.6,Y,al*var)
  if rise:
   from optimizer6 import bowl
   ctx=g.c;ctx.save();ctx.translate(-95*method_off,-24*method_off)
   bowl(g,c,wide*phase(rise,.34,.96)*(1-method_off),rise)
   ctx.restore()
 if blend_:
  off=1-phase(t,stop-.62,stop-.09);gain=blend_*off;gg=enter(t,change,.56);fixed=c.at('几乎全在黑盒');att=c.at('更精妙的注意力');dat=c.at('相关领域');buy=c.at('买产品的团队')
  for j,(x,co)in enumerate(((447,C),(984,V))):
   y=400+2.2*sin(t*1.08+j*.85);cuboid(g,x,y,195,144,co,gain)
   label(g,('系统 A','系统 B')[j],x,y,37,F,gain)
   line(g,(x-82,553),(x+103,553),E,2.0,gain);ww=135+28*j;rect(g,x-82,536,ww,17,co,gain*.86)
  label(g,'同一个测试集',707,647,32,T,gain);label(g,'Δ = +2',1275,520,41,Y,gain)
  for i,(tag,time,co,ay)in enumerate((('注意力机制',att,C,213),('训练语料',dat,O,279))):
   u=enter(t,time-.22,.59)
   if u:
    path(g,[(1118,402),(1200,402),(1240,ay),(1280,ay)],u,co,2.1,gain)
    label(g,tag+'？',1303,ay,27,co,gain*u,'left')
  if t>=buy-.16:
   u=enter(t,buy-.16,.58);swish(g,881,1081,469,t-buy+.15,V,.7,3.0)
   label(g,'比较成品',715,733,33,V,gain*u)
def score_to_token(g,t,seam):
 # Preserve one chip of material as the two experiment benches dissolve. No letters
 # or boxes change aspect. It lands at the FIRST FineWeb chip of the actual next layout.
 if not seam-.62<t<seam+.74:return
 q=p5((t-(seam-.54))/1.10);x,y=transit((983.5,544.5),(178.,264.),q,76)
 ww=mix(163,18,q);hh=mix(17,18,q);co=blend(V,C,q)
 a=enter(t,seam-.62,.19)*(1-phase(t,seam+.36,seam+.74))
 if .055<q<.97:
  pts=[transit((983.5,544.5),(178.,264.),max(0.,q-j*.022),76) for j in range(6,-1,-1)]
  path(g,pts,1,co,1.65,a*.50)
 rect(g,x-ww*.5,y-hh*.5,ww,hh,co,a*.87)
def exam57(g,c,wheel):
 t=c.t;q=enter(t,wheel,.54);xx,yy=767,422;R0=229;early=c.at('世界史');alg=c.at('抽象代数');score=c.at('前沿模型的得分');collapse=phase(t,score-.35,score+.78);az=1-collapse
 if az:
  for i in range(57):
   # Each mark is one subject, not a subject score.
   z=enter(t,wheel+.012*i,.64);an=-pi/2+i*tau/57;co=(C,T,V,O)[i%4];r=R0+7.2*sin(i*2.31)
   seed=(931 if i%2==0 else 1281,422);aa,bb=cos(an),sin(an)
   px,py=transit(seed,(xx+r*aa,yy+r*bb),p5(z),-37+5*(i%8))
   line(g,(px,py),(px+42*aa*z,py+42*bb*z),co,3.0+2.9*z,az*z)
   if i%5==0:dot(g,px+2*aa,py+2*bb,4.,co,az*z)
  mark(g,'MMLU',xx,391,69,t-wheel-.17,F,mode='pen',dur=.59,op=az)
  label(g,'57 学科 · 四选一',xx,470,33,T,enter(t,wheel+.72,.47)*az)
  for q0,i,text,direction in ((early,41,'世界史',-1),(alg,12,'抽象代数',1)):
   k=enter(t,q0-.15,.55);an=-pi/2+i*tau/57;px,py=xx+(R0+47)*cos(an),yy+(R0+47)*sin(an);ex=px+90*direction
   if k:
    side='left' if direction==1 else 'right';tx=ex+40*direction
    path(g,[(px,py),(ex,py),(ex+29*direction,py-34)],k,Y,2,az)
    label(g,text,tx,py-36,34,Y,k*az,side)
    label(g,'恩克鲁玛 · 非殖民化' if direction<0 else 'ℤ₃[x] / (x² + c)',tx,py+21,31,F,k*az,side)
 if collapse:
  g0=collapse;cap=203;floor=684;vals=(84.7,88.7,90.2);co=(C,T,V);left=423;top=c.at('盯住旧试卷')
  line(g,(233,cap),(1364,cap),M,2,g0);label(g,'100%',1364,157,33,M,g0,'right')
  for j,(nm,n)in enumerate(zip(('GPT-4','GPT-4o','GPT-4.1'),vals)):
   x=left+j*366;h=(floor-cap)*n/100;v=enter(t,score-.20+j*.13,.64);y=floor-h*v
   rect(g,x-60,y,120,h*v,inkcol(co[j],.81),g0*v);label(g,nm,x,floor+51,32,co[j],g0*v)
   mark(g,f'{n:.1f}%',x,y+35,38,t-(score-.15+j*.13),'#181818',mode='wave',dur=.43,op=g0)
   e=enter(t,top+.40*j,.44)
   if e:line(g,(x+79,y),(x+79,cap),O,2.2,g0*e)
  seen=c.at('基准饱和')
  if t>=seen-1.8:mark(g,'基准饱和',800,110,42,t-seen+1.8,Y,mode='wave',dur=.49)
def options(g,c,end):
 t=c.t; judge=c.at('第二刀');split=c.at('十个');drop=c.at('第三刀');one=c.at('要求只选一个')
 if t<judge-.10:
  gone=1-phase(t,judge-.64,judge-.13)
  mark(g,'MMLU-Pro',215,140,53,t-.09,C,'left','pen',.6,gone)
  u=enter(t,c.at('表述不清')-.22,.53);v=enter(t,c.at('标错答案')-.22,.5)
  for j,(x,h,l,col,z)in enumerate(((419,'从 2、4 中挑一个离 3 最近的数','2　←　3　→　4',T,u),(1152,'2² 的值','标答：3',O,v))):
   if z:
    label(g,h,x,288,35,F,z*gone);label(g,l,x,432,48,col,z*gone);cut=enter(t,c.at('清理出局')+.14*j,.49)
    if cut:path(g,[(x-147,550),(x+136,487)],cut,R,3.3,gone)
  if t>one-.07:label(g,'两种答案都成立',418,663,31,T,gone*enter(t,one-.07,.52))
 elif t<drop-.08:
  al=1.0;four=enter(t,judge-.08,.53);early=c.at('这四个选项')
  s=phase(t,c.at('位置拉开')-.14,c.at('补上新的')+.54);a=enter(t,split-.18,.60)
  for j in range(10):
   u=enter(t,judge-.04+j*.065,.44) if j<4 else enter(t,c.at('补上新的')-.12+(j-4)*.052,.47)
   if not u:continue
   x=mix(490+204*j,475+158*(j%5),s) if j<4 else 475+158*(j%5);y=382 if j<5 else 512
   co=C if j<4 else O;w=mix(122,99,s);box(g,x-w/2,y-48,w,96,co,u*al,inkcol(co,.38),1.9)
   label(g,chr(65+j),x,y,46,F,u*al)
  show=enter(t,c.at('百分之二十五')-.17,.45);less=enter(t,c.at('百分之十')-.17,.49)
  label(g,'均匀盲猜',349,675,31,T,four*al)
  if show:mark(g,'1/4 = 25%',690,675,43,t-c.at('百分之二十五')+.17,F,mode='pen',op=al)
  if less:mark(g,'→  1/10 = 10%',1135,675,43,t-c.at('百分之十')+.17,Y,mode='pen',op=al)
 elif t<end:
  o=(1-phase(t,end-.55,end-.05));a=enter(t,drop-.07,.52);n=c.at('需要走好几步');single=c.at('只交一个字母');r=c.at('先把推理做完')
  # Carry the chosen B into its new seat while the other cells peel away.
  transit_=phase(t,drop-.10,drop+.69)
  for jj in range(10):
   xx=475+158*(jj%5);yy=382 if jj<5 else 512
   if jj==1:
    xx,yy=transit((xx,yy),(1279,426),transit_,-62)
    box(g,xx-48,yy-48,96,96,Y,o,inkcol(Y,.29),2);label(g,'B',xx,yy,46,F,o)
   elif transit_<1:
    z=1-transit_;col=C if jj<4 else O;box(g,xx-48,yy-48,96,96,col,z,inkcol(col,.32),1.8);label(g,chr(65+jj),xx,yy,46,F,z)
  for j in range(3):
   x=331+j*302;u=enter(t,min(n-.15,drop+.46)+j*.18,.51);point(g,x,428,11,T,a*u*o)
   if j<2:path(g,[(x,428),(x+262,428)],u,T,2.2,o*u)
  tag=enter(t,single-.15,.57);swish(g,1245,1311,490,t-single+.12,Y,.65,2.8)
  if t>r-.14:
   z=phase(t,r-.14,r+1.15);x=331+948*z;ring(g,x,428,21,C,o,2.5);label(g,'分步推理 → 交选项',803,599,34,T,o*enter(t,r-.14,.53))
def two_stories(g,c,start,end):
 # Each dash stands for one actual word, translated openings locate the two texts.
 from studio_preference import material,weft
 t=c.t;o=1-phase(t,end-.53,end-.05)
 for j,(x,co,title,quote,at)in enumerate(((187,C,'A','734 号擦亮黄铜路灯。',c.at('接近八百词')),(891,V,'B','维修机器人驶过空商场。',c.at('两百多词')))):
  y=265;u=enter(t,start+.12*j,.52);mark(g,quote,x,y,41,t-start-.12*j,F,'left','wave',.46,o)
  line(g,(x,y+43),(x+473,y+43),co,1.9,o*u);mark(g,title,x,y-91,37,t-start-.08*j,co,'left',op=o)
  cells,rows=weft(j);k=enter(t,start+.14+.13*j,.85)
  for n,(px,row,wd) in enumerate(cells):
   v=clip(k*1.26-(n/len(cells))*.24);rect(g,x+px*.91,y+98+row*10.,wd*.91,5.4,co,o*v*(.65+.22*(n%4)/3))
  if t>=at-.11:
   mark(g,f'{len(material()[j])} 词',x,665,42,t-at+.11,co,'left','pen',.57,o)
def cases(g,c,start,end):
 t=c.t;off=1-phase(t,end-.48,end-.06);u=enter(t,start,.47);st=c.at('十二个大型');n=c.at('两千两百九十四');v=c.at('人工核验');num=c.at('五百题');verified=min(c.at('Verified'),end-2.38)
 mark(g,'SWE-bench',167,131,52,t-start,C,'left','pen',.58,off)
 label(g,'从真实仓库取题，跑测试验收',168,204,30,M,u*off,'left')
 mark(g,'sphinx-doc/sphinx',168,351,35,t-start-.19,F,'left',op=off)
 mark(g,'Issue #5560',169,432,38,t-c.at('问题描述')+.12,O,'left',op=off)
 if t>=c.at('就得到')-.15:
  label(g,'＋',363,506,32,M,off);mark(g,'PR #8713',169,571,38,t-c.at('就得到')+.15,T,'left',op=off)
 repos=('astropy','django','flask','matplotlib','pylint','pytest','requests','scikit-learn','seaborn','sphinx','sympy','xarray')
 for j,name in enumerate(repos):
  x=733+j%3*236;y=265+j//3*75;z=enter(t,st-.16+j*.047,.49)
  if z:dot(g,x,y,5,T,z*off);label(g,name,x+16,y,25,F,z*off,'left')
 if t>=n-.16:
  mark(g,'2,294 道题',1020,620,52,t-n+.16,Y,mode='pen',dur=.57,op=off)
 # This annotation enters on the number, with Verified including enough reading time.
 if t>=min(num,verified)-.16:mark(g,'Verified  ·  500 题',1019,718,38,t-min(num,verified)+.16,T,mode='pen',dur=.53,op=off)
