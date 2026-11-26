"""Release date, access, answer key: three physical changes to three separate things."""
from rig4 import *
from studio_dates import seal
from studio_corpus import HIST

def shelf(g,c,st):
 t=c.t;a=c.at
 check_=a('最后校验');expert=a('专家回头重审');ambiguity=a('错标和歧义');cor=a('剔除')
 done=a('三件事修的');date=a('新题隔开时间');secret=a('私题控制接触');audit=a('审题提高');memory=a('已经读过')
 p=enter(t,st,.71);side=easepos(t,expert-.31,1.10);s=enter(t,done-.26,.70)
 # The same chronological scale slides back rather than getting cut to black.
 # The plotted release counts stay as plotted counts as long as it's readable.
 sx=mix(128,141,p);sz=mix(1340,454,p);cy=mix(513,517,p)
 cover=1-phase(t,done-.59,done+.09)*.15
 shift=mix(1.,.49,p)
 line(g,(sx,cy),(sx+sz,cy),M,2.05,cover)
 path(g,[(sx+sz-12,cy-6),(sx+sz,cy),(sx+sz-12,cy+6)],1,M,1.7,cover)
 cut=sx+sz*.507
 line(g,(cut,cy-149*shift),(cut,cy+9),Y,2.4,cover)
 for j,(_,day,n) in enumerate(HIST['releases']):
  xx=mix(128+193+j*201,sx+sz*(.11+j*.149),p)
  h=(158*n/1055)*shift
  co=T if xx>cut and p>.65 else C
  rect(g,xx-6,cy-h,12,h,co,cover if xx>cut else cover*(1-.68*p))
  a0=cover*(1-p)
  if a0>.01:
   label(g,day,xx,cy+46,26,M,a0);label(g,str(n),xx,cy-h-26,27,T,a0)
 if p:
  mark(g,'发布日期',sx,cy-134,28,t-st+.05,T,'left',op=p*cover,dur=.46)
  shade0=during(t,date-.19,date+1.70,.44)
  for tag,offset,x,z,col in (('截止日',0.,cut,41,Y),('更新的题',.14,sx+sz-69,40,T)):
   show=enter(t,date-.27+offset,.58)
   if show:
    label(g,tag,x,cy+z,25,col,show*p)
    if shade0:ring(g,x,cy-15,19,col,shade0*.82,1.7)
 hold=c.u('一套不公开的题',.55);lift=phase(t,check_-.15,check_+.83)
 px=mix(795,817,side);py=mix(382,458,side)
 if hold:
  travel=easepos(t,st-.02,.74);x=mix(1082,px,travel);y=mix(332,py,travel)
  seal(g,x,y,114*(.87+.13*travel),1-lift,hold)
  hatch=sin(pi*lift)**.74
  if lift:
   pts=[(x+80,y+35),(x+103,y+35),(x+121,y+67),(x+161,y+67)]
   path(g,pts,easepos(t,check_-.02,1.03),C,2.05,hold)
   if hatch:
    k=easepos(t,check_-.01,.77);bx,by=transit((x+44,y+6),(x+149,y+67),k,32);point(g,bx,by,6,C,hatch)
  out=enter(t,check_+.57,.46)
  if out:check(g,x+151,y+67,10,True,out*hold)
  label(g,'保留题',x,py+137,29,C,hold)
  focus=during(t,secret-.16,secret+1.70,.42)
  if focus:path(g,[(x-93,y-85),(x-93,y-105),(x+93,y-105),(x+93,y-85)],enter(t,secret-.15,.64),C,2.3,focus)
 script=enter(t,expert-.16,.56)
 if script:
  # A tiny editing example. The two choices live on separate branch tips.
  x,y=1278,392
  mark(g,'2.5',x,y,56,t-expert+.15,F,mode='pen',op=script)
  plus=easepos(t,ambiguity-.21,.62);ok=easepos(t,cor-.11,.58)
  for j,(dx,name,col,ans) in enumerate(((-112,'平局取偶',V,'2'),(112,'半数向上',O,'3'))):
   sx_=x+dx;yy=y+157;real=plus*script*(1-.78*ok if j==0 else 1)
   path(g,[(x,y+41),(x,y+60),(sx_,y+112)],plus,col,2.45,real)
   label(g,ans,sx_,yy,42,col,real);label(g,name,sx_,yy+51,24,F,real)
   if j and ok:
    check(g,sx_+50,yy,11,True,ok*script)
    label(g,'明确进位约定',x,yy+116,27,O,ok*script)
  focus=during(t,audit-.18,audit+1.63,.41)
  if focus:
   pts=[(x-124,318),(x+131,318),(x+131,360)]
   path(g,pts,enter(t,audit-.22,.70),O,2.6,focus)
 # Bring the lens back to the date. A corrected answer key has no conducting
 # path to the past; the two causes remain separate strands.
 if s:
  labops=[enter(t,d-.20,.56)for d in (date,secret,audit)]
  for j,(txt,x,col,h) in enumerate(zip(('时间','接触','标注'),(338,817,1278),(T,C,O),labops)):
   if h:mark(g,txt,x,207,45,t-(date,secret,audit)[j]+.20,col,mode='wave',op=h)
 q=enter(t,memory-.41,.78)
 if q:
  bbox=[(1253,685),(1173,727),(658,727),(536,657),(cut-41,cy+4)]
  path(g,bbox,q,O,1.8,q*.81)
  if q>.59:ring(g,cut-41,cy,13,T,q,1.9)
  note=enter(t,memory-.19,.47)
  mark(g,'旧题的发布日期没动',691,770,29,t-memory+.14,M,op=note)
