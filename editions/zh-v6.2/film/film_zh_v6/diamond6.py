"""Keep the selected question in view as the measured pool grows around it."""
from rig4 import *
def close(g,c,paint):
 t=c.t;a=c.at;count=a('一百九十八');study=a('资料全摊');try_=a('真推理功夫')
 move=easepos(t,count-.46,1.41);lift=enter(t,count-.23,.68)
 if move<1:
  paint();shade(g,move) # clear old arm labels before the same sample acquires neighbours
 # One mark per selected question. The example under the magnifier is not a
 # claim about the distribution of subjects or individual validators.
 p=easepos(t,count-.24,1.39)
 row,cols=11,18;acc=0
 scal=mix(.74,1.,p);cx=558;cy=416
 expand=easepos(t,study-.28,1.31);focus=enter(t,study-.09,.66)
 for j in range(row):
  for k in range(cols):
   idx=k+cols*j;phase_=enter(t,count-.32+.0145*(k+j*2),.51)
   v=mix(1281,cx+(k-8.5)*38.,p);w=mix(713,cy+(j-5)*32.,p)
   sc=phase_*.41+.59;op=phase_*lift
   # A warm rack opens in ordered rows, not an artificial model scoreboard.
   X=mix(v,v-112,expand);Y_=w+16*expand
   co=Y if idx==105 else blend(O,T,(.5+.5*cos((k*13+j*29)*.25))*.60)
   if op:rect(g,X-8.3*sc,Y_-8.3*sc,16.6*sc,16.6*sc,co,op*.91)
   if idx==105 and op:
    xx,yy=X,Y_;one=(X,Y_)
 countvis=enter(t,count-.22,.57)
 label(g,'GPQA Diamond',235,167,32,F,countvis*phase(move,.76,1.),'left')
 mark(g,'198',246,687,58,t-count+.21,Y,'left','pen',.55,countvis)
 label(g,'题',360,687,30,Y,countvis,'left')
 if focus:
  src=(cx+(105%cols-8.5)*38.-112*expand,cy+(105//cols-5)*32.+16*expand)
  x=mix(1070,1182,expand);y=mix(534,388,expand)
  v=.87+.13*expand;avail=focus*(.63+.37*expand)
  photo(g,AS/'gpqa-question.png',x,y,523*v,tilt=-.045+.031*expand,op=avail)
  glance=enter(t,study-.15,1.00)
  if glance:
   R0=11+4*focus;ring(g,*src,R0,Y,focus,2.0)
   where=(x-260*v,y+15);d0=[(src[0]+14,src[1]),(843,mix(src[1],where[1],.32)),where]
   path(g,d0,glance,Y,2.3,focus)
  do=enter(t,try_-.20,.68)
  if do:
   # The paper and the reasoning path are distinct. The small 4 by 4
   # scaffold is the earlier enumerated case, never a new set of test facts.
   xx,yy=1199,649
   n=4
   for i in range(n):
    for j in range(n):
     lift_=enter(t,try_-.18+.075*(i+j),.41)
     rect(g,xx+31*(i-1.5)-9,yy+25*j-10,18,19,T,do*lift_)
   label(g,'4 × 4',xx-138,yy+32,35,T,do)
