"""One fictional encounter, two different tasks. The words come from the same source."""
from ink import *
from mounting import etch
from ink_words import swish
from motion import transit
from studio_examples import pstep,VIO,BLUE
def medical(g,c):
 t=c.t;a=c.at;intro=a('斯坦福');task=a('临床工作任务');note=a('起草病历');dec=a('辅助临床决策');fact=a('真实工作长得越像');out=a('含金量')
 q=pstep(t,intro-.20,.58)
 if not q:return
 # A single voice mark unfolds into text. Both descendants quote from this one encounter.
 x=181;y=446;co=T
 for j in range(44):
  h=12+64*abs(sin(j*.41+.19)*cos(j*.66+t*.63))
  w=phase(t,intro-.16+j*.018,intro+.28+j*.018)
  if w:rect(g,x+j*7.1,y-h*.5,4.4,h,T,w*(.88-.30*phase(t,note-.18,note+.36)))
 etch(g,'就诊片段 · 示意',x,310,27,M,q)
 src=('“来复诊，','上次的报告没带。”')
 for j,ss in enumerate(src):
  etch(g,ss,x,529+j*51,39,F,pstep(t,intro+.31+j*.32,.53))
 path(g,[(x,623),(x+300,623)],q,T,1.8,q)
 r=phase(t,task-.51,task+.18)
 if r:
  for i,(y1,col)in enumerate(((298,C),(548,VIO))):
   pts=[(502,442),(610,442),(694,y1),(816,y1)]
   path(g,pts,r,col,2.8,r)
 # The same facts take different routes: document what was said vs identify a missing input.
 for i,(at,co,lab,body)in enumerate(((note,C,'病历草稿','就诊目的：复诊'),(dec,VIO,'辅助决策','既往报告未提供'))):
  b=pstep(t,at-.21,.52)
  if not b:continue
  y1=(298,548)[i];pos=(849,y1);etch(g,lab,pos[0],pos[1]-52,35,co,b)
  q2=phase(t,at-.08,at+.83)
  if q2<.998:
   xx,yy=transit((408,529+i*51),pos,q2,78 if i==0 else -62);dot(g,xx,yy,9,co,b)
  etch(g,body,pos[0],pos[1]+14,35,F,pstep(t,at+.20,.58))
  if i==0:etch(g,'既往检查单：未携',pos[0],pos[1]+74,26,M,pstep(t,dec-.64,.52))
  else:
   r2=pstep(t,fact-.30,.78);path(g,[(864,y1+48),(864,y1+77),(963,y1+77)],r2,co,2.5,r2)
   etch(g,'调阅上次记录',991,y1+76,28,co,r2)
 if t>=out-.25:swish(g,990,1183,653,t-out+.24,VIO,.74)
