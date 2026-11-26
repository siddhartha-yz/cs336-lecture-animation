"""Two encodings of one fixed byte spine. Drawing data come from the same archived forwards."""
from rig4 import *
D=json.loads((V2/'art2/data/tokenizers.json').read_text())
TXT=D['text'];N=D['bytes'];BIT=D['equal_loss_bits']
assert len(TXT.encode('utf-8'))==N and all(m['boundaries'][-1]==N for m in D['models'])
XL,XR=223.,1477.;STEP=(XR-XL)/N
MSC='DejaVu Sans Mono'
def X(k):return XL+STEP*k
def chars(g,y,sz,alpha,col=F,shade_after=None):
 o=0
 for ch in TXT:
  j=len(ch.encode('utf-8'))
  if ch!=' ':
   fs=sz;tp=col
   if shade_after is not None and o<=shade_after<o+j:tp=Y
   txt(g,ch,X(o+j/2),y,fs,tp,alpha,font=MSC)
  o+=j
def rail(g,y,z,co=T,ap=1):
 for j in range(N):
  q=clip(N*z-j);x=X(j)
  if q:rect(g,x,y,(STEP-1.85)*q,8.6,co,ap*(.86 if j%5==0 or j+1==N else .52))
def clipnote(g,xy,co,a):
 if a:point(g,*xy,4.4,co,a)
def bpb6(g,c):
 t=c.t;a=c.at
 divide=a('换两把分词');first=a('九个词元');second=a('十一个');whole=a('原始的四十五个字节')
 sample=a('先把两边');bits=a('八十九比特');finer=a('切得更碎');share=a('摊到每个');falls=a('掉了一截')
 norm_=a('统一折算');length=a('字节长度');term=a('每字节比特数')
 actual=a('放回模型实测');diff=a('哪一行');history=a('早期像')
 if t>history-.18:archive(g,c,history)
 if t>=history+.15:return
 leave=1-phase(t,history-.64,history-.03)
 p=phase(t,-.09,.37);split=phase(t,divide-.19,divide+.58)
 upper=phase(t,first-.32,first+.45);lower=phase(t,second-.44,second+.44)
 # The text stays in place until we have a reason to make two copies. The first
 # byte, a real space, stays in the register even though it has no printed glyph.
 outer=(1-.48*split)*p*leave
 common=1-phase(t,actual-.05,actual+.54);remix=phase(t,norm_-.22,length+.39)
 left=phase(t,share-.10,share+.82);probs=phase(t,falls-.21,falls+.61)
 real=phase(t,actual-.18,actual+.63);dist=phase(t,diff-.13,diff+.57)
 yy=mix(389,138,split)
 # Carry just the chosen route's mark across the cut. It is the cursor on the
 # original continuation, not a frozen frame of the previous probability chart.
 q0=easepos(t,-.01,.49);read=easepos(t,.14,.73)
 if read<1:
  xx,y0=transit((937.2,363.6),(XL,yy+58),q0,-37)
  if q0<1:p0=mix(27.6,6.4,q0);rect(g,xx-p0/2,y0-p0/2,p0,p0,Y,1-q0)
  ctx=g.c;ctx.save();ctx.rectangle(XL-4,yy-52,max(.01,(XR-XL+8)*read),98);ctx.clip()
  chars(g,yy,44,outer)
  ctx.restore()
 else:chars(g,yy,44,outer*(1-.35*remix)*(1-.26*real))
 sweep=phase(t,whole-.25,whole+.87)
 if not split:
  path(g,[(XL,yy+58),(XR,yy+58)],read,T,2.4,p*leave*.84)
 elif outer>.01:
  line(g,(XL,yy+44),(XR,yy+44),T,2.1,outer*.79)
  mark(g,'同一串原文',XL,yy-54,26,t-divide+.21,M,'left',op=outer,dur=.43)
 if sweep:
  rail(g,206,sweep,T,leave)
  label(g,'45 字节',XR,237,28,T,leave*c.u('四十五个字节',.45),'right')
 # Move only the two text strips. Each model's colored cuts describe real UTF-8
 # intervals; for the "equal loss" experiment height is never a made-up local loss.
 for j,m in enumerate(D['models']):
  co=(C,V)[j];enter_row=(upper,lower)[j]
  fold=phase(t,divide-.10,first+.45) if not j else phase(t,second-.73,second+.44)
  target_y=(341.,503.)[j]
  # The second copy appears outside the upper strip. Its label stays parked
  # in its own lane instead of moving across 'GPT-2' during the division.
  y=mix(yy,target_y,fold) if not j else mix(target_y+62,target_y,p5(fold))
  op=leave*fold
  if op<.01:continue
  dy=(1-remix)*(13 if j else -7)*phase(t,finer-.24,finer+.66)
  for i,(lo,hi,val) in enumerate(zip(m['boundaries'],m['boundaries'][1:],m['bits'])):
   cut=enter(t,(first,second)[j]-.43+i*.048,.43);w=X(hi)-X(lo);x=X(lo)+.8;h=mix(54,39,real);ht=val*2.6
   col=blend(co,Y,math.exp(-((t-finer+.10-i*.078)/.19)**2)*.75 if j else 0)
   av=op*cut
   if av:
    rect(g,x,y-h/2+dy,w-2.8,h,inkcol(co,.33 if i%2 else .49),av)
    line(g,(x,y+h/2+dy),(x+w-2.8,y+h/2+dy),col,2.45,av)
    if lo in (3,32)and j and t<finer+2.:
     uu=during(t,second-.13+i*.044,finer+1.10,.44)
     if uu:line(g,(x-1,y-39),(x-1,y+32),Y,2.05,av*uu)
   if real:
    q=enter(t,actual-.10+j*.11+i*.039,.48)
    rect(g,x,y-23-ht*q,w-2.8,ht*q,col,op*real*.80)
  chars(g,y+dy,36,op*enter_row*1.12,F,shade_after=32 if j and dist>.55 else None)
  label(g,m['label'],XL-23,target_y-9,31,co,op*enter_row,'right')
  count=len(m['raw_tokens']);number=enter(t,(first,second)[j]-.06,.54)
  label(g,f'{count} 词元',XL-23,target_y+27,24,M,op*number*(1-remix),'right')
  v=enter(t,bits-.14,.55)*leave
  if v and common:
   # Hold the same mass for both tokenizers. Identical 89 slivers, regrouped by count
   # (a sliver is one bit for the teaching example, not the measured bit of a token).
   pack=X(3);ew=9.2;span=795.0;sweep0=enter(t,bits+.055*j,.96);groupw=span/count
   f=phase(t,share-.32+j*.11,share+.52+j*.11);by=(423,589)[j]+5*dy
   for n in range(BIT):
    q=clip(BIT*sweep0-n);idx=min(count-1,int((n+.5)*count/BIT))
    x=pack+(span/BIT)*n+f*(idx-count*.5)*2.25
    al=op*common*v*q*(1-.94*remix)
    if al:rect(g,x,by,(ew-1.45)*q,13.5,co if idx%2 and f>.52 else Y,al*.76)
   if f and remix<.98:
    for i in range(count+1):
     x=pack+groupw*i+f*(i-count*.5)*2.25
     line(g,(x,by-5),(x,by+19),F,1.2,op*f*.49*(1-remix))
   xp=XL+949;vp=v*common*(1-remix)*op
   if vp:
    label(g,'89 bit',xp,by+3,36,Y,vp,'left')
    if left:label(g,'÷ '+str(count),xp+145,by+3,34,co,vp*left,'left')
    if probs:
     ppl=2**(BIT/count)
     label(g,f'≈ {ppl:.0f}',XR,by+44,32,co,vp*probs,'right')
     label(g,'PPL',XR-138,by+44,22,M,vp*probs,'right')
  if remix and not real:
   u=phase(t,norm_,length+.28)
   yc=(395,558)[j]
   elems=(f'89',f'÷ {N}',f'= {BIT/N:.3f}')
   for k,(x,ss) in enumerate(zip((555,765,1015),elems)):
    label(g,ss,mix(XL+780+k*156,x,p5(u)),yc,39,(Y,T,co)[k],op*remix*(1-real)*enter(t,norm_-.05+.069*k,.39))
  if real:
   cy=(404.,567.)[j]
   num=enter(t,diff-.20+.09*j,.52)
   v=op*real;label(g,'BPB',1038,cy,24,M,v,'left');label(g,f"{m['bpb']:.3f}",1436,cy,47,co,v,'right')
   path(g,[(1120,cy+15),(1438,cy+15)],num,T,1.6,v*num*.74 if j==0 else 0)
 # The measurement is changing units. Brace both rows around the *same*
 # total, then physically route their two denominators to the bytes above.
 equal=a('模型其实');fair=a('想要跨');clear_frac=a('分母就不能')
 pop=during(t,equal-.12,clear_frac+.53,.47)
 if pop:
  xx=XL+917;ya=425;yb=589;u=easepos(t,equal-.13,.74)
  tex=enter(t,equal-.12,.59)
  for z,co in enumerate((C,V)):
   y=(ya,yb)[z];top=y-22;bottom=y+39
   path(g,[(xx+4,top),(xx-19,top),(xx-19,bottom),(xx+4,bottom)],u,Y,2.05,pop*.82)
   if z:line(g,(xx-57,y+3),(xx-19,y+3),co,1.9,pop*.64)
   else:path(g,[(xx-22,y+4),(xx-73,y+4),(xx-106,462)],u,co,1.9,pop*.64)
  if u>.52:point(g,xx-108,467,4.7,Y,pop*tex)
  if t>=fair-.21:mark(g,'总损失相同',xx-126,465,27,t-fair+.21,Y,'right',op=pop)
 route=during(t,clear_frac-.14,length+.30,.45)
 if route:
  rail0=phase(t,clear_frac-.19,norm_+.08)
  for i,y in enumerate((426,593)):
   col=(C,V)[i];r=[(1394,y),(1501,y),(1501,266),(1476,234)]
   path(g,r,rail0,col,1.85,route*.73)
   if rail0>.025:
    x=1478;y=207;ring(g,x,y,9+4.5*rail0,T,route*rail0,1.75)
 if v:=phase(t,term-.18,term+.62)*leave:
  label(g,'BPB',567,699,34,T,v,'right');line(g,(590,697),(633,697),T,1.65,v)
  label(g,'每字节比特数',652,699,30,F,v,'left')
 if real:
  label(g,'实测损失',XL,260,23,M,real*leave,'left')
  ptr=phase(t,diff-.10,diff+1.38)
  if ptr<1:
   x=mix(XL,XR,ptr);line(g,(x,221),(x,549),T,1.2,leave*real*sin(pi*ptr)*.67)
 if sample-.15<t<bits+.39:
  b=during(t,sample-.15,bits+.39,.54)
  if b:label(g,'先让两行损失相同',799,654,29,M,b*leave)

def archive(g,c,at):
 t=c.t;live=enter(t,at,.64);wiki=c.at('WikiText');splitat=c.at('划训练集和测试集');web=c.at('WebText');zero=c.at('零样本困惑度');done=c.at('考场')
 if not live:return
 # Move from same-document slicing to an actual cross-corpus run. The records
 # form the composition; names are annotations to the streams, not a title card.
 change=phase(t,web-.94,web+.41);qx=phase(t,splitat-.23,splitat+.78)
 names=('Penn Treebank','WikiText-103');ys=(323,513);bands=(C,V)
 for j,(s,y,co) in enumerate(zip(names,ys,bands)):
  z=enter(t,at+.16 if not j else wiki-.11,.54)*live
  y2=mix(y,y+(j-.35)*21,change);x0=mix(251,644,change);w=mix(1079,758,change)
  label(g,s,x0,y2-62,40,F,z,'left')
  for k in range(44):
   q=enter(t,at-.19+j*.57+k*.013,.48);h=46+11*sin(k*2.41+j)
   seg=T if k>=34 else co
   rt=w/44;x=x0+k*rt+1.35+(22*qx if k>=34 else 0)*(1-change)
   rect(g,x,y2-h/2,rt-2.7,h*q,seg,z*q*(.91 if k>=34 else .42+.20*cos(1.15*k)**2))
  f=qx*z*(1-change)
  if f:
   label(g,'训练',x0+250,y2+61,29,co,f);label(g,'测试',x0+917,y2+61,29,T,f)
   x=x0+w*34/44
   path(g,[(x,y2-39),(x,y2+36)],f,F,2.05,f*.83)
 if change:
  co=O;alpha=change*live
  label(g,'WebText',221,323,39,co,alpha)
  for j in range(7):rect(g,91+j*41,370-math.sin(j)*9,31,43,co,alpha*(.87-.08*(j%3)))
  v=phase(t,web-.05,zero+.18)
  for j in range(2):
   path(g,[(383,391),(465,391),(557,mix(391,ys[j],v)),(614,ys[j])],v,co,2.8,alpha)
  if v:
   for i in range(4):
    q=phase(t,web+.12+i*.28,zero+.19+i*.28)
    if 0<q<1:
     x,y=transit((391,392),(633,ys[i%2]),q,(-35 if i%2 else 42));point(g,x,y,4.2,O,alpha*sin(pi*q)**.4)
  v=enter(t,zero-.24,.62)
  if v:
   label(g,'冻结 GPT-2',217,483,31,T,alpha*v)
   label(g,'零样本 PPL',772,669,37,T,alpha*v)
   # Published full-size GPT-2 result on WikiText-103.
   mark(g,'17.48',1148,666,58,t-zero-.03,Y,mode='pen',dur=.65,op=alpha*v)
   path(g,[(1030,622),(1052,593),(1302,593),(1319,548)],enter(t,zero+.08,.65),Y,1.9,v)
