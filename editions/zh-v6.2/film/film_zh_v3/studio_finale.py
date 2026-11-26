"""Fold the actual instruments back into one revolving chain; keep their units separate."""
from ink import *
from motion import transit,out3
from timeline3 import W,OLD,S,B,remap
from studio_examples import silk,pstep,area,BLUE,VIO
from studio_votes import wedge
from studio_tests import arcboard,AR
from studio_exam import crystal
from finale import mini,reprise_case
from score_paloma import P
from domains import PROB
LABELS=('取舍','词元概率','考卷','偏好','行动','推理与安全','效度与污染')
def specimen(g,i,t,r,op=1):
 # All specimens live in a single aperture. Each caption names the operation, not a second title.
 ctx=g.c;ctx.save();ctx.translate(800,460);p=clip(r);co=(C,T,Y,V,G,O,R)[min(i,6)]
 if i==0:
  data=[(-182,34),(-109,34),(-109,6),(-17,6),(-17,-27),(89,-27),(89,-59),(176,-59)]
  path(g,data,1,O,3.4,op)
  for j,(a,b)in enumerate(data[::2]):dot(g,a,b,7,C,op)
  xx=mix(-150,148,p);line(g,(xx,-79),(xx,55),R,2.0,op);txt(g,'加上预算，再选点',0,99,25,M,op)
 elif i==1:
  d=reprise_case();vals=d['models'][0]['nll'];target=d['answer_index']
  for j,v in enumerate(vals):
   x=-179+j*24;cc=R if j==target else C;y=47
   rect(g,x,y-9*v,14,9*v,cc,op*(.95 if j==target else .70))
  line(g,(-186,54),(193,54),M,1.4,op);txt(g,'决定对错的那一步',0,101,25,M,op)
 elif i==2:
  for j in range(2):
   x=(j-.5)*214;pair=P['domains'][j]['values'];txt(g,('Python','数学')[j],x,-56,27,F,op)
   for k,v in enumerate(pair):
    xx=x+(k-.5)*92;co=(C,V)[k];txt(g,f'{v:.2f}',xx,7,29,co,op)
    if v==min(pair):line(g,(xx-30,36),(xx+30,36),T,2.6,op)
  txt(g,'按语料，分开读',0,99,25,M,op)
 elif i==3:
  x=-164
  for z,col in zip(PROB,(O,C,T,V)):
   dx=328*z;rect(g,x,-21,dx-3,45,col,op);x+=dx
  txt(g,'Σ p = 1',0,84,34,T,op)
 elif i==4:
  for j in range(10):
   x=-162+(j%5)*67;y=-58+(j//5)*52;rect(g,x,y,51,43,O if j==2 else '#1C758A',op);txt(g,'ABCDEFGHIJ'[j],x+25,y+21,23,F,op)
  txt(g,'4 项   →   最多 10 项',0,99,26,M,op)
 elif i==5:
  crystal(g,0,0,69,T,op,.25+.50*p)
  for side,lab in [(-1,'同行复核'),(1,'外行搜索')]:txt(g,lab,side*155,4,23,M,op)
  txt(g,'GPQA Diamond',0,101,26,F,op)
 elif i==6:
  for j in range(100):
   x=-170+(j%20)*17.9;y=-42+(j//20)*18.6;dot(g,x,y,4.4,Y,op)
  txt(g,'一点 = 25 道公开题',0,100,25,M,op)
 elif i==7:
  pr=1/(1+10**(-p));z=-pi/2+tau*pr;wedge(g,-78,-3,67,-pi/2,z,BLUE,op);wedge(g,-78,-3,67,z,1.5*pi,VIO,op)
  txt(g,f'{100*pr:.1f}%',90,-1,38,C,op);txt(g,'从分差读胜率',0,102,25,M,op)
 elif i==8:
  path(g,[(-163,41),(0,1),(163,-34)],1,T,3,op);xx=mix(150,0,p);line(g,(0,60),(0,-60),M,1.3,op);dot(g,xx,-.225*xx+1,8,Y,op);txt(g,'令长度差等于零',0,99,26,M,op)
 elif i==9:
  txt(g,'+  _format_docutils_params(…)',0,-46,26,G,op,font='DejaVu Sans Mono')
  for j in range(45):
   xx=-169+(j%15)*24;yy=14+(j//15)*15;rect(g,xx,yy,13,8,T,op*(.4+.6*clip(p*3-j*.038)))
  txt(g,'修好 1 项，守住 45 项',0,101,26,M,op)
 elif i==10:
  d=AR['test'][0];arcboard(g,d['input'],-100,0,100,op);arcboard(g,d['output'],100,0,100,op,open_=p)
  arrow(g,(-35,0),(35,0),1,C,op,2.5);txt(g,'把规则用到新图',0,101,25,M,op)
 elif i==11:
  for j in range(3):
   y=-44+j*41;path(g,[(-160,y),(-83,y),(-4,-y*.5+8),(83,y*.69),(160,y*.69)],1,Y,2.9,op);dot(g,-160,y,4.8,C,op);dot(g,160,y*.69,4.8,T,op)
  txt(g,'追同一道题的两次行为',0,99,25,M,op)
 else:
  for j,ch in enumerate('it takes three hours to prepare a project and two to present it'.split()):
   y=-48+(j//7)*62;x=-204+(j%7)*60;txt(g,ch,x,y,19,C,op)
  xx=mix(-234,-92,p);box(g,xx,-76,218,47,Y,op,inkcol(Y,.12),2.2)
  txt(g,'回原文核对重合片段',0,99,25,M,op)
 ctx.restore()
def orbit(g,c):
 t=c.t;beats=('整条脉络','困惑度','标准化考卷','开放对话','一行补丁','网格里的规则','查考题')
 details=('整条脉络','困惑度','哪类文章','沙箱里复算','标准化考卷','GPQA','HLE','开放对话','校正裁判','一行补丁','网格里的规则','读完整份回答','查考题')
 marks=[c.at(x)for x in details];trs=[c.at(x)for x in beats];closing=phase(t,c.d-1.48,c.d-.56);reveal=phase(t,.75,1.55);center=phase(t,marks[0]-.4,marks[0]+.21)*(1-closing)
 oldstop=B['8-1']['duration']-1/60;theta=.055*sin((t+(oldstop-c.d)*phase(t,c.d-4,c.d-.38))*.097)
 cy=mix(412,472,closing);rx=mix(588,480,closing);ry=mix(248,178,closing);tilt=mix(-.115,0,closing)
 def pos(an,dx=0,dy=0):
  x=(rx+dx)*cos(an);y=(ry+dy)*sin(an);return(800+x*cos(tilt)-y*sin(tilt),cy+y*cos(tilt)+x*sin(tilt))
 pts=[pos(-pi/2+j*tau/224)for j in range(225)];path(g,pts,1,E,1.9,.82)
 u=sum(phase(t,mrk-.48,mrk+.20)for mrk in trs[1:]);trace=1-closing
 ang=-pi/2+tau*u/7+theta
 if .002<trace:dot(g,*pos(ang),8.2,Y,trace)
 for j,nm in enumerate(LABELS):
  an=-pi/2+tau*j/7+theta;x,y=pos(an);focus=clip(1-abs(u-j));f=.55+.45*focus
  alpha=mix(f,.85 if j<6 else 1,closing);g.circle(x,y,43,BLACK)
  mini(g,j,x,y,mix(1.15+.25*focus,1.03,closing),t,alpha)
  vx,vy=x-800,y-cy
  if abs(vx)>300:
   a1=x+(58 if vx>0 else -58);a2=y+(16 if vy>0 else -17)
   txt(g,nm,a1,a2,27,seq[j],alpha*(1-closing),('left' if vx>0 else 'right'))
  else:
   txt(g,nm,x,y+(64 if vy>0 else -62),27,seq[j],alpha*(1-closing))
  if focus>.06 and trace>.01:arc(g,x,y,48,-.87*pi,.65*pi,Y,2.6,trace*focus*.88)
 if center:
  for j,when in enumerate(marks):
   e=marks[j+1]if j+1<len(marks)else c.d;z=phase(t,when-.31,when+.28);end=phase(t,e-.49,e-.16)
   lum=phase(t,when-.30,when+.048)*(1-end)*center
   if not lum:continue
   r=phase(t,when-.17,min(e-.37,when+1.65))
   cj=(0,1,1,1,2,2,2,3,3,4,5,5,6)[j]
   pt=pos(-pi/2+cj*tau/7+theta);v=z*(1-.23*end);xc,yc=lerp(pt,(797,391),v);yc-=24*sin(pi*v)
   sc=mix(.38,(1.54 if j in(1,4,12)else 1.68),v)
   ctx=g.c;ctx.save();ctx.translate(xc,yc);ctx.scale(sc,sc);ctx.translate(-800,-460)
   specimen(g,j,t,r,lum);ctx.restore()
 # On the last revolution the opening capability solid itself comes back. The very next
 # shot uses the exact same projection, target, camera and physical size.
 seed=phase(t,c.d-1.20,c.d-.27)
 if seed:
  import opening
  tar=opening.O;dx,dy,dz=opening.coords(0,opening.GOOD);tg=(tar[0]+dx/2,tar[1]+dy/2,tar[2]-dz/2)
  w=World(g,yaw=-.62,pitch=.21,zoom=mix(.48,.63,seed),target=tg,center=(800,mix(420,405,seed)))
  opening.outer(w,opening.GOOD,C,0,0,seed);w.draw()
