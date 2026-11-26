"""The eight measured factors become eight lengths on one continuous board."""
from rig4 import *
from functools import lru_cache
from itertools import accumulate


@lru_cache(maxsize=4)
def sums(losses,ps):
 return (0.,*accumulate(losses)),tuple(accumulate(ps,lambda a,b:a*b))


def raise_token(g,x,y,b,a=1):
 if b<=.001:return
 s=16*b
 g.poly([(x-s,y+7),(x,y-8),(x+s,y+7)],O,2.3,a)


def scinum(p):
 k=math.floor(math.log10(p));mant=p*10**(-k)
 return f'{mant:.2f} × 10'+str(k).translate(str.maketrans('-0123456789','⁻⁰¹²³⁴⁵⁶⁷⁸⁹'))


def reading(c):
 t=c.t;m=c.at('直接连乘');e=c.at('计算机存不下');l=c.at('文章越长');loss=c.at('取负对数')
 scan=phase(t,l-.13,loss-.40) if t>=l-.13 else phase(t,m-.17,e-.10)
 power=during(t,m-.28,e+.13,.56)+during(t,l-.17,loss-.10,.42)
 u=clip(scan)*7;i=min(6,int(u));f=p5(u-i)
 return i, f, i+(f>=.85), clip(power)


def render(g,c,data,xs,yrow,in_,stop):
 t=c.t;start=c.at('是模型给这整段')-.20;more=c.at('整本书');thousands=c.at('几万个概率')
 multiply=c.at('直接连乘');short=c.at('计算机存不下');longer=c.at('文章越长');loss=c.at('取负对数')
 add=c.at('乘法变成加法');average=c.at('平均损失');exp=c.at('取指数')
 intuition=c.at('它有一个很好用');one=c.at('每一步面临的');candidate=c.at('等效候选词数')
 ls=tuple(data['loss_nats']);ps=tuple(data['probabilities']);S,P_=sums(ls,ps);mu=data['mean_nats']
 r=easepos(t,loss-.16,1.21);fade=1-phase(t,stop-.52,stop)
 A=in_*fade;shell=A*(1-easepos(t,loss-.32,.72))
 Y0=347.;scl=9.25;bottom=607.;Ys=[Y0+s*scl for s in S]
 # One exact product travels along the steps. Show more factors symbolically;
 # the archive supplies only the eight printed probabilities.
 if shell>.002:
  startX=105;axis=enter(t,start+.08,.66);origin=(137,Y0)
  if axis:
   line(g,(startX,Y0-11),(startX,Ys[-1]+25),M,1.8,shell*axis)
   for j,n in enumerate((0,4,8,12)):
    y=Y0+math.log(10)*n*scl;line(g,(startX-7,y),(startX+8,y),M,1.9,shell*axis)
    label(g,('1','10⁻⁴','10⁻⁸','10⁻¹²')[j],startX-17,y,24,M,shell*axis,'right')
  points=[origin];move=enter(t,start+.20,.98)
  for j,x in enumerate(xs):
   at=start+.18+.11*j;f=easepos(t,at,.62);v=shell*enter(t,at,.44)
   y=Ys[j];end=Ys[j+1]
   if v:
    path(g,[(x,yrow+45),(x,y-7)],f,C,1.7,v*.40)
    za=blend(C,Y,.97 if j==2 else .16*j/7)
    line(g,(x-33,y),(x-33,mix(y,end,f)),za,3.0,v)
    if j and f>.8:dot(g,x-33,y,3.5,C,v*.8)
    if f>.43:point(g,x-33,mix(y,end,f),4.5,za,v)
    points.extend(((x-33,y),(x-33,end)))
  if move:path(g,points,move,C,1.8,shell*.61)
  last=(xs[-1]-33,Ys[-1]);tip=(1466,684)
  intensity=0.
  if t>more-.14:
   n=11;run=phase(t,thousands-.19,short+.18)
   # Dashed continuation only. The solid vertices stay tied to measured text.
   for j in range(n):
    p=j/n;u=enter(t,more-.08+.22*j,.66)
    x=mix(last[0]+14,tip[0],p);y=mix(last[1]+4,tip[1],p**1.54)
    if u:line(g,(x,y),(x+7.5,y+4+4*p),O,1.8,shell*u*(1-.44*p))
   blink=during(t,short-.13,short+1.48,.47)
   if blink:
    ring(g,*tip,12-5*run,O,shell*blink,2.15)
    point(g,*tip,3.4,O,shell*blink)
   label(g,'…',1472,641,41,O,shell*enter(t,more+.15,1.0))
   # Keep all eight old marks, with a scanning readout of their actual cumulative
   # probabilities. The long sequence beyond the last measured factor is not fitted.
   i,f,ii,lead=reading(c);intensity=lead
   if lead:
    l0=(xs[i]-33,Ys[i+1]);l1=(xs[i+1]-33,Ys[i+2]);corner=(l1[0],l0[1]);u0=.61
    focus=lerp(l0,corner,clip(f/u0)) if f<u0 else lerp(corner,l1,clip((f-u0)/(1-u0)))
    ring(g,*focus,14,O,shell*lead,2.7)
    yy=698+5*clip(lead);x0=213+16*clip(lead)
    label(g,scinum(P_[ii]),x0,yy,38,Y,shell*lead,'left')
    line(g,(x0,yy+26),(x0+229,yy+26),C,1.5,shell*lead*.72)
  z=enter(t,start+.64,.66)*(1-phase(t,longer-.21,longer+.31))*(1-.74*intensity)
  if z:
   label(g,scinum(P_[-1]),862,703,43,Y,shell*z)
   label(g,'这八个词元的联合概率',860,749,26,M,shell*z)

 # The bars are the exact old vertical offsets with a common zero. Relevelling
 # preserves the total area: sum((1−p)*l_i+p*mean(l)) = sum(l_i).
 if r>.001:
  log_op=A*enter(t,loss-.18,.47);new=enter(t,add-.19,.60)
  even=easepos(t,average-.18,1.10);zoom=easepos(t,loss+.36,1.10)
  reset=phase(t,intuition-.21,intuition+1.06)
  bar_scale=mix(scl,35.,zoom)
  addend=1-phase(t,average-.22,average+.24)
  for j,x in enumerate(xs):
   z=easepos(t,loss-.14+j*.043,.89)
   h=mix(ls[j],mu,even)*bar_scale
   end=(x,bottom-h*.5);H=Ys[j+1]-Ys[j]
   src=(x-33,(Ys[j]+Ys[j+1])*.5);xx,cy=transit(src,end,z,(j-3.5)*11)
   co=C if j!=2 else Y;a=log_op*(.58+.42*z)
   rect(g,xx-mix(1.7,34,z),cy-mix(H,h,z)*.5,2*mix(1.7,34,z),mix(H,h,z),inkcol(co,.89-.14*reset),a)
   note=enter(t,add-.20+.048*j,.52)*(1-phase(t,average-.16,average+.71))
   if note:
    label(g,f'{ls[j]:.2f}',x,635,32,co,log_op*note)
    if j<7:label(g,'+',x+(xs[j+1]-x)/2,635,27,T,log_op*note*addend)
   if z>.999 and t>intuition+.41:
    at=intuition+.41+j*.418;lit=during(t,at,at+.82,.33)
    if lit:
     y=bottom-mu*bar_scale
     if t<one+.44:
      beam=[(x,yrow+44),(x,y-22)];p=easepos(t,at,.63)
      path(g,beam,p,T,2.0,lit*A*.87);dot(g,*lerp(*beam,p),4.60,T,lit*A)
     path(g,[(x-38,y-8),(x-38,y-17),(x+38,y-17),(x+38,y-8)],enter(t,at,.49),Y,2.45,lit*A)
     dot(g,x,y+12,5.7,Y,lit*A)
  base=enter(t,loss+.55,.56)
  if base:line(g,(118,bottom),(1470,bottom),M,1.65,base*log_op)
  if new:
   h=new*(1-phase(t,average-.12,average+.39))*log_op
   if h:mark(g,'−log p',212,337,38,t-add+.13,T,'left','pen',.55,h)
  if even:
   y=bottom-mu*bar_scale;pr=enter(t,average-.03,.67)
   path(g,[(117,y),(1470,y)],pr,T,2.7,even*A)
   v=enter(t,average+.31,.47)*(1-phase(t,exp+.21,exp+1.38));u=enter(t,exp-.14,.51)
   if v:label(g,f'{mu:.4f} nat',1343,y-26,34,T,v*even*A)
   if u:
    # A detached equalized mean lands where the exponent is read, below the
    # same graph rather than opening a new page of equations.
    s=easepos(t,exp-.12,.92)
    if s<1:point(g,*transit((1298,y),(1063,714),s,-38.),7,T,u*A)
  texwrite(g,'ppl',721,725,492,t-exp+.10,.67,F,A)
  e=enter(t,c.at('也叫 PPL')-.15,.64)
  if e:
   label(g,f'≈ {math.exp(mu):.2f}',1119,723,42,Y,e*A)
   swish(g,1061,1182,752,t-c.at('也叫 PPL')+.05,Y,.56,2.8)
   if t>candidate-.17:
    # A representative position is marked; the model is about to give way
    # to a separate *uniform* example, so do not paint fractional token slots.
    wink=during(t,candidate-.17,stop-.08,.41)
    path(g,[(535,661),(535,649),(909,649),(909,661)],enter(t,candidate-.17,.58),O,2.4,wink*A)
