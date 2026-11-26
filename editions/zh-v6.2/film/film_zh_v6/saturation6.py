"""The top of the old exam is finite. Move the eye into the shrinking space above the bars."""
from rig4 import *
from motion import guide

SUBJECTS=(('世界史','恩克鲁玛 · 非殖民化',41,C),('抽象代数','ℤ₃[x] / (x² + c)',12,V))
MODELS=('GPT-4','GPT-4o','GPT-4.1');VALS=(84.7,88.7,90.2);CO=(C,T,V)
def exam(g,c,wheel):
 t=c.t;a=c.at;n=57
 early=a('世界史');alg=a('抽象代数');different=a('背后用的')
 score=a('前沿模型的得分');lift=a('盯住旧试卷');tip=a('那一小截空隙')
 shrinks=a('越来越少');pub=a('公开试卷');chase=a('哪儿使劲')
 lock=a('卷子自己');sat=a('基准饱和')
 pivot=phase(t,score-.39,score+.54);rr=1-pivot
 if rr:
  name=enter(t,wheel,.55);op=name*rr
  opening=phase(t,wheel-.04,wheel+1.22);x0=760;y0=403;r=223
  focus0=enter(t,early-.13,.59);focus1=enter(t,alg-.15,.61)
  fold=phase(t,early-.23,early+.67)
  cx=mix(x0,788,fold);cy=mix(y0,393,fold);rad=mix(r,r-21,fold)
  for i in range(n):
   pp=enter(t,wheel-.19+.016*i,.48);theta=-pi*.5+i*tau/n
   z=math.cos(theta);v=math.sin(theta);co=(C,T,V,O)[i%4]
   ob=(1-.62*focus0)+.20*focus1;h=38+6*math.cos(i*1.29)**2
   if abs(i-41)<2 and focus0:
    co=blend(co,C,focus0);ob=mix(ob,1.,focus0);h+=13*focus0
   if abs(i-12)<2 and focus1:
    co=blend(co,V,focus1);ob=mix(ob,1.,focus1);h+=13*focus1
   x,y=transit((931 if i%2==0 else 1281,422),(cx+rad*z,cy+rad*v),p5(pp),-30+10*sin(i*2.3))
   path(g,[(x,y),(x+h*z*pp,y+h*v*pp)],pp,co,4.5+1.3*pp,rr*pp*ob)
  mark(g,'MMLU',cx,cy-19,65,t-wheel-.29,F,mode='pen',dur=.64,op=rr*(1-.22*focus1))
  label(g,'57 学科 · 四选一',cx,cy+67,32,T,enter(t,wheel+.77,.49)*rr)
  for i,(top,line_,ix,col) in enumerate(SUBJECTS):
   at=(early,alg)[i];p=enter(t,at-.22,.57);op=rr*p
   if not op:continue
   theta=-pi*.5+ix*tau/n;tx=cx+(rad+54)*cos(theta);ty=cy+(rad+54)*sin(theta)
   xx=188 if not i else 1105;yy=239 if not i else 516
   stop=(xx+334,yy+108) if not i else (xx-28,yy+44)
   path(g,[(tx,ty),(stop[0],ty),(stop[0],stop[1])],p,col,2.0,op)
   label(g,top,xx,yy,38,col,op,'left')
   mark(g,line_,xx,yy+72,32,t-at-.17,F,'left','wave',.44,op)
   if t>different-.15:
    tag=enter(t,different-.18+i*.14,.54)
    label(g,('读史料','做推导')[i],xx,yy+129,24,col,op*tag,'left')
 if not pivot:return
 ctx=g.c;ctx.save()
 # Change the framing on the same three measured marks; their tops keep
 # their distances from the ceiling while the eye gets an uncluttered closer view.
 z=easepos(t,tip-.20,max(1.20,shrinks-tip+1.15))
 r0=1+.115*z;yoff=22*z;ctx.translate(800,194+yoff);ctx.scale(r0,r0);ctx.translate(-800,-194)
 top=202;floor=633;starts=(379,800,1221);w=142
 part=phase(t,lift-.24,tip+.39)
 line(g,(211,top),(1383,top),F,2.0,pivot*.80);label(g,'100%',1382,153,31,F,pivot,'right')
 for j,(name,value,col,x) in enumerate(zip(MODELS,VALS,CO,starts)):
  gpop=enter(t,score-.24+j*.148,.72);y=floor-(floor-top)*(value/100)*gpop;fade=pivot*gpop
  rect(g,x-w/2,y,w,floor-y,inkcol(col,.71+.12*part),fade)
  if gpop:line(g,(x-w/2,y),(x+w/2,y),col,2.7,fade)
  label(g,name,x,floor+46,31,col,fade)
  mark(g,f'{value:.1f}%',x,y+41,37,t-score+.19-j*.148,'#141414',mode='wave',dur=.47,op=fade)
  search=phase(t,lift-.16,shrinks+.46)*(len(starts)-1)
  bar=math.exp(-((j-search)/.43)**2);k=enter(t,tip-.12+j*.19,.54)
  if part:
   xx=x+86;path(g,[(xx-9,y),(xx+9,y),(xx+9,top),(xx-9,top)],part,O,2.2,fade*(.52+.48*bar))
   # A highlighted strip can contract with real headroom without inventing another model score.
   q=part*k;rect(g,x-w/2,top+2,w,(y-top-2)*q,col,fade*.13*q)
   if k:
    label(g,f'{100-value:.1f}',x,top+(y-top)*.50,29,F,fade*k*(.68+.32*bar))
  move=enter(t,chase-.18+.10*j,.54)
  if move and t<lock+.8:
   ht=phase(t,pub-.24,chase+.62);u=phase(t,chase-.34+.13*j,lock+.28+.16*j)
   # The thin arrow points to the old public metric, not to an invented increment.
   path(g,[(x+108,floor-67),(x+138,floor-99),(x+138,y+31),(x+w*.50,y+14)],u,col,2.0,ht*.59*(1-phase(t,lock-.18,lock+.38))*fade)
   if .01<u<.995:guide(g,[(x+108,floor-67),(x+138,floor-99),(x+138,y+31),(x+w*.50,y+14)],u,col,fade*.98,3.2,.20)
 ctx.restore()
 if part:label(g,'到满分还差的百分点',1498,114,24,M,part*pivot,'right')
 if pub-.21<t<lock+.6:
  pr=enter(t,pub-.20,.51)*(1-phase(t,lock-.19,lock+.50))
  label(g,'公开试卷',119,703,28,T,pr,'left');path(g,[(115,725),(230,725),(264,683)],phase(t,pub-.09,chase+.17),T,1.8,pr)
 if t>sat-.45:
  at=enter(t,sat-.44,.53);path(g,[(232,160),(311,160),(342,192)],at,Y,2.10)
  mark(g,'基准饱和',216,117,42,t-sat+.45,Y,'left','pen',.49,at)
