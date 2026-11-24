"""Act III — an answer leaves the page and has to work.

A gold evidence tile walks from a retail bug through the test harness, turns into
a candidate patch and then a grid cell. The final green light leaves its origin
out of view: the question Act IV picks up.
"""
from visual import *
from itertools import combinations
from pathlib import Path
import json

FILL=blend(BG, GRID, .46)
PAPER=blend(BG, MUTED, .15)
OBJECT='#DDDDDD'
FAINT=blend(BG,MUTED,.48)

def text(g,s,x,y,z=27,color=MUTED,alpha=1,**kwargs):
    g.text(s,x,y,z,color,alpha,**kwargs)

def anim(u,a,b): return step(u,a,b)

def fade(u,start,finish):
    return 1-step(u,start,finish)

def particle(g,x,y,color,alpha=1,r=5):
    g.circle(x,y,r*2.8,fill=color,alpha=alpha*.075)
    g.circle(x,y,r,fill=color,alpha=alpha)

def flow(g, x1,y1,x2,y2,progress, opacity=1, color=GOLD):
    g.arrow(x1,y1,x2,y2,MUTED,2,opacity*.66,head=10)
    if 0<progress<1:
        q=ease(progress)
        particle(g,mix(x1,x2,q),mix(y1,y2,q),color,opacity*.94,5)

def trace(g, points, color=MUTED, alpha=1, width=2, pct=1, tip=False):
    """Arc-length path reveal, including corners."""
    if alpha<=0 or pct<=0:return
    lens=[math.hypot(x-u,y-v) for (x,y),(u,v) in zip(points,points[1:])]
    dist=clamp(pct)*sum(lens)
    verts=[points[0]]
    for length,(x,y),(nx,ny) in zip(lens,points,points[1:]):
        if length<=0:continue
        frac=clamp(dist/length)
        verts.append((mix(x,nx,frac),mix(y,ny,frac)))
        dist-=length
        if dist<=0:break
    if len(verts)>1:
        if len(verts)>2:g.poly(verts[:-1],color,width,alpha)
        if tip:g.arrow(*verts[-2],*verts[-1],color,width,alpha,head=10)
        else:g.line(*verts[-2],*verts[-1],color,width,alpha)

def sheet(g,x,y,w=91,h=107,a=1,col=MUTED,style='plain'):
    # Flat silhouettes; an issue, repo and patch share outlines and subdivisions.
    x0,y0=x-w/2,y-h/2
    ear=min(w,h)*.205
    outline=[(x0,y0),(x0+w-ear,y0),(x0+w,y0+ear),(x0+w,y0+h),(x0,y0+h)]
    g.poly(outline,col,2.2,a,close=True,fill=blend(BG,col,.102))
    g.poly([(x0+w-ear,y0),(x0+w-ear,y0+ear),(x0+w,y0+ear)],col,1.3,a*.7)
    if style=='patch':
        subs=.23*w
        g.line(x-subs,y-15,x-subs*.35,y-15,RED,2.5,a)
        g.line(x+subs*.08,y-15,x+subs,y-15,RED,2,a*.50)
        g.line(x-subs,y+15,x-subs*.35,y+15,GREEN,2.5,a)
        g.line(x-subs*.67,y+15-5,x-subs*.67,y+15+5,GREEN,2.5,a)
        g.line(x+subs*.08,y+15,x+subs*1.2,y+15,GREEN,2,a*.58)
    elif style=='ticket':
        g.line(x-w*.29,y-15,x+w*.17,y-15,col,2.5,a*.79)
        g.line(x-w*.29,y,x+w*.29,y,col,2.5,a*.61)
        g.line(x-w*.29,y+15,x+w*.01,y+15,col,2.5,a*.48)
    elif style=='text':
        for j,f in enumerate((.32,.23,.28,.05)):
            yy=y-h*.155+j*(h*.124)
            g.line(x-w*.30,yy,x+w*f,yy,col,max(1,w*.022),a*.52)

def receipt(g,x,y,total,fee,a=1,emph=0,scale=1):
    # Dashed perforation separates order total and shipping fee.
    if a<=0:return
    w=138*scale;h=168*scale
    x0=x-w/2; y0=y-h/2
    serr=[(x0+w-k*w/14,y0+h-((k%2)*5*scale)) for k in range(15)]
    points=[(x0,y0),(x0+w,y0),*serr]
    col=blend(MUTED,GOLD,emph)
    g.poly(points,col,2.1*scale,a,close=True,fill=blend(BG,col,.105))
    g.line(x0+14*scale,y+4*scale,x0+w-14*scale,y+4*scale,col,1.35*scale,a*.6,
           dash=[4*scale,6*scale])
    g.text(total,x,y-33*scale,38*scale,GOLD if emph>.45 else INK,a,font='math')
    if fee is not None:
        g.text('+'+str(fee),x,y+38*scale,29*scale,
               RED if emph>.45 and fee==8 else GREEN if fee==0 else MUTED,a,font='math')
    if emph>0:
        g.circle(x0+w,y0,5*scale,fill=GOLD,alpha=a*emph)

def money(g,u):
    # Anchor, 100-yuan order, neighboring evidence, split between answer and act.
    ax=anim(u,.09,.31)
    ti=anim(u,.08,.32)
    g.tile(800,mix(420,355,ti),mix(68,137,ti),mix(62,165,ti),'',GOLD,fade(u,.08,.26),True)
    xs=(510,800,1090); fees=(8,8,0)
    al=(anim(u,.12,.31),anim(u,.18,.33),anim(u,.28,.43))
    axis=anim(u,.11,.28)
    g.line(337,482,1263,482,GRID,2,axis)
    g.arrow(1194,482,1263,482,MUTED,2,axis*.63)
    g.line(800,449,800,497,GOLD,2,axis*.58)
    for j in range(3):
        pop=al[j]
        x=mix(800,xs[j],ax if j!=1 else 1)
        emph=(anim(u,.26,.41) if j==1 else 0)
        receipt(g,x,mix(401,355,pop),str(99+j),fees[j] if u>.21+j*.06 else None,
                pop,emph,mix(.73,1,pop))
    g.text('≥ 100',800,214,28,GOLD,anim(u,.11,.22),font='math')
    g.line(800,242,800,262,GOLD,1.8,anim(u,.18,.28))
    q=anim(u,.05,.35)
    g.disk(mix(530,482,q),mix(420,590,q),BLUE,mix(53,43,q),'A',fade(u,.88,1))
    g.disk(mix(1070,1185,q),mix(420,590,q),PURPLE,mix(53,43,q),'B')
    n=anim(u,.46,.66)
    sheet(g,mix(482,625,n),590,66,77,n,BLUE,'text')
    code=anim(u,.57,.77)
    g.text('>',mix(1171,948,code),590,40,MUTED,code,font='math')
    g.arrow(984,590,1025,590,MUTED,2,code)
    g.text('≥',1062,590,40,GOLD,code,font='math')
    ring=anim(u,.76,.89)
    g.arc(800,354,102,-math.pi*.72,-math.pi*.72+TAU*ring,RED,2,ring*.52)

def folder_stack(g,x,y,a=1):
    for dy,dx,col,alpha in ((-24,-18,GRID,.8),(-12,-9,MUTED,.54),(0,0,MUTED,1)):
        sheet(g,x+dx,y+dy,94,102,a*alpha,col,'text')

def test_gate(g,x,y,a=1,activated=0, scale=1):
    w=136*scale;h=112*scale
    g.rect(x-w/2,y-h/2,w,h,fill=blend(BG,GRID,.39),
           stroke=blend(MUTED,GREEN,activated),width=2.5*scale,r=13*scale,alpha=a)
    for i in range(2):
        yy=y+(i-.5)*40*scale
        g.line(x-w*.275,yy,x+w*.01,yy,MUTED,2.25*scale,a*.74)
        g.circle(x+w*.245,yy,13*scale,stroke=GREEN if activated else GRID,
                 width=1.6*scale,alpha=a)
        g.check(x+w*.245,yy,True,9*scale,a*activated)

def workflow(g,u):
    start=anim(u,.00,.16)
    for j,x in enumerate((510,800,1090)):
        receipt(g,x,355,str(99+j),(8,8,0)[j],fade(u,0,.17)*(1 if j==1 else .72),float(j==1),1)
    flow_y=404
    issuex=mix(800,287,start)
    sheet(g,issuex,flow_y,95,108,start,GOLD,'ticket')
    rack=anim(u,.10,.25)
    folder_stack(g,623,flow_y,rack)
    flow(g,346,flow_y,556,flow_y,(u-.14)/.20,rack)
    b=anim(u,.20,.45)
    g.disk(mix(1185,658,b),mix(590,269,b),PURPLE,mix(43,35,b),'B')
    g.line(658,315,639,345,PURPLE,1.9,b*.62)
    pc=anim(u,.38,.55)
    sheet(g,977,flow_y,97,106,pc,GOLD,'patch')
    flow(g,688,flow_y,909,flow_y,(u-.29)/.26,pc)
    tc=anim(u,.53,.70)
    # A common execution surface keeps the runtime and historical version fixed.
    hull=anim(u,.61,.76)
    outline=[(543,315),(1410,315),(1410,482),(543,482),(543,315)]
    trace(g,outline,GRID,hull*.88,1.8,hull)
    flow(g,1042,flow_y,1225,flow_y,(u-.50)/.23,tc)
    test_gate(g,1305,flow_y,tc,anim(u,.60,.73))
    cap=anim(u,.51,.68)
    g.text('SWE-bench',800,196,52,INK,cap,font='serif')
    z=anim(u,.73,.92)
    g.text('2,294',702,657,31,GOLD,z,font='math')
    g.line(763,657,804,657,MUTED,1.55,z)
    g.text('Verified',844,657,29,MUTED,z,align='left')

def lamp(g,x,y,ok,alpha=1,rad=24):
    col=GREEN if ok else RED
    g.circle(x,y,rad+8,stroke=col,width=1,alpha=alpha*.24)
    g.circle(x,y,rad,fill=blend(BG,col,.13),stroke=col,width=2,alpha=alpha)
    g.check(x,y,ok,rad*.62,alpha)

def regression(g,u):
    p=anim(u,0,.13)
    if p<1:
        test_gate(g,mix(1305,1095,p),mix(404,413,p),1-p,1,scale=mix(1,1.3,p))
        sheet(g,mix(977,800,p),mix(404,190,p),97,106,1-p,GOLD,'patch')
    x1,x2,x3=421,825,1157
    ys=(354,511,617)
    focus=anim(u,.08,.25)
    broken=anim(u,.29,.49)
    correct=anim(u,.62,.80)
    body=anim(u,.47,.64)
    g.line(421,275,421,661,GRID,1.8,p*.85)
    g.line(825,278,825,661,GRID,1.8,p*.67)
    g.line(1157,275,1157,661,GRID,1.8,p*.85)
    for title,x in (('应收',x2-53),('实收',x2+55)):
        text(g,title,x,238,24,MUTED,p)
    for r,(total,want,historical) in enumerate(((100,0,8),(99,8,8),(101,0,0))):
        y=ys[r]
        target=r==0
        a=(focus,broken,body)[r]
        row=GOLD if target else MUTED
        g.line(550,y,689,y,GRID,1.8,a)
        g.arrow(698,y,743,y,MUTED,1.8,a*.65)
        g.tile(x1,y,104,79,total,row,a,selected=target)
        g.text(str(want),x2-53,y,39,row,a,font='math')
        g.text('→',x2+4,y,30,MUTED,a*.78,font='math')
        z=anim(u,.55,.67)
        prev=historical if u<.19 else 0
        prevAlpha=a*(1-correct)
        good_prev=prev==want
        g.text(str(prev),x2+55,y,39,GREEN if good_prev else RED,prevAlpha,font='math')
        g.text(str(want),x2+55,y,39,GREEN,a*correct,font='math')
        lamp(g,x3,y,good_prev,prevAlpha*(1-z*.10))
        lamp(g,x3,y,True,a*correct)
    a=anim(u,.12,.26)
    g.text('运费 = 0',800,159,35,INK,a*(1-correct),weight='medium')
    g.text('>',739,159,46,MUTED,correct,font='math')
    g.arrow(777,159,824,159,MUTED,2,correct,head=12)
    g.text('≥',868,159,46,GOLD,correct,font='math')
    g.text('目标测试',183,354,25,GOLD,focus*.9)
    g.poly([(242,454),(207,454),(207,656),(242,656)],GRID,2,body)
    g.text('回归',159,556,24,MUTED,broken)
    y=693
    ok=anim(u,.86,.96)
    g.line(451,y,1144,y,GREEN,1.5,ok*.34)
    g.circle(800,y,4.2,fill=GREEN,alpha=ok)

def loop_wire(g, x0,y0,x1,y1, x2,y2, x3,y3,alpha,p,color=MUTED):
    if alpha<=0 or p<=0:return
    def at(t):
        v=1-t
        return ((v*v*v*x0+3*v*v*t*x1+3*v*t*t*x2+t*t*t*x3),
                (v*v*v*y0+3*v*v*t*y1+3*v*t*t*y2+t*t*t*y3))
    # Poly vertices are intentionally parameterized to keep reveal speed smooth.
    steps=25
    pts=[at(p*i/steps) for i in range(steps+1)]
    g.poly(pts[:-1],color,2.15,alpha)
    g.arrow(*pts[-2],*pts[-1],color,2.15,alpha,head=11)

def clock(g,x,y,a,col=MUTED,spin=.68,rad=19):
    g.circle(x,y,rad,stroke=col,alpha=a,width=2)
    g.poly([(x,y-rad*.54),(x,y),(x+rad*.60*math.sin(spin*TAU),y-rad*.60*math.cos(spin*TAU))],col,2,a)
    g.circle(x,y,2.5,fill=col,alpha=a)

def scaffold(g,u):
    unfold=anim(u,.03,.19)
    for x in (443,1139):
        g.disk(mix(793,x,unfold),mix(419,391,unfold),BLUE,mix(53,48,unfold),'A',unfold if x>700 else 1)
        g.tile(x,207,68,57,'',GOLD,unfold,True)
        flow(g,x,249,x,330,(u-.06)/.17,unfold)
    direct=anim(u,.18,.39)
    retry=anim(u,.33,.66)
    sheet(g,443,604,64,74,direct,GOLD,'patch')
    flow(g,443,454,443,552,(u-.22)/.21,direct)
    rightx=1139
    retX=1366; retY=388
    g.circle(retX,retY,36,fill=FILL,stroke=MUTED,width=2,alpha=retry)
    toolswitch=anim(u,.41,.48)
    g.rect(retX-17,retY-13,35,24,stroke=MUTED,width=2.1,r=3,alpha=retry)
    g.line(retX-17,retY-6,retX+18,retY-6,MUTED,1.8,retry*(1-toolswitch))
    for yy in (retY-5,retY+4):
        g.line(retX-10,yy,retX+3,yy,MUTED,1.8,retry*toolswitch)
        g.circle(retX+9,yy,2.3,fill=MUTED,alpha=retry*toolswitch)
    flow(g,1200,387,1322,387,(u-.31)/.16,retry)
    loop_wire(g,1366,433,1357,526,1145,523,1139,452,retry,anim(u,.39,.65))
    if .42<u<.65:
        t=ease((u-.42)/.23)
        # Follow the feedback arc from tool to the same model.
        particle(g,mix(1366,1139,t),450+57*math.sin(math.pi*t),RED,retry*.9,4.5)
    fault=anim(u,.35,.47)*fade(u,.60,.70)
    g.check(retX,458,False,11,fault)
    polish=anim(u,.63,.78)
    sheet(g,rightx,604,64,74,polish,GOLD,'patch')
    flow(g,rightx,470,rightx,552,(u-.59)/.18,polish)
    # Completion is not correctness; separate result marks stay outside the sheets.
    results=anim(u,.67,.82)
    g.check(500,604,False,18,results*.89)
    g.check(1196,604,True,18,results*.97)
    fair=anim(u,.80,.93)
    for x in (443,1139):
        yy=699
        clock(g,x-62,yy,fair,spin=.59)
        for j in range(4):
            g.rect(x-25+j*14,yy-6,9,12,stroke=GOLD,width=1.4,alpha=fair*.73,r=2)

PAIRCOMBOS=list(combinations(range(4),2))
PATCH_X=(533,711,889,1067)
RESULT=(False,False,True,False)

def candidate(g,j,x,y,sz,a=1,known=1):
    if a<=0:return
    # Neutral square first; its test result is a separate inspection mark.
    g.tile(x,y,sz,sz,'',GOLD,a)
    g.text(str(j+1),x,y,sz*.35,INK,a,font='math')
    if known:
        g.check(x+sz*.44,y+sz*.44,RESULT[j],sz*.15,a*known)

def pairing(g,x,y,sz,pair,a=1,resolve=0):
    good=any(RESULT[j] for j in pair)
    background=blend(BG,(GREEN if good else RED),.08*resolve)
    col=blend(GRID,(GREEN if good else RED),resolve*.78)
    g.rect(x-sz*1.50,y-sz*.78,sz*3,sz*1.56,fill=background,stroke=col,width=1.85,r=9,alpha=a)
    for j,dx in zip(pair,(-.68,.68)):
        candidate(g,j,x+dx*sz,y,.78*sz,a,0)
    if resolve:
        g.check(x+1.51*sz,y+.66*sz,good,sz*.22,a*resolve)

def sample_one(g,u):
    build=anim(u,.02,.25)
    found=anim(u,.17,.39)
    # Stay with the just-submitted patch as it turns into a sampling pool.
    # No verdict travels with the blank patch shells; those are tested anew.
    carry=fade(u,.032,.087)
    g.disk(1139,391,BLUE,48,'A',fade(u,.005,.071))
    flow(g,1139,470,1139,552,-1,fade(u,.01,.066))
    sheet(g,mix(1139,PATCH_X[0],build),mix(604,273,build),64,74,carry,GOLD,'patch')
    for j,x in enumerate(PATCH_X):
        candidate(g,j,mix(1139,x,build),mix(604,273,build),mix(66,82,build),
                  anim(u,.02+.048*j,.15+.048*j),found)
    g.text('pass@1',800,166,38,INK,anim(u,.25,.43)*fade(u,.57,.70),font='serif')
    g.text('pass@2',800,166,38,INK,anim(u,.59,.73),font='serif')
    g.text('1 / 4',800,424,54,GOLD,anim(u,.32,.47)*fade(u,.58,.72),font='math')
    two=anim(u,.52,.71)
    g.text('?',800,424,60,INK,two*fade(u,.72,.85),font='serif')
    for idx,pair in enumerate(PAIRCOMBOS):
        al=anim(u,.68+idx*.032,.79+idx*.031)
        ix,iy=idx%3,idx//3
        x=550+250*ix;y=490+110*iy
        pairing(g,x,y,46,pair,al)

def score_cells(g,x,y,portion,a,scale=1):
    if a<=0:return
    width,space=22*scale,7*scale
    total=6*width+5*space
    for j in range(6):
        sx=x-total/2+j*(width+space)
        sd=clamp(portion-j)
        g.rect(sx,y-11*scale,width,22*scale,stroke=MUTED,width=1.35*scale,r=3,alpha=a*.56)
        g.rect(sx+2,y-9*scale,(width-4)*sd,18*scale,fill=GREEN,r=2,alpha=a*.84)

def sample_two(g,u):
    win=anim(u,.04,.34)
    lose=anim(u,.27,.50)
    select=anim(u,.68,.85)
    generic=anim(u,.55,.591)*fade(u,.727,.758)
    regroup=anim(u,.529,.602)*fade(u,.691,.753)
    bars=anim(u,.629,.666)*fade(u,.722,.753)
    average=anim(u,.683,.718)
    settle=anim(u,.724,.749)
    compare=anim(u,.921,.98)
    proof=1-compare
    for j,x in enumerate(PATCH_X):
        spotlight=(anim(u,0,.055)*fade(u,.12,.31)) if j==2 else 0
        candidate(g,j,x,273,82+13*spotlight,mix(1,.20,bars)*proof,1)
        if spotlight:g.circle(x,273,69,stroke=GREEN,width=2,alpha=.6*spotlight)
    left=800-g.measure('pass@2',38,font='serif')/2
    g.text('pass@',left,166,38,INK,proof,align='left',font='serif')
    suffix='k' if generic>=.5 else '2'
    emphasis=.67+.33*abs(2*generic-1)
    g.text(suffix,left+g.measure('pass@',38,font='serif'),166,38,INK,proof*emphasis,align='left',font='serif')
    hits=[pair for pair in PAIRCOMBOS if any(RESULT[j] for j in pair)]
    misses=[pair for pair in PAIRCOMBOS if pair not in hits]
    for idx,pair in enumerate(PAIRCOMBOS):
        ix,iy=idx%3,idx//3
        x=550+250*ix;y=490+110*iy
        good=pair in hits
        group_index=(hits if good else misses).index(pair)
        nx=mix(x,550+250*group_index,regroup)
        ny=mix(y,489 if good else 612,regroup)
        if regroup>0 and (ix!=group_index or iy!=int(not good)):
            ny+=math.sin(math.pi*regroup)*(26 if good else -26)
        reveal=anim(u,.02+idx*.021,.21+idx*.041)*win if good else lose
        if good and reveal>0 and u<.53:
            q=1-abs(u-(.23+idx*.02))*5.0
            col=blend(GOLD,GREEN,reveal)
            loop_wire(g,889,330,889,395,x,371,x,y-42,reveal*.42*clamp(q),reveal,col)
        pairing(g,nx,ny,46,pair,(1-(.32 if idx!=1 else 0)*select)*(1-bars)**1.65*proof,reveal)
        if good:
            q=anim(u,.065+group_index*.035,.18+group_index*.051)
            if 0<q<1:
                dx=x+(-.68 if pair[0]==2 else .68)*46
                vx=mix(889,dx,q);vy=mix(273,y,q)-33*math.sin(math.pi*q)
                candidate(g,2,vx,vy,mix(62,36,q),math.sin(math.pi*q)**.55,0)
    matha=anim(u,.42,.58)
    g.text('3 / 6  =  1 / 2',800,715,40,GOLD,matha*(1-bars)**1.65*proof,font='math')
    # Three examples of per-task estimates; their lengths converge to one
    # equal-weight average. This uses possible 3/6, 5/6, and 6/6 pair counts.
    for j,n in enumerate((3,5,6)):
        x=mix(452+j*348,800,average)
        y=mix(530,591,average)
        score_cells(g,x,y,mix(n,14/3,average),bars*fade(u,.7,.72))
    score_cells(g,800,591-133*settle,14/3,bars*average)
    if select>0:
        # Pull a wrong candidate out of a green pair: existence is not selection.
        styl=anim(u,.76,.868)
        cy=mix(490,403,styl)
        g.line(769,450,769,cy+20,MUTED,1.6,styl*.72*proof,dash=[3,6])
        candidate(g,0,mix(769,590,compare),cy,mix(36,46,styl),styl*proof,anim(u,.852,.925))
    if compare:
        for j,(n,c) in enumerate(((4,1),(6,3))):
            x=mix(800,546+j*508,compare);y=485
            g.text(f'pass@{j+1}',x,y-104,34,INK,anim(compare,.25,.64),font='serif')
            for k in range(n):
                left=x-122+k*(244/n)
                g.rect(left,y-12,244/n-3,24,
                       fill=GREEN if k<c else None,stroke=None if k<c else MUTED,
                       width=1.3,r=2,alpha=compare*(.89 if k<c else .52))
            g.text('1 / 4' if not j else '1 / 2',x,y+78,43,GOLD,compare,font='math')

# Fixed puzzles. Positions zero-indexed from top left. The first two examples
# fit "right 2". The longer third example reveals the relational rule.
DEMOS=(
    (((1,1),(1,2)),(4,1),2),
    (((0,2),(1,2)),(4,2),2),
    (((0,1),(0,2),(1,2)),(5,2),3),
)
QUERY=(((0,0),(1,0),(0,1)),(3,0),1)
DISAMBIG=(((0,1),(0,2)),(5,1),4)

def cell_box(g,x,y,s,col,a,ghost=False,outline=None):
    g.rect(x+2,y+2,s-4,s-4,
           fill=None if ghost else blend(BG,col,.9),
           stroke=outline or col,width=1.5 if ghost else .75,
           r=min(4,s*.12),alpha=a)

def grid(g,x,y,s,shape=(),anchor=None,shift=0,a=1,obs=1,moving=1,
         border=GRID,trails=0):
    # x,y are top left. 'shift' continuous, so the eye can track each source cell.
    w=6*s;h=4*s
    g.rect(x,y,w,h,fill=blend(BG,GRID,.27),stroke=border,width=1.7,r=2,alpha=a)
    for i in range(1,6):g.line(x+i*s,y,x+i*s,y+h,GRID,1.08,a)
    for i in range(1,4):g.line(x,y+i*s,x+w,y+i*s,GRID,1.08,a)
    if anchor is not None:
        ax,ay=anchor
        cell_box(g,x+ax*s,y+ay*s,s,GOLD,a*obs)
        g.circle(x+(ax+.5)*s,y+(ay+.5)*s,max(1.6,s*.067),fill=BG,alpha=a*obs*.73)
    if moving:
        for cc,rr in shape:
            if trails:
                cell_box(g,x+cc*s,y+rr*s,s,OBJECT,a*trails,True)
                if shift>.2:
                    g.line(x+(cc+.5)*s,y+(rr+.5)*s,x+(cc+shift+.5)*s,
                           y+(rr+.5)*s,MUTED,1.2,a*trails*.76,dash=[3.0,5.5])
            cell_box(g,x+(cc+shift)*s,y+rr*s,s,OBJECT,a*moving)

def pair_grids(g,x,y,s,gap,setup,show,shift,a=1,start=1,board=1,trails=0, question=0):
    shape,anchor,_=setup
    rx=x+6*s+gap
    grid(g,x,y,s,shape,anchor,a=a,obs=start,moving=start)
    flow(g,x+6*s+gap*.20,y+2*s,rx-gap*.20,y+2*s,-1,a*board)
    grid(g,rx,y,s,shape if show else (),anchor if show else None,shift,
         a=a*board,obs=show,moving=show,trails=trails)
    if question>0:
        g.text('?',rx+3*s,y+2*s,s*1.46,MUTED,a*question,font='serif')
    return rx

PAIR0=(221,249,28,76)
PAIR1=(904,249,28,76)
PAIR2=(513,487,31,202)

def arc_intro(g,u):
    # Reuse squares from the patch pool to reveal the grid as a new instrument.
    travel=anim(u,.01,.27)
    prev=fade(u,.07,.29)
    for j,x in enumerate(PATCH_X):
        nx=(220+28*1.5,220+28*1.5,904+28*.5,904+28*1.5)[j]
        ny=(249+28*1.5,249+28*2.5,249+28*2.5,249+28*2.5)[j]
        candidate(g,j,mix(x,nx,travel),mix(273,ny,travel),mix(82,26,travel),prev,0)
    for idx,(_x,_y,_s,_gap) in enumerate((PAIR0,PAIR1)):
        a=anim(u,.12+idx*.18,.32+idx*.18)
        show=anim(u,.23+idx*.19,.39+idx*.19)
        offset=anim(u,.28+idx*.24,.44+idx*.24)*2
        tracks=anim(u,.24+idx*.24,.31+idx*.24)*fade(u,.44+idx*.24,.6+idx*.20)*.49
        pair_grids(g,_x,_y,_s,_gap,DEMOS[idx],show,offset,a,start=a,trails=tracks)
    stamp=anim(u,.73,.88)
    if stamp>0:
        g.text('+2 ?',800,524,63,GOLD,stamp,font='math')
        g.line(685,580,915,580,GOLD,1.9,stamp*.54)

def arc_third(g,u):
    # Rewind and replay the first two movements together: equal distance
    # becomes visible before comparing their invariant endpoint relation.
    compare=anim(u,.414,.455)*fade(u,.531,.562)
    rewind=anim(u,.444,.469)
    replay=anim(u,.477,.525)
    metric=anim(u,.451,.479)*fade(u,.526,.555)
    top=[]
    for idx,(_x,_y,_s,_gap) in enumerate((PAIR0,PAIR1)):
        cur=(_x+compare*(16 if idx==0 else -17),_y-32*compare,_s+5*compare,_gap)
        top.append(cur)
        pair_grids(g,*cur,DEMOS[idx],1,2-2*rewind+2*replay,1,trails=metric*.67)
    x,y,s,gap=PAIR2
    a=anim(u,.04,.17)
    g.text('+2',800,mix(524,513,a),mix(63,32,a),GOLD,fade(u,.16,.37),font='math')
    slide=anim(u,.10,.30)
    reveal=anim(u,.23,.35)
    q=anim(u,.58,.78)
    rx=pair_grids(g,x,y,s,gap,DEMOS[2],reveal,2*slide+q,a,start=a,
                  trails=anim(u,.25,.41)*fade(u,.63,.89)*.31)
    # One empty cell is an observable difference, not just a red label.
    conflict=anim(u,.26,.39)*fade(u,.54,.73)
    if conflict>0:
        g.rect(rx+4*s+2,y+2*s+2,s-4,s-4,stroke=RED,width=2.0,
               r=4,alpha=conflict)
        cx=rx+4.5*s
        g.line(cx,y+3*s+4,cx,y+4*s+15,RED,1.7,conflict*.74)
        g.circle(cx,y+4*s+19,3,fill=RED,alpha=conflict)
    # Show the actual demonstration shape while the wrong prediction is tested.
    aa=anim(u,.416,.456)*fade(u,.57,.75)
    for cc,rr in DEMOS[2][0]:
        if (cc+3,rr) not in {(k+2,r) for k,r in DEMOS[2][0]}:
            cell_box(g,rx+(cc+3)*s,y+rr*s,s,OBJECT,aa*.62,True)
    # Reveal the invariant as identical points of contact in all three results.
    resolved=anim(u,.74,.89)
    contact=anim(u,.516,.545)*fade(u,.61,.72)
    for idx,((_x,_y,_s,_gap),demo) in enumerate(zip((*top,PAIR2),DEMOS)):
        ring=resolved if idx==2 else max(resolved,contact)
        rxx=_x+6*_s+_gap
        ax,ay=demo[1]; cx=rxx+ax*_s;cy=_y+_s*(ay+.5)
        g.circle(cx,cy,_s*.20,fill=GOLD,alpha=ring*.84)
        g.circle(cx,cy,_s*.35,stroke=GOLD,width=1.5,alpha=ring*.47)

def arc_query(g,u):
    q=anim(u,.02,.23)
    for idx,(_x,_y,_s,_gap) in enumerate((PAIR0,PAIR1,PAIR2)):
        newx=(259,709,1159)[idx]
        x=mix(_x,newx,q); y=mix(_y,191,q); s=mix(_s,18,q); gap=mix(_gap,54,q)
        pair_grids(g,x,y,s,gap,DEMOS[idx],1,DEMOS[idx][2],mix(1,.62,q))
    x,y,s,gap=350,411,47,337
    bump=anim(u,.13,.29)
    show=anim(u,.373,.42)
    move=anim(u,.43,.57)
    want=fade(u,.377,.449)
    rx=pair_grids(g,x,y,s,gap,QUERY,show,move,bump,start=bump,board=1,
                  trails=anim(u,.41,.45)*fade(u,.53,.63)*.52,
                  question=want)
    check=anim(u,.71,.881)
    g.text('ARC-AGI',800,330,47,INK,anim(u,.58,.72),font='serif')
    if check>0:
        g.line(rx, y-13, rx+6*s*check,y-13,GREEN,1.7,.52)
        g.line(rx, y+4*s+13, rx+6*s*check,y+4*s+13,GREEN,1.7,.52)
        if check<.99:
            g.line(rx+6*s*check,y-13,rx+6*s*check,y+4*s+13,GREEN,1.4,.29)
        g.check(rx+6*s+40,y+2*s,True,19,anim(u,.84,.94))

def tiny_match(g,x,y,setup,proposal,a=1,solved=0):
    shape,anchor,k=setup
    w=15
    grid(g,x,y,w,shape,anchor,proposal,a)
    if solved:
        g.check(x+101,y+30,proposal==k,10,solved*a)

def search(g,u):
    morph=anim(u,0,.15)
    if morph<1:
        pair_grids(g,mix(350,686,morph),mix(411,174,morph),mix(47,19,morph),
                   mix(337,61,morph),QUERY,1,1,(1-morph)*.9)
        g.text('ARC-AGI',800,330,47,INK,(1-morph),font='serif')
    for j,setup in enumerate(DEMOS):
        x=(658,772,886)[j]
        tiny_match(g,x-44,181,setup,setup[-1],anim(u,.02,.18)*.77)
    g.line(800,249,800,297,MUTED,2.1,anim(u,.08,.23)*.8)
    xxs=(395,800,1205)
    for j,x in enumerate(xxs):
        branch=anim(u,.13+j*.032,.34+j*.028)
        trace(g,[(800,296),(x,296),(x,354)],MUTED,branch*.86,2,branch,True)
        cellA=anim(u,.17+j*.043,.36+j*.056)
        # Rule glyphs are miniature motions: count displacement, join two
        # neighbors, or join them within a three-cell budget.
        if j==0:
            g.arrow(x-49,407,x+5,407,MUTED,2.1,cellA,head=11)
            g.text('2',x+34,407,31,INK,cellA,font='math')
        else:
            cx=x-49 if j==2 else x-22
            a0=cellA*anim(u,.16+j*.041,.3+j*.04)
            p=anim(u,.24+j*.043,.38+j*.046)
            g.rect(cx-34*(1-p),391,28,28,fill=OBJECT,stroke=OBJECT,width=.8,r=3,alpha=a0)
            g.rect(cx+30,391,28,28,fill=GOLD,stroke=GOLD,width=.8,r=3,alpha=a0)
            if j==2:
                g.text('≤ 3',x+53,405,30,INK,a0,font='math')
        for k,setup in enumerate(DEMOS):
            vis=anim(u,.29+k*.049+j*.031,.43+k*.057+j*.031)
            bit=2 if j==0 else setup[-1] if j==1 else min(setup[-1],3)
            cx=x+(k-1)*43
            g.circle(cx,487,4.8,fill=GREEN if bit==setup[-1] else RED,alpha=vis*.82)
        results=anim(u,.44+j*.065,.58+j*.071)
        g.check(x,535,j!=0,16,results)
        # Extra example (a four-cell translation) separates two rules that
        # agreed on every observed demonstration.
        b=anim(u,.80,.94)
        if j:
            grid(g,x-3*22,601,22,DISAMBIG[0],DISAMBIG[1],
                 anim(u,.79,.98)*(4 if j==1 else 3),b,obs=1,
                 moving=1,trails=b*.27)
            g.check(x+99,645,j==1,14,anim(u,.93,1)*b)
    equal=anim(u,.63,.79)
    trace(g,[(800,567),(800,581),(1205,581),(1205,568)],GOLD,equal*.55,1.9,equal)
    # Spending time is visible but does not manufacture a discriminating example.
    time=anim(u,.42,.63)
    clock(g,395,637,time,col=MUTED,spin=anim(u,.44,.75)*.66,rad=24)
    for j in range(3):
        k=anim(u,.43+j*.05,.56+j*.052)
        g.rect(356+j*28,687,22,8,fill=GOLD,r=3,alpha=k*.65)

def lock(g,x,y,s=24,col=MUTED,a=1):
    g.arc(x,y-s*.18,s*.27,math.pi,TAU,col,2.15,a)
    g.rect(x-s*.38,y-s*.21,s*.76,s*.56,
           fill=blend(BG,col,.13),stroke=col,width=1.9,r=3,alpha=a)
    g.circle(x,y+s*.07,s*.062,fill=col,alpha=a)

def gate_icon(g,x,y,a,col=MUTED):
    g.rect(x-27,y-31,54,62,stroke=col,r=6,width=2,alpha=a)
    g.line(x,y-30,x,y+30,col,1.5,a*.72)
    g.circle(x-7,y,2.15,fill=col,alpha=a)
    g.circle(x+7,y,2.15,fill=col,alpha=a)

def response_box(g,x,y,a,kind,ok):
    col=GREEN if ok else RED
    g.tile(x,y,168,74,'',col,a,selected=ok)
    if kind=='hour':
        clock(g,x-44,y,a,GREEN,spin=.5,rad=16)
        g.text('19:30',x+19,y,26,INK,a,font='math')
    elif kind=='public':
        lock(g,x-42,y,25,MUTED,a)
        g.text('节目单',x+28,y,22,INK,a)
    else:
        gate_icon(g,x,y,a*.83,RED if not ok else MUTED)
    g.check(x+113,y,ok,17,a)

def theater(g,u):
    # The last accepted grid supplies the gold marker for a new job.
    # Detach it and carry it into the receiving model position.
    carry=fade(u,.019,.075)
    if carry:
        q=anim(u,0,.069)
        old=fade(u,.006,.060)
        grid(g,734,601,22,DISAMBIG[0],None,4,old)
        g.check(899,645,True,14,old)
        xp=mix(855,800,q);yp=mix(634,420,q);size=mix(22,35,q)
        cell_box(g,xp-size/2,yp-size/2,size,GOLD,carry)
        g.circle(xp,yp,max(1.6,size*.067),fill=BG,alpha=carry*.73)
    onset=anim(u,.00,.16)
    for y in (326,513):
        g.line(335,y,1265,y,GRID,2,onset*.70)
    g.line(800,247,800,603,GRID,1.5,onset*.68)
    g.disk(800,420,BLUE,53,'A',onset)
    # Gold request forms differ by subject, never by a presumed evaluation result.
    for j,(txt,y) in enumerate(zip(('开场？','剧本？'),(326,513))):
        a=anim(u,.09+j*.11,.29+j*.11)
        x=mix(800,417,anim(u,.05+j*.09,.29+j*.11))
        g.tile(x,y,167,76,'',GOLD,a,selected=(j==0))
        g.text(txt,x+17,y,24,GOLD,a,weight='medium')
        if j:lock(g,x-46,y,25,GOLD,a)
        else:clock(g,x-46,y,a,GOLD,spin=.48,rad=15)
        trace(g,[(x+93,y),(645,y),(747,394 if j==0 else 446)],MUTED,a*.74,2,a,True)
        reply=anim(u,.38+j*.095,.54+j*.08)
        trace(g,[(852,394 if j==0 else 446),(955,y),(1067,y)],MUTED,reply*.74,2,reply,True)
        good=reply*(1-anim(u,.69,.84))
        response_box(g,1168,y,good,'hour' if j==0 else 'public',True)
        bad=reply*anim(u,.69,.84)
        response_box(g,1168,y,bad,'block',j!=0)
    fault=anim(u,.72,.88)
    if fault:
        trace(g,[(1322,546),(1355,546),(1355,292),(1322,292)],
              MUTED,fault*.63,1.55,fault)

BEHAVIOR=(False,False,True,False,False,False)
USE=(False,True,False,False,True,False)

def behavior_eval(g,u):
    m=anim(u,.0,.19)
    for j,txt in enumerate(('剧本？','开场？')):
        x=mix(417,492+616*j,m);y=mix((513,326)[j],362,m)
        g.tile(x,y,167,76,'',GOLD,1-m)
        g.text(txt,x,y,24,GOLD,1-m)
    b=anim(u,.09,.28)
    g.text('HarmBench',492,178,46,INK,b,font='serif')
    g.line(800,292,800,631,GRID,1.9,anim(u,.26,.55))
    for side,(name,arr) in enumerate(zip(('有害帮助','误挡正常请求'),(BEHAVIOR,USE))):
        x=492+616*side
        a=anim(u,.23+side*.3,.46+side*.29)
        g.text(name,x,309,31,INK,a,weight='medium')
        for j,wrong in enumerate(arr):
            al=anim(u,.24+side*.28+j*.028,.41+side*.26+j*.029)
            y=422+(j//3)*91
            cx=x+(j%3-1)*88
            g.tile(cx,y,55,55,'',MUTED,al)
            after=anim(u,.33+side*.29+j*.023,.47+side*.27+j*.027)
            g.check(cx,y,not wrong,14,after)
        c=anim(u,.70,.88)*a
        k=sum(arr)
        left=x-132;yy=620
        g.line(left,yy,x+132,yy,MUTED,2.2,c*.49)
        span=264*(k/len(arr))*anim(u,.69,.84)
        g.line(left,yy,left+span,yy,RED,4.0,c*.91)
        g.circle(left+span,yy,4.8,fill=RED,alpha=c)
    undef=anim(u,.79,.94)
    g.poly([(470,672),(470,692),(1130,692),(1130,672)],MUTED,1.5,undef*.61)
    g.text('示例',800,721,18,MUTED,undef*.77)

def twist_close(g,u):
    # The verdict icons persist; what they know about the history does not.
    carry=anim(u,.00,.25)
    before=1-carry
    for x,arr,label in zip((492,1108),(BEHAVIOR,USE),('有害帮助','误挡正常请求')):
        for j,wrong in enumerate(arr):
            y=mix(422+(j//3)*91,418,carry)
            xx=mix(x+(j%3-1)*88,x,carry)
            g.tile(xx,y,mix(55,39,carry),mix(55,39,carry),'',MUTED,before)
            g.check(xx,y,not wrong,14,before)
        g.text(label,x,309,31,INK,before*.72,weight='medium')
    anchor=anim(u,.76,.94)
    keep=1-anchor
    test_gate(g,mix(511,530,anchor),415,anim(u,.055,.25)*keep,1,mix(1.19,.68,anchor))
    grid(g,1007+51*anchor,359+11*anchor,mix(30,22,anchor),
         QUERY[0],QUERY[1],1,anim(u,.08,.25)*keep)
    lamp(g,mix(1266,1070,anchor),419,True,anim(u,.13,.30)*keep,22)
    origins=anim(u,.35,.59)
    g.line(614,419,986,419,GOLD,1.6,origins*.3*keep,dash=[4,9])
    if origins:
        g.tile(800,mix(419,420,anchor),mix(67,68,anchor),62,'',GOLD,origins,True)
        g.text('?',800,419,38,GOLD,origins*keep,font='serif')
    if anchor:
        g.disk(530,420,BLUE,53,'A',anchor)
        g.disk(1070,420,PURPLE,53,'B',anchor)

SCENES=(money,workflow,regression,scaffold,sample_one,sample_two,
        arc_intro,arc_third,arc_query,search,theater,behavior_eval,twist_close)

# A handful of concept reveals follow the take instead of an estimate of how
# fast the lecturer reaches that word. Positions on the right are the authored
# scene clock; g.cue gives the corresponding point on the delivered take.
SYNC={
    0: (('九十九块',.20),('刚好一百',.31),
        ('写了段挺有道理',.50),('改了个符号',.68)),
    2: (('一律免运费',.16),('刚才报错的订单立刻对了',.25),
        ('小额订单',.36),('分两道关',.54),('改完还得过',.72),
        ('两排都绿',.88)),
    5: (('它可以跟其余三份',.14),('剩下的三对',.29),
        ('有一半的组合',.52),('把这件事推广到抽 K 份',.56),
        ('真测时',.628),('再把各题取平均',.685),
        ('只交一份时',.765),('给一次机会和给两次机会',.918)),
    7: (('两格走完，停',.25),('中间还隔着一格',.33),
        ('可示范里的灰块',.44),('移动的距离刚好一样',.475),
        ('停下来的关系也刚好一样',.53),('原来要做的是',.59),
        ('滑到贴住金块为止',.77)),
    8: (('停在哪儿',.25),('对，刚好贴上',.37),
        ('这就是 ARC-AGI',.59),('评分会对整张图',.76)),
    10:(('今晚几点开场',.23),('还没公开的剧本',.36),
        ('应该拿到时间',.46),('停在公开信息',.56),
        ('都一口回绝',.73),('也进不了门',.88)),
}

HOLDS=tuple(beat.get('hold',.45) for beat in
            json.loads(Path(__file__).with_suffix('.json').read_text()))

def scene_clock(g,i,u,stop):
    # Real breathing space is still. Between words the choreography stays
    # continuous; the key reveals themselves follow the delivered take.
    if u<=0:return 0.
    if u>=stop:return 1.
    if i not in SYNC:return u/stop
    a,b=0.,0.
    for phrase,wanted in SYNC[i]:
        x=clamp(g.cue(phrase,wanted*stop),a+.002,stop-.014)
        if u<=x:
            return mix(b,wanted,(u-a)/(x-a))
        a,b=x,wanted
    return mix(b,1,(u-a)/(stop-a))

def draw(g,i,t,duration):
    stop=(duration-HOLDS[i])/duration
    SCENES[i](g,scene_clock(g,i,clamp(t/duration),stop))
