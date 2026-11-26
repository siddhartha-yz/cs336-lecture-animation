"""Five marked attempts are the same objects in the sample and in the estimator."""
from itertools import combinations
from rig4 import *
from motion6 import ArcLength
from studio_tests import patch
FIVE=(341.7,567.1,800,1032.9,1266.8)
PAIRS=tuple(combinations(range(5),2))
CO=(G,G,R,R,R)
PROOF_VALUE=(635,715)
def score_arc(t):
 # Carry the numerical readout around (never through) the already-visible
 # patches. Start near the green strip, arrive above the sample deck.
 a,b,c,d=PROOF_VALUE,(137,670),(106,178),(800,181);u=1-t
 return tuple(u**3*k+3*u*u*t*l+3*u*t*t*m+t**3*n for k,l,m,n in zip(a,b,c,d))
VALUE_RAIL=ArcLength([score_arc(j/96)for j in range(97)])

def proof(g,c,keep,ex,stop,*,parts=True,opacity=1.):
 t=c.t
 all_at=c.at('先数所有挑法');numer=c.at('分子里');denom=c.at('分母就是')
 two=c.at('抽两份');spread=c.at('所有配对摊开');bad=c.at('三对两份都错');good=c.at('剩下七对')
 num0=c.at('十对里');pass_1=c.at('单次通过率');pass_2=c.at('十分之七')
 minus=c.at('用一减去');win=c.at('至少有一份能用');in_strip=easepos(t,minus-.13,1.00)
 keep_7=easepos(t,win-.13,.68);result_op=(.57+.43*keep_7)*(1-.43*easepos(t,stop-1.45,1.42))
 unfold=easepos(t,two-.29,.74);scale=easepos(t,ex-.35,.94)
 out_=opacity
 answer=easepos(t,pass_1-.07,.54)*(1-easepos(t,two-.28,.69))
 pairno=enter(t,num0-.2,.49)
 lasts=easepos(t,pass_2-.12,.57);extend=enter(t,c.at('把五份换成')-.13,.54)
 y=mix(mix(336.375,276,unfold),326,scale)
 for i,u in enumerate(FIVE):
  x=mix(u,382+209*i,unfold)
  maybe=(i<2)
  color=CO[i];lamps=(1-unfold)*out_
  if parts:patch(g,x,y,i,color,mix(1.12*1.035,.92,unfold),out_)
  if lamps>0:
   lamp=enter(t,keep-.09+.13*i,.40)
   if lamp:
    yy=y+86;check(g,x,yy,13,maybe,lamp*lamps)
  if extend:
   uh=enter(t,denom-.14+i*.049,.4);bar0=(x-40,y+57);bar1=(x+40,y+57)
   color2=blend(O,R,enter(t,numer-.17,.62))
   if uh and (t<numer or i>=2):path(g,[bar0,bar1],uh,color2,2.0,extend*out_)
 if answer:
  mark(g,'2 / 5',800,592,71,t-pass_1+.08,Y,mode='pen',dur=.58,op=answer)
  underline(g,711,650,178,t-pass_1+.34,Y)
 floor=mix(470,467,scale);step=mix(117,108,scale)
 detail=enter(t,bad-.08,.53)
 for j,(i,k) in enumerate(PAIRS):
  xx0=356+211*(j%5);yy0=floor+step*(j//5)
  strip=easepos(t,minus-.13+.017*j,.82)
  strip_y=easepos(t,minus-.08,.70) if j<5 else easepos(t,minus+.68+.024*(j-5),.52)
  wrong=i>=2;peel=easepos(t,minus+1.25+.076*(j-7),.65) if wrong else 0.
  xx=mix(xx0,305+j*110,strip)
  yy=mix(yy0,506,strip_y)+83*peel
  gap=mix(27,19,strip);rgb=1-.21*peel
  off=.062*j if j<5 else .063*(j-5)+.245
  st=spread-.13+off
  f=easepos(t,st,.82);u=enter(t,st,.52)*out_;revealed=enter(t,st+.49,.41)*out_
  if not u:continue
  hit=enter(t,good-.12+.061*j,.38) if not wrong else 0.
  cross=easepos(t,bad-.09+.087*(j-7),.66) if wrong else 0.
  lower_level=(1-mix(.68,.15,strip)*cross*extend)*rgb
  for z,letter in enumerate((i,k)):
   src=(mix(FIVE[letter],382+209*letter,unfold),y+47)
   dst=(xx-gap+2*gap*z,yy)
   bx,by=transit(src,dst,f,-30-14*z)
   a0=u*(.78+.22*f)*lower_level
   dot(g,bx,by,11.6+2.8*hit-mix(0,2,strip),inkcol(CO[letter],.92),a0)
   if f>.92:ring(g,bx,by,13-1.4*strip,CO[letter],a0*.74,1.45)
  co=R if wrong else T
  span=mix(13,7,strip);line(g,(xx-span,yy),(xx+span,yy),co,2.,revealed*lower_level)
  label(g,'ABCDE'[i]+'ABCDE'[k],xx,yy+35,25,F if not wrong else R,revealed*lower_level)
  if hit:
   line(g,(xx-40,yy+58),(xx+40,yy+58),T,2.1,hit*out_*.86*(1-strip))
  if cross:
   half=mix(55,36,strip)
   path(g,[(xx-half,yy+17),(xx+half,yy-18)],cross,R,3.1,out_*(.92-.37*extend)*rgb)
  focus=(denom-.08+.06*j) if not wrong else (numer-.14+.13*(j-7))
  if extend and t>focus:
   focus0=during(t,focus,focus+1.12,.38)*(1-strip)
   if focus0:box(g,xx-57,yy-26,113,72,O if t<numer else R,out_*focus0,sw=1.8)
 # Two numbers are selected from the count, not independent widgets pasted to a new page.
 if pairno:
  s0=1-easepos(t,c.at('把五份换成')-.09,.58)
  label(g,'10 对',263,702,35,F,pairno*out_*s0*(1-in_strip))
 if detail:
  label(g,'3 对全错',540,702,32,R,detail*out_*(1-.65*extend)*(1-in_strip))
  label(g,'3 对全错',1185,677,32,R,enter(t,minus+1.47,.56)*out_*.92)
 if in_strip:
  # The same ten paired samples travel into the unit. Lift the complement out of
  # it; seven teal sections and the three empty positions preserve the divisor.
  a=in_strip*out_;curve=[(260,458),(260,445),(1338,445),(1338,458)]
  path(g,curve,in_strip,T,1.9,a*.83)
  label(g,'10 对',797,420,29,T,a)
  for j in range(10):
   x=305+110*j;col=T if j<7 else R
   a0=enter(t,minus+1.36+.022*j,.43)*a
   box(g,x-52,566,104,10,col,a0*(1-keep_7*.36) if j>=7 else .62*a0,inkcol(col,.16) if j<7 else None,1.25)
   if j<7 and keep_7:
    k=enter(t,win-.15+.071*j,.42)
    rect(g,x-52,566,104*k,10,inkcol(G,.94),k*a)
 if lasts and parts:
  a=mix(1-.43*extend,result_op,in_strip)
  mark(g,'7 / 10',mix(1119,PROOF_VALUE[0],in_strip),PROOF_VALUE[1],62,t-pass_2+.1,Y,mode='pen',op=lasts*out_*a)
 if scale:
  texwrite(g,'passk',800,163,734,t-ex+.17,.88,F,out_)
  if extend:
   label(g,'n = 5',245,169,34,F,extend*out_,'left')
   label(g,'c = 2',245,222,29,G,extend*out_,'left')
   label(g,'k = 2',1357,169,34,F,extend*out_,'right')
  depth=enter(t,all_at-.21,.53)
  if depth:
   top=easepos(t,denom-.28,.73);col=blend(T,R,easepos(t,numer-.18,.59))
   y_=mix(231,179,easepos(t,numer-.15,.64))
   swish(g,967,1112,y_,t-(numer if t>numer-.12 else denom)+.1,col,.68,3.0)
   if top and t<denom+2.4:path(g,[(1285,448),(1351,448),(1351,612),(1285,612)],top,T,2.3,depth*out_*(1-phase(t,denom+1.90,denom+2.4)))
