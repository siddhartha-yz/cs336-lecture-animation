"""Paloma's case reversal, independent scoring, and the limits of the exam ruler."""
import json
from math import cos, exp, log, pi, sin
from pathlib import Path

from cut_common import *

DATA = Path(__file__).with_name('data')
MATH = 'Latin Modern Math'
ROW_COL = (CYAN,PURPLE)
S = (321,285)
CW = 149
CH = 112
ROW_Y = (341,453)
COL_X = tuple(S[0]+CW*(j+.5) for j in range(6))
P_X = 1352
AUDIT_Y = 595
STACK_X = 1099
PITCH = 280
OUTPUT_X = (1051,1134,1217,1300)
COMPONENTS = (GOLD,CYAN,TEAL,PURPLE)
LOGIT = (log(4),log(2),0,-log(2))
EXP = tuple(exp(z) for z in LOGIT)
PROB = tuple(q/sum(EXP) for q in EXP)
INVALID = (.8,.55,.34,.16)
SUBS = ('₁','₂','₃','₄')


def q(t,a,b):
    return step(t,a,max(a+.0001,b))


def mark(g,d,phrase,frac):
    return d*g.cue(phrase,frac)


def txt(g,s,x,y,z=34,c=WHITE,a=1,align='center'):
    g.text(s,x,y,z,c,a,align=align,font=SERIF)


def ftxt(g,s,x,y,z=34,c=WHITE,a=1):
    g.text(s,x,y,z,c,a,font=MATH)


def poly(g,points,color=WHITE,stroke=2,a=1,p=1):
    """Reveal a path by arc length, not by its constituent segment count."""
    if a<=0 or p<=0:return
    if p>=1:
        g.poly(points,color,stroke,a)
        return points[-1]
    lengths=[math.hypot(b[0]-a[0],b[1]-a[1]) for a,b in zip(points,points[1:])]
    budget=sum(lengths)*p
    visible=[points[0]]
    for j,l in enumerate(lengths):
        if l==0:continue
        if l<=budget:
            visible.append(points[j+1]);budget-=l
        else:
            visible.append(tuple(mix(i,k,budget/l) for i,k in zip(points[j],points[j+1])));break
    g.poly(visible,color,stroke,a)
    return visible[-1]


def route(g,p0,p1,h,col,alpha,p=1,width=2):
    if p<=0 or alpha<=0:return
    x0,y0=p0;x1,y1=p1
    points=[(mix(x0,x1,u),mix(y0,y1,u)+h*sin(pi*u)) for u in (p*j/32 for j in range(33))]
    g.poly(points,col,width,alpha)
    return points[-1]


def alpha_group(g,a,draw):
    if a<=.002:return
    if a>=.998:
        draw();return
    c=g.c
    c.push_group();draw();c.pop_group_to_source();c.paint_with_alpha(a)


def invalid_sample(g,t,start,bars,mass_at,unit,refuse,forward):
    faded=1-q(t,forward-.83,forward+.51)
    a=q(t,start-.48,start+.54)*faded
    if not a:return
    pivot=q(t,bars-.15,bars+.95)
    claim_move=q(t,refuse-.10,refuse+1.18)
    caption=(1-pivot)*a
    square=44+62*pivot
    send=q(t,start+.57,bars-.22)
    claim_x=mix(800,685,send);claim_y=mix(413,512,send)
    g.rect(claim_x-square/2,claim_y-square/2,square,square,GOLD,alpha=caption)
    txt(g,'Submitted score',claim_x,claim_y+75,39,WHITE,caption)
    if 0<send<1:
        g.line(claim_x+20,claim_y,800,claim_y,GOLD,2.25,caption*(1-send))
    if not pivot:return
    mass=q(t,mass_at+.17,unit+1.16)
    thickness=46
    base=AUDIT_Y
    series=(513,626,739,852)
    g.line(460,base,905,base,AXIS,1.8,a*pivot)
    txt(g,'Submitted probabilities · illustration',685,190,41,WHITE,a*pivot)
    running=0
    for j,(x,p) in enumerate(zip(series,INVALID)):
        emerge=q(t,bars+.22+j*.40,bars+1.35+j*.40)
        h=PITCH*p*.78*emerge
        color=blend(COMPONENTS[j],CORAL,claim_move)
        g.rect(x-thickness/2,base-h,thickness,h,color,alpha=a*pivot)
        ftxt(g,'p'+SUBS[j],x,base+37,29,MILD,a*pivot*emerge)
        merge=q(mass,.08*j,.61+.08*j)
        if merge:
            p1=(x,base-h/2); p2=(STACK_X,base-running-PITCH*p*.78/2)
            tip=route(g,p1,p2,30,color,a*.44*(1-merge),merge,1.95)
            if tip:g.circle(*tip,4.5,color,alpha=a*(1-merge))
            g.rect(STACK_X-24,base-running-PITCH*p*.78*merge,48,PITCH*p*.78*merge,color,
                   alpha=a*pivot)
            running+=PITCH*p*.78*merge
    target=base-PITCH*.78
    gate=q(t,unit-.35,unit+.48)
    g.line(991,target,1216,target,WHITE,2.25,a*gate)
    txt(g,'1.00',1243,target,29,WHITE,a*gate,align='left')
    txt(g,'Total mass',STACK_X,667,30,WHITE,a*gate)
    ready=q(mass,.77,1)
    if ready:
        # Algebraic inconsistency appears only once components have all arrived.
        txt(g,f'{sum(INVALID):.2f}',STACK_X,base-running-32,42,CORAL,a*ready)
        x=mix(1181,1312,claim_move)
        g.check(x,base-running+17,False,25,a*ready*(.78+.22*claim_move))
    if claim_move:
        txt(g,'Unverified',685,686,37,CORAL,a*claim_move)
        extra=q(t,refuse+.89,refuse+3.14)
        if extra:
            ytop=base-running
            g.poly(((1191,target),(1202,target),(1202,mix(target,ytop,extra)),
                    (1191,mix(target,ytop,extra))),CORAL,2.18,a*extra)
            txt(g,'0.85 excess',1223,(target+ytop)/2,26,CORAL,a*q(extra,.71,1),align='left')


def integrity_art(g,alpha=1,edge=1,inputs=1,logits=1,soft=1,verify=1,loss=1,ink=1,flow=1):
    """Independent illustrative computation. Invalid submitted bars never enter this path."""
    if alpha<=.002:return
    alpha=alpha*1.0
    t_y=187
    baseline=AUDIT_Y-17
    top=(143,t_y); bl=(143,677);br=(1457,677);tr=(1457,t_y)
    poly(g,(top,bl,br,tr,top),CYAN,2.16,alpha*.87,edge)
    txt(g,'Independent forward pass',800,131,49,WHITE,alpha*ink*edge)
    txt(g,'Controlled sandbox',286,226,28,CYAN,alpha*ink*edge)
    py=(335,497)
    for j,(y,name,col) in enumerate(zip(py,('Frozen model','Fixed corpus'),(CYAN,GOLD))):
        al=alpha*inputs
        g.rect(230,y-12,24,24,col,alpha=al)
        txt(g,name,274,y,34,WHITE,al*ink,align='left')
        pather=((242,y+28),(479,y+28),(479,420),(538,420))
        p=poly(g,pather,col,2.0,al*.66,q(logits,.08,.83))
        if p and (0<flow<1):
            p=poly(g,pather,col,.4,0.001,flow)
            if p:g.circle(*p,6,col,alpha=al*sin(pi*flow)**.67)
    if logits:
        txt(g,'Logits',704,228,33,WHITE,alpha*ink*logits*(1-q(soft,.10,.33)))
        txt(g,'Exponential weights',704,228,33,WHITE,alpha*ink*logits*q(soft,.42,.78))
        bx=(581,660,739,818); center=431
        g.line(547,center,853,center,AXIS,1.34,alpha*logits)
        morph=q(soft,.18,.77)
        for j,(x,z,e) in enumerate(zip(bx,LOGIT,EXP)):
            enter=q(logits,.045*j,.77+.045*j)
            v=mix(79*z,34*e,morph)*enter
            col=COMPONENTS[j]
            g.rect(x-15,min(center,center-v),30,max(1,abs(v)),col,alpha=alpha*enter)
            ftxt(g,'z'+SUBS[j],x,548,24,MILD,alpha*ink*enter*(1-q(morph,.15,.44)))
            ftxt(g,f'{e:g}',x,467,26,WHITE,alpha*ink*enter*q(morph,.48,.88))
        p_soft=q(soft,.06,.61)
        p_norm=q(soft,.33,.91)
        if p_soft:
            poly(g,((874,490),(874,342),(935,342),(935,490)),GOLD,2.24,alpha,p_soft)
            txt(g,'Softmax',906,308,30,GOLD,alpha*ink*p_soft)
            ftxt(g,'exp(zᵢ) / Σⱼ exp(zⱼ)',756,627,27,WHITE,alpha*ink*p_norm)
        if p_norm:
            txt(g,'Probabilities',1177,228,34,WHITE,alpha*ink*p_norm)
            g.line(1005,baseline,1349,baseline,AXIS,1.35,alpha*p_norm)
            for j,(x,p,col) in enumerate(zip(OUTPUT_X,PROB,COMPONENTS)):
                enter=q(p_norm,j*.14,.65+j*.11)
                hh=PITCH*.91*p*enter
                g.rect(x-19,baseline-hh,38,hh,col,alpha=alpha*enter)
                ftxt(g,('8/15','4/15','2/15','1/15')[j],x,baseline+25,26,WHITE,alpha*enter*ink)
    if verify:
        unit=q(verify,.09,.76)
        y_bar=round(622)
        x=1024
        for j,(part,col) in enumerate(zip(PROB,COMPONENTS)):
            width=276*part
            p=q(verify,j*.15,.50+j*.15)
            g.rect(x,y_bar,width*p,9,col,alpha=alpha)
            x+=width
        ftxt(g,'Σ p = 1',1162,654,28,TEAL,alpha*q(unit,.65,1)*ink)
        g.check(1338,646,True,18,alpha*q(unit,.65,1))
    if loss:
        l=q(loss,.03,.59)
        ready=q(loss,.30,1)
        y_gold=baseline-PITCH*.91*PROB[0]
        origin=(1051,y_gold-4)
        target=((1051,390),(1354,390),(1354,487))
        col=poly(g,(origin,*target),GOLD,2.38,alpha*(.85-.55*ready),l)
        if 0<l<1 and col:g.circle(*col,5.1,GOLD,alpha=alpha*l)
        if ready:
            g.arrow(1354,455,1354,487,GOLD,2.05,alpha*ready,head=10)
        ftxt(g,'−ln p(target)',1359,515,25,GOLD,alpha*ink*ready)
        txt(g,'Four-token illustration',800,720,25,MILD,alpha*ink*q(loss,.34,.82))


class _IntegrityStage:
    def __init__(self,g,alpha):
        self.g,self.alpha=g,alpha
    def draw(self):
        integrity_art(self.g,self.alpha)


def integrity_stage(g,alpha=1):
    return _IntegrityStage(g,alpha)


def domains(g,t,d):
    if t<=0:
        from tradeoff import answer_stage
        answer_stage(g).draw();return
    if t>=d-.09:
        integrity_stage(g).draw();return
    m=lambda phrase,frac:mark(g,d,phrase,frac)
    board=m('leaderboard receives',.457)
    bars=m('bars are supposed to be probabilities',.514)
    mass_at=m('mass together',.570)
    unit=m('exactly one',.590)
    reject=m('claimed score gives you no way',.615)
    sandbox=m('controlled sandbox',.721)
    soften=m('apply softmax to the logits',.765)
    check=m('check the total probability mass',.819)
    loss=m('compute the loss yourself',.867)
    checking=m('checking the sum',.913)
    actual=m('actual model',.965)
    from score_paloma import table
    table(g,g.clock,board)
    invalid_sample(g,t,board,bars,mass_at,unit,reject,sandbox)
    start=sandbox-.45
    if t>start:
        edge=q(t,start,sandbox+1.38)
        inputs=q(t,start+.45,max(sandbox+1.90,soften-.42))
        logits=q(t,sandbox+.48,max(sandbox+2.13,soften+.07))
        soft=q(t,soften-.14,max(soften+2.68,check+.15))
        s_check=q(t,check-.08,check+2.40)
        s_loss=q(t,loss-.07,loss+2.65)
        latch=q(t,check+1.22,loss+.32)
        if 0<latch<1:
            x=mix(1024,1300,latch)
            g.rect(x-8,615,16,22,fill=WHITE,alpha=sin(pi*latch)**.74)
        flow=1 if t>actual+1.26 else q(t,(sandbox+.18 if t<check else check+.32 if t<loss else loss+.51 if t<actual-.10 else actual-.10),
                                      (soften+.21 if t<check else loss-.08 if t<loss else actual-.25 if t<actual-.10 else actual+1.26))
        integrity_art(g,q(t,start,start+.50),edge,inputs,logits,soft,s_check,s_loss,flow=flow)
        trace=q(t,checking-.19,actual+.95)
        if 0<trace<1:
            p=poly(g,((1338,646),(1423,646),(1423,201),(242,201),(242,315)),
                   CYAN,2.05,.46*sin(pi*trace)**.70,trace)
            if p:g.circle(*p,5.3,CYAN,alpha=sin(pi*trace)**.47)
        solid=q(t,actual-.12,d-.09)
        if 0<solid<1:
            a=sin(pi*solid)**.84
            tip=poly(g,((201,314),(201,365),(489,365),(489,421),(539,421)),
                     CYAN,4.4,a,solid)
            if tip:g.circle(*tip,7,CYAN,alpha=a)

TARGET=(4.32,-1.31,.115)
QUIZ_Y=430
QUIZ_X=(494,698,902,1106)
QUIZ_TOP=214
EXAM_COLOR=(CYAN,TEAL,GOLD)


def draw(g,i,t,duration):
    if i!=0:raise ValueError(i)
    domains(g,t,duration)
