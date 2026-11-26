from ink import *
from motion import transit,guide
from ink_words import letter,swish,carryword
from studio_examples import pstep,silk,area,mark,BLUE,AQUA,VIO,MONO
from timeline3 import W,S,clock
from termnotes import hint
from functools import lru_cache
def pro(g,c):
 t=c.t;filter_=c.at('题目筛一遍');amb=c.at('有歧义');wrong=c.at('标错');drop=c.at('拿掉');two=c.at('第二刀');four=c.at('四个选项');ten=c.at('最多十个');quarter=c.at('百分之二十五');tenp=c.at('百分之十',0);multi=c.at('第三刀');direct=c.at('直接交一个字母');reason=c.at('先推理再选择');case=c.at('换一张卷子');spread=c.at('又拉开了')
 # The previous title is one solid piece of type. Keep all four original letters on the board.
 fr=.76;k=phase(t,.03,fr)
 if t<fr:
  from stage3 import surface,raw
  ctx=g.c;wd=ctx.get_target().get_width();cc=getattr(g,'_pro_base',None)
  if cc is None:
   cc,old=surface(wd);raw(old,'3-1',S['3-1']['duration']-1/60);cc.flush();g._pro_base=cc
  # The old readings physically subside under their baseline. New data never print over old values.
  ctx.save();ctx.rectangle(0,148,1600,655);ctx.clip();ctx.translate(0,130*k);ctx.scale(1600/wd,1600/wd);ctx.set_source_surface(cc,0,0);ctx.paint_with_alpha(1-k);ctx.restore()
 xx=mix(800,751,k);txt(g,'MMLU',xx,111,47,F)
 if k>.2:
  dx=g.measure('MMLU',47,font=SERIF)/2
  silk(g,'-Pro',xx+dx+5,111,47,t-.24,F,1,'pen','left',.54)
 sub=pstep(t,.8,.40);txt(g,hint('MMLU-Pro'),800,169,26,M,sub)
 exit_=phase(t,two-.46,two+.30)
 if exit_<1:
  op=1-exit_;f=pstep(t,.70,.60);aa=phase(t,amb-.31,amb+.38);bb=phase(t,wrong-.20,wrong+.50);sweep=phase(t,drop-.24,drop+.44)
  for side,(x,head,col,sel) in enumerate(((437,'从 2、4 中选离 3 最近的数',C,aa),(1150,'2² 的值',T,bb))):
   v=f*(1-.70*sweep)*op
   silk(g,head,x,301,39,t-.76-side*.09,F,v)
   if side==0:
    line(g,(x-190,458),(x+190,458),M,2,v)
    for j,n in enumerate((2,3,4)):
     xx0=x+(j-1)*143
     if j==1:line(g,(xx0,447),(xx0,470),M,2.2,v)
     else:dot(g,xx0,458,10,Y,v)
     txt(g,str(n) if j!=1 else '参照 3',xx0,508,32 if j!=1 else 24,Y if j!=1 else M,v)
    if sel:
     for sg in (-1,1):line(g,(x,414),(x+sg*143*sel,414),O,2.3,v);dot(g,x+sg*143*sel,414,4.5,O,v)
    if aa:silk(g,'两个答案一样近',x,611,30,t-amb+.14,O,v)
   else:
    for j,n in enumerate((3,4)):
     xx0=x+(j-.5)*172;ring(g,xx0,450,36,(O,T)[j],v,2.4);txt(g,str(n),xx0,450,32,F,v)
     if sel:check(g,xx0,527,10,j==1,v*sel)
    if bb:silk(g,'标成 3，算来是 4',x,611,30,t-wrong+.13,O,v)
  if sweep:
   for x in (437,1150):line(g,(x-145,626),(x-145+290*sweep,590),R,3,op*sweep)
  txt(g,'清除歧义和错键 · 构造例',800,728,23,M,f*op)
 nxt=phase(t,multi-.48,multi+.25)
 if exit_ and nxt<1:
  op=exit_*(1-nxt);ex=phase(t,ten-.36,ten+.29);panel=159;wid=1280;y=416
  txt(g,'一次均匀盲猜',800,293,37,F,op)
  for j in range(4):
   xx=panel+(j+.5)*mix(wid/4,wid/10,ex);ww=mix(wid/4,wid/10,ex)-8;co=Y if j==1 else BLUE
   rect(g,xx-ww/2,y-43,ww,86,inkcol(co,.68 if j==1 else .43),op)
   line(g,(xx-ww/2,y+43),(xx+ww/2,y+43),co,2.2,op);txt(g,'ABCD'[j],xx,y,38,F,op)
  for j in range(4,10):
   u=pstep(t,ten+.31+(j-4)*.053,.39);xx=panel+(j+.5)*wid/10;ww=wid/10-8
   if u:rect(g,xx-ww/2,y-43+(1-u)*23,ww,86,inkcol(BLUE,.43),op*u);txt(g,'ABCDEFGHIJ'[j],xx,y+(1-u)*23,38,F,u*op)
  # One winning sector out of equal sectors. Count and area describe the same
  # probability. Four and ten coexist when the narrator actually compares them.
  both=phase(t,ten-.29,ten+.40)
  for jj,(cnt,xx,tr) in enumerate(((4,509,quarter),(10,1058,tenp))):
   active=1 if jj==0 else both
   if not active:continue
   now=phase(t,tr-.22,tr+.53);clr=Y if now>.03 else O
   aa=op*active;cy=621;r=51+7*sin(pi*now)
   ctx=g.c;ctx.save();ctx.move_to(xx,cy);ctx.arc(xx,cy,r,-pi*.5,-pi*.5+tau/cnt);ctx.close_path();g.source(clr,aa);ctx.fill();ctx.restore()
   for ii in range(cnt):
    an=-pi*.5+ii*tau/cnt;line(g,(xx,cy),(xx+r*cos(an),cy+r*sin(an)),M,1.5,aa*.85)
   ring(g,xx,cy,r,C if jj else O,aa,2.5)
   txt(g,f'1/{cnt}',xx+82,cy-17,39,F,aa,'left')
   if now:txt(g,('25%','10%')[jj],xx+82,cy+33,32,Y,aa*now,'left');swish(g,xx+81,xx+174,cy+64,t-tr+.18,Y,.48)
 if nxt:
  op=nxt;trans=phase(t,case-.18,case+.73)
  if trans<1:
   old=op*(1-trans);at=[multi,c.at('好多步') if '好多步' in c.s['chars'] else c.at('好几步'),direct,reason]
   nk=phase(t,direct-.30,direct+.50)
   for j,(n,cl) in enumerate((('条件',C),('推断',T),('检验',T),('选择',Y))):
    xx=323+j*315;p=pstep(t,multi+.14+j*.14,.50)
    if p:txt(g,n,xx,339,33,cl,p*old*(1-.65*nk))
    if j:arrow(g,(xx-232,339),(xx-74,339),p,cl,old*(1-.74*nk),2.2)
   k0=pstep(t,direct-.20,.67);k1=pstep(t,reason-.12,.64)
   for j,(lb,xval,grow,co)in enumerate((('直接选',53.5,k0,O),('先推理再选',72.6,k1,C))):
    yy=484+91*j
    txt(g,lb,472,yy,28,F,old*grow,'right');rect(g,507,yy-12,xval*9.1*grow,24,co,old*grow)
    txt(g,f'{xval:.1f}%',527+xval*9.1,yy,33,co,old*grow,'left')
   if k0:txt(g,'GPT-4o · 同一张 MMLU-Pro',800,705,26,M,old*k0)
  if trans:
   a=op*trans;xx0,xx1=425,1114
   ty=lambda n:556-(n-59)*7.09
   txt(g,'MMLU',xx0,271,31,F,a);txt(g,'MMLU-Pro',xx1,271,31,F,a)
   q=phase(t,case+.14,spread+.08)
   for j,(label,v1,v2,col)in enumerate((('GPT-4o',88.7,72.6,C),('GPT-4 Turbo',86.5,63.7,VIO))):
    y0,y1=ty(v1),ty(v2);u0=pstep(t,case+.15+j*.09,.51)
    txt(g,label,xx0-82,y0+(-19 if not j else 19),25,col,a,'right');dot(g,xx0,y0,7,col,a)
    # Separate the close old scores with true leaders; the data points do not move.
    txt(g,str(v1),xx0+12,y0+(-27 if not j else 31),24,col,a,'left')
    end=lerp((xx0,y0),(xx1,y1),q);line(g,(xx0,y0),end,col,3.6,a*q);dot(g,*end,7,col,a*q)
    if q>.97:txt(g,f'{v2}%',xx1+22,y1,29,col,a,'left')
   l0,l1=ty(72.6),ty(63.7);q0=pstep(t,spread-.12,.64)
   if q0:
    path(g,[(1308,l0),(1324,l0),(1324,l1),(1308,l1)],q0,Y,2.4,a)
    txt(g,'两模型差距：2.2 → 8.9 个百分点',800,680,31,Y,a*q0)
def crystal(g,x,y,size,col,op=1,turn=0):
 # Actual faceted solid, no gradient. A quarter turn follows the passage through the two tests.
 az=.33+turn*1.17;el=-.24
 pts=[(0,-1.12,0),(0,.98,0)]+[(cos(j*tau/5),-.075,sin(j*tau/5))for j in range(5)]
 def proj(p):
  a,b,c=p;xx=a*cos(az)+c*sin(az);z=c*cos(az)-a*sin(az);yy=b*cos(el)-z*sin(el);dd=b*sin(el)+z*cos(el);return(x+xx*size/(1-.07*dd),y+yy*size/(1-.07*dd),dd)
 v=[proj(p)for p in pts];faces=[(top,2+j,2+(j+1)%5)for j in range(5)for top in (0,1)]
 for f in sorted(faces,key=lambda f:sum(v[i][2]for i in f)):
  mean=sum(v[i][2]for i in f)/3;g.poly([v[i][:2]for i in f],col,1.45,op,True,inkcol(col,max(.16,.36+.30*mean+(.08 if f[0]==0 else 0))),1)
def gpqa(g,c):
 t=c.t;name=c.at('GPQA');search=c.at('搜索引擎');diamond=c.at('Diamond');round1=c.at('两位同领域博士');explain=c.at('核对解析');outs=c.at('三位其他学科');min_=c.at('至少十五分钟');avg=c.at('平均三十七');one=c.at('一人答对');end=c.at('两道关都过')
 paper=pstep(t,.3,.60);t0=diamond-.42
 silk(g,'GPQA',137,103,51,t-.15,F,paper,'pen','left')
 dx=g.measure('GPQA',51,font=SERIF)+12
 if t>diamond-.19:silk(g,'Diamond',137+dx,103,51,t-diamond+.19,Y,1,'pen','left',.64)
 silk(g,'专家复核、外行也难查到答案的科学题',139,159,25,t-name+.1,M,1,align='left')
 phase2=phase(t,t0,t0+.69)
 if phase2<1:
  a=1-phase2
  # The empirical landscape behind the two validation rooms: no public test question is reproduced.
  sections=[('物理',C),('化学',T),('生物',VIO)]
  for j,(s,col) in enumerate(sections):
   u=pstep(t,.36+j*.12,.65);xx=347+j*444
   if j==0: # the field of a simple dipole, used here only as a subject identifier
    for n in range(-3,4):
     z=n/3;pts=[(xx-82+164*k/42,386+72*z*math.sin(k*pi/42))for k in range(43)];path(g,pts,u,col,2.3,a*.86)
    dot(g,xx-82,386,7,col,a*u);dot(g,xx+82,386,7,col,a*u)
   elif j==1:
    for k in range(6):
     l=-pi/2+k*tau/6;l1=l+tau/6;pp=(xx+76*cos(l),387+76*sin(l));qq=(xx+76*cos(l1),387+76*sin(l1))
     path(g,[pp,qq],u,col,3.3,a);dot(g,*pp,6.4,col,a*u)
   else:
    for k in range(25):
     y=307+k*6.8;w=cos(k*.22);x1=xx+52*w;x2=xx-52*w
     if k%3==0:line(g,(x1,y),(x2,y),col,2,a*.72*u)
     dot(g,x1,y,3.6,col,a*u);dot(g,x2,y,3.6,C,a*u)
   txt(g,s,xx,539,35,col,a*u)
  if t>=search-.15:
   pp=pstep(t,search-.15,.7)
   # Published figure 1 uses four possibilities on each of two axes. Show that combinatorial structure,
   # not the wording of a test item. The check is geometric rather than another document icon.
   for row in range(4):
    for col in range(4):
     po=pstep(t,search-.12+(row*4+col)*.034,.38);rect(g,661+19*col,588+19*row,12,12,(C,T,VIO,O)[row],a*po)
   txt(g,'4 类起点 × 4 种方向',796,611,28,F,pp*a,'left');txt(g,'公开示例的计数思路',797,658,23,M,pp*a,'left')
   swish(g,792,1077,636,t-search+.02,Y,.55)
 if phase2:
  a=phase2
  crystal(g,245,435,75,Y,a,.25*phase(t,diamond,round1)+.34*phase(t,explain,outs)+.41*phase(t,one,end+.66));txt(g,'候选题',244,599,29,Y,a)
  for j,(xx,lab,col,at,N) in enumerate(((665,'同领域验证',C,round1,2),(1220,'跨领域验证',VIO,outs,3))):
   k=pstep(t,at-.40,.70)
   if not k:
    for i in range(N):
     x=xx+(i-(N-1)/2)*83;y=429
     path(g,[(x,y-30),(x+21,y),(x,y+30),(x-21,y),(x,y-30)],1,col,1.65,.25*a)
    continue
   arrow(g,(xx-289,435),(xx-175,435),k,col,a,2.4);txt(g,lab,xx,295,34,col,a*k)
   for i in range(N):
    x=xx+(i-(N-1)/2)*83;h=pstep(t,at-.20+i*.13,.52);y=429
    area(g,[(x,y-45),(x+31,y),(x,y+45),(x-31,y)],inkcol(col,.45),a*h)
    if j==0:
     kk=pstep(t,explain-.2+i*.15,.47);check(g,x,y,9,True,kk*a)
    else:
     kk=pstep(t,one-.41+i*.10,.48);check(g,x,y,9,i==1,kk*a)
   if j==0:txt(g,'核对后达成共识',xx,584,27,F,a*pstep(t,explain-.22,.56))
   else:
    kmin=pstep(t,min_-.16,.64);kavg=pstep(t,avg-.11,.60)
    if kmin:txt(g,'至少 15 分钟',xx,554,25,F,a*kmin*(1-kavg))
    if kavg:txt(g,'平均 37 分钟',xx,554,29,F,a*kavg)
    if t>=one-.25:txt(g,'至多 1 / 3 答对',xx,617,28,VIO,a*pstep(t,one-.24,.60))
  if t>end-.22:
   swish(g,665,1213,698,t-end+.22,Y,.68);silk(g,'两道筛选都通过',910,690,32,t-end+.13,Y,a)
