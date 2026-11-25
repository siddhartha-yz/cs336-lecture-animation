"""One noun phrase, one pair of votes and one untouched pair of original texts.
The text which changes in the bias demonstration is a translation; in the regression shot,
each tiny dash stands for a real whitespace-delimited word of the unchanged recorded answer."""
from ink import *
from timeline3 import W
from studio_examples import pstep,silk,area,symbol,VIO,MONO,BLUE
from motion import transit
from ink_words import swish
from mounting import etch
import json
from functools import lru_cache
@lru_cache(None)
def material():
 row=json.loads((W/'source/arena-pair.json').read_text())['rows'][0]['row']
 return [[x for x in row['conversation_'+which][1]['content'][0]['text'].split()]for which in ('a','b')]
@lru_cache(None)
def weft(i):
 # Preserve original order and vary stroke length by spelling. Sentence endings leave a little breathing room.
 result=[];xx=0;row=0;span=516
 for token in material()[i]:
  w=2.0+min(15,len(token))*.79
  if xx+w>span:xx=0;row+=1
  result.append((xx,row,w));xx+=w+(3.7 if token.endswith(('.','?','!'))else 1.75)
 return result,row+1
def tapes(g,c,op):
 t=c.t;a=c.at;obs=a('胜负判断');equal=a('一个字都不用删');fix=a('长度差设成零')
 for i,(yy,co,quote)in enumerate(((154,C,'734 号擦亮黄铜路灯。'),(465,VIO,'维修机器人驶过空商场。'))):
  words=material()[i];ds,n=weft(i);s=pstep(t,.16+.16*i,.73);x=107+63*i;dot(g,x-19,yy,6.9,co,s*op);etch(g,quote,x,yy,38,F,op)
  etch(g,('A','B')[i]+'  ·  '+str(len(words))+' 词',x,yy+52,26,co,op)
  # Tick from the ruler moves along identical words when the narrator says their texts stay unchanged.
  y0=yy+94;pitch=10.1;pen=phase(t,equal-.36,equal+.75);start=round(.243*len(ds))
  for j,(xx,row,w)in enumerate(ds):
   show=clip(s*1.46-.46*j/len(ds));zz=(1 if j//27%3==0 else .73 if j//16%2==0 else .59)
   if not show:continue
   gold=1-phase(abs(j-start-pen*(len(ds)-start)*.76),1,8) if .002<pen<.998 else 0
   rect(g,x+xx,y0+pitch*row,w,5.0,blend(co,Y,gold),op*show*zz)
  if i==0 and t>a('回答的长度差')-.14:
   v=phase(t,a('回答的长度差')-.14,a('回答的长度差')+.43)
   etch(g,'一画一词',x+409,yy+52,23,M,op*v,'right')
  if t>obs-.18:
   r=phase(t,obs-.18,obs+.51);y1=y0+pitch*(n-1)
   path(g,[(x+529,y0-2),(x+536,y0-2),(x+536,y1+4),(x+529,y1+4)],r,co,2.2,op*r)
def _paragraph(g,i,x,y,sz,op,change,length,t):
 ctx=g.c;ctx.save();ctx.translate(x,y);ctx.scale(sz,sz);co=(C,VIO)[i];name='AB'[i]
 # One common data mark persists underneath its words at every translation and scale.
 shape=((-199,6) if i==0 else(-152,17))
 symbol(g,name,*shape,(1.12 if i==0 else 1.00),op,.88)
 etch(g,name,-97,-108,36,co,op)
 if i==0:
  etch(g,'734 号的职责，',-96,-48,38,F,op);etch(g,'是擦亮黄铜路灯。',-96,12,38,F,op)
 else:
  for j,(base,reword)in enumerate((('老维修机器人穿过','空商场里，'),('空荡荡的购物中心。','老维修机器人驶过。'))):
   yy=-47+53*j
   if change<.999:
    dx=64*change;etch(g,base,-96+dx,yy-15*change,37,F,op*(1-change))
   if change>.001:
    etch(g,reword,-96-37*(1-change),yy+13*(1-change),37,F,op*change)
  if length:
   for j,ss in enumerate(('四周一个人也没有，','偌大的商场空荡荡。')):
    k=clip(length*2.18-j);etch(g,ss,-96,64+39*j+9*(1-k),29,VIO,op*k)
 line(g,(-97,59+length*82),(218,59+length*82),co,2.6,op);ctx.restore()
def judgement(g,c):
 a=c.at;t=c.t;people=a('等几万个人');auto=a('大模型裁判');pair=a('自动化打分');same=a('把目光留在');sw=a('左右两个');vote=a('坑位改判');style=a('自我偏好');rep=a('换一种措辞');length=a('长度偏见');expand=a('写得更长');win=a('更容易给高分')
 fx=phase(t,sw-.1,sw+1.04)*(1-phase(t,style-.75,style-.12))
 close=phase(t,same-.16,same+.60)*(1-phase(t,sw-.65,sw+.13));focus=phase(t,style-.14,style+.42)
 lx,ly=(407,354);rx,ry=(1096,522);forward=sin(pi*fx)
 x1,y1=transit((lx,ly),(rx,ry),fx,135);x2,y2=transit((rx,ry),(lx,ly),fx,-105)
 cq=phase(t,rep-.08,rep+.48)*(1-phase(t,length-.65,length-.10));extra=phase(t,expand-.14,expand+.75)
 x1-=37*close;y1-=18*close;y2-=31*extra
 tag=(1-phase(t,auto-.30,auto+.44))
 if tag>.001:
  # A real queue: one vote enters at a time and the *next* place remains unfilled.
  queue=phase(t,people-.12,people+.71)
  for j in range(45):
   u=pstep(t,.11+j*.044,.41);xx=143+(j%15)*36;yy=586+(j//15)*32
   if not u:continue
   if j<9+int(20*queue):dot(g,xx,yy,6.6,(C,VIO,T)[j%3],tag*u)
   else:ring(g,xx,yy,6.5,M,u*tag*.67,1.45)
  if queue:etch(g,'待投票',144,714,25,M,tag*queue)
 judge=1-tag
 if judge:
  ox,oy=837,252;k=phase(t,auto-.10,auto+.5);step=phase(t,pair-.14,pair+.51)
  area(g,[(ox-35,oy),(ox,oy-36),(ox+35,oy),(ox,oy+36)],VIO,judge)
  if t<same-.20:etch(g,'LLM-as-a-Judge',ox-41,oy-98,32,F,judge);etch(g,'用模型比较两份回答',ox-39,oy-56,24,M,judge)
  # The model, the two real uses of it, and the arriving decisions each respond on their word.
  alpha=1-phase(t,same-.47,same-.04)
  if alpha:
   model=phase(t,a('GPT-4')-.13,a('GPT-4')+.42)
   etch(g,'GPT-4',ox-58,oy+63,28,VIO,model*alpha)
   for zz,(nm,col)in enumerate((('AlpacaEval',C),('MT-Bench',T))):
    ev=a(nm);k2=phase(t,ev-.10,ev+.47)
    if k2:
     yb=oy-71+zz*68;xe=ox+358+69*zz
     route=[(ox+37,oy-9),(ox+127,oy-9),(xe-38,yb),(xe-6,yb)]
     path(g,route,k2,col,2.1,alpha);etch(g,nm,xe,yb,26,col,k2*alpha)
     v1=phase(t,pair-.10+zz*.13,pair+.48+zz*.13)
     if v1:dot(g,xe-21,yb,5.9,Y,k2*alpha)
  for j,(z,co)in enumerate((((x1-67,y1-100),C),((x2-70,y2-97),VIO))):
   from_=((x1 if j==0 else x2)-40,(y1 if j==0 else y2)-120);end=(ox+(-30 if j==0 else 32),oy+27);d=[from_,((from_[0]+end[0])/2,oy+67),end];path(g,d,k,co,1.75,judge*(.35+.42*(1-focus)))
   if 0<step<1:dot(g,*transit(from_,end,step,22),6,Y,judge)
 _paragraph(g,0,x1,y1,1.12+.17*close-.10*focus,1-.43*focus,0,0,t)
 _paragraph(g,1,x2,y2,1.23-.07*extra,1,cq,extra,t)
 if same-.08<t<sw-.17:
  h=pstep(t,same-.08,.49);line(g,(x1-110,y1+48),(x1-108+222*h,y1+48),Y,2.5,h)
 if sw-.14<t<style-.72:
  q=pstep(t,sw-.14,.5);pick=phase(t,vote-.1,vote+.53)
  # This selection is pinned to position, not to whichever character happens to occupy it.
  band=ly+121;dot(g,lx-113,band,8.2,Y,q);line(g,(lx-91,band),(lx+152,band),Y,2.1,q)
  etch(g,'位置偏见',lx-91,band+45,29,Y,q);etch(g,'左位：'+('B'if fx>.5 else'A'),lx+76,band+45,28,F,q*pick)
 if style-.15<t<length-.19:
  k=phase(t,style-.15,style+.44);etch(g,'自我偏好',807,319,27,VIO,k)
  # The judge and the new phrasing share the same short–long cadence mark.
  st=phase(t,a('自己写法')-.12,a('自己写法')+.50)
  if st:
   for ox,oy,op_ in ((871,286,st),(x2-102,y2+55,cq)):
    for jj,ww in enumerate((13,22,39)):
     rect(g,ox+jj*43,oy,ww,4,VIO,op_)
  if cq:swish(g,x2-113,x2+198,y2+61,t-rep-.12,VIO,.61);etch(g,'同一件事 · 改写示意',x2-115,y2+127,26,M,cq)
 if extra:
  k=phase(t,win-.21,win+.36);x=x2+291;y=y2+88
  path(g,[(x-11,y-39),(x,y-39),(x,y+68),(x-11,y+68)],extra,O,2.6)
  etch(g,'重复',x+12,y+10,25,O,extra)
  if k:dot(g,x1+38,y1+107,9,Y,k*.30);dot(g,x2-112,y2+204,8,Y,k);etch(g,'长度偏见 · 扩写示意',x2-87,y2+204,27,O,k)
