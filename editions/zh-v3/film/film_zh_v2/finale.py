from ink import *
from machines import grid,ARC
import opening
def mini(g,i,x,y,s,t,op=1):
 col=(C,T,Y,V,G,O,R)[i]
 if i==0:
  pts=[(x-38*s,y+22*s),(x-10*s,y+22*s),(x-10*s,y),(x+14*s,y),(x+14*s,y-17*s),(x+37*s,y-17*s)]
  path(g,pts,1,Y,2.8*s,op)
  for j in [0,2,4]:dot(g,*pts[j],3.4*s,C,op)
 elif i==1:
  for j,h in enumerate((18,37,52,24,32,12,26)):
   rect(g,x+(j-3)*10*s,y+(25-h)*s,6*s,h*s,Y if j==2 else C,op)
 elif i==2:
  for j in range(10):box(g,x-41*s+(j%5)*17*s,y-18*s+(j//5)*19*s,13*s,15*s,Y if j==2 else C,op,sw=1.4*s)
 elif i==3:
  xs=[(x-43*s+j*2.7*s,y+(1/(1+exp((j-16)*.25))-.5)*49*s) for j in range(32)]
  path(g,xs,1,V,2.7*s,op);dot(g,x,y,4.6*s,Y,op)
 elif i==4:
  for j in range(10):dot(g,x+(j%5-2)*13*s,y+(j//5-.5)*18*s,4.3*s,G if j>1 else O,op)
 elif i==5:grid(g,ARC['test'][0]['input'],x,y,65*s,1,op)
 else:
  for j in range(8):line(g,(x+(-3.5+j)*11*s,y-10*s),(x+(-3.5+j)*11*s,y+12*s),C,2.2*s,op)
  box(g,x-17*s,y-19*s,44*s,43*s,Y,op,sw=2*s)
def orbit(g,c):
 t=c.t;dur=c.d
 triggers=['整条脉络','困惑度','标准化考卷','开放对话','Docker','纯网格','生态效度']
 names=['取舍','词元概率','考卷','偏好','行动','推理与安全','效度与污染']
 cx,cy=800,472
 title(g,'一把尺，看见一种东西',105,sub='每换一次评测，把上一次看不见的东西加进来')
 pts=[]
 for j in range(201):
  a=-pi/2+j*tau/200;pts.append((cx+480*cos(a),cy+178*sin(a)))
 path(g,pts,1,E,1.6,.82)
 for j in range(7):
  a=-pi/2+tau*j/7+.055*sin(t*.097);xx=cx+480*cos(a);yy=cy+178*sin(a)
  k=on(c,triggers[j],1.45)
  next_topic=on(c,triggers[j+1],1.24) if j<6 else 0.
  gather=phase(t,c.at('数据污染')+.35,dur-.26)
  ink=.27+.25*k+.48*k*(1-next_topic)+.33*k*next_topic*gather
  # Black eclipses preserve contrast at an orbit crossing.
  g.circle(xx,yy,44,BLACK)
  mini(g,j,xx,yy,.78+.25*k,t,ink)
  xx2=cx+581*cos(a);yy2=cy+249*sin(a);txt(g,names[j],xx2,yy2,27,seq[j],ink)
  if k>.01 and k<.998:ring(g,xx,yy,36+14*k,Y,sin(pi*k),1.8)
 # These three questions require different measurements. Use the very same
 # token losses, Paloma columns and normalised probabilities seen in Beat 2.
 from motion import guide
 from domains import PROB
 from score_paloma import P
 token=c.at('困惑度');error=c.at('决定对错');domain=c.at('哪类文章');pal=c.at('Paloma')
 inspect=c.at('交上来的分数');seal=c.at('沙箱里复算');next_=c.at('标准化考卷')
 inside=phase(t,token-.44,token+.35)*(1-phase(t,next_-.29,next_+.39))
 txt(g,'模型评测',cx,mix(cy,375,inside),45,blend(F,M,inside*.20),1)
 if inside:
  case=reprise_case();vals=case['models'][0]['nll'];last_token=case['answer_index']
  rail=phase(t,token-.25,token+.52)*(1-phase(t,domain-.43,domain-.13))
  if rail:
   bottom=524;line(g,(611,bottom),(991,bottom),E,1.3,rail)
   for i,v in enumerate(vals):
    x=629+i*24;begin=phase(t,token-.20+i*.035,token+.37+i*.035)
    red=phase(t,error-.22,error+.40) if i==last_token else 0.
    rect(g,x-6,bottom-8.0*v*begin,12,8.0*v*begin,blend(C,R,red),rail*.94)
    if red:check(g,x,bottom+25,7,False,rail*red)
  columns=phase(t,domain-.09,domain+.47)*(1-phase(t,inspect-.42,inspect-.08))
  if columns:
   for j,(x,txt_,col) in enumerate(((700,'Python',C),(903,'数学',V))):
    a=phase(t,domain-.07+j*.26,domain+.57+j*.26)*columns
    txt(g,txt_,x,438,24,M,a)
    A,B=P['domains'][j]['values'];v1=x-40;v2=x+40
    txt(g,f'{A:.2f}',v1,497,27,C,a);txt(g,f'{B:.2f}',v2,497,27,V,a)
    v=v1 if A<B else v2;u=phase(t,pal-.38+j*.22,pal+.35+j*.22)
    line(g,(v-20,523),(v-20+40*u,523),T,2.8,a*u)
  audit=phase(t,inspect-.02,inspect+.56)*inside
  if audit:
   xx=641;dx=204
   for j,(z,col) in enumerate(zip(PROB,(O,C,T,V))):
    v=phase(t,inspect+.10+j*.12,inspect+.73+j*.12);rect(g,xx,474,dx*z*v,18,col,audit*v);xx+=dx*z
   done=phase(t,seal-.22,seal+.38)
   txt(g,'Σ p = 1',921,481,30,T,audit*done)
   if done:check(g,983,481,8,True,audit*done)
   if 0<done<1:guide(g,[(637,510),(846,510),(860,497)],done,T,audit,2.0,.4)
@lru_cache(None)
def reprise_case():return json.loads((W/'art2/data/tradeoff_case.json').read_text())
def return_home(g,c):
 t=c.t;d=c.d;make=on(c,'终极考卷',2.2);multi=on(c,'多量几个方向',2.35,early=.16);last=on(c,'第一步',1.7);fade=phase(t,d-.50,d-.04)
 allalpha=1-.13*fade
 if allalpha>.001:
  center=(800,405);tar=opening.O
  dd=opening.coords(0,opening.GOOD)
  target=(tar[0]+dd[0]/2,tar[1]+dd[1]/2,tar[2]-dd[2]/2)
  tc=min(t,d-2.15);ww=World(g,yaw=-.62+.20*sin(tc*.13),pitch=.21+.12*sin(tc*.10),zoom=.63+.10*multi,target=target,center=center)
  # Move the camera INSIDE the exact orbit left by 8-1. Its seven instruments retain
  # their identity and drift out of view, rather than adding together into a misleading score.
  if t<2.66:
   from direct import state
   from wetjoins import crop
   stop=state('8-1')[0]['duration']-1/60;push=phase(t,.08,2.47)
   cy=mix(472,405,push);rx=480*(1+1.40*push);ry=178*(1+1.40*push)
   fade_type=1-phase(t,0,.66);rail=1-phase(t,.51,2.02)
   title(g,'一把尺，看见一种东西',105,fade_type,sub='每换一次评测，把上一次看不见的东西加进来')
   txt(g,'模型评测',800,cy,45,F,1-phase(t,.04,.58))
   def tools_on_orbit():
    if rail:
     pts=[(800+rx*cos(-pi/2+j*tau/160),cy+ry*sin(-pi/2+j*tau/160))for j in range(161)];path(g,pts,1,E,1.6,rail*.82)
    for j,nm in enumerate(('取舍','词元概率','考卷','偏好','行动','推理与安全','效度与污染')):
     an=-pi/2+tau*j/7+.055*sin((stop+min(t,1.86))*.097)
     x=800+rx*cos(an);y=cy+ry*sin(an)
     z=1-phase(t,.50+j*.04,1.88+j*.08);op=(.85 if j<6 else 1)*z
     if not op:continue
     k=1+.24*push;g.circle(x,y,44*k,BLACK);mini(g,j,x,y,1.03*k,t,op)
     xt=800+581*(1+1.40*push)*cos(an);yt=cy+249*(1+1.40*push)*sin(an)
     txt(g,nm,xt,yt,27,seq[j],op*fade_type)
   crop(g,0,184,1600,573,tools_on_orbit)
  opacity=phase(t,.39,2.66)*allalpha
  cnear,cfar=opening.outer(ww,opening.GOOD,C,t,0,opacity)
  # First show the exact 82/100 shadow from the opening. The ruler belongs to
  # the same camera as the body; turning the camera cannot change its reading.
  from cut_common import vlerp
  ink=phase(t,.85,3.6)*allalpha;dock=phase(multi,.12,.93);single=ink*(1-dock)
  if ink:
   x0=tar[0];ry=tar[1]+mix(-.78,-.24,dock);rz=tar[2]+mix(.30,.065,dock)
   aa=(x0,ry,rz);bb=(x0+opening.LX,ry,rz);point=vlerp(aa,bb,.82)
   # The 82-point measurement stays under the same physical edge as the rest
   # of the scale retracts. The six new directions do not replace the evidence.
   ww.segment(aa,point,Y,mix(2.25,1.5,dock),ink*mix(.91,.69,dock))
   ww.segment(point,bb,Y,2.25,single*.91)
   for h in range(11):
    xx=x0+opening.LX*h/10;hi=.12 if h in (0,5,10) else .07
    ww.segment((xx,ry-hi,rz),(xx,ry+hi,rz),Y,1.45,single*.86)
    if h in (0,10):ww.text(str(h*10),(xx,ry-.27,rz),22,M,single,font=SERIF)
   ww.path((cnear,(point[0],ry,cnear[2]),point),Y,1.8,single*.8,dash=[5,5])
   if dock:
    for xx in (x0,point[0]):ww.segment((xx,ry-.065,rz),(xx,ry+.065,rz),Y,1.65,ink*dock*.79)
   ww.dot(point,Y,mix(.066,.048,dock),ink)
   lx=mix(point[0],x0+opening.LX*.072,phase(multi,.015,.56))
   ww.text('基准 82 分',(lx,ry-mix(.59,.40,dock),rz),32,Y,ink,font=SERIF)
  y0,p0=-.62,.23
  right=(cos(y0),0,-sin(y0));up=(-sin(y0)*sin(p0),cos(p0),-cos(y0)*sin(p0));front=(sin(y0)*cos(p0),sin(p0),cos(y0)*cos(p0))
  labels=[]
  for j,lab in enumerate(['概率','推理','行动','安全','生态效度','防污染']):
   a=-pi/2+tau*j/6
   dr=4.72*cos(a);du=-2.78*sin(a);df=1.37*sin(2*a+.43)
   end=tuple(target[h]+dr*right[h]+du*up[h]+df*front[h] for h in range(3))
   k=phase(multi,j*.04,.75+j*.04);op=k*allalpha
   if op:
    foot=vlerp(target,end,.36);tip=vlerp(foot,end,k)
    ww.segment(foot,tip,seq[j],1.9,op*.85);ww.dot(tip,seq[j],.066,op)
    # Register two graduations on each ray to read them as measurements, not a halo.
    for h in (.72,.86):
     cp=vlerp(target,tip,h);dxyz=tuple(.058*(-sin(a)*right[m]-cos(a)*up[m]) for m in range(3))
     ww.segment(tuple(cp[m]-dxyz[m] for m in range(3)),tuple(cp[m]+dxyz[m] for m in range(3)),seq[j],1.45,op*.87)
    xp,yp=ww.pos(end);labels.append((lab,800+(xp-800)*1.20,405+(yp-405)*1.18,seq[j],op))
  ww.draw()
  for lab,x2,y2,col,op in labels:
   if lab=='安全':
    xp,yp=x2,y2-20;xe,ye=x2+76,min(y2-10,673);line(g,(xp+5,yp),(xe-17,ye),col,1.4,op);txt(g,lab,xe,ye,30,col,op,'left')
   else:txt(g,lab,x2,y2,31,col,op)
  txt(g,'从单一投影，到多维测量',800,737,31,M,allalpha*phase(t,1.12,2.16))
