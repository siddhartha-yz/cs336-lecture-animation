"""Six question pauses. Reveal the following scene only after the letters leave."""
from rig4 import *
from gates6 import puzzle_gate

QUESTIONS={
    'door1':'该用哪一把尺子，又到底在评什么？',
    'door2':'把困惑度压到最低，就真的够了吗？',
    'door3':'直接出考卷、判对错，就够了吗？',
    'door4':'没有唯一标准答案，开放式回答怎么评？',
    'door5':'放进真实的电脑里，它能把活干成吗？',
    'door6':'考题像真实工作吗，模型又有没有见过题？',
}
NEXT={'door1':'1-1','door2':'2-1','door3':'3-1','door4':'4-1','door5':'5-1','door6':'7-1'}
_seats={'door4':(744,554),'door5':(865,356)}


def reveal(g,k,progress):
    from shoot4 import drawclean
    ctx=g.c
    ctx.save()
    try:
        if progress<1.:
            ctx.new_path()
            if k=='door1':
                # Raise the first blue bars off their actual baseline.
                ctx.rectangle(-2,590-594*progress,1604,4+904*progress)
            elif k in _seats:
                # Open from the real specimen: an envelope or a repository issue.
                x,y=_seats[k];r=math.hypot(max(x,1600-x),max(y,900-y))
                ctx.arc(x,y,4+(r+4)*progress,0,tau)
            else:
                ctx.rectangle(-2,-2,1604*progress,904)
            ctx.clip()
        # This is the next shot's entry at native scale and its actual clock.
        # No snapshots of the old chapter or the discarded bridge enter this layer.
        drawclean(g,NEXT[k],0.)
    finally:
        ctx.restore()


def show(g,c):
    k=c.k;t=c.t
    if k=='inter':
        puzzle_gate(g,c)
        return
    op=enter(t,.33,.27)*(1-phase(t,c.d-.79,c.d-.50))
    if op:
        mark(g,BOOK[k]['title'],800,393,57 if k=='door5' else 66,t-.34,F,mode='pen',dur=.77,op=op)
        mark(g,QUESTIONS[k],800,520,32,t-.70,'#C6CBD0',dur=.49,op=op)
        u=enter(t,.37,.59)
        line(g,(800-12*u,460),(800+12*u,460),O,1.35,u*op)
    arrive=easepos(t,c.d-.45,.40)
    if arrive:reveal(g,k,arrive)
