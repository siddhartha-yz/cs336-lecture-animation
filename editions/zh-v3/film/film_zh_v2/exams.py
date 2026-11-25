from termnotes import hint
from ink import *
from motion import transit,guide
from exam_start import saturation,mmlu_pro
def gpqa(g,c):
 t=c.t;expert=on(c,'两位同领域博士',2);proof=on(c,'核对解析',1.6);non=on(c,'三位其他学科',2);mins=on(c,'平均三十七分钟',1.8);diamond=on(c,'最多只能有一人答对',2)
 title(g,'GPQA  ·  Diamond',114,sub=hint('GPQA Diamond'))
 # Each row is one candidate diene; each column is one possible direction of approach.
 # Figure 1's corresponding product is a cell, not a purely decorative dot pattern.
 txt(g,'有机化学：数异构体',402,228,33,F); x,y=316,346
 lead=phase(t,c.at('基础学科')-.26,c.at('基础学科')+.60)
 dim=phase(t,c.at('上网的电脑')-.14,c.at('上网的电脑')+.61)
 g1=phase(t,c.at('核对解析')-.20,c.at('核对解析')+.95)
 txt(g,'四种接近方向',411,279,23,M,dim)
 txt(g,'四类二烯',177,422,24,M,lead)
 for j in range(4):
  ry=y+j*48
  line(g,(246,ry),(282,ry),(C,V,O,T)[j],2.7,lead)
  for k in range(4):
   q=phase(t,1.1+j*.46+k*.14,2.0+j*.46+k*.14); pair=j*4+k
   xx=x+k*62;yy=ry
   if j==0 and dim:
    ang=(pi*.25,pi*.75,pi*1.25,pi*1.75)[k]
    a2=(xx+7*cos(ang),309+7*sin(ang));b2=(xx-7*cos(ang),309-7*sin(ang))
    arrow(g,a2,b2,1,M,dim,1.3)
   uq=phase(g1,pair*.047,pair*.047+.17)
   ring(g,xx,yy,9,(C,V,O,T)[j],q,2)
   if dim:
    ang=(pi*.25,pi*.75,pi*1.25,pi*1.75)[k]
    line(g,(xx+10*cos(ang),yy+10*sin(ang)),(xx+17*cos(ang),yy+17*sin(ang)),M,1.65,q*dim)
   if uq:dot(g,xx,yy,3.6,Y,uq)
 txt(g,'4 × 4 = 16',400,551,38,Y,g1)
 for j,(val,ch) in enumerate([(2,'A'),(16,'B'),(8,'C'),(4,'D')]):
  xx=235+j*105;col=Y if j==1 and proof else M
  txt(g,f'{ch} · {val}',xx,611,23,col,.62+.38*proof)
 line(g,(680,267),(680,626),E,1.4,.68)
 ask=c.at('靠搜索');pick=c.at('精选集');gate=c.at('校验关卡');poster=c.at('博士出题');outer=c.at('三位其他学科');accept=c.at('完全认同')
 search=phase(t,c.at('一搜就到')-.21,c.at('一搜就到')+.44)*(1-phase(t,pick-.65,pick+.04))
 if search:
  # A retrieved page is a source, not an answer key. Two ingredients still have to be combined.
  tx=(898,1100,1302);lab=('反应物','接近方向','可能的产物')
  for j,(px,stxt) in enumerate(zip(tx,lab)):
   q=phase(t,1.85+j*.45,2.73+j*.45);docs(g,px-54,335,108,120,(C,O,T)[j],search*q,4,j)
   txt(g,stxt,px,499,24,M,search*q)
  examined=phase(t,poster-.34,poster+.42)
  for j,ta in enumerate((c.at('给非本领域的人'),c.at('上网的电脑'),ask)):
   f=phase(t,ta-.30,ta+1.14);x=tx[j]
   if 0<f<1:guide(g,[(x-45,365),(x+40,365),(x+40,386),(x-24,386)],f,Y,search,2.5,.43)
  probe=phase(t,ask-.18,ask+1.03)
  if probe:
   path(g,[(898,546),(898,566),(1302,566),(1302,546)],probe,E,1.6,search)
   txt(g,'哪一种组合才算一个异构体？',1101,615,27,Y,search*probe)
 gate_a=phase(t,pick-.2,pick+.66)
 if gate_a:
  txt(g,'同领域专家',811,282,30,C,gate_a,'left')
  txt(g,'非本领域专家',811,475,30,O,gate_a,'left')
  agree=phase(t,accept-.21,accept+.55)
  for j in range(2):
   xx=1115+j*120;voter(g,xx,290,C,gate_a*(.45+.55*expert),1.38)
   q=phase(t,c.at('盲做')-.38+j*.28,c.at('盲做')+.55+j*.28)
   if q:
    px,py=transit((651,415),(xx,340),q,42)
    docs(g,px-10,py-12,20,25,C,gate_a*(1-agree),2,j)
   if agree:check(g,xx,360,13,True,agree)
  for j in range(3):
   xx=1040+j*136;voter(g,xx,488,O,gate_a*(.29+.71*non),1.28)
   q=phase(t,outer+.06+j*.23,outer+1.31+j*.23)
   if q:
    px,py=transit((652,424),(xx,545),q,-26)
    docs(g,px-10,py-12,20,25,O,gate_a*(1-diamond),2,j)
   if diamond:check(g,xx,556,12,j==1,diamond)
  closed=phase(t,gate-.2,gate+.66)
  if 0<closed<1:guide(g,[(775,256),(775,515),(800,515)],closed,T,1,2.8,.39)
 if mins:
  arc(g,871,581,30,-pi/2,-pi/2+tau*mins*.62,C,2.5,mins)
  txt(g,'37 分钟',916,581,26,F,mins,'left')
 txt(g,'复核后两位均认同 · 非专家最多一人答对',804,686,28,Y,diamond)
 certified=phase(t,c.at('两道关都过了')-.12,c.at('才进 Diamond')+.50)
 if certified:
  pts=[(1382,359),(1434,359),(1434,554),(1386,554)]
  path(g,pts,certified,T,1.8);d=phase(certified,.43,.96);xx,yy=1434,455
  g.poly([(xx,yy-13),(xx+12,yy),(xx,yy+13),(xx-12,yy)],Y,1.9,d,True,inkcol(Y,.12),1)
 source(g,'Rein 等 · 图 1、表 2 · Diamond 子集 198 题')
def hle(g,c):
 t=c.t;f=on(c,'对抗筛网',2);mk=[on(c,k,1.7) for k in ['七万次','一万三千','六千道','两千五百道']]
 pivot=c.at('日常用大模型');split=on(c,'数据清洗脚本',2.1)
 words=1-phase(t,pivot-.18,pivot+.24);field=1-phase(t,pivot+.01,pivot+.60)
 unfold=phase(t,pivot-.06,pivot+.95);op=phase(t,pivot+.42,pivot+.99)
 title(g,'HLE',111,words,sub=hint('HLE'))
 xs=[230,598,959,1311];ns=['70,000','13,000','6,000','2,500'];ls=['初始尝试','进入专家评审','候选题','公开题']
 for j,x in enumerate(xs):
  a=words*(.40+.60*mk[j]);ht=[156,105,75,50][j]
  line(g,(x,451-ht),(x,451+ht),[C,T,V,Y][j],2,field*(.40+.60*mk[j])*.75)
  txt(g,ns[j],x,229,42,[C,T,V,Y][j],a);txt(g,ls[j],x,278,24,M,a)
 for j in range(360):
  u=(j/360+t*.067)%1; xx=mix(xs[0],xs[-1],u)
  spread=mix(140,40,u); amp=sin(13.3*j+u*2.2)*spread
  rank=((j*137+19)%359+.5)/359;remain=1.
  for gate,part in ((.34,13000/70000),(.676,6000/70000),(.933,2500/70000)):
   if rank>part:remain*=1-phase(u,gate-.035,gate)
  if remain>.004:
   dot(g,xx,450+amp,2.5+(j%3)*.65,Y if u>.80 else (C,T,V)[(j//6)%3],remain*field*(.46+.53*f))
 if mk[-1]:txt(g,'另留私有集',1311,616,24,M,mk[-1]*words)
 source(g,'HLE 制题流程 · 讲义图 201',words)
 if 0<unfold<1:
  # One question survives the last sieve. Follow it into the actual sheet;
  # no dissolve between the old subtitle and the next question.
  ux,uy=transit((1311,451),(800,470),unfold,-54)
  w=mix(4,200,unfold);h=mix(4,190,unfold)
  docs(g,ux-w/2,uy-h/2,w,h,blend(Y,V,unfold),phase(unfold,0,.15),0,1)
 if op:
  txt(g,'一个答案，还是一份作品？',800,182,46,F,op)
  for j,(lab,col,when) in enumerate([('清洗脚本',C,'数据清洗脚本'),('商务邮件',V,'商务邮件'),('食谱',O,'食谱')]):
   x=mix(800,375+j*425,split);y=375-35*sin(j*pi/2)*split
   vis=(float(unfold>=1) if j==1 else op*phase(split,.16,.88))
   docs(g,x-100,y,200,190,col,vis,0,j)
   p0=c.at(when)
   for n in range(6):
    grow=phase(t,p0-.21+n*.11,p0+.44+n*.11)
    # Let each artifact visibly be written as its name is spoken. End poses
    # match the three documents that the next shot will fold into a blind pair.
    lng=200*(.39+.37*((11*n+3*j)%13)/12);xl=x-76;yl=y+190*(.21+n*.124)
    if grow:line(g,(xl,yl),(xl+lng*grow,yl),col,2.8,vis*.56)
   txt(g,lab,x,y+242,32,col,op*phase(t,p0-.2,p0+.4))
  # The multiple-choice test is still visible when it is named; the four
  # targets leave before the cue that writes the first open-ended artifact.
  only=c.at('只让它');fresh=c.at('数据清洗脚本')
  options=phase(t,only-.46,only+.18)*(1-phase(t,fresh-.77,fresh-.28))
  if options:
   for i,ch in enumerate('ABCD'):
    x=744+(i%2)*68;y=434+(i//2)*61
    ring(g,x,y,9,T if i==2 else M,options,1.8);txt(g,ch,x+17,y,17,F,options,'left')
   chosen=phase(t,c.at('单选题')-.10,c.at('单选题')+.54)
   if chosen:dot(g,744,495,4.6,T,options*chosen)
  unique=c.at('没有唯一标准答案');match=c.at('字符串匹配')
  if unique-.2<t<match+.85:
   u=phase(t,unique-.15,unique+1.03);a=1-phase(t,match+.17,match+.85)
   if u:
    # One literal answer key cannot match three kinds of work.
    for x0 in (375,800,1225):
     path(g,[(x0,625),(x0,639),(800,663)],u,M,1.35,a*.61)

  present=phase(t,match-.20,match+.51)
  txt(g,'字符串匹配',800,703,28,M,present*(1-.6*phase(t,match+1.02,match+1.68)))
