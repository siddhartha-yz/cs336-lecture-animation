"""Give the null condition a thing to move: ordering metadata already in an unseen source."""
from rig4 import *
from motion import guide
def cause(g,c,tail,gx):
 t=c.t;at=c.at;chron=at('按年代')-.20;level=at('难度')-.16;doc=at('同一篇文章')-.11;easy=at('容易预测');solid=at('不能替我们证明')
 if t<chron:return
 z0=phase(t,chron,chron+.62);z1=phase(t,level,level+.51);z2=phase(t,doc,doc+.64)
 u=1-phase(t,solid+.52,min(c.d-.22,solid+2.09))
 lift=enter(t,easy-.15,.57)
 # The same four plates are sorted by three different ordinary reasons. Their
 # content stays attached; black receives the old lettering before it changes.
 x0=359;space=291;base=235
 inks=(T,Y,V,C)
 positions=[]
 for j,co in enumerate(inks):
  p=enter(t,chron+.10*j,.49);phase_=max(z1,z2)
  y=base+mix(58*(j%2),31*(3-j),z0)+44*sin(pi*z1+j*.39)*z1*(1-z2)
  y=mix(y,268,z2);x=x0+j*space
  x+=47*sin(pi*z1)*(-1 if j%2 else 1)
  w=mix(131,171,z0);h=mix(46,53,z2);alpha=u*p
  positions.append((x,y))
  if not p:continue
  box(g,x-w/2,y-h/2,w,h,co,alpha,inkcol(co,.35+.18*z2),2.0)
  for k in range(5):
   wid=(11.5+((j*17+k*13)%22))*.90;x1=x-w*.33+k*24
   if x1+wid<x+w*.45:line(g,(x1,y),(x1+wid,y),co,2.05,alpha*.78)
  s=1-phase(t,level-.17,level+.18);tot=phase(t,level+.20,level+.61)*(1-phase(t,doc-.29,doc-.06))
  d=phase(t,doc+.08,doc+.51)
  label(g,('最早','早','晚','最晚')[j],x,y+61,25,co,alpha*s)
  label(g,('基础','入门','进阶','较难')[j],x,y+61,25,co,alpha*tot)
  label(g,('第 1 段','第 2 段','第 3 段','第 4 段')[j],x,y+62,25,co,alpha*d)
 if lift:
  route=[(x,y-54)for x,y in positions]
  k=phase(t,easy-.13,solid-.20);path(g,route,k,O,2.6,u*.88)
  if .01<k<.995:guide(g,route,k,O,u,3.8,.26)
  label(g,'顺序本身带信息',844,140,34,O,u*lift)
 uncover=c.u('即使闪在',.72)
 if uncover:
  a=phase(t,solid-.36,solid+.28)
  # Do not call the gold observation a past event. Show the condition that can
  # push any never-seen document toward an ordinary predictable ordering.
  ring(g,gx,530,20+7.2*a,O,uncover*(1-.58*a),2.75)

def leave_case(g,c):
 # The clinical record lifts off the table as one rigid piece. A split
 # viewport through the middle of a word would look like corrupted text.
 t=c.t
 if t>=1.08:return
 from v4_act7 import miniature_record
 x0,y0=1060.,371.;theta=.017
 if t<.075:
  endpaper(g,'7-1')
  return
 q=easepos(t,.08,.96)
 hold=1-phase(t,.08,.60)
 if hold:
  ctx=g.c;ctx.save();ctx.rectangle(-2,-2,1604,904)
  for i,(x,y) in enumerate(((-303,-164),(303,-164),(303,164),(-303,164))):
   x,y=x0+x*cos(theta)-y*sin(theta),y0+x*sin(theta)+y*cos(theta)
   (ctx.move_to if not i else ctx.line_to)(x,y)
  ctx.close_path();ctx.set_fill_rule(cairo.FILL_RULE_EVEN_ODD);ctx.clip()
  endpaper(g,'7-1',0,0,1.,hold)
  ctx.restore()
 ctx=g.c;ctx.save()
 x,y=transit((x0,y0),(1470,114),q,18)
 ctx.translate(x,y);s=mix(1,.53,q);ctx.scale(s,s)
 miniature_record(g,0,0,mix(theta,.18,q),1-phase(t,.67,1.08),t)
 ctx.restore()

def publiccase(g,c,stop):
 from v4_act7 import bundled,PALS
 t=c.t;a=c.at;public=a('挂上互联网');permit=a('混进训练语料');mark0=a('模型考得高')
 infer=a('当场解出来');memory=a('背过原题');black=a('不公开训练集');seq=a('题目原来的排列')
 leave_case(g,c)
 h=enter(t,.52,.68);close=1-phase(t,stop-.53,stop-.022)
 p=phase(t,permit-.20,mark0+.96);peek=phase(t,mark0-.18,mark0+.58)*(1-phase(t,black-.44,black+.13))
 seal=phase(t,black-.17,black+.57)*(1-phase(t,seq-.10,seq+.51))
 slide=phase(t,seq-.46,seq+.61)
 if p<1 or close:
  base=enter(t,public-.30,.71);tank=h*close
  for i,col in enumerate(PALS):
   q=enter(t,.29+.12*i,.51);x=mix(468,445,slide);y=mix(306+i*100,231+i*112,slide)
   if q:
    bundled(g,x,y,i,q*tank,small=1.13)
    # Possible route for the four public pieces, with no claim that any was seen.
    u=phase(t,permit-.15+.175*i,permit+1.06+.19*i)
    if u and t<black+.3:
     route=[(x+227,y),(735,y),(960,158+i*137),(1043,262+i*76)]
     op=.69*h*close*(1-phase(t,black-.18,black+.27))
     path(g,route,u,col,2.0,op)
     if u<1:guide(g,route,u,col,op,3.3,.32)
  if base:label(g,'公开试题',231,152,33,C,tank*base,'left')
  for j in range(9):
   q=enter(t,permit-.27+j*.040,.46)
   if not q:continue
   y=243+j*29;x=1036+23*sin(.55*j);lens=seal
   rt=1.-phase(t,seq-.13,seq+.27);co=T if j%3 else V
   for i in range(13):
    wg=10+((i*29+j*13)%12);x0=x+i*24
    rect(g,x0,y,wg,11,co,q*tank*rt*(.17+.36*(1-lens)))
  if not p:label(g,'训练材料',1053,182,30,M,tank*base,'left')
 if peek>.001:
  vx=1255;vy=634;a1=enter(t,infer-.19,.62);a2=enter(t,memory-.18,.62)
  label(g,'高分',vx,vy+43,33,Y,peek)
  for j,(u,col,text_) in enumerate(((a1,C,'现场解题'),(a2,V,'见过原题'))):
   x=835+j*223;ys=554
   label(g,text_,x,ys,28,col,u*peek)
   line(g,(x,ys+24),(x+max(0.,u*(vx-x)),vy),col,2.0,u*peek)
 if seal:
  xx=1213;yy=478;outline=[(xx-109,yy-183),(xx-109,yy+35),(xx+109,yy+35),(xx+109,yy-183)]
  path(g,outline,seal,T,2.1,.93*seal*close);label(g,'训练语料不可见',xx,yy+80,30,T,seal*close)
 if slide:
  for j,co in enumerate(PALS):
   xx=912+j*142;yy=526;u=phase(t,seq-.27+j*.068,seq+.39+j*.063)
   if u:
    rect(g,xx-24,yy-17,48,33,co,u*close*.43);label(g,'ABCD'[j],xx,yy,29,F,u*close)
  path(g,[(854,591),(1378,591)],slide,Y,2.08,slide*close)
