"""A controlled toy experiment, drawn on one common analytic loss surface."""
from rig4 import *

N=15
GRID=tuple(-1.72+3.44*j/N for j in range(N+1))
STEP=7
START=(-1.31,1.28)


@lru_cache(2)
def track(j):
    """Gradient of .19*x²+.72*y²; the second optimizer uses a diagonal scale."""
    r=(1.,1.) if not j else (3.30,.63)
    xs=[START]
    for k in range(STEP):
        x,y=xs[-1];xs.append((x-.26*.38*r[0]*x,y-.26*1.44*r[1]*y))
    return tuple(xs)


def bowl(g,c,op,pose):
    if op<.001:return
    t=c.t;a=c.at;land=a('优化器');go=a('成绩跟着变');credit=a('把差异追到');stop=a('这场实验比的是方法')
    angle=.46-.76*pose+.32*phase(t,go-.23,stop+.10)
    ca,sa=cos(angle),sin(angle)
    scale=148+24*pose
    origin=(804,535)

    def body(p):
        x,y=p;z=.19*x*x+.72*y*y
        across=ca*x-sa*y;depth=sa*x+ca*y;cam=1/(1-.072*depth)
        return (origin[0]+across*scale*cam,origin[1]+(.45*depth-.72*z)*scale*cam),depth,z

    triangles=[];vertices=[[body((x,y))for x in GRID]for y in GRID]
    for j in range(N):
        for i in range(N):
            p=vertices[j][i];q=vertices[j+1][i];r=vertices[j+1][i+1];s=vertices[j][i+1]
            points=[p,q,r,s]
            z=sum(v[2]for v in points)/4;depth=sum(v[1]for v in points)/4
            faces=tuple(v[0]for v in points);triangles.append((depth,z,faces))
    for depth,z,points in sorted(triangles,key=lambda x:x[0]):
        tone=blend(T,C,phase(z,.18,2.43));a0=.79-.43*phase(z,.35,2.71)
        # Opaque separate planar faces without glow or blur. Brighter near the valley.
        g.poly(points,tone,.95,op*.32,True,inkcol(tone,.57+.24*phase(depth,-1.5,1.4)),a0*op*.86)
    for q0 in (0,3,6,9,12,15):
        u=[vertices[j][q0][0]for j in range(N+1)]
        v=[vertices[q0][j][0]for j in range(N+1)]
        path(g,u,1,C,1.30,op*.52);path(g,v,1,T,1.30,op*.48)

    zero=body(START)[0]
    if t<stop+.90:
        k=enter(t,land-.38,.65)
        point(g,*zero,8.8,Y,k*op)
        path(g,[zero,(zero[0]-56,zero[1]-39),(zero[0]-143,zero[1]-39)],k,Y,2.,op*k)
        label(g,'同一起点',zero[0]-154,zero[1]-42,30,Y,op*k,'right')
    move=clip((t-(land-.04))/max(1.15,credit-land+.54));stops=easepos(t,go-.21,1.24)
    for j,co in enumerate((C,V)):
        pts=track(j);marks=[body(p)[0]for p in pts];span=STEP*move;front=min(STEP-1,int(span));q=span-front
        visible=enter(t,land-.12+j*.11,.45)
        for n in range(front+1):
            v=q if n==front else 1.
            if v<=0:continue
            p0,p1=pts[n:n+2]
            interp=[body(lerp(p0,p1,(i/12)*v))[0] for i in range(13)]
            path(g,interp,1,co,4.5,op*visible*.94)
            point(g,*marks[n],5.05,co,visible*op*.82)
        xx,yy=body(lerp(pts[front],pts[front+1],q))[0]
        if visible:
            point(g,xx,yy,8.4,co,op*visible)
            if stops:ring(g,xx,yy,13+2.7*stops,co,op*visible*stops,2.15)
        f=enter(t,go-.17+.13*j,.52)
        if f:
            xx2=1119+93*j;yy2=563+69*j
            path(g,[(xx+12,yy),(1043+23*j,yy2),(xx2,yy2)],f,co,2.,op*f*.82)
            label(g,('方法 A','方法 B')[j],xx2+19,yy2,30,co,op*f,'left')
            compare=enter(t,credit-.21+.14*j,.62)
            if compare:
                on=(1443,yy2);path(g,[(xx2+125,yy2),on],compare,Y,2.2,op*f*compare)
                ring(g,*on,8.4,Y,op*f*compare,2.1)
    both=enter(t,credit+.27,.58)
    if both:
        path(g,[(1443,574),(1443,681),(1395,681)],both,Y,1.9,op*both*.75)
        label(g,'同一测试集',1384,681,28,Y,op*both,'right')
    q=enter(t,land-.43,.70)
    label(g,'优化路径 · 示意',795,718,30,M,op*q)
