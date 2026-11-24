"""Freshness, ecological validity, and the return to the opening word strip."""
from visual import *
import itertools

def grow(u,a,b): return step(u,a,b)
def cue(g,u,phrase,fallback,clear=.10):
    at=g.cue(phrase,fallback) if hasattr(g,'cue') else fallback
    return step(u, at-clear*.30, at+clear*.70)
def stripe(g,x,y,lengths,color=MUTED,alpha=1,gap=19,width=2.8):
    for k,l in enumerate(lengths): g.line(x,y+gap*k,x+l,y+gap*k,color,width,alpha*(.72 if k==0 else .46))
def ledger(g,x,y,scale=1,alpha=1,kind='order',accent=GOLD):
    """Document icon, center anchored, with real content grouping."""
    if alpha<=0:return
    c=g.c
    c.save(); c.translate(x,y); c.scale(scale,scale)
    fold=24; w=166; h=204
    g.poly([(-w/2,-h/2),(w/2-fold,-h/2),(w/2,-h/2+fold),(w/2,h/2),(-w/2,h/2)],accent,2.6,alpha,True,blend(BG,accent,.06))
    g.poly([(w/2-fold,-h/2),(w/2-fold,-h/2+fold),(w/2,-h/2+fold)],accent,1.6,alpha*.7)
    if kind=='bill':
        g.line(-57,-57,56,-57,accent,2,alpha*.8)
        for k in range(4):
            g.line(-58,-29+k*23,56,-29+k*23,GRID,1.8,alpha)
            g.line(-42,-20+k*23,-13,-20+k*23,MUTED,2.8,alpha)
            g.line(19,-20+k*23,45,-20+k*23,accent if k==3 else MUTED,2.8,alpha*.85)
        g.line(1,-44,1,63,GRID,1.6,alpha)
    elif kind=='note':
        g.rect(-57,-70,31,27,None,accent,1.6,4,alpha*.8)
        g.line(-47,-56,-35,-56,accent,2.4,alpha*.8)
        g.line(-41,-62,-41,-50,accent,2.4,alpha*.8)
        stripe(g,-11,-63,[52,39],MUTED,alpha)
        stripe(g,-56,-10,[99,114,87,64],MUTED,alpha)
    elif kind=='plot':
        g.poly([(-52,63),(-52,-49),(-52,63),(55,63)],MUTED,1.3,alpha*.65)
        for k,hv in enumerate([36,55,43,82]):
            g.rect(-39+23*k,63-hv,13,hv,blend(BG,accent,.45),accent,1,1,alpha*.8)
    else:
        stripe(g,-54,-57,[106,82,103,61],MUTED,alpha)
        g.line(-54,42,45,42,GRID,1.7,alpha)
        stripe(g,-54,63,[45],accent,alpha)
    c.restore()
def glow(g,x,y,r,color,alpha=1):
    if alpha<=0 or r<=0:return
    c=g.c
    pat=cairo.RadialGradient(x,y,0,x,y,r)
    pat.add_color_stop_rgba(0,*rgb(color),.16*alpha)
    pat.add_color_stop_rgba(.55,*rgb(color),.08*alpha)
    pat.add_color_stop_rgba(1,*rgb(color),0)
    c.set_source(pat);c.new_path();c.arc(x,y,r,0,TAU);c.fill()
def badge(g,x,y,ok,alpha=1,r=23):
    co=GREEN if ok else RED
    g.circle(x,y,r,fill=blend(BG,co,.11),stroke=co,width=1.35,alpha=alpha)
    g.check(x,y,ok,r*.56,alpha)
def bracket(g,x1,x2,y,color=GOLD,alpha=1,up=False):
    dy=-10 if up else 10
    g.poly([(x1,y+dy),(x1,y),(x2,y),(x2,y+dy)],color,2,alpha)
def rail(g,y,x0=300,x1=1300,alpha=1):
    g.line(x0,y,x1,y,GRID,3,alpha)
    for x in range(x0,x1+1,100):g.line(x,y-5,x,y+5,GRID,1.8,alpha)

def reveal_old(g,u):
    z=grow(u,0,.15); age=cue(g,u,'旧记录',.25,.21); equal=cue(g,u,'连答案',.47,.18); flow=cue(g,u,'进了训练集',.63,.14)
    # Last frame of previous act is exactly this three-object arrangement.
    g.disk(mix(530,314,z),mix(420,457,z),A,mix(53,46,z),'A',1)
    g.disk(mix(1070,1286,z),mix(420,457,z),B,mix(53,46,z),'B',1)
    g.tile(800,420,68,62,color=GOLD,alpha=1-z,selected=True)
    mainx=mix(800,930,age)
    scale=mix(.36,1.11,z)
    ledger(g,mainx,412,scale,z,'bill',GOLD)
    badge(g,mainx+scale*73,412-scale*76,True,z*(1-.45*flow),19)
    # The red copy is under the sheet before it slides into view.
    lift=cue(g,u,'拿走这份旧卷子',.78,.19)
    ox=mix(793,659,age); oy=mix(421,413,age)+180*lift
    keep=1-lift
    ledger(g,ox,oy,1.10,age*.94*keep,'bill',blend(INK,MUTED,.56))
    for j in range(2):
        y=413+49+j*23
        g.line(ox-41,y+180*lift,ox+42,y+180*lift,RED if j==0 else GOLD,3.2,equal*.84*keep)
        g.line(mainx-41,y,mainx+42,y,RED if j==0 else GOLD,3.2,equal*.84*(1-lift*.79))
        g.line(ox+92,y+35*lift,mainx-92,y,RED if j==0 else GOLD,2,equal*.57*keep,dash=[6,7])
    g.text('旧记录',ox,566,24,MUTED,age*(1-flow*.65)*keep)
    g.text('测试题',mainx,566,24,GOLD,z*(1-flow*.65))
    if flow>0:
        g.arrow(ox-103,419,387,450,RED,2.1,flow*.83*keep,10)
        g.circle(mix(ox-105,387,flow),mix(419,450,flow),5,fill=RED,alpha=flow*keep)
        g.arc(314,457,60,-math.pi*.5,math.pi*mix(1.5,.96,lift),RED,1.3,flow*.45)
    if lift>0:
        g.arc(mainx,409,127,-math.pi*.5,mix(-math.pi*.5,math.pi*.49,lift),GOLD,1.3,lift*.57)


def change_case(g,u):
    # Rescale the bottom of the exam sheet into an order axis.
    z=grow(u,.02,.16); m=cue(g,u,'一百二',.40,.25); change=cue(g,u,'边界订单',.49,.20); result=cue(g,u,'会看规则',.63,.14); reset=cue(g,u,'搬旧答案',.75,.13)
    lx,rx=365,1235
    yy=mix(510,407,z)
    xp=lambda v: 400 + (v-90)*20
    carry=1-z
    ledger(g,mix(930,801,z),mix(412,yy,z),mix(1.11,.24,z),carry,'bill',GOLD)
    badge(g,mix(1010,924,z),mix(329,yy,z),True,carry*.58,19)
    g.line(mix(672,lx,z),yy,mix(926,rx,z),yy,GRID,3,z)
    for v in (90,100,110,120,130):
        x=xp(v); g.line(x,yy-6,x,yy+8,MUTED,1.55,z*.57); g.text(v,x,yy+39,28,MUTED,z*.9,font='math')
    o=xp(100); n=xp(120)
    q=xp(119)
    c=mix(o,n,m)
    g.rect(c,yy-22,max(0,rx-c),22,fill=blend(BG,GOLD,.24),r=2,alpha=z)
    g.line(c,yy-93,c,yy+10,GOLD,2.7,z)
    g.tile(c,yy-111,115,46,'免邮',GOLD,z,True)
    g.line(o,yy-54,o,yy+4,MUTED,1.7,m*.6,dash=[5,6])
    g.text('旧门槛',o,yy-75,24,MUTED,m*.8)
    g.circle(mix(o,q,change),yy,8,fill=GOLD,alpha=z)
    g.text('119',mix(o,q,change),yy+81,35,GOLD,change,font='math')
    rows=[(A,545,'A','¥0',False,reset),(B,650,'B','¥8',True,result)]
    for color,y,label,fee,ok,alpha in rows:
        gx,gy=(314,457) if label=='A' else (1286,457)
        g.disk(mix(gx,489,z),mix(gy,y,z),color,mix(46,31,z),label)
        g.line(532,y,1001,y,GRID,2,z)
        g.circle(mix(541,995,alpha),y,5,fill=color,alpha=alpha)
        g.text(fee,1061,y,51,color,alpha,font='math')
        badge(g,1130,y,ok,alpha,19)
    mark=cue(g,u,'数据污染',.89,.12)
    g.arc(o,yy,19,-math.pi*.5,math.pi*1.5,RED,1.9,mark*.62)

def ngrams(g,u):
    src=['活动','满','百','免','运','费']
    z=grow(u,0,.12)
    move=cue(g,u,'从左往右挪',.31,.39)
    win=cue(g,u,'三格滑窗',.23,.11)
    located=cue(g,u,'大仓库',.54,.17)
    exact=step(located,.84,1)
    longer=cue(g,u,'十三个词元',.73,.16)
    oldalpha=1-longer*.92
    xs=[510+j*115 for j in range(6)]
    for j,x in enumerate(xs):
        g.tile(x,297,94,76,src[j],GOLD if j in (1,2,3) else MUTED,z*oldalpha,False)
    scan=mix(xs[0],xs[3],move)
    pos=mix(scan,xs[1],located)
    g.rect(pos-57,246,344,102,None,GOLD,2.3,10,win*oldalpha)
    g.text('3-gram',pos+115,216,34,GOLD,win*oldalpha,font='math')
    evidence=(1-z)*oldalpha
    if evidence>0:
        g.circle(mix(980,855,z),mix(407,297,z),mix(8,42,z),stroke=GOLD,width=2.4,alpha=evidence)
        g.text('119',mix(980,855,z),mix(488,297,z),mix(35,23,z),GOLD,evidence,font='math')
    ys=(485,558,630)
    for j,y in enumerate(ys):
        for k in range(12):
            x=306+k*89
            col=RED if j==1 and 4<=k<=6 else MUTED
            found=j==1 and 4<=k<=6
            a=z*(.25+(.75*exact if found else .27))*oldalpha
            it=['满','百','免'][k-4] if found else ''
            g.tile(x,y,64,46,it if exact>.35 else '',blend(MUTED,col,exact) if found else col,a,found and exact>.35)
    match=exact*oldalpha
    c0=306+4*89
    for j in range(3):
        g.line(pos+j*115,358,c0+j*89,530,GOLD,1.4,match*.55,dash=[4,8])
    g.rect(c0-37,525,89*2+73,66,None,RED,2.2,8,match)
    for j in range(13):
        x=284+j*86
        p=step(longer,j*.025,.50+j*.025)
        g.tile(x,432,65,61,'',GOLD,p,True)
    bracket(g,249,1350,490,GOLD,longer)
    g.text('13-gram',800,550,58,GOLD,longer,font='math')

def span_case(g,u):
    z=grow(u,0,.14); head=cue(g,u,'公共页眉',.26,.16); para=cue(g,u,'重新说',.43,.16); cut=cue(g,u,'只切走',.65,.17); whole=cue(g,u,'扔掉整页',.79,.16)
    sl=1-cut
    # The long matching window becomes snippets inside two concrete pages.
    for j in range(13):
        group=j>=6
        k=j-6 if group else j
        dx=(1060 if group else 540)-142+(k%6)*56
        dy=338+(51 if k>=6 else 0)
        go=step(z,j*.022,.59+j*.031)
        g.tile(mix(284+j*86,dx,go),mix(432,dy,go),mix(65,43,go),mix(61,28,go),'',
               blend(GOLD,MUTED,go),1-z*.97,go<.39)
    bracket(g,249,1350,490,GOLD,1-z)
    for idx,(x,label) in enumerate([(540,'相同页眉'),(1060,'原题改写')]):
        yy=420+mix(0,-65,cut)
        a=z*sl
        g.rect(x-192,yy-121,384,242,fill=blend(BG,MUTED,.05),stroke=GRID,width=2,r=8,alpha=a)
        for j in range(4):
            yy2=yy-82+j*51
            for k in range(6):
                cx=x-142+k*56
                found=(idx==0 and j==0 and k<3)
                col=blend(MUTED,RED,head) if found else MUTED
                if idx==1 and j==2 and 1<=k<=4:col=blend(MUTED,GOLD,para*.60)
                g.tile(cx,yy2,43,28,'',col,a*(1 if found else .57),found and head>.4)
        if idx==0:
            bracket(g,x-167,x-6,yy-103,RED,head*a)
            g.text(label,x,yy+169,30,RED,head*a)
        else:
            g.line(x-101,yy+44,x+125,yy+44,GOLD,2.4,para*a)
            g.text(label,x,yy+169,30,GOLD,para*a)
    if cut>0:
        for idx,x in enumerate((550,1050)):
            a=cut*(1 if idx==0 else whole)
            push=whole if idx else cut
            if idx==0:
                ledger(g,x,418,1.34,a,'order',MUTED)
                g.rect(x-79,416,158,53,fill=blend(BG,RED,.25),stroke=RED,width=1.9,r=3,alpha=a*.76)
                g.rect(x-80,416+push*138,160,53,fill=blend(BG,RED,.7),stroke=RED,width=1.9,r=3,alpha=a)
            else:
                ledger(g,x,418+push*123,1.34,a*(1-.53*push),'order',RED)
                g.line(x-118,494,x+119,494,RED,2.15,a*.65)
            g.text(('局部剔除','整页剔除')[idx],x,719,29,RED,a*.94)

def question_card(g,x,y,n,alpha=1,selected=False,scale=1):
    c=g.c; c.save(); c.translate(x,y); c.scale(scale,scale)
    col=GOLD if selected else MUTED
    g.rect(-77,-57,154,114,fill=blend(BG,col,.08),stroke=col,width=2.1,r=8,alpha=alpha)
    g.text(n,-43,-2,49,col,alpha,font='math')
    g.line(-10,-19,52,-19,MUTED,2.6,alpha*.8)
    g.line(-10,-3,43,-3,MUTED,2.6,alpha*.6)
    g.line(-10,22,26,22,GOLD,2.7,alpha*.9)
    c.restore()

def order(g,u):
    z=grow(u,.00,.13); orders=cue(g,u,'公开文件',.52,.15); swap=cue(g,u,'交换几个',.66,.32)
    g.disk(800,mix(449,226,z),A,46,'A',z)
    g.arc(800,226,67,math.pi*.08,math.pi*.92,GRID,1.6,z)
    g.text('训练集',1100,223,27,MUTED,z*(1-orders)*.9)
    g.rect(1036,186,128,74,None,GRID,1.7,8,z*(1-orders))
    g.line(1051,250,1149,197,RED,2,z*(1-orders)*.78)
    for j,x in enumerate((563,800,1037)):
        xx=mix(800,x,z)
        question_card(g,xx,381,j+1,z,orders>.4,1)
        if orders>0:question_card(g,xx,560,j+1,orders*.85,False,1) if j==1 else None
    g.text('原顺序',327,381,27,GOLD,orders,align='right')
    g.text('重排',327,560,27,MUTED,orders,align='right')
    arcs=[(563,1037,76),(1037,563,-57)]
    for j,(x,d,yoff) in enumerate(arcs):
        xx=mix(x,d,swap); yy=560+math.sin(math.pi*swap)*yoff
        question_card(g,xx,yy,(1,3)[j],orders*.92,False)
    if swap>0 and swap<.999:
        g.arc(800,560,238,math.pi*1.015,math.pi*1.1,MUTED,1.8,orders*.5)

PERMS=(0,1,1,2,2,2,3,3,3,3,4,4,4,4,4,4,5,5,5,5,5,6,6,6,6,7,7,7,8,8,9)
def score_order(g,u):
    thick=cue(g,u,'题叠加厚',.16,.16)
    fold=grow(u,.03,.30)
    z=grow(u,.12,.31); n=cue(g,u,'多打乱几次',.21,.41); canon=cue(g,u,'出厂顺序',.44,.17); cond=cue(g,u,'可以交换',.66,.17); dates=cue(g,u,'按日期排',.80,.16)
    y=592; lx=348; w=914
    g.disk(800,mix(226,309,fold),A,mix(46,17,fold),'A',1-fold)
    for j in range(6):
        j0=j%3; orderx=[563,800,1037][j0]
        is_new=j>=3
        end_x=1115 if is_new else 1170
        for row,yy in enumerate((381,560)):
            xx=mix(orderx,800+(j-2.5)*113,thick*(1-fold))
            endx=end_x if row==0 else 465+4*59
            y0=yy-(25*thick if is_new else 0)
            card_alpha=(1-fold)*((.87 if row else 1)*(thick if is_new else 1))
            question_card(g,mix(xx,endx,fold),mix(y0,566,fold),[1,2,3,4,5,6][j if row==0 else ([2,1,0,3,5,4][j])],card_alpha,row==0,1-.83*fold)
    g.text('原顺序',327,381,27,GOLD,(1-fold)*.9,align='right')
    g.text('重排',327,560,27,MUTED,(1-fold)*.85,align='right')
    g.arrow(lx,y,lx+w,y,MUTED,1.7,z,10)
    g.text('顺序的联合对数概率',800,668,27,MUTED,z,font='serif')
    g.text('重排',291,472,27,MUTED,z*.87,align='right')
    stacks={}
    for j,b in enumerate(PERMS):
        stacks[b]=stacks.get(b,0)+1
        x=465+b*59; y2=y-19-24*(stacks[b]-1)
        a=step(n,j/len(PERMS)*.67,j/len(PERMS)*.67+.25)
        g.circle(x,y2,8.8,fill=blend(BG,MUTED,.41),stroke=MUTED,width=1.15,alpha=a)
    gx=mix(1170,1160,dates)
    g.line(gx,y-212,gx,y+2,GOLD,1.7,canon*.76,dash=[5,8])
    glow(g,gx,y-20,58,GOLD,canon)
    g.circle(gx,y-19,9,fill=GOLD,alpha=canon)
    g.text('原顺序',gx,y-249,30,GOLD,canon)
    memorize=cue(g,u,'背过整叠',.55,.22)
    if memorize>0:
        a=memorize*(1-dates)
        for j in range(3):
            question_card(g,1033+j*34,261-j*9,j+1,a*(.48+.26*j),j==2,.42)
        g.arrow(1125,273,gx-6,338,GOLD,1.7,a*.64)
    g.arc(gx,y-19,mix(12,22,cond),-math.pi*.5,math.pi*1.5,GOLD,1.35,cond*(1-dates)*.66)
    if dates>0:
        for j in range(3):
            xx=577+j*222
            g.tile(xx,291,143,54,('周一','周二','周三')[j],RED,dates*.92)
            if j:g.arrow(xx-141,291,xx-85,291,RED,2,dates*.6)
        g.arc(gx,y-19,24,-math.pi/2,math.pi*1.5,RED,2.1,dates)

def lock(g,x,y,a):
    g.arc(x,y-8,15,math.pi,TAU,GOLD,2.35,a)
    g.rect(x-21,y-7,42,33,fill=blend(BG,GOLD,.2),stroke=GOLD,width=2.35,r=5,alpha=a)
    g.circle(x,y+7,3.2,fill=GOLD,alpha=a)
def time_split(g,u):
    z=grow(u,.00,.13); cutoff=cue(g,u,'截止点',.29,.15); later=cue(g,u,'明确发布时间',.43,.18); lcb=cue(g,u,'LiveCodeBench',.59,.13); private=cue(g,u,'私测',.76,.18)
    y=mix(592,450,z)
    g.arrow(mix(348,256,z),y,mix(1262,1345,z),y,MUTED,2.4,.65+.35*z,12)
    g.text('时间',1368,y,25,MUTED,z,align='left')
    for j,x in enumerate((410,542,672)):
        a=step(z,j*.11,.60+j*.11)
        g.tile(x,y-67,62,58,'',MUTED,a)
        g.line(x,y-31,x,y-5,GRID,1.7,a)
    x=800
    g.line(x,252,x,532,BLUE,2.4,cutoff)
    g.disk(x,235,A,34,'A',cutoff)
    g.text('数据截止',x,575,27,BLUE,cutoff)
    for j,x in enumerate((922,1056,1190)):
        a=step(later,j*.09,.60+j*.09)
        g.tile(x,y-67,62,58,'',GOLD,a,True)
        glow(g,x,y-68,46,GOLD,a*.62)
        g.line(x,y-31,x,y-5,GOLD,1.55,a*.74)
    bracket(g,887,1225,482,GOLD,lcb)
    g.text('LiveCodeBench',1054,539,31,GOLD,lcb,font='serif')
    for j in range(2):
        xx=1060+j*57
        g.tile(xx,665-j*4,56,46,'',GOLD,private*.35)
    lock(g,1086,664,private)
    g.text('私测',1182,670,27,GOLD,private)

def link_bundle(g,x,y,a):
    for j,((k,ac),(xx,yy)) in enumerate(zip([('order',GOLD),('order',GOLD),('order',MUTED)],[(x-35,y+21),(x+30,y-8),(x-14,y-20)])):
        ledger(g,xx,yy,.62,a*(.64 if j<2 else 1),k,ac)
def routine(g,u):
    z=grow(u,0,.13); context=cue(g,u,'优惠券',.34,.16); deliver=cue(g,u,'交来的表格',.54,.21); gap=cue(g,u,'选一个数',.75,.17)
    shift=step(u,.07,.4)
    px=mix(1190,412,shift)
    arc_y=mix(383,408,shift)-36*math.sin(math.pi*shift)
    g.tile(px,arc_y,mix(62,92,shift),mix(58,72,shift),'',GOLD,1-z,True)
    link_bundle(g,px,arc_y,z)
    x=689
    g.arrow(515,408,x-54,408,MUTED,2,context*.85)
    g.tile(x,408,97,76,'优惠',GOLD,context)
    g.arrow(x+55,408,833,408,MUTED,2,context*.85)
    g.tile(893,408,99,76,'运费',GOLD,context,True)
    g.arrow(950,408,1083,408,MUTED,2,deliver)
    ledger(g,1200,408,1.29,deliver,'bill',GOLD)
    badge(g,1289,484,True,deliver,20)
    if gap>0:
        g.tile(412,658,93,58,'¥0',MUTED,gap)
        g.arrow(467,658,1112,658,MUTED,1.8,gap*.45)
        g.line(784,638,813,675,RED,2.3,gap*.9)
        g.line(812,638,785,675,RED,2.3,gap*.9)

def person(g,x,y,a):
    g.circle(x,y-25,15,stroke=MUTED,width=2.15,alpha=a)
    g.arc(x,y+26,28,math.pi,TAU,MUTED,2.15,a)
def benchmarks(g,u):
    z=grow(u,0,.13); gd=cue(g,u,'GDPval',.22,.17); expert=cue(g,u,'熟悉工作',.42,.12); med=cue(g,u,'MedHELM',.56,.18); separate=cue(g,u,'另一种',.75,.19)
    both=step(med,0,.5); yy=mix(434,328,both)
    match=cue(g,u,'对不对得上',.28,.17)
    relevance=cue(g,u,'题目越像',.03,.29)
    pre=1-gd
    # Carry the invoice and order bundle over. The small arithmetic answer alone
    # can't close this gap; real attachments physically spread along the path.
    mix_x=mix(412,610,gd)
    link_bundle(g,mix_x,mix(408,yy,gd),pre)
    ledger(g,mix(1200,1031,gd),mix(408,yy,gd),mix(1.29,.72,gd),pre,'bill',GOLD)
    g.tile(mix(698,559,relevance),615,80,54,'¥0',MUTED,pre*(1-relevance))
    points=[(517,408),(mix(605,728,relevance),408),(mix(802,986,match),408),(1084,408)]
    for j in range(3):
        a=relevance if j==0 else match
        g.line(*points[j],*points[j+1],GOLD,2.1,pre*a*.64,dash=None if j==1 else [6,8])
    if relevance>0:
        f=clamp(relevance*.73+match*.27)
        g.circle(mix(527,1084,f),408,5,fill=GOLD,alpha=pre)
    g.text('GDPval',289,yy,36,INK,gd,align='left',font='serif')
    link_bundle(g,610,yy,gd)
    g.arrow(706,yy,792,yy,MUTED,2,gd)
    ledger(g,864,yy,.72,gd,'plot',A)
    ledger(g,1031,yy,.72,gd,'plot',B)
    person(g,1232,yy+5,expert)
    g.arrow(1197,yy,1102,yy,MUTED,1.9,expert)
    badge(g,1073,yy+59,True,expert,15)
    g.line(288,450,1292,450,GRID,1.3,med*.8)
    g.text('MedHELM',289,586,36,INK,med,align='left',font='serif')
    ledger(g,611,586,.75,med,'note',GOLD)
    g.arrow(701,586,814,586,MUTED,1.9,med)
    g.line(825,586,898,mix(586,547,separate),MUTED,2,med)
    g.line(825,586,898,625,MUTED,2,separate)
    for j,(name,y,a) in enumerate((('记录整理',mix(586,547,separate),med),('决策支持',625,separate))):
        g.tile(985,y,157,51,name,GOLD,a)
        g.line(1067,y,1194,y,GRID,2,a)
        g.circle(1189,y,5,fill=GOLD,alpha=a)

def test_rows(g,u):
    z=grow(u,.00,.12); border=cue(g,u,'踩线',.36,.16); unusual=cue(g,u,'退一半',.64,.20); avg=cue(g,u,'平均数',.88,.12)
    inputs=cue(g,u,'订单记录',.14,.16)
    outputs=cue(g,u,'准确账单',.30,.18)
    ledger(g,mix(611,475,inputs),mix(586,285,inputs),mix(.69,.33,inputs),(1-inputs)*.89,'order',GOLD)
    ledger(g,mix(1031,1090,outputs),mix(328,285,outputs),mix(.72,.32,outputs),(1-outputs)*.89,'bill',GOLD)
    g.text('订单',475,199,28,MUTED,inputs)
    g.text('正确账单',1090,199,28,MUTED,outputs)
    rules=cue(g,u,'退款后的金额',.69,.14)
    regress=cue(g,u,'改错和误伤',.47,.18)*(1-unusual)
    arr=[('¥119','¥8',GOLD,border),('¥120','¥0',GOLD,border),('退一半','',GOLD,unusual)]
    for j,(price,fee,col,a) in enumerate(arr):
        y=284+j*146
        zz=step(inputs,j*.16,.63+j*.19)
        oo=step(outputs,j*.11,.63+j*.19)
        aa=zz if j<2 else a
        text_color=blend(MUTED,col,a)
        if j<2:
            g.tile(mix(427,475,zz),y,172,69,price,text_color,aa,True)
            g.tile(mix(1138,1090,oo),y,163,69,fee,text_color,oo,True)
            badge(g,1235,y,True,a,19)
            g.circle(mix(576,989,oo),y,5,fill=GOLD,alpha=oo*(1-oo)*2.1)
            if regress>0:
                miss='¥0' if j==0 else '¥8'
                rp=step(regress,j*.21,.62+j*.24)
                sx=mix(643,796,rp)
                g.tile(sx,y,89,47,miss,RED,rp)
                g.check(mix(770,875,rp),y,False,14,rp)
        else:
            g.tile(475,y,mix(172,242,rules),69,'',text_color,aa,True)
            if rules<.5:
                g.text(price,475,y-11*rules,33,text_color,aa*(1-2*rules),weight='medium')
            else:
                g.text('¥120 − ¥60',475,y+11*(1-rules),31,GOLD,2*rules-1,font='math')
            g.tile(1090,y,163,69,'',text_color,aa,True)
            g.text('¥8',1090,y,35,GOLD,rules,font='math')
            g.rect(328,y-48,972,96,None,RED,1.6,7,avg)
        g.arrow(597 if j==2 else 575,y,mix(575,993,oo) if j<2 else 993,y,MUTED,1.8,(oo if j<2 else aa)*.73)
    bracket(g,429,1137,691,RED,avg,True)

def decision(g,u):
    z=grow(u,.01,.16); s=cue(g,u,'紫模型',.37,.19); a_fast=cue(g,u,'蓝模型动得更快',.52,.1); fails=cue(g,u,'都出了错',.62,.17); decide=cue(g,u,'哪类订单',.83,.18)
    # Expected charges collapse onto the test rows while the model branches
    # move into place. The new check operation starts on those same orders.
    for j,(fee,st) in enumerate((('¥0','¥120'),('¥8','¥120 − ¥60'))):
        yy=(430,576)[j]; dst=(375,519)[j]
        x=mix(475,465,z);y=mix(yy,dst,z)
        w=mix(242 if j else 172,108,z)
        g.tile(x,y,w,mix(69,52,z),'',GOLD,(1-z)*.90,True)
        g.text(st,x,y,min(33,w*.129 if j else w*.19),GOLD,(1-z)*.90,font='math')
        g.tile(mix(1090,1038,z),y,mix(163,82,z),mix(69,54,z),fee,GOLD,(1-z)*.90,True)
        g.line(mix(560,532,z),mix(yy,dst,z),mix(1008,997,z),mix(yy,dst,z),GRID,2,1-z)
    g.disk(mix(645,697,z),mix(223,235,z),A,42,'A',z)
    g.disk(mix(1055,1003,z),mix(223,235,z),B,42,'B',z)
    g.line(354,307,1251,307,GRID,1.8,z)
    g.line(354,448,1251,448,GRID,1.35,z)
    g.line(354,589,1251,589,GRID,1.35,z)
    g.text('门槛',465,375,31,GOLD,z)
    g.text('退货',465,519,31,GOLD,z)
    badge(g,697,373,False,s,28);badge(g,1003,373,True,s,28)
    badge(g,697,516,False,fails,28);badge(g,1003,516,False,fails,28)
    g.text('耗时',465,650,27,MUTED,a_fast)
    g.line(617,652,777,652,GRID,5,a_fast)
    g.line(923,652,1083,652,GRID,5,a_fast)
    g.line(617,652,617+73*a_fast,652,A,5.8,a_fast)
    g.line(923,652,923+131*a_fast,652,B,5.8,a_fast)
    if decide>0:
        g.arrow(1040,373,1142,373,GREEN,2,decide)
        g.arrow(1040,516,1142,516,MUTED,2,decide)
        g.text('验收',1230,373,28,GREEN,decide)
        g.text('人工',1230,516,28,MUTED,decide)

WORD='二加二等于四'
def finale(g,u):
    z=grow(u,0,.13); advantage=cue(g,u,'赚下来的优势',.31,.18); last=cue(g,u,'最后一格',.57,.14); outside=cue(g,u,'没进考卷',.90,.11)
    lose=.78*outside
    g.disk(mix(697,180,z),mix(235,442,z),A,42,'A',1-lose)
    g.disk(mix(1003,180,z),mix(235,572,z),B,42,'B',1-lose)
    for y in (307,448,589):
        g.line(mix(354,292,z),mix(y,257,z),mix(1251,1266,z),mix(y,257,z),GRID,1.5,(1-z)*.55)
    for j,ch in enumerate(WORD):
        x=363+158*j
        b=step(z,j*.07,.64+j*.06)
        is_last=j==5
        co=GOLD if is_last else blend(MUTED,GOLD,.50)
        al=b*(1-lose if not is_last else 1-outside*.38)
        g.tile(x,257,104,84,ch,co,al,is_last)
        if not is_last:
            for col,y,v in ((A,442,.90),(B,572,.60)):
                g.line(x-45,y,x+45,y,GRID,7,b*(1-lose))
                g.line(x-45,y,x-45+90*v*advantage,y,col,7,b*(1-lose))
        else:
            for col,y,let,ok in ((A,442,'五',False),(B,572,'四',True)):
                g.tile(x,y,96,75,let,GOLD if ok else col,z*(1-outside*.38),ok)
                g.check(x+72,y,ok,14,last*(1-outside*.6))
            g.rect(x-69,192,138,430,None,GOLD,2.1,13,last*(1-outside*.48))
    nx=mix(1285,1350,outside)
    if outside>0:
        glow(g,nx,444,100,GOLD,outside)
        g.rect(nx-57,401,114,86,None,GOLD,2.8,9,outside)
        g.text('？',nx,444,42,GOLD,outside,font='serif')
        g.line(1229,444,nx-60,444,GOLD,1.4,outside*.72,dash=[3,8])

SCENES=(reveal_old,change_case,ngrams,span_case,order,score_order,time_split,routine,benchmarks,test_rows,decision,finale)
def draw(g,i,t,duration):
    SCENES[i](g,clamp(t/duration))
