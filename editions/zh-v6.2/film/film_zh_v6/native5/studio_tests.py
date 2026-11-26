"""Count physically possible pairs, keep the model fixed, and hand the viewer an unsolved ARC grid."""
from ink import *
from ink import arc as draw_arc
from motion import guide,transit,out3
from ink_words import letter,swish,carryword
from studio_examples import area,pstep,silk,VIO,BLUE,AQUA,MONO,mark
from timeline3 import W,OLD,S
from termnotes import hint
import itertools,json
AR=json.loads((OLD/'data/arc-67a3c6ac.json').read_text())
PAL=['#000000','#2178DE','#FF514B','#2ECC40','#FFDC00','#AAAAAA','#EB43C0','#FF9B31','#7FDBFF','#8D2E23']
REC=json.loads((OLD/'data/scaffolds.json').read_text())
def tile(g,x,y,w,col,op=1):
 rect(g,x,y,w,w,inkcol(col,.92),op);line(g,(x+1,y+1),(x+w-1,y+1),col,1.4,op)
def arcboard(g,mat,cx,cy,sz,op=1,xmix=0,open_=1,hl=None):
 n=len(mat);m=len(mat[0]);cell=sz/max(m,n);left=cx-m*cell/2;top=cy-n*cell/2;gap=max(1,min(3,cell*.07))
 for i,row in enumerate(mat):
  for j,col in enumerate(row):
   xx=left+mix(j,m-1-j,xmix)*cell;yy=top+i*cell
   if open_>=1 or (i*m+j+.5)/(m*n)<=open_:tile(g,xx+gap*.5,yy+gap*.5,cell-gap,PAL[col],op)
   else:box(g,xx+gap,yy+gap,cell-2*gap,cell-2*gap,'#707070',op*.84,sw=1.5)
 if hl:
  i,j,f=hl;xx=left+mix(j,m-1-j,xmix)*cell;yy=top+i*cell;box(g,xx+1,yy+1,cell-2,cell-2,Y,f,sw=3)
def patch(g,x,y,n,col,s=1,op=1):
 if s<=.0001 or op<=.001:return
 # Five candidate patches are five runs of one test, not five reproductions of source documents.
 ctx=g.c;ctx.save();ctx.translate(x,y);ctx.scale(s,s)
 lane=inkcol(col,.24);area(g,[(-49,-41),(48,-41),(58,0),(48,41),(-49,41),(-59,0)],lane,op)
 path(g,[(-49,-41),(48,-41),(58,0),(48,41),(-49,41),(-59,0),(-49,-41)],1,col,1.85,op)
 txt(g,chr(65+n),0,0,32,F,op);ctx.restore()
def combinations(g,c):
 t=c.t;five=c.at('五份候选');two=c.at('两份通过');one=c.at('闭眼抽一份');pk=c.at('pass@1');more=c.at('允许交两份');out=c.at('都错的配对');ten=c.at('十对');three=c.at('其中三对');seven=c.at('余下七对');frac_=c.at('十分之七');pivot=c.at('先把中间');tools=c.at('工具调用循环');ds=c.at('同一套');base=c.at('底座一直');fixed=c.at('固定下来')
 vanish=phase(t,pivot-.46,pivot+.23);old=1-vanish
 if old:
  silk(g,'候选补丁',132,105,49,t-.12,F,old,align='left')
  silk(g,'pass@k',1451,111,48,t-pk+.52,C,old,'pen','right')
  if t>pk-.20:txt(g,hint('pass@k'),1447,168,24,M,old*phase(t,pk-.2,pk+.28),'right')
  rowpx=[349,575,800,1025,1251];k=phase(t,more-.25,more+.64)
  for j,x in enumerate(rowpx):
   p=pstep(t,.15+j*.06,.46);col=blend(C,(G,R)[j>=2],phase(t,two-.18+j*.055,two+.39+j*.055))
   xx=mix(x,260+150*j,k);yy=mix(405,315,k);sz=mix(1.12,.78,k)
   patch(g,xx,yy,j,col,sz*p,old*p)
   if t>one-.20 and k<.99:
    dot(g,x,514,6,col,old*phase(t,one-.16+j*.074,one+.34+j*.074)*(1-k))
  if t<more+.05:
   op=phase(t,pk-.50,pk+.15)*(1-k);silk(g,'2 / 5',800,642,52,t-pk+.5,Y,op,'pen')
  if k:
   pairs=list(itertools.combinations(range(5),2));p2=phase(t,out-.12,out+1.04);z=phase(t,seven-.19,seven+.52)
   for j,(a,b)in enumerate(pairs):
    # Two colour-coded traits at equal spacing represent the ten equally weighted unordered pairs.
    x=225+(j%5)*149;y=475+(j//5)*104;rt=pstep(t,more+.13+j*.055,.47);o=rt*k*old
    tx=260+a*150;ty=315
    xx,yy=transit((tx,ty),(x,y),rt,34)
    good=a<2 or b<2;co=T if good else R
    rect(g,xx-55,yy-26,109,52,inkcol(co,.21+.36*(z if good else p2)),o)
    line(g,(xx-55,yy+26),(xx+54,yy+26),co,2.2,o)
    txt(g,chr(65+a)+chr(65+b),xx,yy,27,F,o)
    if not good:
     kk=pstep(t,three-.11+(j-7)*.09,.34)
     if kk:line(g,(xx-41,yy+14),(mix(xx-41,xx+41,kk),mix(yy+14,yy-14,kk)),R,3.6,o)
   oo=pstep(t,ten-.12,.60);line(g,(1050,314),(1470,314),E,1.65,old*oo);txt(g,'等可能的十对',1252,373,31,M,old*oo)
   for j in range(10):
    px=1074+(j%5)*76;py=471+(j//5)*74;co=T if j<7 else R
    ff=pstep(t,(seven if j<7 else three)-.13+(j%7)*.055,.38)
    if ff:rect(g,px-20,py-20,40,40,co,ff*old)
   if t>frac_-.18:
    silk(g,'7 / 10',1242,672,54,t-frac_+.18,Y,old,'pen')
    swish(g,1144,1334,713,t-frac_+.03,Y,.6)
 if vanish:
  a=vanish
  # Tool interfaces are roles, not claims about an individual implementation.
  # The four events run round the fixed centre, then dock two separate report fields.
  job=c.at('所以一份');mdl=c.at('什么模型');kit=c.at('什么脚手架')
  changec=c.at('换一套脚手架');evt=phase(t,changec-.33,changec+.55)
  report=phase(t,job-.38,job+.55)
  swap=c.at('工具可以换');still=c.at('底座没动');diff_=c.at('解决率照样')
  silk(g,'脚手架',151,106,46,t-pivot+.16,F,a,align='left');txt(g,hint('脚手架（Scaffold）'),151,160,24,M,a,'left')
  ctx=g.c;xc,yc=445,453;arm=phase(t,pivot-.1,pivot+.65)
  ring(g,xc,yc,95,C,arm,3.4);wedgepoly=[(xc+84*cos(j*tau/42),yc+84*sin(j*tau/42))for j in range(42)]
  area(g,wedgepoly,'#103742',arm);txt(g,'GPT-4o',xc,yc,41,F,arm)
  # A fixed copper axle receives two differently shaped outer frames. The centre never moves.
  # These rings denote replacement, not undocumented internals of either agent.
  from math import atan2
  slot=pstep(t,pivot-.23,.67);hinge=phase(t,swap-.24,swap+.55)
  for m in range(2):
   a0=pi*.22+m*pi+hinge*.64;coords=[]
   for j in range(48):
    an=a0+1.24*j/47;coords.append((xc+123*cos(an),yc+123*sin(an)))
   path(g,coords,slot,O if not m else T,6.4,a*(.92-.30*hinge))
  if still-.19<t<still+.52:swish(g,xc-80,xc+80,yc+110,t-still+.19,Y,.70)
  # Two already documented scaffold results are visible at the word '换', before the five-way comparison expands.
  lo=pstep(t,pivot-.10,.60);hi0=pstep(t,swap-.15,.67);rr=pstep(t,diff_-.16,.57)
  layer=1-phase(t,ds-.39,ds+.13)
  if layer:
   for h0,n0,co,qt in ((0,'SWE-Agent',C,lo),(1,'Agentless',T,hi0)):
    u=qt*layer
    if not u:continue
    tx=856;yy0=359+h0*156
    pts=[(xc+131,yc),(746,yc),(793,yy0),(tx,yy0)]
    path(g,pts,qt,co,2.7,u);dot(g,tx,yy0,6,co,u)
    txt(g,n0,tx+30,yy0-29,33,F,u,'left')
    rect(g,tx+27,yy0+8,363*REC[n0]/35*rr,26,inkcol(co,.83),u)
    if rr:txt(g,f'{REC[n0]:g}%',tx+42+363*REC[n0]/35,yy0+22,33,co,u*rr,'left')
   if hi0:txt(g,'同一模型，换外面的工具',1113,672,26,M,hi0*layer)
  at=[c.at(q)for q in ('工具调用循环','文件检索','状态管理','任务派发')]; labs=('调用工具','文件检索','状态管理','任务派发')
  for j,(lab,kt)in enumerate(zip(labs,at)):
   an=-pi/2+j*pi/2;k=pstep(t,tools-.69+j*.075,.54);kk=pstep(t,kt-.11,.5)
   x=xc+186*cos(an);y=yc+163*sin(an)
   if k:
    p0=(xc+97*cos(an),yc+97*sin(an));path(g,[p0,(x,y)],k,O,2,k*.90);dot(g,x,y,6.6,O,k);txt(g,lab,x+cos(an)*31,y+sin(an)*31-(39 if j==1 else 0),24,O,kk,('left' if j==1 else 'right' if j==3 else 'center'))
  # A path only exists once both endpoint tools have appeared. Direction follows the
  # spoken call → retrieval → state → dispatch rather than a continuously spinning ornament.
  for j,(from_,to_)in enumerate(zip(at,at[1:])):
   span=phase(t,from_-.03,to_+.40)
   if span and t<ds-.12:
    e=pi*.5*j-pi*.5;u=e+pi*.5*span
    draw_arc(g,xc,yc,143,e,u,T,3.0,1-phase(t,ds-1.01,ds-.30))
    if span<.999:dot(g,xc+143*cos(u),yc+143*sin(u),8,Y)
  txt(g,'同一底座',xc,706,28,C,a*(1-report))
  heads=pstep(t,ds-.48,.64)
  if heads:
   from mounting import etch
   add=phase(t,changec-.2,changec+.70)
   book=phase(t,c.at('测试集和模型')-.27,fixed+.4)
   pivotrow=phase(t,kit-.19,kit+.59)
   # Each real success rate is evaluated on 500 items. No simulated per-item statuses
   # are printed: '115' and '166' are the actual aggregate counts 500*p.
   etch(g,'SWE-bench Verified',849,221,26,C,heads)
   etch(g,'500 题',1318,221,32,F,heads)
   line(g,(828,270),(1451,270),E,1.45,heads)
   for j,nm in enumerate(('SWE-Agent','Aider','AutoCodeRover','Moatless Tools','Agentless')):
    vv=REC[nm];begin=ds+.15+j*.17
    r=pstep(t,begin,.72)
    if not r:continue
    yy=327+j*65;col=(C if j==0 else T if j==4 else BLUE)
    focus=1-.51*report*(j not in (0,4))
    xbase=1047;xx=xbase+315*vv/35;ww=(xx-xbase)*r
    etch(g,nm,1018,yy,25,F,r*focus,'right')
    line(g,(xbase,yy+13),(1375,yy+13),E,1.15,heads*.68*focus)
    rect(g,xbase,yy-12,ww,24,col,r*focus)
    etch(g,f'{vv:g}%',xx+19,yy,27,col,r*focus)
    if add and j in (0,4):
     actual=round(5*vv);q=pstep(t,changec-.16+(0 if j==0 else .37),.61);yy2=yy+25
     etch(g,f'{actual} / 500',xx-3,yy2+4,19,col,q,'right')
   if book:
    xx=1047+315*23/35;xx1=1047+315*33.2/35
    bracket(g,xx,662,xx1-xx,Y,book);etch(g,'51 题 · 10.2 个百分点',1392,708,27,Y,book,'right')
   if book:
    # The same test and the same core are latched. Only the external path remains movable.
    for ix,(p0,p1) in enumerate((((xc+79,yc-62),(813,248)),((xc-91,yc),(xc-156,yc)))):
     q=pstep(t,c.at('测试集和模型')-.19+ix*.48,.59)
     if q:
      x0,y0=p0;x1,y1=p1;path(g,[p0,((x0+x1)*.5,y0),((x0+x1)*.5,y1),p1],q,C,1.8,.62)
      if book>.80:check(g,x1,y1,8.7,True,book)
   if report:
    # A worked reporting line: fields appear separately as the narrator identifies their roles.
    aa=phase(t,mdl-.25,mdl+.41);bb=phase(t,kit-.24,kit+.43)
    x0=171;y0=712
    etch(g,'模型',x0,y0,24,C,report);etch(g,'GPT-4o',x0+70,y0,31,F,aa)
    etch(g,'×',x0+209,y0,35,M,bb);etch(g,'脚手架',x0+259,y0,24,T,bb);etch(g,'Agentless',x0+365,y0,31,T,pivotrow)

# The cropped repository becomes a fan of three *real* example pairs. The final pose
# remains mounted across the chapter boundary, so saying 三组 never shows just one.
PAIRS=((256.,483.),(730.,959.),(1186.,1415.))
def _pair(g,i,a,b,y,size,op=1,travel=None,highlight=0):
 ex=AR['train'][i];m=len(ex['input'][0]);marky=y-size/2+size/m*.5
 if op<.001:return
 for side,key,x in [(0,'input',a),(1,'output',b)]:
  # One visible row landmark is taken only AFTER the audience has had its turn.
  h=(0,0 if side else m-1,highlight) if highlight>.001 else None
  arcboard(g,ex[key],x,y,size,op,hl=h)
 q=(a+b)*.5
 if b-a>size+24:arrow(g,(a+size*.53+3,y),(b-size*.53-3,y),1,C,op*.76,1.9)
 if travel is not None:
  l=(a+size*.5-size/m*.5,marky);r=(b-size*.5+size/m*.5,marky);h=sin(pi*travel)*op
  if h>.002:
   path(g,[l,(q,marky-46),r],travel,Y,1.65,h*.73)
   xx,yy=transit(l,r,travel,38);tile(g,xx-size/m*.21,yy-size/m*.21,size/m*.42,PAL[ex['input'][0][-1]],h)
def _footprint(g,u,opacity):
 if opacity<.002:return
 # One unfinished bottom corner: anticipation of the fourth display, not its solution.
 for j,co in enumerate((C,Y)):
  cx=(566,1015)[j];top=612
  for i in range(3):
   path(g,[(cx-38+i*32,top+9),(cx-38+i*32,top),(cx-14+i*32,top)],u,co,2.2,opacity*.81)
def repo_to_arc(g,c):
 t=c.t;open_=c.at('仓库都是公开');train=c.at('预训练');remember=c.at('还是记得');same=c.at('同一段代码');infer=c.at('推理');new=c.at('拿走它熟悉');grid=c.at('三组网格');guess=c.at('记住你猜的');four=c.at('第四张');try_=c.at('试一试')
 p=phase(t,new-.38,new+.65)
 edge=-255+2115*p
 if p<1:
  op=1;ctx=g.c;ctx.save()
  # On ‘拿走’ the repository is physically swept away. Old letters and incoming
  # cells occupy opposite sides of the same moving paper edge, never the same pixels.
  ctx.new_path();ctx.move_to(edge,0);ctx.line_to(1640,0);ctx.line_to(1640,930);ctx.line_to(edge-135,930);ctx.close_path();ctx.clip()
  txt(g,'sphinx-doc / sphinx',143,231,35,C,op,'left')
  codes=[('-','return self._format_fields(…)'),('+','if self._config.napoleon_use_param:'),('+','    return self._format_docutils_params(fields)')]
  go=pstep(t,c.at('跑通了')-.11,.60)
  for j,(ch,st)in enumerate(codes):
   y=345+j*66;col=R if j==0 else G
   rect(g,147,y-21,737,45,inkcol(col,.23),op);txt(g,ch,170,y,30,col,op);txt(g,st,209,y,24,F,op,'left',641,MONO)
  if go:
   check(g,822,546,12,True,go*op);txt(g,'pytest',789,546,24,T,go*op,'right',font=MONO)
  k=pstep(t,open_-.13,.58);txt(g,'#5560 → #8713',140,643,30,T,k*op,'left')
  if k:
   x0,x1=1035,1467;line(g,(x0,350),(x1,350),C,2.4,op*k);line(g,(x0,513),(x1,513),O,2.4,op*k)
   txt(g,'公开仓库',1034,286,27,C,op*k,'left');txt(g,'模型训练',1034,453,27,O,op*k,'left')
   f=phase(t,train-.16,same+.18);xx,yy=transit((1221,350),(1360,513),f,26);dot(g,xx,yy,8,Y,op*k)
   u=phase(t,same-.23,same+.42)
   if u:
    txt(g,'napoleon_use_param',x0+4,545,23,O,u*op,'left',397,MONO)
    swish(g,1038,1308,566,t-same+.15,O,.66)
   for j,(tr,lb,co) in enumerate(((infer,'现场推理',T),(remember,'记得修法',VIO))):
    e=pstep(t,tr-.13,.52);yy=636+58*j
    if e:path(g,[(1360,516),(1362,yy),(1297,yy)],e,co,2.4,op*e);txt(g,lb,1271,yy,27,co,op*e,'right')
  ctx.restore()
 if p:
  ctx=g.c;ctx.save()
  ctx.new_path();ctx.move_to(-45,0);ctx.line_to(edge,0);ctx.line_to(edge-135,930);ctx.line_to(-45,930);ctx.close_path();ctx.clip()
  spread=phase(t,grid-.36,grid+.29)
  for j,(a,b)in enumerate(PAIRS):
   s=1 if j==0 else pstep(t,grid+.18+.15*(j-1),.55)
   if s:
    q=spread if not j else pstep(t,grid+.18+.15*(j-1),.55)
    left=mix(495,a,q)if j==0 else a+19*(1-q);right=mix(1105,b,q)if j==0 else b+19*(1-q)
    cy=mix(434,337,q)if j==0 else 337+167*(1-q);size=mix(272,159,q)if not j else 159
    _pair(g,j,left,right,cy,size,s)
    mk=pstep(t,guess-.10+j*.19,.49)
    if mk:
     txt(g,'ⅠⅡⅢ'[j],(a+b)*.5,cy+size*.5+41,23,M,s*mk)
  u=phase(t,four-.17,four+.72)
  if u:_footprint(g,u,p*u)
  if t>try_-.19:
   e=phase(t,try_-.17,try_+.55)
   path(g,[(747,614),(787,614),(819,614)],e,Y,2.15,p*e);mark(g,829,614,7,Y,p*e)
  ctx.restore()
def arc(g,c):
 t=c.t;a=c.at
 name=a('肖莱设计');inp=a('没有文字题干');ex=a('三到五个');grid=a('二维网格');pairs=a('输入输出示例');infer=a('要求你现场归纳');rule=a('抽象变换规则');test=a('全新测试网格');pixel=a('每一个像素');all_=a('前三组都在这儿');pred=a('先按你的猜法');first=a('看第一组');right=a('右上');left=a('输出的左上角');other=a('另两组也一样');final=a('左右翻转');end=a('逐格')
 show=phase(t,test-.22,test+.53)
 # The goal stays empty. Nothing in the preparatory motion encodes the answer.
 _footprint(g,1,(1-show)*(1-.84*phase(t,1.2,2.05)))
 if t<1.60:
  r=1-phase(t,.15,1.6);line(g,(747,614),(819,614),Y,2.15,r);mark(g,829,614,7,Y,r)
 near=phase(t,inp-.69,inp+.28)*(1-phase(t,ex-.63,ex+.33))
 # After the viewer's guess, come CLOSE to the actual red corner, then bring
 # the other two examples into focus. Nothing gives the answer away beforehand.
 inspect1=phase(t,first-.17,first+.53)*(1-phase(t,other-.31,other+.31))
 inspect2=phase(t,other-.18,other+.37)*(1-phase(t,final-.29,final+.34))
 for j,(x,z) in enumerate(PAIRS):
  wide=near+inspect1
  cy=337+(19*wide if j==0 else -12*wide)
  margin=(34*wide if not j else 9*inspect2);x1=x-margin;x2=z+margin
  sz=159+(75*wide if j==0 else -17*wide+26*inspect2)
  opacity=1-(.59*wide if j else .48*inspect2)
  trg=right if not j else other+.22+(j-1)*.43;stop=left+.65 if not j else other+.94+(j-1)*.37
  h=phase(t,trg-.12,trg+.36)*(1-phase(t,stop,stop+.55))
  t0=left-.35 if not j else other+.20+(j-1)*.49
  tr=phase(t,t0,t0+.64)if t0<t<t0+.64 else None
  _pair(g,j,x1,x2,cy,sz,opacity,tr,h)
  txt(g,'ⅠⅡⅢ'[j],(x1+x2)*.5,cy+sz*.5+41,23,M,opacity)
  if near:
   for xx,lab,co in [(x1,'输入',C),(x2,'输出',T)]:
    if j==0:txt(g,lab,xx,cy+sz*.5+44,28,co,near)
  # At “二维” measure the two edges of the real grid. Display the sizes as inspectable facts.
  di=phase(t,grid-.14+j*.085,grid+.43+j*.12)*(1-phase(t,infer-.37,infer+.04))
  if di:
   n=len(AR['train'][j]['input']);le=x1-sz*.5;yy=cy+sz*.5
   path(g,[(le-9,yy-sz),(le-9,yy+10),(le+sz,yy+10)],di,C,2.4,di)
   if di>.28:txt(g,f'{n} × {n}',x1,yy+44,23,C,di)
  ir=phase(t,all_-.08+j*.09,all_+.38+j*.10)*(1-phase(t,pred-.22,pred+.30))
  if ir:
   for xx in (x1,x2):line(g,(xx-sz*.5,cy+sz*.5+9),(xx+sz*.5,cy+sz*.5+9),T,2.6,ir)
  # Three observations meet at one unknown transformation, before the independent fourth input is exposed.
  ag=phase(t,infer-.13+j*.16,rule+.31+j*.08)*(1-phase(t,test-.42,test+.19))
  if ag:
   x0=(x+z)*.5;path(g,[(x0,cy+sz*.5+63),(x0,507),(803,574)],ag,(C,T,VIO)[j],2.15,ag*.79)
  if j==2 and ag:
   dot(g,803,574,39,Y,ag*.17);ring(g,803,574,39,Y,ag,2.4);txt(g,'f',803,574,37,Y,ag,font='math')
 if show:
  doc=AR['test'][0];c1,c2=566,1015;yy=628;sz=180
  arcboard(g,doc['input'],c1,yy,sz,show)
  reveal=phase(t,final-.07,end+.25)
  # The square lights up on arrival, not underneath a still-flying duplicate.
  done=0
  if reveal<1:arcboard(g,doc['output'],c2,yy,sz,show,open_=0)
  if 0<reveal<1:
   n=3;d=sz/n
   for ri,row in enumerate(doc['input']):
    for j,v in enumerate(row):
     p0=(c1-sz/2+(j+.5)*d,yy-sz/2+(ri+.5)*d);p1=(c2-sz/2+(n-.5-j)*d,yy-sz/2+(ri+.5)*d)
     u=clip((reveal*1.68-ri*.27-j*.035)/.96)
     if u>=1:
      tile(g,p1[0]-d*.5+1.5,p1[1]-d*.5+1.5,d-3,PAL[v],show);done+=1
     elif u>0:
      xx,yy0=transit(p0,p1,u,49+j*21);ww=(d-3)*(.57+.43*u)
      tile(g,xx-ww*.5,yy0-ww*.5,ww,PAL[v],min(1,u*4)*show)
  if reveal>=1:arcboard(g,doc['output'],c2,yy,sz,show);done=9
  txt(g,'新输入',414,yy,26,C,show,'right')
  if not reveal:txt(g,'先在心里填',1152,yy,27,Y,show*(1-phase(t,first-.28,first+.16)),'left')
  else:txt(g,f'{done} / 9',1152,yy,32,T,show,'left')
  px=phase(t,pixel-.14,pixel+.64)*(1-phase(t,all_-.20,all_+.25))
  if px:
   q=phase(t,pixel-.05,all_-.06);ix=min(8,int(q*9));row,col=divmod(ix,3)
   box(g,c2-sz/2+col*60+3,yy-sz/2+row*60+3,54,54,Y,px,sw=2.45)
  if not reveal:
   a0=a('填好第四张')+.36;u=phase(t,a0,first-.22);xx=c2+sz*.57
   if t>a0:path(g,[(xx+8,yy-sz*.47),(xx+21,yy-sz*.47),(xx+21,yy+sz*.47),(xx+8,yy+sz*.47)],u,Y,2.7,show*.92*(1-phase(t,first-.28,first+.16)))
