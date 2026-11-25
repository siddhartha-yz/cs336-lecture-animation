"""One wrong final token grows into a four-way exam; the remaining headroom becomes four answer slots."""
from termnotes import hint
from ink import *
from motion import *
def choice_row(g,xs,y,ws,letters,vis,sel=-1):
 for j,(x,w,ch,k) in enumerate(zip(xs,ws,letters,vis)):
  if k<.002:continue
  col=Y if j==sel else M
  box(g,x-w/2,y-34,w,68,col,k,fill=inkcol(col,.11 if j==sel else .02),sw=2.2 if j==sel else 1.3)
  txt(g,ch,x,y,34,col,k)
def saturation(g,c):
 t=c.t;question=c.at('那道算术题');pick=c.at('最后选了哪一项');exam=c.at('标准化考试');key=c.at('标准答案');auto=c.at('自动批改');nm=c.at('MMLU');disc=c.at('五十七个学科');data=c.at('公开试卷');sat=c.at('基准饱和');offer=c.at('区分度找回来')
 # A checkmark survives the sandbox. It says probabilities sum to one, not that the answer is right.
 seed=1-phase(t,question-.55,question-.04)
 if seed:
  for j,(n,col) in enumerate(zip(('字节','分域','概率和'),(C,V,T))):
   a=phase(t,.34+j*.48,1.07+j*.48)
   ring(g,520+j*280,411,27,col,seed*a,2);check(g,520+j*280,411,9,True,seed*a)
   txt(g,n,520+j*280,503,30,col,seed*a)
 show=phase(t,question-.46,question+.35);old=1-phase(t,data-.58,data-.16)
 heading=phase(t,nm-.30,nm+.39);old_head,new_head=reletter(heading)
 if show*old:
  a=show*old
  title(g,'只判最后的选择',111,a*old_head,sub='整句平均值，把这一步也平均进去了')
  clean=phase(t,exam-.25,exam+.68);s=phase(t,pick-.53,pick+.45)
  txt(g,'9 − 7 = ?',800,mix(312,269,clean),63,F,a*(1-phase(t,disc-.53,disc-.05)),font='Latin Modern Math')
  subjects=phase(t,disc-.22,disc+1.03)
  explain=phase(t,pick-.33,pick+.57)*(1-phase(t,exam-.47,exam-.15))
  if explain:
   # These are the actual competing argmaxes on the sentence seen before the sandbox.
   for ch,x,yy,col in [('基座选 3',899,566,C),('指令版选 2',698,635,V)]:
    txt(g,ch,x,yy,27,col,a*explain)
    tx=(858 if col==C else 741);path(g,[(x,yy-24),(x,yy-41),(tx,484)],explain,col,1.5,a)

  for j,(label,col) in enumerate((('历史',O),('代数',C),('伦理',V))):
   xx=800+(j-1)*385*subjects;yy=414
   if j!=1 and subjects<.002:continue
   q=a*(subjects if j!=1 else 1)
   if subjects:txt(g,label,xx,285,33,col,q*subjects)
   xs=[xx+(n-1.5)*mix(117,60,subjects) for n in range(4)]
   if j==1 and subjects<.999:
    # The measured prompt really offered only two candidates: two and three.
    # Do not invent two extra responses while recapping that experiment.
    choice_row(g,xs[1:3],yy,[mix(95,49,subjects)]*2,'23',[q*(1-phase(subjects,.04,.47))]*2,0 if s>.6 else -1)
   if subjects>.01:
    aa=q*phase(subjects,.49,.88);choice_row(g,xs,yy,[mix(95,49,subjects)]*4,'ABCD',[aa]*4,(1,1,3)[j] if s>.6 else -1)
   if clean>.005 and subjects<.005 and j==1:
    # A result is a physical mark at the chosen cell; the key occupies its own lane.
    check(g,xs[1],515,14,True,a*phase(t,auto-.13,auto+.45))
    txt(g,'答案：2',800,579,28,T,a*phase(t,key-.1,key+.46))
   elif subjects:check(g,xs[(1,1,3)[j]],499,11,True,q*subjects)
 title(g,'MMLU',111,new_head,sub=hint('MMLU'))
 for j in range(57):
  p=phase(t,disc-.24+j*.027,disc+.30+j*.027)
  if p:
   xx=170+j*22.5;yy=654;col=(C,O,V,T,G)[j//12%5]
   line(g,(xx,yy),(xx,yy-32*settle(p)),col,4.6,p*(.82-.36*(1-old)))
 if old:txt(g,'一格，一门学科',800,709,24,M,phase(t,disc,disc+1.47)*old)
 chart=phase(t,data-.08,data+.80);trigs=[c.at('从 GPT-4')+.2,c.at('到 GPT-4o')+.18,c.at('再到 GPT-4.1')+.28]
 yy=lambda z:555-(z-60)*7.42;xs=(424,798,1171);vals=(84.7,88.7,90.2);cols=(C,T,Y)
 if chart:
  for n in (60,70,80,90,100):
   y=yy(n);line(g,(231,y),(1375,y),M if n==100 else E,1.5 if n==100 else 1,chart*(.86 if n==100 else .58));txt(g,f'{n}%',209,y,23,M,chart,'right')
  for j,(x,v,col,ta) in enumerate(zip(xs,vals,cols,trigs)):
   k=phase(t,ta-.16,ta+.66);y=yy(v)
   if not k:continue
   h=settle(k);vy=mix(yy(60),y,h)
   line(g,(x,yy(60)),(x,vy),col,2.3,k*.70);dot(g,x,vy,8,col,k)
   txt(g,('GPT-4','GPT-4o','GPT-4.1')[j],x,601,27,F,k)
   txt(g,f'{v:.1f}%',x,vy-32,37,col,phase(k,.44,1))
  rem=phase(t,c.at('空间越来越小')-.3,c.at('空间越来越小')+.64)
  if rem:
   xt=1317;top=yy(100);bottom=yy(90.2)
   path(g,[(xt-11,top),(xt,top),(xt,bottom),(xt-11,bottom)],rem,Y,2.8,1)
   txt(g,'余量',xt+19,(top+bottom)/2,21,Y,rem,'left')
  if t>sat-.23:
   phase1=phase(t,sat-.23,sat+.87);guide(g,[(xs[2]-88,yy(vals[2])+5),(xs[2]-10,yy(vals[2])+5),(xs[2]+61,yy(vals[2])+5)],phase1,Y,1,2.8)
   txt(g,'基准饱和',800,715,33,Y,phase1)
  source(g,'OpenAI simple-evals · 零样本 MMLU · 三次独立测量',chart)
def mmlu_pro(g,c):
 t=c.t;clean=c.at('第一刀');expand=c.at('现在最多十个');chance=c.at('均匀盲猜');multi=c.at('第三刀');routes=c.at('先推理再选择');replace=c.at('效果真的不同');end=c.at('同一批模型')
 title(g,'MMLU-Pro',110,sub=hint('MMLU-Pro'))
 # Two readers inspect the SAME page; each rejection is synchronized to its stated reason.
 review=c.at('人工和模型');ambigu=c.at('表述含糊');double=c.at('存在歧义');miskey=c.at('标错答案');drop=c.at('彻底剔除');second=c.at('第二刀')
 yy=254;rowop=1-phase(t,multi+.08,multi+.92)
 js=(4,10,17);cues=(ambigu,double,miskey)
 def sheet(i):return 176+i*54
 for i in range(23):
  x=sheet(i);bad=i in js;j=js.index(i) if bad else 0
  select=phase(t,cues[j]-.16,cues[j]+.40) if bad else 0.
  u=phase(t,drop-.28+j*.12,drop+.78+j*.12) if bad else 0.
  y=yy-46*u;a=rowop*(1-u)
  col=blend(C,R,select)
  box(g,x,y,36,46,col,a,fill=inkcol(col,.13 if select else .065))
  for n in range(3):line(g,(x+6,y+12+8*n),(x+28-(n*i%7),y+12+8*n),col,1.3,a)
  if select>0:line(g,(x+5,y+35),(x+31,y+11),R,2.2,a*select)
 # The sweep consists of distinct readers and observable marks, not a decorative scanner.
 read=phase(t,review-.12,review+.55)*(1-phase(t,drop-.3,drop+.2))
 if read:
  x=sheet(js[0])+18
  x=mix(x,sheet(js[1])+18,phase(t,double-.43,double+.03))
  x=mix(x,sheet(js[2])+18,phase(t,miskey-.43,miskey+.03))
  sweep=phase(t,review-.15,ambigu-.10)
  x=mix(sheet(0)+12,x,sweep)
  voter(g,x-12,yy-33,T,read,.63);g.poly([(x+13,yy-48),(x+24,yy-37),(x+13,yy-26),(x+2,yy-37)],V,1.5,read,True,inkcol(V,.10),1)
  for i,(lab,at) in enumerate(zip(('表述含糊','多种解释','答案误标'),cues)):
   v=phase(t,at-.09,at+.40);px=sheet(js[i])+18
   txt(g,lab,px,332,22,R,read*v)
 scrub=phase(t,drop-.07,drop+.64)
 if scrub:txt(g,'留下能判定的题',800,331,23,M,scrub*rowop)
 give=c.at('直接交一个字母');transfer=phase(t,give+.04,give+.95)
 low=1-phase(t,give+.08,give+.54)
 # Old letters have stable identities. D vacates the new E location BEFORE E is ever painted.
 if low:
  x0=231;span=1138;yy=434;prog=phase(t,expand-.38,expand+.48)
  for j in range(4):
   k=phase(prog,.025*j,.88+.025*j)
   oldx=x0+(j+.5)*span/4;newx=x0+(j+.5)*span/10
   x=mix(oldx,newx,k);w=mix(span/4-12,span/10-8,k)
   choice_row(g,[x],yy,[w],'ABCD'[j],[low],0 if j==0 else -1)
  for j in range(4,10):
   q=phase(t,expand+.49+(j-4)*.09,expand+.90+(j-4)*.09);x=x0+(j+.5)*span/10
   if q:choice_row(g,[x],yy+18*(1-settle(q)),[span/10-8],'ABCDEFGHIJ'[j],[q*low],-1)
  third=phase(t,multi-.18,multi+.53)
  if third<1:
   a=low*(1-third)
   txt(g,'均匀盲猜',545,620,29,M,a)
   # Only eligible choices count. There was no 22% intermediate four/ten-item exam.
   if t<expand-.28:txt(g,'1 / 4  =  25%',905,613,46,Y,a)
   elif t>=expand+1.46:txt(g,'1 / 10  =  10%',905,613,46,Y,a)
   else:
    for h in range(10):
     xx=799+h*23;k=phase(t,expand-.35+h*.11,expand+.08+h*.11)
     line(g,(xx,622),(xx,622-24*k),Y,3.2,a*k)
 # One letter and one worked route now enter the two rows of the same experiment.
 # Crucially, the reasoning chain stays in its own lane while the direct score grows.
 for j,(tx,lab,col) in enumerate(((375,'条件',C),(630,'推断',T),(895,'检验',T),(1165,'选择',Y))):
  q=phase(t,multi+j*.68,multi+.75+j*.68);u=phase(t,routes-.52+j*.08,routes+.37+j*.08)
  before=1-phase(u,.02,.48)
  txt(g,lab,tx,619,31,col,q*before)
  if j:arrow(g,(tx-166,619),(tx-64,619),q,col,q*before,2.5)
  if 0<u<1:
   xx,yp=transit((tx,619),(504,490),u,(-27,32,49,62)[j])
   dot(g,xx,yp,5.7,blend(col,C,u),q*phase(u,.02,.29))
 if 0<transfer<1:
  xx,yp=transit((287.9,434),(504,405),transfer,43)
  ring(g,xx,yp,mix(22,6.5,transfer),blend(Y,O,transfer),1,2.1)
  dot(g,xx,yp,5.3,blend(Y,O,transfer),transfer)
 table=phase(t,give+.47,give+1.04)
 if table:
  switch=phase(t,c.at('换一张卷子')-.17,c.at('换一张卷子')+.64)
  # First comparison: same model and exam, only its prompting changes.
  if switch<1:
   alpha=table*reletter(switch)[0];txt(g,'GPT-4o',800,270,39,F,alpha)
   for j,(lab,v,col) in enumerate((('直接选',53.5,O),('先推理再选',72.6,C))):
    y=405+j*85;row=phase(t,routes-.10,routes+.49) if j else 1
    txt(g,lab,443,y,28,col,alpha*row,'right')
    start_cd=routes+.56 if j else give+.95
    grow=phase(t,start_cd,start_cd+.74)
    xx=504+v*9.2*grow;line(g,(504,y),(xx,y),col,6,alpha*row)
    if not j or switch==0:dot(g,xx,y,7,col,alpha*row)
    if not j or switch==0:txt(g,f'{v:.1f}%',xx+23,y,29,col,alpha*grow,'left')
   txt(g,'同一张 MMLU-Pro，换作答方式',800,657,27,M,alpha*phase(t,routes+.13,routes+.64))
  # The 72.6% reading is the very same GPT-4o / Pro / CoT point in
  # the next figure. Carry the observation across, not a generic transition.
  pro_y=610-(72.6-55)*7.6;landing=end+.99
  if switch and t<landing+.09:
   xx,yp=transit((504+72.6*9.2,490),(1096,pro_y),switch,29)
   dot(g,xx,yp,6.8,C,1);txt(g,'72.6%',xx+mix(23,24,switch),yp,29,C,1,'left')
   if 0<switch<1:ring(g,xx,yp,10+5*sin(pi*switch),C,.75*sin(pi*switch),1.8)
  # Second comparison: two model identities and a common CoT setup, across the two tests.
  if switch:
   a=reletter(switch)[1];old_x,new_x=504,1096
   # Same 55–95% vertical scale on both sides. Insets label close readings without shifting the data.
   yy=lambda percent:610-(percent-55)*7.6
   for x,cap in ((old_x,'MMLU'),(new_x,'MMLU-Pro')):
    line(g,(x,274),(x,621),E,1.4,a);txt(g,cap,x,236,31,F,a)
    for v in (60,70,80,90):line(g,(x-6,yy(v)),(x+6,yy(v)),M,1.2,a*.82)
   for j,(name,v,w,cl) in enumerate([('GPT-4o',88.7,72.6,C),('GPT-4 Turbo',86.5,63.7,V)]):
    y1=yy(v);y2=yy(w)
    pos=phase(t,end-.11+j*.22,end+.99+j*.22)
    if pos:
     x=mix(old_x,new_x,pos);y=mix(y1,y2,pos)
     line(g,(old_x,y1),(x,y),cl,2.5,a)
     dot(g,x,y,6.8,cl,a)
    dot(g,old_x,y1,6,cl,a)
    ylab=y1+(-23 if j==0 else 23);lx=old_x-47
    g.poly([(old_x-8,y1),(old_x-26,y1),(lx,ylab)],cl,1.25,a)
    txt(g,f'{name}  {v:.1f}%',lx-10,ylab,26,cl,a,'right')
    if pos>.4 and (j or t>=landing+.09):
     k=phase(pos,.4,1);txt(g,f'{w:.1f}%',new_x+24,y2,29,cl,a*k,'left')
   gap=phase(t,c.at('挤在一起')-.15,c.at('挤在一起')+.70)
   if gap:
    for x,v,w in ((old_x+41,88.7,86.5),(new_x-42,72.6,63.7)):
     ya,yb=yy(v),yy(w)
     g.poly([(x-5,ya),(x,ya),(x,yb),(x-5,yb)],Y,1.8,a*gap)
    txt(g,'两者的差距：2.2 → 8.9 个百分点',800,673,30,Y,a*gap)
   else:txt(g,'都先推理再选，换考卷',800,673,27,M,a)
  source(g,'Wang 等 · 表 3 · 同实验的整体准确率',table)
