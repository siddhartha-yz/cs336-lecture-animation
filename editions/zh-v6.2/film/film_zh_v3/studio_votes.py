"""Evidence observers can manipulate with their eyes: same vote, same words, one varied input."""
from ink import *
from motion import guide,transit,out3,formula
from ink_words import letter,swish,carryword
from studio_examples import pstep,area,symbol,quote,VIO,AQUA,BLUE,MONO,silk
from timeline3 import W,OLD
from cut_common import cairo
import json
from mounting import etch
from termnotes import hint
RANKS=json.loads((W.parent/'beats_real/data/arena-ranks-0.raw.json').read_text())['rows']
RANKS=sorted([item['row']for item in RANKS if item['row']['category']=='overall' and 1<=item['row']['rank']<=6],key=lambda row:row['rank'])
MEASURE=json.loads((OLD/'data/alpaca-length-control.json').read_text())
def wedge(g,x,y,r,a,b,color,op=1):
 if b-a<.0001:return
 ctx=g.c;ctx.save();ctx.move_to(x,y);ctx.arc(x,y,r,a,b);ctx.close_path();g.source(color,op);ctx.fill();ctx.restore()
def pend(g,x,y,t,many=14,op=1):
 for i in range(many):
  xx=x+(i%7)*16;yy=y+(i//7)*14;dot(g,xx,yy,3.4,C if i%3 else VIO,op*(.45+.46*math.sin(i*.72+t*.42)**2))
def rating(g,c):
 t=c.t;intro=c.at('Bradley');chart=c.at('胜率曲线');delta=c.at('先看两人的分差');subtract=c.at('减去');divide=c.at('除以四百');power=c.at('十的指数');add=c.at('然后加一');inv=c.at('再取倒数');equal=c.at('积分完全相同');zero=c.at('指数为零');plus=c.at('高出四百分');odds=c.at('十比一');fit=c.at('极大似然');evidence=c.at('真实投票记录');end=phase(t,fit-.48,fit+.61)
 alpha=1-end;cx,cy=1202,398;radius=190
 silk(g,'Bradley–Terry',114,106,52,t-.21,F,1,'pen','left',.76)
 silk(g,hint('Bradley–Terry'),114,167,25,t-intro+.08,M,1,align='left')
 if alpha>.002:
  # Negative, tied and positive score differences drive four readouts from ONE scalar.
  initial=phase(t,chart-.5,delta-.34);val=-400*initial+400*phase(t,equal-.25,equal+.60)+400*phase(t,plus-.15,plus+.61)
  pa=1/(1+10**(-val/400));xo,bo,w,h=153,658,759,391
  def point(x):return xo+(x+600)*w/1200,bo-h/(1+10**(-x/400))
  line(g,(xo,bo),(xo+w+10,bo),M,1.7,alpha);line(g,(xo,bo),(xo,bo-h-18),M,1.7,alpha)
  for u,hint_ in ((.1,'10%'),(.5,'50%'),(.9,'90%')):
   ytick=bo-h*u;line(g,(xo-7,ytick),(xo+w,ytick),'#434343',1.3,alpha*.85);txt(g,hint_,xo-12,ytick,22,M,alpha,'right')
  for d in [-400,0,400]:
   x,y=point(d);line(g,(x,bo),(x,bo+8),M,1.4,alpha);txt(g,f'{d:+d}'if d else '0',x,bo+30,23,M,alpha)
  txt(g,'分差  A − B',xo+w*.5,732,27,M,alpha)
  txt(g,'A 胜',xo,224,26,C,alpha,'left')
  q=phase(t,.40,chart+.58);pts=[point(-600+j*10)for j in range(121)]
  path(g,pts,q,C,4.2,alpha);x,y=point(val);pr=phase(t,chart-.65,chart+.08)
  if pr:
   # A filled under-curve patch is tied to x; the ordinate is read from the dot, not its area.
   line(g,(x,bo),(x,y),Y,2.4,alpha*pr);line(g,(xo,y),(x,y),Y,1.15,alpha*pr*.62);dot(g,x,y,8,Y,alpha*pr)
  pie=phase(t,.67,1.53)
  if pie:
   a=-pi/2;split=a+tau*pa
   wedge(g,cx,cy,radius,a,split,BLUE,pie*alpha);wedge(g,cx,cy,radius,split,a+tau,VIO,pie*alpha)
   ring(g,cx,cy,radius+1,F,pie*alpha*.8,1.5)
   ex,ey=cx+radius*cos(split),cy+radius*sin(split);line(g,(cx,cy),(ex,ey),F,2,pie*alpha)
   txt(g,f'{100*pa:.1f}%',cx,650,65,C,pie*alpha);txt(g,'A 的预测胜率',cx,718,30,F,pie*alpha)
   # Each letter follows its own sector, even when the small blue and purple wedges change sides.
   for name_,mid,share_ in (('A',(a+split)/2,pa),('B',(split+a+tau)/2,1-pa)):
    rad=radius*(.83 if share_<.20 else .55)
    txt(g,name_,cx+rad*cos(mid),cy+rad*sin(mid),30 if share_<.20 else 43,F,pie*alpha)
  if t>=intro-.2:
   foc=phase(t,delta-.36,delta+.32)*(1-phase(t,inv+.55,inv+1.20))
   formula(g,'elo',525,116,638+61*foc,alpha*phase(t,intro-.18,intro+.40))
  events=[(subtract,'B − A = 400'),(divide,'400 / 400 = 1'),(power,'10¹ = 10'),(add,'1 + 10 = 11'),(inv,'1 / 11'),(zero,'1 + 10⁰ = 2'),(plus,'1 + 10⁻¹ = 1.1'),(odds,'10 : 1')]
  for idx,(when,expr) in enumerate(events):
   fin=events[idx+1][0] if idx+1<len(events)else fit
   al=phase(t,when-.12,when+.20)*(1-phase(t,fin-.37,fin-.13))*alpha
   if al:
    silk(g,expr,1240,145,36,t-when+.12,Y,al,'pen',dur=.40)
    swish(g,1135,1345,184,t-when-.25,Y,.40)
 else:pass
 if end:
  # Retain the S curve on the left in miniature; the live rating is a fit to a graph of votes.
  p=end;x,y=382,457;m=eye=phase(t,evidence-.19,evidence+.68);scoreD=400*math.log10(3)
  vals=[(144+485*j/60,584-220/(1+10**(-(-600+1200*j/60)/400)))for j in range(61)]
  path(g,vals,1,C,3,end);line(g,(145,584),(632,584),M,1.4,end)
  voters=(C,VIO,C,C);stepgap=min(.95,max(.38,(evidence-fit-.6)/3))
  votes=[]
  for j,col in enumerate(voters):
   h=pstep(t,fit-.10+j*stepgap,.59);xx,yy=transit((221+j*92,276),(252+j*91,338),h,23)
   if h:dot(g,xx,yy,11,col,p*h)
   if h>.98:votes.append(col)
  if len(votes)>=2:
   pct=votes.count(C)/len(votes);we=400*math.log10(pct/(1-pct));wx=144+485*(we+600)/1200;wy=584-220*pct
   if not eye:dot(g,wx,wy,7,Y,end)
  else:pct=0.
  sx=144+485*(scoreD+600)/1200;sy=584-220*.75
  dot(g,sx,sy,7,Y,eye);txt(g,(f'{len(votes)} 票里，A 赢 {votes.count(C)} 次' if votes else '一场给一票'),383,652,27,F,end)
  etch(g,'Text Arena · 模型',891,225,26,M,end)
  etch(g,'等级分 · 2026-11-22',1454,224,24,M,end,'right')
  for j,row in enumerate(RANKS):
   q=pstep(t,fit+.08+j*.095,.47)*end;yy=283+j*66;col=Y if j==0 else C
   txt(g,str(j+1),860,yy,25,M,q,'right');txt(g,row['model_name'].replace('(High)','· High'),893,yy,26,F,q,'left',400)
   txt(g,f"{row['rating']:.1f}",1455,yy,28,col,q,'right');line(g,(866,yy+28),(1454,yy+28),D,1.2,q)
  txt(g,'拟合全部对局',856,709,24,M,end,'left')
def storybit(g,i,x,y,sc=1,op=1,edition=0,length=0):
 co=(C,VIO)[i];ctx=g.c;ctx.save();ctx.translate(x,y);ctx.scale(sc,sc)
 symbol(g,'AB'[i],-173,-22,.72,op)
 txt(g,'回复 '+('A','B')[i],-92,-101,26,co,op,'left')
 rows=(('734 号的职责，','是擦亮黄铜路灯。'),('老维修机器人穿过','空荡荡的购物中心。'))[i]
 if edition and i==1:rows=('空商场里，','老维修机器人驶过。')
 for j,s in enumerate(rows):txt(g,s,-92,-37+j*44,32,F,op,'left',342)
 if length and i==1:
  for j,s in enumerate(('四周一个人也没有，','偌大的商场空荡荡。')):
   a=clip(length*2-j);txt(g,s,-92,57+j*39,26,VIO,op*a,'left',340)
 line(g,(-94,64+max(0,length)*80),(229,64+max(0,length)*80),co,2.1,op);ctx.restore()
def judgement(g,c):
 t=c.t;auto=c.at('大模型裁判');human=c.at('等几万个人');same=c.at('把目光留在');where=c.at('左右两个');verdict=c.at('跟着坑位改判');style=c.at('自我偏好');change=c.at('换一种措辞');length=c.at('长度偏见');verbose=c.at('写得更长');win=c.at('更容易给高分');loop=c.at('按这把尺')
 base=1-phase(t,same-.54,same-.08)
 if base:
  silk(g,'LLM-as-a-Judge',800,119,50,t-auto+.1,F,base,'pen')
  if t>auto-.10:silk(g,hint('LLM-as-a-Judge'),800,174,25,t-auto-.25,M,base)
 swap=phase(t,where-.09,where+.65)*(1-phase(t,style-.75,style-.12));lift=95*sin(pi*swap)
 cx1=mix(420,1115,swap);cx2=mix(1115,420,swap)
 # Short, staggered semantic labels; the answer remains intact during each positional swap.
 focus=0 if t<style else 1 if t<length else 2;steps=[same,style,length]
 if 1-base>.02:
  nm=('位置偏见','自我偏好','长度偏见')[focus]
  silk(g,nm,800,113,47,t-steps[focus]+.16,(Y,VIO,O)[focus],1-base)
  txt(g,('追踪同一份回答','改写示意 · 语义保留','扩写示意 · 信息不增')[focus],800,173,25,M,1-base)
 e=phase(t,change-.10,change+.32)*(1-phase(t,length-.47,length-.12));ln=phase(t,verbose-.15,verbose+.80)
 storybit(g,0,cx1,408-lift,.94);storybit(g,1,cx2,409+lift,.94,1,edition=1 if e>.50 else 0,length=ln)
 if t<auto:
  wait=phase(t,human-.55,human+1.06)
  for j in range(31):
   a=pstep(t,.39+j*.073,.38);x=347+(j%16)*59;y=607+(j//16)*39
   if a:dot(g,x,y,4.2+1.9*wait,(C,VIO)[j%2],a*.85)
  txt(g,'真人的票',800,712,25,M,wait)
 else:
  k=pstep(t,auto-.22,.54);area(g,[(800,311),(834,353),(800,395),(766,353)],VIO,k);txt(g,'裁判',800,436,24,VIO,k)
  if t>where-.36 and t<style-.26:
   for j in range(2):line(g,(800,529),(cx1 if j==0 else cx2,529),E,1.2,.62)
   # Select left POSITION, not an inherent ground truth about this pair.
   ky=phase(t,verdict-.18,verdict+.36)
   x=mix(cx1,420,ky);markx=x
   dot(g,markx,567,8,Y,1);txt(g,'同一个位置',420,636,24,Y,ky)
  if e:
   swish(g,1010,1332,440,t-change-.18,VIO,.55);txt(g,'事实没有换',800,654,30,T,e)
  if ln:
   ky=pstep(t,win-.27,.7);xx,yy=transit((800,378),(1120,629),ky,68)
   dot(g,xx,yy,8,Y,ky);txt(g,'长度增加',1135,688,26,O,ln)
   if t>loop:txt(g,'这次加长的是措辞',422,681,26,M,pstep(t,loop,.52))
def length(g,c):
 t=c.t;name=c.at('AlpacaEval');reg=c.at('长度控制回归');obs=c.at('胜负判断');fit=c.at('先拟合');fix=c.at('长度差设成零');avg=c.at('最后取平均');paper=c.at('论文比较');to=c.at('电脑环境里')
 txt(g,'AlpacaEval 2.0',122,99,48,F,1,'left');txt(g,hint('AlpacaEval 2.0'),125,158,26,M,1,'left')
 pub=phase(t,paper-.33,paper+.46);exit_=phase(t,to-.61,to-.04);al=(1-pub)*(1-exit_)
 if al:
  from studio_preference import tapes
  tapes(g,c,al)
  intro=phase(t,obs-.33,obs+.37); model=phase(t,fit-.28,fit+.49);q=phase(t,fix-.22,fix+.54);pool=phase(t,avg-.18,avg+.56)
  x0,x1=729,1474;mid=(x0+x1)/2;bottom=615;top=297
  txt(g,'同一题 · 模型中的长度差',1100,210,29,F,al)
  line(g,(x0,bottom),(x1,bottom),M,1.8,al);line(g,(x0,bottom),(x0,top),M,1.8,al)
  line(g,(mid,top+5),(mid,bottom),E,1.3,al);txt(g,'0',mid,bottom+29,26,Y,al);txt(g,'较短',x0+43,bottom+33,23,M,al);txt(g,'较长',x1-34,bottom+33,23,M,al)
  def point(z,j):
   y=1/(1+exp(-((.50,-.45,1.14)[j]+1.65*math.tanh(z*1.14))))
   return mid+z*(x1-x0)/2,bottom-y*(bottom-top)
  for i in range(30):
   if not intro:break
   jj=i%15;zz=(jj-7)/8.35;onv=(i*53%103)/103 < 1/(1+exp(-1.4*zz));x=mid+zz*(x1-x0)/2.+(i//15)*4
   a=pstep(t,obs-.18+.026*i,.38);dot(g,x,top if onv else bottom,4.5,(C,VIO)[onv],al*intro*a*(1-.44*model))
  initial=phase(t,.3,reg+.28)
  # Animating the predictor, not the two recorded stories: same words, different conditional calculation.
  z=(-.66+.1*phase(t,.05,1.2)+1.36*phase(t,c.at('额外优势')-.64,c.at('额外优势')+.63)-1.26*phase(t,c.at('裁判偏爱哪一边')-.38,c.at('裁判偏爱哪一边')+.65)+1.18*phase(t,c.at('一个字都不用删')-.41,c.at('一个字都不用删')+.65))*(1-q)
  for j,co in enumerate((C,T,VIO)):
   op=(1 if j==0 else pool*.70)*al
   if not op:continue
   points=[point(-1+2*k/80,j)for k in range(81)]
   path(g,points,max(initial*.87,model),co,3.3 if j==0 else 1.9,op*(.67 if j else 1))
   if j==0:
    xx,yy=point(z,j);line(g,(xx,yy),(xx,bottom),Y,2,op);dot(g,xx,yy,8,Y,op)
    sl='Δℓ = 0' if q>.98 else 'Δℓ'
    txt(g,sl,xx,yy-39,29,Y,op)
    # The thumbnail and the number read the very same ordinate as the dot.
    prob=(bottom-yy)/(bottom-top);gauge=phase(t,reg-.48,reg+.14)
    if gauge:
     vx,vy,r=1350,142,24;wedge(g,vx,vy,r,-pi/2,-pi/2+tau*prob,BLUE,op*gauge);wedge(g,vx,vy,r,-pi/2+tau*prob,3*pi/2,VIO,op*gauge)
     txt(g,f'{prob*100:.0f}%',1390,142,27,F,op*gauge,'left')

   elif pool:xx,yy=point(0,j);dot(g,xx,yy,6.4,co,op)
  if q:
   # Fixed fitted curves. Only the covariate goes to zero; no line rotates flat.
   swish(g,mid-26,mid+27,bottom+47,t-fix-.2,Y,.55)
  if t<avg-.21:txt(g,'原文一直没改',345,712,27,T,al);txt(g,'单题回归曲线示意',1104,717,22,M,al)
  else:txt(g,'各题等长胜率，再取平均',1087,711,28,T,al*pool)
 if pub and not exit_>=1:
  a=pub*(1-exit_)
  txt(g,'两款模型的胜率（%）',381,251,35,F,a)
  xleft,xright=211,587;vv=phase(t,paper+.06,c.at('控制长度之后')+.2)
  for j,r in enumerate(MEASURE['win_rates_percent']):
   col=(C,VIO)[j];yA=578-9.0*r['uncontrolled'];yB=578-9.0*r['length_controlled']
   dot(g,xleft,yA,6.5,col,a);path(g,[(xleft,yA),(xright,yB)],vv,col,3.3,a);dot(g,xright,yB,7,col,a*phase(vv,.90,1))
   txt(g,f"{r['uncontrolled']:.1f}",xleft-19,yA,23,col,a,'right')
   txt(g,f"{r['length_controlled']:.1f}",xright+18,yB+(-11 if j==0 else 14),24,col,a*phase(vv,.90,1),'left')
   txt(g,r['label'],344,624+j*47,25,col,a)
  txt(g,'原胜率',xleft,562,24,M,a);txt(g,'控制长度',xright,562,24,M,a)
  txt(g,'与人类盲测的排名相关',1120,248,34,F,a)
  corr=c.at('零点九四');adj=c.at('零点九八')
  for i,(r,col,at)in enumerate(((.94,C,corr),(.98,T,adj))):
   k=pstep(t,at-.18,.62);y=392+i*115
   txt(g,('原排名','等长排名')[i],841,y,25,F,a*k,'left');rect(g,998,y-11,303*r*k,22,col,a*k);txt(g,f'{r:.2f}',1370,y,39,col,a*k)
  txt(g,'38 个模型 · Spearman ρ',1108,646,26,M,a)
 if exit_:
  # One real setting goes into the parser; its actual and expected text are different.
  # The underscore name stays in place as everything else retracts at the cut.
  t0=c.at('它到底能不能');tw=c.at('把活干成呢');hold=1-phase(t,c.d-1.10,c.d-.16)
  n=pstep(t,to-.32,.47);m=pstep(t,t0-.16,.52);j=pstep(t,tw-.14,.52)
  a=exit_*hold
  if n*hold:
   txt(g,'napoleon_use_param',366,264,28,F,a*n,font=MONO)
   txt(g,'= True',554,264,28,Y,a*n,'left',font=MONO)
   path(g,[(380,296),(459,296),(601,409)],n,T,2.6,a)
  txt(g,'other_parameters',800,449,38,C,exit_,font=MONO)
  if m*hold:
   path(g,[(1003,465),(1120,565),(1352,565)],m,R,2.7,a)
   txt(g,'实际输出',1057,603,24,M,a*m,'right')
   txt(g,':Other Parameters:',1094,603,31,R,a*m,'left',395,MONO)
  if j*hold:
   txt(g,'测试期望',1057,669,24,M,a*j,'right')
   txt(g,':param param2:',1094,669,31,T,a*j,'left',395,MONO)
   swish(g,1088,1348,702,t-tw-.21,T,.55)
