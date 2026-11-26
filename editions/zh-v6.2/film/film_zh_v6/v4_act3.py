from rig4 import *
from studio_exam import crystal
def saturation(g,c):
 t=c.t;wheel=c.at('这波浪潮')-.18
 if t<wheel:
  # Start the next measurement, not a recap of bytes/domains/softmax.
  # Two answer tokens are enough to grade, however the reasoning was obtained.
  a=enter(t,.03,.59);key=c.at('客观标准答案');auto=c.at('批改全自动');split=c.at('学科和难度');hide=c.at('遮住解题过程')
  left=199;zz=1-phase(t,wheel-.42,wheel);fade=a*zz
  u=enter(t,key-.20,.56);v=enter(t,auto-.18,.61)
  label(g,'9 − 7',left,300,80,F,zz)
  for i,(lab,x,col,t2)in enumerate((('3',931,C,1),('2',1281,V,0))):
   ss=enter(t,.41+.24*i,.60);prop=ss*fade if not i else zz
   ring(g,x,422,58,col,prop,2.5);dot(g,x,422,51,inkcol(col,.46),prop)
   label(g,lab,x,420,50,F,prop);label(g,'基础版' if not i else '指令版',x,303,31,col,ss*fade)
   verify=enter(t,auto-.16+.23*i,.55);toward=enter(t,auto-.24+.22*i,.70)
   if verify:check(g,x+86,425,14,not t2,verify*zz)
   if toward:path(g,[(474,489),(552,536),(x,536),(x,502)],toward,Y,2.2,toward*zz)
  if u:
   path(g,[(left,397),(left,467),(left+87,467)],u,Y,2.2,zz)
   label(g,'标答  2',394,472,43,Y,u*zz)
  for i,j in enumerate(('学科','难度')):
   dt=enter(t,split-.15+i*.36,.51);fade0=1-phase(t,hide-.53,hide+.19)
   if dt:label(g,j,712+i*157,667,31,(T,O)[i],dt*fade0*zz)
  de=enter(t,hide-.19,.67)
  if de:
   xx=left+292-305*de;rect(g,xx,237,305*de,135,BLACK,.96*zz)
   line(g,(xx,254),(xx,357),C,2.6,.87*zz)
   if c.u('只留模型填的'):
    for i,x in enumerate((931,1281)):
     swish(g,x-45,x+45,486,t-c.at('只留模型填的')-.17*i,(C,V)[i],.57,2.6)
   isok=c.u('机器已经能判',.59)
   if isok:label(g,'按答案位判分',1106,673,33,T,isok*zz)
  return
 from saturation6 import exam
 exam(g,c,wheel)
def pro(g,c):
 t=c.t;data=c.at('看同一个 GPT')-.28;end=c.at('把旧卷')-.20
 if t<data:
  from exam_paper6 import options
  options(g,c,data)
  return
 from exam_readout6 import draw
 draw(g,c,data,end)
def gpqa(g,c):
 t=c.t;en=c.at('就看这道');leave=c.at('查到这个分子')+1.7;paper=0
 knots=((0,0),('GPQA','GPQA'),('搜索引擎','搜索引擎'),('十六种','题干要是搜一搜'),('题写出来','Diamond'),('同领域专家','两位同领域博士'),('核对理由','核对解析'),('其他学科的聪明','三位其他学科'),('谷歌随便查','给足每人'),('至少给十五分钟','至少十五分钟'),('平均用了三十七','平均三十七'),('至少两个没答对','最多只能有一人答对'),('通过这些筛选','两道关都过'),('$','$'))
 first=c.at('GPQA')
 if t<first+.22:
  from exam_readout6 import lookup
  # The old graph leaves intact. Briefly show the loophole in the *same*
  # answer tiles, then enter the foreground of the actual subjects.
  lookup(g,c)
  u=phase(t,first-.43,first+.22)
  if u:
   ctx=g.c;ctx.save();ctx.push_group();native(g,c,'3-3',knots)
   ctx.pop_group_to_source();ctx.paint_with_alpha(u);ctx.restore()
  return
 # Read the photographic evidence in one exposure: the field and helix leave before any white paper enters.
 if en-.62 <= t < leave+1.15:
  if t<en-.18:
   native(g,c,'3-3',knots);shade(g,phase(t,en-.62,en-.18))
  elif t<leave+.52:
   page(g,AS/'gpqa-question.png',655,393,737,t-en+.18,leave-en+.66,tilt=-.030,read='化学题与审题批注')
   page(g,AS/'gpqa-review.png',1229,420,341,t-en+.06,leave-en+.46,tilt=.034)
  else:
   native(g,c,'3-3',knots);shade(g,1-phase(t,leave+.52,leave+1.15))
 elif t>=c.at('一百九十八')-.46:
  from diamond6 import close
  close(g,c,lambda:native(g,c,'3-3',knots))
 else:native(g,c,'3-3',knots)
 # Bring the reference book back on the speaker's actual search cue, after the clock.
 age=t-c.at('谷歌随便查资料')
 if -.10<age<2.25:
  h=enter(age,-.10,.44)*(1-phase(age,1.70,2.25));swish(g,38,150,311,age+.06,T,.57,3.4)
  # The label travels with the opened real record, on science6's clock.
import random
rng=random.Random(4014)
DUST=[(rng.random(),rng.random(),rng.random(),rng.random(),rng.random())for _ in range(1040)]
TOP100=sorted(range(len(DUST)),key=lambda i:-DUST[i][3])[:100]
REGISTER={idx:k for k,idx in enumerate(TOP100)}
def plane(g,x,y,h,skew,co,u,phase_,lab):
 if u<.001:return
 w=h*.30;a,b=(x-w,y-h*.50),(x+w,y-h*.50-skew);d,e=(x-w,y+h*.50),(x+w,y+h*.50-skew)
 g.poly([a,b,e,d],co,1.9,u,True,inkcol(co,.25),.39*u)
 for j in range(1,7):
  f=j/7;line(g,lerp(a,b,f),lerp(d,e,f),co,.9,u*.29)
 for j in range(1,11):
  f=j/11;line(g,lerp(a,d,f),lerp(b,e,f),co,1.05,u*.43)
 f=(phase_*.27)%1;line(g,lerp(a,d,f),lerp(b,e,f),co,2.8,u*.90)
 label(g,lab,x,y-h*.5-skew-33,25,co,u)
def hle(g,c):
 t=c.t;pre=c.at('左边亮起')-.33;second=c.at('单位换了');submit=c.at('一万三千');six=c.at('六千道');pub=c.at('两千五百');end=c.at('日常用大模型')
 if t<pre:
  move=easepos(t,.012,.46)
  if move<1:endpaper(g,'3-3',dx=-222*move,dy=51*move,sc=1+.078*move,op=(1-move)**.86)
  u=enter(t,.37,.68);pic=c.u('图遮掉',.55);sf=V3/'source/regina-detail.png'
  title=c.at('人类最后考试');authors=c.at('全球专家');visual=c.at('带图像');one=c.at('有的答案')
  # The camera first meets an artefact, then the eye follows a genuine row of
  # its inscription. The photographic evidence is occluded only on the verb.
  magnify=phase(t,authors-.25,one+.20);w=660+53*magnify;px=534-6*magnify;py=417-12*magnify;theta=-.047+.013*magnify
  photo(g,sf,px+126*(1-u),py-38*(1-u),w*(.88+.12*u),tilt=theta+.125*(1-u),op=u)
  mark(g,'HLE',1071,305,73,t-title+.17,F,mode='pen',dur=.60,op=u);mark(g,'人类最后考试',1074,390,35,t-title+.42,O,op=u)
  label(g,'Regina 墓碑 · 铭文细部',535,662,25,M,u)
  if t>authors-.21 and t<visual+.59:
   h=during(t,authors-.21,visual+.59,.42)
   # Independent authors converge on a collection. No geographic counts are inferred.
   for j,co in enumerate((C,T,V,O)):
    sx=920+102*j;sy=535+36*(j%2);z=phase(t,authors-.20+.17*j,visual+.14)
    if z:
     ring(g,sx,sy,8,co,h,1.7);xx,yy=transit((sx,sy),(1080,468),z,23)
     point(g,xx,yy,4.2,co,h);path(g,[(sx,sy),(sx+6,sy-19),(1080,468)],z,co,1.4,h*.76)
  tag=enter(t,visual-.20,.56)
  if tag:
   label(g,'图像证据',1069,531,29,C,tag)
   path(g,[(982,525),(932,525),(861,467)],tag,C,2.1)
  if t>=one-.26 and not pic:
   z=enter(t,one-.25,.69);ctx=g.c;ctx.save();ctx.translate(px,py);ctx.rotate(theta)
   path(g,[(-266,45),(-266,58),(176,58),(176,44)],z,'#59391C',3.8,u);ctx.restore()
  if pic:
   ctx=g.c;ctx.save();ctx.translate(px,py);ctx.rotate(theta);half=w*.5;ht=w*img(sf).get_height()/img(sf).get_width()
   for side in (-1,1):
    x=-half if side<0 else half-half*pic;rect(g,x,-ht*.5,half*pic,ht,'#222426',.988)
   if pic>.96:label(g,'原图被遮住',0,0,31,M,enter(t,c.at('图遮掉')+.37,.38))
   ctx.restore()
  if t>pre-.48:shade(g,phase(t,pre-.48,pre))
  return
 age=t-pre;fade=enter(t,pre,.68);gate1=enter(t,pre+.24,.65);gate2=enter(t,submit-.40,.65);gate3=enter(t,six-.22,.68)
 dock=phase(t,pub-.13,pub+1.82);ports=phase(t,second-1.25,six+.55);zoom=1.55-.47*ports
 zoom=mix(zoom,1,dock)
 center=(mix(410,800,ports),mix(432,422,ports))
 origin=(800+(800-center[0])*zoom,415+(425-center[1])*zoom)
 qread=c.at('镜头拉近');styles=phase(t,qread-.52,qread+.17);qq=c.u('日常用大模型',.69)
 if styles<1:
  opacity=1-styles;ctx=g.c;ctx.save();ctx.translate(*origin);ctx.scale(zoom,zoom);ctx.translate(-800,-425)
  stages=((466,460,326,39,C,gate1,'前沿模型试答'),(824,422,250,40,O,gate2,'同行复核'),(1104,402,187,32,F,gate3,'终审'))
  for x,y,h,sk,co,v,lab in reversed(stages):plane(g,x,y,h,sk,co,v*(1-dock)*opacity,age,lab)
  batches={}
  for i,(seed,rv,depth,fate,dither)in enumerate(DUST):
   # The depth of the particle fixes its impact point on each sloping glass plane.
   # Rejected particles fall at that impact point and never reappear beyond a later plane.
   ix0,ix1,ix2=[x+(depth-.5)*.52*h for x,_,h,_,_,_,_ in stages]
   u=(seed+age*(.059+.018*dither))%1
   maxx=mix(ix0+135,ix1+70,gate2);maxx=mix(maxx,1400,gate3);xx=mix(69,maxx,u)
   ym=460-72*u;spread=(.46+depth*.41)*(1-.43*u);yy=ym+(rv-.5)*510*spread+(depth-.5)*26
   rr=1.45+2.1*depth;at=ix0 if fate<.53 else ix1 if fate<.783 else ix2 if i not in REGISTER else 1467
   if at==ix1 and gate2<.60:at=1525
   if at==ix2 and gate3<.60:at=1525
   if xx>at:
    diff=xx-at;op=max(0,1.-diff/102)
    if op<=0:continue
    xx=at+diff*.070;yy+=.020*diff**2;co=R if diff>2 else F;rr*=1.27
   else:
    op=.56+.43*depth;co=Y if xx>ix2 and gate3 else O if xx>ix1 and gate2 else T if xx>ix0 else C
   if dock and i in REGISTER:
    k=REGISTER[i];fromx,fromy=xx,yy;v_=clip(dock*1.33-(k//10+k%10)*.0169)
    # Final rack is in the camera's destination coordinate system. No duplicate particles.
    xx=mix(fromx,952+(k%10)*32,v_);yy=mix(fromy,241+(k//10)*32,v_)-58*sin(pi*v_)
    co=Y;rr=mix(rr,5.25,v_);op=max(op,v_)
   elif dock:op*=1-dock
   op*=fade*opacity
   if op<.015:continue
   key=(co,min(7,max(1,round(op*7))));batches.setdefault(key,[]).append((xx,yy,rr))
  for (co,al),group in batches.items():
   ctx.new_path()
   for x,y,r in group:ctx.move_to(x+r,y);ctx.arc(x,y,r,0,tau)
   g.source(co,al/7);ctx.fill()
  ctx.restore()
  if dock:
   label(g,'公开题',1105,614,35,Y,dock*opacity);label(g,'1 点 = 25 题',1105,673,24,M,dock*opacity)
   path(g,[(685,405),(779,405),(833,341),(916,341)],dock,Y,2.8,opacity)
   path(g,[(685,405),(779,405),(832,507),(892,507)],dock,T,2.8,opacity)
   label(g,'另留私测',821,575,27,T,dock*opacity)
   label(g,'2,500',420,392,78,Y,dock*opacity);label(g,'公开题',424,477,36,F,dock*opacity)
  if dock<1:
   # Keep quantities on one baseline while the spatial camera moves; unit changes on a cut, not a count-up.
   qty,unit,col=('≈ 6,000','候选题',O)if t>=six else ('≈ 13,000','正式投稿',T)if t>=submit else ('70,000+','出题尝试',C)
   rect(g,192,676,802,89,BLACK,.78*(1-dock)*opacity)
   label(g,qty,430,718,58,col,fade*(1-dock)*opacity);label(g,unit,588,718,34,F,fade*(1-dock)*opacity,'left')
   if second-.23<t<submit+.8:label(g,'次数 → 题数',919,716,26,M,opacity)
 if styles:
  ff=styles;ctr=(1120,378);rad=14+107*styles
  ctx=g.c;ctx.save();xx=mix(1120,553,styles);yy=mix(378,405,styles)
  if styles<1:ring(g,xx,yy,rad,Y,1-styles,2.1)
  # Two distinct, real HLE answer formats. Keep their evidence on the same page as the final question.
  a=enter(t,qread+.14,.67);b=c.u('精确短答案',.61)
  for i,(cx,lab,col)in enumerate(((452,'计算机科学',C),(1154,'生态学',T))):
   v=a if i==0 else b
   if not v:continue
   mark(g,lab,cx,221,41,t-qread-.13-(0 if i==0 else c.at('精确短答案')-qread),col,op=v)
   if i==0:
    label(g,'Which of the following graph classes…',cx,330,26,M,v)
    for j,ch in enumerate('ABCDE'):
     x=cx-204+93*j;box(g,x-29,424,58,64,col,v,inkcol(col,.24),1.85);label(g,ch,x,457,36,F,v)
    label(g,'选择一个选项',cx,590,31,col,v)
   else:
    label(g,'“Answer with a number.”',cx,330,35,M,v)
    line(g,(cx-114,492),(cx+114,492),col,2.5,v)
    label(g,'交一个数',cx,590,31,col,v)
  label(g,'HLE 原题节选 · 论文图 2',800,731,24,M,a)
  definite=c.at('事先能确定');lock=enter(t,definite-.24,.67)
  if lock:
   rr=1-phase(t,end-.23,end+.40)
   if rr:
    for x0,col in ((452,C),(1154,T)):path(g,[(x0,627),(x0,649),(802,649)],lock,col,2.1,rr)
    label(g,'事先有标答',802,682,33,Y,lock*rr)
  if qq:
   shade(g,qq)
   from fork6 import draw
   draw(g,c,end)
