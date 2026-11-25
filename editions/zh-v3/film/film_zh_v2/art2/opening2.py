"""A continuous route from the eight-token frame to three zero-shot tests."""
from cut_common import *
from ink import measured_token_stage
import bisect
from math import log,log2,exp,prod
R=Path(__file__).resolve().parent
P=json.loads((R/'token_packet.json').read_text())
ROWS=token_data()
PS=tuple(P['probabilities'])
LOSSES=tuple(-log(p) for p in PS)
MEAN=sum(LOSSES)/len(LOSSES)
JOINT=prod(PS)
GAP=.36

def smooth(t,a,b):
    return step(t,a,max(a+.015,b))

def word(g,d,n,at,occ=0):return g.cue(n,at/d,occ)*d
def pulse(t,a,b):return math.sin(math.pi*clamp((t-a)/(b-a)))
def area(w,x,y,wd,ht,col,al=1.,solid=False,z=.105):
    q=((x-wd*.5,y-ht*.5,z),(x+wd*.5,y-ht*.5,z),(x+wd*.5,y+ht*.5,z),(x-wd*.5,y+ht*.5,z))
    if solid:w.face(q,col,al,1.,0)
    else:w.path((*q,q[0]),col,1.55,al)
def focus_token(w,j,al):
    x=token_positions()[j]
    area(w,x,-.08,.98,1.45,CYAN,.24*al,True,z=.051)
    area(w,x,TOKEN_Y,.98,TOKEN_HEIGHT,GOLD,al,z=.127)
    w.segment((x-.30,TOKEN_Y-.28,.138),(x+.30,TOKEN_Y-.28,.138),GOLD,2.6,al)

def rare_word_ruler(w,q):
    """Read the cat bar without falsely giving an invisible mass a minimum height."""
    if q<=.001:return
    j=2; x=token_positions()[j]-.204; p=PS[j]
    # Both bar heights describe the same conditional event. The upper ruler spans
    # 0..0.05%; the main board retains its original uniform scale and its true zero.
    assert 0<p<.0005
    y=TOKEN_BASELINE+TOKEN_SCALE*p; z=.249; h=1.24; y0=1.035
    bx=-3.58;ax=-4.18;top=y0+h*p/.0005
    rim=.058
    w.path(tuple((x+rim*math.cos(a*math.tau/32),y+rim*math.sin(a*math.tau/32),z)
                 for a in range(33)),GOLD,2.2,q)
    line=smooth(q,.04,.67)
    # A single, jointed leader links the subpixel original to the enlarged scale.
    route=((x-.048,y+.041,z),(x-.38,.44,z),(x-.38,.82,z),(bx,.82,z),(bx,y0,z))
    for i,(a,b) in enumerate(zip(route,route[1:])):
        f=clamp(line*(len(route)-1)-i)
        if f:w.segment(a,vlerp(a,b,f),CYAN,1.72,q*.82)
    v=smooth(q,.28,.76)
    if v:
        w.segment((ax,y0,z),(bx+.34,y0,z),'#B0B8C4',1.65,v)
        w.segment((ax,y0,z),(ax,y0+h*v,z),'#B0B8C4',1.65,v)
        for frac in (0,.5,1):
            yy=y0+h*frac;tick=smooth(v,frac*.62,frac*.62+.27)
            if tick:w.segment((ax-.055,yy,z),(ax+.055,yy,z),'#B0B8C4',1.6,tick)
        w.text('0.05%',(ax-.13,y0+h,z),34,WHITE,v,'right',font=SERIF)
        w.text('0',(ax-.13,y0+.026,z),28,WHITE,v,'right',font=SERIF)
    mass=smooth(q,.40,.91)
    if mass:
        yy=y0+(top-y0)*mass
        w.face(((bx-.095,y0,z),(bx+.095,y0,z),(bx+.095,yy,z),(bx-.095,yy,z)),GOLD,mass,1.,0)
        w.segment((bx+.11,yy,z),(bx+.33,yy,z),GOLD,1.45,mass)
        w.text(f'{p*100:.3g}%',(bx+.43,yy,z),43,GOLD,mass,'left',font=SERIF)
        w.text('局部刻度',(bx+.43,y0+.39,z),30,'#BBC2C9',mass,'left')

def costly_arithmetic(g,t,d,anchors):
    ltr,multi,low,neg,avg,expa=anchors
    ltr=min(ltr,multi-1.7)
    here=g.clock.at('读到这里');joint=g.clock.at('整句续写')
    # On “到这里”, the head must actually arrive at cat; keep it there while
    # naming its conditional probability. The product gets its own eight visits.
    if t<ltr+.29:scan=mix(2,0,smooth(t,ltr-.29,ltr+.29))
    elif t<here+.12:scan=mix(0,2,smooth(t,ltr+.29,here+.12))
    elif t<multi-.43:scan=2.
    elif t<multi+.10:scan=mix(2,0,smooth(t,multi-.43,multi+.10))
    else:scan=7*clamp((t-multi-.10)/max(.75,joint+1.02-multi-.10))
    up=clamp(scan)
    head=max(0,min(7,int(scan+.35)))
    k=smooth(t,neg-.05,neg+2.58)
    w=measured_token_stage(g)
    lens=smooth(t,here-.07,here+.65)*(1-smooth(t,multi-.64,multi-.12))
    clear=smooth(t,here-.49,here+.01)*(1-smooth(t,multi-.12,multi+.35))
    if clear or lens:
        keep=[];label=f'{PS[2]*100:.3g}%'
        for it in w.items:
            if it[1]==3:
                factor=(1-clear if (it[2].startswith('P(x') or it[2] in ('T','| prefix)',')'))
                        else 1-smooth(lens,.04,.39) if it[2]==label else 1)
                if factor<1:
                    piece=list(it);piece[7]*=factor;it=tuple(piece)
            keep.append(it)
        w.items=keep
        rare_word_ruler(w,lens)
    if k>0:
        # Take only the existing bars out of the canonical plate. The token
        # boxes, baseline, exact anchors and model credit stay put.
        w.items=[it for it in w.items if it[1]!=0]
        for j,(x,p,loss,(_,_,alts)) in enumerate(zip(token_positions(),PS,LOSSES,ROWS)):
            q=smooth(t,neg+.13*j-.09,neg+.13*j+1.56)
            z=.105
            bx=mix(x-.204,x,q)
            balance=smooth(t,avg+.63,expa+.32)
            h=mix(TOKEN_SCALE*p,.142*mix(loss,MEAN,balance),q)
            ww=mix(.128,.244,q)
            area(w,bx,TOKEN_BASELINE+h/2,ww,h,GOLD,1,True,z)
            for i,(_,v) in enumerate(alts):
                y=TOKEN_SCALE*v*(1-q)
                if y>0:area(w,x+.204*i,TOKEN_BASELINE+y/2,.128,y,CYAN,1-q,True,z)
        # Give the old probabilities and new heights separate lenses.
        fade=1-smooth(k,.02,.34)
        kept=[]
        for it in w.items:
            if it[1]==3 and isinstance(it[2],str) and it[2].endswith('%'):
                a=list(it);a[7]*=fade;kept.append(tuple(a))
            elif it[1]==3 and str(it[2]).startswith(('P(x₁','| prefix)')) or (
                it[1]==3 and it[2]=='T'):
                a=list(it);a[7]*=fade;kept.append(tuple(a))
            else:kept.append(it)
        w.items=kept
        ink=smooth(k,.39,.66)
        w.text('−ln pᵢ  ·  nats per token',(0,1.807,.145),51,WHITE,
               ink*(1-smooth(t,expa-.43,expa-.12)),font='math')
        w.ppl_tex=ink*smooth(t,expa-.08,expa+.56)
    q=smooth(t,.075,.66)*(1-smooth(t,neg-.32,neg+.45))
    if q:
        for j in range(len(PS)):
            al=max(0.,1-abs(scan-j)/1.04)*q
            if al:focus_token(w,j,al)
        # The read-head has a continuous trajectory; the highlighted column
        # is the token it is currently scoring.
        if scan<6.995:
            xs=token_positions()
            sx=mix(xs[0],xs[-1],scan/7)
            w.segment((sx,.98,.171),(sx,.77,.171),CYAN,3.45,q*(1-lens))
            pin(w,(sx,.772,.173),CYAN,.063,q*.94*(1-lens))
        n=min(8,1+head)
        p=prod(PS[:n])
        show=smooth(t,multi-.05,multi+.75)
        if show:
            num=f'{p:.4f}' if p>.001 else f'{p:.3e}'
            factors=('p₁','p₁ × p₂','p₁ × p₂ × p₃')[n-1] if n<=3 else f'p₁ × … × p{chr(8320+n)}'
            w.text(f'{factors}  =  {num}',(0,-2.33,.159),42,GOLD,show,font='math')
        small=smooth(t,low-.28,low+.60)*(1-smooth(t,neg-.32,neg+.43))
        if small:
            w.text('Float32 · repeat this product four times → 0',(0,-2.76,.161),24,CORAL,small,font=SERIF)
    mark=smooth(t,avg-.12,avg+1.03)
    if mark:
        line_y=MEAN*.142+TOKEN_BASELINE
        w.path(((TOKEN_LEFT-.12,line_y,.167),(TOKEN_RIGHT+.11,line_y,.167)),WHITE,2.45,1,
               progress=mark)
        show=smooth(t,avg+.09,avg+.72)
        w.text(f'Mean = {MEAN:.3g} nats',(.0,-1.161,.153),40,WHITE,show,font='math')
        for j,(x,l) in enumerate(zip(token_positions(),LOSSES)):
            v=math.sin(math.pi*smooth(t,avg+.055*j,avg+1.76+.055*j))
            if v:
                w.segment((x+.19,TOKEN_BASELINE+.142*l,.18),(x+.30,line_y,.18),GOLD,1.55,v*.87)
    number=smooth(t,expa-.15,expa+.90)
    if number:
        w.text(f'PPL = exp({MEAN:.4f}) ≈ {P["ppl"]:.2f}',(0,-2.262,.171),49,GOLD,number,font='math')
        w.text('Eight-token continuation',(0,-2.69,.14),25,WHITE,number,font=SERIF)
        phase=smooth(t,expa-.30,expa+4.22)
        if .0<phase<1:
            yy=MEAN*.142+TOKEN_BASELINE
            path=((-.2,yy,.176),(5.06,yy,.176),(5.06,-2.28,.176),(3.29,-2.28,.176))
            w.path(path,GOLD,2.5,number*.78,progress=phase,arrow=True)
            j=min(2,int(phase*3))
            pin(w,vlerp(path[j],path[j+1],phase*3-j),GOLD,.071,.97*number)
    return w

def choice_stage(g,collapse=1,appear=1,trace=0,counting=1):
    """10 banks of 10,000 choices, yielding 10 individual equal choices."""
    w=World(g);X=tuple(-4.50+j for j in range(10))
    al=appear
    bank=1-smooth(collapse,.13,.88)
    for j,x in enumerate(X):
        p=clamp(collapse*1.20-.020*j)
        yy=mix(-.03,.02,p)
        bank_alpha=appear*clamp(counting*10-j)
        if bank>.003 and bank_alpha:
            for xj in range(6):
                for yj in range(5):
                    p2=smooth(p,.12+.008*xj,.96)
                    dx=mix((xj-2.5)*.105,0,p2);dy=mix((yj-2)*.125,0,p2)
                    area(w,x+dx,yy+dy,.068,.095,CYAN,bank*bank_alpha*(.64+.18*((xj+yj+j)%2)),True,.10)
            area(w,x,yy,.79,.74,CYAN,.64*bank*bank_alpha,z=.082)
        solid=smooth(p,.34,.90)*al
        if solid:
            area(w,x,yy,.89,.61,CYAN,solid)
            w.text('1/10',(x,yy,.138),28,CYAN,solid,font='math')
        visit=clamp(1-abs(trace-j)/.86)*solid
        if visit:
            area(w,x,yy,.86,.58,CYAN,.46*visit,True,z=.077)
            w.segment((x-.34,yy-.41,.11),(x+.34,yy-.41,.11),GOLD,3.1,visit*.88)
    a1=(1-smooth(collapse,.35,.66))*al;a2=smooth(collapse,.45,.95)*al
    w.text('100,000 equal choices',(0,1.69,.14),58,WHITE,a1,font=SERIF)
    w.text('Ten equal choices',(0,1.69,.14),58,WHITE,a2,font=SERIF)
    w.text('10 banks × 10,000',(0,-.96,.134),32,CYAN,a1,font='math')
    w.text('PPL = 10',(0,-1.09,.139),57,GOLD,a2,font='math')
    return w

def probability(g,t,d):
    if t<1e-6:measured_token_stage(g).draw();return
    ltr=word(g,d,'from left to right',5.5)
    multi=word(g,d,'multiply those probabilities',7.7)
    low=word(g,d,'round it to zero',14.)
    neg=word(g,d,'negative log probability',16.6)
    avg=word(g,d,'average those losses',20.3)
    expa=word(g,d,'then exponentiate',22.9)
    eff=word(g,d,'an effective number of choices',28.5)
    uniform=word(g,d,'uniform guessing',35.9)
    to_ten=word(g,d,'bring it down to ten',41.)
    var=word(g,d,'the actual number of plausible options',48.4)
    if t>=var-.17:
        from ppl_chalk import choice_variation
        choice_variation(g,t,d,var);return
    f=smooth(t,eff-.54,eff+.78)
    ws=costly_arithmetic(g,t,d,(ltr,multi,low,neg,avg,expa))
    if 0<f<.998:
        # Old columns descend through their own baseline while the choice
        # banks rise elsewhere. Preserve the horizontal axes.
        ctx=g.c;ctx.save();ctx.rectangle(0,0,1600,753);ctx.clip();ctx.translate(0,170*f)
        ctx.rectangle(0,0,1600,753*(1-f))
        ctx.clip();ws.draw();ctx.restore()
    elif f<=0:ws.draw()
    tex=getattr(ws,'ppl_tex',0)*(1-smooth(t,eff-.57,eff-.18))
    if tex:
        from motion import formula
        formula(g,'ppl',800,160,505,tex)
    if f>0:
        u=smooth(t,to_ten-.09,to_ten+2.15)
        trace=mix(-1,10,smooth(t,to_ten+2.55,d-.93)) if t>to_ten+1.85 else -10
        w=choice_stage(g,u,f,trace,smooth(t,eff-.43,uniform+.10))
        if 0.001<f<.4: # give the old tableau a separate upper lane while the array lands
            ctx=g.c;ctx.save();ctx.translate(0,-54*(1-f));w.draw();ctx.restore()
        else:w.draw()
        if eff+.47<t<to_ten-.38:
            q=.64*smooth(t,eff+.52,uniform-.14)+.36*smooth(t,uniform-.13,to_ten-.67)
            xx=mix(-4.94,4.94,q)
            w=World(g)
            w.path(((-4.94,-.58,.08),(xx,-.58,.08)),CYAN,1.90,.84)
            pin(w,(xx,-.58,.11),CYAN,.037,.95)
            w.draw()
@lru_cache(maxsize=1)
def demo():return json.loads((R/'data'/'tokenizers.json').read_text())

def sent_units():
    p=demo();text=p['text']
    sizes=[(1 if s!=' ' else .67) for s in text]
    spans=sum(sizes);wid=8.32/spans
    x=-4.65;chars=[];xb=[x]
    for c,size in zip(text,sizes):
        ww=size*wid
        chars.append((c,x+ww*.5,ww))
        nn=len(c.encode())
        xb.extend(x+ww*j/nn for j in range(1,nn+1));x+=ww
    return chars,xb

def token_rows(g,t,d,cues,gain):
    start,cut,split,bits,den,compare=cues
    p=demo();chars,xb=sent_units();w=World(g)
    count=p['bytes'];fixed=p['equal_loss_bits'];demos=p['models']
    row_up=smooth(t,cut-.28,cut+1.20)*gain
    row_dn=smooth(t,cut+.42,cut+2.87)*gain
    bits_an=smooth(t,bits-.40,bits+1.02)*gain
    close=smooth(t,bits+.88,bits+2.66)
    here=smooth(t,compare-.10,compare+.89)
    sentence=smooth(t,start+.2,start+.9)*gain
    for i,(c,x,wid) in enumerate(chars):
        on=smooth(t,start+.15+.073*i,start+.51+.073*i)*sentence
        if i==0:
            w.text('␠',(x,.62,.14),21,WHITE,on*.72,font=SERIF)
        elif c!=' ':w.text(c,(x,.62,.14),31,WHITE,on,font=SERIF)
    marker=smooth(t,start+.42,cut+.1)
    if 0<marker<.999:
        xv=mix(xb[0],xb[-1],marker)
        w.path(((xb[0],.416,.103),(xv,.416,.103)),CYAN,2.6,sentence*.83)
        pin(w,(xv,.416,.126),CYAN,.063,sentence)
    for j,(m,col,y,al) in enumerate(zip(demos,(CYAN,GOLD),(1.03,.18),(row_up,row_dn))):
        if not al:continue
        bz=m['boundaries'];n=len(bz)-1
        w.text(f'{m["label"]} · {n} tokens',(-4.62,y+(.29 if not j else -.36),.15),28,col,al,
               font=SERIF,align='left')
        for sq,(i,e) in enumerate(zip(bz,bz[1:])):
            q=smooth(t,cut+.24*j+.045*sq,cut+.30*j+.045*sq+1.07)
            if j:q*=.42+.58*smooth(t,split+.08*sq-.22,split+.08*sq+.72)
            if q:
                pos=xb[i];end_ab=mix(pos,xb[e],q)
                mid=(pos+end_ab)/2
                area(w,mid,y,max(.006,end_ab-pos-.019),.15,col,al*q,z=.105)
        show=smooth(t,split-.23,split+1.14)*al
        eq=smooth(t,bits-.07,bits+.88)
        old=show*(1-eq)
        if old:
            text=f'{2**(fixed/n):.1f} PPL'
            w.text(text,(4.92,y+.03,.14),32,(CORAL if j else WHITE),old,font='math',align='right')
        if eq:
            bpb=mix(fixed/count,m['bpb'],here)
            w.text(f'{bpb:.3f} BPB',(4.92,y+.03,.14),31,(col if here>0 else WHITE),al*eq,font='math',align='right')
    fig=smooth(t,split-.16,split+.68)*(1-smooth(t,compare-.13,compare+.89))*gain
    if fig:
        w.text('Equal-loss example · 89 bits',(0,2.0,.15),40,WHITE,fig,font=SERIF)
    if cut+1.03<t<split+.32:
        differences=sorted(set(demos[0]['boundaries'])^set(demos[1]['boundaries']))
        if differences:
            q=mix(-.8,len(differences)-.18,smooth(t,cut+1.04,split+.32))
            for j,i in enumerate(differences):
                aa=clamp(1-abs(q-j)/.86)*gain
                if aa:
                    xx=xb[i]
                    w.segment((xx,1.13,.133),(xx,.89,.133),CYAN,4.,aa)
                    w.segment((xx,.30,.133),(xx,.048,.133),GOLD,4.,aa)
                    pin(w,(xx,mix(.98,.19,clamp(q-j+.52)),.155),WHITE,.058,aa)
    if split+.42<t<bits+.04:
        u=smooth(t,split+.45,bits+.04)
        # Equal total loss: the same-length gold beam feeds both divisors.
        xx=mix(-4.42,3.92,u)
        yy=1.83
        shine=math.sin(math.pi*u)**.48
        w.path(((-4.42,yy,.127),(xx,yy,.127)),GOLD,3.34,shine*.84*gain)
        pin(w,(xx,yy,.148),GOLD,.065,shine*gain)
    if here:
        w.text('Measured continuation loss',(0,2.0,.15),40,WHITE,here*gain,font=SERIF)
    if bits_an:
        for i in range(count):
            q=smooth(t,den+.023*i-.24,den+.023*i+.60)
            if q:area(w,(xb[i]+xb[i+1])*.5,-.82,max(.012,(xb[i+1]-xb[i])*.91),.25,WHITE,bits_an*q,z=.11)
        formul=smooth(t,den-.08,den+.91)*gain
        w.text('Bits per byte = total bits ÷ UTF-8 bytes',(0,-1.44,.15),42,WHITE,formul,font='math')
        w.text(f'{count} bytes · leading space included',(0,-1.94,.14),28,CYAN,formul,font=SERIF)
        w.text('log₂ measures bits',(-4.62,-2.46,.135),24,WHITE,formul*.86,font='math',align='left')
        scan=smooth(t,den+.37,compare-.10)
        if 0<scan<1:
            active=math.sin(math.pi*scan)**.48
            front=mix(xb[0],xb[-1],scan)
            w.path(((xb[0],-1.02,.135),(front,-1.02,.135)),CYAN,3.,active*gain)
            pin(w,(front,-1.02,.14),CYAN,.061,active*gain)
        pair=smooth(t,den+1.63,den+2.33)*(1-smooth(t,compare-.2,compare+.52))*gain
        if pair:
            index=p['text'].encode().index('ï'.encode())
            for m in (index,index+1):
                area(w,(xb[m]+xb[m+1])*.5,-.82,(xb[m+1]-xb[m])*.84,.22,CYAN,
                     pair*.8,True,z=.114)
            w.text('ï → C3 AF',(4.83,-2.43,.138),28,CYAN,pair,font='math',align='right')
    return w

ISLANDS=((-3.65,-.40,'PTB','35.76'),(0,-.40,'WikiText-103','17.48'),(3.65,-.40,'1BW','42.16'))
def transfer_stage(g,base=1,closed=1,transfer=1,focus=-10,walk=-10):
    w=World(g)
    g.trace_joint=(0,1.5,.118)
    start_y=1.50
    if transfer:
        w.text('GPT-2 · WebText',(0,2.39,.146),47,WHITE,transfer,font=SERIF)
        for j in range(19):
            q=clamp(transfer*1.58-j*.030)
            if q:area(w,-4.45+j*.491,start_y,.40,.195,CYAN,transfer*q,True,.112)
        w.text('Zero-shot · GPT-2 1.5B · Table 3',(0,-1.97,.13),27,WHITE,transfer,font=SERIF)
    for j,(x,y,name,ppl) in enumerate(ISLANDS):
        al=smooth(base,.05+.07*j,.72+.07*j)
        if not al:continue
        pt=(x,y,.10)
        t=smooth(transfer,.125+.14*j,.50+.155*j)
        ring=[(x+math.cos(c*math.tau/45)*1.03,y+math.sin(c*math.tau/45)*.79,.10) for c in range(46)]
        w.path(ring,WHITE,1.57,al*.87,progress=al)
        if closed:
            c=closed*(1-t)
            if c>0:
                w.path(tuple(ring[12:35]),TEAL,2.49,al*c,progress=al,arrow=True)
                w.text('Train → test',(x,y-.25,.13),24,TEAL,c*al,font=SERIF)
                passed=walk-j*1.10
                if -.12<passed<1.44:
                    angle=math.tau*(.25+.79*passed)
                    k=smooth(passed,-.12,.21)*(1-smooth(passed,1.13,1.44))
                    wing=[(x+1.03*math.cos(angle-q*.069),y+.79*math.sin(angle-q*.069),.125) for q in range(17)]
                    w.path(wing,TEAL,5.22,al*c*k)
                    pin(w,wing[0],TEAL,.075,al*c*k)
        w.text(name,(x,y+.20,.138),31,WHITE,al,font=SERIF)
        if t:
            w.path(((x,start_y-.13,.126),(x,.56,.128)),GOLD,2.45,al,progress=t,arrow=True)
            hit=smooth(t,.62,1)
            w.text(ppl,(x,y-.29,.139),44,GOLD,al*hit,font='math')
            a=max(0,1-abs(j-focus)/.83)
            if a:w.path(ring,GOLD,2.5,a*.62)
    return w

def tokenization(g,t,d):
    if t<=.001:choice_stage(g,trace=-10).draw();return
    C=word(g,d,'two tokenizers',6.)
    split=word(g,d,'split the passage into more pieces',12.)
    bits=word(g,d,'count bits',21.);den=word(g,d,'raw utf-eight bytes',23.)
    measured=word(g,d,'the models can still give',25.)
    historic=word(g,d,'for a long time',30.)
    GPT=word(g,d,'gpt-two took a different route',41.)
    zero=word(g,d,'zero-shot perplexity',45.)
    if t>=d-.78:transfer_stage(g).draw();return
    hinge=smooth(t,.23,1.98)
    if hinge<.999:
        ctx=g.c;ctx.save()
        ctx.translate(0,-42*hinge)
        ctx.rectangle(0,0,1600,max(5,900*(1-hinge)))
        ctx.clip();choice_stage(g,trace=-10).draw();ctx.restore()
    rev=smooth(t,historic-.19,historic+2.03)
    if rev<1:
        # Park the sentence rulers off to the left; projection remains
        # proportional until they are outside the frame.
        ctx=g.c;ctx.save();ctx.translate(-1600*rev,0)
        token_rows(g,t,d,(.65,C,split,bits,den,measured),1).draw()
        ctx.restore()
    enter=smooth(t,historic+.20,historic+2.85)
    if enter:
        traj=smooth(t,GPT-.14,zero+2.31)
        scan=mix(-.9,3.6,smooth(t,zero+.65,d-.84))
        walk=mix(-.2,3.55,smooth(t,historic+1.28,GPT+.31))
        transfer_stage(g,base=enter,closed=1,transfer=traj,focus=scan,walk=walk).draw()

def draw(g,i,t,duration):
    (probability,tokenization)[i](g,t,duration)
