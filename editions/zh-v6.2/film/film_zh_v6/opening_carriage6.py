"""The original opening and final handwritten signature."""
from rig4 import *


def opening(g,c):
    t=c.t;op=during(t,0,c.d,.43)
    poses=((316,210),(1249,192),(1244,682),(304,669),(786,761));angles=(-.075,.062,-.048,.116,-.11)
    # Five shapes and the two title writes keep the original opening's layout.
    if op:
        for j,((px,py),angle) in enumerate(zip(poses,angles)):
            a=.30*op;ctx=g.c;ctx.save()
            ctx.translate(px-33*t+46,py+12*sin(t*.38+j*.19));ctx.rotate(angle)
            if j==0:
                for i in range(27):
                    x=(i*71)%339-152;dot(g,x,-.4*x+((i*37)%88),3.7,C,a)
                path(g,[(-161,111),(-125,111),(-125,60),(-29,60),(-29,22),(35,22),(35,-10),(132,-10)],1,Y,5,a)
            elif j==1:
                def sigmoid(x):return 70-140/(1+exp(-x/47))
                path(g,[(x,sigmoid(x))for x in range(-153,155,4)],1,C,4,a)
                x=116*sin(t);point(g,x,sigmoid(x),8,Y,a)
            elif j==2:
                for i in range(45):rect(g,i%15*17-119,i//15*23-30,11,11,G if (i+t*8)%12>2 else T,a)
            elif j==3:
                for i in range(49):
                    if (i*19)%11<6:rect(g,(i%7-3)*20,(i//7-3)*20,18,18,(C,T,Y,V)[i%4],a)
            else:
                for i in range(28):rect(g,i*14-189,0,10,16,T if (i-t*4)%28<13 else E,a)
            ctx.restore()
        mark(g,'CS336 Lecture 12',800,360,72,t-.16,F,mode='pen',dur=.97,op=op)
        mark(g,'模型评估指标与基准测试评测',800,487,61,t-.74,Y,mode='wave',dur=.67,op=op)

def credit(g,c,t,bye):
    start=bye+.85
    a=during(t,start,c.d-1.50,.36)
    if a:mark(g,'Stanford CS336 · Lecture 12',800,450,46,t-start,F,'center','pen',.56,a)
