"""Keep the real issue and its tests attached; show a checked subset as a subset."""
from rig4 import *
from studio_engineering import ROW,diff
from motion import guide
PASSING=('astropy','django','flask','matplotlib','pylint','pytest','requests','scikit-learn','seaborn','sphinx','sympy','xarray')
FOCAL=(173,323)
def _needle(g,points,at,t,col,vis,span=.67):
 u=easepos(t,at,span)
 if not u:return
 path(g,points,u,col,2.1,vis*.81)
 if .01<u<.99:guide(g,points,u,col,vis,3.9,.22)
def intake(g,c,start,end):
 """A historical checkout, one ticket, and the assertions that can be run against it."""
 t=c.t;a=c.at
 when=a('历史仓库');issue=a('问题描述');tests=a('后来验证');package=a('就得到')
 corpus=a('十二个大型');count=a('两千两百九十四');v=a('人工核验');number=a('五百题');full=a('当年出事')
 u=enter(t,start,.56);fade=1-phase(t,end-.48,end-.05)
 if not fade:return
 p=phase(t,corpus-.34,corpus+.67);flash=enter(t,full-.25,.65)
 border=u*fade
 from task_assembly6 import draw
 draw(g,c,ROW,start,corpus,fade)
 tag=enter(t,start+.82,.61)
 ox=mix(304,284,p);oy=mix(359,428,p)
 rv=phase(t,when-.24,package+.91)
 mark(g,'SWE-bench',183,mix(124,153,p),49,t-start-.66,C,'left','pen',.64,border*tag)
 label(g,'同一份任务',183,mix(176,205,p),23,M,border*enter(t,package-.15,.65),'left')
 slot1=(ox,oy-71);slot2=(ox+42,oy+47);slot3=(ox+94,oy+156)
 nodes=((slot1,when,C,'sphinx-doc/sphinx'),(slot2,issue,O,'Issue #5560'),(slot3,tests,T,'PR #8713'))
 for jj,((xx,yy),cue_,col,lab) in enumerate(nodes):
  g0=enter(t,cue_-.17,.51)*fade
  if not g0:continue
  mark(g,lab,xx,yy,36,t-cue_+.17,col,'left',('wave','pen','pen')[jj],.50,g0)
  # Checkpoints join along a centre spine. One visible ticket remains selected.
  path(g,[(xx-31,yy),(xx-66,yy),(xx-66,yy+56),(xx-29,yy+56)],rv,col,1.7,g0*.79)
  point(g,xx-67,yy,4.3,col,g0)
 if not p:return
 # 12 repositories remain visible while the database turns into a field of
 # marks. It is a quantitative picture: every full mark is 10 tasks; the last
 # four are its partial mark. The subset is highlighted together, not a fake rank.
 v_more=phase(t,count-.29,count+.62);morph=phase(t,count-.22,count+.81);long=enter(t,corpus-.22,.58)
 x0,y0=673,259
 titleop=fade*long*(1-v_more)
 for j,nm in enumerate(PASSING):
  x=(685,949,1219)[j%3]+(-31,17,0,11)[j//3];y=265+83*(j//3)
  st0=corpus-.18+j*.080;step=enter(t,st0,.43);co=(C,T,V,O)[j%4]
  # One coherent field, staggered to leave the identifier the reader needs.
  if titleop:point(g,x,y,5.25,co,step*titleop);mark(g,nm,x+21,y,25,t-st0,F,'left',op=titleop,dur=.41)
 if not morph:return
 par=mix(-6.,0.,morph)
 pick=phase(t,number-.17,number+.76);ok=enter(t,v-.21,.72);clip_=fade*long*morph
 for j in range(230):
  i=j%23;row=j//23
  # Intermix sample positions to avoid suggesting that the subset was a prefix.
  sample=((j*41+19)%230)<50;trail=enter(t,count-.25+.020*i+.028*row,.46)
  xx=x0+i*33.4;yy=y0+row*36.8+.8*par
  v0=1-.25*flash*(not sample);co=blend(C,T,pick if sample else 0)
  k=trail*clip_*v0*(1-.70*pick*(not sample))
  last=.4 if j==229 else 1.
  rect(g,xx-11,yy-6,22.5*last,12.5,co,k*.88)
  if ok and sample:
   f=enter(t,v+.020*i+.026*row,.42);line(g,(xx-11,yy+10),(xx+11,yy+10),T,1.5,clip_*ok*f*.71)
 if v_more:
  mark(g,'2,294',x0+1,665,58,t-count+.15,Y,'left','pen',.61,fade*v_more)
  label(g,'每格 10 道题',x0+1,717,24,M,fade*v_more,'left')
 if pick:
  mark(g,'Verified',1273,645,34,t-number+.19,T,'left','wave',.53,fade*pick)
  mark(g,'500',1273,705,46,t-number+.08,T,'left','pen',.53,fade*pick)
  label(g,'题',1408,704,26,T,fade*pick,'left')
 if flash:
  _needle(g,[(611,469),(661,469),(677,507),(720,507)],full-.19,t,O,fade*flash)
  path(g,[(ox-98,oy-108),(ox-112,oy-108),(ox-112,oy+186),(ox-99,oy+186)],flash,Y,2.5,fade*.83)

def checkout(g,c,start,end):
 """Run the actual changed formatting branch and bring the generated RST into view."""
 t=c.t;a=c.at;find=a('定位到');commit=a('改完交一份');not_pretty=a('写得漂不漂亮')
 outcome=a('跑出来的文档');gate=1-phase(t,end-.49,end-.03);p=enter(t,start,.55)*gate
 head=phase(t,find-.20,find+.66);q=phase(t,commit-.17,commit+.55)
 bend=phase(t,outcome-.31,end-.42)
 label(g,'sphinx/ext/napoleon/docstring.py',149,131,33,T,p,'left')
 label(g,'#5560 → #8713',1455,131,30,O,p,'right')
 line(g,(144,173),(1454,173),E,1.55,p*.74)
 # Actual excerpts available from the archived pull request and regression assertion.
 cx=mix(171,135,bend);cy=mix(294,315,bend);w=mix(836,855,bend)
 if q<.40:
  old=p*(1-phase(q,0,.40))
  label(g,'napoleon_use_param = True',cx,cy,40,F,old,'left')
  label(g,'_format_fields(…)',cx,cy+109,36,R,old*head,'left')
  u=enter(t,find-.12,.64)
  path(g,[(cx+342,cy+39),(cx+335,cy+62),(cx+196,cy+84)],u,O,2.25,old)
 if q>.35:
  meet=easepos(t,end-.88,.88-1/60)
  x1,y1=transit((cx,cy),(244,334),meet,27.)
  diff(g,x1,y1,mix(w,685,meet),mix(.99,.90,meet),phase(q,.35,1.),max(p,meet))
  if .01<head<1:swish(g,cx,cx+596,cy+49,t-find+.08,Y,.64)
 bx,by=1051,336;read=enter(t,outcome-.17,.60);visit=enter(t,not_pretty-.14,.55)
 if p:
  h=read if read else .22
  # The new output is the behaviour to test; typography remains on its own pane.
  label(g,'文档输出',bx,270,31,T,p*visit,'left')
  for j,(s1,s2) in enumerate(zip((':Other Parameters:','**param2** …'),(':param param2:',':type param2: …'))):
   yy=by+66*j
   u1=1-phase(t,outcome-.18,outcome+.09);u2=phase(t,outcome+.11,outcome+.57)
   mark(g,s1,bx,yy,31,t-not_pretty+.14,F,'left','wave',.43,p*visit*u1)
   mark(g,s2,bx,yy,33,t-outcome-.04,T,'left','wave',.50,p*u2)
  if read:
   path(g,[(bx,by+154),(bx+238,by+154),(bx+311,by+90)],read,T,2.0,p*read)
   point(g,bx+315,by+86,6.1,T,p*read)
  _needle(g,[(cx+w-4,cy+185),(1012,cy+185),(1087,by+169),(bx+230,by+169)],commit-.09,t,Y,p*visit,1.16)


def enclose(g,c,start,end):
    """Place the same diff into a measured run; the graphic ends in a real test lamp."""
    t=c.t
    docker=c.at('Docker');version=c.at('代码版本');deps=c.at('依赖')
    q=easepos(t,start,.84)
    z=1-phase(t,end-.42,end-.06)
    x,y=transit((244,334),(326,319),q,35.)
    if z:diff(g,x,y,mix(685,588,q),mix(.90,.85,q),1.,z)
    left=x-41;right=mix(967,997,q);head=257;tail=mix(528,574,q)
    conf=enter(t,start+.06,.615)*z
    if conf:
        corners=[(left,head),(right,head),(right,tail),(left,tail),(left,head)]
        route=[(right,head),(right+47,head-43),(right+47,tail-43),(right,tail)]
        path(g,corners,easepos(t,start+.06,.89),C,2.3,conf)
        a=enter(t,docker-.19,.56)
        if a:
            path(g,route,a,T,2.4,z)
            g.poly(corners[:4],C,1.5,0.,True,inkcol(C,.20),.31*a*z)
            label(g,'Docker',left,head-47,38,C,z*a,'left')
            paths=[(right+47,head-43),(right+95,head-43),(1094,403),(1139,403)]
            v=easepos(t,docker-.16,1.0)
            path(g,paths,v,T,2.1,z)
            if .03<v<.995:guide(g,paths,v,T,z,4.5,.23)
        for j,(at,word,cl) in enumerate(((version,'仓库当时的版本',O),(deps,'锁定运行依赖',T))):
            u=enter(t,at-.18,.52)*z
            if u:
                tx=1146;ty=329+133*j
                w=enter(t,at-.24,.65)
                path(g,[(right-11,head+33+108*j),(1099,head+33+108*j),(1112,ty),(tx-13,ty)],w,cl,2.25,u*.88)
                label(g,word,tx,ty,34,cl,u,'left')
                for k in range(4):
                    a=enter(t,at+.10+k*.08,.38)
                    rect(g,tx+k*45,ty+39,31,8.,cl,a*u*.68)
    verdict=phase(t,end-.55,end)
    if verdict:
        ring(g,1058,278,13+43*verdict,C,verdict,2.15)
