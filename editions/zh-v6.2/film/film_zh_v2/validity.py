from termnotes import hint
from ink import *
from motion import guide,transit,reletter
from itertools import permutations
def jig_sheet(g,xx,yy,scale,op,ink):
 # One concept-drawing sheet at two sizes. Orthographic views use the same hub,
 # feet and centreline as the physical cable reel in the middle of the board.
 if op<.002:return
 z=g.c;z.save();z.translate(xx,yy);z.scale(scale,scale)
 docs(g,-145,-100,290,200,O,op,0)
 def stroke(points,start,length,col=O,sw=1.7):
  path(g,points,phase(ink,start,start+length),col,sw,op)
 def wheel(x,y,r,st,dur):
  q=phase(ink,st,st+dur)
  if q:arc(g,x,y,r,-pi*.5,-pi*.5+tau*q,O,2.2,op)
 # Front elevation. The two inclined struts support the shaft, not the rim.
 wheel(-65,-5,42,.00,.37);wheel(-65,-5,9,.10,.22)
 stroke([(-120,64),(-65,-5),(-12,64),(-120,64)],.23,.32,sw=2.2)
 stroke([(-119,71),(-10,71)],.34,.23)
 stroke([(-122,-5),(-8,-5)],.10,.33,M,1)
 stroke([(-65,-60),(-65,44)],.12,.36,M,1)
 # Side elevation: flanges, drum, shaft and plinth. Fine witness marks give
 # the page the syntax of a drawing without inventing an engineering dimension.
 stroke([(25,38),(25,-45),(33,-45),(33,38),(25,38)],.42,.35,sw=2.1)
 stroke([(91,38),(91,-45),(99,-45),(99,38),(91,38)],.48,.33,sw=2.1)
 for i,dy in enumerate((-26,21)):stroke([(33,dy),(91,dy)],.51+.05*i,.21)
 stroke([(13,-4),(111,-4)],.55,.22,M,1.45)
 stroke([(21,58),(31,16),(37,58),(87,58),(94,16),(101,58)],.61,.26)
 stroke([(11,65),(112,65)],.67,.18)
 for x in (26,98):stroke([(x,-53),(x,-68)],.78,.16,M,1.1)
 stroke([(26,-62),(98,-62)],.80,.18,M,1.1)
 for x,sg in [(26,1),(98,-1)]:stroke([(x+5*sg,-65),(x,-62),(x+5*sg,-59)],.88,.10,M,1)
 z.restore()

def realwork(g,c):
 t=c.t;circle=c.at('圈对一个字母');draw=c.at('交上一张');paper=c.at('一堆材料');match=c.at('越对得上');name=c.at('生态效度')
 example=c.at('真实行业交付');gdp=on(c,'GDPval',.75,.25);med=on(c,'斯坦福',.53,.42);close=on(c,'尺子和真实工作',2)
 swap=phase(t,name-.48,name+.39);aa,bb=reletter(swap)
 title(g,'两份答卷',111,aa);title(g,'生态效度',111,bb,sub=hint('生态效度'))
 sheet=1-phase(t,c.at('斯坦福')-.68,c.at('斯坦福')-.18)
 # The exam paper is the actual landing place of the preceding scene's page.
 docs(g,163,337,215,167,C,1,0,2)
 for j,n in enumerate((111,148,91)):
  line(g,(183,365+j*15),(183+n,365+j*15),C,2,.7)
 for j,char in enumerate('ABCD'):
  x=194+j*47;txt(g,char,x,456,26,Y if j==2 and t>=circle+.65 else M,1)
 trace=phase(t,circle-.12,circle+.80)
 if trace:
  pts=[(288+20*cos(-.7*pi+j*tau*1.04/45),456+22*sin(-.7*pi+j*tau*1.04/45)) for j in range(46)]
  path(g,pts,trace,Y,2.3)
 txt(g,'选择题',270,558,28,C)
 # The large right-hand deliverable is carried into the sequence, rather
 # than replaced with another PDF icon when GDPval is named.
 branch=phase(t,paper-.88,paper+.60);payload=phase(t,draw-.20,draw+.45)*sheet
 x,y=transit((1085,412),(1206,403),branch,19)
 if payload:
  z=mix(1.45,.680,branch);jig_sheet(g,x,y,z,payload,phase(t,draw-.25,draw+2.05))
  # Pin the caption to the moving lower edge. Its outlines and clearance never change at a size boundary.
  txt(g,'设计图',x,y+100*z+40,27,O,payload)
 middle=phase(t,draw-.09,draw+.52)*(1-branch)
 if middle:line(g,(691,308),(691,525),E,1.2,middle*.70)
 if sheet:
  collected=phase(t,paper-.64,paper+.40)
  for j in range(3):
   q=phase(t,paper-.74+.25*j,paper-.05+.25*j);px=557+(2-j)*9;py=357-(2-j)*8
   if q:docs(g,px,py+18*(1-q),98,88,T,q*sheet,4,j)
  lab_out,lab_in=reletter(phase(t,example-.1,c.at('卷筒参数')+.24))
  txt(g,'工作材料',611,511,25,T,collected*sheet*lab_out)
  txt(g,'卷筒参数',611,511,25,T,collected*sheet*lab_in)
  # The drawing points to the deliverable; the model on the axle is the work.
  build=phase(t,match-.16,match+1.23);process=sheet*build
  if process:
   for j in range(2):
    xx=876+j*33;yy=402-j*14
    ring(g,xx,yy,48,V,process,2.8);ring(g,xx,yy,13,V,process,2)
    for k in range(5):
     ang=k*tau/5+(t-match)*.21;line(g,(xx+14*cos(ang),yy+14*sin(ang)),(xx+44*cos(ang),yy+44*sin(ang)),V,1.6,process)
   for delta in [-1,1]:line(g,(876,402+delta*48),(909,388+delta*48),V,2.2,process)
   path(g,[(836,464),(878,412),(922,464),(836,464)],build,O,2.1,sheet)
   txt(g,'夹具建模',899,511,25,V,process)
  for n,(l,r) in enumerate(((688,800),(968,1088))):
   flow=phase(t,match+.40+.37*n,match+1.12+.37*n)
   arrow(g,(l,405),(r,405),flow,M,sheet*.85,1.5)
  # Underline the actual deliverable as soon as the specific example names it.
  detailed=phase(t,c.at('夹具')-.15,c.at('设计图')+.25)
  if 0<detailed<1:guide(g,[(1106,538),(1306,538)],detailed,O,sheet,2.15,.32)
 if med:
  a=med
  note=c.at('起草病历');decision=c.at('辅助临床决策');tasks=c.at('临床工作任务')
  for j,lab in enumerate(('就诊记录','起草病历','辅助决策')):
   xx=(610,898,1206)[j];col=(T,V,O)[j];appear=phase(t,((c.at('斯坦福')+.06,note-.38,decision-.24)[j]),((tasks,note+.60,decision+.66)[j]))
   visible=a*appear
   if j==0:
    for k in range(12):
     h=10+29*abs(sin(.8*k+.51));f=phase(t,c.at('斯坦福')+.09+.12*k,tasks-.60+.12*k)
     line(g,(xx-51+k*9,403-h*.5*f),(xx-51+k*9,403+h*.5*f),col,3,visible)
   elif j==1:
    docs(g,xx-44,354,88,94,col,visible,0,1)
    for k in range(5):
     f=phase(t,note-.07+.14*k,note+.48+.14*k);x=xx-30;yy=375+k*11
     line(g,(x,yy),(x+(55-7*(k%3))*f,yy),col,1.9,visible)
   else:
    for k in (-1,1):
     xx0=xx+22
     f=phase(t,decision-.14+(.22 if k==1 else 0),decision+.70+(.22 if k==1 else 0))
     line(g,(xx-41,400),lerp((xx-41,400),(xx0,400+37*k),f),col,2.1,visible);ring(g,xx+32,400+37*k,9,col,visible*f,2)
    dot(g,xx-41,400,6.3,col,visible)
   txt(g,lab,xx,501,24,col,visible)
  trunk=[(678,399),(708,399),(708,311),(1205,311),(1205,335)]
  branch=phase(t,tasks-.26,note+.4);path(g,trunk,branch,M,1.3,a*.69)
  arrow(g,(708,399),(826,399),phase(t,note-.53,note+.24),M,a*.76,1.5)
  for j,(ta,points,cl) in enumerate(((note,[(676,399),(826,399)],V),(decision,trunk,O))):
   k=phase(t,ta-.49,ta+.58)
   if 0<k<1:guide(g,points,k,cl,a,2.5,.36)
 if branch:line(g,(462,315),(462,510),E,1.3,branch*.71)
 left=gdp*(1-phase(t,c.at('斯坦福')-.57,c.at('斯坦福')-.21))
 if left:txt(g,'GDPval',898,607,34,C,left);txt(g,hint('GDPval'),898,659,25,M,left)
 if med:txt(g,'MedHELM',900,607,35,V,med);txt(g,hint('MedHELM'),900,659,25,M,med)
 if close:line(g,(532,548),(1292,548),Y,2,close)
 if left:source(g,'GDPval · 44 个职业，9 个行业',left)
 if med:source(g,'Stanford MedHELM · 121 项临床任务的分类',med)
QNAME=['青蛙与沸水','能量与质量','零分电影','捷豹 S-Type'];QC=(C,V,O,T)
PERMS=list(permutations(range(4)))
def ll(ids):return math.log(.7 if ids[0]==0 else .1)+sum(math.log(.7 if b==(a+1)%4 else .1) for a,b in zip(ids,ids[1:]))
def shuffle(g,c):
 t=c.t;release=on(c,'原始顺序',1.45);sh=on(c,'随机打乱',2.8);dist=on(c,'乱序版本的得分排开',3.2);pnt=on(c,'那个点落进去',2.6);qual=on(c,'按难度排序',1.7)
 role=phase(t,c.at('可交换性假设')-.24,c.at('可交换性假设')+.36)
 left,right=reletter(role);title(g,'原来的题序，有多特别？',101,left)
 if right:title(g,'可交换性检验',101,right,sub=hint('可交换性检验'))
 # For a black box the training set is out of reach; an ordered sequence can still be scored.
 pre=1-phase(t,c.at('可交换性假设')-.6,c.at('可交换性假设')+2)
 if pre>.003:
  lx,rx=369,1111;seen=on(c,'背过原题',2)
  hide=phase(t,c.at('如果训练集')-.18,c.at('不公开')+.61)
  # What closes here is access to the corpus, not the scoring endpoint.
  # Three neutral file edges disappear behind an opaque face; the public items remain.
  for j in range(3):
   x=rx-163+6*j+hide*(82+5*j);yy=357+17*j
   line(g,(x,yy),(rx-67,yy-13),M,1.45,pre*phase(t,5.15+.19*j,6.10+.19*j)*(1-hide))
  for i in range(4):
   x=lx+(i%2)*128;y=310+(i//2)*108;z=phase(t,.8+i*.75,2.1+i*.75)
   docs(g,x-40,y,82,68,QC[i],pre*z,3,i)
   dot(g,x+26,y+53,5,QC[i],pre*z)
  txt(g,'公开测试题',431,605,29,C,pre)
  g.poly([(rx-118,312),(rx+72,286),(rx+131,336),(rx-64,361),(rx-118,312)],M,1.8,pre,True,inkcol(M,.07),1)
  g.poly([(rx-118,312),(rx-64,361),(rx-64,505),(rx-118,449),(rx-118,312)],E,1.6,pre,True,inkcol(M,.04),1)
  g.poly([(rx-64,361),(rx+131,336),(rx+131,474),(rx-64,505),(rx-64,361)],M,1.8,pre,True,inkcol(M,.07),1)
  txt(g,'?',rx+31,420,49,Y,pre)
  txt(g,'训练语料',rx+4,605,29,M,pre)
  for j in range(8):
   z=phase(seen,j*.055,.53+j*.055);x=592+39*j
   line(g,(x,410),(x+24*(1-hide),410),R,2.1,pre*z*(1-hide))
  query=c.at('还能找到');order=c.at('题序');route=phase(t,query+.02,order+.49)
  # Reading order wraps around the papers rather than crossing their ink.
  routes=[[(410,342),(456,342)],[(539,342),(559,342),(559,397),(317,397),(317,452),(330,452)],[(410,452),(456,452)]]
  for j,pp in enumerate(routes):
   step=phase(route,.15+j*.26,.37+j*.26)
   path(g,pp,step,M,1.6,pre*.81)
   if 0<step<1:guide(g,pp,step,Y,pre,2.8,.34)
  for j in range(4):
   step=phase(route,.03+j*.26,.18+j*.26);xx=lx+(j%2)*128;yy=310+(j//2)*108
   txt(g,str(j+1),xx-22,yy+48,22,F,pre*step)
 display=1-pre
 # Score distinct orders under a four-symbol toy distribution. A colored dot keeps
 # its question identity and a score enters the distribution only after that order settles.
 start=c.at('随机打乱');key=c.at('关键前提');free=c.at('顺序可以交换');initial=c.at('原始顺序的对数概率');system=c.at('不该系统性地');plot=c.at('乱序版本的得分排开');push=c.at('那个点落进去')
 orig=(0,1,2,3);stops=[(start-.18,(0,1,3,2)),(key+.70,(1,2,3,0)),(free-.25,(2,0,3,1)),(system-.18,(0,2,3,1))]
 before=orig;after=orig;u=0.;at=0.
 for tm,perm in stops:
  if t<tm:break
  before,after=after,perm;u=phase(t,tm,tm+1.19);at=tm
 settled=after if u>=.998 else before
 # Vacate the future chart lane first. Its title and dots arrive only after the last paper clears it.
 lay=phase(t,c.at('先看右边')-.32,plot+.08)
 left=mix(460,289,lay);right=mix(1108,660,lay);arrow0=(left+right)/2
 yy0=mix(252,307,lay);step=57.
 for side,xx in enumerate((left,right)):
  current=settled if side else orig
  txt(g,('原始顺序','置换顺序')[side],xx,mix(201,237,lay),29,(C,V)[side],display)
  introduce=c.at('取一组');join=c.at('拼成一段长文本')
  for j in range(4):
   f=u if side else 1.;frompos=before.index(j) if side else j;topos=after.index(j) if side else j
   yy=yy0+step*mix(frompos,topos,f)
   dx=(1 if j%2 else -1)*(65+12*j)*sin(pi*f) if frompos!=topos else 0
   ins=phase(t,introduce-.20+j*.24,introduce+.54+j*.24)
   arrival=phase(t,join-.11+j*.14,join+.74+j*.14)
   a=display*(ins if side==0 else arrival)
   if side and u==0:dx+=(-145)*(1-arrival)
   bx=xx-mix(151,115,lay)+dx
   dot(g,bx,yy,6.0,QC[j],a)
   textvis=1-.98*(sin(pi*f)**.68) if frompos!=topos else 1
   txt(g,QNAME[j],bx+23,yy,25,F,a*textvis,'left',mix(238,173,lay))
   k=current.index(j);prob=.7 if (j==0 if k==0 else j==(current[k-1]+1)%4) else .1
   bar=xx+mix(90,77,lay)+dx
   if side==0 and qual:
    # The alternative explanation is a hypothetical ordering rule, not measured difficulties of these subjects.
    col=O;wide=12+15*j
   else:col=T if prob>.2 else R;wide=59*prob/.7
   line(g,(bar,yy),(bar+wide,yy),col,3.2,a*textvis)
  if side==0 and t<start+.1:
   connect=phase(t,c.at('原始顺序')-.28,join+.63)
   if connect:
    path(g,[(xx-177,yy0),(xx-183,yy0),(xx-183,yy0+3*step),(xx-177,yy0+3*step)],connect,C,1.8,display)
  if t>=start-.2:
   read=(1-.78*sin(pi*u) if side else 1)*display
   val=ll(current);txt(g,f'log P = {val:.2f}',xx,mix(539,599,lay),26,(C,V)[side],read)
  if display:
   xdiv=mix(800,471,lay);line(g,(xdiv,mix(224,279,lay)),(xdiv,mix(471,519,lay)),E,1.2,display*.75)
 if dist:
  vals=[ll(p) for p in PERMS];lo,hi=min(vals),max(vals);L,H=888,1453;base=512
  xxof=lambda v:L+28+(H-L-63)*(v-lo)/(hi-lo)
  line(g,(L,base),(H,base),M,1.6,dist)
  txt(g,'置换分数的分布',1171,237,29,F,dist)
  counts={};shown=[p for tm,p in stops]
  order=shown+[p for p in PERMS if p!=orig and p not in shown]+[orig]
  for j,p in enumerate(order):
   v=ll(p);kk=round(v,7);ix=counts.get(kk,0);counts[kk]=ix+1
   x=xxof(v);y=base-16-ix*16
   if p==orig:
    q=pnt
    if q:
     sx,sy=transit((left,566),(x,y),q,68);dot(g,sx,sy,8,Y,q)
     if qual:ring(g,x,y,14,O,qual,1.75)
   else:
    ft=plot-.21+.15*j
    q=phase(t,ft,ft+.60)
    if q:
     if j<4:
      sx,sy=transit((right+81,577),(x,y),q,47+5*j)
     else:sx=x;sy=mix(base-2,y,q)
     dot(g,sx,sy,5,V,q)
  for xx,lab in ((L,'低'),(H,'高')):txt(g,lab,xx,base+30,21,M,dist)
  txt(g,'序列对数概率',1170,base+52,24,M,dist)
  q0,q1=reletter(qual)
  # Read the right tail of this one finite example, not a claim of a
  # population p-value. Each step counts the actual enumerated permutations.
  tc=c.at('如果它反复');finish=c.at('最右端')+.82;scan=phase(t,tc-.20,finish)
  if scan>0 and q0:
   threshold=mix(lo-.0001,hi-.0001,scan);xx=xxof(threshold);remain=sum(v>=threshold for v in vals)
   strength=phase(t,tc-.22,tc+.23)*q0
   line(g,(xx,base+1),(xx,base-189),Y,1.35,.63*strength)
   rr,ss=reletter(phase(t,finish+.03,finish+.57))
   txt(g,f'线右侧（含线）：{remain} 个排列',1172,655,26,Y,strength*rr)
   txt(g,'原序：24 种排列中排第 1',1172,655,27,Y,strength*ss)
  if qual:
   txt(g,'假如出题本来就从易到难',465,665,23,O,qual)
   txt(g,'原序特别，也可能是排序造成的',1170,655,25,O,q1)
 source(g,'讲义图 208 的题序 · 四符号示例的全部 24 种排列',dist)

WORDS='黄昏 时 一 艘 蓝色 渔船 沿着 海岸 缓缓 驶向 港口 船上 的 人 看见 远处 第一 座 灯塔 亮起 了 灯'.split()
# Fixed toy stream: each public word has a stable ordinal. Verify the outgoing and incoming
# symbols against the same polynomial used to build the lookup, as in a rolling n-gram index.
WORDID={s:i+1 for i,s in enumerate(dict.fromkeys(WORDS))}
WIDTH=13; BASE=257; PRIME=2147483647; FIRST=pow(BASE,WIDTH-1,PRIME)
def fingerprints(ws):
 v=0
 for s in ws:v=(v*BASE+WORDID[s])%PRIME
 return v
def roll_values():
 out=[fingerprints(WORDS[:WIDTH])]
 for i in range(len(WORDS)-WIDTH):
  out.append(((out[-1]-WORDID[WORDS[i]]*FIRST)*BASE+WORDID[WORDS[i+WIDTH]])%PRIME)
 return tuple(out)
STREAM=roll_values()
def bloom_probe(v):return {(v%34+j*(1+2*((v//37)%16)))%34 for j in range(3)}
def ngrams(g,c):
 from motion import guide
 t=c.t;take=c.at('连续十三个词');collection=c.at('评测集');idx=c.at('哈希集合');bf=c.at('布隆过滤器')
 first=c.at('一路扫过去');hit=c.at('核对原片段');count=c.at('重合比')
 train=phase(t,.36,1.24)
 intro=1-phase(t,take-.65,take-.25)
 if intro:title(g,'哪一段训练文字见过考题？',103,intro)
 term=phase(t,take-.22,take+.37)*(1-phase(t,bf-.66,bf-.20))
 if term:title(g,'13-gram',103,term,sub=hint('13-gram'))
 tree=phase(t,bf-.12,bf+.46)
 if tree:title(g,'布隆过滤器',103,tree,sub=hint('布隆过滤器'))
 gram=phase(t,take-.12,take+.93);index=phase(t,idx-.26,idx+.72)
 # An exactly thirteen-word aperture, with twelve words shared by adjacent positions.
 # The camera does part of the tracking so the advancing pair stays inside a readable margin.
 last=len(WORDS)-WIDTH
 begin=c.at('用一个长度为十三')-.42; found=c.at('报了命中')+.10
 if t<begin+1.15:travel=max(0.,min(1.,(t-begin)/1.15))
 else:travel=1+(last-1)*max(0.,min(1.,(t-begin-1.15)/max(.1,found-begin-1.15)))
 step=min(last,int(travel));fr=travel-step
 advance=step+phase(fr,.06,.86)
 dx=78; origin=200; lift=331
 xof=lambda j:origin+(j-.83*advance)*dx
 def onstrip(p):
  return phase(p,79,125)*(1-phase(p,1460,1511))
 for j,s in enumerate(WORDS):
  xx=xof(j);visible=onstrip(xx)*train
  if visible<=.002:continue
  inside=step<=j<step+WIDTH
  if step<last:
   incoming=j==step+WIDTH;outgoing=j==step
  else:incoming=outgoing=False
  a=gram if inside else 0.
  if incoming:a=gram*phase(fr,.35,.89)
  if outgoing:a=gram*(1-phase(fr,.15,.75))
  txt(g,s,xx,lift,29,blend(M,Y,a),visible*(.40+.60*max(a,1-gram)))
  line(g,(xx-23,lift+32),(xx+23,lift+32),E,1.1,visible*(.45+.55*a))
  if incoming or outgoing:
   force=sin(pi*fr)*gram
   line(g,(xx-19,lift+33),(xx+19,lift+33),T if incoming else R,2.8,force*visible)
 edge=xof(advance)-32; span=(WIDTH-1)*dx+64
 if gram:
  # The moving pin at each end encodes which word leaves and which one joins the new window.
  g.poly([(edge,lift+20),(edge,lift-42),(edge+span,lift-42),(edge+span,lift+20)],Y,2.35,gram)
  txt(g,'13 个词',edge+span/2,lift-76,26,Y,gram)
 if 0<travel<last:
  force=sin(pi*fr)
  for j,col in ((step,R),(step+WIDTH,T)):
   xx=xof(j);y=lift+57+18*force
   dot(g,xx,y,3.5,col,force*onstrip(xx))
 vv=STREAM[step];rv=STREAM[-1];want=phase(t,collection-.12,collection+.54)
 # Before there is an index, show how the examiner obtains a reference strip.
 # A line is lifted from the training page; a separate stack contributes the test fragments.
 before=1-phase(t,idx-.83,idx-.22)
 if before:
  doc=phase(t,.18,1.34)*before
  docs(g,441,494,136,125,C,doc,5,2,active=2)
  txt(g,'训练文档',509,663,26,C,doc)
  rail=phase(t,take-.75,take+.82)
  if doc*rail:
   g.poly([(511,487),(511,411),(origin,411),(origin,lift+51)],C,1.45,.72*doc*rail)
  born=phase(t,c.at('GSM8K')-.31,c.at('GSM8K')+.46)*before
  if born:
   for i,(n,col) in enumerate([('GSM8K',V),('MMLU',T)]):
    xx=858+196*i;arrival=born*(1 if i==0 else phase(t,c.at('MMLU')-.15,c.at('MMLU')+.48))
    docs(g,xx,488,102,91,col,arrival,4,i);txt(g,n,xx+51,622,25,col,arrival)
   txt(g,'评测题库',998,690,24,M,born)
 if want:
  pick=want*phase(t,idx-.44,idx+.26)
  txt(g,'示例评测片段',1140,482,26,T,pick)
  # A small strip of the indexed original, not a second wall of words.
  txt(g,'驶向 港口 ⋯ 亮起 了 灯',1140,528,27,F,pick)
 if index:
  center=edge+span/2
  g.poly([(center,lift+48),(center,420),(523,420),(523,466)],C,1.3,index*.79)
  txt(g,'窗口指纹',523,489,25,C,index);txt(g,f'0x{vv:08X}',523,538,32,F,index,font='DejaVu Sans Mono')
  txt(g,f'0x{rv:08X}',1140,578,24,T,index,font='DejaVu Sans Mono')
 active=bloom_probe(rv);probes=bloom_probe(vv);positive=probes<=active
 if tree:
  txt(g,'索引位',557,651,23,M,tree,'right')
  for j in range(34):
   xx=588+(j%17)*23;yy=630+(j//17)*25
   box(g,xx,yy,16,15,Y if j in probes else E,tree,fill=(T if j in active else BLACK),sw=2.5 if j in probes else 1.2)
  p=phase(t,hit-.36,hit+.49)
  wordcheck=phase(t,hit+.03,hit+1.)
  if positive:
   txt(g,'可能命中',781,708,25,Y,tree)
   if step==last and wordcheck:
    arrow(g,(993,650),(1039,650),wordcheck,T,.93,2)
    check(g,1081,650,10,True,wordcheck);txt(g,'原文相同',1187,650,27,G,wordcheck)
  else:txt(g,'有一位是零 → 排除',781,708,24,M,tree)
 ratio=phase(t,c.at('最后算出')-.15,c.at('最后算出')+.54)
 if ratio:txt(g,'1 个重合窗口 / 10 个窗口',1205,703,23,Y,ratio)
 source(g,'连续词示例 · 34 位教学用过滤器 · 最终按原文确认',index)
def masks(g,c):
 t=c.t;whole=c.at('整篇文档直接剔除');part=c.at('局部词元');weights=c.at('损失掩码')
 many=c.at('很多代码');license_=c.at('许可证声明');toss=c.at('扔掉它');collateral=c.at('真正有用的代码');white=c.at('白名单');exam=c.at('重合的试题');head=c.at('文件头')
 title(g,'命中的是原题，还是许可证？',112,sub='同一份文档，比较两种处理')
 xs=(322,792,1227);labs=('命中文档','整篇剔除','局部损失掩码');cols=(C,R,T)
 opened=(1.,phase(t,whole-.20,whole+.65),phase(t,part-.18,part+.59))
 cut=phase(t,whole-.03,whole+.80);m=phase(t,weights-.15,weights+.58)
 reject=phase(t,toss-.16,collateral+.98);perm=phase(t,white-.17,white+.63)
 for i,(x,lab,col,a) in enumerate(zip(xs,labs,cols,opened)):
  if a<=0:continue
  txt(g,lab,x,240,32,col if i else F,a)
  docs(g,x-126,300,252,278,col if i else C,a*.72,0)
  if i:
   opening=opened[i];p=phase(opening,.12,.9)
   if 0<p<1:guide(g,[(xs[0]+130,430),(x-129,430)],p,col,a,2.,.17)
  for j in range(9):
   y=336+j*25;kind=O if j<2 else R if j in (4,5) else C
   live=a
   if i==1:live*=1-.44*cut-.48*phase(t,toss-.22+.12*j,collateral+.34+.10*j)
   ll=132+(j*19%47)
   if i==0 and j in (4,5) and getattr(g,'carry_gram',False):continue
   line(g,(x-98,y),(x-98+ll,y),kind,3.75,live)
   if i==2 and m:
    # The words remain in the model input. Only their contribution to the loss changes.
    hit=j in (4,5);qv=phase(t,weights-.10+(j-4)*.16,weights+.63+(j-4)*.16) if hit else m
    xx=x+155
    if hit:
     out_,in_=reletter(qv)
     txt(g,'1',xx,y,21,M,a*m*out_);txt(g,'0',xx,y,23,R,a*m*in_)
     if 0<qv<1:guide(g,[(x-90+ll,y),(xx-12,y)],qv,R,a,2,.26)
    else:txt(g,'1',xx,y,20,M,a*m*.78)
   if i==0 and j==2:
    hi=phase(t,collateral-.20,collateral+.63)
    if 0<hi<1:guide(g,[(x-98,y),(x-98+ll,y)],hi,Y,a,2.6,.4)
  if i==1 and cut:
   path(g,[(x-98,551),(x+98,323)],cut,R,2.4,a)
   if reject:txt(g,'正文也没了',x,628,26,R,reject)
  if i==2 and m:txt(g,'损失权重',x+155,289,21,M,a*m)
 header=phase(t,many-.24,many+.74)
 if header:
  # The same two amber lines recur in independent files: evidence that a header is generic.
  for i in range(3):
   q=phase(t,many+.02+i*.24,license_+.19+i*.07);x=215+55*i;y=632
   if q:
    docs(g,x-16,y-20,33,39,O,q*.74,0)
    for j in range(2):line(g,(x-11,y-11+j*5),(x+9,y-11+j*5),O,1.65,q)
    line(g,(x-11,y+3),(x+3+2*i,y+3),C,1.35,q)
  txt(g,'MIT License',402,631,23,O,phase(t,license_-.18,license_+.52))
 if perm:
  # Link the exception to the header only; the known test fragment is still excluded.
  ll=phase(t,head-.26,head+.67);e=phase(t,exam-.23,exam+.51)
  for pick,ys,cl in ((ll,(332,362),O),(e,(431,461),R)):
   if pick:path(g,[(196,ys[0]-8),(188,ys[0]-8),(188,ys[1]+6),(196,ys[1]+6)],pick,cl,2.15,perm)
  txt(g,'通用文件头：保留',546,702,28,O,perm);txt(g,'重合试题：权重归零',1062,702,28,T,perm*e)
 source(g,'语料清洗示意 · 右侧输入文字保留，权重决定哪些位置计入训练损失')
LIVE_RECORD=json.loads((W/'data/livecode-history.json').read_text())
def rolling(g,c):
 from calendar import monthrange
 from datetime import date
 t=c.t;named=c.at('LiveCodeBench');datecue=c.at('该留的就是');cut=c.at('九月底停止训练');new=c.at('左边这题');jan=c.at('右边那题');later=c.at('第二道');pv=c.at('私有评测集');last=c.at('最终校验');third=c.at('第三道');review=c.at('专家二次审计');rm=c.at('清洗残次题');gold=c.at('白金版本')
 alive=1-phase(t,later-.55,later-.06);wire=1-phase(t,later-.12,later+.76)
 term=phase(t,named-.21,named+.40)
 if alive:
  title(g,'让考试晚于训练',113,alive*(1-phase(t,named-.61,named-.22)),sub='训练和考试，谁先发生？')
  title(g,'LiveCodeBench',113,alive*term,sub=hint('LiveCodeBench'))
 l,h=200,1415;base=446;first=date(2024,3,1);end=date(2025,4,30);X=lambda d:l+(h-l)*(d-first).days/(end-first).days
 xcut=X(date.fromisoformat(LIVE_RECORD['example_cutoff']))
 cc=phase(t,cut-.26,cut+.65);items=LIVE_RECORD['contest_examples'];rel=LIVE_RECORD['releases']
 if wire:
  line(g,(l,base),(h,base),M,1.55,wire)
  for j,(rev,mth,n) in enumerate(rel):
   yr,mo=map(int,mth.split('-'));px=X(date(yr,mo,monthrange(yr,mo)[1]));p=phase(t,.64+j*.57,1.47+j*.57)
   yy=base-38-(n-400)*.207
   line(g,(px,base),(px,mix(base,yy,p)),C,2.5,wire*p);dot(g,px,mix(base,yy,p),5.2,C,wire*p)
   if j in (0,len(rel)-1):
    txt(g,f'{rev} · {n:,} 题',px-3,yy-37,27,C,alive*p)
   txt(g,mth.replace('-','.'),px,base+29,20,M,alive*p)
  txt(g,'截至各月，累计收录',215,239,23,M,alive*phase(t,1.26,2.04),'left')
  line(g,(xcut,265),(xcut,base-5),Y,2.2,wire*cc)
  caption='举例：训练截止 2024.09.30'
  txt(g,caption,xcut,229,25,Y,cc*alive)
  if 0<cc<1:guide(g,[(xcut,265),(xcut,base-5)],cc,Y,1,2.8,.36)
  for j,r in enumerate(items):
   spoken=(new,jan)[j];p=phase(t,spoken-.24,spoken+.55);px=X(date.fromisoformat(r['day']));col=(M,T)[j]
   y=590;one=phase(t,datecue-.18,datecue+.71)
   if p:
    xx,yy=transit((px,base+3),(px,y-52),p,-13)
    line(g,(px,base+36),(xx,yy),col,1.25,alive*p)
    docs(g,xx-11,yy-12,22,28,col,alive*p,2,j)
    txt(g,r['title'],px,y,26,col,alive*p)
    txt(g,r['day'].replace('-','.'),px,y+43,23,col,alive*p)
    if j and one:check(g,px+84,y+42,9,True,alive*one)
  if cc:txt(g,'取截止日之后发布的题',1124,701,26,T,cc*alive)
  source(g,'LiveCodeBench v1–v6 · 六个累计收录数；两个实例为 AtCoder 竞赛日期',term*alive)
 if t>=later-.06:
  turn=phase(t,later-.06,later+.72);title(g,'把题留到最后，还是把旧题审一遍？',113,turn,sub='两种做法，管的是不同的误差')
  for j,(x,cl,ev) in enumerate(((520,V,pv),(1080,O,review))):
   q=phase(t,ev-.24,ev+.59)
   if not q:continue
   txt(g,('私有留出集','公开题的专家复核')[j],x,280,33,cl,q)
   for n in range(4):
    dx=-79+n*53
    travelling=(j==0 and n==3 and t>=last-.20) or (j==1 and n==1 and t>=rm-.22)
    if not travelling:docs(g,x+dx-19,400,39,51,cl,q,3,n)
   if not j:
    seal=phase(t,pv-.09,pv+.69)*(1-phase(t,last-.36,last+.36))
    ring(g,x,478,12,cl,seal,2);box(g,x-20,479,40,24,cl,seal,fill=inkcol(cl,.25));line(g,(x-102,466),(x+102,466),cl,1.5,q)
    go=phase(t,last-.20,last+.80)
    if go:
     xx,yy=transit((x+80,424),(x+99,540),go,-8)
     docs(g,xx-19,yy-24,38,49,cl,q*go,3,3)
     txt(g,'最后一次检验',x,621,27,cl,q*go)
   else:
    a=phase(t,rm-.22,rm+.63)
    if a:
     xx,yy=transit((x-26,425),(x-35,514),a,-8)
     docs(g,xx-18,yy-23,36,46,R,a,2,1);check(g,xx,yy+42,8,False,a)
    prize=phase(t,gold-.21,gold+.63)
    if prize:
     bracket(g,x-109,471,216,O,prize);txt(g,'白金版本',x,621,29,O,prize)
  if t>=third-.27:line(g,(800,282),(800,647),E,1.4,phase(t,third-.27,third+.46))
