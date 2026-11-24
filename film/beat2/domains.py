"""Paloma's case reversal, independent scoring, and the limits of the exam ruler."""
import json
from math import cos, exp, log, pi, sin
from pathlib import Path

from cut_common import *

DATA = Path(__file__).with_name('data')
PALOMA = json.loads((DATA/'paloma-slices.json').read_text())
MMLU = json.loads((DATA/'mmlu-overall.json').read_text())
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


def heatmap(g,t,pal,separate,pooled,exit_at):
    from tradeoff import answer_stage, example, loss_scale, WEST, EAST
    old=1-q(t,.14,1.08)
    alpha_group(g,old,lambda:answer_stage(g).draw())
    drift=q(t,.60,3.1)
    retire=q(t,exit_at+.03,exit_at+1.48)
    headings=1-q(t,exit_at-.37,exit_at+.43)
    inks=1-q(t,exit_at-.22,exit_at+.56)
    if not drift or retire>=1:return
    w=World(g)
    scale=loss_scale()[0]
    means=tuple(y+scale*m['mean_nll'] for (y,m) in zip((.67,-.797),example()['models']))
    rail=tuple(((WEST,y,.182),(EAST,y,.182)) for y in means)
    edge_retire=1-q(retire,.46,1)
    for j,y in enumerate((285,509)):
        aa,bb=(w.pos(v) for v in rail[j])
        x1,y1=aa;x2,y2=bb
        left=mix(mix(x1,S[0],drift),800,retire)
        right=mix(mix(x2,S[0]+6*CW,drift),800,retire)
        col=blend(blend(WHITE,ROW_COL[j],q(drift,.03,.36)),EDGE,q(drift,.40,1))
        g.line(left,mix(mix(y1,y,drift),413,retire),right,mix(mix(y2,y,drift),413,retire),
               col,2.42-.88*drift,edge_retire*q(t,.60,1.27),
               dash=[5.1*(1+2.1*drift),4.1*(1-q(drift,.15,.63))] if drift<.61 else None)
    before=1-q(t,pal-.67,pal+.06)
    # The first two slices emerge as independent probes, before the named data.
    for j,(ix,start,col,kind) in enumerate(((4,2.51,CYAN,'Web'),(2,5.07,GOLD,'Papers'))):
        f=q(t,start,start+1.45)
        if not f or not before:continue
        x=COL_X[ix]
        yy=mix(510,306,f)
        txt(g,kind,x,260,29,col,before*q(f,.67,1))
        g.rect(x-26,yy,52,510-yy,col,alpha=before*.22*q(f,.04,.80))
        g.line(x-32,yy,x+32,yy,col,3.55,before*.74)
        g.line(x,510,x,yy,col,4.15,before*.91)
        for yy0 in (341,453):
            if yy<yy0:
                g.circle(x,yy0,5,col,alpha=before*q(f,1-(yy0-306)/204,1))
    # Carry the result of the second probe back across the two rails.
    across=q(t,3.76,5.30)
    if 0<across<1 and before:
        for y in ROW_Y:
            x=mix(COL_X[4],COL_X[2],across)
            g.line(x,y-12,x,y+12,CYAN,3.25,before*sin(pi*across)*.88)
            g.circle(x,y,5.5,CYAN,alpha=before*sin(pi*across)*.65)
    to_pair=q(t,6.42,max(7.77,pal-.31))
    if 0<to_pair<1 and before:
        for j,y in enumerate(ROW_Y):
            tip=route(g,(COL_X[2],y),(COL_X[4],y),(-1)**j*22,ROW_COL[j],
                      before*sin(pi*to_pair)**.64,to_pair,1.88)
            if tip:g.circle(*tip,4.7,ROW_COL[j],alpha=before*sin(pi*to_pair)**.46)
    name_a=q(t,pal-.02,pal+.68)*headings
    txt(g,'Paloma',770,155,65,WHITE,name_a)
    txt(g,'Per-token perplexity',770,217,34,WHITE,name_a)
    for j,(label,y) in enumerate(zip(PALOMA['models'],ROW_Y)):
        row_a=q(t,pal+.25+j*.24,pal+1.25+j*.24)*headings
        txt(g,label,272,y,39,ROW_COL[j],row_a,align='right')
    matrix=q(t,pal+.57,separate+2.68)
    divide=q(t,pal+1.05,separate-.08)
    if 0<divide<1:
        for j in range(7):
            r=q(divide,j*.074,.41+j*.076)
            if r:
                x=S[0]+CW*j
                g.line(x,285,x,mix(285,509,r),WHITE,2.8,.42*r*(1-q(divide,.76,1)))
    mid_a=q(matrix,.15,.72)*(1-q(retire,.27,.76))
    if mid_a:
        g.line(mix(S[0],800,retire),397,mix(S[0]+6*CW,800,retire),397,EDGE,1.55,mid_a)
    for j,dom in enumerate(PALOMA['domains']):
        delay=(.11,.51,.86,1.12,1.42,1.75)[j]
        onset=separate-.31+delay
        att=q(t,onset+.30,onset+1.30)*(1-q(t,onset+1.70,onset+2.94))
        look_start=max(separate+2.21,pooled-4.15)+j*.56
        scan=q(t,look_start,look_start+.42)*(1-q(t,look_start+.79,look_start+1.28))
        a=q(t,onset,onset+.91)
        part=q(t,onset-.55,onset+.88)
        if part<=0:continue
        x0=S[0]+CW*j
        x=COL_X[j]
        dx=mix(x0,800,retire); y0=mix(S[1],405,retire)
        g.line(dx,y0,dx,mix(y0,mix(509,423,retire),part),EDGE,1.48,
               (1-q(retire,.30,.75))*part)
        if j==5:
            g.line(mix(x0+CW,800,retire),y0,mix(x0+CW,800,retire),
                   mix(y0,mix(509,423,retire),part),EDGE,1.48,(1-q(retire,.30,.75))*part)
        txt(g,dom['name'],x,260,29,WHITE,a*headings)
        for row,y in enumerate(ROW_Y):
            vals=dom['values']
            c=TEAL if vals[row] < vals[1-row] else CORAL
            z=1-retire
            g.rect(mix(x,800,retire)-(CW/2-1)*z,mix(y,413,retire)-(CH/2-1)*z,
                   (CW-2)*z,(CH-2)*z,c,alpha=a*(.17+.19*max(att,scan))*z)
            # A short colored sample is the cell's rank in this column, not a global scale.
            g.rect(x-38,y+32,76*max(att,scan)*z,2.2,c,alpha=.87*a*inks)
            txt(g,f'{vals[row]:.2f}',x,y,43,WHITE,a*inks)
    aggregate=q(t,pooled-.11,pooled+2.42)
    finish=q(t,pooled+1.76,pooled+2.92)
    if aggregate and inks:
        l=S[0]+6*CW+47;r=1480
        center=(l+r)/2
        for row,y in enumerate(ROW_Y):
            for i,x in enumerate(COL_X):
                a=q(aggregate,.045*i,.58+.06*i)
                if not a:continue
                end=(l-10,y-9+3*i)
                src=(x,y+40)
                c=ROW_COL[row]
                p=route(g,src,end,15+(row-.5)*19+4*i,c,
                         inks*(1-q(a,.62,1))*.49,a,1.38)
                if p:g.circle(*p,3.5,c,alpha=inks*(1-q(a,.86,1)))
            g.rect(l,y-CH/2+5,r-l,CH-10,ROW_COL[row],alpha=.16*finish*inks)
            g.line(l,y-CH/2+4,l,y+CH/2-4,ROW_COL[row],2.08,finish*inks)
            txt(g,f"{PALOMA['aggregate']['values'][row]:.2f}",center,y,45,WHITE,finish*inks)
        txt(g,'Equal-domain PPL',center,260,25,WHITE,finish*headings)
        ftxt(g,'exp(mean log PPL)',center,555,23,MILD,finish*headings)
        compare=q(t,pooled+2.9,max(pooled+4.35,exit_at-.45))
        if 0<compare<1:
            for row,y in enumerate(ROW_Y):
                a=sin(pi*compare)**.88*inks
                g.line(l+22,y+33,l+22+(r-l-44)*compare,y+33,ROW_COL[row],2.15,a)
    if name_a:
        leg=q(t,separate+.38,separate+1.61)*headings
        g.rect(329,564,15,15,TEAL,alpha=leg)
        txt(g,'Lower within column',352,571,24,MILD,leg,align='left')
        g.rect(615,564,15,15,CORAL,alpha=leg)
        txt(g,'Higher within column',639,571,24,MILD,leg,align='left')
        txt(g,'Shared GPT-2 tokenizer · 1.3B class · 300B training tokens',
            800,646,26,MILD,name_a)
        txt(g,'Paloma validation · xLSTM study, Tables 8 and 10',800,681,23,MILD,name_a)
    if 0<retire<1:
        g.rect(800-22*retire,413-22*retire,44*retire,44*retire,GOLD,
               alpha=q(retire,.52,1)*.90)


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
    pal=m('Paloma',.177)
    sep=m('own column',.231)
    pooled=m('pooled score',.374)
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
    heatmap(g,t,pal,sep,pooled,board-.97)
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

def outline(g,x,y,w,h,col,alpha=1,progress=1):
    pp=((x-w/2,y-h/2),(x+w/2,y-h/2),(x+w/2,y+h/2),(x-w/2,y+h/2),(x-w/2,y-h/2))
    poly(g,pp,col,2.18,alpha,progress)


def quiz(g,t,d,start,left,answer,exam,known,grade,subjects,ruler):
    from tradeoff import answer_strip, ANSWER_POINT, example
    w=World(g); tip=w.pos(ANSWER_POINT)
    reveal=q(t,start-.44,start+1.37)
    dim=q(t,answer-.60,answer+.64)
    fade=q(t,answer+.32,exam+.15)
    collect=q(t,answer+.32,exam+.68)
    whole=q(t,answer+.21,exam-.12)
    split=q(t,exam-.05,exam+1.71)
    to_subject=q(t,subjects-.03,subjects+2.95)
    alpha=reveal*(1-fade)
    if alpha:
        alpha_group(g,alpha,lambda: (answer_strip(w,opacity=1,prefix=mix(1,.15,dim)),w.draw()))
    digit=1-q(t,exam-.51,exam+.12)
    progress=q(t,left-.52,answer+.57)
    if reveal and fade<.14 and progress:
        a=.92*reveal*(1-q(progress,.86,1))*(1-.52*dim)
        sx=mix(235,tip[0],progress)
        y=tip[1]-49
        g.line(sx-38,y,sx+38,y,GOLD,3.87,a)
        g.circle(sx,y,5.6,GOLD,alpha=a)
        g.line(sx,y+7,sx,y+34,GOLD,2.5,a*.91)
        g.line(236,y+72,sx,y+72,GOLD,2.10,a*.73)
    if dim and to_subject<1:
        w0=mix(76,132,split);h0=mix(46,108,split)
        midx=mix(tip[0],QUIZ_X[2],collect)
        midy=mix(tip[1],QUIZ_Y,collect)
        focused_a=max(dim*(1-fade),fade)*(1-to_subject)
        for j,x in enumerate(QUIZ_X):
            f=q(split,j*.04,.73+j*.076)
            if not f and j!=2:continue
            px=midx if j==2 else mix(midx,x,f)
            py=(midy if j==2 else mix(midy,QUIZ_Y,f))-to_subject*(40+9*j)
            box_a=(focused_a if j==2 else fade*f)*(1-q(to_subject,.35,.99))
            col=GOLD if j==2 else WHITE
            outline(g,px,py,w0*(1-.84*to_subject),h0*(1-.71*to_subject),
                    col,box_a,q(split,0,.81) if j!=2 else 1)
            t_alpha=q(f,.33,1)*fade*(1-q(to_subject,.0,.30))
            option=('one','three',example()['answer'].strip(),'four')[j]
            txt(g,'ABCD'[j],px,py-16,33,col,t_alpha)
            txt(g,option,px,py+19,24,col,t_alpha)
            if j==2 and split<.58:
                retain=whole*(1-q(split,.12,.58))
                txt(g,option,px,py,33,GOLD,retain)
            if j==2 and not split:
                g.rect(px-w0/2,py-h0/2,w0,h0,GOLD,alpha=.105*dim*digit)
    grading=q(t,grade-.12,grade+1.75)
    known_a=q(t,known-.03,known+.92)
    if known_a and to_subject<.7:
        a=(1-q(to_subject,0,.54))*known_a
        kx=QUIZ_X[2]
        g.rect(kx-27,QUIZ_TOP-26,54,52,stroke=GOLD,width=2.0,alpha=a)
        txt(g,'C',kx,QUIZ_TOP,31,GOLD,a)
        txt(g,'Answer key',kx-45,QUIZ_TOP,30,WHITE,a,align='right')
        r=q(grading,.18,.84)
        if r:
            end=mix(QUIZ_TOP+37,QUIZ_Y-66,r)
            g.arrow(kx,QUIZ_TOP+37,kx,end,GOLD,2.38,a,head=11)
            if r<1:g.circle(kx,end,4,GOLD,alpha=a)
        if grading>.62:
            passed=q(grading,.62,.96)
            g.check(kx,547,True,25,a*passed)
            txt(g,'1 / 1',kx+55,547,33,TEAL,a*passed,align='left')
    if to_subject:
        arrange=q(t,ruler-.44,ruler+1.75)
        rg=1-q(arrange,.14,.70)
        a=q(to_subject,.08,.71)*rg
        txt(g,'57 subjects',800,236,58,WHITE,a)
        for j in range(MMLU['subjects']):
            ix=j%19;iy=j//19
            gt=q(to_subject,.011*j,.37+.010*j)
            if not gt:continue
            x0,y0=QUIZ_X[j%4],QUIZ_Y
            px=mix(x0,247+61.3*ix,gt)
            py=mix(y0,365+73*iy,gt)
            x=mix(px,258,arrange)
            # The subjects are count marks. Their equal strokes carry no scores.
            y=mix(py,645-8.22*j,arrange)
            h=mix(3,33,gt)*(1-.88*arrange)
            swatch=CYAN if (j%7)!=0 else GOLD
            if arrange>.002:swatch=blend(swatch,AXIS,arrange)
            g.line(x,y-h/2,x,y+h/2,swatch,2.8*q(gt,0,.76),gt*rg)


def score_chart(g,t,d,ruler,steps,crowd,saturation):
    arrival=q(t,ruler+.12,ruler+1.94)
    close=q(t,crowd+.31,max(crowd+2.6,saturation+.62))
    if not arrival:return
    left=256;right=1376;top=214;bottom=642
    base=mix(0,70,close)
    x_vals=(535,851,1158)
    def y_for(p):
        return bottom-(bottom-top)*(p-base)/(100-base)
    cap_track=q(t,ruler+1.35,steps+.27)
    lower=q(arrival,0,.86)
    poly(g,((left,bottom),(left,top),(right,top)),AXIS,2.35,arrival,lower)
    poly(g,((left,bottom),(right,bottom)),AXIS,1.54,arrival*.75,q(arrival,.24,1))
    if cap_track:
        b=q(cap_track,0,.62)
        # The cap isn't a score; keep the physical upper bound fixed as the scale expands.
        g.line(left,top,mix(left,right,b),top,WHITE,2.84,arrival*max(.26,b))
        txt(g,'100%',left-22,top,28,WHITE,arrival*b,align='right')
    for level in (0,25,50,70,75,80,90):
        yf=y_for(level)
        aa=arrival*(1-q(close,.12,.38)) if level in (0,25,50) else (
            arrival*q(close,.40,.85) if level in (70,80,90) else arrival*(1-q(close,.55,.91)))
        if aa<=.002 or yf<top+9 or yf>bottom+.001:continue
        g.line(left-8,yf,left,yf,AXIS,1.43,aa*.86)
        txt(g,f'{level}%',left-25,yf,25,MILD,aa,align='right')
    txt(g,'MMLU',800,124,63,WHITE,arrival)
    txt(g,'Overall accuracy · 57 subjects',800,176,30,MILD,arrival)
    txt(g,'OpenAI simple-evals · zero-shot',right,707,25,MILD,arrival,align='right')
    series=MMLU['scores']
    ypast=None
    for j,(r,x,c) in enumerate(zip(series,x_vals,EXAM_COLOR)):
        cue=(steps-.14,steps+1.20,crowd-.36)[j]
        f=q(t,cue,cue+1.44)
        if not f:continue
        score=r['accuracy_percent']
        yf=y_for(score)
        origin=mix(bottom,yf,f)
        # Segments measure actual headroom on the single percent scale.
        g.line(x,bottom,x,origin,c,2.65,arrival*f*.74)
        if ypast is not None:
            px,py=ypast
            route(g,(px,py),(x,yf),-5,MILD,arrival*.48*f,q(f,.38,.98),1.52)
        if f>.04:
            g.circle(x,origin,8.8,c,alpha=arrival*f)
        label_a=q(f,.55,1)
        txt(g,r['short'],x,bottom+37,30,WHITE,arrival*label_a)
        txt(g,f'{score:.1f}%',x+20,yf-31,32,c,arrival*label_a,align='left')
        ypast=(x,yf)
    alert=q(t,saturation-.06,saturation+.95)
    if alert:
        # Make the remaining headroom visible as a literal segment on the same ruler.
        at=y_for(series[-1]['accuracy_percent'])
        x=1371
        h=mix(top,at,alert)
        g.poly(((x-11,top),(x,top),(x,h),(x-11,h)),CORAL,2.56,alert)
        txt(g,'Headroom',x-8,(top+h)/2,27,CORAL,alert,align='right')
        if t>=saturation+.72:
            ring=q(t,saturation+.72,saturation+2.0)
            rr=8.8+23*ring
            g.circle(x_vals[-1],at,rr,stroke=GOLD,width=1.45,alpha=sin(pi*ring)**2)
        txt(g,'Benchmark saturation',741,755,40,WHITE,q(t,saturation+.23,saturation+1.18))


def exams(g,t,d):
    if t<=0:
        integrity_stage(g).draw();return
    m=lambda phrase,frac:mark(g,d,phrase,frac)
    alignment=m('units aligned',.035)
    domains_split=m('domains split out',.112)
    verified=m('probabilities verified',.164)
    stream=m('whole stream of text',.209)
    hard=m('a hard question',.252)
    spot=m('where the answer matters',.331)
    exam=m('standardized exams',.390)
    known=m('a known answer',.458)
    grade=m('automatic grading',.496)
    subjects=m('dozens of subjects',.560)
    ruler=m('different ruler',.607)
    steps=m('clear steps upward',.743)
    crowd=m('strongest models crowded',.832)
    satur=m('benchmark saturation',.941)
    erase=q(t,stream-.48,stream+1.24)
    if erase<1:
        ink=1-q(t,stream-1.31,stream-.22)
        al=1-erase
        integrity_art(g,alpha=al,ink=ink)
        for j,(a,x,y,c,to) in enumerate(((alignment,232,335,CYAN,382),
                                        (domains_split,232,497,GOLD,430),
                                        (verified,1053,642,TEAL,1297))):
            p=q(t,a-.07,a+1.6)
            if 0<p<1:
                tip=mix(x,to,p)
                g.line(x,y-25,tip,y-25,c,4.00,al*sin(pi*p)**.51)
                g.circle(tip,y-25,6.2,c,alpha=al*sin(pi*p)**.66)
        if erase:
            w=World(g);target=w.pos(TARGET)
            ys=target[1]
            for j,x in enumerate(OUTPUT_X):
                p=q(erase,.09*j,.63+.105*j)
                if not p:continue
                tip=route(g,(x,AUDIT_Y-17),(mix(249,target[0],j/3),ys),46+j*9,COMPONENTS[j],
                          .47*sin(pi*p)**2,p,1.48)
                if tip:
                    g.rect(tip[0]-4,tip[1]-4,8,8,COMPONENTS[j],alpha=sin(pi*p)**.8)
    quiz(g,t,d,stream,hard,spot,exam,known,grade,subjects,ruler)
    score_chart(g,t,d,ruler,steps,crowd,satur)


def draw(g,i,t,duration):
    (domains,exams)[i](g,t,duration)
