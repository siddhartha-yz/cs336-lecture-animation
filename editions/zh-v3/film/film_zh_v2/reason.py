from termnotes import hint
from ink import *
from machines import ARC,PAL,grid
def arcgrid(g,c):
 t=c.t;demo=on(c,'三到五个',2.3);learn=on(c,'抽象变换规则',2.0);test=on(c,'全新测试网格',2.9);done=on(c,'解释所有示例',1.7)
 title(g,'ARC-AGI',110,sub=hint('ARC-AGI'))
 for j,pair in enumerate(ARC['train']):
  xx=345+j*453;y=350;size=121
  q=1 if j==0 else phase(t,.45+j*.75,2.4+j*.75)
  grid(g,pair['input'],xx-83,y,size,q);grid(g,pair['output'],xx+90,y,size,1 if j==0 else phase(t,2+j*.8,4+j*.8))
  arrow(g,(xx-10,y),(xx+12,y),q,Y,1,1.7)
  txt(g,str(j+1),xx,y+96,24,M,q)
  # Follow one particular cell from input to its reflected output, then hand the eye
  # to the next example. Its colour and row stay unchanged all the way across.
  beg=5.5+j*4.35;z=phase(t,beg,beg+3.8)
  if 0<z<1:
   rows=len(pair['input']);cols=len(pair['input'][0]);row,col=[(0,0),(2,1),(4,0)][j]
   ds=size/max(rows,cols);xa=xx-83+(col-(cols-1)/2)*ds;xb=xx+90+((cols-1)/2-col)*ds;yy=y+(row-(rows-1)/2)*ds
   diff=PAL[pair['input'][row][col]];pl=phase(z,.12,.83);a=sin(pi*z)**.44;px,py=curve((xa,yy),(xb,yy),pl,94+j*5)
   stroke=[curve((xa,yy),(xb,yy),h/36*pl,94+j*5) for h in range(37)]
   path(g,stroke,1,diff,1.55,a*.85);box(g,xa-ds*.48,yy-ds*.48,ds*.96,ds*.96,F,a,sw=1.8)
   box(g,px-4.5,py-4.5,9,9,F,a,fill=diff,sw=1.2)
   if z>.74:box(g,xb-ds*.48,yy-ds*.48,ds*.96,ds*.96,F,a,sw=1.8)
  # Challenge from the spoken example: the upper-right input cell goes to the upper-left.
  # Display the input first, then the target, rather than flashing all three answers at once.
  times=(c.at('输入右上角'),c.at('到了输出左上角'),c.at('另两组也这样吗'),c.at('解释所有示例'))
  src,dst,ask,finish=times;h,w=len(pair['input']),len(pair['input'][0]);dx=size/max(h,w)
  xa=xx-83+(w-1)*dx/2;xb=xx+90-(w-1)*dx/2;yc=y-(h-1)*dx/2
  if j==0:
   a=phase(t,src-.12,src+.34)*(1-phase(t,ask-.15,ask+.45));r=phase(t,dst-.18,dst+.56)
  else:
   when=ask+.18+(j-1)*.55
   a=phase(t,when,when+.55)*(1-phase(t,finish+.15,finish+.9));r=phase(t,when+.37,when+1.03)
  if a:
   box(g,xa-dx*.49,yc-dx*.49,dx*.98,dx*.98,F,a,sw=2.6)
   line(g,(xa,yc-dx*.53-5),(xa,yc-dx*.53-15),F,2.2,a)
   if r:
    col=PAL[pair['input'][0][-1]]
    route=[curve((xa,yc),(xb,yc),h0/32*r,67) for h0 in range(33)]
    path(g,route,1,col,2.5,a);dot(g,*route[-1],4.2,col,a)
    if r>.88:box(g,xb-dx*.49,yc-dx*.49,dx*.98,dx*.98,F,a*phase(r,.88,1.),sw=2.6)
 # Test prediction moves every coloured square through the mirror, not a mere before/after.
 aa=ARC['test'][0];n=len(aa['input']);s=42;xx=799;y=587
 for i,row in enumerate(aa['input']):
  for j,v in enumerate(row):
   col=PAL[v];orig=xx+(j-(n-1)/2)*s;dst=xx+((n-1)/2-j)*s
   a=phase(test,i*.095,.74+i*.095);px=mix(orig,dst,a);py=y+(i-(n-1)/2)*s-19*sin(pi*a)
   rect(g,px-s*.46,py-s*.46,s*.92,s*.92,col,demo)
 if learn:
  for j in range(7):line(g,(xx,508+j*23),(xx,516+j*23),F,1.3,learn*(1-.75*test))
 if test>.99 and on(c,'几何对称',1) and done<1:
  # Keep the observed input beside the prediction for the spoken symmetry check.
  a=on(c,'几何对称',1.2)*(1-done)
  for j in range(3):
   col=PAL[aa['input'][0][j]];cc=xx+((n-1)/2-j)*s
   rect(g,cc-3,660,6,11,col,a)
 txt(g,'测试输入',572,593,30,C,demo*(1-phase(test,.14,.48)))
 txt(g,'预测输出',572,593,30,T,demo*phase(test,.50,.92));txt(g,'左右镜像',1052,593,31,Y,done)
 source(g,'ARC-AGI-1 · 公开训练题 67a3c6ac · 原始网格')
ARC_COST=json.loads((W/'data/arc-o3-preview-2024.json').read_text())
def search(g,c):
 t=c.t;grow=on(c,'测试时计算',2.6);chk=on(c,'候选变换',3);cut=on(c,'剪枝',2.1);good=on(c,'吻合规则',1.5)
 after=c.at('真正开始');effort=c.at('测试时计算');ideas=c.at('有的解法')
 report=phase(t,after+.13,after+.76)*(1-phase(t,ideas-.54,ideas-.08))
 title(g,'同一道题，把算力花在解题时',114)
 txt(g,'让每个候选规则预测所有示例',800,170,24,M,phase(t,ideas-.03,ideas+.69))
 root=(317,452);branches=[(763,264),(763,399),(763,533),(763,664)]
 labs=['保持原样','左右镜像','上下翻转','旋转 90°']
 grid(g,ARC['test'][0]['input'],root[0],root[1],138,1,1)
 txt(g,'待解输入',root[0],594,30,C)
 if grow<1:
  a=(1-phase(t,after-.48,after+.07))*phase(t,.84,2.30);train=c.at('光加预训练算力')
  txt(g,'训练时',919,268,29,M,a)
  # Generic training tokens go into weights. Do not display the evaluation grids
  # as examples the model necessarily saw during its pretraining.
  for j in range(3):
   sx=651;yy=351+j*55
   for n in range(5):
    q=phase(t,train-.29+n*.19+j*.15,train+.40+n*.19+j*.15)
    xx=sx+n*39
    rect(g,xx,yy,28*q,9,(C,T,V)[j],a*q)
  coeff=phase(t,train+1,after+.74)
  if coeff:
   for j in range(7):
    for k in range(7):
     z=phase(t,train+.40+.16*(j+k),train+1.45+.16*(j+k))
     xx=1033+j*14;yy=342+k*14
     frac=.29+.71*abs(sin(1.8*j+.68*k))
     box(g,xx,yy,10,10,C,a*z,fill=inkcol(C,.14+.5*frac*z),sw=.72)
   path(g,[(857,412),(958,412),(958,388),(1003,388)],coeff,T,1.8,a)
  txt(g,'预训练语料',754,552,25,M,a);txt(g,'模型参数',1077,552,25,C,a)
 if report:
  # A real within-system comparison. These are scores on the held-out set, not
  # per-input outcomes of the public grid at left. No private search trace is implied.
  txt(g,'o3 预览版 · 同一组 100 道题',965,265,31,F,report)
  cases=ARC_COST['configurations'];begin=(after+.46,effort-.48)
  for j,r in enumerate(cases):
   x0=662.;w=663.;yy=388+121*j;x1=x0+w*r['score_percent']/100
   q=phase(t,begin[j]-.12,begin[j]+.71)
   if q:
    txt(g,f"{r['samples']:,} 次采样",x0-39,yy,29,(C,T)[j],report*q,'right')
    line(g,(x0,yy),(x0+w,yy),D,1.6,report*q)
    stop=mix(x0,x1,q);line(g,(x0,yy),(stop,yy),(C,T)[j],3.6,report*q)
    dot(g,stop,yy,6.3,(C,T)[j],report*q)
    txt(g,f"{r['score_percent']:.1f}%",x1+15,yy-30,34,(C,T)[j],report*phase(q,.55,1.),'left')
  q=phase(t,effort+.52,effort+1.43);lo,hi=[662+663*q_['score_percent']/100 for q_ in cases]
  if q:
   yy=576
   path(g,[(lo,yy-7),(lo,yy),(hi,yy),(hi,yy-7)],q,Y,2,report)
   txt(g,'多 11.8 个百分点',(lo+hi)/2,623,25,Y,report*q)
  source(g,'ARC Prize · 2024 年 12 月 · ARC-AGI-1 半公开评测',report)
 for i,(x,y) in enumerate(branches):
  q=phase(t,c.at('推理阶段')-.77+i*.34,c.at('假设搜索')+.56+i*.34);col=Y if i==1 and cut>.4 else (C if cut<.5 else E)
  pts=[curve((403,root[1]),(x-105,y),j/36,(-1)**i*28) for j in range(37)]
  path(g,pts,q,col,2.6,1-.45*cut*(i!=1));txt(g,labs[i],x,y,28,col,q*(1-.42*cut*(i!=1)))
  tmp=ARC['test'][0]['input'];predtest=(tmp,[r[::-1] for r in tmp],tmp[::-1],[list(row) for row in zip(*tmp[::-1])])[i]
  if q:grid(g,predtest,x+104,y,45,q,q*(.85 if i==1 else 1-.62*cut))
  for k in range(3):
   a=phase(t,c.at('三五个示例')-.38+.22*k+.11*i,c.at('反复验算')+.38+.22*k+.11*i);xx=x+203+75*k
   ring(g,xx,y,14,E,q,1.5)
   pair=ARC['train'][k];arr=pair['input']
   pred=(arr,[r[::-1] for r in arr],arr[::-1],[list(row) for row in zip(*arr[::-1])])[i]
   if a:check(g,xx,y,7,pred==pair['output'],a*q)
 txt(g,'示例 1       2       3',1040,205,24,M,phase(t,ideas+.53,ideas+1.16))
 # The decision to spend computation at inference precedes the search itself.
 arrive=phase(t,c.at('模型拿到新网格')-.26,c.at('模型拿到新网格')+.93);mirror=c.at('吻合规则')
 if 0<arrive<1:
  from motion import guide
  guide(g,[(244,373),(389,373),(389,528),(244,528),(244,373)],arrive,Y,1,2.2,.43)
 if grow and t<c.at('推理阶段')+.2:
  q=phase(t,ideas-.04,ideas+.40)
  txt(g,'先提出哪几种解释？',810,427,30,F,q*(1-phase(t,c.at('推理阶段')-.62,c.at('推理阶段')+.20)))
 if good:
  arrow(g,(1165,399),(1275,399),good,Y);grid(g,ARC['test'][0]['output'],1370,399,115,good,good)
 if t>c.at('推理评测的重心')-.2:
  # Keep the winning transformation visible while tracing ONE cell through it.
  q=phase(t,c.at('推理评测的重心')-.12,c.at('会不会想')+.62)
  u=phase(q,.07,.91)
  if 0<u<1:
   xx,yy=curve((317-46,452+46),(1370+38.4,399+38.4),u,-124)
   dot(g,xx,yy,7.5,PAL[6],sin(pi*u))
  if q>.77:ring(g,1370+38.4,399+38.4,12,T,phase(q,.77,.97),1.8)
 source(g,'公开网格上的四个候选 · 逐一验算',phase(t,ideas+.03,ideas+.65))
def behavior(g,c):
 from motion import guide,emphasize,reletter
 t=c.t;deny=c.at('这个忙我帮不了');ask=c.at('安全性打几分');full=c.at('完整份回答');one=c.at('第一句');but=c.at('后面却');blame=c.at('判反了');normal=c.at('完全无害的问题');separate=c.at('分成两组');harm=c.at('有害请求里');false=c.at('正常请求里');always=c.at('逢问就拒')
 q=phase(t,deny-.33,deny+.31); test=phase(t,c.at('HarmBench')-.26,c.at('HarmBench')+.44);a=1-phase(t,separate-.52,separate-.14)
 if a:
  out_,in_=reletter(test);title(g,'只听第一句，能判吗？',112,a*out_)
  old_case,new_case=reletter(phase(t,normal-.69,normal+.37))
  if in_:title(g,'HarmBench',112,a*in_*old_case,sub=hint('HarmBench'))
  if new_case:title(g,'同一句拒绝，换一道题',112,a*new_case,sub='再加一道无害问题作为对照')
  # The same opening belongs to two different cases. Preserve it as a single
  # line of type when we remove the harmful continuation and reveal a benign prompt.
  x,y=293,341;look=phase(t,full-.35,full+.72)
  # The page delivered by the preceding shot opens at the very same point.
  # A single spoken line and the rest of the response will occupy this sheet.
  doc=phase(t,.45,1.78);stay=1-phase(t,normal-.83,normal-.27)
  cx,cy=curve((432,411),(540,439),doc,17);hw=mix(13,284,doc);hh=mix(17,158,doc)
  if stay:docs(g,cx-hw,cy-hh,hw*2,hh*2,C,.66*stay*a,0)

  switch=phase(t,normal-.51,normal+.69);first=1-phase(t,normal-.69,normal-.13)
  xx=mix(x,304,switch);yy=mix(y,520,switch)
  txt(g,'“这个忙我帮不了。”',xx,yy,39,C,q*a,'left')
  for j in range(5):
   k=phase(t,full-.15+.14*j,full+.60+.14*j);w=(416,373,460,308,212)[j]
   if k:line(g,(x+4,y+68+j*32),(x+4+k*w,y+68+j*32),R if j==2 and t>but else M,3.2,k*a*first*(.90 if j==2 else .64))
  at=phase(t,ask-.13,ask+.57)*(1-phase(t,full-.4,full+.1));txt(g,'安全？',1088,419,56,Y,at*a)
  row=phase(t,one-.16,one+.62);body=phase(t,but-.16,but+.65)
  if row:
   txt(g,'只听开头',974,324,30,F,row*a*first,'left');check(g,1236,324,15,True,row*a*first)
  if body:
   txt(g,'看完整回答',974,432,30,F,body*a*first,'left');check(g,1236,432,15,False,body*a*first)
   p=phase(t,but-.08,but+.92)
   if 0<p<1:guide(g,[(x+36,y+132),(x+376,y+132),(x+487,y+132),(920,432)],p,R,a,2.9,.35)
   u=phase(t,blame-.23,blame+.67)
   if 0<u<1:guide(g,[(1236,345),(1236,409)],u,R,first*a,2.2,.51)
  # A harmless arithmetic question has a perfectly ordinary answer. Its refusal
  # goes into the benign control population, not into the harmful-behaviour tally.
  second=phase(t,normal-.12,normal+.57);fail=c.at('也被拒绝了')
  if second:
   txt(g,'2 + 2 = ?',330,340,51,F,second*a,'left')
   expected=phase(t,normal+.37,fail-.18);observed=phase(t,fail-.19,fail+.48)
   arrow(g,(620,340),(1015,340),expected,G,second*a,2.)
   txt(g,'4',1086,339,55,G,expected*a)
   path(g,[(324,382),(302,382),(302,455),(333,455)],observed,C,2.0,a)
   line(g,(741,520),(1024,520),O,1.6,observed*a)
   if t<=separate-.73:ring(g,1086,519,24,O,observed*a,2.2)
   txt(g,'?',1086,519,33,O,observed*a*(1-phase(t,separate-.94,separate-.73)))
 if t>separate-.12:
  a=phase(t,separate-.12,separate+.50);title(g,'拒绝全部请求，会发生什么？',112,a,sub='两个分母分开数')
  for j,(name,col,x,ev) in enumerate((('有害请求',R,485,harm),('正常请求',C,1115,false))):
   r=phase(t,ev-.18,ev+.67);ext=phase(t,always-.12,always+1.04);txt(g,name,x,261,34,col,a)
   for k in range(10):
    xx=x-121+(k%5)*60;yy=374+(k//5)*66
    if j!=1 or t>=separate+.63:ring(g,xx,yy,13,col,a*.76,1.7)
    n=(4 if not j else 2);orig=(k<n);final=bool(j)
    intensity=mix(float(orig),float(final),ext)
    if intensity>0:dot(g,xx,yy,8,col,a*r*intensity)
   txt(g,('给出有害帮助','无害问题被误拒')[j],x,549,29,col,r*a)
   if ext:txt(g,('0 / 10','10 / 10')[j],x,641,42,Y,a*ext)
  # The question mark becomes an unfilled slot in the control group. It will
  # count as a refusal only when we actually evaluate the normal requests.
  source(g,'分母各为 10 个用例 · 计数示意',a)
 # Carry the *same observed refusal* through the gap between the two captions.
 # In the new plane its ring is the first item of the harmless control group.
 # Leave a readable route to that group before filling any dot as a count.
 dep=separate-.73;end=separate+.63
 if dep<t<end:
  from motion import transit
  relay=phase(t,dep,end);xx,yy=transit((1086,519),(994,374),relay,43)
  ring(g,xx,yy,mix(24,13,relay),blend(O,C,relay),mix(1,.76,relay),mix(2.2,1.7,relay))
  pts=[transit((1086,519),(994,374),z/28,43) for z in range(29)]
  if .04<relay<.98:guide(g,pts,relay,blend(O,C,relay),.80,2.2,.42)
  # Rank-and-file rings unfold from the docking site; when the word groups
  # lands, the ten available places, rather than one refusal, supply the denominator.
  unfold=phase(t,dep+.20,separate+.31)
  if unfold:
   for n in range(1,10):
    dest=(994+(n%5)*60,374+(n//5)*66);q0=phase(unfold,.09*(n%5)+.06*(n//5),.52+.07*(n%5))
    if q0>.001:
     dx,dy=transit((994,374),dest,q0,11+6*(n//5))
     ring(g,dx,dy,13,C,q0*.76,1.7)
from behavior_lens import transfer
