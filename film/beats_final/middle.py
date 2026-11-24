"""The same twenty configurations become a decision chart, then a second kind of evidence."""
from math import log10, sqrt, pi, cos, sin
from pathlib import Path
import json
from cut_common import *

SRC=Path(__file__).resolve().parent.parent/'beats_real'/'data'
LOCAL=Path(__file__).resolve().parent/'data'
def read(path):
    return json.loads(path.read_text(encoding='utf-8'))
AA=read(SRC/'artificial_analysis.json')['models']
ARENA=read(SRC/'arena.json')
ARCHIVE=read(LOCAL/'arena-robot.json')
TRAFFIC=read(SRC/'openrouter.json')['models']
TOP=tuple(sorted((r['row'] for r in read(SRC/'arena-ranks-0.raw.json')['rows']
                  if r['row']['category']=='overall' and 1<=r['row']['rank']<=8),key=lambda r:r['rank']))
BY={m['slug']:m for m in AA}
FRONT=tuple(m for m in AA if m['frontier'])
LUNA=BY['gpt-6-luna']
LIMIT=1
BEST=max((m for m in AA if m['cost']<=LIMIT),key=lambda m:m['index'])
TOP_MODEL=AA[-1]
ASTRA=BY['gpt-6-2-astra'];OPUS=BY['claude-opus-5-5']
LUNA_ARENA=next(r for r in ARENA['leaderboard'] if r['model_name']=='GPT-6 Luna (Max)')
LUNA_ROUTER=next(r for r in TRAFFIC if r['slug']=='openai/gpt-6-luna-20260922')
PALETTE=(CYAN,GOLD,TEAL,CORAL,'#96E8FF',PURPLE)
SELECTED=(-3.86,1.26,.15)
ORIG=(-3.95,-1.85,0)
XEND=(4.63,-1.85,0)
YEND=(-3.95,2.20,0)
PROMPT=(838,187,1484,277)
PAPER_Y=373
CARD_X=(846,1192)
WIN_PT=(1325,589)

def ramp(t,a,b):
    return step(t,a,max(b,a+.032))

def cue(g,d,phrase,guess,part=None):
    if isinstance(phrase,str):phrase=(phrase,)
    for p in phrase:
        hit=g.cue(p,-1)
        if hit>=0:return hit*d
    return d*(g.part(part,guess) if part is not None else guess)

def phase(t,a,b,c,d):
    return ramp(t,a,b)*(1-ramp(t,c,d))

def B(a,b,c,d,t):
    u=1-t
    return tuple(u**3*p+3*u*u*t*q+3*u*t*t*r+t**3*s for p,q,r,s in zip(a,b,c,d))

def lineprog(g,aa,bb,q,c=WHITE,wi=2,al=1):
    if q>0:g.line(*aa,*(mix(a,b,q) for a,b in zip(aa,bb)),c,wi,al)

def arrow(g,a,b,q,c=GOLD,alpha=1,w=2.25):
    if q<=0 or alpha<=0:return
    sec=tuple(mix(x,y,q) for x,y in zip(a,b))
    if q>.06:g.arrow(*a,*sec,c,w,alpha,11)
    else:lineprog(g,a,b,q,c,w,alpha)

def curve(g,a,b,c,d,q,color=GOLD,width=2.3,alpha=1):
    if q<=0 or alpha<=0:return
    pts=[B(a,b,c,d,j*q/32) for j in range(33)]
    g.poly(pts,color,width,alpha)
    return pts[-1]

def dot(g,p,c=CYAN,r=6,a=1):
    g.circle(*p,r,c,alpha=a)

def circle_world(w,p,r,c=CYAN,a=1,width=1.85):
    x,y,z=p
    w.path(tuple((x+r*cos(i*pi/26),y+r*sin(i*pi/26),z) for i in range(53)),c,width,a)

def data_x(cost):
    return mix(ORIG[0],XEND[0],(1+log10(cost))/log10(400.))

def data_y(index):
    return mix(ORIG[1],YEND[1],(index-10)/60)

def pos(m,z=.11):
    return data_x(m['cost']),data_y(m['index']),z

# Actual labels occupy local numerical geometry; their positions are not data.
M_MARKS={
 'claude-fable-5-2': ('Claude Fable 5.2',.16,.25,'left'),
 'gpt-6-2-astra': ('GPT-6.2 Astra',-.09,.26,'right'),
 'gpt-6-2-sol': ('GPT-6.2 Sol',-.14,.23,'right'),
 'muse-ember': ('Muse Ember',.10,.21,'left'),
 'gpt-6-luna': ('GPT-6 Luna',.16,-.14,'left')
}

def chart_art(w,appear=1,axis=1,spread=1,relabel=1,label=1,alpha=1,
              lead=0,x10=(0,0),yaxis=0,compare=0,remove=1,frontier=1,wall=1,
              talk_front=0,book=0,probe=0,witness=(0,0),rejected=(0,0),reading=0,ink=1,leader=1):
    if alpha<=.002:return
    w.path((ORIG,YEND),AXIS,2.05,alpha,arrow=True)
    if axis:
        w.path((ORIG,vlerp(ORIG,XEND,axis)),AXIS,2.04,alpha,arrow=True)
    for j,s in enumerate((10,20,30,40,50,60,70)):
        v=data_y(s)
        a=appear*ramp(appear,.021*j,.55+.033*j)
        w.segment((ORIG[0]-.06,v,.005),(ORIG[0]+.06,v,.005),AXIS,1.25,alpha*a)
        w.text(s,(ORIG[0]-.19,v,.03),25,MILD,alpha*a*ink,align='right',font=SERIF)
    if 0<reading<1:
        p=reading
        top=data_y(TOP_MODEL['index'])
        y=mix(top,data_y(22),p)
        x=ORIG[0]+.119
        al=alpha*ramp(p,0,.12)*(1-ramp(p,.82,1))
        w.segment((x,y+.31,.16),(x,y,.16),GOLD,3.08,al*.82)
        w.dot((x,y,.17),GOLD,.104,al)
    if yaxis:
        w.path((ORIG,YEND),CYAN,3.2,alpha*.92*sin(min(1,yaxis)*pi),
               progress=ramp(yaxis,0,.73))
    if axis:
        for j,p in enumerate((.1,.2,.3,.4,.5,.6,.7,.8,.9,1,2,3,4,5,6,7,8,9,10,20,30)):
            x=data_x(p)
            when=(x-ORIG[0])/(XEND[0]-ORIG[0])
            a=ramp(axis,when-.05,when+.025)
            major=p in (.1,1,10);h=.061 if major else .029
            w.segment((x,ORIG[1]-h,.027),(x,ORIG[1]+h,.027),WHITE,1.55 if major else 1.,
                      alpha*a*(1 if major else .54))
            if major:
                w.text('$0.10' if p==.1 else f'${int(p)}',(x,ORIG[1]-.257,.046),25,WHITE,
                       alpha*a*ink,font=SERIF)
        w.text('Dollars per task (log)',(XEND[0],ORIG[1]-.59,.065),29,WHITE,alpha*axis*ink,
               font=SERIF,align='right')
    short=alpha*ink*appear*(1-ramp(relabel,0,.44))
    long=alpha*ink*ramp(relabel,.47,1)
    w.text('Benchmark score',(ORIG[0],2.67,.06),33,WHITE,short,align='left',font=SERIF)
    w.text('Intelligence Index',(ORIG[0],2.67,.06),33,WHITE,long,align='left',font=SERIF)
    w.text('Artificial Analysis · November 2026',(XEND[0],2.67,.067),24,MILD,alpha*label*relabel*ink,
           align='right',font=SERIF)
    if wall:
        bx=data_x(LIMIT)
        pts=((ORIG[0],ORIG[1],-.07),(bx,ORIG[1],-.07),(bx,YEND[1],-.07),(ORIG[0],YEND[1],-.07))
        w.face(pts,TEAL,alpha*wall*.13,.24,0)
        w.path(((bx,YEND[1],.043),(bx,ORIG[1],.043)),CORAL,2.53,alpha*wall,
               dash=[6,6],progress=ramp(wall,0,.96))
        w.text('$1 / task',(bx+.17,YEND[1]+.17,.08),28,CORAL,alpha*wall*ink,align='left',font=SERIF)

    prog=frontier
    for j,m in enumerate(AA):
        x,y,z=pos(m)
        a=alpha*ramp(appear,min(.55,j*.025),min(.995,.49+j*.024))
        jump=ramp(spread,.003*j,.65+.018*j)
        px=mix(ORIG[0]+.12,x,jump)
        dropped=remove*(not m['frontier'])
        q=.90-.74*dropped
        c=(GOLD,TEAL,CYAN,PURPLE)[j%4]
        if m in (ASTRA,OPUS):
            rel=c if m==ASTRA else CORAL
            c=blend(c,rel,compare)
        if m==BEST:c=blend(c,CYAN,wall)
        if m==TOP_MODEL:c=blend(c,GOLD,lead)
        r=.060+(.022 if m in (BEST,TOP_MODEL,LUNA) else 0)
        w.dot((px,y,z),c,r,a*q)
        if lead and m==TOP_MODEL:
            circle_world(w,(px,y,z),.135+.028*probe,GOLD,a*lead)
        if m['slug'] in M_MARKS and label and spread:
            name,dx,dy,side=M_MARKS[m['slug']]
            la=alpha*label*ink*ramp(spread,.65,.97)
            if m==ASTRA:la*=1-ramp(compare,.0,.17)
            w.text(name,(x+dx,y+dy,.129),22,WHITE,la*.93,font=SERIF,align=side)
    if compare:
        x1,y1,_=pos(OPUS);x2,y2,_=pos(ASTRA)
        pair=alpha*compare
        route=((x1,y1,.141),(x2,y1,.141),(x2,y2,.141))
        w.path(route,GOLD,2.46,pair,arrow=True,progress=ramp(compare,0,.95))
        w.dot((x2,y2,.16),GOLD,.106,pair)
        w.dot((x1,y1,.16),CORAL,.106,pair)
        name=ramp(compare,.18,.68)*alpha*ink
        w.text('GPT-6.2 Astra',(x2-.109,y2+.38,.17),26,GOLD,name,font=SERIF,align='right')
        w.text('$4.00',(x2-.109,y2+.13,.16),22,WHITE,name,font=SERIF,align='right')
        w.text('Claude Opus 5.5',(x1+.13,y1-.30,.163),26,CORAL,name,font=SERIF,align='left')
        w.text('$10.04',(x1+.13,y1-.55,.163),22,WHITE,name,font=SERIF,align='left')
    if prog:
        pts=[pos(FRONT[0],.085)]
        for m in FRONT[1:]:
            x,y,z=pos(m,.085)
            pts.extend(((x,pts[-1][1],z),(x,y,z)))
        pts.append((XEND[0]-.025,pts[-1][1],.085))
        w.path(pts,GOLD,3.18,alpha,progress=prog)
        for j,m in enumerate(FRONT):
            if ramp(prog,.022+j*.14,.07+j*.16) and m!=BEST:
                w.dot(pos(m,.17),GOLD,.067,alpha*ramp(prog,.022+j*.14,.07+j*.16))
        pt=(len(pts)-1)*prog
        n=min(int(pt),len(pts)-2)
        cp=vlerp(pts[n],pts[n+1],min(1,pt-n))
        if prog<.997:w.dot(cp,GOLD,.086,alpha)
    if wall:
        q=pos(BEST,.23);x,y,z=q
        circle_world(w,q,.126+.082*book,CYAN,alpha*wall)
        w.dot(q,CYAN,.085,alpha*wall)
        # Terra has exactly one label state (the budget readout), no scatter
        # alias underneath. The readout and its entire leader stay left of the wall.
        la=alpha*ramp(wall,.22,.88)*label*ink
        end=(x-.78,y-.41,.25)
        w.path(((x-.135,y-.029,.25),(x-.48,y-.41,.25),end),CYAN,1.62,la*leader)
        w.text(f"{BEST['index']:.1f} · ${BEST['cost']:.2f}",(x-.84,y-.48,.255),25,CYAN,la,
               font=SERIF,align='right')
        w.text('GPT-6.1 Terra',(x-.84,y-.23,.255),28,WHITE,la,
               font=SERIF,align='right')
    for q,v0,v1 in zip(x10,(.1,1),(1,10)):
        if q<=0:continue
        x0,x1=data_x(v0),data_x(v1)
        yy=ORIG[1]-.518
        p=((x0+.037,yy,.20),(x1-.037,yy,.20))
        a=alpha*min(1,q*2)*(1-ramp(q,.74,1))
        w.path(p,CYAN,2.32,a,arrow=True,progress=ramp(q,0,.47))
        for x in (x0,x1):
            w.segment((x,ORIG[1]-.071,.21),(x,ORIG[1]+.11,.21),GOLD,2.03,a)
        w.text('×10',((x0+x1)/2,yy-.239,.204),29,GOLD,a*ink,font='math')
    if wall and rejected[1]:
        q,a=rejected
        x,y,z=pos(TOP_MODEL,.189)
        circle_world(w,(x,y,z),.141,CORAL,alpha*a)
        datum=(x,ORIG[1]+.098,z)
        w.path(((x,y-.13,z),datum),CORAL,1.86,alpha*a*.88,dash=[5,6],
               progress=ramp(q,0,.71))
        h=ramp(q,.55,1)
        w.path((datum,(data_x(LIMIT)+.04,datum[1],z)),CORAL,2.06,alpha*a*.82,
               arrow=True,progress=h)
    if wall and max(witness)>0:
        x,y,z=pos(BEST,.227); h,v=witness
        bx=data_x(LIMIT)
        sx,sy,_=pos(FRONT[0],z)
        ax,ay,_=pos(ASTRA,z)
        for c,q,pts in ((TEAL,h,((sx,sy,z),(x,sy,z),(x,y-.13,z))),
                        (CORAL,v,((ax,ay,z),(bx+.072,ay,z)))):
            a=alpha*ramp(q,0,.17)*(1-ramp(q,.81,1))
            if not a:continue
            u=ramp(q,0,.78)
            w.path(pts,c,3.25,a,arrow=True,progress=u)
            j=min(int((len(pts)-1)*u),len(pts)-2)
            cur=vlerp(pts[j],pts[j+1],clamp((len(pts)-1)*u-j))
            ring=.116+.085*(1-ramp(q,.10,.42))
            circle_world(w,cur,ring,c,a,2.9)
            w.dot(cur,c,.108,a)
    if talk_front:
        note(w,(1.4,-.90,.14),'Pareto frontier',('A better score comes at a higher cost',),
             GOLD,alpha*talk_front*ink)

def dock_chart(g,q=1,alpha=1,retreat=0):
    w=World(g,zoom=mix(1,.535,q)*(1-.55*retreat),
            center=(mix(800,mix(437,212,retreat),q),mix(404,mix(369,153,retreat),q)))
    chart_art(w,label=0,ink=0,alpha=mix(1,.76,q)*alpha,book=.2*q)
    return w

def prompt_art(g,a=1,q=1,origin=None):
    x0,y0,x1,y1=PROMPT
    if a<=.002 or q<=0:return
    origin=origin or (x0,(y0+y1)/2)
    x=mix(origin[0],x0,q);y=mix(origin[1],y0,q)
    w=mix(0,x1-x0,q);h=mix(2,y1-y0,q)
    stamp=ramp(q,.66,.99)
    if stamp:
        g.line(x,y+h,x+w*stamp,y+h,CYAN,1.9,a*stamp)
    g.text(ARCHIVE['prompt'],x+12,y+h*.54,35,WHITE,a*ramp(q,.92,1),align='left',font=SERIF)

def prompt_handoff(g,w,p):
    """The budget readout's bent leader straightens into the prompt baseline."""
    if p<=.004:return
    x,y,_=pos(BEST,.23)
    hooks=tuple(w.pos(pt) for pt in ((x-.78,y-.41,.25),(x-.48,y-.41,.25),(x-.135,y-.029,.25)))
    x0,y0,x1,y1=PROMPT
    travel=ramp(p,.034,.72)
    unfold=ramp(p,.36,1)
    width=mix(64,x1-x0,unfold)
    finals=((x0,y1),(x0+.38*width,y1),(x0+width,y1))
    # The elbow follows a different path from the two endpoints; the three
    # vertices only become collinear as the old leader turns into a baseline.
    lift=39*sin(pi*travel)
    spine=tuple((mix(a[0],b[0],travel),mix(a[1],b[1],travel)-lift*(1-j*.29))
                for j,(a,b) in enumerate(zip(hooks,finals)))
    a=ramp(p,.004,.095)
    g.poly(spine,CYAN,mix(1.62,1.9,travel),a)
    terminal=mix(5.7,0,ramp(p,.78,.996))
    if terminal>.35:dot(g,spine[-1],CYAN,terminal,a)
    # The physical ruler's tip is the writing aperture, not a crossfade.
    chart_right=w.pos((XEND[0],YEND[1],.09))[0]
    written=ramp(p,.67,.982)*ramp(x0-chart_right,7,28)
    if written:
        edge=min(x1,max(x0,spine[-1][0]))
        g.c.save()
        g.c.rectangle(x0,y0-2,(edge-x0)*written,y1-y0+3);g.c.clip()
        g.text(ARCHIVE['prompt'],x0+12,y0+(y1-y0)*.54,35,WHITE,1,
               align='left',font=SERIF)
        g.c.restore()


def c_d_seam(g):
    dock_chart(g).draw()
    prompt_art(g)

def chart(g,t,d):
    if t<=0:vertical(g).draw();return
    if t>=d-.46:c_d_seam(g);return
    cost=cue(g,d,('cost','inference cost'),.244,1)
    intelligence=cue(g,d,('intelligence against','plot their intelligence'),.404,2)
    log_at=cue(g,d,('logarithmic scale',),.49)
    boundary=cue(g,d,('boundary takes shape',),.559)
    cap_at=cue(g,d,('real-world budget','real world budget'),.632,3)
    ast=boundary-.03
    name_step=cue(g,d,('Pareto frontier',),.743)
    highest=cue(g,d,('highest model on the board','highest model'),.689)
    cheapest=cue(g,d,('no cheaper model',),.797)
    stronger=cue(g,d,('no stronger model',),.838)
    hand=cue(g,d,('objective answer key','there isn'),.945,4)
    hand=max(d-5,min(hand,d-2.85))
    make=ramp(t,.028,1.19)
    take_start=hand-.61
    take=ramp(t,take_start,d-.49)
    if make<1:vertical(g,1-make).draw()
    a=ramp(t,.105,2.49)
    x=ramp(t,cost-.055,cost+2.79)
    spread=ramp(t,cost+.14,cost+3.9)
    rr=ramp(t,intelligence-.105,intelligence+1.21)
    q0=ramp(t,log_at-.041,log_at+3.8)
    q1=ramp(t,log_at+1.18,log_at+3.8)
    v=ramp(t,intelligence-.06,intelligence+2.54)
    comp=phase(t,ast-.09,ast+.82,max(ast+1.14,cap_at+.26),max(ast+2.7,cap_at+1.32))
    remove=ramp(t,name_step-.22,max(name_step+2.12,stronger-.76))
    ff=ramp(t,name_step-.08,max(name_step+2.45,stronger+.37))
    wall=ramp(t,cap_at-.066,cap_at+1.84)
    rejected=(ramp(t,highest-.055,max(highest+1.83,name_step-.02)),
              phase(t,highest-.055,highest+.57,name_step-.08,name_step+.55))
    noteq=phase(t,name_step-.025,name_step+.84,hand-.31,hand+.42)
    witness=(ramp(t,cheapest-.04,max(cheapest+2.94,stronger+.84)),
             ramp(t,stronger-.04,max(stronger+2.20,hand-.03)))
    reading=ramp(t,1.88,cost-.02)
    label=ramp(t,cost+1.51,cost+5.01)
    ink=1-ramp(t,take_start-.30,take_start+.63)
    lead=phase(t,1.24,2.55,cost+.22,cost+.79)
    zoom=mix(1,.535,take)
    alone=ramp(t,.39,2.14)*(1-ramp(t,cost-.025,cost+1.52))
    drift=(.5+.5*sin(t*1.75))*alone
    w=World(g,zoom=zoom,center=(mix(800+240*alone,437,take),mix(404,369,take)))
    chart_art(w,appear=a,axis=x,spread=spread,relabel=rr,label=label,
              alpha=make*mix(1,.72,take),lead=lead,x10=(q0,q1),yaxis=v,
              compare=comp,remove=remove,frontier=ff,wall=wall,talk_front=noteq,book=.2*take,
              probe=drift,witness=witness,rejected=rejected,reading=reading,ink=ink,
              leader=1-ramp(take,0,.12))
    w.draw()
    if take:prompt_handoff(g,w,take)


def premise(g,i,x,y,q,op):
    if op<=.002:return
    if i==0:
        col=CYAN
        g.poly(((x,y+24),(x,y-24),(x+13,y-37),(x+30,y-37)),col,2.75,op)
        g.line(x-15,y+24,x+15,y+24,col,2.3,op)
        g.poly(((x+24,y-37),(x+44,y-37),(x+46,y-25),(x+22,y-25)),GOLD,2.5,op,True)
        r=sin(pi*clamp(q)); rx=x-60+48*r; ry=y+6
        g.rect(rx-13,ry-23,26,21,None,col,2.35,alpha=op)
        dot(g,(rx-7,ry+3),col,3.2,op);dot(g,(rx+7,ry+3),col,3.2,op)
        g.line(rx+13,ry-16,rx+26,ry-29-12*r,col,2.54,op)
        g.line(rx+25,ry-31-12*r,rx+38,ry-31-12*r,GOLD,3.55,op)
    else:
        col=TEAL; leaf=31*clamp(q); rx=x-50+34*sin(pi*clamp(q)*.55)
        g.rect(rx-13,y+2,26,21,None,col,2.35,alpha=op)
        dot(g,(rx-7,y+27),col,3.2,op);dot(g,(rx+7,y+27),col,3.2,op)
        g.line(rx+13,y+10,x-10,y+2,col,2.4,op)
        g.line(x,y+23,x,y-12-leaf,col,2.60,op)
        yy=y-9-leaf
        g.poly(((x,yy+14),(x+14,yy-4),(x+24,yy-8),(x+17,yy+5),(x,yy+14)),
               col,1.9,op,True,col,.53)
        g.poly(((x,yy+21),(x-12,yy+1),(x-24,yy-4),(x-18,yy+10),(x,yy+21)),
               col,1.9,op,True,col,.53)
        g.line(x-18,y+24,x+20,y+24,col,2.4,op)

def draw_story(g,a,b,phase_,al=1,exit=0,vote=0,look=0,hero=0,preview=0):
    if al<=.002:return
    g.c.save()
    # Keep the archived reply layer on the right, away from the growing left graph.
    k=1-.095*exit
    g.c.translate(137*exit,-30*exit)
    g.c.scale(k,k)
    x0,y0,x1,y1=PROMPT
    retract=1-ramp(exit,.49,.994)
    if retract:
        g.c.save();g.c.rectangle(x0-4,y0-4,(x1-x0+10)*retract,y1-y0+8);g.c.clip()
        prompt_art(g,al,1)
        g.c.restore()
    g.text('Blind comparison · 8 July 2025',1480,159,23,WHITE,
           al*ramp(a,0,.54)*(1-ramp(exit,.74,.966)),align='right',font=SERIF)
    use=(a,b)
    card_lines=(('A lamppost-polishing robot','loses its job.'),
                ('A maintenance robot finds','a plant in an empty mall.'))
    name=('Gemini 2.5 Pro','Claude Opus 4')
    for i,(x,q) in enumerate(zip(CARD_X,use)):
        # Each reply exits along the underline it grew from. Its text, names
        # and illustration share that closing aperture; the dated prompt keeps
        # its own edge until after the last reply has folded away.
        fold=1-ramp(exit,.018+.15*i,.64+.19*i)
        if not fold:continue
        g.c.save()
        g.c.rectangle(x-12,333,(323 if i==0 else 312)*fold,279);g.c.clip()
        if q:
            y=PAPER_Y-11*(1-q);xx=x+14*(1-q)
            on=al*ramp(q,0,.91)
            paint_color=CYAN if i==0 else TEAL
            g.line(xx,y+27,xx+min(235,321*fold),y+27,paint_color,2.04,on)
            reveal=ramp(vote,.44,.99)
            if reveal<.50:
                g.text(('Model A','Model B')[i],xx,y,29,paint_color,on*(1-ramp(reveal,.21,.50)),
                       align='left',font=SERIF)
            else:
                g.text(name[i],xx,y,28,paint_color,on*ramp(reveal,.51,.89),align='left',font=SERIF)
            for j,s in enumerate(card_lines[i]):
                g.text(s,xx,y+73+j*33,25,WHITE,on*ramp(q,.36+j*.09,.87+j*.12),
                       align='left',font=SERIF)
        ink=al*max(preview,ramp(q,.20,.91)*ramp(phase_,.025,.54))
        premise(g,i,x+105,PAPER_Y+172,hero,ink)
        g.c.restore()
    if 0<look<1:
        start=(950,571);end=(1306,571)
        travel=ramp(look,.10,.84)
        x,y=B(start,(1038,575),(1223,575),end,travel)
        vote_ink=al*sin(pi*look)**.62*(1-vote)
        previous=B(start,(1038,575),(1223,575),end,max(0,travel-.22))
        g.line(*previous,x,y,WHITE,2.45,vote_ink*.78)
        dot(g,(x,y),blend(WHITE,GOLD,vote),8.1,vote_ink)
    if vote:
        a=al*ramp(vote,0,.83)
        x,y=WIN_PT
        reveal=1-ramp(exit,.035,.45)
        g.c.save()
        g.c.rectangle(x-84,y-20,168*reveal,46);g.c.clip()
        g.text('B preferred',x,y,30,GOLD,a,font=SERIF)
        g.c.restore()
        if reveal:
            g.line(x-73,y+24,x-73+146*reveal,y+24,GOLD,1.81,a)
    g.c.restore()

GRAPH_P=((167,323),(247,262),(325,304),(394,259),(477,318),(565,278),
         (192,437),(293,410),(384,464),(482,423),(569,409),(291,514),(450,529))
GRAPH_E=((7,8),(0,1),(0,2),(1,3),(1,7),(2,4),(2,7),(3,5),(3,9),
         (4,6),(4,8),(4,10),(5,10),(6,8),(6,11),(7,12),(8,10),(9,12),
         (10,12),(11,12))
def archive_network(g,q,doc,alpha,arrival):
    """Place the historical vote on the first edge of the schematic left-hand graph."""
    if q<=0 or alpha<=.002:return
    pts=[(x-37*doc,y-30*doc) for x,y in GRAPH_P]
    played=ramp(arrival,.78,1)
    for j,(a,b) in enumerate(GRAPH_E):
        u=ramp(q,j*.020,.43+j*.024)
        if not u:continue
        if j==0:
            # The actual ballot lights its example edge, after the traveling
            # gold marker gets to the left-hand network.
            lineprog(g,pts[b],pts[a],played,GOLD,3.6,alpha*played)
        else:
            c=blend(EDGE,CYAN,(j%3)*.29)
            lineprog(g,pts[a],pts[b],u,c,1.56,u*alpha)
    for j,p in enumerate(pts):
        u=ramp(q,.033*(j%5),.54+.066*(j%5))
        c=blend(CYAN,GOLD,played) if j in (7,8) else CYAN
        dot(g,p,c,5.75 if j in (7,8) else 4.9,u*alpha)
    p0=pts[7]
    label=alpha*ramp(q,.3,.93)
    g.text('One vote',p0[0]-14,p0[1]-24,25,GOLD,alpha*played,align='right',font=SERIF)
    g.text('Pairwise comparisons · schematic',374-55*doc,578-30*doc,24,WHITE,label,font=SERIF)
    g.text('Archive example · 8 July 2025',374-55*doc,609-30*doc,22,MILD,label,font=SERIF)

def ballot_flight(g,q,anchor,doc,alpha=1):
    if not 0<q<1:return
    dst=(GRAPH_P[8][0]-37*doc,GRAPH_P[8][1]-30*doc)
    p=(anchor,(anchor[0]-247,anchor[1]+97),(dst[0]+238,dst[1]+135),dst)
    pts=[B(*p,ramp(q,0,1)*i/32) for i in range(33)]
    vis=alpha*ramp(q,.0,.14)*(1-ramp(q,.85,1))
    g.poly(pts[-10:],GOLD,2.75,vis*.85)
    dot(g,pts[-1],GOLD,8.25,vis)

def rating_x(x):
    return mix(1127,1386,(x-1488)/64)
BOARDS=tuple(230+52*j for j in range(8))

def board(g,q,alpha,zoom_out=0,overlap=0):
    if q<=0 or alpha<=.002:return
    g.c.save()
    k=1-.59*zoom_out
    g.c.translate(370*zoom_out,16*zoom_out)
    g.c.scale(k,k)
    a=alpha*ramp(q,0,.35)*(1-ramp(zoom_out,.17,.53))
    g.text('Text Arena',712,171,42,WHITE,a,align='left',font=SERIF)
    g.text('Overall · snapshot, 22 November 2026',1488,143,25,WHITE,a,align='right',font=SERIF)
    if overlap:
        data=(max(TOP[0]['rating_lower'],TOP[1]['rating_lower']),
              min(TOP[0]['rating_upper'],TOP[1]['rating_upper']))
        x,z=map(rating_x,data)
        g.rect(x,BOARDS[0],z-x,(BOARDS[1]-BOARDS[0])*overlap,TEAL,alpha=alpha*.47)
    for j,m in enumerate(TOP):
        rr=ramp(q,j*.047,.54+j*.062)
        close=1-ramp(zoom_out,.23+.026*(7-j),.61+.042*(7-j))
        edge=712+790*min(rr,close)
        if edge<=713:continue
        y=BOARDS[j]; x=rating_x(m['rating']);l=rating_x(m['rating_lower']);r=rating_x(m['rating_upper'])
        c=(GOLD,CYAN)[j] if j<2 else MILD
        a=alpha
        # A row draws from its ordinal towards its own numeric interval.
        # Independent slots, not a stream of old votes landing in a new table.
        g.c.save()
        g.c.rectangle(708,y-17,edge-708,34);g.c.clip()
        g.text(f"{j+1:02}",716,y,24,WHITE,a,align='left',font=SERIF)
        g.text(m['model_name'],785,y,25,WHITE,a,align='left',font=SERIF)
        g.line(l,y,r,y,c,2.25,a)
        for to in (l,r):
            g.line(to,y-6,to,y+6,c,1.55,a)
        dot(g,(x,y),c,4.6,a)
        g.text(f"{m['rating']:.1f}",1488,y,26,c,a*ramp(edge,1488,1501),align='right',font=SERIF)
        g.c.restore()
        if .018<rr<.98 and close>.98:
            fade=ramp(rr,0,.12)*(1-ramp(rr,.73,.98))
            g.line(edge,y-9,edge,y+9,c,1.75,fade*.82*a)
    if overlap:
        x,y=map(lambda m:rating_x(m['rating']),TOP[:2])
        q=TOP[0]['rating']-TOP[1]['rating']
        g.poly(((y,200),(y,192),(x,192),(x,200)),GOLD,1.65,overlap*alpha)
        g.text(f'{q:.1f} pts',(x+y)/2,176,22,GOLD,overlap*alpha,font=SERIF)
    g.c.restore()

DETAIL_SINK=(469,510,540,569,598,627)
DETAIL_HEAD=(850,403)
DETAIL_START=851
DETAIL_EXIT=1088

def traffic_detail(g,t,paid,closing):
    """An on-demand detail of the API cell; widths share one token denominator."""
    q=ramp(t,paid,paid+.47)
    if q<=.001 or closing>=1:return
    appeared=ramp(q,.19,.83)
    caption=appeared*(1-ramp(closing,.01,.51))
    g.text('OpenRouter · 23 Nov 2026',*DETAIL_HEAD,26,WHITE,caption,align='left',font=SERIF)
    g.text('Public API tokens · share of these six',DETAIL_HEAD[0],430,22,WHITE,
           caption*.93,align='left',font=SERIF)
    stack=480
    attention=ramp(t,paid+.60,paid+1.55)
    for i,m in enumerate(TRAFFIC):
        share=m['share_of_shown']
        thick=101*share
        start_y,stack=stack+thick/2,stack+thick
        last_y=DETAIL_SINK[i]
        focal=(i==4)
        extent=ramp(q,.035*i,.73+.040*i)*(1-ramp(closing,.21 if focal else .035,
                                                    .45 if focal else .63))
        if extent<.002:continue
        color=blend(PALETTE[i],GOLD,attention) if focal else PALETTE[i]
        band_a=ramp(extent,0,.095)*(1-.24*attention*(not focal))
        upper,lower=[],[]
        for j in range(34):
            f=j*extent/33
            x=mix(DETAIL_START,DETAIL_EXIT,f)
            yy=mix(start_y,last_y,ramp(f,.03,.98))
            upper.append((x,yy-thick/2));lower.append((x,yy+thick/2))
        g.poly(upper+lower[::-1],color,0,band_a,True,color,.94)
        lab=appeared*(1-ramp(closing,.04 if focal else .025,.44 if focal else .51))
        g.text(m['name'],1106,last_y,23,color if focal else WHITE,lab,align='left',font=SERIF)
        g.text(f'{share*100:.1f}%',1487,last_y,23,color,lab,align='right',font=SERIF)
        if focal and closing<=.002:
            run=ramp(t,paid+.61,paid+2.65)
            x=mix(DETAIL_START,DETAIL_EXIT,run*extent)
            yy=mix(start_y,last_y,ramp(run*extent,.03,.98))
            dot(g,(x,yy),WHITE,3.2,ramp(run,0,.115))
            if run>.65:
                end=ramp(run,.65,1)
                g.line(DETAIL_EXIT,last_y,DETAIL_EXIT+11*end,last_y,GOLD,1.8,band_a)

METRICS=(
    (-2.65,1.26,'Intelligence Index',f"{LUNA['index']:.1f}",f"Rank {LUNA['index_rank']} of 20 shown",CYAN),
    (2.65,1.26,'Cost per task',f"${LUNA['cost']:.3f}",f"{LUNA['cost_rank']}nd cheapest · 20 shown",GOLD),
    (-2.65,-.83,'Text preference',f"{LUNA_ARENA['rating']:.1f}",f"Rank {int(LUNA_ARENA['rank'])} of {ARENA['ranked_entries']} · Arena",TEAL),
    (2.65,-.83,'API tokens',f"{LUNA_ROUTER['trillion_tokens']:.2f} T",f"{LUNA_ROUTER['rank']}th · OpenRouter day",PURPLE),
)
METRIC_MARKS=(SELECTED,(1.42,1.26,.15),(-3.86,-.83,.15),(1.42,-.83,.15))

def selection_stage(g,alpha=1,quantities=(1,1,1,1),focus=1,ready=1,scan=0,heads=None,highlights=None,title_opacity=None,lens=0,ruling=1,upper_rule=None):
    """Exact D-to-E paste-like layer. Every measurement keeps its own units and pool."""
    w=World(g)
    if alpha<=.002:return w
    w.text('GPT-6 Luna',(0,2.59,.10),48,WHITE,alpha*(ready if title_opacity is None else title_opacity),font=SERIF)
    if ruling>=.999:
        w.segment((-4.65,2.17,.023),(4.65,2.17,.023),EDGE,1.28,alpha*ready)
        w.segment((-.0,-1.77,.022),(.0,2.05,.022),EDGE,1.19,alpha*ready*.64)
        w.segment((-4.66,.20,.021),(4.66,.20,.021),EDGE,1.19,alpha*ready*.64)
    elif ruling>0 or upper_rule:
        # The horizontal and vertical dividers are drawn from their joint,
        # so the four separate lanes exist before any measure counts.
        h=ramp(ruling,.08,.78);v=ramp(ruling,.21,.89)
        top=ramp(ruling,.32,1) if upper_rule is None else upper_rule
        top_a=ready if upper_rule is None else max(ready,.86*upper_rule)
        arriving=0 if upper_rule is None else 1-ramp(upper_rule,.58,1)
        top_ink=blend(EDGE,WHITE,.46*arriving)
        for dx in (-1,1):
            w.path(((0,.20,.021),(4.66*dx,.20,.021)),EDGE,1.19,alpha*ready*.64,progress=h)
            w.path(((0,2.17,.023),(4.65*dx,2.17,.023)),top_ink,1.28+.33*arriving,alpha*top_a,progress=top)
        for y in (-1.77,2.05):
            w.path(((0,.20,.022),(0,y,.022)),EDGE,1.19,alpha*ready*.64,progress=v)
    for j,(x,y,label,value,scope,color) in enumerate(METRICS):
        q=quantities[j]
        p=METRIC_MARKS[j]
        h=q if heads is None else heads[j]
        if h:
            w.text(label,(p[0]+.29,p[1]+.423,.15),29,WHITE,alpha*h,
                   align='left',font=SERIF)
        if q<=0:continue
        a=alpha*q
        col=color if j!=0 else blend(WHITE,CYAN,focus)
        w.dot(p,col,.074,a)
        if j==0 and focus:
            circle_world(w,p,.159,CYAN,a*focus,2.06)
        w.text(value,(p[0]+.29,p[1],.163),53,col,a,align='left',font=SERIF)
        beat=4*scan-j
        sweep=(sin(pi*beat)**1.2) if 0<beat<1 else 0
        w.text(scope,(p[0]+.29,p[1]-.473,.14),24+5*sweep,blend(WHITE,color,.63*sweep),
               a*(.9+.1*sweep),align='left',font=SERIF)
        if j==1:
            w.text('At $1: feasible, off frontier',(p[0]+.29,p[1]-.707,.144),19,MILD,
                   a*.93,align='left',font=SERIF)
        if highlights:
            v=highlights[j]
            if 0<v<1:
                a0=alpha*ramp(v,0,.095)*(1-ramp(v,.69,1))
                circle_world(w,p,.127+.093*ramp(v,0,.60),color,a0,2.38)
                y1=p[1]-.648 if j!=1 else p[1]-.812
                points=((p[0]+.28,y1,.146),(p[0]+2.24,y1,.146))
                w.path(points,color,2.38,a0,progress=ramp(v,0,.74))
        if sweep:
            under=.825 if j==1 else .656
            a1=(p[0]+.29,p[1]-under,.147)
            a2=(p[0]+2.37,p[1]-under,.147)
            w.path((a1,a2),color,3.3,alpha*sweep,progress=ramp(beat,0,.72))
            circle_world(w,p,.106+.118*ramp(beat,0,.72),color,alpha*sweep,2.72)
    if 0<lens<1:
        p=METRIC_MARKS[0]
        a=alpha*ramp(lens,0,.19)*(1-ramp(lens,.72,1))
        v=ramp(lens,0,.76)
        # Follow the benchmark pin into the next scene, without reconnecting ranks.
        radius=mix(.40,.178,v)
        arc=tuple((p[0]+radius*cos(pi*2*i/54),p[1]+radius*sin(pi*2*i/54),p[2])
                  for i in range(55))
        w.path(arc,CYAN,3.15,a,progress=v)
        w.dot((p[0]+radius*cos(2*pi*v),p[1]+radius*sin(2*pi*v),p[2]),CYAN,.085,a)
    w.text('Max effort for tests, cost and Arena; endpoint-level API use.',(0,-2.02,.11),
           23,WHITE,alpha*ready*.84,font=SERIF)
    return w

def caption_topics(g,t,d,a,at):
    if a<=.002:return
    a0,a1,a2=at
    for j,(x,label,when,col) in enumerate(zip((939,1148,1348),('Essay','Bug','Tone'),at,(CYAN,PURPLE,TEAL))):
        q=ramp(t,when-.06,when+.49)
        if q:
            g.text(label,x,126,28,col,a*q,font=SERIF)
            g.line(x-30,149,x-30+60*q,149,col,1.56,a*q)

def facts_shelf(g,t,d,anchors,al=1):
    if al<=.002:return
    cells=[
        (224,'Intelligence Index',f'{LUNA["index"]:.1f}',CYAN),
        (633,'Cost per task',f'${LUNA["cost"]:.3f}',GOLD),
        (961,'Preference rating',f'{LUNA_ARENA["rating"]:.1f}',TEAL),
    ]
    for (x,kind,value,col),time in zip(cells,anchors):
        p=ramp(t,time-.058,time+.54)
        if p:
            g.line(x,708,x+270*p,708,col,1.55,al*p*.80)
            g.text(kind,x,735,22,WHITE,al*p,align='left',font=SERIF)
            g.text(value,x+270,735,27,col,al*p,align='right',font=SERIF)

def dialogue(g,t,d):
    if t<=0:c_d_seam(g);return
    if t>=d-.43:selection_stage(g).draw();return
    p=lambda s,k,part=None:cue(g,d,s,k,part)
    essay=p(('drafting a persuasive essay','persuasive essay'),.036)
    bug=p(('explaining a complex bug','complex bug'),.077)
    tone=p(('adjusting tone',),.121)
    ar=p(('Chatbot Arena changes','Chatbot Arena'),.17,1)
    rigid=p(('grading against a rigid rubric','against a rigid rubric'),.253,2)
    blind=p(('blind, pairwise human votes','blind pairwise human votes','pairwise human votes'),.325,2)
    vo=p(('human votes','pairwise human'),.358,2)
    network=p(('By fitting those binary choices','fitting those binary choices'),.389,3)
    fit=p(('Elo rating system','Elo rating'),.438,3)
    later=max(network+.82,fit-.11)
    compare=p(('compare the exact same model','exact same model'),.620,4)
    ind=p(('raw benchmark accuracy','benchmark accuracy'),.671)
    cheap=p(('budget-constrained Pareto efficiency','Pareto efficiency'),.729)
    pref=p(('blind human preference',),.782)
    paid=p(('actual paid API volume','API volume'),.824)
    ranks=p(('rankings shift',),.866,5)
    inner=p(('which trade-off','which trade off'),.963,6)
    flight_start=max(vo+.77,network-.13)
    flight_end=flight_start+1.76
    story_start=flight_start+.24
    story_end=flight_start+1.35
    later=max(later,story_end+.11)
    opening_exit=ramp(t,story_start,story_end)
    retreat=ramp(t,flight_start-.42,flight_start+1.22)
    plot_a=1-ramp(retreat,.38,1)
    if plot_a:
        dock_chart(g,1,plot_a,retreat).draw()
    if opening_exit<1:
        story_a=1
        boot=ramp(t,ar-.06,ar+1.05)
        boot2=ramp(t,ar+.72,ar+2.06)
        ai=ramp(t,ar+.19,blind-.33)
        win=ramp(t,vo-.08,vo+.76)
        look=ramp(t,rigid-.06,max(rigid+.72,vo+.21))
        hero=ramp(t,essay+.27,max(ar+.65,blind-.41))
        preview=phase(t,essay-.075,essay+.61,ar+.51,ar+1.20)*.93
        draw_story(g,boot,boot2,ai,story_a,opening_exit,win,look,hero,preview)
        topic_a=phase(t,0,.22,ar-.39,ar+.38)
        caption_topics(g,t,d,topic_a,(essay,bug,tone))
    flight=ramp(t,flight_start,flight_end)
    dock_hist=ramp(t,flight_end+.36,compare+.02)
    archive_a=ramp(t,flight_start+.05,flight_end-.62)*(1-ramp(dock_hist,.49,1))
    archive_motion=ramp(t,flight_start+.17,flight_end+1.29)
    archive_network(g,archive_motion,dock_hist,archive_a,flight)
    # The dated archive stays left. Nothing flies out of it toward the new board.
    ballot_flight(g,flight,(WIN_PT[0],WIN_PT[1]+24),dock_hist)
    board_q=ramp(t,later-.04,later+2.65)
    # Carry the observed intervals into the first comparison rules; close
    # their slots before the next model title appears.
    shrink_board=ramp(t,compare+.93,ind-.69)
    old_board=1-ramp(shrink_board,.28,.94)
    range_trace=ramp(t,later+.89,compare-.23)
    board(g,board_q,old_board,zoom_out=shrink_board,overlap=range_trace)
    fit_note=phase(t,fit-.035,fit+.92,compare-.45,compare+.36)
    if fit_note:
        g.text('Bradley–Terry rating',175,677,31,WHITE,fit_note,align='left',font=SERIF)
        g.text('Fit pairwise win probabilities',175,713,24,WHITE,fit_note,align='left',font=SERIF)
        g.text('P(A wins) = σ(sₐ − sᵦ)',175,749,26,GOLD,fit_note,align='left',font='math')

    # Only the spoken fourth measure opens its own evidence detail. In
    # particular, there is no usage window under the end of the Arena board.
    intro=ramp(t,ind-1.16,ind-.19)
    title=ramp(t,ind-.67,ind+.025)
    into=ramp(t,inner-.24,d-.44)
    closing=ramp(t,paid+2.80,paid+3.35)
    if intro or title:
        words=(ind,cheap,pref)
        first_heads=tuple(ramp(t,cue_-.038,cue_+.37) for cue_ in words)
        heads=(*first_heads,ramp(t,paid+3.15,paid+3.54))
        nums=(*(ramp(t,time-.075,time+.55) for time in words),
              ramp(t,paid+3.19,paid+3.64))
        pulses=(*(ramp(t,time-.070,next_-.12) for time,next_ in zip(words,(cheap,pref,paid))),
                ramp(t,paid+3.13,paid+4.26))
        tail=ramp(t,ranks-.062,max(ranks+2.75,inner+.30))
        w=selection_stage(g,1,nums,focus=max(into,.34*ramp(t,ind,ind+.66)),
                          ready=intro,scan=tail,heads=heads,highlights=pulses,
                          title_opacity=title,lens=into,ruling=ramp(t,ind-1.16,ind-.17),
                          upper_rule=ramp(t,ind-1.12,ind-.49))
        w.draw()
        if t>=paid and closing<1:
            traffic_detail(g,t,paid,closing)
        if 0<closing<1:
            src=(DETAIL_EXIT,DETAIL_SINK[4])
            dst=w.pos(METRIC_MARKS[3])
            u=ramp(closing,.09,.98)
            a=(1-ramp(closing,.84,1))*ramp(closing,0,.19)
            v=curve(g,src,(src[0]-50,src[1]+23),(dst[0]-142,dst[1]+36),dst,u,GOLD,2.28,a)
            if v:dot(g,v,GOLD,6.9,a)

def draw(g,i,t,duration):
    (chart,dialogue)[i](g,t,duration)
