from termnotes import hint
from ink import *
from motion import *
# The x-axis is E_A-E_B; the exponent in the conventional Elo denominator is E_B-E_A.
def rating(g,c):
 t=c.t;ret=c.at('极大似然');leave=phase(t,ret-.62,ret-.16);fit=phase(t,ret-.14,ret+.86)
 title(g,'Bradley–Terry  ·  Elo 刻度',107,sub=hint('Bradley–Terry'))
 x0=141;base=601;wide=mix(1230,660,fit);ht=265
 def plot(d):return x0+wide*(d+620)/1240,base-ht/(1+10**(-d/400))
 tr=phase(t,c.at('胜率曲线')-.53,c.at('胜率曲线')+1.23)
 line(g,(x0,base),(x0+wide,base),M,1.65);line(g,(x0,base),(x0,base-ht-32),E,1.65)
 for k in (-400,0,400):
  xx,y=plot(k);line(g,(xx,base),(xx,base+8),M,1.4);txt(g,f'{k:+d}' if k else '0',xx,base+32,23,M)
 txt(g,'A 与 B 的分差',x0+wide/2,695,27,M);txt(g,'A 的胜率',143,266,25,C,1,'left')
 linepts=[plot(-620+1240*j/120) for j in range(121)]
 path(g,linepts,tr,C,3.8)
 same=c.at('积分完全相同');adv=c.at('高出四百分');delta=c.at('先看两人的分差')
 initial=(1-phase(t,same-.32,same+.44))*(-400);d=initial+400*phase(t,adv-.15,adv+.84)
 observed=c.at('真实投票记录');trial=phase(t,observed-.18,observed+1.28);d=mix(d,400*math.log10(3),trial)
 mark=phase(t,delta-.22,delta+.39);xx,y=plot(d)
 line(g,(xx,y),(xx,base),Y,1.55,mark);dot(g,xx,y,7.5,Y,mark);txt(g,f'{100/(1+10**(-d/400)):.1f}%',xx+10,y-30,31,Y,mark)
 begin=phase(t,c.at('Bradley')-.5,c.at('Bradley')+.45)
 form='elo'
 if c.at('减去')-.14<=t<c.at('然后加一')-.12:form='elo_diff'
 elif c.at('然后加一')-.12<=t<c.at('再取倒数')-.12:form='elo_add'
 elif c.at('再取倒数')-.12<=t<c.at('预测胜率')+.36:form='elo_inv'
 look=c.at('看这个分母');zero=c.at('指数为零')
 focus=phase(t,look-.22,look+.52)*(1-phase(t,adv-.25,adv+.55))
 fw=414+102*focus;fx=800-32*focus;fy=236+12*focus;fa=begin*(1-leave)
 # The denominator, not the whole fraction, changes ink. Retain the same
 # TeX box for the highlight, so its baseline and rule never jump.
 if focus<.999:formula(g,form,fx,fy,fw,fa)
 if focus>.001:formula(g,'elo_den',fx,fy,fw,fa*focus)
 # At the worked score difference A-B=-400 the algebra can be watched in actual numbers.
 # The strip occupies the free upper-right region and leaves before the real leaderboard.
 if begin*(1-leave):
  minus=c.at('减去');divide=c.at('除以四百');power=c.at('作为十的指数');plus=c.at('然后加一');inverse=c.at('再取倒数')
  marks=[(minus,'B − A = 400'),(divide,'400 / 400 = 1'),(power,'10¹ = 10'),(plus,'1 + 10 = 11'),(inverse,'1 / 11 ≈ 9.1%')]
  for j,(tm,expr) in enumerate(marks):
   stop=marks[j+1][0] if j+1<len(marks) else same
   a=phase(t,tm-.16,tm+.34)*(1-phase(t,stop-.30,stop-.04))*(1-leave)
   if a:txt(g,expr,1218,232,31,T,a)
  q=phase(t,same-.16,same+.61)*(1-leave)
  if q:
   odds=phase(t,c.at('十比一')-.20,c.at('十比一')+.69);start=1144;wd=152
   if t<adv:
    for j,col in enumerate((C,O)):rect(g,start+j*wd/2,227,wd/2-2,10,col,q)
    txt(g,'1 : 1',1220,268,21,M,q)
    eq=phase(t,zero-.13,zero+.53)*(1-phase(t,adv-.45,adv-.08))
    if eq:txt(g,'1 + 10⁰ = 2',1220,197,29,Y,q*eq,font='math')
   elif odds:
    for j in range(11):rect(g,start+j*wd/11,227,wd/11-2,10,C if j<10 else O,q*odds)
    txt(g,'10 : 1',1220,268,21,M,q*odds)
 # The probability marker leaves its copy on the fitted curve. Its path leads to ratings,
 # not to a fictitious claim that two observations produced the whole leaderboard.
 if fit:
  a=phase(t,ret+.08,ret+.97);arcpts=[transit((xx,y),(1366,287),k/40,67) for k in range(41)]
  if 0<a<1:guide(g,arcpts,a,Y,1,2.15,.21)
  entries=[('Claude Opus 4.7 · thinking',1503),('Claude Opus 4.6 · thinking',1502),('Claude Opus 4.6',1497),('Gemini 3.1 Pro Preview',1493),('Claude Opus 4.7',1491),('Muse Spark',1491),('GPT-5.5 High',1488),('Gemini 3 Pro',1486),('Grok 4.20 Beta 1',1480),('Grok 4.20 · 0309 Reasoning',1477)]
  z=phase(t,ret+.15,ret+.76);txt(g,'Text Arena · 讲义快照',1135,220,30,F,z)
  for i,(name,val) in enumerate(entries):
   k=phase(t,ret+.30+i*.081,ret+.84+i*.081);yy=282+i*42
   line(g,(883,yy+19),(1425,yy+19),D,1.2,k);txt(g,str(i+1),884,yy,21,M,k,'right');txt(g,name,910,yy,22,M if i else F,k,'left',401);txt(g,str(val),1402,yy,25,Y if i==0 else C,k,'right')
  if t>=ret:
   panel=phase(t,ret-.02,ret+.61)
   txt(g,'看一对模型的四票',462,213,23,M,panel)
   for j,col in enumerate((C,C,C,O)):
    f=phase(t,observed-.73+j*.34,observed+.01+j*.34)
    if f:
     px,py=transit((290+j*103,301),(365+j*64,267),f,13)
     dot(g,px,py,7,col,f);txt(g,'A' if j<3 else 'B',px,py+25,17,col,f)
   if trial:txt(g,'最合这四票的胜率：3 / 4',459,338,22,T,trial)
  source(g,'讲义图 203 · 历史榜单 · 同分可并列',z)
def length_lesson(g,c):
 t=c.t;fit=c.at('先拟合');fix=c.at('长度差设成零');mean=c.at('最后取平均');corr=c.at('零点九四');adj=c.at('零点九八');turn=c.at('电脑环境里')
 name=c.at('AlpacaEval');named=phase(t,name-.16,name+.50)
 title(g,'长一点，就更好吗？',110,1-phase(t,name-.58,name-.13),sub='两份回答保持原样')
 title(g,'AlpacaEval 2.0',110,named,sub=hint('AlpacaEval 2.0'))
 x0,x1=191,958;mid=(x0+x1)/2;bottom=620;top=304
 def point(z,j):return mid+.5*(x1-x0)*z,bottom-(bottom-top)/(1+exp(-((.80,-.24,.38)[j]+1.61*z)))
 ln=phase(t,c.at('两份回答的长度差')-.3,c.at('两份回答的长度差')+.9);model=phase(t,fit-.24,fit+.97)
 line(g,(x0,bottom),(x1,bottom),M,1.55);line(g,(x0,bottom),(x0,top-24),M,1.55)
 for i,(lab,x) in enumerate((('−',x0+40),('0',mid),('+',x1-40))):
  line(g,(x,bottom-5),(x,bottom+6),M,1.4);txt(g,lab,x,650,22,Y if i==1 else M)
 txt(g,'回答长度差（A − B）',mid,700,28,M);txt(g,'A 胜出：判决 / 概率',x0,242,24,M,1,'left')
 if model<1:
  for j,(n,col) in enumerate(((4,C),(7,V))):
   for k in range(n):
    p=phase(t,.9+j*.57+k*.18,1.6+j*.57+k*.18);rect(g,345+k*62,385+j*69,52*p,12,col,(1-model)*.94)
   txt(g,'回答 '+('A','B')[j],305,391+j*69,24,col,1-model,'right')
  bracket(g,593,512,186,Y,ln*(1-model))
  intro=1-phase(t,c.at('胜负判断')-.52,c.at('胜负判断')+.11)
  if intro:
   diff=c.at('长度红利');stat=c.at('长度控制回归');gg=phase(t,diff-.26,diff+.71)
   if gg:
    # A has four occupied slots and B has seven. We never cut B to match A.
    xp=345+4*62;span=3*62-10
    bracket(g,xp,508,span,Y,gg*intro)
    tag=phase(t,c.at('剥离出来')-.16,c.at('剥离出来')+.48)
    txt(g,'4 − 7  =  −3',1173,441,41,Y,tag*intro)
    prog=phase(t,stat-.26,stat+1.34)
    if prog:
     x,y=transit((1173,478),(mid-163,bottom-7),prog,-42)
     dot(g,x,y,6,Y,prog*intro)
 obs=phase(t,c.at('胜负判断')-.22,c.at('胜负判断')+.66)
 for k in range(30):
  z=k%15/14*1.89-.945;yes=(k*53%103)/103<1/(1+exp(-1.55*z));x=mid+z*(x1-x0)*.5+(k//15-.5)*5;y=top if yes else bottom
  # Recorded votes never change from a 0 to a 0.5. Only predictions move.
  v=phase(t,c.at('胜负判断')-.20+.036*k,c.at('胜负判断')+.55+.036*k)
  dot(g,x,y,4.6,C if yes else O,obs*(.72-.29*model)*v)
 if obs:
  txt(g,'1',x0-20,top,22,M,obs,'right');txt(g,'0',x0-20,bottom,22,M,obs,'right')
 hold=c.at('两份原文');fixed=c.at('一个字都不用删')
 reveal=phase(t,hold-.31,hold+.54)*(1-phase(t,mean-.62,mean-.10))
 if reveal:
  # Same two documents before and after the statistical control. Only the input to
  # the fitted curve moves to zero; neither answer nor its recorded vote is rewritten.
  for j,co in enumerate((C,V)):
   px=1106+j*181;docs(g,px-55,335,111,99+24*j,co,reveal,3+j,j)
   txt(g,('回答 A','回答 B')[j],px,505,23,co,reveal)
  show=phase(t,fixed-.15,fixed+.56)
  bracket(g,1047,549,301,T,show*reveal)
  txt(g,'原文保持不动',1198,598,26,T,show*reveal)
 zero=phase(t,fix-.16,fix+1.20);pool=phase(t,mean-.19,mean+.96)
 if model:
  for k,(col,z0) in enumerate(((C,.73),(V,-.80),(O,.50))):
   arcpts=[point(-1+i/58*2,k) for i in range(59)]
   path(g,arcpts,phase(model,.055*k,.84+.055*k),col,2.8,model*(1-.34*zero))
   z=mix(z0,0,zero);px,py=point(z,k);dot(g,px,py,7,col,model)
   if zero and not pool:line(g,(mid,bottom-4),(mid,top+5),Y,1.25,zero*.60)
   forq=phase(t,c.at('每道题')-.15+k*.23,c.at('每道题')+.50+k*.23)
   if 0<forq<1:ring(g,px,py,7+11*forq,col,sin(pi*forq)*model,1.7)
   if pool:
    val=1/(1+exp(-(.80,-.24,.38)[k]))
    destination=(1114+82*k,567-val*228);p=phase(t,mean+.08+k*.23,mean+1.29+k*.23);x,y=transit((px,py),destination,p,56-14*k)
    a0=1-phase(t,c.at('在论文比较')-.30,c.at('在论文比较')+.44)
    if p>.72:line(g,(destination[0],567),(destination[0],mix(567,destination[1],phase(p,.72,1))),col,4,a0)
    dot(g,x,y,6.7,col,a0*pool)
 if pool:
  pre,title2=reletter(phase(t,c.at('在论文比较')-.30,c.at('在论文比较')+.44));txt(g,'各题等权',1200,323,27,F,pool*pre);line(g,(1077,567),(1319,567),M,1.5,pool*pre)
  avg=sum(1/(1+exp(-h)) for h in (.80,-.24,.38))/3
  mid_y=567-228*avg;ag=phase(t,mean+.96,mean+1.93)
  if ag and pre:
   line(g,(1082,mid_y),(1082+235*ag,mid_y),Y,1.85,pre*ag)
   txt(g,f'三题示意均值　{100*avg:.1f}%',1200,633,25,Y,pre*ag)
 if model:source(g,'长度回归示意 · 三道题分别预测，再取平均',model)

ALPACA=json.loads((W/'data/alpaca-length-control.json').read_text())
def length(g,c):
 t=c.t;report=c.at('在论文比较');switch=c.at('控制长度之后')
 if t<report-.52:
  length_lesson(g,c);return
 # Samples of instructions yielded one estimated win rate on the old board. To
 # ask about an ordering we now need different, actually evaluated model identities.
 from wetjoins import crop
 old=1-phase(t,report-.53,report+.22);new=phase(t,report-.03,report+.55)
 if old:
  crop(g,0,142,1600,646,lambda:curtain(g,old,lambda:length_lesson(g,c)))
 title(g,'AlpacaEval 2.0',110)
 rail=phase(t,report-.53,report+.68)
 if 0<rail<1:
  # Keep the chalk edge while the statistical object changes; no toy observation
  # gets relabelled as one of the historical model scores.
  xx=mix(191,450,rail);hi=mix(280,352,rail);lo=mix(620,558,rail)
  line(g,(xx,lo),(xx,hi),M,1.7,sin(pi*rail)**.6)
 if not new:return
 txt(g,'两款模型的先后',534,234,29,F,new)
 raw=c.at('原始榜单');arena=c.at('Chatbot Arena');corr=c.at('排名相关');first=c.at('零点九四');second=c.at('零点九八');turn=c.at('电脑环境里')
 low,high=523,380;x0,x1=450,824
 txt(g,'原始胜率',x0,307,25,M,new)
 line(g,(x0,352),(x0,558),E,1.3,new)
 reveal=phase(t,switch-.33,switch+.58)
 if reveal:
  txt(g,'等长胜率',x1,307,25,M,reveal);line(g,(x1,352),(x1,558),E,1.3,reveal)
 for j,(r,col,y0,y1)in enumerate(zip(ALPACA['win_rates_percent'],(C,V),(low,high),(high,low))):
  seen=phase(t,report+.13+j*.20,report+.89+j*.20)
  if not seen:continue
  label=r['label'];v0=r['uncontrolled'];v1=r['length_controlled']
  op=new*seen
  txt(g,label,x0-27,y0-17,25,col,op,'right');txt(g,f'{v0:.1f}%',x0-27,y0+23,29,F,op,'right')
  dot(g,x0,y0,7,col,op)
  k=phase(t,switch-.16+j*.09,switch+1.16+j*.09)
  if k:
   xx=mix(x0,x1,k);yy=mix(y0,y1,k);line(g,(x0,y0),(xx,yy),col,2.25,op);dot(g,xx,yy,7,col,op)
   txt(g,f'{v1:.1f}%',x1+21,y1,29,col,op*phase(k,.65,1.),'left')
 labels=phase(t,arena-.23,arena+.63)
 if labels:
  txt(g,'与人类盲测的排名相关',1243,250,28,F,labels)
  txt(g,'38 款模型 · Spearman ρ',1243,302,24,M,phase(t,corr-.37,corr+.42))
  for j,(field,col,event) in enumerate((('spearman_raw',M,first),('spearman_length_controlled',G,second))):
   v=ALPACA['figure1'][field];q=phase(t,event-.24,event+.52);yy=403+j*119
   if q:
    txt(g,('原始','等长')[j],1064,yy,25,col,q,'left');txt(g,f'{v:.2f}',1291,yy,51,col,q)
    line(g,(1090,yy+45),(1376,yy+45),D,1.1,q);line(g,(1090,yy+45),(1090+286*v*q,yy+45),col,3.3,q)
 action=phase(t,turn-.32,turn+.74)
 if action:
  txt(g,'会被选中',644,678,28,V,action);arrow(g,(736,678),(841,678),action,M,action,1.7)
  txt(g,'能运行？',946,678,31,Y,action)
 source(g,'Dubois 等 · 图 4 两款自动胜率；图 1 与人类榜单的相关',phase(t,report+.16,report+.70))
