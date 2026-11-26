"""Keep the axle, change the tool path. Then measure each whole configuration."""
from rig4 import *
from bench6 import PASSING
from motion6 import ArcLength
CORE='#58C4DD';DEPTH='#234859'
MEASURES=(('SWE-Agent',23.0,115,C),('Agentless',33.2,166,T))
MODULES=('文件检索','终端调用','整理上下文')
XL=(371,1149,889);YL=(396,407,687)

def chip(g,x,y,scale=1,op=1,ring_size=0):
 ctx=g.c;ctx.save();ctx.translate(x,y);ctx.scale(scale,scale)
 v=[(92*cos(a),81*sin(a))for a in (-pi*.5+tau*i/6 for i in range(6))]
 g.poly([(x,y+13)for x,y in v],DEPTH,2.1,op,True,inkcol(CORE,.33),op)
 g.poly(v,CORE,2.3,op,True,inkcol(CORE,.47),op)
 label(g,'GPT-4o',0,0,36,F,op);ctx.restore()
 if ring_size>.06:ring(g,x,y+3,(102+12*ring_size)*scale,CORE,op*.76*ring_size,1.85)
def panel(g,x,y,w,h,co,a,phase):
 # Three open shapes, with visible moving contents. The tapered side is the connector.
 for dx,dy in ((.13,.11),(.08,.08)):
  g.poly([(x-w*.5+dx*w,y-h*.5+dy*h),(x+w*.5+dx*w,y-h*.5+dy*h),
          (x+w*.5+dx*w,y+h*.5+dy*h),(x-w*.5+dx*w,y+h*.5+dy*h)],
       co,1.15,a*.45,True,inkcol(co,.29),a*.53)
 box(g,x-w*.5,y-h*.5,w,h,co,a,inkcol(co,.20+.12*phase),1.75)
def attribution(g,c,t,pivot,first):
 if t>=first+.18:return
 q=easepos(t,pivot-.10,1.21);split=easepos(t,c.at('归因陷阱')-.32,.78)
 finish=1-easepos(t,first-.13,.31)
 actual=(1127,601);dst=(796,319)
 x,y=transit(actual,dst,q,-125)
 dot(g,x,y,mix(0,19,q),T,finish*(1-.12*q));check(g,x,y,16.,True,finish)
 ring(g,x,y,17+18*q,T,finish*q*.88,2.1)
 lab=enter(t,pivot+.54,.49)*finish
 if lab:label(g,'解决结果',x,y-66,33,T,lab)
 for i,col in enumerate((C,V)):
  land=(mix(548,577,split),555)if not i else(mix(1055,1017,split),555)
  begin=enter(t,pivot+.44+.19*i,.70);bend=easepos(t,pivot+.33+.16*i,1.37)
  pts=[(x-13+26*i,y+37),(x-38+76*i,y+121),land]
  if begin:
   path(g,pts,bend,col,3.3,finish*begin*.83)
   if 0<bend<.99:point(g,*ArcLength(pts).at(bend),7.8,col,finish*begin)
   reach=enter(t,pivot+1.04+i*.16,.56)
   if reach:
    # A component silhouette belongs to a hypothesis, not to either one of
    # the trial patches on the previous screen.
    r=32+13*split
    h=finish*begin*reach
    if not i:
     body=[(land[0]+r*cos(-pi/2+j*tau/6),land[1]+r*sin(-pi/2+j*tau/6))for j in range(6)]
     g.poly(body,col,1.95,h,True,inkcol(col,.39),h)
     dot(g,*land,8,col,h)
    else:
     body=[(land[0]+r*cos(j*tau/8),land[1]+r*sin(j*tau/8))for j in range(9)]
     path(g,body,easepos(t,pivot+1.0,1.19),col,3.55,h)
     for j in (0,2,4,6):
      dot(g,*body[j],7.1,col,h)
  if split:
   label(g,('底座模型','外围工程')[i],land[0],land[1]+76,31,col,finish*split)
def still(g,c,t,pivot,pub):
 clear=easepos(t,pub-.59,1.39)
 first=c.at('把底座模型')-.16
 u=enter(t,first,.64);settle=enter(t,c.at('钉在正中间')-.17,.55)
 attribution(g,c,t,pivot,first)
 x0=796;y0=mix(405,292,clear)
 pins=easepos(t,c.at('钉在正中间')-.21,.58)
 reduce=easepos(t,c.at('怎么检索文件')-.39,.84)
 size=1.35+.27*pins*(1-reduce)-.25*clear
 if u:chip(g,x0,y0,size,u,settle*(1-clear))
 if pins and reduce<1:
  stroke=2.7;vis=.93*pins*(1-reduce)
  for j in (-1,1):
   x=x0+154*j
   path(g,[(x+12*j,y0-35),(x,y0-35),(x,y0+33),(x+12*j,y0+33)],pins,O,stroke,vis)
 if t<pivot:return
 call=[c.at(q)-.13 for q in ('怎么检索文件','怎么调用终端','上下文快满了')]
 final=c.at('脚手架')
 arms=(((-144,-33),(-227,-70)),((139,-21),(220,-44)),((31,113),(54,185)))
 for j in range(3):
  by=YL[j];bx=XL[j];co=(O,G,V)[j]
  when=call[j];op=enter(t,when,.55)*(1-clear)
  if op<.004:continue
  xx,yy=transit((x0+arms[j][0][0],y0+arms[j][0][1]),(bx,by),easepos(t,when-.05,.64),-11+18*j)
  off=(143,-154,-165)[j]
  stub=(bx+off,by+19) if j<2 else (bx-8,by-95)
  ax,ay=arms[j][0]
  rail=[(x0+ax,y0+ay),(x0+arms[j][1][0],y0+arms[j][1][1]),stub]
  draw=easepos(t,when-.14,.71)
  path(g,rail,draw,co,2.1,op*.76)
  t1=when+.30;q=clip((t-t1)/.98)
  if 0<q<1 and draw>.22:
   r=ArcLength(rail);px,py=r.at(easepos(t,t1,.98));point(g,px,py,5.5,co,op)
  vis=easepos(t,when+.30,.71)
  if j==0:files(g,xx,yy,co,op,vis,when,t)
  elif j==1:terminal(g,xx,yy,co,op,vis,when,t)
  else:context(g,xx,yy,co,op,vis,when,t)
 m=enter(t,final-.17,.55)*(1-clear)
 if m:
  # The enclosing path is the scaffold. The model chip stays where it was pinned.
  pts=[(497,246),(663,206),(940,205),(1090,255),(1272,344),(1287,524),
       (1107,602),(862,605),(749,609),(553,553),(330,503),(316,325),(497,246)]
  path(g,pts,easepos(t,final-.21,1.11),Y,2.1,m*.89)
  mark(g,'Scaffold',997,170,42,t-final+.12,O,mode='pen',op=m)
  path(g,[(949,184),(893,206)],m,O,2.0,m)
  label(g,'外侧工具循环',1096,211,25,M,m)

def files(g,x,y,c,a,p,when,t):
 panel(g,x,y,270,190,c,a,p)
 label(g,MODULES[0],x-112,y-62,28,c,a,'left')
 line(g,(x-112,y-39),(x+111,y-39),M,1.15,a*.57)
 for j,name in enumerate(('sphinx/','ext/napoleon/','docstring.py')):
  v=enter(t,when+.07+j*.143,.41);left=x-114+18*j;cy=y-10+j*37
  path(g,[(left-7,cy-11),(left-7,cy),(left+3,cy)],v,c,1.4,v*a)
  mark(g,name,left+11,cy,25,t-when-.07-j*.143,F,'left',op=a*v,dur=.41)
 swish(g,x-69,x+69,y+83,t-when-.71,c,.47,2.1)
def terminal(g,x,y,c,a,p,when,t):
 panel(g,x,y,302,195,c,a,p)
 label(g,MODULES[1],x-125,y-64,28,c,a,'left')
 label(g,'$  pytest …',x-128,y-4,30,F,a*enter(t,when+.26,.54),'left')
 h=enter(t,when+.69,.55)
 for j in range(8):
  z=enter(t,when+.68+.058*j,.39);rect(g,x-122+j*24,y+61,14,7,c,a*z)
 check(g,x+108,y+63,10,True,h*a)
def context(g,x,y,c,a,p,when,t):
 panel(g,x,y+1,399,135,c,a,p)
 label(g,MODULES[2],x-176,y-43,27,c,a,'left')
 for j in range(18):
  u=enter(t,when+.13+.026*j,.34);fold=easepos(t,when+.89+.012*j,.51)
  xx=x-173+j*19.8+fold*(151-6*j)
  val=1-.88*fold if j<10 else 1
  rect(g,xx,y+12,14,15,c,a*u*val*.95)
  if j==10 and fold:
   box(g,xx-18,y-1,159,47,Y,a*fold,sw=1.8)

def forest(g,c,t,repo,p):
 if not p:return
 reach=c.at('以前读过');fresh=c.at('现场想出');leave=c.at('收走熟悉的')
 u=easepos(t,repo-.16,.90);vanish=easepos(t,leave-.21,1.01)
 gaze=enter(t,reach-.18,.46)
 for j,nm in enumerate(PASSING):
  offset,jy=j%4,j//4
  landing=(235+277*offset+(-14,20,55)[jy],300+112*jy)
  xx,yy=transit((852+102*cos(j*tau/12),458+99*sin(j*tau/12)),landing,u,25+4*j)
  lift=easepos(t,leave-.41+j*.045,.78);xx-=170*lift;yy-=180*lift
  v=enter(t,repo-.13+.046*j,.50)*p*(1-lift)
  if not v:continue
  co=(C,T,V,O)[(j+jy)%4]
  # A repository has a path and a short readable name; the decisive observable
  # is still the same lamp. Two causal possibilities stay separate above it.
  anchor=(xx-15,yy);dot(g,*anchor,4,co,v);path(g,[(xx-38,yy-14),(xx-38,yy+18),(xx-20,yy+18)],v,co,1.9,v)
  types=enter(t,repo+.45+.052*j,.54)
  label(g,nm,xx,yy,30,F,v*types,'left',224)
 for j,(word,co,at) in enumerate((('见过相近改法',V,reach),('现场想出',T,fresh))):
  v=enter(t,at-.15,.61)*p*(1-vanish);x=447+j*634
  if v:
   label(g,word,x,656,29,co,v)
   ss=[(x+10,692),(x+54*(1 if not j else -1),723),(782+26*j,723)]
   path(g,ss,easepos(t,at-.08,.71),co,2.4,v)
   ww=easepos(t,at+.23,.94)
   if 0<ww<1:
    r=ArcLength(ss);px,py=r.at(ww);point(g,px,py,6,co,v)
 if gaze and not vanish>=.999:check(g,798,723,15,True,gaze*(1-vanish))
 if vanish:
  # Bring three actual input grids into the cut; do not reveal the fourth result.
  from studio_tests import AR,arcboard
  for j,rec in enumerate(AR['train']):
   q=enter(t,leave+.07+.17*j,.48)
   if q:
    x=(465,799,1134)[j];y=(465,357,501)[j]
    arcboard(g,rec['input'],x+65*(1-q),y-30*(1-q),135+49*q,q)

def experiment(g,c,t,pub,repo):
 appear=enter(t,pub-.19,.60);retire=easepos(t,repo-.39,.79);roll=1-retire
 collect=c.at('底座同样');switch=c.at('不同配置');more=c.at('一百六十六道')
 diff=c.at('差了五十一道');observe=c.at('提议修改')
 if appear and roll:
  # The held-fixed chip and actual 500-task test set branch simultaneously,
  # then produce two counts on their own reading decks.
  a=appear*roll;cx,cy=796,292;to=(433,1157)
  grow=enter(t,collect-.24,.54);op=enter(t,c.at('同一套五百题')-.11,.54)
  label(g,'SWE-bench Verified',796,114,37,F,a*op)
  label(g,'同一组 500 题',796,165,26,M,a*op)
  for idx,(name,score,n,co) in enumerate(MEASURES):
   go=c.at('从百分之二十三' if idx==0 else '到百分之三十三点二')
   read=c.at('一百一十五道' if idx==0 else '一百六十六道')
   xx=to[idx];y=390+idx*42;lead=enter(t,switch-.19+idx*.095,.57)
   track=[(cx+(-93 if idx==0 else 93),cy-6),
          ((627,979)[idx],cy+33+idx*13),(xx,cy+33+idx*35),(xx,y-35)]
   spr=easepos(t,switch-.19+idx*.13,.85);path(g,track,spr,co,3.0,a*lead)
   if 0<spr<1:
    px,py=ArcLength(track).at(spr);point(g,px,py,5.8,co,a*lead)
   label(g,name,xx,y-22,37,co,lead*a)
   nopen=enter(t,go-.10,.58);force=easepos(t,go-.09,.96);count=n*force
   # Array is a counting grid, not a claim the solved tasks line up by identity.
   for ii in range(500):
    iy,ix=divmod(ii,25);wait=enter(t,pub-.11+idx*.12+(ix+iy)*.006,.41)
    bx=xx-208+ix*17.0;by=y+49+iy*7.8;p0=clip(count-ii)
    if wait and p0<.999:rect(g,bx,by,11.4,4.6,'#575C61',a*wait*.62)
    if p0:rect(g,bx,by,11.4*p0,4.6,co,a*(.78+.22*nopen))
   if nopen:
    mark(g,f'{score:.1f}%',xx+176,y+237,49,t-go+.06,co,align='right',mode='pen',op=nopen*a,dur=.58)
   g0=enter(t,read-.13,.53)
   if g0:label(g,f'{n} / 500',xx-200,y+237,31,F,a*g0,'left')
  w=enter(t,diff-.16,.66)
  if w:
   x=800;y=730
   toks=[('166',T,-143),('−',F,-82),('115',C,-24),('=',F,47),('51',Y,114)]
   for j,(txt,co,dx) in enumerate(toks):mark(g,txt,x+dx,y,40,t-diff+.16-.063*j,co,mode='pen',op=w*a,dur=.39)
   if t>diff+.50:swish(g,887,944,761,t-diff-.49,Y,.53,2.65)
  if grow:line(g,(731,246),(861,246),CORE,1.55,a*grow)
  q=enter(t,observe-.15,.55)
  if q:
   for k,x in enumerate(to):
    phase0=enter(t,observe+.14*k,.79);h=359+k*40
    ring(g,x,h,15+17*phase0,(C,T)[k],q*(1-phase0)*a,2.1)
 if retire:forest(g,c,t,repo,retire)
def logic(g,c,pivot,pub,repo):
 t=c.t
 if t<pub+.80:
  still(g,c,t,pivot,pub)
 elif t<repo+.41:
  chip(g,796,292,1.1,1-easepos(t,repo-.44,.86))
 if t>pub-.21:experiment(g,c,t,pub,repo)
