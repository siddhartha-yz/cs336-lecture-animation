"""Replay the archived wall-clock record as a wall clock, then keep the target."""
from rig4 import *
from datetime import date
from motion6 import ArcLength

ARCHIVE=json.loads((W.parent/'beats_real/data/nanogpt_main_track_2024_2025.json').read_text())
REC=ARCHIVE['records'];assert len(REC)==20 and ARCHIVE['cross_entropy_target']==3.28
assert REC[0]['minutes']==45.0 and REC[-1]['minutes']==2.992
FIRST,LAST=(date.fromisoformat(REC[k]['date'])for k in (0,-1))
L=229.;R0=1413.;BASE=647.
def graph_point(day,minutes):
 return (L+(R0-L)*(date.fromisoformat(day)-FIRST).days/(LAST-FIRST).days,
         BASE-minutes*8.48)
def goldrail(g,a,b,q,op):
 if op<.003:return
 q=clip(q)
 xx,yy=lerp(a,b,q);g.line(*a,xx,yy,Y,2.3,op,[6.4,5.3])
def watch(g,x,y,r,op,q):
 if op<.002:return
 ring(g,x,y,r,F,op,2.10);point(g,x,y,min(4.2,r*.43),Y,op)
 ang=-pi*1.20+q*2.93
 line(g,(x,y),(x+r*.72*cos(ang),y+r*.72*sin(ang)),O,2.38,op)
 if r>15:
  for j in range(12):
   an=j*tau/12;inn=r-(9 if j%3==0 else 4)
   line(g,(x+inn*cos(an),y+inn*sin(an)),(x+r*cos(an),y+r*sin(an)),M,1.4,op)
  path(g,[(x-5,y-r-3),(x-5,y-r-12),(x+8,y-r-12),(x+8,y-r-3)],1,F,1.6,op)
def latest(g,c,fin):
 from v4_act1 import _speed_finish
 t=c.t;a=c.at;q=easepos(t,fin-.0,1.36)
 first=a('历史记录')-.08;last=a('不到三分钟')
 motion=a('真正的训练提速');loss=a('这条线量的');how=a('如果语言模型')
 fs=1-phase(t,fin,fin+.57);alive=1-phase(t,loss+.25,loss+1.36)
 line0=((931,494),(1495,494));line1=((229,715),(1413,715))
 if fs:
  # The outgoing sim uses its own untouched geometry. Clear it once through
  # the right-hand watch port; no two axes grow through one another.
  cx=g.c;cw=cx.get_target().get_width();work=_speed_finish(cw)
  cx.save()
  if t>=fin+.13:
   # Keep just the transported form of the watch, not a second stamped copy.
   cx.new_path();cx.rectangle(0,0,1600,900);cx.new_sub_path()
   cx.arc(1405,153,56,0,tau);cx.set_fill_rule(cairo.FILL_RULE_EVEN_ODD);cx.clip()
  cx.scale(1600/cw,1600/cw);cx.set_source_surface(work,0,0);cx.paint_with_alpha(fs);cx.restore()
 kn=enter(t,fin+.43,.75)*alive
 startx,starty=graph_point(REC[0]['date'],REC[0]['minutes']);hand=transit((1405,153),(startx,starty),q,-120)
 if fin+.13<=t<fin+1.36:
  watch(g,*hand,mix(36,5.2,q),enter(t,fin+.09,.27)*(1-phase(q,.87,1)),q)
 if alive:
  # One shared threshold at exactly 3.28; the new vertical coordinate is time.
  rim=max(0.,1.-fs)*alive
  aa=lerp(line0[0],line1[0],q);bb=lerp(line0[1],line1[1],q)
  goldrail(g,aa,bb,1,rim)
  if q>.998:label(g,'3.28 · 留出验证目标',aa[0]+34,aa[1]+39,30,Y,rim*enter(t,fin+1.22,.58),'left')
  p=enter(t,fin+.63,.76)*alive;line(g,(L,BASE),(R0,BASE),M,1.9,p)
  path(g,[(L,BASE),(L,202)],p,M,1.9,alive)
  label(g,'实际用时（分钟）',L-43,167,33,F,kn,'left')
  for k,n in enumerate((0,15,30,45)):
   yy=BASE-n*8.48;vis=enter(t,fin+.65+.06*k,.54)*alive
   line(g,(L-8,yy),(L,yy),M,1.7,vis)
   label(g,str(n),L-20,yy,23,M,vis,'right')
   line(g,(L+1,yy),(R0,yy),E,1.,vis*(0.58 if n else 0.))
  for k,(when,name)in enumerate((('2024-05-28','2024.05'),('2024-08-01','08'),('2024-11-01','11'),('2025-01-16','2025.01'))):
   x,_=graph_point(when,0);vis=enter(t,fin+.61+.08*k,.50)*alive
   line(g,(x,BASE),(x,BASE+7),M,1.8,vis);label(g,name,x,BASE+29,22,M,vis)
  src=[graph_point(r['date'],r['minutes'])for r in REC]
  step=[src[0]]
  for e in src[1:]:
   step.extend([(e[0],step[-1][1]),e])
  when=max(last+.40,motion-.30)
  lineprogress=easepos(t,first+.30,max(.9,when-first-.33))
  marker=enter(t,fin+1.02,.55)*alive
  if marker:
   dot(g,*src[0],9,O,marker);ring(g,*src[0],13,O,marker,1.8)
   tag=enter(t,first-.10,.58)*alive
   path(g,[src[0],(src[0][0]+39,src[0][1]+70),(src[0][0]+122,src[0][1]+70)],tag,O,2.1,tag)
   label(g,'45 分钟',src[0][0]+136,src[0][1]+55,32,O,tag,'left')
   label(g,'2024.05.28',src[0][0]+136,src[0][1]+93,24,M,tag,'left')
  if lineprogress:
   path(g,step,lineprogress,C,4.0,alive)
   rail=ArcLength(step);p0=rail.at(lineprogress)
   point(g,*p0,7.5,Y,alive)
   for j,z in enumerate(src):
    if rail.fraction(2*j)<=lineprogress:dot(g,*z,4.15,C,alive)
  reached=enter(t,when-.04,.64)*alive
  if reached:
   px,py=src[-1];point(g,px,py,9.,Y,reached)
   path(g,[(px,py),(px-55,py-85),(px-190,py-85)],reached,Y,2.15,reached)
   label(g,'2.992 分钟',px-204,py-91,38,Y,reached,'right')
   label(g,'2025.01.16',px-204,py-61,23,M,reached,'right')
  revisit=phase(t,motion-.10,motion+.93)
  if revisit:
   label(g,'少用约 42 分钟',1021,314,30,T,alive*revisit)
   path(g,[(1224,282),(1290,282),(1290,576)],revisit,T,2.1,alive*revisit*.76)
 
 # The former target line opens into slots of ONE different, measured example.
 # Maintaining the type lanes distinguishes the record's loss from this forward.
 door=easepos(t,loss+.31,1.47)
 if door:
  from v4_act2 import OP
  xs=len(OP['tokens']);start_line=229;end_line=1413
  cy=mix(715,494,door)
  full=phase(t,how+.21,how+1.02)
  for j,(tag,p) in enumerate(zip(OP['tokens'],OP['probabilities'])):
   x=mix(start_line+(end_line-start_line)*(j+.5)/xs,182+172*j,door)
   s=easepos(t,loss+.39+.047*j,1.32)
   ww=mix((end_line-start_line)/xs-3.,139,s);h=70*s
   if s:
    box(g,x-ww/2,cy-h/2,ww,h,Y,s,inkcol(C,.18),1.65)
    mark(g,tag,x,cy+2,40,t-loss-.55-.05*j,F,op=s)
    side=enter(t,loss+1.16+.068*j,.70)*(1-enter(t,how+.18,1.12))
    if side:line(g,(x-54,cy+61),(x+54,cy+61),Y,2.4,side*.80)
   if full:
    base=cy-82;scale=376;w=24.
    ppp=[(r['p'],C)for r in OP['alternatives'][j]]+[(p,Y)]
    for i,(prob,col) in enumerate(ppp):
     ht=scale*prob*full;rect(g,x-61+i*32,base-ht,w,ht,col,full)
    label(g,(f'{p:.2%}' if p>=.001 else f'{100*p:.4f}%'),x,cy+67,27,Y,full)
  if full:
   mark(g,'P(x₁, x₂, …, xₜ | 前文)',805,137,55,t-how-.16,F,mode='pen',op=full)
   label(g,'The room was quiet.',129,719,28,M,full,'left')
   label(g,'SmolLM2-135M  ·  一次实测',1447,720,25,M,full,'right')
