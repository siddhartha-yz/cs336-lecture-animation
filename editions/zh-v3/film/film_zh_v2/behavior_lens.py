from termnotes import hint
from ink import *
from motion import *
def transfer(g,c):
 t=c.t;name=c.at('GCG');proxy=c.at('负对数');whole=c.at('评测要判的');survey=c.at('HarmBench');four=c.at('约四倍');pair=c.at('怎么量迁移');twenty=c.at('二十道题');eight=c.at('八次问题');keep=c.at('把这八张留下');flip=c.at('逐张翻过来');three=c.at('只有三张');den=c.at('这八张里');all_=c.at('两个模型同时');all20=c.at('最初的二十张');last=c.at('这些考题')
 sweep=phase(t,survey-.48,survey-.05);old=1-sweep
 if old:
  named=phase(t,name-.16,name+.45);white=c.at('白盒上');new=c.at('输入一变');opening=c.at('回复开头');higher=c.at('这个开头的概率越高')
  title(g,'只看开头，能判整份回答吗？',111,old*(1-phase(t,name-.66,name-.18)))
  title(g,'GCG',111,old*named,sub=hint('GCG'))
  # Harmless counterexample: two pages have the same greeting and different bodies.
  # We show the shared prefix and the full observable outputs. Nothing is generated or searched here.
  branch=phase(t,whole-.69,whole+.57);focus=phase(t,opening-.20,opening+.65)
  for j in range(2):
   x,y=1034+j*180,346;col=(T,V)[j];intro=phase(t,.51+j*.44,1.29+j*.44)*old
   docs(g,x-63,y-42,126,144,col,intro,0,j)
   txt(g,'好的。',x,y-15,21,Y if focus else F,intro)
   for z in range(3):
    line(g,(x-43,y+18+z*15),(x+23-((z*j+2*z)%3)*12,y+18+z*15),col,1.6,intro*(.50-.20*focus))
   if j:
    for z in range(3):
     line(g,(x-43,y+64+z*9),(x+36,y+64+z*9),col,1.1,intro*(.68+.28*branch))
    for xx in (x-43,x-3,x+36):line(g,(xx,y+64),(xx,y+82),col,1.1,intro*(.68+.28*branch))
   if focus and branch<1:
    line(g,(x-38,y+3),(x+26,y+3),Y,2.15,intro*focus*(1-branch))
   if branch and t<=survey-.67:
    f=phase(t,whole-.12+j*.22,whole+.78+j*.22)
    path(g,[(x-69,y-43),(x-76,y-43),(x-76,y+103),(x-68,y+103)],f,col,2.2,old)
  prev,next_=reletter(branch);txt(g,'同一开头',1125,510,29,Y,focus*old*prev);txt(g,'完整回答不同',1125,510,29,T,next_*old)
  if branch:txt(g,'逐例判断行为',1125,582,24,M,branch*old)
  sample=phase(t,white-.24,white+.50)
  if sample:
   txt(g,'固定的回复开头 u',459,269,28,C,old*sample)
   formula(g,'surprise',465,370,290,old*sample)
   l=242;r=703;y=510
   line(g,(l,y),(r,y),M,1.5,old*sample)
   for j in range(6):line(g,(l+(r-l)*j/5,y-6),(l+(r-l)*j/5,y+6),M,1.4,old*sample)
   # Each fixed input produces one probability. Moving between the outcomes only explicates the scale.
   p0,p1=.16,.74
   prim=phase(t,new-.28,opening+.15);trace=phase(t,higher-.35,proxy+.55)
   if prim:
    for j,(prob,clr) in enumerate(((p0,C),(p1,T))):
     a=phase(prim,.42*j,.56+.42*j);xx=l+(r-l)*prob
     ring(g,xx,y,8,clr,old*a,1.8);txt(g,('条件 A','条件 B')[j],xx,y+46,24,clr,old*a)
   p=mix(p0,p1,trace);xx=l+(r-l)*p
   if trace:line(g,(l+(r-l)*p0,y),(xx,y),Y,2.0,old*trace)
   dot(g,xx,y,6,Y,old*sample);txt(g,f'p = {p:.2f}',xx,y-41,26,Y,sample*old)
   txt(g,f'−ln p  =  {-log(p):.2f}',464,640,34,C,sample*old)
   txt(g,'示意概率',697,702,21,M,sample*old,'right')
 # The paper brackets belonged to *how a full response is judged*. They
 # unfold into two empty reading rails. No illustrative probability ever travels
 # into the empirical bars; those start from zero after the paper is named.
 hand=phase(t,survey-.67,survey+.51)
 if 0<hand<1:
  for j,col in enumerate((T,V)):
   left=1034+j*180;yy=339+j*144
   before=[(left-69,303),(left-76,303),(left-76,449),(left-68,449)]
   after=[(475,yy-5),(475,yy),(1239,yy),(1239,yy-5)]
   points=[lerp(p,q,hand) for p,q in zip(before,after)]
   g.poly(points,blend(col,D,hand),mix(2.2,1.3,hand),1)
   if .03<hand<.96:guide(g,points,hand,blend(col,C if not j else T,hand),.89,2.65,.25)
 data=phase(t,survey-.02,survey+.55);close=1-phase(t,pair-.72,pair-.29)
 if data*close:
  a=data*close;title(g,'换个模型，发生率变了多少？',111,a,sub='相同协议 · 三种 GCG 条件的平均')
  for j,(nm,v,col) in enumerate((('Llama 2 13B',1,C),('Zephyr + R2D2',.25,T))):
   xx=475;yy=339+j*144;grow=phase(t,survey+.1+j*.62,survey+1.26+j*.62)
   txt(g,nm,xx-35,yy,31,F,a,'right');line(g,(xx,yy),(xx+764,yy),D,1.3,a)
   rect(g,xx,yy-11,718*v*grow,22,col,a*grow);txt(g,('1','≈ 0.25')[j],xx+718*v*grow+21,yy,33,col, a*grow,'left')
  txt(g,'相对发生率 · 以第一行为 1',800,638,29,M,a)
  source(g,'HarmBench 论文图 7 · 三种条件的平均 · 不是绝对成功率',a)
 if t>=pair-.20:
  op=phase(t,pair-.20,pair+.44);q=phase(t,twenty-.55,twenty+.64);draw8=phase(t,eight-.23,eight+.54);isolate=phase(t,keep-.13,keep+1.30);rev=phase(t,flip-.18,flip+2.07);n3=phase(t,three-.12,three+.73);d1=phase(t,den-.34,den+.55);return20=phase(t,all_-.08,all20+.5);d2=phase(t,all20-.17,all20+.66)
  title(g,'同样三张，除以几张？',111,op,sub='配对示例：每张卡是同一道题，在两个模型上各测一次')
  first=(1,3,5,7,10,13,15,18);both=(3,10,18)
  for j in range(20):
   isA=j in first;isB=j in both;x=294+(j%5)*108;y=315+(j//5)*89
   if isA:
    n=first.index(j);tar=(292+(n%4)*129,375+(n//4)*100)
   else:tar=(x,y-32)
   p=isolate*(1-return20);x,y=transit((x,y),tar,p,19 if isA else -8)
   a=(1-p*(0 if isA else .83))*q
   col=blend(M,C if isA else E,draw8);col=blend(col,T,n3 if isB else 0)
   # Rotate only the blank paper edge; the case number is never horizontally squashed.
   rf=phase(t,flip-.16+(first.index(j)*.105 if isA else 30),flip+.60+(first.index(j)*.105 if isA else 30)) if isA else 0
   width=73*(.15+.85*abs(cos(pi*rf)));height=54
   box(g,x-width/2,y-height/2,width,height,col,a,fill=inkcol(col,.14 if isA else .04),sw=2.2 if isA else 1.25)
   if width>53:txt(g,f'{j+1:02d}',x,y,20,F if isA else M,a*(.44+.55*(width-53)/20))
   if isB and n3:dot(g,x+26,y-17,4,Y,n3*a)
  vs=phase(t,twenty-.13,twenty+.63);txt(g,'20 个配对用例',510,697,27,M,vs*(1-isolate*(1-return20)))
  # Label the actual sets under their cards: the eight are failures of A,
  # not eight failures shared by the two models. The same three gold marks
  # survive when the twenty-card denominator returns.
  subset_label=phase(isolate,.41,.94)*(1-phase(return20,.09,.58))
  if subset_label:
   box(g,257,625,24,17,C,subset_label,sw=1.8)
   txt(g,'A 出问题：8 题',296,634,27,C,subset_label,'left')
   both_label=subset_label*n3
   if both_label:
    dot(g,527,634,5.2,Y,both_label)
    txt(g,'其中 B 也出问题：3 题',548,634,27,Y,both_label,'left')
  if d1:
   formula(g,'transfer',1131,342,321,d1)
   # A single affine text group moves up; no crossfade between two fractions.
   cx,cy=transit((1126,456),(1127,408),return20,0);z=mix(1.,37/71,return20)
   ctx=g.c;ctx.save();ctx.translate(cx,cy);ctx.scale(z,z)
   txt(g,'3 / 8',0,0,71,blend(T,M,return20),d1*(1-.34*return20));ctx.restore()
  if return20:
   # Explicitly move the denominator, not the three highlighted observations.
   formula(g,'both',1130,519,325,d2);txt(g,'3 / 20',1130,638,55,Y,d2)
   txt(g,'仍是那三张，分母换回全部用例',514,731,23,Y,d2)
  again=c.at('还是那三张');switch=c.at('换个分母');ahead=c.at('再往前走一步');target=c.at('真实工作')
  if t>again-.22:
   # The numerator has not changed: briefly retrace those same three physical markers.
   for n,j in enumerate(both):
    x=294+(j%5)*108;y=315+(j//5)*89;start=again-.13+n*.21
    v=phase(t,start,start+.81)
    if 0<v<1:ring(g,x+26,y-17,6+12*v,Y,sin(pi*v),2.3)
   span=phase(t,switch-.13,switch+1.05);out=1-phase(t,ahead-.57,ahead-.16)
   if span and out:
    for jj,(N,xx,col) in enumerate(((8,898,C),(20,1182,Y))):
     xx0=xx-55;yy=708
     for ii in range(N):
      q=phase(span,ii*.25/N,.52+ii*.25/N)
      if q:rect(g,xx0+7.2*ii,yy,5.2,7.2,Y if ii<3 else E,q*out)
   link=phase(t,ahead-.16,target+.32)
   if link:
    # Carry ONE unchanged test case beyond its row. It becomes the exam sheet in the next chapter.
    px,py=transit((294+(18%5)*108,315+(18//5)*89),(829,426),link,40)
    docs(g,px-18-14*link,py-13-25*link,36+28*link,26+50*link,T,link,2,1)
    if link>.37:txt(g,'真实任务？',832,510,24,T,phase(link,.36,.94))
  if 0<d2<1:guide(g,[(775,623),(824,623),(846,642),(937,642)],d2,Y,1,2.75,.38)
