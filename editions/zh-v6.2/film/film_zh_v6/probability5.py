"""One hundred equally likely paths, regrouped without creating or erasing any of them."""
from rig4 import *
def paths100(g,c,st):
 t=c.t; s2=c.at('又各接二十个'); a=c.at('五分之一');b=c.at('二十分之一');allpaths=c.at('五乘二十');single=c.at('原文只占一条');fold=c.at('排得一样宽');ten=c.at('十乘十');root=c.at('开平方');end=c.at('十个等效选项')
 built=enter(t,st,.52);s=phase(t,fold-.12,fold+1.32);live=1-s;trace=enter(t,a-.10,.53);key=48
 cut=easepos(t,c.d-.75,.75-1/60);rest=1-phase(t,c.d-.71,c.d-.16);focus=(937.2,363.6)
 label(g,'第一步',331,104,38,C,built*live)
 label(g,'第二步',785,104,38,T,enter(t,s2-.16,.49)*live)
 if s:label(g,'同样 100 条路，重新分组',787,92,36,F,s*rest)
 rx,ry=153,404.;cx=322;ys=[194+i*103 for i in range(5)];light=enter(t,b-.11,.51)
 # Fold the ten previous equal-probability tiles into the five first-step nodes.
 old=phase(t,st,st+.68)
 if old<1:
  for j in range(10):
   px,py=transit((215.4+129.8*j,413),(cx,ys[j//2]),old,(-1 if j%2 else 1)*28);ww=mix(122.8,12,old);hh=mix(113,12,old)
   box(g,px-ww/2,py-hh/2,ww,hh,C,1-old,inkcol(C,.35),1.8)
   if old<.5:label(g,'1/10',px,py,34,F,1-2*old)
 if live:
  point(g,rx,ry,8,F,built*live)
  for r,y in enumerate(ys):
   u=enter(t,st+.053*r,.49);co=Y if r==2 and trace>.4 else C
   pts=[(rx,ry),(rx+51,ry),(cx-29,y),(cx,y)];path(g,pts,u,co,2.65,(.42+.5*(r==2))*live*u);dot(g,cx,y,11,co,u*live)
   if r==2 and trace:
    label(g,'1/5',cx-32,y-47,35,Y,trace*live)
    move=easepos(t,a-.15,.58)
    if move:
     x0,y0=lerp((rx,ry),(cx,y),move)
     pw=during(t,a-.16,a+1.44,.39)
     if pw:point(g,x0,y0,7.7,Y,live*pw)
   # All other rows still have the same width. The focus is one route, not a
   # different odds calculation for the rest of the rows.
   if r!=2 and trace and light and t<b+.63:
    pulse=during(t,a+.03+r*.146,a+.67+r*.112,.30)
    if pulse:line(g,(cx+16,y),(cx+31,y),C,1.75,live*pulse*.68)
 for i in range(100):
  r,j=divmod(i,20);ii,jj=divmod(i,10)
  z=enter(t,s2-.13+.033*j+.042*r,.43);xx=495+31.9*j;yy=ys[r];cx2=550+48.4*jj;cy2=178+46.4*ii
  u=p5(clip((s*1.19-.14*(j/19)-.05*(r/4))));x,y=transit((xx,yy),(cx2,cy2),u,(-16+8*(r%3))*sin(pi*u))
  co=Y if i==key and light>.32 else (blend(T,C,(ii%2)*.54) if s>.68 else T if r%2 else C)
  if z and live and j==0:path(g,[(cx+14,yy),(xx-21,yy)],z,T,2.0,live*z*.65)
  if z:
   ww=mix(18.5,27.6,u);h=mix(23,27.6,u)
   # Keep the one gold path stationary across the cut. All other squares
   # follow the same camera gesture into it; no old chart is ever overlaid.
   if i==key:
    rect(g,x-ww/2,y-h/2,ww,h,co,z*mix(.93,1,cut))
   else:
    f=clip(cut*1.25-(sqrt((x-focus[0])**2+(y-focus[1])**2)/594.)*.22)
    x,y=transit((x,y),focus,f,9.+5*math.sin(j*.71))
    w1=ww*(1-.79*f);h1=h*(1-.79*f)
    if f<.999:
     rect(g,x-w1/2,y-h1/2,w1,h1,co,z*(.75+.15*(r==2))*(1-f)**1.37)
   if i==key and light:
    box(g,x-ww/2-4,y-h/2-4,ww+8,h+8,Y,light*rest,sw=2.0)
    if live:
     label(g,'1/20',x,y+38,31,Y,light*live)
     run=easepos(t,b-.19,.79);moving=run
     if moving:
      a0=(cx+14,ys[r]);a1=(x-17,y);k=during(t,b-.19,allpaths+.12,.40)
      if k:path(g,[a0,a1],moving,Y,2.30,live*k*.92)
      if .01<moving<.98 and k:point(g,*lerp(a0,a1,moving),6.6,Y,live*k)
    if single-.25<t<ten+.18:
     touch=during(t,single-.24,ten+.18,.65)
     if touch:ring(g,x,y,24+7*sin(pi*u),Y,touch*.78,2.)

 if s:
  for i in range(10):
   yy=178+46.4*i;u=enter(t,fold+.034*i,.60);line(g,(512,yy),(534,yy),T,1.9,u*s*rest)
  label(g,'10',466,382,40,C,s*rest);label(g,'步一',466,434,25,M,s*rest)
  line(g,(545,635),(998,635),T,1.8,s*rest);label(g,'步二  ·  10',769,681,30,T,s*rest)
 if t>s2:
  if t<a:
   label(g,'每个词后都有二十种续写',800,725,31,M,enter(t,s2+.37,.59))
  elif t<fold:
   col=Y;v=enter(t,a-.10,.49);w=enter(t,b-.08,.47)
   label(g,'1/5',589,716,45,C,v);label(g,'×',697,716,41,F,w);label(g,'1/20',821,716,45,T,w)
   if t>=allpaths-.24:mark(g,'= 1/100',1026,716,44,t-allpaths+.24,col,mode='pen',dur=.54)
   if t>single-.1:swish(g,936,1117,755,t-single+.10,Y,.65,3.1)
 if t>fold-.08:
  q=enter(t,fold-.08,.7)*rest;x=1258
  label(g,'走法总数',x,235,28,M,q);label(g,'100',x,314,72,Y,q)
  if t>ten-.18:
   mark(g,'10 × 10',x,414,48,t-ten+.18,C,mode='pen',dur=.61,op=rest)
   # The first factor is the number of rows; the second is width. Sweep the
   # corresponding bracket while the words pass, never move the values.
   for j,(pts,col) in enumerate(((((505,164),(485,164),(485,608),(505,608)),C),
                                  (((538,624),(538,642),(996,642),(996,624)),T))):
    st0=ten-.15+j*.43;p=enter(t,st0,.48);h=during(t,st0,ten+2.16,.43)
    if h:path(g,pts,p,col,2.4,h*.95)

  if t>root-.21:
   texwrite(g,'root100',x,519,274,t-root+.21,.66,Y,op=rest)
   label(g,'两步的等效候选数',x,616,28,T,enter(t,end-.70,.48)*rest)
