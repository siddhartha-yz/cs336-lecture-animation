"""Match cuts between measurements. The chapter names stay in the player."""
from rig4 import *
from v4_act2 import OP
from motion import guide
from v4_act4 import MAT
from machines import grid,ARC
from studio_tests import patch

def keyhole(g,c):
 t=c.t;q=phase(t,.34,2.58);p=enter(t,.17,.56)
 carry=1-phase(t,.02,.33)
 if carry:endpaper(g,'2-4',0,0,1.,carry)
 cells=['Choose','one',':','nine','minus','seven','…','Answer',':','two']
 origin=337;step=103
 for i,ss in enumerate(cells):
  x=origin+step*i
  if i!=len(cells)-1:
   leave=.73+.042*(8-i);ink=1-easepos(t,leave,.22)
   # Remove each set of glyphs before moving the envelope it was written on.
   # The answer is the only element still legible when the rest folds away.
   j=easepos(t,leave+.19,.48);w=mix(96,35,j);h=mix(64,11,j)
   xx=x-10*j;yy=mix(487,424+(i%2)*12,j)
   box(g,xx-w/2,yy-h/2,w,h,C,p*(1-j)*.68,inkcol(C,.25),1.55)
   if ink:label(g,ss,x,487,27,M,p*ink)
  else:
   y=mix(487,422,q);xx=mix(x,1281,q);rad=mix(41,58,q)
   ring(g,xx,y,rad,blend(Y,V,q),p,2.8);dot(g,xx,y,mix(rad-4,51,q),inkcol(blend(Y,V,q),mix(.36,.46,q)),p)
   label(g,'two',xx,y,31,Y,p*(1-phase(t,1.71,2.00)))
   label(g,'2',xx,y-2*q,50,F,p*phase(t,2.03,2.45))
 hop=phase(t,1.15,3.23)
 if hop:
  path(g,[(199,350),(199,446),(950,446)],hop,T,1.9,p*.78*(1-phase(t,c.d-.55,c.d)))
  mark(g,'9 − 7',199,300,80,t-1.25,F,'left','pen',.59,p*hop)
def two_lanes(g,c):
 t=c.t;f=1-phase(t,c.d-.65,c.d)
 travel=easepos(t,.05,1.55);form=easepos(t,c.d-.73,.71)
 M0=(mix(730,801,travel),mix(509,664,travel))
 half=mix(1,.06,travel)
 line(g,(M0[0]-95*half,M0[1]),(M0[0]+152*half,M0[1]),Y,mix(5.2,2.8,travel),f*(1-travel))
 point(g,*M0,mix(10,3.,travel),Y,f*(1-.76*travel))
 note=1-phase(t,.08,.64)
 if note:label(g,'已测的安全条件',M0[0]+43,M0[1]+64,33,O,note)
 bridge=1-phase(t,.04,.62)
 if bridge:path(g,[(518,250),(518,221),(1080,221),(1080,244)],1,M,1.7,bridge*.63)
 for j,(old,dst,col,lab) in enumerate((((353,297),(486,407),C,'是否见过题'),
                                       ((1114,247),(1129,409),T,'真实工作'))):
  x,y=transit(old,dst,travel,-15 if j==0 else 24)
  mid=(mix(M0[0],x,mix(.45,.51,travel)),mix(M0[1],y,mix(.61,.51,travel))-mix(14,17,travel))
  path(g,[M0,mid,(x,y)],1,col,mix(2.75,2.58,travel),f)
  ring(g,x,y,mix(15,9,travel),col,1-phase(t,1.16,1.62),2.25)
  h=1-phase(t,1.09,1.84);ww=mix(44,42,travel)
  if h:label(g,lab,x+(27 if j else -26),y-mix(18,29,travel),ww,col,h,'left' if j else 'right')
  k=enter(t,1.29+j*.17,.57)
  if k:
   if j==0:
    for hh,ch in enumerate('ABCD'):
     X=mix(x-74+59*hh,211+99*hh,form);Y0=mix(y,423,form)
     rect(g,X-17,Y0-17,34,35,col,k*f*.77*(1-form))
     label(g,ch,X,Y0,mix(23,53,form),F,max(form,k*f))
   else:
    from studio_field import reel
    reel(g,x,y,.68+.22*travel,.86-.57*travel,f*k)
from gates6 import array,fold_words,filing,issues_on_wire,puzzle_gate
DRAW={'door1':array,'door2':fold_words,'door3':keyhole,'door4':filing,'door5':issues_on_wire,'inter':puzzle_gate,'door6':two_lanes}
def show(g,c):DRAW[c.k](g,c)
