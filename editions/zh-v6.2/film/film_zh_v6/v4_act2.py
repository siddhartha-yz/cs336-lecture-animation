"""A single lamp, then a single denominator. All plotted probabilities come from the archived forwards."""
from rig4 import *
from motion import formula
from ppl_chalk import five_twenty
DATA=json.loads((W.parent/'beat2/verified-data.json').read_text());OP=DATA['opening'];REV=DATA['rank_reversal'];PAL=DATA['paloma']['domains']
def tokens(g,c):
 t=c.t;first=c.at('假如词表')-.26;five=c.at('一排分成五格')-.23
 bridge=first-.45
 if t<first:
  # The same observed word controls its conditional distribution, the selected factor
  # in the product and, after a change of units, the corresponding information bar.
  pre=c.at('原文接下去');walk=c.at('沿原文');moving=c.at('每走一步');last=c.at('乘起来')
  v=phase(t,moving-.14,last-.37);raw=2+5*v;j=min(7,int(raw));phase2=raw-j
  j2=min(j+1,7);z=p5(clip((phase2-.47)/.53));morph=c.u('取负对数',.94);token_x,step=182,172
  change=c.at('是模型给这整段')-.20
  lecture=easepos(t,change+.25,.61)
  up=1-easepos(t,change,.65)
  if lecture:
   from length_chain6 import reading
   _,_,current,power=reading(c)
  else:current,power=7,0.
  label(g,'The room was quiet.',153,105,38,M,up,'left');label(g,'前文',153,154,25,T,up,'left')
  yrow=mix(244,218,morph)
  for i,(tok,p0)in enumerate(zip(OP['tokens'],OP['probabilities'])):
   if t>=bridge:break # The same eight box outlines are now carried by uniform_example.
   op=1.;x=token_x+i*step;active=(1-z if i==j else z if i==j2 else 0)
   if i==j==j2:active=1
   active=mix(active,float(i==current),power*lecture)
   active=mix(active,float(i==2),morph)
   pref=enter(t,c.at('读到 small')-.10,.50)*(1-phase(t,pre-.09,pre+.47))
   if i in (0,1):
    if pref:line(g,(x-59,yrow+49),(x+59,yrow+49),T,2.9,pref)
   if t<pre+.45:active*=enter(t,pre-.08,.50)
   box(g,x-70,yrow-33,140,71,blend(E,Y,active),op,inkcol(blend(M,Y,active),.086+.16*active),1.65+1.1*active)
   label(g,tok,x,yrow+1,40,blend(F,Y,active),op)
  if up>.002:
   u=enter(t,pre-.15,.6);actx=token_x+(j+(z if j2!=j else 0))*step;yy=474
   if u:
    # Keep the large lens in one seat. When the camera advances, alternate sets of
    # bars are never superimposed: switch names and heights at the midpoint.
    cur=j2 if z>.5 else j;switch=(1-2*min(z,1-z))**.52 if j!=j2 else 1
    rows=[(r['token'],r['p'],C) for r in OP['alternatives'][cur]]+[(OP['tokens'][cur],OP['probabilities'][cur],Y)]
    path(g,[(actx,yrow+42),(actx,yrow+68),(670,333),(670,357)],u,T,1.95,up*.86)
    vmax=.10+.50*phase(t,moving-.22,moving+.60);axisy=593
    st0=pre-.08 if cur!=2 else c.at('语言模型逐个')-.22
    for k,(n,p0,col)in enumerate(rows):
     # Three rival words appear as alternatives, the observed word already points to the verbatim continuation.
     gate=enter(t,st0+.32*k,.52) if k!=3 and cur==2 else u
     x=439+k*188;h=226*p0/vmax;h=max(1.42,h)*gate*switch
     rect(g,x-39,axisy-h,78,h,col,up*gate);label(g,n,x,axisy+33,31,col,up*gate*switch)
     label(g,(f'{p0*100:.4f}%' if p0<.001 else f'{p0*100:.2f}%'),x,axisy-h-25,27,col if k==3 else M,up*gate*switch)
    line(g,(345,axisy+1),(1103,axisy+1),M,1.6,up*u)
    label(g,'局部刻度 10%' if vmax<.11 else '固定刻度 60%',341,axisy-209,21,M,up*u,'right')
    q=enter(t,walk-.11,.61);full=OP['probabilities'];pr=math.prod(full[:cur+1])
    if q:
     # A mantissa is too abstract to feel the contraction: each contributed factor steps down the same log ruler.
     label(g,'沿原文连乘',1280,401,31,T,q*up);label(g,f'{pr:.2e}',1281,464,36,Y,q*up)
     yb=602;xl=1158;xr=1439;loglo=-13
     def lx(n):return xl+(xr-xl)*clip(-math.log10(max(1e-30,n))/-loglo)
     line(g,(xl,yb),(xr,yb),M,1.5,q*up)
     for dec in (0,4,8,12):
      tickx=lx(10**-dec);line(g,(tickx,yb-5),(tickx,yb+7),M,1.7,q*up);label(g,('1','10⁻⁴','10⁻⁸','10⁻¹²')[dec//4],tickx,yb+31,20,M,q*up)
     for ki in range(cur+1):
      tickx=lx(math.prod(full[:ki+1]));dot(g,tickx,yb,3.8,C if ki<cur else Y,q*up)
     point(g,lx(pr),yb,6.1,Y,q*up)
    else:
     from probe_next6 import condition
     condition(g,c,tuple(token_x+i*step for i in range(3)),yrow,OP['probabilities'][2],up*u)
     note=during(t,c.at('语言模型逐个')-.14,c.at('条件概率')-.12,.48)
     if note:label(g,'词表中的四项',1266,437,29,M,up*u*note)
   label(g,'SmolLM2-135M  ·  实测条件概率',800,727,26,M,u*up*(1-phase(t,c.at('连乘起来')-.65,c.at('连乘起来')-.04)))
  if lecture:
   from length_chain6 import render
   render(g,c,OP,tuple(token_x+i*step for i in range(8)),yrow,lecture,first)
  if t>=bridge:uniform_example(g,c,first,bridge)
 elif t<five:
  uniform_example(g,c,first,bridge)
 else:
  from probability5 import paths100
  paths100(g,c,five)


def uniform_example(g,c,first,bridge):
 t=c.t;u=enter(t,first+.19,.67);ten=c.at('压到了十');switch=phase(t,ten-.10,ten+1.02)
 grid=1-clip(switch/.64);frac=clip((switch-.70)/.30);seen=c.at('每一格都是十分之一')
 cw=122.8;gap=7;xl=154;cy=413
 gop=u*grid
 if gop:
  label(g,'十万个等可能词',800,168,43,T,gop)
  label(g,'每一小点代表 100 个词',802,235,28,M,gop)
 for i in range(10):
  z=easepos(t,bridge+.026*i,1.02);x=xl+i*(cw+gap)
  mid=x+cw/2;co=Y if i==2 else E
  if i<8:
   xx,yy=transit((182+172*i,218),(mid,cy),z,18.-i*3.)
   width=mix(140,cw,z);height=mix(71,113,z);a=1.
  else:
   previous=easepos(t,bridge+.026*7,1.02)
   xx,yy=mid,cy+18*(1-z);width=cw*(.45+.55*z);height=mix(71,113,z)
   a=phase(previous,.977,.999)*phase(z,.57,.98)
  blink=math.exp(-((t-seen-i*.068)/.145)**2)*frac
  box(g,xx-width/2,yy-height/2,width,height,blend(co,blend(C,Y,blink),z),a,
      blend(inkcol(Y,.246) if i==2 else inkcol(M,.086),inkcol(C,.33+.11*frac),z),2.05)
  if i<8 and z<.58:label(g,OP['tokens'][i],xx,yy+1,40,Y if i==2 else F,1-phase(z,.06,.58))
  cells=a*grid*phase(z,.77,1)
  if cells:
   for h0 in range(10):
    for kk in range(10):
     cx=xx+(-cw/2+9+kk*11.1)*width/cw;sy=yy+(-48+h0*10.2)*height/113
     rect(g,mix(xx,cx,grid)-3.3,mix(yy-2,sy,grid)-3.0,6.6,6.1,T if kk%3 else C,cells)
  if frac:label(g,'1/10',mid,cy,36,F,a*frac)
  if blink>.01:line(g,(x+5,cy+53),(x+cw-5,cy+53),Y,5.4,blink)
 if gop:
  label(g,'10 × 100 × 100 = 100,000',799,576,49,F,gop)
  label(g,'PPL = 100,000',800,687,37,Y,c.u('就是十万',.46)*grid)
 if frac:
  label(g,'等可能',800,209,41,T,frac);label(g,'PPL = 10',800,614,58,Y,frac)
def byte(g,c):
 from byte6 import bpb6
 bpb6(g,c)
def jointlens(g,c,stop):
 """Four outcomes make a complete joint distribution. Conditioning literally stretches a row to 100%."""
 t=c.t;on=enter(t,.02,.64);ideal=c.at('题目和答案')-.23;take=c.at('给定题目')-.17;choice=c.at('得分规则')-.13;lim=c.at('工程现实')-.17;different=c.at('两条曲线')-.29
 q=enter(t,ideal,1.14);sel=enter(t,take,.87);choose=enter(t,choice,.66);theory=enter(t,lim,.68);changed=.27*phase(t,lim+.29,c.at('真的逼近')+.44)+.73*phase(t,different,different+1.39)
 lhs=169;bw=539;bh=116;rowys=(306,465);r=tuple(rowys)
 # The true mass under the first input totals 40%; the other 60% belongs to the second input.
 label(g,'题目与答案',lhs,149,40,F,on,'left');label(g,'示意联合分布',lhs+2,200,24,M,on,'left')
 for j,(y,p1,p2) in enumerate(((r[0],.30,.10),(r[1],.12,.48))):
  av=on*(1-.77*sel if j else 1);label(g,'题 '+('A','B')[j],lhs-28,y+bh/2,29,(O,M)[j],av,'right')
  for i,(p0,col)in enumerate(((p1,C),(p2,V))):
   x=lhs+((p1/.60*bw) if i else 0);w=p0/.60*bw;v=enter(t,.25+.17*(2*j+i),.61)
   rect(g,x+1,y,w*v-2 if w*v>2 else 0,bh,inkcol(col,.49 if j==0 else .41),av)
   if v>.05:line(g,(x+1,y),(x+max(2,w*v-2),y),col,2.4,av*v)
   if v>.35:label(g,f'{p0:.0%}',x+w*.50,y+bh/2,32,F,av*v)
  if not j:
   # Same proportions, a different denominator. The two bundles physically travel right and grow.
   qq=q*(1-.6*sel)
   if qq:label(g,'A 与 α',lhs+130,y-36,25,C,qq);label(g,'A 与 β',lhs+322,y-36,25,V,qq)
 if q:label(g,'四格相加 = 100%',lhs+228,661,29,M,q)
 if sel:
  stw=563;xx=875;yy=327;bh2=112;w0=.30/.40;mixup=.35*changed
  target=.75-mixup
  xx_a=lhs;original=[(.30,.0),(.10,.30)];lr=(C,V)
  for i,(val,off)in enumerate(original):
   init=lhs+bw*off/.60;srcw=val*bw/.60;tarx=xx+(target*stw if i else 0);tarw=stw*((1-target)if i else target)
   x=mix(init,tarx,p5(sel));y=mix(rowys[0],yy,p5(sel))-41*sin(pi*sel);w=mix(srcw,tarw,sel)
   rect(g,x+1,y,w-2,bh2,inkcol(lr[i],.65),sel);line(g,(x+1,y),(x+w-1,y),lr[i],2.6,sel)
   ss=target if i==0 else 1-target
   if sel>.86:label(g,f'{ss:.0%}',x+w/2,y+bh2/2,39,F,sel)
  mark(g,'Q(答案 | 题 A)' if theory>.5 else 'P(答案 | 题 A)',xx+281,186,42,t-take,T,op=sel)
  label(g,'模型估计' if theory>.5 else '只保留 A，再归一化',xx+281,246,25,M,sel)
  if changed:
   xx0=xx+stw*.75;line(g,(xx0,yy-23),(xx0,yy+5),F,1.8,changed);label(g,'真实 75%',xx0,yy-47,23,F,changed)
  if choose:
   label(g,'α',xx+stw*target*.5,yy+bh2+47,35,C,sel)
   label(g,'β',xx+stw*(1+target)*.5,yy+bh2+47,35,V,sel)
   pos=xx+(stw*target*.5 if target>=.5 else stw*(1+target)*.5)
   top=yy+bh2+70
   if abs(target-.50)>=.005:path(g,[(pos-32,top),(pos+32,top)],choose,Y,3.75,sel)
  if not theory:label(g,'30% ÷ 40% = 75%',xx+279,654,37,Y,sel*choose)
 if theory:
  # Piecewise-linear frequency polygons compare four *discrete* masses, read at their dots.
  vals=[.30,.10,.12,.48];mods=[.30-.14*changed,.10+.14*changed,.12,.48]
  xs=[903+152*j for j in range(4)];baseline=735;sc=228
  for vv,col,off in ((vals,F,0),(mods,C,1)):
   pts=[(x,baseline-v*sc)for x,v in zip(xs,vv)]
   path(g,pts,theory,col,2.4 if off else 4.7,theory)
   for x,y in pts:
    if off:dot(g,x,y,3.65,C,theory)
    else:ring(g,x,y,5.5,F,theory,1.6)
  label(g,'真实',892,561,23,F,theory);label(g,'模型',987,561,23,C,theory)
  # When the two laws start to separate, follow one mass unit across the
  # pair. The left distribution never changes; the competing model's total
  # for this question remains 40%. A tiny miss can leave the decision intact.
  inspect=c.at('真的逼近');index=c.at('刚刚低了')
  for j,(i0,i1,at0,dt) in enumerate(((0,1,lim+.42,inspect-lim),(0,1,different+.02,1.21))):
   v=clip((t-at0)/max(.48,dt))
   if 0<v<1:
    u=p5(v);x,y=transit((xs[i0],baseline-sc*mods[i0]),(xs[i1],baseline-sc*mods[i1]),u,-28)
    dot(g,x,y,5.8,O,sin(pi*v)**.35*theory)
  if inspect-.17<t<different+.75:
   ap=during(t,inspect-.17,different+.75,.46)
   if ap:
    # A fitted average and a conditional answer are different objects.
    lab='逐项对照' if t<index-.08 else '只报一个平均数'
    label(g,lab,450,740,30,T if t<index-.08 else M,ap)
    if t<index-.08:
     v=phase(t,inspect-.15,index-.28);j=min(3,int(4*v));x=xs[j];y=baseline-mods[j]*sc
     ring(g,x,y,12,O,ap,2.1)
    else:
     for j,x in enumerate((344,417,490,563)):
      v=phase(t,index-.09+.08*j,index+.90+.08*j)
      y=705;dot(g,mix(x,450,v),mix(y,686,v),4,T,ap)
  if changed>.05 and t>different+.58:
   ok=target>.5
   if not ok and abs(target-.50)>=.005:swish(g,xx+stw*target+41,xx+stw-43,top+19,t-different-.77,Y,.68,2.45)
 if t>stop-.46:shade(g,phase(t,stop-.46,stop))

def reversal(g,c):
 t=c.t;show=c.at('来看一个小得');pick=c.at('收起整行平均数');z=phase(t,pick-.16,pick+.80)
 bars_at=c.at('比较候选答案')-.22;detail=phase(t,bars_at,bars_at+.65)
 from loss_lens6 import slots,live_losses,take_focus
 if t<show:
  jointlens(g,c,show)
  return
 end=c.at('正解是二');forms=c.at('把题干');ramp=phase(t,forms-.14,forms+1.15);l=181;labels=[s.strip()for s in REV['tokens']];ai=REV['answer_index']
 if ramp<1:
  u=enter(t,show,.63);minus=c.u('九减七',.94);select=c.u('正解是二',.50);opacity=(1-ramp)*u
  label(g,'9 − 7',800,236,85,O,opacity)
  for i in range(9):
   xx=512+i*72;rem=phase(t,c.at('九减七')+.05*(i-2),c.at('九减七')+.62+.05*(i-2)) if i>=2 else 0
   rect(g,xx-21,385+51*rem,42,42,blend(C,R,rem),opacity*(1-.88*rem))
  for j,nm in enumerate(('two','three')):
   x=649+j*306;v=1-phase(ramp,.06,.31)
   if j or not ramp:label(g,nm,x,604,47,Y if select and j==0 else F,opacity*v)
   if select and not j and ramp<.12:swish(g,x-50,x+50,645,t-end,Y,.68,3.8)
  # Two goes with the original text, toward its measured answer position.
  if ramp:
   xp,yp=transit((649,604),(l+ai*82,439),ramp,-72)
   label(g,'two',xp,yp,47-19*ramp,Y,u*(1-phase(ramp,.75,.97)))
 if ramp and z<.999:
  rows=(302,591);xx=l;alpha0=ramp*(1-z)
  early=c.u('前面许多',.74);endgap=c.u('大失误',.66)
  slots(g,c,labels,xx,82,439,ai,alpha0)
  for j,(m,col)in enumerate(zip(REV['models'],(C,V))):
   y=rows[j];alpha=alpha0*enter(t,forms+.43+j*.2,.57)
   label(g,('基础版','指令版')[j],74,y+15,25,col,alpha,'left')
   line(g,(l-29,y),(1400,y),E,1.6,alpha)
   for i,loss in enumerate(m['nll']):
    x=l+i*82;u=enter(t,c.at('从头到尾')-.31+i*.047+j*.09,.63);hi=loss*9.7
    # Separate rows have the same units and scale; leave the tokens in their own reading lane.
    rect(g,x-21,y-hi*u,42,hi*u,inkcol(col,.82),alpha)
    if i==ai and t>=end:line(g,(x-27,y+4),(x+27,y+4),Y,2.6,alpha)
   if early:
    label(g,f"前十四项  {sum(m['nll'][:-1]):.2f} nat",455,y+46,25,col,early*alpha)
   if endgap:
    label(g,f"答案  {m['nll'][ai]:.2f}",1325,y+45,25,Y,endgap*alpha)
   avg=c.u('先看整行',.58)
   if avg:
    line(g,(l-31,y-m['mean_nll']*9.7),(1402,y-m['mean_nll']*9.7),O,1.8,alpha)
    label(g,f"PPL  {m['ppl']:.2f}",943,y+43,32,col,avg*alpha)
  label(g,'同一原文  ·  逐词元负对数损失',802,744,26,M,alpha0)
  live_losses(g,c,REV['models'],labels,xx,82,alpha0)
 if t>=pick-.16 and detail<.999:
  take_focus(g,c,439,l+ai*82)
 if z:
  split=c.at('于是就有了');cross=phase(t,split-.1,split+1.12);use=detail*(1-phase(t,split-.10,split+.66));question=phase(t,pick+.69,c.at('最后那一格')+.12)*(1-phase(t,split-.10,split+.66));label(g,'9 − 7',800,131,57,Y,question);label(g,'在 two 与 three 之间作答',800,202,28,M,use)
  for j,(m,col)in enumerate(zip(REV['models'],(C,V))):
   x=(378,1002)[j];label(g,('基础版','指令版')[j],x,259,37,col,use,'left')
   ps={r['token'].strip().lower():r['p']for r in m['top'][:2]};b=586;names=('two','three')
   for i,name in enumerate(names):
    p0=ps[name];xx=x+37+i*170;h=p0*945;v=enter(t,bars_at+.09*i+.11*j,.73)
    rect(g,xx-40,b-h*v,80,h*v,inkcol(col,.77),use);label(g,f'{p0:.1%}',xx,b-h*v-29,26,F,use*v);label(g,name,xx,b+37,30,col,use)
   revat=c.at('押给了三') if j==0 else c.at('押给了二')
   v=enter(t,revat-.08,.52)
   if v*use>.001:
    win=1-j;xx=x+37+win*170;check(g,xx,b+94,15,j==1,v*use);label(g,('选三','选二')[j],xx+33,b+94,25,R if j==0 else G,v*use,'left')
  label(g,'两个候选的原始词表概率',800,742,24,M,use)
  if cross:
   # One lens, then two verdicts. Follow the same two measured points through
   # both tests; the crossed strands, not a caption, make the reversal visible.
   st=c.at('衡量全句');tb=c.at('真正盯住答案');lo,hi=442,1144;top,bottom=339,575
   names=('基础版','指令版');colors=(C,V);left=((lo,top),(lo,bottom));right=((hi,bottom),(hi,top))
   axis=enter(t,st-.17,.63);arm=phase(t,split-.13,split+.94);ans=enter(t,tb-.16,.65);first_win=c.u('基础版赢',.53);last_win=c.u('指令版赢',.48)
   label(g,'整句 PPL',lo,161,45,F,axis);label(g,'越低越好',lo,220,27,M,axis)
   if arm:
    origin_y=mix((top+bottom)/2,top-34,arm)
    end_y=mix((top+bottom)/2,bottom+36,arm)
    line(g,(lo,origin_y),(lo,end_y),blend(C,M,axis),2.,arm*.85)
   label(g,'9 − 7',hi,161,49,Y,ans);label(g,'只判最后一格',hi,220,27,M,ans)
   if ans:line(g,(hi,top-34),(hi,bottom+36),E,1.8,ans)
   for j,(m,col) in enumerate(zip(REV['models'],colors)):
    p0=max(x['p'] for x in m['top'][:2]);arg=1-j;ori=(378+624*j+37+arg*170,586-945*p0)
    pos=transit(ori,left[j],cross,(-1 if j else 1)*75)
    if cross<.999:
     # The peak being inspected is a real candidate bar. Its filled cap travels
     # while the unit label changes independently at the left-hand destination.
     ph=945*p0
     w=mix(53,11,cross);h=mix(ph*.57,11,cross)
     rect(g,pos[0]-w*.5,pos[1]-3*cross,w,h,inkcol(col,.81),cross*(1-.87*axis))
    point(g,*pos,7.8,col,cross)
    a1=enter(t,st-.10+.17*j,.51);lx,ly=left[j];rx,ry=right[j]
    label(g,f"{m['ppl']:.2f}",lx-36,ly-9,47,col,a1,'right')
    label(g,names[j],lx-38,ly+43,28,M,a1,'right')
    theta=phase(t,tb-.08+.25*j,tb+.94+.34*j)
    if theta:
     pts=[(mix(lx,rx,u/70),mix(ly,ry,p5(u/70)))for u in range(71)]
     path(g,pts,theta,col,3.7,theta)
     if theta<1:point(g,mix(lx,rx,theta),mix(ly,ry,p5(theta)),6.4,col,theta)
     if theta>.80:
      endop=clip((theta-.80)/.20);point(g,rx,ry,8.4,col,endop);label(g,('选 three','选 two')[j],rx+39,ry-2,41,col,endop,'left');check(g,rx+242,ry,17,j==1,endop)
   if first_win:ring(g,lo,top,15.1,Y,first_win,2.5)
   if last_win:ring(g,hi,top,15.1,Y,last_win,2.5)
def domains(g,c):
 t=c.t;switch=c.at('还有一道');sandbox=c.at('受控环境');read=c.at('六个领域投') if '六个领域投' in c.s['chars'] else c.at('每个领域投一票')
 if t<switch:
  main=c.at('Paloma');foc=phase(t,main-.55,main+.34);mat=enter(t,main-.30,.70);readv=enter(t,read,.8);tot=c.u('八点三二',.49)
  if t<1.30:
   b=phase(t,.07,.88);a0=1-phase(t,.84,1.30);x,y=transit((442,339),(261,347),b,-41);ring(g,x,y,mix(15.1,9.8,b),Y,a0,2.45);dot(g,x,y,6.5,blend(C,O,b),a0)
  if foc<1:
   from domains6 import weight
   weight(g,c)
  if not foc:return
  xs0=[274+208*i for i in range(6)];xs1=[247+147*i for i in range(6)];xs=[mix(x,y,readv)for x,y in zip(xs0,xs1)];width=mix(173,129,readv);names=['代码','数学','论文','百科','网页','书籍']
  panelnote(g,'Paloma','按语料领域分别测量困惑度',143,122,t-main+.08,C)
  comp=c.at('领先的一方');same=c.at('同一对十三亿');cols_at=c.at('取六个');compare=enter(t,comp-.11,.51)*(1-phase(t,cols_at-.45,cols_at+.59))
  for j,(r,x)in enumerate(zip(PAL,xs)):
   v=enter(t,main-.18+.090*j,.57);hi=(c.u('代码这一列') if j==0 else c.u('数学那一列') if j==1 else 0);av=v*(1-.67*compare if j>1 else 1)
   label(g,names[j],x,290,31,(C,T,V,C,O,G)[j],av)
   for i,raw in enumerate(r['values']):
    y=389+i*130;col=(C,V)[i];winner=raw==min(r['values'])
    box(g,x-width/2,y-41,width,84,col,av,inkcol(col,.23+.26*(14-raw)/14),1.65)
    label(g,f'{raw:.2f}',x,y,32,F,av)
    if hi and winner:line(g,(x-width*.34,y+29),(x+width*.34,y+29),Y,2.7,hi)
  for i,name in enumerate(['Llama','Mamba']):label(g,name,78,389+i*130,26,(C,V)[i],mat,'left')
  if compare:
   # Join the *actual* two winning cells; keep the connector in their gutter, not across text.
   l,r=xs[0]+width/2+2,xs[1]-width/2-2;mx=(l+r)/2
   path(g,[(l,389),(mx,389),(mx,519),(r,519)],compare,Y,2.6,compare)
   for j,x in enumerate(xs[:2]):
    delta=PAL[j]['values'][0]-PAL[j]['values'][1];tag=c.at('这个换位')+.42*j;v=enter(t,tag-.13,.52)
    label(g,f'{delta:+.2f}',x,626,30,Y,v*compare)
   v=enter(t,c.at('这个换位')+.60,.42)*compare;label(g,'Llama − Mamba',xs[1]+112,626,23,M,v,'left')
  model_at=c.at('同一对十三亿');tok_at=c.at('共用一套分词器');txt_at=c.at('只是拿来考的文字')
  if model_at-.2<t<cols_at+.42:
   for j,tag in enumerate((model_at,tok_at,txt_at)):
    v=during(t,tag-.15,tag+1.76,.33);cap=('1.3B','同一分词器','只换评测语料')[j]
    if v:label(g,cap,1154,175,31,T,v);underline(g,1062,209,175,t-tag+.06,T)
  if readv:
   from domains6 import aggregate
   line(g,(1086,274),(1086,607),E,1.65,readv)
   aggregate(g,c,PAL,xs,read)
  revisit=c.at('回头再对照');alt=c.at('只差零点一')
  if revisit-.12<t<alt+.31:
   sel=0 if t<revisit+1.10 else 1 if t<revisit+2.31 else -1
   if sel>=0:
    xx=xs[sel];bb=389 if sel==0 else 519
    swish(g,xx-width*.37,xx+width*.37,bb+26,t-revisit-1.10*sel+.08,Y,.68,3.9)
  label(g,'同为 1.3B 档  ·  共用 GPT-2 分词器',746,731,25,M,mat)
  if t>switch-.48:shade(g,phase(t,switch-.48,switch))
 else:
  hand=c.at('评测方得')-.16
  if t<hand:
   score_only(g,c,t,switch,hand);return
  a=enter(t,hand,.55);z=c.u('规范化',.66);xx=153;ys=481
  label(g,'评测方',xx,188,38,T,a,'left');label(g,'模型',xx+26,315,35,C,a,'left')
  for j in range(4):
   for i in range(6):rect(g,xx+i*29,374+j*32,21,22,inkcol(C,.36+.49*((i*3+j*5)%11)/11),a)
  try_=enter(t,sandbox-.16,.61)
  if try_:path(g,[(346,428),(462,428),(528,428)],try_,T,3.2)
  label(g,'logits',645,331,35,F,try_)
  for i,val in enumerate((1.14,.72,-.13,-.44)):
   x=552+i*58;h=val*67;raw=enter(t,c.at('原始输出')-.42+i*.115,.55)
   rect(g,x,ys-max(0,h*raw),35,abs(h)*raw,O,try_)
   if raw:label(g,f'{val:.2f}',x+17,ys-126,20,M,raw)
   if try_:
    f=clip((t-(sandbox+.13*i))/.80)
    if 0<f<1:
     px,py=transit((320,423),(x+17,ys-11),p5(f),-19);dot(g,px,py,4.5,C,try_)

  line(g,(528,ys),(796,ys),M,1.8,try_)
  if z:
   path(g,[(805,427),(886,427),(938,427)],z,T,3.3);label(g,'log-softmax',869,366,27,T,z);label(g,'log p → exp → p',894,488,22,M,z)
   logits=(1.14,.72,-.13,-.44);sm=sum(exp(q)for q in logits);probs=[exp(l)/sm for l in logits]
   visit=c.at('看这几根');settle=c.at('总和得是一');other=c.at('不能证明柱子');back=c.at('掌握产生')
   walk=phase(t,visit-.18,settle+.41);alt=enter(t,other-.17,.82)*(1-phase(t,back-.15,back+.67));reset=enter(t,back-.14,.70)
   altvals=(.10,.20,.29,.41)
   for i,p in enumerate(probs):
    x=1015+i*95;v=enter(t,visit-.16+i*.43,.52)
    rect(g,x-25,550-446*p*z,49,446*p*z,inkcol(C if i!=2 else Y,1-.60*alt),z)
    if v and t<other:
     rr=clip((t-visit-i*.43+.15)/.57)
     if rr<1:path(g,[(x-25,549),(x-25,550-446*p),(x+24,550-446*p)],rr,F,2.35,z)
    if alt:
     endy=550-446*altvals[i]*alt
     path(g,[(x-32,550),(x-32,endy),(x+30,endy),(x+30,550)],1,V,2.15,alt)
    label(g,f'{(altvals[i] if alt>.53 else p):.1%}',x,584,24,V if alt>.53 else F,z)
   label(g,'Σ p = 1',1185,229,45,T,c.u('总和得是一',.58))
   if alt:label(g,'另一组也加到 1',1185,286,26,V,alt)
   elif walk and not reset:
    startx=1010;run=0.
    for i,p in enumerate(probs):
     v=enter(t,visit-.16+i*.43,.52);ww=p*336;rect(g,startx+run,289,ww*v,13,C if i!=2 else Y,v);run+=ww
   single=c.u('原文那个词',.62)*(1-alt)
   if single:
    x=1015+2*95;v=enter(t,c.at('原文那个词')+.12,.61)
    path(g,[(x,613),(x,632),(x-61,658)],v,Y,1.9,single)
    label(g,f'−ln({probs[2]:.3f}) = {-log(probs[2]):.2f} nat',1088,679,30,Y,single)

  if c.u('掌握产生'):
   l=enter(t,c.at('掌握产生')-.20,.73);path(g,[(1394,706),(1394,738),(121,738),(121,587)],l,T,2.5);label(g,'同一次独立前向',762,713,24,M,l)
  q=c.u('既然平均概率',.72);shade(g,.59*q)

def score_only(g,c,t,sw,end):
 """What the evaluator hasn't seen yet: a lone number moves without its computation."""
 source=c.at('不能让参赛方');machine=c.at('自己机器');send=c.at('再只交');fade=1-phase(t,end-.42,end)
 show=enter(t,sw+.06,.66)*fade;host=enter(t,source-.21,.68);front=phase(t,send-.14,send+.91)
 label(g,'榜单',1195,239,41,F,show)
 path(g,[(1013,492),(1013,569),(1410,569),(1410,492)],enter(t,sw+.10,.64),M,2.35,show)
 for j in range(3):
  aa=enter(t,sw+.32+.23*j,.48)*(1-front)
  if aa:
   px=1106+24*j;py=353+43*j;line(g,(px,py),(px+173-27*j,py),M,2.1,aa*show);dot(g,px-24,py,4.3,T,aa*show)
 label(g,'参赛方',425,228,38,C,host*fade)
 if host:
  verts=[(249,311),(569,285),(608,474),(285,508)]
  g.poly(verts,C,2.35,host*fade,True,inkcol(C,.24),.71*host*fade)
  for j in range(3):
   v=enter(t,machine-.16+j*.18,.43);x=324+j*77;dot(g,x,396-6*j,7,C,v*fade)
  cx,cy=transit((522,432),(1201,455),p5(front),-75)
  if t>send-.23:
   v=enter(t,send-.22,.48);label(g,'PPL = s',cx,cy,42,Y,v*fade)
   path(g,[(601,461),(742,461),(839,413),(1003,413)],front,T,2.0,fade*.81)
  if front>.82:label(g,'结果到了，计算过程没来',1195,658,28,M,fade*front)
