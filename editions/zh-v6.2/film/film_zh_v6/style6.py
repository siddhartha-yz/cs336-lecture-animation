"""Two meanings survive a change of typesetting; a ballot follows the form."""
from rig4 import *

CLAUSES=('核对发票金额','回复更正结果')
START=((627,393),(627,487))
END=(((278,414),(300,493)),((996,385),(996,478)))
CLAUSE_COLORS=(C,T)


def compare_style(g,c,start,end):
 t=c.t;same=c.at('同一件事');judge=c.at('裁判也可能');custom=c.at('自己惯用')
 syntax=c.at('句式');layout=c.at('排版');tone=c.at('口吻');vote=c.at('用了它惯用')
 compare=c.at('这里两段话');difference=c.at('分别')
 focus=during(t,difference-.14,vote+.44,.50)
 fade=1-easepos(t,end-.55,.52);draw=enter(t,start,.58)*fade
 if not draw:return
 # Keep the same two CJK paths as they leave the join. Plain courtesy and list
 # numbering have separate shapes, so the meaning does not have to be re-read.
 dy=[1.65*sin(1.19*(t-start)+2.2*i) for i in range(2)]
 for side,poses in enumerate(END):
  for i,(x,y) in enumerate(poses):
   at=same-.19+.035*i
   z=easepos(t,at,.94)
   # The duplicated paths remain hidden until the branches have a readable gap.
   r=phase(z,.56,.83);a=draw*(r if side else 1.)
   xx,yy=transit(START[i],(x,y+dy[side]),z,35*(2*side-1))
   color=blend(CLAUSE_COLORS[i],F,.67*z);color=blend(color,M,.37*focus)
   mark(g,CLAUSES[i],xx,yy,56,t-start-.15*i,color,'left','wave',.51,a)
   if z>.12:
    lit=during(t,syntax-.14+.14*i,syntax+1.03+.14*i,.32)
    path(g,[(xx,yy+36),(xx+336,yy+36)],enter(t,at+.13,.53),CLAUSE_COLORS[i],2.35,a*(.55+.45*lit-.32*focus)*z)
    swish(g,xx,xx+336,yy+36,t-compare+.11-.11*i,CLAUSE_COLORS[i],.61,2.9)
   if z<.72:continue
   pf=draw*phase(z,.72,.98)
   wrap=('请','再')[i] if side==0 else ('1.','2.')[i]
   pulse0=t-(tone if side==0 else layout)-i*.095
   pulse=during(pulse0,-.09,.84,.26)
   ck=blend(M,O if side==0 else V,max(pulse,focus*.89))
   mark(g,wrap,xx-19,yy,47,t-at-.31,ck,'right','wave',.42,pf)
   if side==0:
    dotline=('，','。')[i]
    label(g,dotline,xx+g.measure(CLAUSES[i],56,font=SERIF)+8,yy,47,M,pf,'left')
   if pulse and side==0:swish(g,xx-67,xx-18,yy+36,pulse0,O,.53,2.25)
   if pulse and side==1:swish(g,xx-63,xx-19,yy+36,pulse0,V,.53,2.35)
 # The tiny two-line template is the judge's habit, not its extra evidence.
 j=enter(t,judge-.13,.54)*draw;d=enter(t,custom-.14,.49)*draw
 bx,by=774,220
 if j:
  label(g,'裁判',bx+30,by,27,V,j,'left');area(g,[(bx-20,by),(bx,by-20),(bx+20,by),(bx,by+20)],V,j*.70)
 if d:
  by+=49
  for i in range(2):
   y=by+29*i;u=enter(t,custom-.12+.084*i,.43)*d
   label(g,f'{i+1}.',bx-26,y,20,V,u,'right');line(g,(bx-15,y),(bx+42,y),V,2.7,u)
 if t>=vote-.13:
  st=(bx+31,by+30);en=(946,532);route=[st,(876,340),(916,429),en]
  f=easepos(t,vote-.13,.81);a=enter(t,vote-.13,.40)*draw
  xy=path(g,route,f,V,1.8,a*.69*(1-easepos(t,vote+.26,.42))) if f<1 else en
  dot(g,*(xy or st),7.2,V,a)
  final=enter(t,vote+.41,.52)*draw
  if final:
   path(g,[(946,358),(929,358),(929,510),(946,510)],final,V,2.5,final)
   mark(g,'自我偏好',996,583,34,t-vote-.48,V,'left','wave',.43,final)
 label(g,'同义改排 · 示意',1423,616,24,M,draw*enter(t,same+.13,.55),'right')
