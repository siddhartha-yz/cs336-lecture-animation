"""The apparatus that makes the film a loop: keep the coordinate of a projected corner invariant."""
from rig4 import *
import opening as orig
import random
def cold(g,c):
 from cold6 import draw
 draw(g,c)
def solid(w,n,col,mel=0,al=1):
 cs=orig.corners(n)
 for face,alpha,bright in [((0,1,2,3),.30,.34),((3,2,6,7),.44,.50),((1,5,6,2),.49,.39)]:
  w.face(tuple(cs[i] for i in face),col,al*alpha,fill=bright,edge=0)
 for x,y in ((0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7)):
  old=x in (4,5,6,7);w.segment(cs[x],cs[y],blend(col,R,mel*.83),2.85 if not old else 1.85,al*(.65 if old else .96))
def block(g,c,closing=False):
 t=c.t;good=(82,80,78);other=(82,26,20);bad=(96,15,10)
 if closing:
  alt=enter(t,.14,.80);melt=0;pan=phase(t,c.at('绕过去')-.1,c.at('差别')+.3);show_dim=phase(t,c.at('多量几个方向')-.1,c.at('遮住')+.1)
  fold=0;build=1;proj=1;shadow=1;ar=[1]*3;fade=1-phase(t,c.d-7.05,c.d-5.75);theta=.39+.51*pan+.07*sin(t*.28);phi=.14-.09*pan
 else:
  show_dim=0;pan=0;build=enter(t,.08,.6)
  ar=[enter(t,c.at(q)-.19,.67)for q in ('推理','对话','自己把一件事做完')]
  proj=c.u('只准交一个分数',1.1);shadow=c.u('尺子上',1.0)
  alt=enter(t,c.at('第二个盒子')-.12,.82)*(1-phase(t,c.at('还是这同一把尺'),c.at('金色端点')+.50))
  melt=phase(t,c.at('挑下一代模型')-.12,c.at('它们被挤薄')+.48);fade=1
  fold=c.u('古德哈特定律',.60);theta=.40+.11*phase(t,0,c.at('撑起一个盒子'))-.08*proj+.048*sin(t*.15);phi=.10+.08*phase(t,0,c.at('三条边'))-.06*proj
 n=tuple(mix(q*(.2+.8*u) if not closing else q,z,melt)for q,z,u in zip(good,bad,ar));mark_=n[0]
 w=orig.roto(g,t,yaw=theta,pitch=phi,zoom=1.038+.01*math.sin(t*.17),target=(.025,.0,.0))
 orig.x_ruler(w,al=1 if closing else .24+.76*proj,labels=1 if closing else .30+.70*proj,markpos=mark_ if closing or proj>.04 else None);orig.dimension_axes(w,(.48+.52*max(ar))*fade)
 # The depth label is painted in front of the face, independent of camera ordering.
 ax0=orig.add(orig.O,(-.05,-.18,-orig.LZ-.36));px,py=w.pos(ax0)
 solid(w,n,C,melt,build*fade*(1-.47*alt))
 if alt:solid(w,other,V,0,alt*fade)
 for j,(h,color)in enumerate(zip(ar,(Y if closing else blend(C,Y,proj),C,T))):
  if closing:hi=.25+.71*max(0,sin(2.2*t-j*1.5))**4*show_dim
  else:hi=(.18+.82*max(0,1-abs(t-c.at(('推理','对话','自己把一件事做完')[j]))/1.12))*h
  orig.edge_map(w,n,hi*fade,color,j)
 if proj:
  if closing:anchor=-8.
  else:anchor=c.at('光沿平行线')
  orig.shadow_tracks(w,n,t,anchor,Y,build*proj*fade)
  if alt:orig.shadow_tracks(w,other,t,(-5 if closing else c.at('第二个盒子')-.35),V,alt*fade)
  a=orig.add(orig.O,(0,.03,.037));b=orig.add(orig.O,(orig.LX*mark_/100*shadow,.03,.037));w.segment(a,b,Y,4.7,proj*fade);orig.pin(w,b,Y,.067,proj*fade)
 w.draw()
 if ar[2]*fade>.005:
  path(g,[(px,py),(px-42,py-38),(px-154,py-38)],.99,T,1.53,ar[2]*fade)
  label(g,'自主规划',px-64,py-67,26,T,ar[2]*fade)
 if not closing:
  xx,yy=1055,218
  label(g,'模型 A',xx,yy,32,C,build,'left');label(g,'B',1450,yy,31,V,alt,'right')
  for j,(v,vb,name,co)in enumerate(zip(n,other,('推理','对话','自主规划'),(blend(C,Y,proj),C,T))):
   y=yy+71+j*98;h=ar[j];label(g,name,xx,y-14,28,co,h,'left');line(g,(xx,y+20),(xx+246,y+20),E,1.7,h)
   co2=blend(co,R,melt*.85)if j else co;line(g,(xx,y+20),(xx+2.46*v,y+20),co2,5.2,h);point(g,xx+2.46*v,y+20,5.7,co2,h)
   label(g,str(round(v)),xx+267,y+20,29,co2,h,'left')
   if alt:line(g,(xx,y+34),(xx+2.46*vb,y+34),V,3.8,alt);dot(g,xx+2.46*vb,y+34,4,V,alt);label(g,str(vb),1450,y+32,24,V,alt,'right')
  sha=phase(t,c.at('也落在八十二')-.15,c.at('也落在八十二')+.5)*alt
  if sha:
   x,y=w.pos(orig.add(orig.O,(orig.LX*.82,0,.06)));label(g,'同影',x+82,y+83,28,V,sha)
   path(g,[(x+8,y+10),(x+44,y+64),(x+61,y+64)],1,V,1.6,sha)
  if fold:
   mark(g,'Goodhart’s law',1107,589,41,t-c.at('古德哈特定律')+.07,R,'left','pen')
   label(g,'指标成为目标',1109,648,28,F,fold,'left');label(g,'漏量的退步仍能过关',1109,696,26,M,fold,'left')
  if t>c.at('可要是'):shade(g,.65*phase(t,c.at('可要是')-.18,c.at('可要是')+.62))
 else:
  if show_dim:
   # Six rays are attached to one small measuring instrument; no new chart title.
   ox,oy=1232,385;labels=('概率','推理','对话','行动','安全','生态与清白');vals=(.83,.61,.69,.77,.42,.84);vals2=(.83,.48,.59,.24,.73,.55);cols=(Y,T,V,C,R,G)
   for j,(lab,co)in enumerate(zip(labels,cols)):
    u=clip(show_dim*2-j*.18);an=-pi/2+j*tau/6;xf,yf=ox+176*cos(an),oy+176*sin(an)
    path(g,[(ox,oy),(xf,yf)],u,co,1.9,fade);label(g,lab,ox+211*cos(an),oy+202*sin(an),28,co,u*fade)
   for vs,co in [(vals2,V),(vals,C)]:
    pts=[(ox+176*vs[j]*cos(-pi/2+j*tau/6)*show_dim,oy+176*vs[j]*sin(-pi/2+j*tau/6)*show_dim) for j in range(6)]
    if fade:g.poly(pts,co,2.4,fade,True,inkcol(co,.80),.30*fade)
   label(g,'多方向示意',ox,693,24,M,fade)
  shade(g,1-fade)
  a=during(t,c.d-5.80,c.d-1.50,.60)
  if a:mark(g,'Stanford CS336 · Lecture 12',800,450,46,t-c.d+5.80,F,'center','pen',.73,a)
def projection(g,c):block(g,c)
def closing(g,c,*,time=None):
 t=c.t if time is None else time;rotate=phase(t,c.at('绕过去')-.19,c.at('先前被影子')+.5);net=phase(t,c.at('多量几个方向')-.08,c.at('多量几个方向')+1.31)
 # 2.5 seconds to watch the finished instrument after the final spoken word.
 bye=c.s['speech']+2.5;out=1-phase(t,bye,bye+.85)
 if out>.001:
  # The same 82-point bodies change seats rather than spawning a small competing dashboard.
  # Their first exposure has the same camera as the opening projection. Later the six
  # measurement directions grow around these *same* two solids.
  vec=orig.coords(0,(82,80,78));centre=tuple(o+z for o,z in zip(orig.O,(vec[0]/2,vec[1]/2,-vec[2]/2)))
  target=tuple(mix(a,b,rotate)for a,b in zip((.025,0,0),centre))
  yaw=.43+.53*rotate+.11*sin(t*.23)*rotate
  w=orig.World(g,yaw=yaw,pitch=.14+.13*rotate,zoom=1.035-.41*rotate,target=target,distance=16,center=(800,419))
  orig.x_ruler(w,al=out*(1-.80*rotate),labels=1-.90*rotate,markpos=82)
  orig.dimension_axes(w,out*(1-rotate));solid(w,(82,80,78),C,0,out*(.73-.37*rotate));solid(w,(82,26,20),V,0,out*.85)
  if rotate<1:
   orig.shadow_tracks(w,(82,80,78),t, -8,Y,(1-rotate)*out);orig.shadow_tracks(w,(82,26,20),t,-8,V,(1-rotate)*out)
  w.draw()
  if net:
   ox=800;oy=418;phi=.11*sin(t*.21)*rotate;rx,ry=486,288
   labs=('概率','推理','对话','行动','安全','生态与清白');cols=(O,C,T,Y,R,V)
   def p(j,f):a=-pi/2+j*tau/6+phi;return (ox+rx*f*cos(a),oy+ry*f*sin(a))
   for f in (.34,.67,1):
    ps=[p(j,f*net)for j in range(6)];path(g,ps+[ps[0]],net,'#58606A',1.28,out*.48)
   for j,(lab,col)in enumerate(zip(labs,cols)):
    h=clip(net*1.63-j*.098);finish=p(j,h);path(g,[(ox,oy),finish],1,col,2.25,out*h*.74)
    xx,yy=p(j,1.19);label(g,lab,xx,yy,35,col,h*out)
   for vals,col in (((.86,.75,.73,.63,.51,.81),C),((.86,.37,.31,.72,.78,.45),V)):
    pts=[p(j,v*net)for j,v in enumerate(vals)]
    g.poly(pts,col,3.25,out,True,inkcol(col,.45),.20*out)
    for j,pt in enumerate(pts):dot(g,*pt,5.6,col,out*net)
   label(g,'六个方向 · 示意',1356,731,24,M,net*out,'right')
  shade(g,1-out)
 from opening_carriage6 import credit
 credit(g,c,t,bye)
def doors(g,c):
 from question_doors6 import show
 show(g,c)
def front(g,c):
 from opening_carriage6 import opening
 opening(g,c)
