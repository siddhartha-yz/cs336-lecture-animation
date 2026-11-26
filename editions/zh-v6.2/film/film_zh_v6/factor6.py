"""Join the three inputs into the existing fitted curve; retain both raw responses."""
from rig4 import *
from motion6 import ArcLength


def probe(c):
    """One state for cursor, axis reading and pie; it stays on the plotted domain."""
    t=c.t;a=c.at
    start=a('偏长的这一侧');sweep=a('只动长度差');sector=a('小扇面')
    zero=a('拨回零')
    if t<sweep+.17:return mix(.16,.78,easepos(t,start-.17,max(.59,sweep+.17-(start-.17))))
    if t<zero-.30:return mix(.78,-.55,easepos(t,sweep+.17,max(.63,sector+.43-(sweep+.17))))
    return mix(-.55,0.,easepos(t,zero-.30,.88))


def projected_reading(g,c,point_,left,tile_,opacity):
    """Attach the probability to its measured ordinate, not to a new headline."""
    t=c.t;intro=c.at('统计模型');at=c.at('多大机会');zero=c.at('拨回零')
    x,y=point_;cx,cy=tile_
    for j,(word,tail) in enumerate(((intro,zero-.40),(at,c.at('每道题都')-.18))):
        u=during(t,word-.18,tail,.37)*opacity
        if u<.002:continue
        f=easepos(t,word-.17,.76)
        if j:
            path(g,[(x,y),(left+1,y)],f,Y,2.2,u*.80)
            point(g,*(mix(x,left,f),y),4.65,Y,u)
        else:
            bend=94 if x<1040 else 51
            coords=[(x+6,y-10),(x+18,y-bend),(1277,234),(cx-21,cy+38)]
            path(g,coords,f,T,2.20,u*.81)
            if f<.99:point(g,*ArcLength(coords).at(f),5.1,T,u)
        ring(g,cx,cy,48+4*sin(pi*f),Y,u*f,2.3)
def fit_arc(g,c,fit,op):
 t=c.t;a=c.at
 ramp=easepos(t,fit-.32,.93);settled=phase(t,fit+.74,fit+1.16)
 active=ramp*(1-settled)*op
 if active:
  x1,y1=(933,470);el=(879,1099,1319);ys=(419,454,473)
  for i,(ox,oy,co) in enumerate(zip(el,ys,(Y,T,V))):
   coords=[(ox,oy),(ox,oy+32),(x1-9+i*9,507),(x1,y1)]
   u=easepos(t,fit-.31+.08*i,.70)
   path(g,coords,u,co,1.7,active*.70)
   if .01<u<.995:point(g,*ArcLength(coords).at(u),5.1,co,active)
  ring(g,x1,y1,7+13*ramp,T,active*.76,2.)
 read=a('左边的原文');ins=a('统计模型');dur=ins-read
 if read-.16<t<ins+.62:
  ux=enter(t,read-.16,.59);p=easepos(t,read-.08,max(.49,dur*.57));o=during(t,read-.17,ins+.60,.42)
  # The left words remain locked while right-hand data moves. Select just its
  # two paper edges; the text itself is neither scanned away nor brightened.
  for z,(xx,yy,co) in enumerate(((119,252,C),(171,557,V))):
   if o:
    b=[(xx-4,yy-18),(xx-19,yy-18),(xx-19,yy+82),(xx-4,yy+82)]
    u=enter(t,read-.19+z*.14,.58);path(g,b,u,co,2.5,u*o*op)
   if p and p<.998:
    ex=xx+142+298*p;ey=yy-14-.6*z
    line(g,(ex-27,ey),(ex,ey),co,2.6,o*op)
