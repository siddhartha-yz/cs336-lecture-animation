"""An anonymous answer becomes a point. The first edge is the vote we just followed."""
from rig4 import *
TBL=json.loads((AS/'arena-top5.json').read_text())
LEFT=('734 号擦亮','黄铜路灯。')
RIGHT=('维修机器人驶过','空商场。')
NODES=((184,354),(226,534),(367,281),(370,489),(583,335),(555,551),(799,447),(761,229),(955,334),(904,574),(1112,252),(1156,466),(1334,318),(1309,557),(1442,408))
EDGES=((3,11),(0,1),(0,2),(3,1),(2,1),(4,3),(4,5),(5,3),(5,1),(7,2),(4,7),(7,6),(6,4),(5,6),(5,9),(6,9),(8,6),(7,8),(10,8),(8,9),(11,8),(10,11),(10,12),(11,12),(11,9),(9,13),(11,13),(12,14),(13,14))
def xy(points,p):return tuple(mix(a,b,p)for a,b in points)
def mark_id(g,x,y,r,co,a):
 if a<=.001:return
 dot(g,x,y,r,co,a*.14);ring(g,x,y,r,co,a,2.4)
 line(g,(x-r*.43,y),(x+r*.43,y),co,2.65,a)
def footprints(g,j,x,y,t,alpha):
 if alpha<.01:return
 ctx=g.c;ctx.save();ctx.translate(x,y)
 if j==0:
  # Brass lamp, borrowing only the object in the recorded story. Air around the type is the street.
  p=enter(t,0,.51);emit=phase(t,.32,1.40);o=blend(C,O,.80*emit)
  path(g,[(-13,55),(-13,-17),(-10,-39),(5,-48),(22,-48)],p,C,2.35,alpha*.76)
  pts=[(22,-56),(37,-56),(49,-44),(15,-44)];g.poly(pts,o,2.0,alpha*p,True,inkcol(o,.39))
  g.poly([(21,-42),(45,-42),(67,17),(-2,17)],None,0,alpha*.37*emit,True,inkcol(O,.40))
  for i in range(3):
   m=enter(t,.50+i*.11,.47);dy=i*11
   path(g,[(-62-dy,46+dy),(-25,41+dy),(27+dy,42+dy),(91+dy,65+dy)],m,o,1.15,alpha*.46*m)
 else:
  # Long shopfront perspective, with one travelling wheel rather than a stock robot icon.
  p=enter(t,.04,.63);vp=(47,-48)
  for a in ((-67,44),(-25,67),(61,69),(105,69)):path(g,[vp,a],p,V,1.55,alpha*.50)
  for j0 in range(3):
   v=enter(t,.13+j0*.11,.56);x0=mix(-48,32,j0*.36);y0=mix(37,-19,j0*.36);w=mix(35,12,j0*.38)
   path(g,[(x0,y0),(x0,y0-w),(x0+w,y0-w-7),(x0+w,y0-14)],v,V,2.35,alpha*.56)
  q=p5((t-.46)/2.35);pos=transit((-41,53),(43,-40),q,16);r=mix(11.5,3.5,q)
  point(g,*pos,r,V,alpha*.85*p)
 ctx.restore()

def chart(g,c,at,stop):
 t=c.t;arr=TBL[:4]
 ei=c.at('细横线');stand=c.at('名次就还没站稳');end=1-phase(t,stop-.71,stop-.12)
 pane=enter(t,at-.17,.59)*end
 Y0=315;X1=1070;X2=1434;SS=(1500,1552)
 X=lambda z:mix(X1,X2,(z-SS[0])/(SS[1]-SS[0]))
 if not pane:return
 label(g,'Text Arena',1073,177,44,F,pane,align='left')
 label(g,'2026-11-22',1502,222,23,M,pane,'right')
 for j,r in enumerate(arr):
  y=Y0+j*94;pd=p5((t-at+.04-.10*j)/.69);co=(C,T,V,O)[j];a=pane*pd
  name=r['model_name'].split(' (',1)[0]
  label(g,name,978,y-24,27,F,a,'left')
  label(g,f"{r['rating']:.1f}",1498,y-24,28,co,a,'right')
  line(g,(X1,y),(X2,y),E,1.4,a*.63)
  x=X(r['rating']);range_=p5((t-ei+.07-.067*j)/.60)
  if range_:
   low,hi=(mix(x,X(r[k]),range_)for k in ('rating_lower','rating_upper'));ha=9*range_
   line(g,(low,y),(hi,y),co,3.0,a*.94)
   for xx in (low,hi):line(g,(xx,y-ha),(xx,y+ha),co,1.85,a*.86)
   # Subtle emphasis on the width of the actual confidence interval; no fabricated votes.
   if j==0:
    al=math.exp(-((t-stand+.08)/.58)**2)*a*.60
    path(g,[(low,y+15),(low,y+22),(hi,y+22),(hi,y+15)],1,co,1.7,al)
  point(g,x,y,8.0 if j==0 else 6.7,co,a)
 for x,lab in [(X(1500),'1500'),(X(1525),'1525'),(X(1550),'1550')]:
  line(g,(x,630),(x,640),M,1.2,pane*.56);label(g,lab,x,667,24,M,pane)
 label(g,'Arena 等级分',1113,732,22,M,pane,'left')
 ann=enter(t,c.at('置信区间')-.10,.47)*pane
 if ann:label(g,'置信区间',1448,732,24,T,ann);line(g,(1343,732),(1381,732),T,2.3,ann)

def capture(g,c,stop):
 t=c.t;chat=c.at('真和它聊');story=c.at('短篇故事');show=c.at('Chatbot Arena');hide=c.at('名字盖住');choose=c.at('让读者选')
 vote=c.at('选票落下来');pair=c.at('两个点');many=c.at('这样的线');rank=c.at('估出大家')
 start=chat-.33;story_out=phase(t,vote-.38,vote+.13)
 # previous physical data remain just long enough to locate the limitation.
 back=phase(t,start-.57,start+.38)
 if back<1:endpaper(g,'1-1',-280*back,27*back,1-.08*back,1-back)
 if t<start:return
 intro=phase(t,start,start+.49);words=phase(t,story-.25,story+.76);narr=1-story_out
 pivot=(765,635);sites=((390,464),(1135,464));ink=(C,V)
 if narr>.002:
  fresh=words*narr;py=mix(424,231,words)
  mark(g,'写一个机器人的短篇故事。',773,py,50,t-start,F,mode='wave',dur=.50,op=intro*narr)
  # Unfurl at the moment the narration gives the object to compare.
  path(g,[(507,py+48),(1039,py+48)],intro,T,2.7,intro*narr)
  if t>=show-.10:
   mark(g,'Chatbot Arena',774,136,36,t-show+.1,T,op=enter(t,show-.10,.49)*narr)
  for j,(row,co,(x,_)) in enumerate(zip((LEFT,RIGHT),ink,sites)):
   e=story+.13+.16*j;g0=enter(t,e,.55)*fresh
   mask=phase(t,hide-.22+.06*j,hide+.27+.07*j)
   for i,s in enumerate(row):mark(g,s,x,402+i*60,48,t-e-.10*i,F,mode='wave',dur=.47,op=g0)
   footprints(g,j,x-196,437,t-e,narr*enter(t,e+.23,.55)*.79)
   if mask:
    # Two opaque covers align to the identity of these texts. No unnecessary dummy model logos.
    y=324;ww=mix(147,47,mask)
    rect(g,x-ww/2,y-15,ww,30,co,g0*.32);label(g,('甲','乙')[j],x,y,27,co,g0*phase(mask,.42,1))
   else:
    w0=p5((t-e)/.60);line(g,(x-84,325),(x-84+168*w0,325),co,2.6,g0*.57)
   v=phase(t,choose-.22,choose+.43);origin=(x,513)
   path(g,[origin,(x,554),(pivot[0]+(-46 if j==0 else 46),602),pivot],v,co,2.55,g0*.85)
 if t<vote-.24:return
 # The two measured things survive the exit. Letter glyphs dissolve in their own
 # place, while a gold vote falls onto the physical edge.
 pp=phase(t,vote-.08,pair+.37);startp=enter(t,vote-.25,.47);go=phase(t,many-.24,rank-.18);shift=phase(t,rank-.55,rank+.68)
 focus=phase(t,stop-.96,stop-.06)
 end=1-focus
 # With a clean midpoint the graph can leave the centre without pulling along a small crop of old labels.
 scale=mix(1.,.55,shift);ox=mix(0.,55.,shift);oy=mix(0.,113.,shift)
 pos=lambda x,y:(ox+x*scale,oy+y*scale)
 nodes=[pos(x,y)for x,y in NODES];pA=transit(sites[0],NODES[3],p5(pp),-94);pB=transit(sites[1],NODES[11],p5(pp),69);a=pos(*pA);b=pos(*pB)
 # Single contest is undirected here; direction only enters when we model preferences later.
 arrived=phase(t,vote+.17,pair+.23)
 if arrived:line(g,a,b,Y,3.6*scale,end*arrived)
 for j,(q,co)in enumerate(zip((a,b),ink)):
  x,y=q;dot(g,x,y,mix(14.5,8.4,go)*scale,co,startp*end)
  label(g,('甲','乙')[j],x,y-39*scale,mix(36,21,shift),co,enter(t,vote+.18,.43)*end*(1-go))
 tip=transit(pivot,xy(((pA[0],pB[0]),(pA[1],pB[1])),.56),phase(t,vote-.27,pair+.35),-56)
 if vote-.27<t<pair+.8:
  x,y=pos(*tip);up=enter(t,vote-.27,.31)*(1-phase(t,pair+.37,pair+.83))*end
  ring(g,x,y,15.8*scale,Y,up*.64,2.05);point(g,x,y,7.0*scale,Y,up)
 if t>many-.18:
  for j,(x,y)in enumerate(nodes):
   if j not in (3,11):
    z=enter(t,many-.17+abs(7-j)*.098,.53)*end;dot(g,x,y,scale*(5.8+.9*(j%3)),C if j%4 else V,z*.91)
  for j,(aa,bb) in enumerate(EDGES[1:]):
   z=enter(t,many-.19+.061*j,.50)
   path(g,[nodes[aa],nodes[bb]],z,T if j%3==0 else C,2.2*scale,end*z*.55)
  # Just a handful of neighbouring edges stay live while the sample builds.
  for i in range(9):
   st=many+.18+i*.24;dt=.46+.055*(i%3)
   if st<t<st+dt:
    aa,bb=EDGES[2+(i*3)%20];q=phase(t,st,st+dt)
    if q>0 and q<1:
     x,y=lerp(nodes[aa],nodes[bb],q);dot(g,x,y,4.5*scale,T,end*sin(pi*q)**.40)
 if shift:
  lab=phase(t,rank-.23,rank+.6)
  chart(g,c,rank,stop)
  label(g,'成对胜负',475,649,29,T,shift*end)
  pts=[(763,423),(865,423),(912,393),(957,393)];path(g,pts,lab,O,2.0,shift*end*.69)

def traffic(g,c,st,en,mods):
 """Visible widths are the measured shares; explanations move the eye, not the data."""
 t=c.t;mass=c.at('最粗');price=c.at('便宜');long=c.at('长篇');free=c.at('免费调用')
 p=enter(t,st,.65);exit_=1-phase(t,en-.58,en-.02);master=p*exit_
 if not master:return
 hues=(C,T,Y,V,O,G);q=phase(t,mass-.18,mass+.78)
 cx=mix(384,359,q);cy=mix(422,449,q)
 v=phase(t,long-.30,long+.68)
 label(g,'OpenRouter',78,208,45,F,master,'left')
 label(g,'日词元量',80,260,31,T,master,'left')
 center=(cx,cy)
 path(g,[(91,cy),(cx,cy)],enter(t,st-.05,.70),T,10.4,master*.91)
 for j,row in enumerate(mods):
  co=hues[j];y=140+j*101;bench=1026
  op=enter(t,st+.12+j*.094,.65)*master
  a1=phase(t,mass-.08,mass+.70)*(1-phase(t,price-.43,price+.26))
  ramp=1 if not j else 1-.78*a1
  pts=[(mix(cx,bench,s),mix(cy,y,phase(s,.12,.91)))for s in [i/88 for i in range(89)]]
  wt=row['share_of_shown'];width=129.0*wt;c0=inkcol(co,.77+.18*a1*(j==0))
  path(g,pts,op/master,c0,width,op*ramp)
  if op>.20:
   count=max(1,int(6*wt+1));cycle=2.4+1.7*wt
   for i in range(count):
    v0=((t-st-.28-.094*j)/cycle+(i/count+.12*j))%1.
    if v0<op/master:
     yy=mix(cy,y,phase(v0,.12,.91));cc=co if j else F
     dot(g,mix(cx,bench,v0),yy,2.65+2.6*wt,cc,op*ramp*sin(pi*v0)**.28)
  lab=row['name'].replace(' 1017',' · 1017')
  label(g,lab,1068,y-16,31 if not j else 28,F,op*ramp,'left',410)
  label(g,row['display']+'   ·   '+f'{100*wt:.1f}%',1070,y+22,28 if not j else 25,co,op*ramp,'left')
  if a1 and not j:
   tail=phase(t,mass+.30,mass+1.52)
   if tail<1.:path(g,pts,max(0.,tail),F,2.8,master*a1*.91)
 begin=c.at('模型要是');end=1-phase(t,en-.76,en)
 ybase=582;cap=master*end
 arm=[(price,'便宜',O),(long,'长输出',V),(free,'免费调用',T)]
 for j,(at,lbl,co) in enumerate(arm):
  if t<at-.18:continue
  y=ybase+j*56;v0=enter(t,at-.18,.64);f=cap*v0;active=1-phase(t,at+1.02,at+2.58)*.31
  viz=phase(t,at-.12,at+1.18)
  # Three reading clues use the same intake; the data itself never animates a hypothetical share.
  x=78;rt=[(342,y),(366,y),(389,cy+40+j*13),center]
  label(g,lbl,x,y,28,co,f*.91*active,'left')
  for i in range(4 if j!=1 else 7):
   u=enter(t,at-.05+i*.075,.32);px=220+i*16.1
   rect(g,px,y-5,9.8,10,co,f*u*active)
  if viz:
   if viz<1.0:
    from motion import guide
    guide(g,rt,viz,co,f*active,2.5,.25)
   path(g,rt,viz,co,1.55,f*.59*active)
 label(g,'六项之和为占比的分母',1450,770,24,M,master,'right')
