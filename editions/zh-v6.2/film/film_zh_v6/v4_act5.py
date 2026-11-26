from rig4 import *
from studio_tests import patch as patchglyph
def sandbox(g,c):
 t=c.t;pageend=c.at('报错那天')+.38;diffat=c.at('把仓库交给它')-.12;lit=c.at('现在把同一份补丁')-.09
 if t<pageend:
  # A short physical landing, then the camera goes to the *actual* lines the report compares.
  q=c.u('真的工单',.68);u=enter(t,.02,.52);subject=c.at('一种参数');other=c.at('其他参数')
  focus=phase(t,subject-.40,other+.10) # coordinates belong to the 1294x774 source crop below
  from gates6 import issue,issue_pose
  cx,cy,w,theta=issue_pose(u,focus);issue(g,u,focus)
  ctx=g.c;ctx.save();ctx.translate(cx,cy);ctx.rotate(theta);sc=w/1294;ctx.scale(sc,sc);ctx.translate(-647,-387)
  # Neutral paper and brown/teal ink, in the coordinate system of the photographed issue.
  for tag,px,yy,ww,col in (('按配置排版',214,673,241,'#276A64'),('其他参数',114,497,427,'#A54930')):
   at=c.at(tag);z=during(t,at-.19,at+2.06,.37)
   if z:path(g,[(px,yy),(px+ww,yy)],enter(t,at-.17,.55),col,3.25,z)
  ctx.restore()
  if focus<.73:label(g,'sphinx-doc/sphinx  ·  #5560',789,749,30,O,q*(1-focus))
 elif t<diffat:
  from bench6 import intake
  intake(g,c,pageend,diffat)
 elif t<lit:
  from bench6 import checkout
  checkout(g,c,diffat,lit)
 elif t<c.at('第一排灯')-.18:
  first=c.at('第一排灯')-.18
  from bench6 import enclose
  enclose(g,c,lit,first)
 else:testrack(g,c)
def testrack(g,c):
 # The narrator says “上面”“下面”. Use two actual deck heights all the way from
 # the first red reproduction to the verdict. A counterexample is not the state of the accepted patch.
 t=c.t;first=c.at('第一排灯')-.18;a=enter(t,first,.62);red=enter(t,c.at('一盏红')-.22,.45);green=enter(t,c.at('红灯得变绿')-.15,.60)
 second=c.at('四十五盏')-.22;reg=enter(t,second,.69);stress=c.at('另一种')-.20;broken=c.at('就会亮红')-.14;ok=c.at('两排一起')-.15
 caught=enter(t,broken,.54);repair=enter(t,ok,.64);hyp=enter(t,stress,.53)*(1-repair)
 mark(g,'FAIL_TO_PASS',210,224,43,t-first,C,'left','pen',.57)
 label(g,'test_parameters_with_class_reference',212,300,27,F,a,'left')
 col=blend(blend(C,R,red),G,green);cx,cy=1058,278;rad=49+4*sin(pi*green)
 ring(g,cx,cy,rad+7,col,max(a*.80,1-phase(t,first+.07,first+.50)),1.85);dot(g,cx,cy,rad,inkcol(col,.65),a);label(g,'1',cx,cy,39,F,a)
 if green:label(g,'1 / 1',1491,278,37,G,green,'right')
 if reg:
  mark(g,'PASS_TO_PASS',211,443,43,t-second,T,'left','pen',.58)
  label(g,'原本通过的回归用例',212,516,31,M,reg,'left')
  left,top=737,424;sz=20;pitch=37;x0,y0=0,0
  jbad=22
  for j in range(45):
   x=left+(j%15)*pitch;y=top+(j//15)*pitch;v=enter(t,second+.03+j*.020,.51)
   hit=caught*(1-repair)if j==jbad else 0.;co=blend(G,R,hit)
   ww=sz*(.40+.60*v);rect(g,x-ww/2,y-ww/2,ww,ww,inkcol(co,.93),v)
   if j==jbad:
    x0,y0=x,y
    if hyp:ring(g,x,y,22+14*enter(t,stress,.54),O,.72*hyp,1.9)
  example=c.at('原来就通过');guard=c.at('回归测试')
  if example-.10<t<stress-.12:
   # This first lamp is an actual PASS_TO_PASS entry from sphinx__sphinx-8713,
   # not an arbitrary box. It is a different case from the one under repair.
   vis=during(t,example-.10,stress-.12,.40);zh=enter(t,guard-.18,.58)
   ring(g,left,top,16+5*zh,T,vis,2.05)
   path(g,[(left-13,top+2),(left-64,top+44),(630,570),(593,570)],zh,T,1.8,vis)
   label(g,'test_attributes_docstring',216,568,27,T,vis*zh,'left')
  if caught:label(g,'45 / 45'if repair>.60 else'44 / 45',1491,top+pitch,37,G if repair>.60 else R,caught,'right')
  else:label(g,'45 / 45',1491,top+pitch,37,G,reg,'right')
  if hyp:label(g,'若另一种正常写法坏了',1000,608,30,R if caught else O,hyp)
  here=c.at('上面这一关');there=c.at('下面叫')
  swish(g,212,508,260,t-here,C,.62,3.2);swish(g,212,516,480,t-there,T,.62,3.2)
  if repair:
   # Real patch and hypothetical break stay distinct; both test constraints feed this verdict.
   label(g,'实际补丁',626,689,29,O,repair)
   for p0 in ((cx+61,cy),(left+14*pitch+16,top+pitch)):
    dest=(963,676);route=[p0,(1297,p0[1]),(1297,622),(1126,676),dest]
    path(g,route,repair,G,2.0,repair*.82)
   check(g,897,682,20,True,repair);label(g,'通过',838,686,36,G,repair,'right')
   local=c.at('修到了那处');pres=c.at('还保住')
   # Trace backward from the accepted test result to each row independently.
   fg=during(t,local-.36,pres+.10,.40)
   if fg:
    q=phase(t,local-.32,pres+.07)
    ring(g,cx,cy,rad+12,G,fg,2.6)
    dot(g,1297,mix(622,cy,q),5.5,G,fg)
   seen=during(t,pres-.06,c.d-.20,.43)
   if seen:
    p0=phase(t,pres-.1,c.d-.57);j0=min(44,int(p0*45));x=left+j0%15*pitch;y=top+j0//15*pitch
    ring(g,x,y,17,G,seen,2.35)
    cap=enter(t,pres+.03,.49);swish(g,212,516,550,t-pres+.02,G,.88,3.2)

def chances(g,c):
 t=c.t;ex=c.at('这就是 pass')-.12;pivot=c.at('读任何智能体榜单')-.12;pub=c.at('同一套五百题')-.10;repo=c.at('还有一点藏在')
 five=c.at('五份候选');pass_=c.at('恰好两份');keep=c.at('随机交一份')-.40
 if t<keep:
  # The accepted repair on the previous plate is the test apparatus, not sample A.
  # Carry its check along the rail; five new, initially ungraded candidates emerge.
  collect=phase(t,.63,c.at('多采几份')+.72);wave=phase(t,c.at('多采几份')-.10,five+.08)
  if collect<1:endpaper(g,'5-1',0,0,1,1-collect)
  start=(897,682);receiver=(800,493);head=transit(start,receiver,p5(collect),60)
  lamp=1-phase(t,five+.38,pass_-.08)
  if lamp:
   check(g,*head,19,True,lamp);rad=16+18*collect
   ring(g,*head,rad,G,collect*lamp*.72,1.75)
   label(g,'同一台验收机',head[0],head[1]+65,28,G,collect*lamp)
  centered=(800+1.035*(349-800),800+1.035*(575-800),800,800+1.035*(1025-800),800+1.035*(1251-800))
  yy=414+1.035*(405-480);oneby=c.at('一份一份跑')
  for j,target in enumerate(centered):
   start_at=c.at('多采几份')+.06+.22*j;z=phase(t,start_at,five-.16+.15*j)
   xx,y2=transit((800,493),(target,yy),z,49+.13*abs(target-800))
   co=blend(C,(G,R)[j>=2],phase(t,pass_+.07*j-.10,pass_+.55+.07*j))
   if z:
    patchglyph(g,xx,y2,j,co,1.12*1.035*(.37+.63*z),z)
    pulse=during(t,oneby-.22+.15*j,oneby+.48+.15*j,.19)
    if pulse:line(g,(xx-43,yy+69),(xx+43,yy+69),O,2.5,pulse)
 elif t<pivot:
  blind=c.at('自己会识别')-.35
  if t>=blind:blind_samples(g,c,t,blind,pivot)
  else:
   from pair6 import proof
   proof(g,c,keep,ex,blind)
 else:
  from scaffold6 import logic
  logic(g,c,pivot,pub,repo)

def blind_samples(g,c,t,st,en):
 # The five samples remain the *same patch bodies* while their result marks
 # become hidden. A new verifier, not a new rank, applies the two results.
 from pair6 import proof,CO,VALUE_RAIL
 z=easepos(t,st,.73);xx0=(444,623,802,981,1160);y=382
 ex=c.at('这就是 pass')-.12;keep=c.at('随机交一份')-.40
 if z<.999:proof(g,c,keep,ex,st,parts=False,opacity=1-z)
 arc=easepos(t,st+.15,1.33)
 xx,yy=VALUE_RAIL.at(arc)
 label(g,'7 / 10',xx,yy,mix(62,53,arc),Y,(.57+.43*arc)*(1-phase(t,en-.62,en-.12)))
 note=enter(t,st+1.06,.48)*(1-phase(t,en-.31,en-.03))
 label(g,'随机抽两份的成功率',800,248,27,M,note)
 send=c.at('哪份答案正确')-.22;test=c.at('提前把测试答案');sel=phase(t,send,send+1.03);gate=enter(t,test-.12,.61)
 bg=1-phase(t,en-.28,en-.013)
 for ii,x in enumerate(xx0):
  prev=(382+209*ii,326);xx,yy=transit(prev,(x,y),z,8*ii-12)
  co=blend(CO[ii],C,z)
  if ii in (1,3):
   dst=(610 if ii==1 else 775,570);xx,yy=transit((xx,yy),dst,p5(sel),-36)
  patchglyph(g,xx,yy,ii,co,mix(.92,.70,z),bg)
 if gate:
  line(g,(930,476),(930,672),M,2.1,gate*bg)
  label(g,'评测方验收',1207,515,33,F,gate*bg)
  v=enter(t,test+.20,.50);path(g,[(822,570),(903,570),(931,592),(1042,592)],v,T,2.2,gate*bg)
  if v:
   carry=enter(t,en-.50,.47)
   check(g,1127,601,16,True,max(v*bg,carry))
   check(g,1274,601,16,False,v*bg)
 label(g,'抽样时不看标准答案',800,748,29,O,enter(t,st+.29,.66)*bg)
