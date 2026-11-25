"""One Sphinx defect, one upstream diff, one real red test, forty-five selected regressions."""
from ink import *
from motion import guide,transit
from studio_examples import pstep,silk,area,VIO,BLUE,AQUA,MONO
from ink_words import carryword,swish,letter
from timeline3 import W,clock,S
from termnotes import hint
from pathlib import Path
import json
ROW=json.loads((W/'source/swe-8713.json').read_text())
F2P=ROW['FAIL_TO_PASS'];P2P=ROW['PASS_TO_PASS']
if isinstance(F2P,str):F2P=json.loads(F2P)
if isinstance(P2P,str):P2P=json.loads(P2P)
assert(len(F2P),len(P2P))==(1,45)
lines_=[('-','return self._format_fields(…)'),('+','if self._config.napoleon_use_param:'),('+','    fields = self._consume_fields(multiple=True)'),('+','    return self._format_docutils_params(fields)')]
def diff(g,x,y,w,s,phase_,op=1):
 for i,(side,label) in enumerate(lines_):
  q=clip(phase_*1.41-i*.12);col=R if not i else T
  if not q:continue
  yy=y+i*56*s
  rect(g,x-5,yy-17*s,w*q,35*s,inkcol(col,.22),op*q);txt(g,side,x+14,yy,24*s,col,op*q)
  txt(g,label,x+39*s,yy,25*s,F,op*q,'left',w-55*s,MONO)
def repos(g,c):
 t=c.t;name=c.at('SWE-bench');real=c.at('真正出了问题');twelve=c.at('十二个开源');issue=c.at('工单写的是问题');pair=c.at('把两边配起来');n2294=c.at('两千两百九十四');case=c.at('完整的代码库');find=c.at('定位问题');patch=c.at('一份 Git 补丁');filter_=c.at('没说清要求');picky=c.at('只认一种写法');verified=c.at('Verified')
 # The identifier from the previous frame persists; it is enlarged before becoming a source file.
 title_=pstep(t,name-.43,.66)
 silk(g,'SWE-bench',130,101,52,t-name+.60,F,1,'pen','left')
 if title_:silk(g,hint('SWE-bench'),132,163,26,t-name-.05,M,title_,align='left')
 early=1-phase(t,case-.50,case+.24);done=phase(t,verified-.40,verified+.42);p=phase(t,.0,.90)
 if early:
  x0=425;tx,ty=transit((800,449),(x0,363),p,31)
  txt(g,'other_parameters',tx,ty,mix(38,35,p),C,early,font=MONO)
  u=pstep(t,real-.42,.62)
  if u:
   txt(g,'Sphinx · Issue #5560',x0,294,30,T,u*early);txt(g,'设置为 True，输出却仍是旧格式',x0,455,26,F,u*early)
   # The on-screen bug has a visibly ignored argument, not a generic paperwork emblem.
   frame=phase(t,issue-.09,issue+.49);txt(g,'napoleon_use_param',274,551,25,C,u*early,'left',335,MONO)
   txt(g,'True',570,551,26,Y,u*early,'left',font=MONO)
   if frame:swish(g,272,606,586,t-issue+.03,Y,.62)
  v=pstep(t,twelve-.12,.61)
  if v:
   lab=['astropy','django','flask','matplotlib','pylint','pytest','requests','scikit-learn','seaborn','sphinx','sympy','xarray']
   for j,name_ in enumerate(lab):
    x=829+(j%3)*215;y=270+(j//3)*75;h=pstep(t,twelve-.08+j*.041,.42)
    if h:
     a=(1 if j==9 else .71)*early*h;dot(g,x,y,5.5,T if j==9 else BLUE,a);txt(g,name_,x+16,y,22,F if j==9 else C,a,'left',181,MONO)
   txt(g,'12 个开源 Python 项目',1110,589,28,M,v*early)
   if t>=pair-.20:
    q=pstep(t,pair-.20,.73);xx,yy=transit((829,495),(700,362),q,44)
    dot(g,xx,yy,8,Y,q*early);txt(g,'PR #8713',651,278,25,Y,q*early)
   if t>=n2294-.24:silk(g,'2,294 道题',1111,696,39,t-n2294+.24,Y,early,'pen')
 if early<1:
  a=1-early;h=pstep(t,case-.25,.60)
  txt(g,'sphinx / ext / napoleon / docstring.py',145,249,31,C,a,'left',849,MONO);txt(g,'#8713',1454,249,27,T,a,'right')
  line(g,(145,288),(1454,288),E,1.4,a)
  # Separate source from behaviour. The yellow trace preserves the identity of the configuration flag.
  kk=phase(t,find-.22,find+.53);d0=phase(t,patch-.37,patch+.43)
  if d0<1:
   txt(g,'napoleon_use_param = True',158,386,38,F,a*(1-d0),'left',780,MONO)
   txt(g,'_format_fields(…)',158,496,38,R,a*(1-d0),'left',740,MONO)
   arrow(g,(637,397),(426,474),kk,O,a*(1-d0),2.1)
  if d0:diff(g,156,369,820,1.,d0,a)
  # A small view of the emitted RST is more concrete than an icon for a file.
  wait=pstep(t,case-.11,.60);txt(g,'文档输出',1194,356,29,M,a*wait)
  # Same parameter as the public regression assertion and the preceding match cut.
  # The omitted class reference does not affect the field prefix being tested.
  txt(g,':param param2:' if d0>.56 else ':Other Parameters:',1191,454,32,T if d0>.56 else R,a*wait,width=365,font=MONO)
  txt(g,':type param2: …' if d0>.56 else '**param2** …',1191,517,30,F,a*wait,width=365,font=MONO)
  ax=phase(t,filter_-.16,filter_+.51);bx=phase(t,picky-.16,picky+.51)
  if ax:txt(g,'复核工单要求',324,689,26,T,a*ax)
  if bx:txt(g,'复核测试约束',724,689,26,T,a*bx)
  if done:silk(g,'Verified：500 题',1202,686,36,t-verified+.29,Y,a,'pen')
def tests(g,c):
 t=c.t;name=c.at('Docker');fixed=c.at('运行依赖');patch=c.at('补丁打进');both=c.at('两道测试');first=c.at('Fail-to-Pass');red=c.at('原本复现');green=c.at('转绿通过');second=c.at('Pass-to-Pass');reg=c.at('原本正常');all_=c.at('全部通过');bad=c.at('把整段逻辑删掉');cost=c.at('另一项功能');caught=c.at('亮红灯');finish=c.at('两排一起看')
 # Start with the exact flag tested on the previous board.
 wait=pstep(t,name-.30,.65);txt(g,'Docker',143,157,29,C,wait,'left');txt(g,ROW['base_commit'][:9],306,158,23,M,wait,'left',font=MONO)
 shift=phase(t,both-.57,both+.3)
 if shift<1:
  op=1-shift;v=pstep(t,.18,.56);diff(g,179,283,841,.97,v,op)
  from mounting import etch
  eye=c.at('目测打分');run=c.at('真跑代码');ver=c.at('代码版本');tar=pstep(t,run-.22,.61)
  # Pass the actual changed branch and test identifier into the same isolated process.
  eyeop=phase(t,eye-.19,eye+.32)*(1-phase(t,run-.27,run+.20))
  if eyeop:
   pp=phase(t,eye-.13,run-.17)
   path(g,[(1101,408),(1170,360),(1228,362),(1302,408),(1231,449),(1166,449),(1101,408)],1,M,2.15,op*eyeop)
   dot(g,1192+17*pp,402,11,C,op*eyeop)
  open_=pstep(t,name-.26,.74);px=1062;yy=287
  if tar:
   path(g,[(1018,352),(1018,531),(1440,531)],tar,T,2.6,op)
   etch(g,'pytest',px,yy,32,T,tar*op)
   etch(g,'test_parameters_with_',px,yy+64,24,F,tar*op)
   etch(g,'class_reference',px,yy+103,24,F,tar*op)
   if open_:
    path(g,[(1021,302),(1021,236),(1440,236),(1440,527)],open_,C,2.7,op)
    cap=pstep(t,ver-.14,.60);deps=pstep(t,fixed-.12,.61)
    etch(g,'commit',px,yy+169,22,M,cap*op);etch(g,ROW['base_commit'][:9],px+97,yy+169,27,O,cap*op)
    etch(g,'Sphinx '+str(ROW['version']),px,yy+215,25,C,deps*op)
    if cap:check(g,1378,yy+169,9,True,cap*op)
    if deps:check(g,1378,yy+215,9,True,deps*op)
   u=phase(t,patch-.22,patch+.66)
   if 0<u<.99:
    xx,dy=transit((800,365),(px+6,yy+101),u,62);dot(g,xx,dy,9,T,op)
 if shift:
  a=shift;fail=phase(t,red-.32,red+.36);pass_=phase(t,green-.2,green+.47);reg_=pstep(t,second-.38,.63);bad_=phase(t,bad-.14,bad+.51);blink=phase(t,caught-.48,caught+.41)
  x=415;y=457
  txt(g,'FAIL_TO_PASS',x,278,36,C,a,font=MONO);txt(g,'PASS_TO_PASS',1122,278,36,T,a*max(.29,reg_),font=MONO)
  # Actual row for Sphinx: one named failing test and forty-five regression assertions.
  cc=blend(blend(C,R,fail),G,pass_)
  ph=1+.13*sin(pi*pass_);r=65*ph
  g.circle(x,y,r,inkcol(cc,.34),cc,3.7,a);txt(g,'1',x,y,52,F,a)
  txt(g,'test_parameters_with_class_reference',x,590,22,M,a,'center',517,MONO)
  pathop=phase(t,c.at('报错的单元测试')-.18,c.at('打完补丁')+.56)
  if fail and pass_<.99 and pathop:
   q=clip(pathop);arc(g,x,y,r+16,-pi/2,-pi/2+tau*q,R,3.3,a*(1-pass_))
  if fail and pass_<1:txt(g,'旧版失败',x,655,30,R,a*(1-pass_))
  if pass_:txt(g,'打补丁后通过',x,655,30,G,a*pass_)
  # No fake completed run: the false-candidate vignette is explicitly flagged, and no simulated 7/45 is published.
  ci=22
  for i,case in enumerate(P2P):
   xx=900+(i%9)*55.3;yy=365+(i//9)*54
   orig=phase(t,reg-.35+i*.021,reg+.05+i*.021);running=phase(t,reg-.1,all_+.26)*45
   genuine=G if orig else '#666C70';col=blend(genuine,R,blink) if i==ci else genuine
   val=.36+.61*orig;rect(g,xx-11,yy-11,23,23,inkcol(col,val),a*max(.44,reg_))
   if 0<running<45 and i==int(running):box(g,xx-16,yy-16,33,33,Y,a,sw=2.1)
   if blink and i==ci:
    rr=13+24*blink;ring(g,xx,yy,rr,R,a*(1-.62*blink),2.0)
  if bad_:
   from mounting import etch
   pos=(900+ci%9*55.3,365+ci//9*54)
   fit=phase(t,cost-.25,caught+.3);ret=1-phase(t,finish-.31,finish+.18)
   if fit and ret:
    path(g,[(x+90,460),(770,460),(pos[0]-48,pos[1]+5),pos],fit,R,2.4,ret)
    if fit<1:dot(g,*transit((x+91,460),pos,fit,20),7,O,ret)
  if reg_:
   lab='45 项回归检查' if not bad_ else '假设一次删错逻辑的补丁'
   txt(g,lab,1113,659,28,R if bad_ else T,a*reg_)
  if t>=finish-.15:
   swish(g,306,1367,717,t-finish+.12,Y,.68)
