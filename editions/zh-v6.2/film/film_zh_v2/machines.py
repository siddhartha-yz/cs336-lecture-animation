from termnotes import hint
from ink import *
from itertools import combinations
ARC=json.loads((W/'data'/'arc-67a3c6ac.json').read_text())
# ARC demonstration uses the public task's exact integers (display palette follows the film).
PAL=('#080808','#58C4DD','#FC6255','#83C167','#FFFF00','#969696','#C58AF9','#F0AC5F','#5CD0B3','#AD3954')
def grid(g,a,cx,cy,size,p=1,op=1,mark=None,empty=False):
 n=len(a);m=len(a[0]);s=size/max(m,n);x=cx-m*s/2;y=cy-n*s/2
 for i,row in enumerate(a):
  for j,v in enumerate(row):
   k=phase(p,0.34*(i*m+j)/(m*n),.62+.34*(i*m+j)/(m*n))
   col=PAL[v] if not empty else '#121212'
   box(g,x+j*s,y+i*s,s-.9,s-.9,D,op,sw=.8)
   if not empty and k>0:
    pad=(1-k)*s*.48+1.0
    rect(g,x+j*s+pad,y+i*s+pad,s-2*pad,s-2*pad,col,op*.93)
 if mark is not None:
  i,j=mark;box(g,x+j*s,y+i*s,s,s,F,op,sw=2.6)
def repo(g,c):
 t=c.t;agent=on(c,'调用工具',2);bench=on(c,'SWE-bench',1.5);num=on(c,'两千两百九十四',2);find=on(c,'定位问题',2);patch=on(c,'Git 补丁',2);ver=on(c,'Verified',1.6)
 title(g,'SWE-bench',115,sub=hint('SWE-bench'))
 x=170;y=282;names=[('sphinx',0),('ext',1),('napoleon',2),('docstring.py',3)]
 for j,(nm,depth) in enumerate(names):
  xx=x+depth*42;yy=y+60*j;col=Y if j==3 and find>.45 else C
  if j: g.poly([(xx-31,yy-43),(xx-31,yy),(xx-7,yy)],E,1.8,.87)
  txt(g,nm,xx,yy,32,col,1,'left')
 # Twelve source projects are not twelve steps through one repository. One sheet
 # detaches from the collection and turns into Sphinx issue #5560 on the right.
 count=c.at('十二个');issue=c.at('工单写的是问题');submission=c.at('提交记录');from_repo=c.at('把两边配起来');case=c.at('一份 Issue');audit=c.at('逐题复核');env=c.at('有些工单')
 pre=1-phase(t,env-.38,env+.38)
 txt(g,'12 个 Python 项目',177,599,28,C,phase(t,count-.15,count+.50)*pre,'left')
 for j in range(12):
  k=phase(t,count-.16+j*.105,count+.40+j*.105);dx=191+27*j
  if k:docs(g,dx-8,637,16,22,T if j==10 else C,k*pre,2,j)
 txt(g,'2,294 个问题',177,701,31,Y,num*pre,'left')
 # One actual issue and its accepted change are the unit of a benchmark instance.
 # The entire twelve-project collection is a source pool, not twelve repair steps.
 pair_end=1-phase(t,case-.55,case+.08)
 if pair_end:
  left=phase(t,issue-.16,issue+.48)*pair_end;right=phase(t,submission-.17,submission+.51)*pair_end
  txt(g,'工单 #5560',178,534,25,C,left,'left')
  txt(g,'PR #8713',420,534,25,T,right,'left')
  join=phase(t,from_repo-.11,from_repo+.76)
  if join:arrow(g,(325,535),(403,535),join,Y,pair_end,2.0)
 itm=phase(t,from_repo+.51,case+.38)
 if 0<itm<1:
  from motion import guide,transit
  q=phase(itm,.07,.90);px,py=transit((461,648),(1268,343),q,54)
  docs(g,px-10,py-13,20,26,T,sin(pi*itm),2,1)
 ince=phase(t,case-.31,case+.46)
 if ince:txt(g,'Issue #5560',1373,341,23,T,ince*(1-phase(t,c.at('Git 补丁')-.52,c.at('Git 补丁')-.02)),'right')
 if env-.30<t:
  # Human annotators looked at what the issue says and what the tests accept;
  # environment reproducibility is handled by the sandbox in the following scene.
  tests=c.at('有些测试')
  for j,(cap,col,event) in enumerate((('要求说清了',V,env),('容许等价改法',T,tests))):
   x=(242,457)[j];nn=phase(t,event-.21,event+.53);r=phase(t,audit-.18+j*.16,audit+.48+j*.16)
   if nn:
    docs(g,x-17,551,34,43,col,nn,3,j)
    txt(g,cap,x,630,24,col,nn)
    if r:check(g,x,670,8,True,r)
 line(g,(605,265),(605,650),E,1.3)
 txt(g,'Other Parameters',737,283,35,F,1,'left')
 txt(g,'忽略了 napoleon_use_param 设置',737,339,27,M,bench,'left')
 if patch<1:
  # The actual discrepancy: a configuration flag never reaches the formatting branch.
  a=(1-phase(t,c.at('Git 补丁')-.72,c.at('Git 补丁')-.19))*phase(t,2.0,4.5)
  if a:
   txt(g,'napoleon_use_param',736,437,26,C,a,'left',385,'DejaVu Sans Mono')
   txt(g,'True',1155,437,27,Y,a,'left')
   line(g,(750,496),(1173,496),E,1.4,a)
   trace=phase(t,c.at('完整的代码库')-.6,c.at('定位问题')+1.1)
   txt(g,'_format_fields(…)',737,558,25,O,a,'left',415,'DejaVu Sans Mono')
   if trace:
    zz=curve((1190,496),(1000,519),trace,-17)
    path(g,[(1190,454),(1190,496),(1000,519)],trace,R,2,a)
    dot(g,zz[0],zz[1],4.6,R,a*trace)
 if patch:
  from wetjoins import patch_code
  for j in range(5):
   q=phase(patch,.06*j,.68+.06*j);patch_code(g,j,738,423+j*39,q)
 if find and patch<1:
  p=(t*.24)%1
  path(g,[(512,462),(582,462),(582,385),(725,385)],p,C,2.4,find*(1-patch))
 if patch:txt(g,'PR #8713',1402,287,24,G,patch,'right')
 if ver:txt(g,'Verified · 人工筛选的 500 题',1062,680,30,T,ver)
 source(g,'讲义图 205 · Sphinx #5560 → #8713 · 文档解析修复节选')
def testlamps(g,x,y,n,cols,rows,status,p=1,base=G):
 for j in range(n):
  xx=x+(j%cols)*27;yy=y+(j//cols)*30;k=phase(p,j/n*.34,.65+j/n*.34)
  col=R if j in status else base
  ring(g,xx,yy,7.8,col,.62);dot(g,xx,yy,4.55,col,k)
def docker(g,c):
 t=c.t;branch=on(c,'Docker',1.9);failpass=on(c,'Fail-to-Pass',1.5);passpass=on(c,'Pass-to-Pass',1.5);bad=on(c,'把整段逻辑删掉',2.3);caught=on(c,'回归测试就会亮红灯',2)
 title(g,'补丁通过，得看两排灯',115,sub='把修复放回原版本和依赖中运行')
 # Both test populations inhabit one and the same sandbox.
 p=[(235,251),(1367,251),(1367,650),(235,650),(235,251)];path(g,p,branch,C,2.4,.68)
 txt(g,'Docker · 固定代码与依赖',800,286,27,C,branch)
 txt(g,'FAIL_TO_PASS',444,374,31,F);txt(g,'PASS_TO_PASS',1075,374,31,F)
 for j in range(2):
  xx=390+j*110
  reopen=phase(t,c.at('原本复现')-.26,c.at('原本复现')+.40)
  solved=phase(t,c.at('转绿通过')-.18+j*.14,c.at('转绿通过')+.42+j*.14)
  col=blend(blend(E,R,phase(t,c.at('真跑代码')-.1,c.at('真跑代码')+.57)),G,solved)
  ring(g,xx,500,26,col,1,2.5);dot(g,xx,500,10,col)
  if reopen and solved<1:check(g,xx,557,8,False,reopen*(1-solved))
  if solved:check(g,xx,557,9,True,solved)
 p=phase(t,c.at('运行依赖')-.3,c.at('两道测试')+1.65)
 testlamps(g,923,443,45,12,4,set([6,10,14,21,28,34,39]) if caught>.4 else set(),.37+.63*p)
 if passpass and not caught>=1:
  # Sweep the suite in execution order. The ring marks a running test, not an extra observation.
  en=phase(t,c.at('Pass-to-Pass')-.1,c.at('也必须全部通过')+1);idx=min(44,int(en*45))
  if en<1:ring(g,923+idx%12*27,443+idx//12*30,12,Y,passpass,2.2)
 txt(g,'从失败转为通过',448,608,26,G,solved)
 txt(g,'不能引入新回归',1062,608,26,R if caught>.35 else T,passpass)
 if bad:
  txt(g,'删去逻辑的候选补丁',803,709,28,R,bad)
  if caught:check(g,1009,709,10,False,caught)
 # The centre keeps the identity of the change. We run the whole old suite, not
 # just the new regression. The deliberately bad deletion replaces that one candidate.
 old=phase(t,c.at('代码版本')-.17,c.at('代码版本')+.56)
 if old:
  here=phase(t,c.at('补丁打进沙箱')-.15,c.at('补丁打进沙箱')+.80)
  x,y=754,517
  docs(g,x-47,y-36,94,79,T,old,0,0)
  for j,wid in enumerate((43,54,34)):
   yy=y-13+j*12
   line(g,(x-28,yy),(x-28+wid,yy),M,1.7,old*(1-bad*.68))
  if here:
   line(g,(x-26,y-1),(x+23,y-1),G if bad<.55 else R,2.7,here)
  if bad:line(g,(x-30,y-10),(x+27,y+14),R,2.3,bad)
  txt(g,'同一份补丁' if here>.55 else '固定版本',x,590,22,T,old)
  run=phase(t,c.at('打完补丁后')-.26,c.at('转绿通过')+.14)
  if 0<run<1:
   pts=[(x-52,y),(590,y),(590,476),(499,476)];path(g,pts,run,Y,2.3)
 # A patch enters one fixed environment. Two independent tests read that same change.
 from motion import guide
 from wetjoins import packet_pose,patch_sheet
 px,py,entry=packet_pose(t,c)
 if not getattr(g,'carry_patch',False) and entry<1:
  patch_sheet(g,px,py,1-phase(entry,.75,.998))
  txt(g,'候选补丁',px,py+70,23,T,1-phase(entry,.03,.45))
  inspect=phase(t,c.at('目测打分')-.18,c.at('目测打分')+.71)
  if 0<inspect<1:
   yy=py-29+57*inspect
   line(g,(px-42,yy),(px+41,yy),M,1.4,sin(pi*inspect)*.62)
 for tip,key in [((444,458),'Fail-to-Pass'),((1044,432),'Pass-to-Pass')]:
  t0=c.at(key);q=phase(t,t0-.32,t0+.72)
  if 0<q<1:guide(g,[(755,452),(755,415),(tip[0],415),tip],q,Y,1,2.7,.33)
 if 0<caught<1:
  xx=923+(6%12)*27;yy=443+(6//12)*30;ring(g,xx,yy,8+16*caught,R,sin(pi*caught),2.3)
 source(g,'两组测试必须同时通过 · 代码行为判定示意')
from scaffold_lens import scaffolds
def abstract(g,c):
 t=c.t;memory=on(c,'预训练',2.7);new=on(c,'不给它熟悉的代码',2.9);rule=on(c,'三组网格',2.2)
 title(g,'修过旧仓库，就会解新题吗？',125,sub='把熟悉的题材拿走，只留下可观察的变换')
 for k in range(12):
  xx=265+(k%4)*95;yy=303+(k//4)*82
  docs(g,xx,yy,68,54,(C,T,V)[k%3],1-new,3,k)
 if memory and new<1:
  path(g,[(235,603),(605,603),(640,555)],memory,O,2.2,1-new)
  txt(g,'曾经读过的代码？',411,672,26,O,memory*(1-new))
 arrow(g,(663,439),(911,439),.4+.6*new,Y,1,2.4)
 a=ARC['train'][0];size=mix(145,227,new)
 grid(g,a['input'],mix(1104,515,new),443,size,.55+.45*new,.85);grid(g,a['output'],1132,443,size,rule,rule)
 txt(g,'输入',mix(1104,515,new),637,30,C,1);txt(g,'输出',1132,637,30,Y,rule)
