"""A screening room, three actual artifacts, and one documented vote."""
from ink import *
from motion import out3,transit,guide
from ink_words import letter,swish,carryword
from cut_common import cairo
from timeline3 import W,S,clock
from functools import lru_cache
import json,random
MONO='DejaVu Sans Mono';BLUE='#29ABCA';AQUA='#40BC9C';VIO='#BD89F5';PAPER='#EEE9D9'
def pstep(t,at,d=.53):return out3((t-at)/d)
def area(g,points,col,a=1):g.poly(points,col,0,a,True,col,1)
def silk(g,s,x,y,sz,tm,col=F,aa=1,mode='wave',align='center',dur=.52):
 letter(g,s,x,y,sz,tm,mode,col,aa,align,dur=dur)
@lru_cache(None)
def plate(name):return cairo.ImageSurface.create_from_png(str(W/'source'/name))
def pictured(g,name,x,y,w,op=1):
 if op<.002:return
 sf=plate(name);w0=sf.get_width();h0=sf.get_height();ctx=g.c;ctx.save();ctx.translate(x,y);ctx.scale(w/w0,w/w0);ctx.rectangle(0,0,w0,h0);ctx.clip()
 ctx.set_source_surface(sf,0,0);ctx.get_source().set_filter(cairo.FILTER_BEST);ctx.paint_with_alpha(op);ctx.restore()
def mark(g,x,y,s,col,alpha=1):
 # Physical pointers use filled chevrons, not UI tags.
 area(g,[(x-s,y-s*.65),(x+s*.45,y),(x-s,y+s*.65)],col,alpha)
def leaf(g,x,y,s,col,op=1):
 ctx=g.c;ctx.save();ctx.translate(x,y);ctx.scale(s,s);ctx.move_to(0,0);ctx.curve_to(3,-17,18,-26,34,-27);ctx.curve_to(32,-10,18,0,0,0);ctx.close_path();g.source(col,op);ctx.fill();ctx.restore()
def symbol(g,which,x,y,sc=1,op=1,anim=1):
 ctx=g.c;ctx.save();ctx.translate(x,y);ctx.scale(sc,sc);z=op
 if which=='A':
  # A brass street lantern: the same brass/gold detail marks the copied line on both passes.
  line(g,(0,-10),(0,75),C,5,z);line(g,(-17,76),(18,76),C,3,z);line(g,(-10,65),(10,65),C,2,z)
  g.poly([(-23,-55),(23,-55),(15,-15),(-15,-15)],C,2,z,True,'#184753',.95)
  area(g,[(-10,-48),(9,-48),(5,-22),(-5,-22)],O,z*(.55+.45*anim))
  g.poly([(-30,-55),(0,-79),(30,-55)],C,2,z,True,'#1C758A',.96)
  dot(g,0,-83,3,C,z);line(g,(-14,-14),(14,-14),C,2,z)
 else:
  g.poly([(-28,32),(30,32),(20,69),(-20,69)],VIO,2,z,True,'#744DA0',.95)
  path(g,[(-1,30),(-4,15),(2,-8),(9,-24),(12,-47)],anim,T,3,z)
  if anim>.13:
   leaf(g,-1,4,-.63,T,z);leaf(g,1,-1,.78,G,z)
   if anim>.58:leaf(g,10,-27,.62,T,z)
 ctx.restore()
def works(g,prog,end=0,slots=(1,1,1),emailfirst=0):
 # Three different artifacts with three different verification gestures. No identical outer boxes.
 col=(C,VIO,O)
 for i,(base,act) in enumerate(zip((282,800,1316),slots)):
  if act<.002:continue
  x=base;y=403-17*act; brightness=act
  active=act*(1-(slots[i+1]if i<2 else end))
  # Work from the selected artifact outward. With all three compared, each returns to its original scale.
  focus=(.32,.23,.18)[i]*active
  sx=x+([131,0,-17][i])*active;sy=y+26*active
  ctx0=g.c;ctx0.save();ctx0.translate(sx,sy);ctx0.scale(1+focus,1+focus);ctx0.translate(-x,-y)

  if i==0:
   txt(g,'>>>',x-177,y-138,26,C,brightness,'left',font=MONO);txt(g,'清洗脚本',x-112,y-138,35,F,brightness,'left')
   line(g,(x-178,y-100),(x+173,y-100),C,2.1,brightness*.8)
   txt(g,'df.drop_duplicates(',x-174,y-58,27,C,brightness,'left',335,MONO)
   txt(g,'subset=["brand"])',x-146,y-18,24,F,brightness,'left',318,MONO)
   vals=(('Yum Yum','cup'),('Yum Yum','cup'),('Indomie','cup'))
   for j,(co,sty)in enumerate(vals):
    kill=phase(prog,1.1,1.65) if j==1 else 0;yy=y+48+j*39-(35*phase(prog,1.59,2.07)if j==2 else 0)
    rect(g,x-173,yy-10,7,20,[C,C,T][j],brightness*(1-kill));txt(g,co,x-147,yy,23,F,brightness*(1-kill),'left',font=MONO)
    txt(g,sty,x+154,yy,22,M,brightness*(1-kill),'right',font=MONO)
  elif i==1:
   txt(g,'✉',x-186,y-138,29,VIO,brightness,'left');txt(g,'工作邮件',x-134,y-138,35,F,brightness,'left')
   line(g,(x-185,y-100),(x+185,y-100),VIO,2,brightness)
   txt(g,'Subject:',x-181,y-63,22,VIO,brightness,'left',font=MONO)
   pictured(g,'mail-subject.png',x-183,y-34,366,brightness)
   txt(g,'“Finally, it’s final!”',x,y+62,33,F,brightness)
   swish(g,x-126,x+126,y+88,prog-2.0,VIO,.56)
   txt(g,'Python 发布通知 · 2023',x,y+133,23,M,brightness)
  else:
   txt(g,'§',x-179,y-138,33,O,brightness,'left');txt(g,'食谱',x-132,y-138,35,F,brightness,'left')
   line(g,(x-180,y-100),(x+178,y-100),O,2,brightness)
   pictured(g,'recipe-ink.png',x-182,y-58,365,brightness)
   # The real 2 eggs are counted on screen; shell outlines never stand in for a page.
   for j in range(2):
    ctx=g.c;ctx.save();ctx.translate(x-76+j*61,y+77);ctx.scale(14,20);ctx.arc(0,0,1,0,tau);g.source(('#F0AC5F','#F6CC8A')[j],brightness);ctx.fill();ctx.restore()
   txt(g,'2 eggs',x+80,y+75,27,O,brightness);txt(g,'烤 30–35 分钟',x,y+138,25,F,brightness)
  ctx0.restore()
 if end:
  line(g,(281,624),(1313,624),E,1.25,end)
  txt(g,'运行',278,683,28,C,end);txt(g,'读措辞',800,683,28,VIO,end);txt(g,'照着做',1310,683,28,O,end)
rng=random.Random(201)
FIELD=[(rng.random(),rng.random(),rng.random(),rng.random())for i in range(938)]
# Stable colour bins keep the surviving population recognisable at each gate.
def screenplane(g,x,y,z,col,op,open_=1):
 h=129*z;w=88*z;pts=[(x-w,y-h*.80),(x+w,y-h*1.18),(x+w,y+h*.77),(x-w,y+h*1.15)]
 g.poly(pts,col,2.2*z,op,True,inkcol(col,.11*open_),1)
 for i in range(1,6):
  k=i/6;line(g,lerp(pts[0],pts[1],k),lerp(pts[3],pts[2],k),col,1.05,op*.44);line(g,lerp(pts[0],pts[3],k),lerp(pts[1],pts[2],k),col,.9,op*.42)
def hfield(g,t,c):
 a=c.at('向各学科专家征题');b=c.at('第一道对抗筛网');qa=c.at('七万多次');sub=c.at('一万三千份');can=c.at('六千道');pub=c.at('两千五百');reserv=c.at('还有一份');out=c.at('可把这封');op=1-phase(t,out-.65,out+.02)
 if op<.001:return
 oldsample=1-phase(t,b-.82,b-.12)
 sample=phase(t,.25,1.20)*oldsample
 # The inscription is kept in its own coordinate system as the eye moves from the monument to the text.
 if sample:
  # The black photographic ground is the actual stone's silhouette. Start inside its relief,
  # pull back to context, then follow the inscription itself into a legible close shot.
  pull=phase(t,.34,2.32);glass=phase(t,c.at('必须看图')-.55,c.at('必须看图')+.64)
  width=mix(mix(882,520,pull),381,glass);xx=mix(mix(388,391,pull),114,glass);yy=mix(mix(-345,-25,pull),125,glass)
  pictured(g,'regina.png',xx,yy,width,sample)
  ox,oy=xx+width*.80,yy+width*1.21
  from mounting import etch
  if glass:
   srcx,srcy=xx+width*.10,yy+width*1.10;dstx,dsty=571,237
   cx,cy=transit((srcx,srcy),(dstx,dsty),glass,59)
   ww=mix(width*.78,895,glass)
   pictured(g,'regina-detail.png',cx,cy,ww,glass*sample)
   path(g,[(ox,oy),(ox+69,oy+15),(dstx+15,dsty+343)],glass,O,2.1,sample)
   etch(g,'帕尔米拉文',dstx+886,dsty+374,27,O,sample*glass,'right')
  where=pull*(1-glass)
  if where:
   path(g,[(ox,oy),(ox+60,oy-8),(1000,440)],where,O,1.8,sample)
   etch(g,'雷吉娜墓碑',1021,419,42,F,sample*where)
   etch(g,'HLE 图像题 · 公元 2 世纪',1021,469,25,O,sample*where)
  if .0<glass<.997:dot(g,ox,oy,5,Y,sample)
 # The eye rides a single filament. The frame is full because the candidates themselves occupy it.
 particles=phase(t,b-.68,b+.88);d1=phase(t,b-.45,b+1.5);z1=phase(t,sub-.48,sub+.88);z2=phase(t,can-.42,can+.91);z3=phase(t,pub-.45,pub+1.0);rv=phase(t,reserv-.20,reserv+.75)
 silk(g,'HLE',138,114,56,t-.24,F,op,'pen','left',.86)
 silk(g,'专家出的学术难题，有些还必须看图',138,178,25,t-1.1,M,op,align='left')
 labels=[('尝试','70,000+',qa,C),('投稿','≈ 13,000',sub,T),('候选','≈ 6,000',can,VIO),('公开题','2,500',pub,Y)]
 for j,(lab,val,at,col) in enumerate(labels):
  k=pstep(t,at-.14,.45);next_=labels[j+1][2] if j<3 else out
  if t<at-.14 or t>next_+.1:continue
  mask=k*(1-phase(t,next_-.34,next_-.07))*op
  xx=(266,584,907,1260)[j]
  txt(g,lab,xx,654,28,M,mask);silk(g,val,xx,708,56,t-at+.14,col,mask,'pen','center',.48)
 # A staggered set of planes opens a corridor, not a spreadsheet of four boxes.
 for x,y,s,col,vis in ((398,490,1.20,C,d1*(1-z3)),(762,445,1.04,T,phase(t,b+.9,b+2.0)*(1-z3)),(1088,402,.90,VIO,z1*(1-z3))):
  if vis:
   kk=phase(t,b-.45+(x-398)/494,b+.55+(x-398)/494);pos=x-(1-kk)*149
   screenplane(g,pos,y,s,col,op*vis)
   if .005<kk<.999:
    line(g,(pos-66*s,y-99*s),(pos-66*s,y+130*s),col,3.5*s,op*vis*(.2+.8*sin(pi*kk)))
 xs=[220,525,902,1218];ys=[523,492,454,412]
 # batch dots into a few Cairo paths. One position is computed per actual visible particle per frame.
 batches={}
 for i,(u,v,z,tag)in enumerate(FIELD):
  layer=1.11-z*.68
  az=-.12+.26*d1+.09*math.sin(.28*t);wx=(u-.5)*2.07;wz=(z-.5)*.99
  axis=wx*cos(az)+wz*sin(az);deep=wz*cos(az)-wx*sin(az);pers=1/(1+.43*deep)
  x=800+655*axis*pers+12*math.sin(v*5+t*.26);y=445+(410*(v-.5)-38*deep)*pers+15*math.sin(u*6+t*.23)
  m=z1*(1 if i>=234 else 0);n=z2*(1 if 100<=i<234 else 0)
  fade=1-max(m,n)
  if fade<.028:continue
  if m or n:
   y+=min(220,255*(m+n)**1.7);x+=30*(m+n)
  if i<234:
   k1=z1*.76;ax=432+u*746;ay=307+v*290;x=mix(x,ax,k1);y=mix(y,ay,k1)
  if i<100:
   k=z3
   # Exactly 100 macrocells: the public sample is 25 questions per cell.
   cx=756+(i%20)*32;cy=333+(i//20)*42
   x=mix(x,cx,k);y=mix(y,cy,k)
  rad=mix(1.8+3.5*(1-z),6.65,z3 if i<100 else 0)
  if not 210<y<656:continue
  bright=mix(.46+.52*(1-z),.94,z3 if i<100 else 0)*(1 if i<100 or z1<.01 else .86)
  col=(Y if z3>.4 and i<100 else (R if m+n>.13 else T if z1>.28 and i<234 else (BLUE,C,'#2384A3','#7CDDDF')[int(tag*4)%4]))
  bkey=(col,round(min(1,bright*fade*op*particles)*10)/10)
  if bkey[1]>.02:batches.setdefault(bkey,[]).append((x,y,rad))
 for (col,alpha),pts in batches.items():
  ctx=g.c;ctx.new_path()
  for x,y,r in pts:ctx.move_to(x+r,y);ctx.arc(x,y,r,0,tau)
  g.source(col,alpha);ctx.fill()
 # Physical sample of the input formats (before they have been sorted).
 desc=phase(t,b-.2,b+.41)*(1-phase(t,qa-.45,qa-.08))*op
 if desc:
  x=230 if t<b else 215
  txt(g,'文字题',x,716,26,C,desc,'left'); txt(g,'图像题',650,716,26,T,desc,'left');line(g,(x+98,716),(605,716),D,1.4,desc)
  ar=phase(t,c.at('必须看图')-.14,c.at('必须看图')+.53);g.poly([(785,728),(815,680),(855,728),(785,728)],T,2,desc*ar)
  if d1:txt(g,'模型先试答',1130,716,27,F,desc*d1)
 if z1 and z3<.99:
  follow=phase(t,sub-.20,pub+.12);start0=(397,492);end0=(1088,402);x,y=transit(start0,end0,follow,65)
  dot(g,x,y,7.4,F,op*(1-z3));ring(g,x,y,14.8,O,op*(1-z3),2.05)
 if z3:
  txt(g,'一点 = 25 道公开题',1064,560,25,Y,op*z3)
  # Keep the actual units legible at a glance instead of suggesting that an attempt was always a question.
  if t>pub-.1:
   for ii,(val,unit,co)in enumerate((('70,000+','尝试',C),('≈13,000','投稿',T),('≈6,000','候选',VIO))):
    xx=142+ii*196;y0=392+34*ii;txt(g,val,xx,y0,31,co,op*z3);txt(g,unit,xx,y0+49,24,M,op*z3)

 if rv:
  line(g,(1392,496),(1458,555),VIO,1.9,op*rv);txt(g,'另存私测',1440,597,25,VIO,op*rv)
def sieve(g,c):
 t=c.t;ask=c.at('可把这封');new=c.at('清洗脚本');hfield(g,t,c)
 if t>=ask-.22:
  a=pstep(t,ask-.22,.60);grow=phase(t,ask-.08,ask+1.1)
  # One strip of real work bursts out of the answer slot before the question ends.
  txt(g,'开放式任务',800,113,43,F,a)
  xa=(1-phase(t,new-.56,new-.13))*a
  if xa:
   pictured(g,'mail-subject.png',451,305,698,xa);silk(g,'改得客气一点',800,462,42,t-ask-.55,VIO,xa,'wave')
   for j,lab in enumerate('ABCD'):
    box(g,562+j*124,574,88,45,E,xa*(1-.72*grow),sw=1.4);txt(g,lab,606+j*124,597,24,M,xa*(1-.72*grow))
  if t>new-.35:
   times=[new,c.at('商务邮件'),c.at('食谱')];op=[pstep(t,v-.18,.45)for v in times]
   works(g,t-new,phase(t,c.at('对字符串')-.38,c.at('对字符串')+.46),op)
def quote(g,i,x,y,sc,op=1,icon=True):
 w=g.c;w.save();w.translate(x,y);w.scale(sc,sc);co=(C,VIO)[i];p='AB'[i]
 if icon:symbol(g,p,-177,-5,.86,op)
 txt(g,'回答 '+p,-83,-92,25,co,op,'left')
 for j,s in enumerate((('734 号的唯一职责，','是擦亮城里的黄铜路灯。'),('老维修机器人穿过','空荡荡的购物中心。'))[i]):
  txt(g,s,-83,-23+j*47,32,F,op,'left',365)
 line(g,(-81,73),(233,73),co,2.2,op*.85)
 w.restore()
def arena(g,c,handoff_only=False):
 t=c.t;anonymous=c.at('匿名模型');actual=c.at('投票谁更好');zoom=c.at('把这一票留下');many=c.at('模型有上百个');cyc=c.at('A 赢过 B');wrap=c.at('顺着箭头');scale=c.at('更可能赢')
 if t<.78:
  # Unfold the three real artifacts towards opposite margins; the centre is a continuous blackboard.
  ctx=g.c
  for away in (-1,1):
   k=out3(t/.78);ctx.save();ctx.rectangle(0 if away<0 else 800,0,800,900);ctx.clip();ctx.translate(away*845*k,0);works(g,8,1);txt(g,'开放式任务',800,113,43,F,1);ctx.restore()
 pi_=phase(t,.30,.88);grow=phase(t,zoom-.25,zoom+.83);ap=pi_*(1-grow)
 if ap and not handoff_only:
  silk(g,'为同一个机器人，写个短故事',800,149,47,t-.31,F,ap)
  for j,x in enumerate((436,1108)):
   quote(g,j,x,410,1.12,ap)
  txt(g,'真人对战 · 原回答中译节选',800,657,25,M,ap)
  if t>=actual-.10:
   p=pstep(t,actual-.10,.75);xx,yy=transit((798,621),(1127,551),p,79)
   dot(g,xx,yy,8,Y,ap*p);txt(g,'原记录：B 获选',1150,605,28,Y,ap*p)
 if grow>0:
  p=phase(t,zoom,many+.54);op=grow;tet=phase(t,cyc-.49,cyc+.36)
  head='一票只比较一对' if t<cyc-.45 else '三场对局可以绕成一圈'
  ttl=1-phase(t,cyc-.9,cyc-.48) if t<cyc-.45 else phase(t,cyc-.45,cyc+.05)
  txt(g,head,800,128,45,F,op*ttl)
  nodes=[(800+435*math.cos(j*tau/13-.91),430+209*math.sin(j*tau/13-.91))for j in range(13)]
  for j,(x,y)in enumerate(nodes):
   a=pstep(t,many-.2+j*.075,.48)
   if a:
    line(g,(x,y),nodes[(j+3)%13],BLUE,1.62,op*a*(.64-.46*tet));dot(g,x,y,7.8,C,op*a*(.76-.51*tet))
  a0,a1=(457,468),(1143,426);kp=pstep(t,zoom-.13,1.01)
  xp,yp=transit((1127,551),a0,kp,80);dot(g,xp,yp,8,Y,op*(1-tet))
  line(g,a0,a1,C,3.3,op*(1-tet));txt(g,'B',a0[0]-30,a0[1]-42,41,VIO,op*(1-tet));txt(g,'A',a1[0]+30,a1[1]-42,41,C,op*(1-tet))
  if tet:
   tri=[(500,517),(799,282),(1100,517)];st=[cyc,c.at('B 赢过 C'),c.at('C 又可能赢 A')]
   for j,co in enumerate((C,VIO,T)):
    x,y=tri[j];dot(g,x,y,18,co,tet);txt(g,'ABC'[j],x,y-51,35,F,tet)
    q=pstep(t,st[j]-.17,.56)
    if q:arrow(g,lerp(tri[j],tri[(j+1)%3],.072),lerp(tri[j],tri[(j+1)%3],.93),q,co,tet,4)
   pool=c.at('许多场');manyobs=phase(t,pool-.22,pool+.45)
   txt(g,'重复观测同一对 · 示意' if manyobs>.6 else '另三场对局 · 示意',800,669,25,M,tet)
   if manyobs:
    # Multiple *possible recorded votes*, not an observed leaderboard nor literal priors.
    # Identical endpoints can acquire different outcomes: the past winner is not a rule.
    for h in range(12):
     st0=pool-.18+h*.17;ph=phase(t,st0,st0+.73)
     if not ph:continue
     jj=h%3;lft,rgt=tri[jj],tri[(jj+1)%3]
     if h in (4,8,10):lft,rgt=rgt,lft
     endpos=(596+38*h,610);startpos=lerp(lft,rgt,.29)
     xx,yy=transit(startpos,endpos,ph,38+h%3*6);dot(g,xx,yy,6.5,(C,VIO,T)[jj],manyobs)

   loop=phase(t,wrap-.2,scale+.15)
   if 0<loop<1:
    n=min(2,int(loop*3));u=loop*3-n;xx,yy=lerp(tri[n],tri[(n+1)%3],u);dot(g,xx,yy,7,Y)
   if t>scale-.32:
    pr=pstep(t,scale-.32,.82);line(g,(504,705),(504+596*pr,705),Y,2.4,pr)
    v=phase(t,scale+.1,c.d-.26);xx=504+596*(.17+.66*v)
    dot(g,xx,705,6.6,C,pr);txt(g,'预测下一场的胜率',800,752,25,M,pr)
