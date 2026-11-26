"""A benchmark item consists of a fixed checkout, the issue and the evaluator's tests."""
from rig4 import *
from motion import guide
from gates6 import issue_pose


def route_line(g,xy,st,t,col,a,dur=.79):
 p=easepos(t,st,dur)
 if p:
  path(g,xy,p,col,1.8,a*.63)
  if p<.999:guide(g,xy,p,col,a,3.85,.24)


def draw(g,c,row,st,corpus,fade):
 t=c.t;repo=c.at('历史仓库');ticket=c.at('问题描述');test=c.at('后来验证')
 join=c.at('对起来');again=c.at('可以重跑')
 if t>=corpus-.04:return
 out=easepos(t,corpus-.93,.86);op=(1-out)*fade
 if not op:return
 f=easepos(t,join-.15,.92);g0=c.at('就得到')
 lock=enter(t,repo-.17,.54);spot=enter(t,ticket-.14,.54);inspect=enter(t,test-.19,.55)
 z=easepos(t,st,1.32);first=c.at('后来验证')-.17
 ident=(1066,438);join_x=1097;move=68*out
 # Same reported issue, first readable and later collected into the matched case.
 px,py,pw,angle=issue_pose(1,1.)
 x,y=transit((px,py),ident,z,-22.)
 shrink=easepos(t,first-.46,.69)
 x=mix(x,mix(1072,1111,f),shrink)+move
 y=mix(y,mix(418,417,f),shrink)-23*out
 w=mix(mix(pw,703,z),mix(427,407,f),shrink);theta=mix(mix(angle,.019,z),0.,.51*f)
 photo(g,AS/'sphinx-issue.png',x,y,w,tilt=theta,op=op)
 if spot:
  h=w*774/1294
  line(g,(x-w*.51,y-h*.47),(x-w*.51,y-h*.47+h*.55*spot),O,2.65,op*spot)
 # One genuine checkout before the bug fix. The issue remains legible while
 # the recorded commit is put on a separate layer above it.
 if lock:
  x=mix(1041,join_x,f)+move;y=mix(169,214,f)-33*out;ww=mix(488,420,f)
  cx=x-ww/2+27;co=C
  route=[(662,293),(693,293),(711,y),(cx-12,y)]
  route_line(g,route,repo-.10,t,co,op*lock)
  path(g,[(x-ww/2,y-25),(x+ww/2,y-25),(x+ww/2,y+22),(x-ww/2,y+22)],lock,co,2.29,op*lock)
  rect(g,x-ww/2,y-24,ww,48,inkcol(co,.22),op*lock)
  pts=[(cx,y+10),(cx,y-12),(cx+24,y-12),(cx+33,y-6),(cx+53,y-6),(cx+53,y+10)]
  g.poly(pts,co,2.1,op*lock,True,inkcol(co,.34))
  mark(g,row['base_commit'][:7],cx+81,y,33,t-repo+.13,F,'left','pen',.52,op*lock)
  label(g,'历史版本',x+ww/2-18,y,26,co,op*lock,'right')
 # A few literal lines from the evaluator, not the repair handed to the model.
 if inspect:
  bx=mix(1039,join_x,f)+move;by=mix(644,612,f)-49*out;ww=mix(550,449,f)
  a=op*inspect;co=T;xx=bx-ww/2+19
  panel=[(xx-24,by-64),(xx-24,by+76),(xx+8,by+76)]
  path(g,panel,inspect,co,2.35,a)
  rect(g,xx-14,by-62,ww,129,inkcol(co,.105),a)
  mark(g,'验收测试',xx,by-39,27,t-test+.10,co,'left','wave',.48,a)
  lines=[':param param2:',':type param2: …','self.assertEqual(expected, actual)']
  for i,s in enumerate(lines):
   p=easepos(t,test+.02+.15*i,.54);size=min(25,25*max(1,ww-39)/max(1,g.measure(s,25,font=SERIF)))
   mark(g,s,xx,by-6+30*i,size,t-test-.12*i,co if i==2 else F,'left','wave',.47,a*p)
  xy=[(670,520),(725,520),(765,by),(xx-25,by)]
  route_line(g,xy,test-.15,t,co,a)
 if f:
  rx=1491+move;yy=417-31*out
  ar=[(1320+move,216-31*out),(rx,216-31*out),(rx,612-47*out),(1320+move,612-47*out)]
  path(g,ar,enter(t,join-.10,.81),T,2.2,op*f*.79)
  ready=enter(t,g0-.14,.54)
  if ready:mark(g,'sphinx-8713',1341+move,yy+27,27,t-g0+.1,F,'left','wave',.49,op*ready)
  if t>=again-.11:
   lap=easepos(t,again-.12,1.26)
   p=[(rx,yy),(rx,696-54*out),(849+move,696-54*out),(773+move,626-48*out)]
   route_line(g,p,again-.12,t,O,op*ready,1.12)
   if .01<lap<.999:guide(g,p,lap,Y,op*ready,4.9,.20)
   if lap>.76:
    label(g,'可重跑',780+move,715-54*out,25,O,phase(lap,.76,.999)*op*ready)
