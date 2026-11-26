"""Hold the solved square back; let behavior, not the shape of a disclaimer, determine the verdict."""
from rig4 import *
from studio_tests import arcboard,AR,PAL,tile
from studio_compute import TRANSFORMS,comparisons
from studio_votes import wedge
def grids(g,c):
 t=c.t;rest=c.rest('第四张网格');read=rest['end'];candidate=c.at('旋转半圈')-.25;budget=c.at('模型也可以')-.20;split=c.at('看同一组')-.20
 if t<budget:
  z=enter(t,0,.71);examples=AR['train'];test=AR['test'][0];zoom=phase(t,read,read+1.65);m=phase(t,candidate-.45,candidate+.55);names=('I','II','III')
  roll=c.at('不妨盯住同一行');proof=c.at('第二张')-.08;again=phase(t,roll-.35,roll+.38)*(1-phase(t,proof-.48,proof+.17))
  first=c.at('第一组输入右上');marks=(first,c.at('另外两组'),c.at('另外两组')+.69)
  # A single full-size input opens this puzzle. It physically settles into row I,
  # leaving space for two more examples; the fourth output is never visible early.
  assemble=c.at('三组二维彩色');in_at=c.at('给你输入');out_at=c.at('也给你输出');kp=phase(t,assemble-.75,assemble+.80)
  if kp<1:
   pres=1-kp;term=enter(t,.18,.90)
   mark(g,'ARC-AGI',1080+80*kp,342,69,t-.18,F,mode='pen',op=pres)
   label(g,'从示例归纳图形规则',1083+80*kp,431,33,T,term*pres)
   if t>c.at('每道题')-.22:
    f=enter(t,c.at('每道题')-.22,.75)*pres
    path(g,[(876,473),(947,473),(973,499),(1152,499)],f,C,2.2,f)
  for i,r in enumerate(examples):
   y=205+i*208;v=enter(t,assemble+.64+(i-1)*.29,.52)if i else 1.
   small=1-.11*zoom;label(g,names[i],111,y,26,M,v*kp)
   xy0,xy1=(mix(506,289,kp) if not i else 289,mix(420,y,kp) if not i else y),(616,y);size=mix(535,160,kp) if not i else 160.
   # Read the specimen by revealing its real pixels, not an invented attention pattern.
   fillin=1. if not i else enter(t,assemble+.54+(i-1)*.33,.68)
   arcboard(g,r['input'],*xy0,size,v*small,open_=fillin)
   r_out=enter(t,out_at-.33+i*.23,.51)
   pathin=enter(t,in_at-.10+i*.13,.48)
   arrow(g,(390,y),(515,y),pathin,T,v*pathin*.86,2.2);arcboard(g,r['output'],*xy1,160,r_out*small)
   n=len(r['input']);dd=size/n;probe=phase(t,marks[i]-.12,marks[i]+.80)
   # Do not show even a single highlighted answer square until the genuine five seconds have elapsed.
   if t>=read:
    a0=(xy0[0]+size/2-dd/2,y-size/2+dd/2);a1=(xy1[0]-size/2+dd/2,y-size/2+dd/2)
    pp=min(1,max(0,(t-marks[i]+.04)/.83));strength=max(0,1-abs(t-(marks[i]+.47))/1.04)
    if strength:
     path(g,[a0,(a0[0]+34,a0[1]-29),(a1[0]-35,a1[1]-29),a1],probe,Y,2.35,strength)
     bx,by=transit(a0,a1,p5(pp),31);dot(g,bx,by,6,Y,strength)
    if probe:
     hh=probe*(.36+.50*strength);box(g,a0[0]-dd/2+1,a0[1]-dd/2+1,dd-2,dd-2,Y,hh,sw=2.2)
     box(g,a1[0]-dd/2+1,a1[1]-dd/2+1,dd-2,dd-2,Y,hh,sw=2.2)
  a=enter(t,c.at('第四组只给输入')-.33,.64);x0,y0=975,318;readable=1-phase(again,.0,.50)
  if readable>.001:
   arcboard(g,test['input'],x0,y0,201,a*readable);label(g,'新输入',x0,168,33,C,a*readable)
   ap=enter(t,c.at('画出每一个像素')-.24,.64);targetx,targety=1281,493;siz=251
   path(g,[(x0+116,y0),(1155,y0),(1208,356)],ap,T,2.4,a*readable)
   if t<read:arcboard(g,test['output'],targetx,targety,siz,ap*readable,open_=0)
   else:
    from arc6 import actual_output
    actual_output(g,t,read,x0,y0,201,targetx,targety,siz,readable)
    if t>read+1.31:check(g,1457,408,13,True,enter(t,read+1.31,.38)*readable)
   if rest['start']<=t<read:
    pp=(t-rest['start'])/(read-rest['start']);line(g,(1110,696),(1440,696),M,1.9);line(g,(1110,696),(1110+330*pp,696),Y,3.65)
   if t>=read:label(g,'逐行左右翻转',targetx,704,31,T,enter(t,c.at('每一行')-.25,.6)*readable)
   # First the spectator solves the puzzle. Then the three actual coloured rows
   # travel between the two grids: the y index stays put, the x index reverses.
   rowbeat=c.at('每一行')-.13;rowend=c.at('如果你的第一反应')-.25
   if rowbeat<t<rowend and readable>.99:
    for i,row in enumerate(test['input']):
     launch=rowbeat+(rowend-rowbeat-1.35)*i/2;time_=t-launch
     if not (-.02<time_<1.45):continue
     q0=p5(clip(time_/1.18));light=sin(pi*clip((time_+.08)/1.50))**.65
     sy=y0+(i-1)*67;dy=targety+(i-1)*(siz/3)
     line(g,(x0-104,sy+34),(x0+104,sy+34),Y,2.5,light)
     line(g,(targetx-siz/2,dy+siz/6),(targetx+siz/2,dy+siz/6),Y,2.5,light)
     for j,col in enumerate(row):
      sx=x0+(j-1)*67;dx=targetx+(1-j)*siz/3
      px,py=transit((sx,sy),(dx,dy),q0,-22-(j-1)*22);side=17+8*sin(pi*q0)
      if .01<q0<.99:tile(g,px-side/2,py-side/2,side,PAL[col],light)
  # Guide the gaze across complete examples before the silent vote; no mark singles
  # out a corner or the candidate transformation.
  st=c.at('这三组输入');en=c.at('给你五秒钟')
  if st-.20<t<en+.65:
   span=(en-st)/3
   for i in range(3):
    go=st+i*span;hp=during(t,go-.15,go+span+.12,.31);y=205+i*208
    if hp:
     path(g,[(174,y-68),(158,y-68),(158,y+68),(174,y+68)],enter(t,go-.15,.42),O,2.2,hp)
     path(g,[(723,y-68),(739,y-68),(739,y+68),(723,y+68)],enter(t,go-.15,.42),O,2.2,hp)
  if again>.001:
   from arc6 import hypothesis
   hypothesis(g,c,phase(again,.51,1.))
  if t>=proof:
   for i,tag in enumerate(('第二张','第三张','新图上')):
    pa=c.at(tag);vv=enter(t,pa-.12,.48);xx=772 if i<2 else 1416;yy=413+208*i if i<2 else 345
    if vv:check(g,xx,yy,10,True,vv*.90)
 elif t<split:
  # In the old film the quantitative record came *before* the tree. Enter
  # that source only after the old record has wholly left. The common material
  # at this new cut is the original, unchanged fourth input.
  bridge=budget+1.60
  if t<bridge:open_search(g,t,budget)
  else:
   from arc6 import branch
   branch(g,c,bridge,split)

 else:
  sample_readout(g,c,t,split)
  from readout6 import out
  out(g,c)
@lru_cache(maxsize=4)
def _puzzle_pose(width):
 c=cue('6-1');old=c.t;sf,gg=prev.surface(width)
 try:
  c.t=c.at('模型也可以')-.20-1/60;stage(gg);grids(gg,c)
 finally:c.t=old
 sf.flush();return sf
def open_search(g,t,budget):
 ctx=g.c;at=t-budget;cx,cy,side=975,318,201
 if at<.61:
  q0=p5(at/.61);x=mix(0,cx-side/2,q0);y=mix(0,cy-side/2,q0)
  sf=_puzzle_pose(ctx.get_target().get_width())
  ctx.save();ctx.rectangle(x,y,mix(1600,side,q0),mix(900,side,q0));ctx.clip()
  ctx.scale(1600/sf.get_width(),1600/sf.get_width());ctx.set_source_surface(sf,0,0);ctx.paint();ctx.restore()
 else:
  q0=p5((at-.61)/.99);xx,yy=transit((cx,cy),(560,425),q0,31)
  zz=mix(side,353,q0);arcboard(g,AR['test'][0]['input'],xx,yy,zz)
  ink=enter(at,.94,.61)
  label(g,'67a3c6ac · 新输入',xx,yy+zz*.53+29,25,M,ink)
  label(g,'候选规则演算',xx+zz*.68,yy-37,33,T,ink,'left')
  label(g,'把猜想拿回三个例子去验',xx+zz*.68,yy+15,25,M,ink,'left')
@lru_cache(maxsize=4)
def _search_pose(width):
 # Freeze the previous shot only at its last open-shutter frame. That real grid
 # is the island in the cut, instead of dissolving two complete graphics together.
 c=cue('6-1');old=c.t;sf,gg=prev.surface(width)
 try:
  c.t=c.at('看同一组')-.20-1/60
  stage(gg);grids(gg,c)
 finally:c.t=old
 sf.flush();return sf
def sample_readout(g,c,t,split):
 a=enter(t,split,.65);xx0,yy0=146,319
 take=c.at('候选采样预算');six=c.at('从六')+.09;more=c.at('一千零二十四');report=c.at('报告的分数');ends=c.at('计量算力')
 iris=phase(t,split,split+.91);move=phase(t,c.at('两种o3')-.20,take+.34)
 typ=enter(t,c.at('一百道半私有题')-.34,.69);o3=enter(t,c.at('两种o3')-.08,.61)
 show=1-phase(t,report-.22,report+.43);chart=enter(t,report-.20,.58);rule=enter(t,take-.17,.61)
 # The geometric situation changes from one worked example to a different,
 # common test set. These hundred small stamps are tasks, not model samples.
 if show>.002:
  target=(mix(778,1157,move),mix(420,404,move));ww=mix(815,410,move);hh=ww*.32
  x0,y0=target[0]-ww/2,target[1]-hh/2
  poly=[(x0-15,y0+6),(x0+ww-18,y0-20),(x0+ww+19,y0+hh-6),(x0+19,y0+hh+20)]
  g.poly(poly,C,1.9,typ*show,True,inkcol(C,.16),typ*show*.75)
  for j in range(5):
   for i in range(20):
    f=enter(t,c.at('一百道半私有题')-.31+.012*(j*7+i),.36)*show
    x=x0+ww*(i+.50)/20+(j-2)*ww*.008;y=y0+hh*(j+.52)/5-(i-9.5)*ww*.0014
    rr=ww/144;col=(C,T)[(j//2+i//3)%2];box(g,x-rr,y-rr,2*rr,2*rr,col,f,inkcol(col,.51),1.1)
  if move<.995:label(g,'同一组 100 道题',target[0],y0-61,40,F,typ*show*(1-move))
  if o3:
   q=phase(t,c.at('两种o3'),take+.62)
   for i,col in enumerate((O,C)):
    h=target[1]+hh*.50+25;ox=target[0]+(-.24 if i==0 else .24)*ww;dx=(1043,1289)[i]
    path(g,[(ox,h),(ox,h+21),(dx,527),(dx,550)],q,col,2.15,show*o3)
  label(g,'o3 预览版 · 同一组 100 题',1135,177,34,F,move*o3*show)
 if rule:
  s=11.45;u=phase(t,more-.09,more+1.04);sixup=enter(t,six-.11,.38)
  n=6+1018*p5(u);ctx=g.c;ctx.save();ctx.translate(xx0+80,yy0+20);ctx.transform(cairo.Matrix(1,-.20,.47,.82,0,0))
  for j in range(32):
   for i in range(32):
    ix=j*32+i
    if ix<6:
     if sixup<.998:rect(g,i*s,j*s,8.1,8.1,E,rule*.38*(1-sixup))
     if sixup:rect(g,i*s,j*s,8.1,8.1,O,sixup)
    else:
     pin=clip(n-ix)
     if pin<.999:rect(g,i*s,j*s,8.1,8.1,C,.145*rule*(1-pin))
     if pin:rect(g,i*s,j*s,8.1,8.1,(C,T,'#349EBA')[(j+i*2)%3],pin)
  ctx.restore()
  label(g,'采样预算',408,153,38,F,rule);label(g,'6',320,690,45,O,sixup);label(g,'→',411,690,39,M,enter(t,more-.23,.46));label(g,'1,024',540,690,45,C,enter(t,more-.05,.57))
 if chart:
  label(g,'o3 预览版 · 同一组 100 题',1135,177,34,F,1-show)
  path(g,[(891,268),(891,647),(1454,647)],chart,M,2)
  for i,(v,co,cap,go)in enumerate(((75.7,O,'6 次','百分之七十五点七'),(87.5,C,'1,024 次','八十七点五'))):
   xx=1043+i*246;q=enter(t,c.at(go)-.08,.57);h=v*3.91
   rect(g,xx-51,647-h*q,102,h*q,co,q);label(g,f'{v:g}%',xx,647-h*q-36,39,co,q);label(g,cap,xx,696,27,M,chart)
  label(g,'ARC-AGI-1 半私有评测 · 2024.12',1111,747,24,M,chart)
 # Let the eye travel from the score back to its cost when the narrator does so.
 po=during(t,c.at('同时读')-.15,min(c.d-.27,ends+1.25),.50)
 if po:
  fr=enter(t,c.at('同时读')-.12,.63);path(g,[(1350,281),(1350,234),(788,234),(746,266),(602,266)],fr,Y,2.8,po*.87)
 if iris<.999:
  ctx=g.c;ctx.save();cx,cy=1085,434;rad=1870*(1-iris)
  ctx.new_path();ctx.arc(cx,cy,max(.01,rad),0,tau);ctx.clip()
  sf=_search_pose(ctx.get_target().get_width());ctx.scale(1600/sf.get_width(),1600/sf.get_width());ctx.set_source_surface(sf,0,0);ctx.paint();ctx.restore()
def foldfilm(g,xx,yy,co,q,a,w=88):
 # A translucent gate in a depth stack carries a whole response, never a single prefix.
 h=w*.66;corn=[(xx-w,yy-h),(xx+w,yy-h-16),(xx+w,yy+h-16),(xx-w,yy+h)]
 g.poly(corn,co,2.25,a,True,inkcol(co,.44),.29*a)
 for k in range(2):
  y=yy-13+k*23;path(g,[(xx-w+6,y+7),(xx+w-5,y-7)],q,co,1.25,.50*a)
def rate_paper(g,c,t,j,unfold,fold,zoom,level,gain=1):
 """A continuous percentage ruler (not 100 trial records). Ten by ten becomes one by one hundred."""
 base=(219.,351.);side=314.;dx=(280.,1001.)[j];dy=295.;color=(C,T)[j]
 ybar=(379,522)[j];xbar=544;bar_span=756;limit=mix(100,35,zoom);unit=bar_span/limit
 nval=(30.2,5.9)[j]*level
 def project(u,v):
  a=(base[0]+315*u+25*v,base[1]-27*u+221*v)
  b=(dx+side*u,dy+side*v)
  return(a[0]+(b[0]-a[0])*unfold,a[1]+(b[1]-a[1])*unfold)
 if gain<.001:return
 if fold<.999:
  o=[project(x,y)for x,y in ((0,0),(1,0),(1,1),(0,1))]
  g.poly(o,color,2.15,gain*(1-fold),True,inkcol(color,.16),gain*.56*(1-fold))
 for i in range(100):
  row,col=divmod(i,10);q=fold;fraction=clip(nval-i);barpos=xbar+i*unit;exposed=gain*(1-zoom)
  if zoom and barpos>1455:continue
  def tile(fraction,colr,opacity):
   if fraction<=0 or opacity<.003:return
   px=.04+.92*fraction;ux=(.04,px,px,.04);vy=(.05,.05,.94,.94)
   if q>=.999:rect(g,barpos+.055*unit,ybar-19.5,.89*unit*fraction,39,colr,opacity);return
   four=[]
   for u0,v0 in zip(ux,vy):
    a0,b0=project((col+u0)/10,(row+v0)/10)
    endx=barpos+unit*(.055+(u0-.04)/.92*.89);endy=ybar+mix(-19.5,19.5,(v0-.05)/.89)
    four.append((mix(a0,endx,q),mix(b0,endy,q)))
   cc=g.c;cc.new_path();cc.move_to(*four[0]);cc.line_to(*four[1]);cc.line_to(*four[2]);cc.line_to(*four[3]);cc.close_path();g.source(colr,opacity);cc.fill()
  tile(1.0,inkcol(color,.29 if row%2 else .34),exposed)
  tile(fraction,inkcol(color,.89),exposed)
 # The many 1% marks settle into a single continuous scale before zooming.
 if zoom:
  rect(g,xbar,ybar-20,nval*unit,40,inkcol(color,.78),gain*zoom)
  line(g,(xbar,ybar-19),(xbar+nval*unit,ybar-19),color,2.45,gain*zoom)
def protocol(g,c,t,st,en):
 a=enter(t,st,.59);use=c.at('只换测试条件');right=c.at('模型和行为判定');pair=c.at('把两套模型')-.16
 unfold=phase(t,pair,en+.35);clear=1-phase(t,pair-.08,pair+.79)
 panelnote(g,'GCG','利用梯度信息的压力测试条件',160,109,t-st,O,clear)
 label(g,'HarmBench',1410,117,38,T,a*clear,'right')
 # Three published labels on three glass measuring slides. They represent different
 # protocols, not successive stages of an attack. A single model stays seated.
 for j,co in ((2,V),(1,O)):
  x=259+j*188;y=337-j*35;z=enter(t,st+.17*j,.58)*clear
  pts=[(x,y),(x+298,y-25),(x+323,y+193),(x+25,y+219)]
  if z:g.poly(pts,co,2.25,z,True,inkcol(co,.50),.57*z)
  for yy in (.25,.50,.75):
   yy0=y+yy*220
   line(g,(x+yy*25+4,yy0),(x+yy*25+292,yy0-24),co,1.6,z*.62)
  label(g,('','Multi','Transfer')[j],x+200,y+237,30,co,z)
 if t>=st:
  rate_paper(g,c,t,0,unfold,0,0,0,a)
  label(g,'标准 GCG',425,614,35,C,a*clear)
  if unfold:rate_paper(g,c,t,1,unfold,0,0,0,unfold)
 rt=enter(t,right-.16,.55);flow=enter(t,use-.20,.68)
 if clear>.001:
  lx,ly=1169,407
  for j in range(3):
   sh=(2-j)*9;o=[(lx+u+sh,ly+v-sh)for u,v in ((-113,-65),(115,-65),(115,68),(-113,68))]
   g.poly(o,T,1.9,a*clear,True,inkcol(T,.35),.78*a*clear)
  label(g,'同一模型',lx,ly,37,F,a*clear)
  for j,col in enumerate((C,O,V)):
   tu=clip((t-use+.12-.42*j)/.98);x=535+j*120;y=322-j*36
   pts=[(x,y),(x,y-37),(909,256),(1022,ly-4)]
   if tu:path(g,pts,tu,col,2.1,a*clear*(1-.52*j/2))
  if rt:
   path(g,[(lx,ly+81),(lx,540),(lx-52,587)],rt,T,2.35,a*clear)
   label(g,'按整份回答判定',lx,635,29,T,a*clear*rt)
 label(g,'更换条件，保留同一判定规程',804,748,29,F,a*flow*clear)
 if unfold:label(g,'同一把百分比标尺',803,744,27,M,unfold)
def incidence(g,c,t,st,limit):
 """Lock one protocol. Read two fractions at full scale, then reveal the 0–35% close-up."""
 pair=c.at('把两套模型')-.16;unfold=phase(t,pair,st+.35);at=c.at('这里数的是');fold=phase(t,at-.12,at+1.13);z=phase(t,at+1.15,limit)
 a=enter(t,st,.57);focus=c.at('蓝色这组');next_=c.at('换成专门');l1=c.u('三十点二',.72);l2=c.u('五点九',.71)
 label(g,'HarmBench · 标准 GCG 条件',184,126,44,F,a,'left')
 label(g,'完整回答中出现指定有害行为的比例',186,187,27,M,a,'left')
 for j,(xx,nm,col,lev,rate)in enumerate(((437,'Llama 2 13B Chat',C,l1,30.2),(1158,'Zephyr 7B + R2D2',T,l2,5.9))):
  rate_paper(g,c,t,j,unfold,fold,z,lev)
  # The two names occupy different histogram rows, without running subtitles
  # or a second axis through either one of them.
  mv=p5(fold);xp=mix(xx,516,mv);yp=mix(249,(379,522)[j],mv)
  if fold<.99:label(g,nm,xp,yp,32,col,a*(1-phase(fold,.025,.26)))
  if fold>.89:label(g,nm,516,(379,522)[j],32,col,phase(fold,.89,1.0),'right')
  picked=(focus,next_)[j];pulse=enter(t,picked-.14,.63)*(1-phase(t,picked+1.10,picked+1.71))
  if pulse and not fold:
   path(g,[(xx-154,611),(xx-166,611),(xx-166,295),(xx-154,295)],pulse,col,3.25,pulse)
  if lev:
   unit=756/mix(100,35,z);barend=544+rate*unit;origin=(xx,671);dest=(barend+15,(379,522)[j])
   if fold<.40:label(g,f'{rate:.1f}%',origin[0],origin[1],44,col,phase(lev,.49,1)*(1-phase(fold,.04,.39)))
   if fold>.92:label(g,f'{rate:.1f}%',dest[0],dest[1]-34*(1-z),37,col,phase(fold,.92,1.0),'left')
 if fold<1:
  cap='同一把百分比标尺' if t<c.at('标准压力条件') else '一小格 = 1 个百分点'
  label(g,cap,803,744,27,M,1-phase(fold,.02,.39))
 if fold>.88:
  hi=mix(100,35,z);unit=756/hi;vis=phase(fold,.88,1.0)
  for n in (0,10,20,30,50,100):
   x=544+n*unit
   if x>1330:continue
   sw=vis if n in (0,10,20,30)else vis*(1-z)
   # Only exterior tick fragments are needed while a solid bar travels through.
   line(g,(x,300),(x,347),M if not n else E,1.55,sw*.65);line(g,(x,576),(x,619),M if not n else E,1.55,sw*.65)
   label(g,f'{n}%',x,661,26,M,sw)
  label(g,'同一判定规程',1014,742,29,M,vis)
def conduct(g,c):
 t=c.t;room=c.rest('拒答陷阱');reveal=room['end'];normal=c.at('看右边另一条路')-.13;standard=c.at('HarmBench')-.11;gc=c.at('GCG')-.08;paper=c.at('在 HarmBench 论文')-.13;q=c.at('这些考题')-.14
 if t<normal:
  from reply6 import branch
  branch(g,c,normal)
  return
 if t<gc:
  a=enter(t,normal,.60);shut=c.u('也照样拒绝',.67);goal=c.u('正常请求挡',.59);redfocus=c.u('只看红色那一列',.72);back=c.u('绿色那一列接回来',.72);method=c.u('HarmBench',.66)
  # Left and right are different populations. We can exactly enact the all-refuse
  # baseline without pretending to have measured a single empirical benchmark rate.
  fade=1-phase(t,gc-.53,gc-.09);safevis=(1-.86*redfocus*(1-back));fg=a*fade
  nshow=6;leftx=421;rightx=1174
  label(g,'危险请求',leftx,221,37,R,fg);label(g,'正常请求',rightx,221,37,T,fg*safevis)
  trail=('整理公开资料','修正错字','摘取目录','换算单位','改写邮件','归纳要点')
  q0=c.at('整理公开资料')
  if t<q0+2.6:
   z=enter(t,q0-.18,.58)*(1-phase(t,q0+1.94,q0+2.60));label(g,'“帮我整理这些公开资料。”',rightx,143,32,F,z*fg)
  for side,(xx,col)in enumerate(((leftx,R),(rightx,T))):
   cvis=fg*(safevis if side else 1);labels=trail if side else ('α','β','γ','δ','ε','ζ')
   for j in range(6):
    xx0=xx+(-1 if j%2==0 else 1)*113;yy=313+(j//2)*104;y2=yy+42
    z=enter(t,normal+.28+j*.20,.43);prog=clip((t-(c.at('也照样拒绝')+.27*j+(0 if side else .23)))/.74)
    if side:
     label(g,labels[j],xx0,yy,25,T,z*cvis)
    else:
     label(g,labels[j],xx0,yy,32,R,z*cvis)
    if prog:
     # A bolt travels towards the stop and is redirected into a return trough.
     pos=transit((xx0-45,y2),(xx0+38,y2),prog,22);point(g,*pos,4.5,O,cvis)
     line(g,(xx0-44,y2),(xx0+37*prog,y2),O,1.7,cvis*.86)
     line(g,(xx0+44,y2-8),(xx0+44,y2+8),O,2.7,cvis)
    if method:dot(g,xx0,yy+23,2.0,col,cvis)
   if shut:
    label(g,('未提供危险帮助','本可答，却被挡住')[side],xx,638,31,col,cvis*shut)
  count=c.at('把所有请求');collapse=c.at('需要测的行为');cv=enter(t,count-.21,1.08);to_method=enter(t,collapse-.10,.92)
  if goal and not method and not cv:label(g,'一律拒答 · 演示',800,722,32,O,goal*fg)
  if cv:
   # The two rates have separate denominators. Six small full-answer marks turn into
   # two very different numerators for the same all-refuse policy.
   early=1-to_method
   for jj,x0 in enumerate((leftx,rightx)):
    ratecolor=R if not jj else T;h=fg*(safevis if jj else 1)
    for ii in range(6):
     step=enter(t,count+.13*ii,.55);src=(x0+(-1 if ii%2==0 else 1)*113,313+(ii//2)*104+41)
     des=(x0-88+ii*35,693)
     xx,yy=transit(src,des,p5(step),40-6*ii);ww=15.7
     if step and early:
      if jj:rect(g,xx-ww/2,yy-ww/2,ww,ww,ratecolor,early*h)
      else:box(g,xx-ww/2,yy-ww/2,ww,ww,ratecolor,early*h,sw=1.75)
   if t>count+.43 and early:
    label(g,'有害帮助  0 / 6',leftx,746,27,R,cv*fg*early)
    label(g,'正常请求误拒  6 / 6',rightx,746,27,T,cv*fg*early)
  if method:
   panelnote(g,'HarmBench','针对指定有害行为检验完整回答',160,105,t-standard,R,fg)
   label(g,'另取无害对照',rightx,163,24,M,fg*safevis*method)
   for j,(xx,col,tag,title)in enumerate(((leftx,R,'行为发生率','行为发生 / 危险请求'),(rightx,T,'误拒率','误拒 / 正常请求'))):
    rr=enter(t,c.at(tag)-.22,.58)
    if rr:
     label(g,title,xx,719,29,col,rr*fg)
     path(g,[(xx-145,750),(xx-145,758),(xx+145,758),(xx+145,750)],rr,col,1.9,fg)
   read=c.at('完整输出');uq=enter(t,read-.24,.56)*(1-phase(t,c.at('行为发生率')+.21,c.at('行为发生率')+.66))
   if uq:
    x0=800;label(g,'整份回答',x0,370,26,M,uq)
    for jj,ss in enumerate((44,69,56,35)):rect(g,x0-39,415+jj*17,ss,5.3,O,uq)
    path(g,[(x0+43,406),(x0+51,406),(x0+51,479),(x0+43,479)],uq,O,2.,uq)
  return
 if t<paper:protocol(g,c,t,gc,paper);return
 resume=c.at('不是下一步')-.09
 if t<resume:incidence(g,c,t,paper,resume);return
 a=enter(t,paper,.62);first=c.u('三十点二',.77);second=c.u('五点九',.77);warn=c.u('直接写成',.85);shadow=c.u('压成了',1.23);hold=1-.49*warn;x0=544;x1=1300;sc=(x1-x0)/35
 # As the last question opens, keep one literal shadow and rotate the camera
 # towards the two unmeasured directions, instead of dimming the whole blackboard.
 pull=phase(t,q-.15,q+.85);zz=a*(1-pull)
 label(g,'HarmBench · 标准 GCG 条件',184,126,44,F,zz,'left')
 label(g,'完整回答中出现指定有害行为的比例',186,187,27,M,zz,'left')
 for n in (0,10,20,30):
  xx=x0+n*sc;line(g,(xx,300),(xx,619),M if not n else E,1.55,.65*zz*hold)
  label(g,str(n)+'%',xx,661,26,M,zz*hold)
 for j,(nm,col,y,value,z)in enumerate((('Llama 2 13B Chat',C,379,30.2,first),('Zephyr 7B + R2D2',T,522,5.9,second))):
  label(g,nm,x0-28,y,32,col,zz,'right')
  width=value*sc*z
  if z:
   rect(g,x0,y-20,width,40,inkcol(col,.78),zz*hold)
   line(g,(x0,y-19),(x0+width,y-19),col,2.5,zz*hold);label(g,f'{value:.1f}%',x0+width+15,y,37,col,zz*hold*z,'left')
 if second:
  state=c.at('这里数的是');prefix=c.at('不是下一步');middle=c.at('两根柱子')
  label(g,'同一判定规程',1014,742,29,M,zz*second*hold*(1-enter(t,middle-.31,.59)))
  if t-c.at('五点九')<1.1:swish(g,x0,x0+sc*5.9,552,t-c.at('五点九')+.15,Y)
  if state-.25<t<middle-.36:
   # A lens encompasses a whole response. No single next-token forecast would
   # give the binary outcome being tabulated on this chart.
   f=enter(t,state-.23,.69);op=f*(1-phase(t,middle-.88,middle-.36))
   lab='按整份输出判定';label(g,lab,808,686,28,O,op)
   for j in range(13):
    xx=1005+j*19;co=O if j<2 else T;cl=enter(t,state-.15+j*.075,.41)
    rect(g,xx,681,14,8 if j%3 else 12,co,cl*op)
   wide=enter(t,prefix-.23,.70)
   if wide:path(g,[(1004,702),(1004,712),(1246,712),(1246,702)],wide,T,1.9,op)
  if t>=middle-.27:
   u=enter(t,middle-.25,.89);l=x0+5.9*sc;r=x0+30.2*sc;yy=600;iv=1-warn
   path(g,[(l,yy-9),(l,yy),(r,yy),(r,yy-9)],u,O,2.7,zz*iv)
   label(g,'相差 24.3 个百分点',(l+r)/2,yy+29,28,O,zz*u*iv)
   contra=c.u('底座也换了',.62)
   if contra:
    label(g,'两套系统',x0-182,654,28,T,zz*contra*iv)
    for xx,yy0 in ((x0-156,379),(x0-156,522)):swish(g,xx-131,xx+102,yy0+32,t-c.at('底座也换了')+.15,T,.74,2.6)
 if warn:
  for j,(ew,yy)in enumerate(((30.2,379),(5.9,522))):
   x=x0+ew*sc;path(g,[(x,yy+31),(x,yy+69),(909,688)],shadow,O,1.8,zz*warn)
  if shadow:line(g,(851,688),(962,688),Y,4.0,shadow*zz);label(g,'只说明这组条件',909,754,30,O,zz*shadow)
 if pull:
  base=(mix(909,730,pull),mix(688,509,pull));sizes=(95,152)
  line(g,(base[0]-sizes[0]*pull,base[1]),(base[0]+sizes[1]*pull,base[1]),Y,5.2,pull)
  point(g,base[0],base[1],10,Y,pull)
  label(g,'已测的安全条件',base[0]+43,base[1]+64,33,O,pull)
  for j,(end,co,term,word,align) in enumerate((((1114,247),T,'真实工作','真实工作','left'),((353,297),C,'训练时','是否见过题','right'))):
   l=c.at(term);z=enter(t,l-.21,.71)
   alpha=pull*z
   if not alpha:continue
   vx,vy=end;route=[base,(mix(base[0],vx,.45),mix(base[1],vy,.61)-14),(vx,vy)]
   path(g,route,z,co,2.75,alpha);ring(g,vx,vy,15,co,alpha,2.25)
   mark(g,word,vx+(27 if not j else -26),vy-18,44,t-l+.16,co,align,op=alpha)
  if t>c.at('偷看过')-.22:
   l=c.at('偷看过');u=enter(t,l-.22,.75)
   if u:path(g,[(518,250),(518,221),(1080,221),(1080,244)],u,M,1.7,pull*.63)
