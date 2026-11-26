from rig4 import *
from motion import formula
from studio_votes import wedge
from studio_preference import weft
MAT=json.loads((AS/'specimens.json').read_text())['mail']
LB=json.loads((AS/'arena-top5.json').read_text())
PAPER='#F4F1E9';INK='#262422'
def paperbody(g,x,y,w,h,theta,op,fn):
 if op<.002:return
 m=g.c;m.save();m.translate(x,y);m.rotate(theta);rect(g,-w*.5,-h*.5,w,h,PAPER,op);fn();m.restore()
def mail(g,x,y,sc,op,theta,c):
 m=g.c;m.save();m.translate(x,y);m.scale(sc,sc)
 def content():
  label(g,'POD  /  payment invoice',-238,-79,28,INK,op,'left');line(g,(-239,-42),(236,-42),'#B8B3A8',1.6,op)
  for j,tb in enumerate(MAT['prompt']):label(g,tb,-237,4+j*40,24,INK,op,'left',469)
  def read(ri,needle,anchor,colour):
   sentence=MAT['prompt'][ri];ts=c.t-c.at(anchor);h=during(ts,-.09,1.48,.30)
   if h<.003:return
   fs=min(24,24*469/max(1,g.measure(sentence,24,font=SERIF)));j=sentence.index(needle);xx=-237+g.measure(sentence[:j],fs,font=SERIF);ww=g.measure(needle,fs,font=SERIF)
   yy=4+ri*40+fs*.69;path(g,[(xx,yy),(xx+ww,yy)],enter(ts,-.09,.37),colour,2.25,h*op)
  for subject in [(1,'payment invoice','发票开错了','#246880'),(1,'urgently','尽快更正','#9C402D'),(0,'please','关系弄僵','#247654'),(0,'please','原信已经用了','#247654'),(1,'POD payment invoice','哪张票要改','#246880'),(0,'confirm with','谁得跟进','#714284'),(1,'urgently','事情很急','#9C402D')]:read(*subject)
 paperbody(g,0,0,552,229,theta,op,content);m.restore()
def storypage(g,i,x,y,op,t,mag=1):
 m=g.c;m.save();m.translate(x,y);m.scale(mag,mag);m.rotate((-.021,.018)[i]);co=(C,V)[i]
 label(g,('甲','乙')[i],-214,-89,35,co,op,'left');line(g,(-215,-58),(-156,-58),co,2.4,op)
 for j,s in enumerate(MAT['A' if i==0 else 'B']):mark(g,s,-215,j*53,40,t-.10*j,F,'left','wave',.42,op)
 m.restore()
def letterdesk(g,c):
 t=c.t;choice=c.at('两份回复')-.20;vote=c.rest('匿名投票');reveal=vote['end'];net=c.at('现在先别')
 if t<choice:
  desk=enter(t,.05,.58);q0=c.u('清理一列',.47);q1=c.u('食材',.50);q2=c.u('中间这一封',.53)
  zoom=c.u('发票开错了',1.06)
  def code():
   label(g,'pandas',-161,-60,27,INK,q0,'left');label(g,'df.drop_duplicates(', -161,3,28,'#154A68',q0,'left');label(g,"    subset=['brand'])",-161,50,26,'#82451D',q0,'left')
  if q0 and zoom<.56:
   slide_out=1-phase(zoom,.29,.56)
   paperbody(g,386-372*zoom,307-91*zoom,397,223,-.053-.12*zoom,q0*slide_out,code)
  if q1 and zoom<1:page(g,V3/'source/recipe-ink.png',1198+698*zoom,459-92*zoom,415,t-c.at('食材')+.10,c.at('真实匿名盲测')-c.at('食材')+.83,tilt=.058+.16*zoom)
  if not q2:
   from gates6 import MAIL_RUN,cut_mail
   hold=.22*(1-q2)*(1-phase(t,choice-.66,choice))
   if hold:cut_mail(g,t,MAIL_RUN,hold)
  if q2:
   x=mix(744,804,zoom);y=mix(554,420,zoom);m=mix(.91,1.58,zoom);mail(g,x,y,m,mix(.22,1.,q2),-.034+.014*zoom,c)
   if zoom:label(g,'Chatbot Arena  ·  真实邮件摘录',x,y+221,25,O,c.u('真实匿名盲测',.54))
  if t>choice-.62:
   z=phase(t,choice-.62,choice);ctx=g.c;ctx.save()
   # Reveal from the centre crease of the invoice, not a whole-board dissolve.
   for side in (-1,1):
    x=806*(1-z) if side<0 else 806
    rect(g,x,-1,806*z+1,902,BLACK,1)
   ctx.restore()
  return
 if t<net:
  h=enter(t,choice,.57);focus=enter(t,reveal,.54);op=1-phase(t,net-.48,net)
  label(g,'同一张开错的发票',189,161,34,O,h*op,'left')
  for j,(x,y) in enumerate(((486,360),(1114,482))):
   u=enter(t,choice+.12+.16*j,.49);storypage(g,j,x,y,op*u,t-choice-.12-.16*j)
   xx=x-213;yy=y+117;ring(g,xx,yy,14,(C,V)[j],op*u,2.6)
   if j==0 and focus:
    if t<net-.48:point(g,xx,yy,9,Y,focus)
    label(g,'原记录：甲获选',xx+36,yy,29,Y,focus*op,'left')
  # Mark both as *inputs* to the viewer, without suggesting a winner.
  blind=c.at('名字先遮住');read=c.at('左右各取');choose=c.at('选一封')
  if t<vote['start']:
   for j,(x,y)in enumerate(((273,264),(901,386))):
    f=during(t,read-.24+j*.65,blind+.63,.31);z=enter(t,read-.16+j*.65,.54)
    if f:path(g,[(x-22,y-13),(x-32,y-13),(x-32,y+111),(x-22,y+111)],z,(C,V)[j],2.15,f)
    f=during(t,blind-.16+.11*j,choose+.20,.36)
    if f:
     label(g,'匿名',x+146,y-19,23,M,f)
     z=phase(t,blind-.17+j*.11,blind+.48+.11*j);line(g,(x+113,y+1),(x+113+63*z,y+1),O,2.1,f)
  if focus:
   other=c.at('你选乙');both=c.at('我们收的是');gold=c.at('不是信封');z=enter(t,other-.21,.61);visible=1-phase(t,net-.73,net-.22)
   if z:
    # The hollow second ballot is possible, never a claim about the person watching.
    xx,yy=901,599;ring(g,xx,yy,22,V,z*visible,1.9)
    label(g,'另一种选择',xx+35,yy,28,V,z*visible,'left')
   if t>=both-.2:
    left=(273,477);right=(901,599);target=(707,695);v=enter(t,both-.2,.79)
    for src,co in ((left,Y),(right,V)):
     path(g,[src,(src[0],src[1]+48),target],v,co,1.6,visible*.68)
    u0=enter(t,gold-.19,.54)
    label(g,'读者的偏好',703,749,30,O,u0*visible)
  if t>=vote['start'] and t<reveal:
   prog=clip((t-vote['start'])/(reveal-vote['start']));line(g,(628,692),(972,692),E,1.7,op);line(g,(628,692),(628+344*prog,692),O,2.9,op)
  if t<reveal:label(g,'两份真实回答 · 匿名节译',802,753,24,M,h*op)
  if t>=net-.48:flying_vote(g,t,net)
  return
 livevotes(g,c,net)
 if t<net+1.54:flying_vote(g,t,net)
def flying_vote(g,t,st):
 a=(273,477);b=(603,365);u=clip((t-st+.48)/1.90)
 x,y=transit(a,b,p5(u),-128)
 point(g,x,y,9.0-3.3*u,Y,1)
 if u>.82:ring(g,*b,7+(u-.82)*105,Y,clip(1-(u-.82)*5.6),1.65)
def livevotes(g,c,st):
 t=c.t;r=enter(t,st,.66);coords=[(403,488),(820,232),(1199,535)];colors=(C,V,T)
 for i,(x,y)in enumerate(coords):
  a=enter(t,st+(.06,.24,3.80)[i],.56);dot(g,x,y,38,inkcol(colors[i],.42),a);ring(g,x,y,39,colors[i],a,2.3);label(g,'甲乙丙'[i],x,y,30,F,a)
 for j,(i,k)in enumerate(((0,1),(1,2),(2,0))):
  x,y=coords[i];u,v=coords[k];dx=u-x;dy=v-y;ll=math.hypot(dx,dy);a1=(x+46*dx/ll,y+46*dy/ll);a2=(u-46*dx/ll,v-46*dy/ll)
  z=enter(t,st+(.62,3.92,5.30)[j],.70);arrow(g,a1,a2,z,(O,T,V)[j],.9,2.5)
  for ii in range(3):
   q=((t-st)*.23+ii/3+j*.14)%1;xx,yy=lerp(a1,a2,q);dot(g,xx,yy,3.5 if ii else 6,(O,T,V)[j],z*.84)
 label(g,'一条边，一次胜负',808,699,31,M,r)
def elo(g,c):
 from rating6 import draw
 draw(g,c,livevotes,fit_ranks)
def fit_ranks(g,c):
 t=c.t;fit=c.at('反过来')-.13
 u=enter(t,fit,.61);fitted=c.at('拟合一组积分');shown=c.at('天梯上');interval=c.at('细细的横线')
 to_list=phase(t,shown-.84,shown+.38);ctx=g.c;ctx.save();ctx.translate(278*(1-to_list),0)
 leftpts=[(195+i*7.7,608-220/(1+10**(-(-600+1200*i/60)/400))) for i in range(61)]
 label(g,'成对胜负',190,185,38,T,u,'left')
 nd=[(265,344),(430,244),(589,353)]
 for j,(xx,yy) in enumerate(nd):
  col=(C,V,T)[j];h=enter(t,fit-.08+j*.11,.48);dot(g,xx,yy,22,inkcol(col,.49),h);ring(g,xx,yy,23,col,h,1.7);label(g,('甲','乙','丙')[j],xx,yy,20,F,h)
 for j,(i,jj) in enumerate(((0,1),(1,2),(2,0))):
  sn,en=nd[i],nd[jj];uv=enter(t,fit+.28+j*.13,.52);path(g,[lerp(sn,en,.16),lerp(sn,en,.86)],uv,(C,V,T)[j],1.8,uv)
  for jj_ in range(4):
   gtime=fit+.39+(.39*(j+jj_));fr=enter(t,gtime,.64);away=enter(t,fitted-.22+(j+jj_)*.20,1.06)
   x0,y0=lerp(sn,en,.22+.18*jj_);x,y=transit((x0,y0),(431,509),p5(away),-31)
   if away<1:dot(g,x,y,4.7,(C,V,T)[j],fr*(1-away*.74))
 fx=enter(t,fitted-.12,1.38);path(g,leftpts,fx,C,3.2);line(g,(194,615),(662,615),E,1.6,fx)
 if fx:
  label(g,'Δ 积分',640,648,23,M,fx);label(g,'P(甲胜)',200,400,23,C,fx)
 label(g,'相对积分',392,674,31,C,fx);label(g,'使已观察到的选择更可能',408,731,25,M,c.u('最贴合',.54));ctx.restore()
 rr=enter(t,shown-.38,.63);L=808;label(g,'Text Arena',L,151,48,F,rr,'left');label(g,'2026-11-22  ·  同一快照',L+1,202,25,M,rr,'left')
 X=lambda v:1184+(v-1480)*2.60
 for j,r in enumerate(LB):
  y=296+j*80;z=enter(t,shown-.31+j*.105,.53);name=r['model_name'].split(' (')[0]
  label(g,name,L,y,31,C if not j else F,z,'left',320);label(g,f"{r['rating']:.1f}",1464,y,32,O if not j else M,z,'right')
  lo,hi=r['rating_lower'],r['rating_upper'];aa,bb=X(lo),X(hi);m=X(r['rating'])
  iv=enter(t,interval-.10+j*.163,.57)
  dot(g,m,y,4.5,F,z);line(g,(mix(m,aa,iv),y),(mix(m,bb,iv),y),T,2.25,iv);line(g,(aa,y-6),(aa,y+6),T,1.8,iv);line(g,(bb,y-6),(bb,y+6),T,1.8,iv)
 arm=c.at('票有多少');z=c.u('跟谁交过手',.59);uu=enter(t,arm-.18,.62)
 if uu:
  # Two repeated real intervals share the numerical scale. Speak of overlapping uncertainty,
  # never reinterpret interval overlap alone as a test of a pairwise difference.
  r0,r1=LB[:2];lo=max(r0['rating_lower'],r1['rating_lower']);hi=min(r0['rating_upper'],r1['rating_upper'])
  if hi>lo and z:rect(g,X(lo),297,(X(hi)-X(lo))*z,81,inkcol(Y,.55),.48*z)
 label(g,'细线：积分估计的不确定区间',L,735,26,M,rr,'left')
def biases(g,c):
 t=c.t;length=c.at('换到同一道写机器人')-.20
 if t>=length:
  st=c.at('把字数当质量')-.12
  if t<st:
   from stories6 import shed
   shed(g,c,length,st)
  else:length_loop(g,c,t,st)
  return
 swap=c.at('互换位置');shift=phase(t,swap-.08,swap+.78);pos=c.u('位置偏见',.56);q=c.u('做裁判',.61)
 trials=c.at('两种摆法')-.25;style=c.at('再看文风')-.11
 stay=pos*(1-phase(t,trials+2.10,trials+2.64))
 if stay:label(g,'位置偏见',257,691,34,T,stay,'left')
 if t<trials:
  op=1-phase(t,trials-.41,trials)
  for j in (0,1):
   x=mix((466,1102)[j],(1102,466)[j],shift);y=mix((335,518)[j],(518,335)[j],shift)+(1 if j else -1)*104*sin(pi*shift)
   storypage(g,j,x,y,op,t+.03,.89)
  hand=c.at('交给另一台');tally=enter(t,c.at('真人众包')-.13,.67)
  fold=phase(t,hand-.42,c.at('做裁判')+.14);fast=c.at('一天改好几版');wait=c.at('等人来')
  if tally and fold<1:
   # No invented vote total: a little crowd gives up *this particular pair*
   # to a faster judge, not an empty document icon or a fake measured latency.
   label(g,'真人选票',469,134,30,T,tally*(1-fold)*op)
   for j in range(28):
    n=enter(t,.10+(j%14)*.092+(j//14)*.23,.49);src=(623+(j%14)*28.,128+(j//14)*40.)
    xx,yy=transit(src,(794,163),fold,28+5*(j%3));co=(C,V,T)[(7*j+1)%3]
    size=6.2 if j%4 else 8.3;dot(g,xx,yy,size,co,tally*op*n*(1-.68*fold))
   if t>=fast-.15:
    for j in range(3):
     f=enter(t,fast-.15+.47*j,.44)*(1-fold)*op
     x=1119+60*j;path(g,[(x-12,132),(x+13,132),(x+13,148),(x-12,148),(x-12,132)],f,O,1.8)
    label(g,'模型迭代',1176,186,24,M,enter(t,fast-.12,.49)*(1-fold)*op)
   if t>wait-.18:
    ph=clip((t-wait+.15)/max(.36,hand-wait));ww=310*phase(ph,0,1)
    line(g,(628,216),(948,216),E,1.6,(1-fold)*op);line(g,(628,216),(628+ww,216),T,2.7,(1-fold)*op)
  if q:
   area(g,[(795,113),(829,151),(795,191),(761,151)],V,q*op)
   label(g,'LLM-as-a-Judge',850,143,34,V,q*op,'left')
   label(g,'由模型比较两份回答',851,194,25,M,q*op,'left')
   for x,name,col in ((413,'MT-Bench',C),(655,'AlpacaEval',T)):
    z=enter(t,c.at(name)-.10,.47);end=1-phase(t,c.at('体检')-.55,c.at('体检')+.20)
    if z and end:label(g,name,x,159,28,col,z*op*end)
   for xx,yy,col in ((465,303,C),(1100,473,V)):
    f=enter(t,hand-.08,.75)*(1-phase(t,c.at('互换位置')-.7,c.at('互换位置')+.02))
    if f:
     path(g,[(xx,yy),(xx,yy-24),(795+(xx-795)*.18,231)],q,col,1.6,.64*op*f)
  # The two answers travel; the judge's seat rule stays put. A gold vote can
  # land on the same seat twice without tracking the answer that was there.
  point_=c.at('排在前面');winner=c.at('原先的赢家')
  if swap-.62<t<trials:
   seat_op=enter(t,swap-.62,.38)*op
   seat=(451,515);hold=enter(t,point_-.15,.48)
   pr=easepos(t,point_-.11,max(.57,winner-point_+.2))
   path(g,[(seat[0]-153,seat[1]),(seat[0]+153,seat[1])],seat_op,O,2.7,seat_op*.77)
   if hold:
    xy=transit((795,193),seat,pr,117.)
    if pr<.999:path(g,[(795,193),(645,238),(seat[0]+137,seat[1]-47),seat],pr,O,2.4,op*.63)
    point(g,*xy,8.5,Y,hold*op)
    if pr>.95:label(g,'这张票仍给左侧',seat[0],seat[1]+46,29,Y,hold*op)
  
  return
 if t<style:
  a=enter(t,trials,.53);outv=1-phase(t,style-.45,style);same=c.u('同一封信',.56);seat=enter(t,min(c.at('两次都选左边')-.12,style-2.85),.55)
  # Two actual elections written in two states. The first judge follows the letter,
  # the second the seat. Keep both counterfactuals visible once they have been spoken.
  for j,(x,lab,arr) in enumerate(((593,'原摆法',('甲','乙')),(1121,'互换后',('乙','甲')))):
   label(g,lab,x,215,34,M,a*outv)
   for rr,(s0,v,col)in enumerate((('每次选甲',same,T),('每次选左',seat,O))):
    y=367+rr*211
    if j==0:label(g,s0,227,y+4,31,col,v*outv)
    for k,s1 in enumerate(arr):
     xx=x+(k-.5)*158;co=C if s1=='甲' else V
     arrived=enter(t,trials+.06+.06*k+.10*j+.07*rr,.45)
     box(g,xx-58,y-42,116,83,co,outv*arrived,inkcol(co,.31),2.3);label(g,s1,xx,y,41,co,outv*arrived)
     if v and (s1=='甲' if not rr else k==0):
      path(g,[(xx-43,y+63),(xx+43,y+63)],v,col,4.5,outv);point(g,xx,y+62,6.5,col,outv*v)
  if seat:label(g,'票数一样，依据不同',803,735,31,O,seat*outv)
  return
 from style6 import compare_style
 compare_style(g,c,style,length)
def length_loop(g,c,t,st):
 """The same event survives both sentences. A hypothetical length-loving judge rewards the extra wrapper, not new information."""
 good=enter(t,st,.51);which=c.at('两个问题');bias=c.at('裁判明显');train=c.at('沿它的分数');again=c.at('多写两段')
 z=enter(t,which-.10,.65);choose=enter(t,bias-.12,.71);circle=enter(t,train-.12,1.01);repeat=phase(t,again-.25,again+.82)
 # The neutral stem is a paraphrase of the same physical event, not a count of
 # the original 241 English words; only the newly added courtesy is synthetic.
 label(g,'片段改写示意',400,240,25,M,good,'left')
 cx=786
 for j,(ss,col)in enumerate((('维修机器人',V),('穿过',F),('空商场',V))):
  x=cx+(-162,4,123)[j];mark(g,ss,x,352,44,t-st-.06*j,col,op=good)
  if z:line(g,(x-(83,39,64)[j],394),(x+(83,39,64)[j],394),T,2.2,z)
 if z:
  label(g,'情节不变',815,437,27,T,z)
  base=662;pitch=26;sy=487
  for j in range(10):
   qq=enter(t,which-.13+.055*j,.39);rect(g,base+j*pitch,sy,18,13,inkcol(T,.78),qq)
  if repeat:
   for j in range(11):
    ii=j-5 if j<5 else j+5;v=enter(t,again-.18+.047*j,.40)
    rect(g,base+ii*pitch,sy,18,13,O,v)
  n=10+sum(t>=again-.18+.047*j+.23 for j in range(11))
  label(g,f'{n} 字',405,sy+6,29,O if n>10 else T,z)

 # An observed choice feeds the *hypothetical* selection loop. No empirical
 # score is attached to this teaching sentence.
 if choose:
  a0=(1171,216);label(g,'假设裁判偏长',1170,167,27,V,choose)
  pts=[(a0[0],a0[1]-30),(a0[0]+32,a0[1]),(a0[0],a0[1]+30),(a0[0]-32,a0[1])]
  g.poly(pts,V,2.,choose,True,inkcol(V,.48),.78*choose)
 if circle:
  coords=[(1168,254),(1220,297),(1220,482),(1113,565),(433,565),(373,500)]
  path(g,coords,circle,V,2.3,circle)
  u=phase(t,train+.19,again+.18)
  if 0<u<1:
   lengths=[math.dist(a,b)for a,b in zip(coords,coords[1:])];at=u*sum(lengths)
   for a,b,ln in zip(coords,coords[1:],lengths):
    if at<=ln:dot(g,mix(a[0],b[0],at/ln),mix(a[1],b[1],at/ln),6.1,Y);break
    at-=ln
  label(g,'这一版更常被留下',801,621,28,V,circle)
 if repeat:
  # The actual event does not move; the added words physically grow at both ends.
  mark(g,'听我慢慢说：',481,351,30,t-again+.22,O,'right')
  mark(g,'。故事就是这样。',997,351,30,t-again-.10,O,'left')
  for l,r in ((292,482),(1001,1197)):
   line(g,(l,392),(mix(l,r,repeat),392),O,2.3,repeat)
  label(g,'多了 11 个字，仍是这一次穿行',810,725,28,O,repeat)
def fixed_stories(g,c,a):
 from studio_preference import material
 t=c.t
 quotes=('734 号擦亮黄铜路灯。','维修机器人驶过空商场。')
 for i,(xx,yy,col)in enumerate(((122,179,C),(171,471,V))):
  u=enter(t,.14+.16*i,.63)*a
  words=material()[i];dims,lines=weft(i)
  mark(g,quotes[i],xx,yy,35,t-.09-.11*i,F,'left',op=a)
  label(g,f"{'AB'[i]}  ·  {len(words)} 词",xx,yy+46,25,col,u,'left')
  pin=c.at('一个字都别删');confirm=c.at('原文还在左边')
  pulse=math.exp(-((t-pin-.27)/.32)**2)+math.exp(-((t-confirm-.42)/.45)**2)
  x0,y0=xx,yy+86
  for j,(x,r,w)in enumerate(dims):
   op=u*(.69+.31*((j//17+2*j//23)%3)/2);rect(g,x0+x*.875,y0+8.00*r,w*.875,4.8,inkcol(col,.93),op)
  if pulse>.008:
   Y0=y0-8;Y1=y0+8*(lines-1)+11
   path(g,[(xx+462,Y0),(xx+472,Y0),(xx+472,Y1),(xx+462,Y1)],1,Y,2.,u*min(1,pulse))
 if t>=c.at('一个字都别删')-.16:
  label(g,'原文保持不动',386,742,27,T,a*c.u('一个字都别删'))
def factor(g,c):
 t=c.t;ticket=c.at('每一张票');fit=c.at('放在一起拟合');zero=c.at('拨回零');avg=c.at('再取平均');pub=c.at('可以跟人类盲测');q=c.at('可就算人类')
 # One standing fitted function is probed throughout; the left-hand raw response objects never change length.
 if t<pub:
  outp=1-phase(t,pub-.53,pub);fixed_stories(g,c,outp)
  title=c.at('统计反事实')-.25;panelnote(g,'AlpacaEval 2.0','在同等长度下估计偏好胜率',751,103,t-title,T,outp)
  from scoring_ribbon6 import strips,ticket_spine
  if t<fit+.38:
   strips(g,c,ticket,outp)
   ticket_spine(g,c,ticket,fit,outp)
  if t<fit-.29:return
  from factor6 import fit_arc,probe,projected_reading
  fit_arc(g,c,fit,outp)
  graph=enter(t,fit-.28,.88)*outp;left,right,top,base=771,1446,299,600;mid=(left+right)/2;half=(right-left)/2
  def sigma(z,i):return 1/(1+exp(-((.48,-.52,1.05)[i]+1.65*math.tanh(1.14*z))))
  def at(z,i):return mid+z*half,base-(base-top)*sigma(z,i)
  path(g,[(left,top),(left,base),(right,base)],graph,M,1.9,graph)
  line(g,(mid,top),(mid,base+2),E,1.4,graph)
  for j,lab in enumerate(('较短','0','较长')):label(g,lab,(left+28,mid,right-28)[j],base+34,25,Y if j==1 else M,graph)
  label(g,'长度差  Δℓ',mid,base+83,28,M,graph);label(g,'条件胜率',left,top-40,26,C,graph,'left')
  if t<avg-.3:label(g,'单题拟合示意',right,base+118,22,M,graph,'right')
  many=c.u('对每道题',.86)
  measure=probe(c)
  for i,col in enumerate((C,T,V)):
   vis=graph if i==0 else many*graph;pr=enter(t,fit-.24,1.13) if i==0 else enter(t,c.at('对每道题')-.13+.18*(i-1),.89)
   if vis<.001:continue
   pts=[at(-1+2*j/80,i)for j in range(81)];path(g,pts,pr,col,3.5 if i==0 else 2.,vis)
   zp=measure if i==0 else 0;px,py=at(zp,i)
   if i==0:
    line(g,(px,py),(px,base),Y,2.0,vis);point(g,px,py,9,Y,vis)
    label(g,'Δℓ = 0' if t>=zero+.54 else 'Δℓ',px,py-33,27,Y,vis)
   else:point(g,px,py,5.5,col,vis)
  # Pull the numeric head of the conditional curve into the little probability
  # sector on the first reading, rather than asking the viewer to find it.
  pt_at=c.at('曲线上的一点');cond=c.at('在这些条件下');prefer=c.at('更可能被选中');limit=c.at('先把手指')
  if pt_at-.25<t<limit+.10:
   xx,yy=at(measure,0);r0=during(t,pt_at-.25,cond+.26,.29)
   if r0:ring(g,xx,yy,16+8*enter(t,pt_at,.65),O,r0*graph,2.1)
   v=during(t,cond-.12,limit+.10,.48);draw=phase(t,cond-.12,prefer+.51)
   if v:
    path(g,[(xx+13,yy-14),(xx+53,yy-55),(1203,277),(1283,204)],draw,T,1.95,v*graph)
    if draw>.70:ring(g,1320,174,50,O,v*graph*.74,1.65)
  pv=sigma(measure,0);cx,cy,rad=1320,174,45
  wedge(g,cx,cy,rad,-pi/2,-pi/2+tau*pv,C,graph);wedge(g,cx,cy,rad,-pi/2+tau*pv,3*pi/2,V,graph);label(g,f'{pv:.0%}',cx+65,cy,34,F,graph,'left')
  projected_reading(g,c,at(measure,0),left,(cx,cy),graph)
  if zero-.4<t<zero+2.7:
   swish(g,mid-22,mid+22,base+53,t-zero+.10,Y,.68,3.1)
  if t>avg-.21:
   av=enter(t,avg-.18,.61)
   if av:
    vals=[sigma(0,i) for i in range(3)];a0=sum(vals)/3
    for j,pval in enumerate(vals):
     a1=c.at('再取平均')+.10*j;yf=base-(base-top)*pval;f=clip((t-a1)/1.23)
     if 0<f<1:
      x0,y0=transit((mid,yf),(1369,710),p5(f),53);dot(g,x0,y0,5.3,(C,T,V)[j],graph)
    label(g,f'三题示意均值  {a0:.1%}',1191,741,28,T,graph*av)
  keep_text=c.at('不是去剪文章');curve=c.at('也不是把回归曲线')
  if keep_text-.16<t<pub:
   # Read the misconception in the actual objects, not in a crossed-out label.
   for j,(x,y,n,col) in enumerate(((120,258,len(weft(0)[0]),C),(172,557,len(weft(1)[0]),V))):
    qh=during(t,keep_text-.16+.23*j,curve+.16,.42);yy=y+8*(weft(j)[1]-1)
    if qh:path(g,[(x-2,y-8),(x-15,y-8),(x-15,yy+11),(x-2,yy+11)],enter(t,keep_text-.12+.23*j,.64),col,2.4,qh*graph)
   v=during(t,curve-.11,pub-.11,.46);f=phase(t,curve,pub-1.13)
   if v:
    # Traverse the slope without moving the statistical intervention away from zero.
    xx,yy=at(-.80+1.6*f,0);ring(g,xx,yy,10,F,v*graph,2.1)
    pts=[at(-.81+1.62*j/60,0)for j in range(61)];path(g,pts,f,C,4.5,v*graph*.71)
  return
 if t<=q:
  from studio_votes import MEASURE
  h=enter(t,pub,.70)*(1-phase(t,q-.53,q-.035));left,right=229,617;zz=enter(t,pub+.32,1.1);take=c.at('三十八个');compare=c.at('零点九八')
  label(g,'两款模型的原始与等长胜率',393,186,36,F,h)
  yy=lambda val:591-val*7.9
  for j,(r,col) in enumerate(zip(MEASURE['win_rates_percent'],(C,V))):
   a,b=yy(r['uncontrolled']),yy(r['length_controlled']);f=clip((t-pub-.56-.15*j)/1.42)
   if h:dot(g,left,a,7,col,h);path(g,[(left,a),(right,b)],p5(f),col,3.3,h)
   if f>0:dot(g,mix(left,right,p5(f)),mix(a,b,p5(f)),7,col,h)
   label(g,f"{r['uncontrolled']:.1f}%",left-14,a,25,col,h,'right');label(g,f"{r['length_controlled']:.1f}%",right+17,b+(-14 if j==0 else 16),25,col,h*f,'left')
   label(g,r['label'],408,648+j*48,27,col,h)
  for x,lab in ((left,'原胜率'),(right,'控制长度')):label(g,lab,x,562,26,M,h)
  label(g,'和人类盲测的排名相关',1129,194,36,F,h)
  label(g,'38 个共有模型  ·  Spearman ρ',1124,654,26,M,c.u('三十八个',.59)*h)
  for i,(value,col,tag)in enumerate(((.94,C,'零点九四'),(.98,T,'零点九八'))):
   v=h*c.u(tag,.62);y=336+i*146
   if v:
    label(g,('原排名','等长排名')[i],861,y,27,F,v,'left');rect(g,1002,y-14,304*value*v,28,inkcol(col,.92),v);label(g,f'{value:.2f}',1371,y,42,col,v)
  if t>=c.at('百分之九十八')-.30 and t<q:
   xf=during(t,c.at('百分之九十八')-.34,q,.29)
   if xf:swish(g,1121,1350,687,t-c.at('百分之九十八')+.22,O,.69,3.0)
  return
 if t>q:
  # Type has left the shutter. New source text enters uncut.
  h0=enter(t,q+.04,.50)
  hinge=phase(t,c.at('电脑环境')-.85,c.at('电脑环境')+.59)
  xx=mix(802,591,hinge);yy=405
  mark(g,'734 号擦亮黄铜路灯。',xx,yy,58,t-q-.10,F,op=h0)
  label(g,'回答 A  ·  节译',xx,yy+78,26,C,enter(t,q+.21,.48))
  pa=c.at('打了高分')
  for j,(name,col,fr,go) in enumerate((('读者',T,(356,230),q+.14),('模型裁判',V,(1242,236),c.at('和裁判')-.13))):
   a2=enter(t,go,.51);f=phase(t,pa+.17*j,pa+1.07+.25*j);to=(xx-47+94*j,yy+131)
   px,py=transit(fr,to,p5(f),-47);dot(g,px,py,mix(8,11,f),col,a2*h0)
   label(g,name,fr[0],fr[1]-43,32,col,a2*(1-f)*h0)
   if a2 and f<1:
    pull=phase(t,go+.32,pa+.72+.14*j);path(g,[fr,(mix(fr[0],to[0],.58),fr[1]+40),to],pull,col,1.7,a2*(1-f)*.66)
  w=c.u('它嘴上',.66)
  if w:line(g,(xx-88,yy+162),(xx+88,yy+162),O,2.25,w);label(g,'偏好',xx,yy+211,31,O,w)
  if hinge:
   # Hypothetical votes certify preference. They have no conducting path to
   # a result lamp: a second observation must actually be made in the next act.
   lx=987;line(g,(lx,235),(lx,651),E,2.0,hinge)
   label(g,'执行结果',1229,367,37,F,hinge)
   hgap=c.u('电脑环境',.63);wire=enter(t,c.at('电脑环境')-.04,.75)
   path(g,[(xx+102,yy+162),(853,yy+162),(910,499),(960,499)],wire,O,2.25,hinge)
   path(g,[(1011,499),(1100,499),(1130,465),(1194,465)],wire,M,2,hinge)
   if hgap:
    ring(g,1222,465,24,M,hgap,2.3);label(g,'待实测',1222,550,29,M,hgap)
