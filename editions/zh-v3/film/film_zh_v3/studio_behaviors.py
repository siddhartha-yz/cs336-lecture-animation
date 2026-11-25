"""A safety result is attached to a complete answer. Track the same cases across conditions."""
from ink import *
from ink_words import letter,swish,carryword
from studio_examples import pstep,silk,area,mark,BLUE,VIO
from motion import transit,guide
from termnotes import hint
def cubic(p,q,r,s,u):
 v=1-u;return(v**3*p[0]+3*v*v*u*q[0]+3*v*u*u*r[0]+u**3*s[0],v**3*p[1]+3*v*v*u*q[1]+3*v*u*u*r[1]+u**3*s[1])
def bez(g,pts,sw,col,op=1):
 z=g.c;z.new_path();z.move_to(*pts[0]);z.curve_to(*pts[1],*pts[2],*pts[3]);z.set_line_width(sw);g.source(col,op);z.stroke()
def refusal(g,c):
 t=c.t;first=c.at('这个忙');eye=c.at('先把第一句');look=c.at('再往下读');name=c.at('HarmBench');result=c.at('完整回答');body=c.at('后文却给了');not_=c.at('只数开头');wrong=c.at('正好判反');benign=c.at('一道无害');cost=c.at('变成了误拒');two=c.at('分成两组');risk=c.at('实际给出有害帮助');den=c.at('被误拒的比例');all_=c.at('逢问就拒');fee=c.at('马上把代价')
 # Start on one line anyone could read aloud. It then forks into two distinct judgements.
 intro=phase(t,.14,.69);split=phase(t,benign-.5,benign+.41);close=phase(t,two-.47,two+.35);old=1-close
 if old:
  front=1-phase(t,name-.51,name-.14)
  if front:silk(g,'先读第一句',800,108,45,t-.10,F,front*old)
  if not front or t>name-.4:silk(g,'HarmBench',140,103,53,t-name+.24,F,old,'pen','left');silk(g,'用整份回答判断有害行为是否发生',142,163,25,t-name-.2,M,old,align='left')
  x=mix(800,465,split);y=mix(390,337,phase(t,look-.1,look+.66))
  silk(g,'“这个忙我帮不了。”',x,y,53,t-first+.1,F,intro*old)
  swish(g,x-196,x+174,y+48,t-eye+.05,Y,.63)
  if t>=look-.19:
   k=pstep(t,look-.19,.65);line(g,(x-224,y+67),(x+224,y+67),C,1.7,k*old)
   obj=pstep(t,body-.18,.56);op=k*old
   # Annotations reveal just the outcomes of a full review, not an example of harmful assistance.
   txt(g,'首句：拒绝',x,y+123,32,T,op)
   if obj:
    txt(g,'后文：仍提供了有害帮助',x,y+190,31,R,op*obj)
    path(g,[(x-245,y+99),(x-258,y+99),(x-258,y+193),(x-245,y+193)],obj,R,2,op)
   if t>=wrong-.14:silk(g,'行为发生',x,669,37,t-wrong+.14,R,old)
  if split:
   xx=1138;silk(g,'“帮我合并两份会议记录。”',xx,291,31,t-benign+.15,C,old)
   # Re-use the actual rejection, not a stock document icon.
   f=pstep(t,benign+.20,.86)
   if f:
    carryword(g,'“这个忙我帮不了。”',(800,404),(xx,418),f,36,36,F,72,old*f)
   if t>cost-.10:
    silk(g,'正常请求被误拒',xx,610,34,t-cost+.1,O,old);swish(g,1020,1250,650,t-cost,O,.50)
   line(g,(800,267),(800,649),E,1.2,split*old)
 if close:
  op=close
  silk(g,'同一策略，两种代价',132,102,48,t-two+.38,F,op,align='left')
  text='全都拒绝' if t>=all_-.16 else '分开计数'
  for j,(head,sub,col,key) in enumerate((('有害请求','得到有害帮助',R,risk),('正常请求','遭到误拒',O,den))):
   x=442+j*695;prog=pstep(t,two-.10+j*.22,.6);at=pstep(t,key-.2,.47);alt=phase(t,all_-.2,fee+.15)
   if not prog:continue
   silk(g,head,x,248,38,t-two+.18-j*.22,F,op)
   # Ten marks form a unit of proportion. Their shape is a tally, not ten mini documents.
   a=op*prog
   for k in range(10):
    x0=x-221+k*49;ix=phase(t,key-.18+k*.035,key+.31+k*.035);y0=416
    f=(1-alt if j==0 else alt)
    h=(92 if ((k in (0,1,2)) if j==0 else (k in (0,))) else 13)*(1-alt)+(13 if not j else 92)*alt
    if ix:rect(g,x0,y0-h,28,h,col if h>15 else '#747474',a*ix)
    line(g,(x0-1,y0+10),(x0+28,y0+10),M,1.25,a)
   txt(g,sub,x,491,32,col,at*a)
   if t>=fee-.45:silk(g,('0 / 10','10 / 10')[j],x,596,53,t-fee+.35,col,a,'pen')
  line(g,(644,701),(953,701),E,1.45,op);txt(g,'全拒策略 · 十题示意' if t>=all_-.1 else '两组各十题 · 示意',800,667,24,M,op)
def replication(g,c):
 t=c.t;name=c.at('GCG');share=c.at('会说什么');whole=c.at('实际做了什么');ident=c.at('开头那两个字');after=c.at('后面的行为');paper=c.at('HarmBench');cond=c.at('同一套协议');four=c.at('约四倍');cases=c.at('二十道题');pair=c.at('两次结果对');gold=c.at('这三条金线');both=c.at('都出了问题');eight=c.at('八道');keep=c.at('金线还在');frac_=c.at('三条占八条');real=c.at('带出考场')
 turn=phase(t,paper-.5,paper+.14);turn2=phase(t,cases-.57,cases+.25)
 if turn<1:
  op=1-turn
  from mounting import etch
  from studio_science import polycurve
  # A weaving loom of paired *test cases*, not an attack apparatus. A single case comes into
  # the foreground and the two outcome ribbons keep its colour. All twenty remain counted.
  focus=phase(t,name-.58,name+.55);open_=phase(t,share-.64,whole+.41);beg=phase(t,.02,.55)
  sx,sy=225,439;key=8;forms=[]
  for j in range(20):
   u=pstep(t,.03+j*.043,.50)
   if not u:continue
   ye=161+j*22.6;xx=128+j*2.2;col=Y if j==key else (C if j%3 else VIO)
   path0=((xx,ye),(xx+216,ye-29),(494,405+(j-9.5)*6.2),(615,408+(j-9.5)*6.2))
   val=op*u*(1-.70*focus if j!=key else 1)
   tip=polycurve(g,path0,col,4.7 if j==key else 2.5,val,u);dot(g,xx,ye,7.1 if j==key else 4.3,col,val)
   if j==key:
    if .1<t<ident:dot(g,*cubic(*path0,(t*.24)%1),6.2,F,val*.87)
    etch(g,'同一用例',xx-17,ye,24,Y,op*focus,'right')
  # Same complete input set, one change of experimental condition; never manufacture probabilities.
  for j,co in enumerate((C,VIO)):
   yy=278+261*j
   q=pstep(t,.35+j*.18,.74)
   pts=((580,405),(649,409),(659,yy),(755,yy));polycurve(g,pts,co,3.3,op*q,q)
   if q:dot(g,755,yy,8,co,op*q)
   if not j:
    etch(g,'常规测试',755,yy-39,29,C,op*q)
   else:
    etch(g,'GCG 压力条件',752,yy+49,31,VIO,op*focus)
    etch(g,'用梯度构造的对抗测试',752,yy+88,24,M,op*focus)
   if open_:
    # Identical prefix written on the two actual output traces, evidence only after opening.
    px=mix(842,889,open_);etch(g,'“好的”',px,yy,40,Y,op*open_)
    q2=pstep(t,whole-.20+j*.18,.67);dy=(-88,44)[j]
    pts=((px+128,yy),(1080,yy),(1090,yy+dy),(1203,yy+dy))
    polycurve(g,pts,(T,R)[j],4.4,op*q2,q2)
    if q2:
     etch(g,('后文仍然拒绝','后文给了有害帮助')[j],1209,yy+dy,30,(T,R)[j],op*q2)
    if ident-.2<t<after+.75:
     zz=phase(t,ident-.17+j*.15,after+.64+j*.15)
     if 0<zz<1:dot(g,*cubic(*pts,zz),8,Y,op)
  if t>after-.24:
   swish(g,1206,1454,621,t-after+.16,R,.55)
 if turn and turn2<1:
  op=turn*(1-turn2);silk(g,'同一协议下的行为发生率',140,98,46,t-paper+.32,F,op,align='left');txt(g,'三种 GCG 条件取平均',142,156,26,M,op,'left')
  st=cond-.15;barx=479
  for i,(nm,col,n)in enumerate((('Llama 2 13B',C,4),('Zephyr + R2D2',T,1))):
   y=343+175*i;pr=pstep(t,st+i*.24,.82)
   txt(g,nm,428,y,34,F,op*pr,'right')
   for j in range(4):
    x=barx+j*194
    if j<n:
     u=pstep(t,st+(j*.09 if not i else .24),.70)
     rect(g,x,y-31,184*u,62,inkcol(col,.78),op*u)
     line(g,(x,y-31),(x+184*u,y-31),col,2.8,op*u)
    else:line(g,(x,y+31),(x+184,y+31),E,1.0,op*pr*.63)
   txt(g,'1.00' if not i else '≈ 0.25',1302,y,35,col,op*pr,'left')
  txt(g,'以上行作 1；比较的是相对发生率。',800,681,29,M,op)
  # The reported comparison averages three experimental conditions. Three marks
  # share equal weight; no per-condition ASRs are fabricated.
  three=c.at('三种 GCG');mean=c.at('取平均')
  r=phase(t,three-.18,three+.46)
  if r:
   for j in range(3):
    x=786+j*72;yy=633
    pr=pstep(t,three-.16+j*.12,.48);merge=phase(t,mean-.09,mean+.73)
    if pr:
     x2,y2=transit((x,yy),(867,602),merge,12+j*4)
     ring(g,x2,y2,9.3,VIO,op*pr,2.1)
   if merge:swish(g,824,902,611,t-mean+.08,VIO,.54)
  if t>four-.18:swish(g,480,1247,397,t-four+.18,Y,.69)
 if turn2:
  op=turn2;sub=phase(t,eight-.20,eight+.84);highlight=pstep(t,gold-.19,.61);show=pstep(t,pair-.37,1.34)
  Aset=(1,3,5,7,10,13,15,18);shared=(3,10,18);Bset=(3,10,18,8,16)
  silk(g,'同一道题，在两次测量之间',136,99,45,t-cases+.36,F,op,align='left');txt(g,'20 道配对用例 · 示意',137,161,24,M,op,'left')
  xa,xb=320,1063;top=279;dy=19.6
  share_end=c.at('重现的比例');tally=phase(t,frac_-.18,frac_+1.0)
  for j in range(20):
   A=j in Aset;B=j in Bset;h=j in shared;ix=phase(t,cases-.18+j*.026,cases+.48+j*.026)
   if not ix:continue
   a=op*ix*(1-sub*(0 if A else 1))*(1-.81*tally)
   if a<.002:continue
   arank=(list(Aset)+[n for n in range(20)if n not in Aset]).index(j)
   brank=(list(Bset)+[n for n in range(20)if n not in Bset]).index(j)
   aa=mix(top+arank*dy,286+(Aset.index(j)if A else 0)*45,sub)
   order=list(shared)+[n for n in Aset if n not in shared]
   bb=mix(top+brank*dy,286+(order.index(j)if A else 0)*45,sub)
   color=Y if h and highlight>.12 else (C if A else '#555555')
   if not h:a*=1-highlight*.47 if A else 1-highlight*.66
   if A and not h:color=BLUE
   dot(g,xa,aa,5.7 if A else 3.5,color,a);en=(xb,bb);pts=((xa,aa),(xa+285,aa),(xb-280,bb),en)
   f=clip((show-j*.014)/.728)
   if f>=.999:bez(g,pts,5.4 if h else 3.35,color,a)
   elif f>0:path(g,[cubic(*pts,f*z/24)for z in range(25)],1,color,4,a)
   if f>=.999:dot(g,xb,bb,5.7 if h else 4.4,color,a)
   if h and highlight:
    k=phase(t,gold-.17+shared.index(j)*.16,both+.43+shared.index(j)*.16)
    if .001<k<.999:dot(g,*cubic(*pts,k),7.5,F,a)
  txt(g,'模型 A',xa,222,28,C,op);txt(g,'模型 B',xb,222,28,T,op)
  measure=pstep(t,gold-.17,.55)
  if measure:
   # One numerator moves a short arc; the denominator actually changes population.
   carryword(g,'3',(1333,373),(1333,406),sub,73,77,Y,11,op)
   line(g,(1275,mix(432,461,sub)),(1391,mix(432,461,sub)),F,2.15,op)
   aa=1-phase(sub,.0,.43);bb=phase(sub,.55,1)
   txt(g,'20',1333,498,49,M,op*aa);txt(g,'8',1333,527,60,C,op*bb)
   tit='全体' if sub<.43 else 'A 出问题的题'
   txt(g,tit,1333,620,25,M,op*(aa+bb))
  if t>=keep-.3:
   # Identifiers enter at the matching far end of their own gold threads.
   v=pstep(t,keep-.3,.64)
   for j,i in enumerate(shared):
    f=pstep(t,keep-.18+j*.16,.47);yy=286+j*45
    if v*f:
     txt(g,f'#{i+1:02d}',xb+22,yy,24,Y,op*v*f,'left')
   if t>=frac_-.15:
    from mounting import etch
    etch(g,'P(B | A)',1333,298,32,F,pstep(t,frac_-.15,.64),'center')
  if tally:
   # Eight paired outcomes turn into eight equal arcs. Preserve the same case identities,
   # not eight newly sampled cases. Gold = event in both protocols.
   order=list(shared)+[ii for ii in Aset if ii not in shared]
   cx=776;cy=458;rr=137;ctx=g.c
   for j,case in enumerate(order):
    co=Y if case in shared else C
    ang=-pi/2+j*tau/8;stop=ang+tau/8-.025
    f=phase(t,frac_-.17+j*.076,frac_+.56+j*.076)
    if f<=0:continue
    mid=(ang+stop)/2;xx=cx+(rr+13)*cos(mid);yy=cy+(rr+13)*sin(mid)
    px,py=transit((xb,286+j*45),(xx,yy),f,47);dot(g,px,py,7,co,op*f)
    ctx.save();ctx.move_to(cx,cy);ctx.arc(cx,cy,rr,ang,ang+(stop-ang)*f);ctx.close_path();g.source(co,op*f*(.84 if j<3 else .35));ctx.fill();ctx.restore()
    arc(g,cx,cy,rr,ang,ang+(stop-ang)*f,co,2.6,op*f)
   ro=phase(t,share_end-.30,share_end+.55)
   if ro:
    from mounting import etch
    etch(g,'同样这八题',cx,cy+rr+53,31,C,op*ro,'center')
   if t>=frac_-.1:swish(g,1264,1397,570,t-frac_+.08,Y,.60)

