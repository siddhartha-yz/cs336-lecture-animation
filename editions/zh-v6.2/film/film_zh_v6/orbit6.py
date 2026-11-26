"""A single travelling line, the same seven instruments, and the two boxes it resolves into."""
from rig4 import *
from motion6 import ArcLength
from motion import curtain
from finale import mini
from machines import ARC,grid
from studio_field import reel
from v4_act4 import MAT
from v4_act2 import REV

TOOLS=('取舍','词元概率','考卷','偏好','行动','推理与安全','效度与污染')
PAL=(Y,C,T,V,G,O,R)
CUES=('换尺子','一段话预料','移到答案','一票交给读者','补丁','第四张','训练时间')
BEATS=('换尺子','一段话预料','移到答案','一列考分','困难的新题','邮件有好几种写法',
       '怕裁判偏爱','代码能不能用','第四张','整份回答','工作现场','训练时间')

@lru_cache(1)
def rail():
 # True screen-space distance, rather than constant angular velocity on an ellipse.
 return ArcLength((800+646*cos(a)+44*sin(a),426+285*sin(a))for a in (-2.21+tau*i/448 for i in range(449)))
def travel(c,t):
 a=c.at('换尺子');b=c.at('训练时间')+.15;k=.036
 u=clip((t-a)/(b-a))
 def up(p):
  v=p/k
  return k*v**3*(1-.5*v)
 distance=up(u) if u<k else 1-k-up(1-u) if u>1-k else u-.5*k
 return distance*.886/(1-k)
def gate(t,at,stop,d=.53):
 # Slight lead on concrete objects. The outgoing labelled asset finishes clearing
 # before the first new glyph appears in the same aperture.
 return phase(t,at-.16,at+d)*(1-phase(t,stop-.30,stop+.02))
def fret(g,pts,col,h,sw=2.4):
 if h>.001:path(g,pts,1,col,sw,h)

def budget(g,c,st,en,op):
 t=c.t;z=easepos(t,st-.12,.68)
 xv=(481,583,707,837,970,1108);ys=(519,477,429,407,365,329);edge=[]
 for j,(x,y)in enumerate(zip(xv,ys)):
  if j:edge.append((x,ys[j-1]))
  edge.append((x,y))
 path(g,edge,z,O,4.1,op)
 for i,(x,y)in enumerate(zip(xv,ys)):
  q=enter(t,st-.17+.083*i,.48);point(g,x,y,7.5,C,op*q)
 fl=phase(t,c.at('眼前出了件怪事')-.22,en-.42)
 xp=mix(1131,792,fl);v=phase(t,st+.21,st+.89)
 if v:
  for j in range(15):
   y=305+j*17.8;line(g,(xp,y),(xp,y+10.2),R,2.0,op*v*.91)
  plev=1-phase(t,en-.45,en-.01)
  label(g,'预算',xp,599,31,R,op*plev)
  k=sum(x<=xp for x in xv)-1
  if k>=0:ring(g,xv[k],ys[k],17.0,Y,op*v,2.8)

def wholeline(g,c,st,en,op):
 t=c.t;model=REV['models'][0];vv=model['nll'];key=REV['answer_index'];word=REV['tokens'][key].strip()
 wrong=model['top'][0]['token'].strip();assert wrong!=word
 last=c.at('最后一个数');at=c.at('算错')
 narrow=easepos(t,en-.74,.74);f=phase(t,last-.17,at+.32)
 bx=525;step=39.8;x0=bx+key*step
 for j,(token,val) in enumerate(zip(REV['tokens'],vv)):
  u=enter(t,st-.20+.037*j,.46);x=bx+step*j
  y=504;h=val*17.8*u;col=blend(C,Y,f) if j==key else C
  x=mix(x,688 if j==key else 749+3*j,narrow);w=mix(26,83 if j==key else 2,narrow)
  a1=op*u*(1-.84*f)*(1-narrow) if j<key else op*u
  rect(g,x-w/2,y-h,w,h,col,a1*(1-narrow if j==key else 1))
  if j in (3,5,key):
   if j==key:label(g,word,x,mix(y+37,434,narrow),mix(32,49,narrow),col,a1)
   else:label(g,token.strip(),x,y+35,22,col,a1)
 if f:
  x=mix(1082,926,narrow);y=mix(384,434,narrow)
  mark(g,wrong,x,y,mix(37,49,narrow),t-last+.19,R,op=f*op)
  q=enter(t,at-.22,.40);yy=y+40
  if q:
   path(g,[(x-9,yy-9),(x+9,yy+9)],q,R,3.3,op);path(g,[(x-9,yy+9),(x+9,yy-9)],q,R,3.3,op)
  if narrow<.94:label(g,'模型首选',x,y-46,25,R,op*f*(1-narrow))
 fret(g,[(492,504),(x0+32,504)],M,op*(1-narrow)*.68,1.7)
def answer(g,c,st,en,op):
 # Preserve the two candidates as the teacher-forced prefix falls away.
 t=c.t;z=easepos(t,st-.04,.68)
 w=mix(74,399,z);co=T
 path(g,[(803-w/2,485),(803-w/2,520),(803+w/2,520),(803+w/2,485)],z,co,3.0,op)
 label(g,'9 − 7',803,317,43,F,op*enter(t,st+.03,.43))
 for j,(s,co,tick)in enumerate((('two',Y,'✓'),('three',R,'×'))):
  x=(688,926)[j];a=op
  label(g,s,x,434,49,co,a);label(g,tick,x,478,27,co,a*enter(t,st+.07,.34) if j==0 else a)
def scores(g,c,st,en,op):
 t=c.t;z=easepos(t,st-.16,.57);take=easepos(t,en-.56,.62)
 for j,(lab,s,co) in enumerate((('GPT-4',84.7,C),('GPT-4o',88.7,T),('GPT-4.1',90.2,V))):
  x=604+207*j;co2=blend(co,O,take)
  yy=575.;h=s*2.83*enter(t,st-.16+.061*j,.54)
  rect(g,x-66,yy-h,132,h,co2,op*.88)
  if z>.55:label(g,f'{s:.1f}%',x,yy-h+38,31,'#101010',op*phase(z,.55,1))
  if z>.55:label(g,lab,x,yy+43,25,co,op*phase(z,.55,1))
 fret(g,[(505,292),(1095,292)],F,op*.59,1.75)
def dense(g,c,st,en,op):
 t=c.t;z=easepos(t,st-.28,1.32)
 # A field of retained questions, after the funnel already established its scale.
 # Each visible grain is a compositional sample of the pool, not a count.
 for j in range(246):
  u=(j*31)%169/168.;v=(j*107)%193/192.;a=2*pi*(j*.27639320225%1);r=.17+.83*sqrt(u)
  step=phase(t,st-.26+(j%29)*.008,st+.45+(j%29)*.014)
  rad=490-125*z;x=810+cos(a)*r*rad*(.83+.22*v);y=408+sin(a)*r*165*(.68+.26*u)-22*cos(a)*z
  col=blend(T,Y,.36+.64*u)
  dot(g,x,y,2.15+2.05*v,col,op*step*(.76+.24*v))
 label(g,'HLE',800,638,35,Y,op)

def slips(g,c,st,en,op):
 t=c.t;z=easepos(t,c.at('一票交给读者')-.11,.67)
 # Type sits on two physical lines, not a pair of labelled slide panels.
 for j,co in enumerate((C,V)):
  x0=(468,539)[j];y=(360,491)[j]
  x=mix(x0,535+137*j,z);yy=mix(y,422+32*j, .20*z)
  a=op*enter(t,st-.13+.13*j,.47);w=(586,524)[j]
  s=(MAT['A'][0],MAT['B'][0])[j]
  line(g,(x,yy+35),(x+w,yy+35),co,2.2,a*.86)
  mark(g,s,x,yy,34,t-st+.13-.13*j,F,'left',op=a,dur=.46)
 v=enter(t,c.at('一票交给读者')-.20,.47)
 if v:
  x,y=transit((1105,449),(856,613),z,-51);point(g,x,y,9.4,Y,op*v)
  path(g,[(1105,449),(1105,504),(856,613)],z,Y,2.15,op*.56*v)
def delta(g,c,st,en,op):
 t=c.t;z=easepos(t,st-.13,.66);w=easepos(t,c.at('拨回零')-.24,.71)
 xs=[(508+j*9.8,448-88*math.tanh((j-28)/18.))for j in range(60)]
 path(g,xs,z,T,3.5,op)
 fret(g,[(801,327),(801,581)],F,op*.50,1.6)
 x=mix(1008,801,w);y=448-88*math.tanh(((x-508)/9.8-28)/18)
 point(g,x,y,11.3,Y,op*z);label(g,'长度差  0',801,613,27,T,op*w)
def patch(g,c,st,en,op):
 t=c.t
 action=c.at('补丁')
 g0=enter(t,st-.08,.48)
 label(g,'运行同一套测试',799,335,30,G,op*g0*(1-phase(t,action-.31,action+.05)))
 mark(g,'+ _format_docutils_params(…)',801,310,33,t-action+.08,G,mode='pen',dur=.51,op=op)
 # Tests keep their place before the result can turn green. The last few hold for the eyeblink.
 for j in range(45):
  q=enter(t,action-.08+.023*j,.47);x=481+j%15*42.1;y=423+j//15*37;co=blend(O,G,q)
  rect(g,x-11,y-10,19+2*q,20,co,op*q*(.68+.24*(j>=1)))
 label(g,'通过测试',803,616,30,G,op*enter(t,action+.89,.49))
def shape(g,c,st,en,op):
 t=c.t;z=easepos(t,st+.02,.58)
 r=ARC['test'][0];sz=162;grid(g,r['input'],666,423,sz,1,op)
 path(g,[(780,423),(843,423)],z,C,2.7,op)
 grid(g,r['output'],960,423,sz,z,op)
def whole_reply(g,c,st,en,op):
 t=c.t;z=easepos(t,st-.20,.67)
 mark(g,'这个忙我帮不了。',801,321,41,t-st+.22,F,mode='wave',op=op)
 for j,co in enumerate((T,R)):
  x=632+j*339;y=515;u=enter(t,st+.10+.17*j,.52)
  path(g,[(803,373),(803,419),(x,461),(x,501)],z,co,2.6,op*u)
  ring(g,x,y,25,co,op*u,2.5);label(g,('✓','×')[j],x,y,28,co,op*u)
  label(g,('安全替代','实质有害')[j],x,598,27,co,op*u)
def shop(g,c,st,en,op):
 t=c.t;z=easepos(t,st-.25,.73)
 shot=AS/'gdp-delivery.png';x=mix(590,632,z);y=mix(459,421,z)
 photo(g,shot,x,y,499,tilt=-.11+.078*z,op=op)
 reel(g,1067,430,.91,.63+.61*z,op*enter(t,st+.06,.51))
 fret(g,[(872,477),(910,477),(943,436)],O,op*.74)
def overlap(g,c,st,en,op):
 t=c.t;z=easepos(t,st-.10,.88)
 times=(('训练材料',V),('有时间戳的题库',T));u=phase(t,st+.69,st+1.25)
 for j,(lab,co) in enumerate(times):
  y=(377,514)[j];x0=(523,565)[j]
  label(g,lab,x0,y-67,26,co,op,'left')
  for i in range(20):
   p=enter(t,st-.10+j*.09+i*.031,.40);x=x0+i*26
   rect(g,x,y,20,24,blend(co,Y,u if 6<=i<=10 else 0),op*p*.65)
 rx=mix(483,523+26*6-5,z)
 box(g,rx,368,140,178,Y,op*phase(t,st-.16,st+.36),inkcol(Y,.11),2.55)
 label(g,'核对重合',865,614,28,T,op*u)
APP=(budget,wholeline,answer,scores,dense,slips,delta,patch,shape,whole_reply,shop,overlap)

def recap(g,c):
 t=c.t;r=rail();marks=[c.at(z)for z in BEATS]
 seal=c.d-1.57;gather=c.at('每一次进化')+.12
 u=travel(c,t)
 w=easepos(t,gather,seal-gather);seed=easepos(t,seal,.92);ink=1-seed
 # Two distinct stations end up close by on this path because the words do:
 # the light traverses equal distance in equal time, even on the long sides.
 linepop=easepos(t,-.18,1.26)
 if ink:
  path(g,r.xy,1,M,1.73,ink*linepop*.34)
  if u:
   steps=174;front=[r.at(j*u/steps)for j in range(steps+1)]
   path(g,front,1,T,1.75,linepop*ink*.68)
   head=[r.at(mix(max(0,u-.056),u,j/42))for j in range(43)]
   path(g,head,1,Y,3.0,linepop*ink*.89)
  for i,(lab,phrase) in enumerate(zip(TOOLS,CUES)):
   v=travel(c,c.at(phrase));x,y=r.at(v);shine=math.exp(-((v-u)/.045)**2)
   p=enter(t,.07+i*.093,.42)*ink
   x,y=lerp((x,y),(800,425),w*.32*(1-(i+1)*.044))
   if p:
    # A small pupil cuts the orbit behind each object. Its short name moves
    # as part of the same instrument, not a different layer with fresh coordinates.
    g.circle(x,y,29+7*shine,BLACK,alpha=.88*p)
    mini(g,i,x,y,.83+.21*shine+.09*w,t,p*(.53+.47*shine))
    ox=(x-800);oy=y-426
    px=x+40*ox/650;py=y+(33 if oy>25 else -33 if oy<-25 else (-26 if i in (1,5) else 37))
    if px>1364:align='right';px=x-48
    elif px<190:align='left';px=x+47
    else:align='center'
    label(g,lab,px,py,26 if i>=5 else 28,PAL[i],p*(.59+.41*shine)*(1-.87*w),align)
  # The measuring head stays above the station's black cutout. A station
  # can light up under it, but never interrupts the motion of the head.
  if u:
   x,y=r.at(u)
   g.circle(x,y,8.8,BLACK,alpha=.93*ink*linepop)
   point(g,x,y,6.7,Y,linepop*ink)
 if t>marks[0]-.24 and t<seal:
  for idx,(f,st,en) in enumerate(zip(APP,marks,marks[1:]+[gather+.16])):
   a=gate(t,st,en,d=.40 if en-st<2.2 else .56)*(1-.91*w)
   if idx==1:
    if t>=en:continue
    a=phase(t,st-.16,st+.47)
   if idx==2:
    if t<st:continue
    a=1-phase(t,en-.30,en+.02)
   if a<.005:continue
   q=easepos(t,st-.20,.64);z=1-easepos(t,en-.39,.43);h=q*z
   # A measured push on the object, preserving one typographic outline. In 
   # transitions glyphs just retire in their own place; plot objects do the flying.
   ctx=g.c;ctx.save();ctx.translate(800,426);ctx.scale(.960+.047*h,.960+.047*h);ctx.translate(-800,-426)
   f(g,c,st,en,a);ctx.restore()
 if w>0 and seed<1:
  # The sweep is the sum of the directions we've visited, not a sum of scores.
  for j,tag in enumerate(CUES):
   a0=r.at(travel(c,c.at(tag)));x0,y0=lerp(a0,(800,425),w*.32*(1-(j+1)*.044))
   v=easepos(t,gather+.14+j*.089,.84);path(g,[(x0,y0),(mix(x0,800,.55),mix(y0,425,.55)-15),(800,425)],v,PAL[j],2.21,ink*math.sin(pi*clip(w))**.56)
 if seed:
  from v4_act0 import closing
  curtain(g,seed,lambda:closing(g,cue('8-2'),time=0.))
