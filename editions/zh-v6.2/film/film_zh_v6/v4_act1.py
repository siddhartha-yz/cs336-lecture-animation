from rig4 import *
import re
A=sorted(json.loads((AS/'cost-points.json').read_text()),key=lambda x:x['cost'])
FR=[];max_=float('-inf')
for v in A:
 if v['index']>max_:FR.append(v);max_=v['index']
MODS=json.loads((AS/'openrouter-top6.json').read_text());CO=json.loads((AS/'four-axes.json').read_text())
def cost(g,c):
 t=c.t;start=c.at('把每个模型')+.29
 from coststage6 import set_cost,exchange,constraint
 # Both the marks and their values live in this chart coordinate system while
 # it opens. Drawing the guide at the final x over a still-compressed cloud
 # would point into empty space and silently misprice the highlighted model.
 xl,yr,xr,yt=223,660,1388,157
 unfold=.40+.60*phase(t,start+.12,c.at('坐标图')+.22)
 X=lambda v:xl+unfold*(xr-xl)*(log(v/.1)/log(400));Yf=lambda v:yr-v*(yr-yt)/70
 h=enter(t,start,.64);path(g,[(xl,yt-10),(xl,yr),(xl+(xr-xl)*unfold,yr)],h,M,2.3)
 for p in (0,20,40,60):
  y=Yf(p);line(g,(xl-8,y),(xl,y),M,2,h);label(g,str(p),xl-22,y,25,M,h,'right')
 for v in (.1,1,10):
  x=X(v);line(g,(x,yr),(x,yr+9),M,2,h);label(g,f'${v:g}',x,yr+34,26,M,h)
 label(g,'智能指数',xl-7,103,34,F,h,'left');label(g,'每题美元 · 对数刻度',xr,yr+67,29,M,h,'right')
 set_cost(g,c,A,FR,X,Yf)
 if t<start:return
 # The logarithmic ruler has equal geometrical spans for unequal dollar increments.
 ten=c.at('横轴按十倍');small=c.at('几毛钱');big=c.at('好几美元');both=c.at('最便宜');pick=c.at('挑这个点')
 rail=enter(t,ten-.08,.40)*(1-phase(t,both+1.73,both+2.18))
 if rail:
  transit_u=phase(t,small+.30,big+.28);xp=mix(X(.1),X(1),transit_u);ww=X(1)-X(.1)
  y=yr-50;co=O;path(g,[(xp,y+12),(xp,y),(xp+ww,y),(xp+ww,y+12)],enter(t,ten-.08,.65),co,2.55,rail)
  if t>small-.43:
   # The ratio is always ten; only the two *named* endpoints carry absolute dollar differences.
   lab='×10' if .04<transit_u<.96 else '+$9.00' if transit_u>=.96 else '+$0.90'
   label(g,lab,xp+ww/2,y-26,26,O,rail);dot(g,xp,y,3.6,O,rail);dot(g,xp+ww,y,3.6,O,rail)
 peel=c.u('依次拿走',1.74);edge=c.u('帕累托前沿',1.04);wall=c.u('一美元的线',.50);focus=c.u('Terra',.48)
 bad=next(r for r in A if r['slug']=='grok-4-7');good=next(r for r in A if r['slug']=='gpt-6-1-terra')
 cut=c.at('依次拿走')
 constraint(g,c,FR[-1],X,Yf)
 if t<pick:
  # First read the axes as coordinates, not a column of disembodied dots.
  ref=FR[-1];xx,yy=X(ref['cost']),Yf(ref['index'])
  for t1,p1,p2,col in ((c.at('指数越高'),(xl,yy),(xx,yy),T),(c.at('越往右'),(xx,yr),(xx,yy),O)):
   v=during(t,t1-.09,t1+2.11,.33)
   if v:path(g,[p1,p2],enter(t,t1-.09,.66),col,1.9,v*.76);ring(g,xx,yy,13,col,v,1.85)
  # Read a real paired coordinate. The second unit is per completed task,
  # not per million tokens; the numerator and denominator are shown together.
  first=c.at('智能指数');vert=c.at('指数越高');horiz=c.at('越往右');pay=c.at('每百万词元');stop=c.at('横轴按十倍')
  if first-.22<t<stop-.1:
   v=during(t,vert-.29,horiz+1.61,.33);vv=during(t,horiz-.11,pay+.69,.36)
   if v:label(g,f"{ref['index']:.1f}",xx-44,yy-53,35,T,v,'right')
   if vv:label(g,f"${ref['cost']:.2f}",xx-29,yy+64,35,O,vv,'right')
   un=during(t,pay-.20,stop-.10,.37)
   if un:
    q=enter(t,pay-.12,.54);w=enter(t,pay+.32,.53)
    label(g,'总推理开销',1205,494,30,O,un)
    path(g,[(1098,533),(1311,533)],q,O,2.0,un)
    label(g,'完成的任务数',1205,570,28,F,w*un)

 if pick-.12<t<cut+.50:
  x,y=X(bad['cost']),Yf(bad['index']);xe,ye=X(good['cost']),Yf(good['index'])
  op=1-phase(t,cut-.10,cut+.50);init=enter(t,pick-.12,.57)
  ring(g,x,y,13,R,init*op,2.4)
  a0=c.at('往左上方看');a1=c.at('比它便宜');a2=c.at('得分还高');left=phase(t,a0-.04,a1+.33);up=phase(t,a1+.35,a2+.48)
  path(g,[(x,y),(xe,y)],left,T,2.9,op)
  if left and not up:point(g,mix(x,xe,left),y,5.3,T,op)
  if up:path(g,[(xe,y),(xe,ye)],up,T,2.9,op);point(g,xe,mix(y,ye,up),5.8,T,op)
  if up>.9:ring(g,xe,ye,14,T,op,2.05)
  read=enter(t,a1-.15,.47);label(g,'$7.77 → $0.96',.5*(x+xe),y+33,25,T,read*op)
  read=enter(t,a2-.09,.48);label(g,'35.5 → 51.3',xe-24,(ye+y)/2,25,T,read*op,'right')
  cross=c.u('拿走',.48)
  if cross:
   path(g,[(x-11,y-11),(x+11,y+11)],cross,R,2.5,op);path(g,[(x+11,y-11),(x-11,y+11)],cross,R,2.5,op)
 if peel:
  knots=[(X(FR[0]['cost']),Yf(FR[0]['index']))]
  for r in FR[1:]:
   x,y=X(r['cost']),Yf(r['index']);knots+= [(x,knots[-1][1]),(x,y)]
  pos=max(peel*.78,edge);path(g,knots,pos,Y,3.7,1)
 if edge and wall<.98:
  panelnote(g,'帕累托前沿','两项均不差，至少一项更好的对手不存在',725,477,t-c.at('帕累托前沿')+.08,Y,1-wall)
  exchange(g,c,FR,X,Yf)
 if wall:
  x=X(1);rect(g,xl+1,yt+7,x-xl-1,yr-yt-7,inkcol(T,.21),.55*wall)
  g.line(x,yt,x,yr,R,2.2,wall,[7,7]);label(g,'$1 预算',x+16,yt+10,30,R,wall,'left')
  feasible=sorted([r for r in A if r['cost']<=1],key=lambda r:r['index'])
  sweep=c.at('沿着预算内');f=clip((t-sweep+.12)/(c.at('Terra')-sweep+.04))
  if 0<f<1:
   low=mix(Yf(feasible[0]['index']),Yf(good['index']),p5(f));line(g,(xl+2,low),(x,low),T,1.8,.8)
   for r in feasible:
    ptr=Yf(r['index']);touch=clip(1-abs(ptr-low)/19)
    if touch:ring(g,X(r['cost']),ptr,11,T,touch,1.8)
  xe,ye=X(good['cost']),Yf(good['index']);ring(g,xe,ye,12+6*focus,Y,focus,2.3)
  if focus:
   path(g,[(xe-10,ye-8),(xe-60,ye-53),(xe-236,ye-53)],focus,Y,2,focus);label(g,'GPT-6.1 Terra',xe-65,ye-80,33,Y,focus,'right');label(g,'51.3  ·  $0.96 / 题',xe-64,ye-29,24,M,focus,'right')
  if t>c.at('全图最高点')-.1:
   last=FR[-1];uv=during(t,c.at('全图最高点')-.1,c.at('付得起')+.42,.36)
   if uv:ring(g,X(last['cost']),Yf(last['index']),13,M,uv*.75,1.7);label(g,'预算外',X(last['cost'])-35,Yf(last['index'])+35,23,M,uv,'right')
def usage(g,c,st,en):
 from arena6 import traffic
 traffic(g,c,st,en,MODS)
def axis(g,c,st):
 from rank_rail6 import draw
 draw(g,c,st,CO)
def pools(g,c):
 t=c.t;rs=c.at('OpenRouter')-.19;zs=c.at('为了不让比较对象')-.13
 if t<rs:
  from arena6 import capture
  capture(g,c,rs)
 elif t<zs:usage(g,c,rs,zs)
 else:axis(g,c,zs)
def attrib(g,c):
 t=c.t;ns=c.at('NanoGPT')-.19
 lab=c.at('回到模型')-.26
 if t<lab:
  seed=c.at('那个数字背后')-.08;fork=c.at('科学裂缝')-.33;left=c.at('算法方法');right=c.at('黑盒系统');twice=c.at('两行分数')
  family=CO[0];sx=289;sy=mix(615,242,family['pct'][0]/100)
  # All four axes stay put while one datum detaches; let the data leave by the
  # time we introduce the two illustrative experiments (no fictitious Luna scores).
  lift=phase(t,.58,seed+.45);clear=phase(t,seed-.85,seed+.49);u=phase(t,seed-.31,fork+.13)
  if clear<1:endpaper(g,'1-2',0,0,1,1-clear)
  xx,yy=transit((sx,sy),(799,355),p5(u),-63)
  if lift:point(g,xx,yy,9.7+6*lift,C,1-phase(t,fork+.09,fork+.74))
  lens=enter(t,seed-.14,.87)*(1-phase(t,fork+.06,fork+.90))
  if lens:
   rad=16+136*u
   arc(g,xx,yy,rad,-.34*pi,-.34*pi+tau*.73*lens,T,2.7,lens)
   arc(g,xx,yy,rad+.8,.57*pi,.57*pi+pi*.47*lens,V,2.0,lens)
   # The shared reading is one dot. Two visible planes separate behind it as
   # the reason for inspecting it emerges. Draw the faces, not another box label.
   scale=easepos(t,seed-.30,max(.85,fork-seed+.63))
   for j,co in enumerate((C,V)):
    d=(-1 if not j else 1);zz=phase(t,seed+.12+.19*j,fork+.36)
    if not zz:continue
    ww=mix(36,278,scale);hh=mix(31,157,scale);orient=(.12+.21*u)*d
    x1=xx+ww*.64*d;y1=yy+9+22*sin(pi*u)*d
    corners=[(x1-ww*.5,y1-hh*.5-orient*ww*.19), (x1+ww*.5,y1-hh*.5+orient*ww*.37),
             (x1+ww*.5,y1+hh*.5+orient*ww*.37),(x1-ww*.5,y1+hh*.5-orient*ww*.19)]
    g.poly(corners,co,2.25,lens*zz*.79,True,inkcol(co,.26),lens*zz*.77)
    for k in range(6):
     seed0=(xx,yy);dest=(mix(corners[0][0],corners[1][0],(k+.5)/6), y1+4)
     v=phase(t,seed-.12+.081*k+.12*j,fork+.29)
     if v:
      dx,dy=transit(seed0,dest,v,34+5*k)
      rect(g,dx-3,dy-5,6.,10.,co,lens*zz*.91)
   if u:point(g,xx,yy,9.7+6*lift,C,lens)
  if 0<u<.94:
   offset=mix(24,-32,p5(u));weight=clear*(1-phase(u,.22,.56))
   label(g,f"{family['index']:.1f}",xx+19+7*u,yy+offset,30,C,weight,'left')
  if t>=fork-.15:
   s0=enter(t,fork-.15,1.08);alpha=1-phase(t,lab-.64,lab)
   label(g,'两组实验 · 示意',801,167,29,M,s0*alpha)
   for j,(tag,col,start,x)in enumerate((('方法',C,left,467),('系统',V,right,1133))):
    b=enter(t,fork-.06+j*.19,.88);pts=[(799,355),(799,384),(x,458)]
    path(g,pts,b,col,2.3,alpha*.85)
    if b:point(g,x,458,7.6,col,alpha*b)
    vi=enter(t,start-.12,.47)
    if vi:label(g,tag,x,357,50,col,vi*alpha)
    bars=enter(t,twice-.18+j*.10,.67)
    if bars:
     # Equal deltas; there are no invented absolute test scores on the two rulers.
     for d in range(3):
      xoff=x+(d-1)*79;line(g,(xoff,550-5*(d!=1)),(xoff,576+5*(d!=1)),col,2.1,bars*alpha)
     path(g,[(x-79,563),(x+79,563)],bars,col,3.45,alpha)
     label(g,'＋2 分',x,654,42,Y,bars*alpha)
     compare=c.at('只差两分');di=c.at('意思完全不同');r=easepos(t,compare-.11,.72)
     if r:
      for k in range(2):
       v=enter(t,compare-.09+.25*k,.41);pos=x-79+79*k
       line(g,(pos+4,598),(mix(pos+4,pos+75,v),598),Y,2.5,alpha*v)
     # Identical measured deltas; the paths back to a possible cause differ.
     h=easepos(t,di-.17+.11*j,.83)
     if h:
      for k in range(3):
       cx=x+(k-1)*71;cy=467+31*math.cos(pi*(k-1)*.5)
       p=easepos(t,di-.18+.11*j+.11*k,.67);co=(col if j else C) if k!=1 else O
       if j:co=(V,T,O)[k]
       pos=transit((x,458),(cx,cy),p,(k-1)*15)
       if p:
        path(g,[(x,458),pos],p,co,1.8,alpha*h*.61)
        dot(g,*pos,6.4,co,alpha*h)
   if t>lab-.50:shade(g,phase(t,lab-.50,lab))
 elif t<ns:
  from studio5 import two_benches,score_to_token
  two_benches(g,c,lab,ns);score_to_token(g,t,ns)
 else:
  finish=c.at('全场比拼的')-.14
  if t<finish:
   from speed_bench6 import draw as bench
   bench(g,c,ns)
   if t<ns+.74:
    from studio5 import score_to_token
    shade(g,1-enter(t,ns,.58));score_to_token(g,t,ns)
  else:
   from speed6 import latest
   latest(g,c,finish)
@lru_cache(maxsize=2)
def _speed_finish(w):
 sf,g=prev.surface(w)
 from shoot4 import drawclean
 c=cue('1-3');drawclean(g,'1-3',c.at('全场比拼的')-.14-1/60)
 sf.flush();return sf
