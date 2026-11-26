"""Weight by token count or by domain: two different measurements, drawn as material."""
from rig4 import *
def weight(g,c):
 t=c.t;glance=c.at('代码和数学');size=c.at('词元数远远多');pron=c.at('Paloma')
 a=enter(t,.32,.66)*(1-phase(t,pron-.55,pron+.34))
 if not a:return
 # The amount of each material is schematic. The fine blue/purple strips
 # keep their area while the much larger web population contributes more.
 name=(('网页',80,O),('代码',12,C),('数学',10,T))
 tall=c.at('很容易让');x0=(196,842,1169);place=enter(t,tall-.19,.69)
 see=enter(t,glance-.21,.62);check_at=enter(t,size-.24,.67)
 for j,((nm,n,col),x)in enumerate(zip(name,x0)):
  z=enter(t,.66+.31*j,.63)
  if z:
   label(g,nm,x,265,36,col,z*a,'left')
   for i in range(n):
    y=333+40*(i//(16 if not j else 5));xx=x+36*(i%(16 if not j else 5))
    gate=enter(t,.70+.023*i+.31*j,.44)
    sq=28.;mark_op=gate*a*(.91-.32*see if not j else .59+.39*see)
    if gate:rect(g,xx,y,sq,24.,col,mark_op)
   if j and see:
    x2=x+177;u=enter(t,glance-.16+.27*(j-1),.66)
    path(g,[(x-10,318),(x-10,308),(x2,308),(x2,318)],u,col,2.15,see*a)
 if place:label(g,'词元数决定权重',196,163,37,F,place*a,'left')
 if check_at:
  X=245;Y_=675;W=1095
  v=easepos(t,size-.23,1.23)
  # One band for all the tokens; 80+12+10 units, not an assumed PPL.
  for j,(_,n,col) in enumerate(name):
   acc=sum(x[1]for x in name[:j]);w=W*n/102;xx=X+W*acc/102
   q=enter(t,size+.21+j*.12,.54)
   if q:
    rect(g,xx,Y_,w*q,28,col,a*check_at*.90)
    ring_=during(t,size-.22+j*.18,size+1.05+j*.28,.39)
    if ring_:
     src=(x0[j]+32,Y_-164+(23*j))
     dest=(xx+w*.5,Y_-7);head=transit(src,dest,v,-26)
     point(g,*head,5.6,col,a*ring_)
  label(g,'同一个分母',X,Y_+62,28,M,a*check_at,'left')
  label(g,'示意',1350,Y_+57,24,M,a*check_at,'right')

def aggregate(g,c,pal,positions,read_at):
 t=c.t;a=c.at
 each=c.at('一家一票');logs=a('对数困惑度');avg=a('取平均');expo=a('再取指数')
 out=1-phase(t,a('还有一道')-.45,a('还有一道'));u=enter(t,read_at-.20,.55)*out
 if not u:return
 panelnote(g,'六域等权 PPL','一家一票，六个对数取平均',1120,215,t-read_at+.09,Y,u)
 enter_log=easepos(t,logs-.07,.86);pack=easepos(t,avg-.10,.94)
 exponent=phase(t,expo+.19,expo+1.38);ages=enter(t,expo-.10,.63)
 axes_y=(407,568);X0=1118;dx=52;ww=43.
 for model,b in enumerate((C,V)):
  y=axes_y[model];vals=[log(e['values'][model])for e in pal];mean=sum(vals)/len(vals)
  scale=38.;shape=u*(1-exponent)
  labels=('八点三二','八点二二');r=enter(t,a(labels[model])-.13,.55)
  flush=phase(t,logs-.21,logs+.64)
  for i,l in enumerate(vals):
   dest=(X0+dx*(i+.5),y)
   ts=each-.22+.067*i+.10*model;flight=easepos(t,ts,.66)
   x,yy=transit((positions[i],(389,519)[model]),dest,flight,-32-4*(i%3))
   v=enter(t,ts,.56)*shape;w=mix(7.,ww,flight)
   if v:
    # Equal bases. Opening different heights into one level conserves the
    # summed log-loss area throughout the move, not just at its endpoints.
    height=mix(10.,scale*mix(l,mean,pack),enter_log*flight)
    col=inkcol(b,.62+.31*(i%3)/2)
    rect(g,x-w/2,yy-height,w,height,col,v*.93)
    if flush:line(g,(x-w/2,yy-height),(x+w/2,yy-height),b,1.85,v*flush)
  if flush:line(g,(X0,y),(X0+312,y),M,1.45,shape*flush*.81)
  if pack:
   mid=1274;X=mix(X0,mid-19,exponent);Q=mix(X0+312,mid+19,exponent)
   y0=mix(y-scale*mean,y-18,exponent)
   path(g,[(X,y0),(Q,y0)],pack,Y,2.7,u*pack*(1-r))
   if exponent<1:point(g,Q,y0,4.85,Y,u*exponent)
  if ages:
   p0=exp(mean);ex=ages*(1-r)
   label(g,'exp(平均 log)',1274,y+34-13*exponent,26,M,u*ex)
   if r:
    mark(g,f'{p0:.2f}',1272,y-22,55,t-a(labels[model])+.14,b,mode='pen',op=u*r,dur=.52)
    label(g,('Llama','Mamba')[model],1451,y-20,27,b,u*r,'right')
 delta=enter(t,a('只差零点一')-.18,.55)
 if delta:
  rr=[(1160,606),(1160,617),(1431,617),(1431,606)]
  path(g,rr,delta,T,2.1,u)
  label(g,'只差 0.10',1292,661,33,Y,u*delta)
