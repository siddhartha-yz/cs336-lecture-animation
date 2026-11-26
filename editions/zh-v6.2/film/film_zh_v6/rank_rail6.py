"""Three real sources become four rulers; follow a single family's positions."""
from rig4 import *
from motion import guide

X=(289,623,961,1297);TOP=242;BOTTOM=615
SOURCE=(366,804,1242);WHICH=(0,0,1,2)
NAMES=('智能指数','每题成本 ↓','匿名盲测','词元用量')
FAMILIES=(C,V,T,O);METRICS=(C,O,V,T)


def birthplace(source,i):return SOURCE[source]-70+47*i,338+22*(i%2)
def ordinate(r,j):return mix(BOTTOM,TOP,r['pct'][j]/100.)


def draw(g,c,start,models):
 t=c.t;left=c.at('每一列');order=c.at('末位到首位');merge=c.at('同一组模型家族')
 pick=c.at('现在挑');name_at=c.at('盯住');line_at=c.at('连成一条线');arrival=c.at('这三个来源')
 focus=c.at('从指数移到');idx=c.at('移到每题成本');jump=c.at('一下跃高')
 second=c.at('换到匿名盲测');third=c.at('再换到用量');last=c.at('名次又变了')
 follows=c.at('脱离场景');rank_ends=c.at('谁是第一');conclusion=c.at('问错了方向')
 assert models[0]['name']=='GPT-6 Luna'
 sel=models[0];raw=(f"{sel['index']:.1f}",f"${sel['cost']:.2f}",str(round(sel['arena'])),f"{sel['traffic_T']:g}T")
 seam=easepos(t,left-.34,1.06);off=1-easepos(t,left-.65,.51);spot=enter(t,name_at-.17,.57)
 pp=[(x,ordinate(sel,j))for j,x in enumerate(X)]

 # The first column keeps Artificial Analysis's mark; the cost column is the
 # second coordinate of the very same record. No independent duplicate name.
 for j,x in enumerate(SOURCE):
  a=enter(t,start+.23*j,.55)*off;co=METRICS[(0,2,3)[j]]
  if a:
   label(g,('Artificial Analysis','Chatbot Arena','OpenRouter')[j],x,200,35,co,a)
   line(g,(x-119,247),(x+119,247),co,2.,a)
 for i,r in enumerate(models):
  a=enter(t,merge-.53+.096*i,.47)*off
  if a:
   xx=410+(i%2)*726;yy=537+(i//2)*100
   dot(g,xx-139,yy,7,FAMILIES[i],a)
   label(g,r['name'],xx-114,yy,29,F,a,'left',340)
 a=enter(t,start+.22,.57)*off
 if a:label(g,'取三个来源都能辨认的模型家族',800,746,25,M,a)

 bars=enter(t,left-.13,.59);ranks=enter(t,order-.40,.78)
 for j,x in enumerate(X):
  u=enter(t,left-.17+.095*j,.64);a0=bars*u
  if a0:
   cy=(TOP+BOTTOM)*.5;length=(BOTTOM-TOP)*.5
   line(g,(x,cy-length*(.19+.81*u)),(x,cy+length*(.19+.81*u)),M,2.05,a0)
   label(g,NAMES[j],x,BOTTOM+61,33,METRICS[j],a0)
 if ranks:
  for y,s in ((TOP,'组内首位'),(BOTTOM,'组内末位')):label(g,s,167,y,25,M,bars*ranks,'right')
 base=(BOTTOM+TOP)/2;net=enter(t,order+.31,1.15)
 for i,r in enumerate(models):
  points=[]
  a=enter(t,arrival-.12+.12*i,.48)
  for j,x in enumerate(X):
   leave=easepos(t,left-.39+.09*j+.046*i,1.05);rank=easepos(t,order-.52+.15*j+.032*i,1.06)
   old=birthplace(WHICH[j],i);y=mix(base+(i-1.5)*30,ordinate(r,j),rank)
   side=(i-1.5)*8*math.sin(pi*rank)
   sx,sy=transit(old,(x+side,y),leave,(14+3*i)*(1 if j in (0,2)else -1));points.append((sx,sy))
   if j==1 and leave<.08:continue
   v=a*enter(t,arrival-.12+.10*WHICH[j],.48)*(phase(leave,.08,.37) if j==1 else 1)
   if not v:continue
   body=mix(10.,5.6,leave);d=mix(1.,.82-.54*spot,leave)
   if leave<.4:point(g,sx,sy,body,FAMILIES[i],v*d)
   else:dot(g,sx,sy,body,FAMILIES[i],v*d)
  if i and net:path(g,points,net,FAMILIES[i],1.85,.50*seam)

 choose=easepos(t,pick-.14,.69)
 if choose:
  # Gather the same outline before naming the axes. The final measurements only
  # get their numeric readouts as the tracer reaches each specific ruler.
  t0=enter(t,line_at-.20,.72)*(1-easepos(t,focus-.10,.49));before=easepos(t,pick-.10,focus-pick-.14)
  for j,(x,y) in enumerate(pp):
   now=enter(t,pick-.12+.09*j,.40);q=(.43+.21*sin(t*3-j*.8))*now*(1-spot)
   if q:ring(g,x,y,14+2*sin(pi*before),C,q,2.2)
  if t0:
   path(g,pp,enter(t,line_at-.21,.67),C,3.2,t0*.82)
   if t<focus:guide(g,pp,easepos(t,line_at-.21,.96),Y,t0*.88,3.55,.16)
 times=(focus-.17,idx-.15,second-.20,third-.18)
 spans=(.57,max(.65,jump-idx+.283),min(.92,third-second),min(.96,last-third))
 for j,(x,y) in enumerate(pp):
  prog=easepos(t,times[j],spans[j]);read=enter(t,times[j]+(.0 if not j else spans[j]*.79),.50)
  if j and prog:
   path(g,[pp[j-1],(x,y)],prog,Y,5.1)
   if prog<.999:
    guide(g,[pp[j-1],(x,y)],prog,O,.85,7.1,.19)
    point(g,*lerp(pp[j-1],(x,y),prog),9.0,Y)
  if read:
   point(g,x,y,9.6,C,read)
   # Measured values at the bottom live below the rising strokes; no digit is
   # crossed by the very segment it is there to explain.
   tx=x+(19 if j%2==0 else 15);ty=y+(24 if j%2==0 else -36)
   label(g,raw[j],tx,ty,30,Y,read,'left')
   smooth=times[j]+spans[j]-.10
   if t<smooth+.68:swish(g,x-23,x+23,y+(0 if j%2==0 else 18),t-smooth,C,.61,3.05)

 if spot:mark(g,'GPT-6 Luna',361,157,39,t-name_at+.17,C,mode='pen')
 # The top marker alternates two family colours. Keep the viewer on the same
 # positions instead of inventing a fifth aggregate winner.
 finish=1-easepos(t,c.d-.95,.56)
 if finish>0:
  p=easepos(t,last-.10,min(1.12,follows-last-.12))
  if p and t<follows:guide(g,pp,p,Y,finish*.87*sin(pi*p)**.57,6.9,.18)
  for j,x in enumerate(X):
   at=rank_ends-.42+.39*j;k=easepos(t,at,.65);a=enter(t,at,.40)*finish
   if a:
    i=max(range(len(models)),key=lambda i:models[i]['pct'][j]);co=FAMILIES[i]
    ring(g,x,TOP,13+12*k,co,a,2.9)
    dot(g,x,TOP,4.7,co,a)
    yy=TOP-23
    if t<at+.74:path(g,[(x-19,yy),(x+19,yy)],k,co,2.7,a)
   if t>=conclusion-.17:
    z=easepos(t,conclusion-.17,.91);a0=finish*z
    if a0:line(g,(x-21,TOP-30),(x+21,TOP-30),METRICS[j],1.9,a0)
 label(g,'同四个模型家族内比较  ·  成本越低，位置越高',802,746,26,M,enter(t,left-.10,.59))
