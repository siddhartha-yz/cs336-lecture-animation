from termnotes import hint
from ink import *
from motion import *
from itertools import combinations
RECORD=json.loads((W/'data/scaffolds.json').read_text())
def scaffolds(g,c):
 t=c.t;two=c.at('其中两份');one=c.at('只交一份');ks=c.at('交两份');pairs=c.at('十对');bad=c.at('三对两份都错');good=c.at('余下七对');split=c.at('归因陷阱');tool=c.at('工程脚手架');orbit=c.at('工具调用循环');st=c.at('底座一直是');evals=c.at('解决率也会变')
 erase=phase(t,split-.57,split-.14);wire=1-phase(t,split-.16,split+.86);word=1-erase
 if wire:
  named=c.at('要评的 pass');term=phase(t,named-.10,named+.56)
  title(g,'五份补丁，交哪几份？',114,word*(1-phase(t,named-.53,named-.12)),sub='绿色表示通过同一组测试，红色表示未通过')
  if term:title(g,'pass@k',114,word*term,sub=hint('pass@k'))
  colors=(G,G,R,R,R);xs=(488,642,796,950,1104);y=345
  for j,(x,col) in enumerate(zip(xs,colors)):
   k=phase(t,.22+j*.14,.90+j*.14);focus=phase(t,two-.18+j*.065,two+.42+j*.065);col=blend(M,col,focus)
   docs(g,x-32,y-40,64,82,col,k*wire,3,j);dot(g,x+15,y+25,5,col,k*wire)
  answer=c.at('看通过的那两份');p=phase(t,answer-.04,answer+.55);single=phase(t,ks-.48,ks+.45)
  during=phase(t,one-.12,one+.38)*(1-phase(t,answer-.33,answer-.04))
  if during:
   for x in xs:
    line(g,(x-18,y+58),(x+18,y+58),M,1.3,.75*during*word)
  txt(g,'pass@1 = 2 / 5',800,549,43,C,p*(1-single)*word)
  for j,(l,r) in enumerate(combinations(range(5),2)):
   x=199+j*134;yy=507;s=phase(t,pairs-.57+j*.098,pairs+.30+j*.098);a=wire*s;ok=l<2 or r<2
   if not a:continue
   for i,offset in ((l,-17),(r,17)):
    xx,y0=transit((xs[i],y+40),(x+offset,yy),s,(-1 if i>1 else 1)*22)
    dot(g,xx,y0,6.5,colors[i],a)
   line(g,(x-15,yy),(x+15,yy),M,1.35,a)
   focus=phase(t,(good if ok else bad)-.2+.032*j,(good if ok else bad)+.49+.032*j)
   if focus:check(g,x,yy+47,8,ok,focus*a)
  v=phase(t,good-.05,good+.76)
  txt(g,'pass@2 = 7 / 10',800,671,43,Y,v*word)
 if t>=split-.12:
  m=phase(t,split-.13,split+1.05);cx,cy=493,450
  x,y=transit((488,370),(cx,cy),m,27);rad=mix(7,80,m)
  ring(g,x,y,rad,C,phase(m,0,.77),2.7);dot(g,x,y,4,Y,(1-m))
  a=phase(t,split+.34,split+.89);title(g,'脚手架（Scaffold）',111,a,sub=hint('脚手架（Scaffold）'))
  txt(g,'GPT-4o',cx,cy,36,F,a)
  around=phase(t,tool-.17,tool+1.13)
  if around:arc(g,cx,cy,155,-1.57,-1.57+tau*around,O,1.65,around)
  ev=[c.at(x) for x in ('工具调用循环','文件检索','状态管理','任务派发')]
  for j,(lab,qt) in enumerate(zip(('工具调用','检索','状态管理','任务派发'),ev)):
   z=phase(t,qt-.24,qt+.42);ang=-pi/2+j*pi/2;xx=cx+155*cos(ang);yy=cy+155*sin(ang)
   dot(g,xx,yy,6.5,O,around);txt(g,lab,cx+193*cos(ang),cy+193*sin(ang),23,O,z,'left' if j==1 else 'right' if j==3 else 'center')
   if 0<z<1:guide(g,[(cx+80*cos(ang),cy+80*sin(ang)),(xx,yy)],z,Y,1,2.6,.5)
  q=phase(t,st-.5,st+.45);txt(g,'同一组 500 题 · 同一底座',1115,259,27,M,q)
  for i,nm in enumerate(('SWE-Agent','Aider','AutoCodeRover','Moatless Tools','Agentless')):
   p=phase(t,evals-.73+i*.14,evals+.29+i*.14);yy=350+73*i;val=RECORD[nm];col=C if i<4 else Y
   txt(g,nm,959,yy,23,F,p,'right');rect(g,985,yy-6,val*10.3*p,11,col,p);txt(g,f'{val:g}%',1001+val*10.3*p,yy,22,col,p,'left')
  control=c.at('测试集和模型');fixed=phase(t,control-.17,c.at('固定下来')+.43)
  if fixed:
   # Use one dataset-and-base bracket for all rows. Two endpoints of the bracket are literal measurements.
   path(g,[(1432,341),(1446,341),(1446,651),(1432,651)],fixed,M,1.45)
   u=phase(t,control-.04,control+.82)
   if 0<u<1:guide(g,[(983,286),(1009,286),(1009,294),(1253,294)],u,T,1,2.4,.4)
   d0=phase(t,c.at('什么模型')-.25,c.at('什么模型')+.69)
   d1=phase(t,c.at('什么脚手架')-.14,c.at('什么脚手架')+.70)
   if 0<d0<1:guide(g,[(cx-64,cy+34),(cx+65,cy+34)],d0,C,1,3.0,.5)
   if d1:
    y=691;x0=985+23*10.3;x1=985+33.2*10.3
    path(g,[(x0,682),(x0,y),(x1,y),(x1,682)],d1,Y,2)
    txt(g,'相差 10.2 个百分点',1076,700,23,Y,d1,'right')
  source(g,'OpenAI · SWE-bench Verified 发布实验，2024',q)
