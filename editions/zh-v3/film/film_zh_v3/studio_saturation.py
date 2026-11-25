"""From one marked answer to a headroom caliper. Every distance on the final ruler is in percentage points."""
from ink import *
from motion import transit
from ink_words import swish
from studio_examples import pstep,area,BLUE,VIO
from mounting import etch
from timeline3 import W
from functools import lru_cache
SCORES=(84.7,88.7,90.2);MODELS=('GPT-4','GPT-4o','GPT-4.1');COL=(C,T,Y)
@lru_cache(1)
def sources():
 a=json.loads((W/'source/mmlu-abstract_algebra.json').read_text())[0];h=json.loads((W/'source/mmlu-high_school_world_history.json').read_text())[1]
 assert a['choices'][a['answer']]=='1' and h['choices'][h['answer']]=='Decolonization'
 return h['answer'],a['answer']
def bead(g,x,y,r,col,op=1):
 dot(g,x,y,r,col,op*.38);ring(g,x,y,r,col,op,2.1);dot(g,x,y,r*.30,col,op)
def saturation(g,c):
 t=c.t;a=c.at;prob=a('概率也验过');math_=a('算术题');veil=a('前面的字');pick=a('最后选');result=a('直接判');key=a('标准答案');auto=a('自动批改');subj=a('学科的成绩');name=a('MMLU');n57=a('五十七个');hist=a('历史题');alge=a('代数题');data=a('公开试卷');tg=[a(z)for z in('从 GPT-4','到 GPT-4o','再到 GPT-4.1')];hint=a('三个点');grow=a('分数还能');room=a('空间却');eye=a('眼睛盯住');close=a('同一张卷子');sat=a('基准饱和')
 before=1-phase(t,subj-.40,subj+.46);roll=phase(t,subj-.48,subj+.54)*(1-phase(t,data-.46,data+.28));board=pstep(t,data-.31,.76)
 if before:
  once=1-phase(t,math_-.55,math_+.26)
  if once:
   for j,(lb,co,tr)in enumerate((('字节',C,.04),('分域',VIO,a('领域拆开')),('概率和',T,prob))):
    u=pstep(t,tr-.09,.58);x=402+j*376;y=418
    if u:
     bead(g,x,y,43,co,once*u);check(g,x,y,16,True,once*u);etch(g,lb,x,y+98,33,co,once*u,'center')
     if j:path(g,[(x-315,y),(x-63,y)],u,co,2.0,once*u)
  new=1-once;paper=phase(t,veil-.28,veil+.64);choice=pstep(t,pick-.14,.52)
  # Same two measured decisions as Beat 2. A neutral mask removes context, not either answer.
  if new:
   op=new*before
   lx=390-84*paper;yy=418;line(g,(lx-160,yy+87),(1097,yy+87),M,1.7,op*.72)
   etch(g,'9 − 7 =',lx+54,yy,80,F,op*(1-paper*.82),'center')
   if paper:
    x=lx-135+388*paper;line(g,(x,yy-67),(x,yy+67),C,3.1,op*(1-paper*.68))
   for j,(val,co,lb)in enumerate((('2',VIO,'指令版'),('3',C,'基座'))):
    x=780+j*281;rr=52+7*choice;bead(g,x,yy,rr,co,op)
    etch(g,val,x,yy,54,F,op,'center')
    etch(g,lb,x,yy-115,29,co,op*choice,'center')
    k=pstep(t,result-.16+j*.115,.52);sx=x+78
    if k:check(g,sx,yy+17,16,j==0,k*op)
   inp=phase(t,key-.24,key+.48)
   if inp:
    etch(g,'答案 2',408,625,38,Y,op*inp,'center');seed=(509,625)
    for j,xx in enumerate((780,1061)):
     k=phase(t,auto-.15+j*.21,auto+.62+j*.21)
     pts=[seed,(xx,625),(xx,518)]
     xy=path(g,pts,k,Y,2.6,op*inp)
     if xy and k<1:dot(g,*xy,8,Y,op)
 if roll:
  op=roll;spread=phase(t,n57-.33,n57+1.31);step=phase(t,subj-.22,name+.68)
  # An almost-complete wheel makes 57 distinguishable subjects without ever printing a list.
  cx,cy=621,480
  count=3+sum(t>=n57+.12+(j-2)*.021 for j in range(3,57))
  for j in range(57):
   theta=-2.88+5.75*j/56
   p=phase(t,n57-.39+max(0,j-2)*.021,n57+.12+max(0,j-2)*.021) if j>2 else step
   if not p:continue
   q=clip(p);lo=177 if j%7 else 169;hi=206+16*(j%7==0);col=(BLUE,T,VIO,O,G)[(j//12)%5]
   x0,y0=cx+lo*sin(theta),cy-lo*cos(theta);x1,y1=cx+hi*sin(theta),cy-hi*cos(theta)
   line(g,(x0,y0),lerp((x0,y0),(x1,y1),q),col,6.5,op*q)
  if step:
   if t<name-.1:etch(g,'分学科计分',cx,cy,37,F,step*op,'center')
   else:
    etch(g,'MMLU',cx,cy-34,54,C,op,'center')
    etch(g,'四选一 · 分学科判分',cx,cy+25,26,F,op,'center')
    if spread:etch(g,f'{count} 门',cx,cy+83,32,Y,op*spread,'center')
   ix=phase(t,name-.21,name+.50)
   if ix:etch(g,'大规模多任务语言理解',cx,765,25,M,op*ix,'center')
  h=phase(t,hist-.43,hist+.24);al=phase(t,alge-.26,alge+.36)
  # These are two real MMLU dev questions, not custom trivia under the benchmark name.
  xx=1006
  if h:
   th=-2.88+5.75*45/56;zx,zy=cx+214*sin(th),cy-214*cos(th)
   path(g,[(zx,zy),(xx-50,359),(xx-15,359)],h,O,2.1,op);etch(g,'世界史 · 1965',xx,321,29,O,op*h)
   etch(g,'恩克鲁玛的写作背景',xx,374,33,F,op*h)
   rr=pstep(t,hist+.35,.51);etch(g,'B   去殖民化',xx,428,32,O,op*rr)
  if al:
   ga=sources();etch(g,'抽象代数 · 模 3',xx,530,29,T,op*al)
   etch(g,'x² + 1',xx,590,39,F,op*al)
   for j,n in enumerate((1,2,2)):
    r=pstep(t,alge+.03+j*.17,.40);xc=xx+171+j*63;bead(g,xc,592,23,T,r*op);etch(g,str(n),xc,592,25,F,r*op,'center')
   etch(g,'x 为 0、1、2 时的余数',xx,649,24,M,op*al)
   th=-2.88+5.75*49/56;zx,zy=cx+214*sin(th),cy-214*cos(th)
   path(g,[(zx,zy),(xx-63,567),(xx-14,567)],al,T,2.0,op)
 if board:
  # A shared unbroken scale. Later the camera physically narrows the range to 80–100 for all three.
  zoom=phase(t,eye-.30,eye+.88);floor=mix(60,80,zoom);top=204;bottom=641
  yy=lambda sc:top+(100-sc)/(100-floor)*(bottom-top)
  xs=(329,748,1169);ce=pstep(t,data-.25,.55)
  for val in (60,70,80,90,100):
   if val<floor-1e-6:continue
   y=yy(val);vop=clip((val-floor+2)/2)
   line(g,(179,y),(1436,y),M if val==100 else E,2.5 if val==100 else 1.15,board*vop*(.95 if val==100 else .72))
   etch(g,str(val)+'%',156,y,25,M,board*vop,'right')
  dy=phase(t,hint-.19,hint+.61);read=phase(t,grow-.2,grow+.66)
  for j,(x,ta,v,co) in enumerate(zip(xs,tg,SCORES,COL)):
   u=pstep(t,ta-.18,.72)
   if not u:continue
   h=mix(bottom,yy(v),u);rect(g,x-18,h,36,bottom-h,inkcol(co,.72),board*u)
   dot(g,x,h,10,co,board*u)
   etch(g,MODELS[j],x,bottom+56,33,F,board*u,'center')
   etch(g,f'{v:.1f}%',x-33,h+27,34,co,board*u,'right')
   # Pint-sized callipers become the new measurement after the models have all arrived.
   h1=pstep(t,grow+.0+j*.45,.65)
   if h1:
    xx=x+53;path(g,[(xx-9,top),(xx,top),(xx,yy(v)),(xx-9,yy(v))],h1,co,2.45,board*h1)
    tx=xx+15;etch(g,f'{100-v:.1f}',tx,(top+yy(v))*.5,28,co,board*h1)
  if dy:
   for j in range(2):
    p=pstep(t,hint-.2+j*.34,.53);path(g,[(xs[j]+14,yy(SCORES[j])-3),(xs[j+1]-16,yy(SCORES[j+1])-3)],p,Y,1.9,board*p*.68)
  if read:
   etch(g,'距满分 · 百分点',1408,top-43,27,O,board*read,'right')
  z=pstep(t,close-.20,.61)
  if z:
   # A 5.5pp rise across the three checkpoints does not mean zero measurement uncertainty.
   p=phase(t,close-.11,sat+.18)
   x,y=transit((xs[0]+43,yy(SCORES[0])-19),(xs[-1]+61,top),p,-24)
   if p<.98:dot(g,x,y,7,Y,board*sin(pi*p)**.6)
  sat_=pstep(t,sat-.17,.53)
  if sat_:etch(g,'基准饱和',1378,yy(90.2)+90,31,Y,board*sat_,'right')
  etch(g,'MMLU · 零样本',178,745,26,C,board)
