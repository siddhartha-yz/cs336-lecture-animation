"""One known joint; then one real same-token reversal at the answer position."""
from cut_common import *
from pathlib import Path
from functools import lru_cache
import json
import math

CASE=Path(__file__).with_name('data')/'tradeoff_case.json'
AX=4.32
TOKEN_ROW=-1.31
ANSWER_POINT=(AX,TOKEN_ROW,.115)
ANSWER_SIZE=(.59,.36)
WEST=-4.47
EAST=4.71
MODELC=(CYAN,PURPLE)

def a(x,lo,hi):return step(x,lo,hi)
def off(x,lo,hi):return 1-a(x,lo,hi)
def wave(x,lo,hi,lo2,hi2):return a(x,lo,hi)*off(x,lo2,hi2)

@lru_cache(maxsize=1)
def example():
    p=json.loads(CASE.read_text(encoding='utf-8'))
    i=p['answer_index'];m0,m1=p['models']
    if not (i==len(p['tokens'])-1 and m0['ppl']<m1['ppl'] and
            m0['top'][0]['id']!=p['token_ids'][i] and m1['top'][0]['id']==p['token_ids'][i]):
        raise ValueError('The rendered fixture must retain the actual mean/answer rank reversal.')
    return p

def box(w,x,y,z,ww,hh,c=GOLD,op=1,width=1.5,fill=0):
    poly=((x-ww/2,y-hh/2,z),(x+ww/2,y-hh/2,z),
          (x+ww/2,y+hh/2,z),(x-ww/2,y+hh/2,z))
    if fill:w.face(poly,c,op,fill,0)
    if width:w.path((*poly,poly[0]),c,width,op)

def label_tok(s):
    return s.strip() or '␠'

def x_positions():
    n=len(example()['tokens'])
    return tuple(mix(-4.12,AX,j/(n-1)) for j in range(n))

def answer_strip(w,opacity=1,prefix=1,*,appear=1,y=TOKEN_ROW):
    """Shared target identity, with optional dimming of the preceding words."""
    e=example();coords=x_positions();n=len(coords)
    for j,(x,s) in enumerate(zip(coords,e['tokens'])):
        k=a(appear,.025*j,.38+.025*j)
        target=j==n-1
        op=opacity*k*(1 if target else prefix)
        if op<=.002:continue
        if target:box(w,x,y,.115,*ANSWER_SIZE,GOLD,op,1.55)
        # Whole labels arrive in the settled slots; raw UTF-8/space stays in JSON.
        size=31 if target else min(24,28-(len(label_tok(s))-4)*1.25)
        w.text(label_tok(s),(x,y,.151),size,GOLD if target else WHITE,op)
    return w

# Eight illustrative sequence outcomes. Each curve is an envelope through
# discrete masses. Interpolating two normalized vectors preserves total mass.
TRUTH=(.130,.050,.095,.138,.343,.087,.052,.105)
START=(.240,.030,.160,.048,.171,.230,.065,.056)
CENTERS=tuple(mix(-4.63,4.55,j/7) for j in range(8))
QIDS=(3,4,5)
QANS=('Dry','Light rain','Heavy rain')
QPROBS=tuple(TRUTH[j]/sum(TRUTH[k] for k in QIDS) for j in QIDS)
JOINT_Y=-.72

def smoothcurve(pts,N=9):
    ctx=[pts[0],*pts,pts[-1]];ret=[]
    for j in range(1,len(ctx)-2):
        p0,p1,p2,p3=ctx[j-1:j+3]
        for k in range(N):
            t=k/N;s=t*t
            x=mix(p1[0],p2[0],t)
            y=.5*((2*p1[1])+(-p0[1]+p2[1])*t
                  +(2*p0[1]-5*p1[1]+4*p2[1]-p3[1])*s
                  +(-p0[1]+3*p1[1]-3*p2[1]+p3[1])*s*t)
            ret.append((x,max(JOINT_Y-.016,y),p1[2]))
    return (*ret,pts[-1])

def incoming(g,u):
    from opening2 import transfer_stage
    if u<=0:
        transfer_stage(g).draw();return
    old=off(u,.006,.047)
    if old>.002:
        c=g.c;c.save()
        c.push_group(); transfer_stage(g).draw(); c.pop_group_to_source()
        c.paint_with_alpha(old)
        c.restore()
    w=World(g)
    k=a(u,.011,.045)
    if k:
        p=(0,-.45,.14)
        r=mix(.095,.21,a(u,.013,.101))
        path=tuple((p[0]+r*math.cos(j*math.tau/48),p[1]+r*math.sin(j*math.tau/48),p[2]) for j in range(49))
        w.path(path,GOLD,1.85,k*off(u,.088,.154),progress=a(u,.015,.080))
    trail=a(u,.054,.139)
    if trail:
        p0=(0,-.45,.20);p1=(-1.54,-.67,.17);p2=(-3.29,-.56,.17);p3=(-4.83,JOINT_Y,.17)
        w.curve(p0,p1,p2,p3,GOLD,1.75,off(u,.149,.202),progress=trail)
        w.dot(bezier(p0,p1,p2,p3,trail),GOLD,.044,off(u,.143,.191))
    thought=0  # score label stays with its chart, never rides onto the new axis
    if thought:
        w.text('PPL 17.48',(-3.94,JOINT_Y+.34,.18),26,GOLD,thought,align='left')
    w.draw()

def bezier(p0,p1,p2,p3,k):
    q=1-k
    return add(add(mul(p0,q**3),mul(p1,3*q*q*k)),add(mul(p2,3*q*k*k),mul(p3,k**3)))

def joint(g,u):
    tip=a(u,.091,.158)
    al=tip*off(u,.488,.613)
    if al<=.002:return
    # Group these particular answers; a conditional is a subset then normalize.
    gather=a(u,.311,.385)
    shove=a(u,.338,.439)
    p=World(g)
    y0=JOINT_Y+.33*a(u,.476,.571)
    def hval(v):return y0+5.65*v
    xs=tuple(mix(x,-2.48+.63*j,shove) for j,x in enumerate(CENTERS))
    true=tuple((x,hval(q),.128) for x,q in zip(xs,TRUTH))
    starting=tuple((x,hval(q),.143) for x,q in zip(xs,START))
    con=a(u,.229,.342)
    changed=tuple(vlerp(x,y,con) for x,y in zip(starting,true))
    tvis=a(u,.152,.217)*al
    mvis=a(u,.195,.238)*al
    xx0=mix(-4.82,-2.62,shove);xx1=mix(4.73,2.08,shove)
    p.path(((xx0,y0,.08),(xx1,y0,.08)),MILD,1.58,al*.83,progress=tip,arrow=True)
    p.text('Toy joint',(xx0,y0+2.26,.16),31,WHITE,tvis,align='left')
    p.path(smoothcurve(true),WHITE,3.03,tvis,progress=a(u,.152,.229))
    p.path(smoothcurve(changed),CYAN,2.76,mvis*(1-.37*con),progress=a(u,.201,.260))
    p.text('True joint',(xx0,y0+1.711,.17),26,WHITE,tvis,align='left')
    p.text('Model joint',(xx0,y0+1.403,.17),26,CYAN,mvis,align='left')
    p.text('possible outcomes',(mix(3.68,1.07,shove),y0-.245,.13),22,MILD,tvis)
    for j,(x,v) in enumerate(zip(xs,TRUTH)):
        s=1 if j in QIDS else 1-.64*gather
        p.segment((x,y0,.095),(x,hval(v),.095),WHITE,1.03,tvis*s*.26)
        p.dot((x,hval(v),.180),GOLD if j in QIDS and gather>.48 else WHITE,.030,tvis*s)
    if gather:
        span=(xs[QIDS[0]]-.155,xs[QIDS[-1]]+.155)
        p.path(((span[0],y0-.111,.133),(span[0],y0-.228,.133),
                (span[1],y0-.228,.133),(span[1],y0-.111,.133)),
               GOLD,1.88,gather*al,progress=gather)
        p.text('Cloudy morning',((span[0]+span[1])*.5,y0-.396,.160),24,GOLD,
               a(u,.350,.388)*al)
    inference=a(u,.371,.458)
    if inference:
        y=.82;x=3.40
        p.text('P(answer | question)',(x,1.81,.18),32,WHITE,inference*al,font='math')
        basis=.885
        for j,(name,val) in enumerate(zip(QANS,QPROBS)):
            y=basis-j*.66
            k=a(u,.374+j*.012,.445+j*.011)
            v=al*k
            q0=(xs[QIDS[j]],y0-.199,.160);q3=(2.08,y-.263,.155)
            q1=(q0[0]+.85,y0-.18,.153);q2=(q3[0]-.8,q3[1],.153)
            p.curve(q0,q1,q2,q3,GOLD,1.24,v*.58,progress=k)
            box(p,2.14+1.36*val*k,y-.262,.126,2.72*val*k,.072,
                GOLD if j==1 else CYAN,v,0,1.)
            p.text(name,(2.10,y,.169),25,WHITE,v,align='left')
            p.text(f'{100*val:.1f}%',(4.78,y,.174),23,GOLD if j==1 else WHITE,v,align='right')
        decision=a(u,.448,.492)
        guide=wave(u,.420,.431,.485,.496)
        if guide:
            # Inspect the normalized answer masses before choosing the largest.
            pos=2.99*a(u,.421,.484)
            for j,val in enumerate(QPROBS):
                focus=clamp(1-abs(pos-j-.45)/.68)*guide*al
                if focus:
                    yy=basis-j*.66-.263
                    xx=2.14+2.72*val
                    p.segment((2.14,yy-.087,.197),(xx,yy-.087,.197),GOLD,2.47,focus)
                    p.dot((xx,yy,.202),GOLD,.046,focus)
        if decision:
            p.text('Most likely',(3.27,-1.209,.189),25,TEAL,decision*al)
            p.mark((4.19,-1.205,.197),True,.105,decision*al)
    p.draw()

def loss_scale():
    c=example();vals=[z for m in c['models'] for z in m['nll']]
    upper=max(1.,max(vals))
    ceil=math.ceil(upper/2)*2
    return 1.035/ceil,ceil

def loss_stage(w,u,opacity=1,settled=False):
    """One shared unit; each bar is the reference token's -ln p in nats."""
    c=example();xs=x_positions();n=len(xs)
    k=1 if settled else a(u,.689,.794)
    avg=1 if settled else a(u,.791,.860)
    target=1 if settled else a(u,.862,.915)
    verdict=1 if settled else a(u,.886,.938)
    reveal=1 if settled else a(u,.661,.760)
    inv=1 if settled else a(u,.665,.725)
    pscale,ceiling=loss_scale()
    ys=(.67,-.797)
    o=opacity
    w.text('One arithmetic sequence',(-4.48,2.355,.161),34,WHITE,o*inv,align='left')
    w.text('Reference token loss · −ln p · nats',(-4.48,1.965,.161),24,MILD,o*k,align='left')
    # The target strip is recognizably the same row inherited by Chunk 4.
    answer_strip(w,o,1,appear=reveal)
    for r,(m,col,y0) in enumerate(zip(c['models'],MODELC,ys)):
        lead=a(u,.716+r*.015,.753+r*.016) if not settled else 1
        ymean=y0+pscale*m['mean_nll']
        nll=m['nll']
        name='Base' if '· base' in m['name'] else 'Instruct'
        nm='A' if r==0 else 'B'
        w.text(nm+' · '+name,(-4.85,y0+.327,.170),24,col,o*lead,align='right')
        w.segment((WEST,y0,.107),(EAST,y0,.107),EDGE,1.26,o*lead)
        for tick in (0,ceiling/2,ceiling):
            yy=y0+tick*pscale
            w.segment((WEST-.042,yy,.124),(WEST+.068,yy,.124),MILD,1.21,o*lead*.86)
            w.text(f'{tick:.0f}',(WEST-.117,yy,.146),20,MILD,o*lead,align='right')
        for j,(x,h_raw) in enumerate(zip(xs,nll)):
            appear=1 if settled else a(u,.739+.003*j+.006*r,.782+.004*j+.004*r)
            if j==n-1:appear*=.32+.68*target
            b=pscale*h_raw*appear
            if b<=.0001:continue
            focus=0 if settled else wave(u,.763+j*.003,.788+j*.004,.825+j*.002,.858+j*.001)
            if j==n-1:
                tc=GOLD if r==1 else blend(col,CORAL,target)
                width=mix(.183,.30,target)
            else:
                tc=blend(col,WHITE,.33*focus);width=.183+.022*focus
            box(w,x,y0+b*.5,.131,width,b,tc,o*appear*(.94+.06*focus),0,1.)
        # Equal weights: same width contribution at each of the n positions.
        if avg:
            w.path(((WEST,ymean,.182),(EAST,ymean,.182)),WHITE,1.54,o*avg*.94,
                   progress=avg,dash=[5.1,4.1])
            if not settled and avg<.995:
                w.dot((mix(WEST,EAST,avg),ymean,.202),WHITE,.031,o*avg)
        pprob=m['probabilities'][-1]
        if target:
            w.text(f'{100*pprob:.1f}%',(AX+.45,y0+.775,.191),22,GOLD,o*target,align='left')
            if not settled:
                t=wave(u,.859+r*.008,.884+r*.008,.916+r*.005,.948+r*.005)
                if t:
                    p0=(AX,y0+pscale*nll[-1]+.058,.196)
                    p1=(AX+.097,y0+.405,.193)
                    p2=(AX+.21,y0+.779,.196)
                    p3=(AX+.385,y0+.773,.196)
                    q=a(u,.858+r*.007,.904+r*.008)
                    w.curve(p0,p1,p2,p3,GOLD,1.5,t*.82,progress=q)
                    w.dot(bezier(p0,p1,p2,p3,q),GOLD,.036,t)
        if verdict:
            raw=label_tok(m['top'][0]['token'])
            hit=1 if settled else a(u,*( (.927,.964) if r else (.884,.926) ))
            w.text(raw,(AX+.49,y0+.458,.208),27,TEAL if r else CORAL,o*hit,align='left')
            w.mark((AX+1.37,y0+.461,.206),bool(r),.107,o*hit)
        show_avg=avg*a(u,.814,.875) if not settled else 1
        if show_avg:
            # Positioned just above the corresponding mean line, not at the top-1 marker.
            w.text(f'PPL  {m["ppl"]:.2f}',(-3.99,ymean+.130,.206),22,TEAL if not r else WHITE,
                   o*show_avg,align='left')
    if target:
        w.path(((AX-.213,TOKEN_ROW+.251,.192),(AX+.213,TOKEN_ROW+.251,.192)),
               GOLD,1.61,o*target)
        w.text(f'P({c["answer"]})',(AX+.45,1.96,.181),21,GOLD,o*target,align='left')
    if verdict:
        w.text('Top-1 guess',(AX+.45,2.254,.163),21,WHITE,o*verdict,align='left')
        w.text('SmolLM2-135M · base & instruct',(-4.48,-1.795,.146),22,MILD,
               o*verdict,align='left')
    return w

def answer_stage(g):
    return loss_stage(World(g),1.,settled=True)

def average_weights(g,u):
    # Before bars appear, show exactly one unit entering the mean per token.
    v=wave(u,.554,.601,.713,.757)
    if v<=.002:return
    p=World(g);xs=x_positions()
    yy=-.111
    for j,x in enumerate(xs):
        stagger=.0038*j
        k=a(u,.561+stagger,.629+stagger)
        box(p,x,yy,.131,.217,.217,WHITE,v*k,1.10,.36)
        run=a(u,.631+stagger,.699+stagger)
        if 0<run<1:
            y=mix(yy,-.62,run)
            p.dot((x,y,.165),GOLD,.030,v*k*off(run,.79,1.))
    q=a(u,.595,.712)
    p.path(((WEST,-.63,.112),(EAST,-.63,.112)),WHITE,1.85,v*q,progress=q)
    p.text('1 / T per target token',(0,.29,.166),30,WHITE,v*a(u,.601,.645),font='math')
    p.draw()

def clock(g,t,duration):
    """Anchor to the existing read, including the intentional question hold."""
    end=clamp((g.speech if g.speech>0 else duration-1.2)/duration,.78,.998)
    p1=g.part(1,.212)
    wait0=max(.075,p1-1.65/duration)
    plan=(
         (g.cue('driving it down',.080),.085),
         (wait0,.147),(p1,.170),
         (g.cue('true joint distribution',.249),.230),
         (g.cue('conditioning on a question',.321),.332),
         (g.cue('with a rule',.411),.424),
         (g.part(2,.486),.495),
         (g.cue('the same weight',.570),.585),
         (g.cue('a predictable bit of grammar',.644),.669),
         (g.part(3,.731),.746),
         (g.cue('saves enough loss',.799),.804),
         (g.cue('at the answer slot',.855),.862),
         (g.cue('the other model loses',.92),.930),
    )
    now=t/duration
    if now>=end:return 1.
    t0=u0=0.
    for i,(p,u1) in enumerate(plan):
        t1=clamp(p,t0+.004,end-.005*(len(plan)-i))
        if now<=t1:
            return mix(u0,u1,clamp((now-t0)/(t1-t0)))
        t0,u0=t1,u1
    return mix(u0,1.,clamp((now-t0)/(end-t0)))

def draw(g,i,t,duration):
    if t<=0:incoming(g,0);return
    u=clock(g,t,duration)
    if u>=1.:
        answer_stage(g).draw();return
    if u<.208:incoming(g,u)
    joint(g,u)
    average_weights(g,u)
    if u>.660:
        w=loss_stage(World(g),u)
        stop=g.speech if g.speech>0 else duration-1.2
        run=a(t,stop-4.72,stop-.11)
        trace=wave(t,stop-4.68,stop-4.15,stop-.35,stop)
        if trace:
            # The answer box remains the source of the last, single-decision
            # check, not of the unweighted whole-sequence verdict.
            path=((AX+.306,TOKEN_ROW-.005,.212),(5.26,-1.29,.211),
                  (5.52,-.973,.212),(AX+1.36,-.413,.214))
            w.curve(*path,TEAL,2.25,trace*.87,progress=run)
            w.dot(bezier(*path,run),TEAL,.050,trace)
        w.draw()
