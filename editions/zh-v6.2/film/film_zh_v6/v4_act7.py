"""A drawing, a note, an ordered record and a stream of real words: four ways to take the measure outside."""
from rig4 import *
from studio_field import reel
from studio_industry import elevation
from studio_dates import seal
from studio_evidence import glyph
from studio_examples import MONO
from studio_corpus import RAW,ROWS,BASES,DOC,HITS,N,observe,bits,HIST
from itertools import permutations
from v4_act4 import paperbody,PAPER,INK
CLIN=json.loads((AS/'specimens.json').read_text())['clinical']
def miniature_record(g,x,y,theta,op,t):
 def contents():
  label(g,'ACI-BENCH    /    ACI001',-268,-117,23,'#625C52',op,'left')
  line(g,(-268,-83),(268,-83),'#A49E8F',1.5,op)
  label(g,CLIN['section'],-268,-28,27,INK,op,'left')
  label(g,CLIN['note'],-268,40,41,'#243E45',op,'left')
  label(g,'公开模拟病历 · 节选',-267,112,23,'#6B655A',op,'left')
 paperbody(g,x,y,602,324,theta,op,contents)
def workshop(g,c):
 t=c.t;gdp=c.at('GDPval')-.18;med=c.at('临床工作')-.22;echo=c.at('越像实际岗位')-.12
 from jobbench6 import work,fixture_sheet,details
 if t<gdp:
  work(g,c,gdp)
 elif t<med:
  to,theta,u,pose=fixture_sheet(g,c,gdp)
  details(g,c,*pose,theta,u)
  panelnote(g,'GDPval','用职业交付物考查实际工作',159,91,t-gdp,O)
  label(g,'制造工程 · 线缆卷盘夹具方案',mix(773,495,to),mix(780,681,to),27,M,u)
  if to:
   rr=easepos(t,c.at('检查的图纸')-.18,.86)
   x0=1137+118*(1-to)+120*(1-phase(to,.21,.91))
   xp,yp=mix(x0,1027,rr),mix(374,395,rr)
   angle=mix(.43+.42*to+.068*sin((t-gdp)*.49),.11,rr)
   reel(g,xp,yp,mix(1.09,.84,rr),angle,to*(1-phase(rr,.37,.77)))
   rr=phase(rr,.46,1.0)
   if rr:
    elevation(g,1027,395,1.03,'end',rr,to);elevation(g,1312,420,.72,'side',rr,to)
    label(g,'端视',1027,640,27,C,rr);label(g,'侧视',1312,640,27,T,rr)
   path(g,[(812,556),(880,556),(921,508)],to,O,1.8)
  count=c.at('只回答一个数');check_=c.at('替代这份交付')
  if count-.22<t<med-.02:
   uu=during(t,count-.22,med-.02,.42);rr=phase(t,count-.21,count+.51)
   x,y=1154,729
   tag='一个数'
   path(g,[(x-89,y),(x-89,y+20),(x-48,y+20)],rr,O,2.3,uu)
   path(g,[(x+89,y),(x+89,y+20),(x+48,y+20)],rr,O,2.3,uu)
   label(g,tag,x,y,31,O,rr*uu)
   # One number doesn't contain either orthographic view. The obstruction is
   # a real separation in the picture, not a statement pasted on the plate.
   tail=enter(t,check_-.18,.57);gap=phase(t,check_-.25,check_+.48)
   if tail:
    for j,(vx,col) in enumerate(((1027,C),(1312,T))):
     a1=enter(t,check_-.14+.13*j,.50);left=x+(2*j-1)*62
     path(g,[(left,709),(vx,692),(vx,mix(555,653,gap))],a1,col,2.,uu*(1-gap*.71))
    if gap:ring(g,x,y-45,13+5*gap,R,tail*uu,2.12)

  if t>med-.43:shade(g,phase(t,med-.43,med))
 else:
  u=enter(t,med,.57);s=c.u('起草记录',.69);read=c.u('对话里',.58);d=c.u('辅助临床决策',.61)
  panelnote(g,'MedHELM','按临床任务分别评估模型',159,96,t-med,C)
  note_x=1060+95*(1-u);note_y=371-76*(1-u);miniature_record(g,note_x,note_y,.017+.047*(1-u),u,t-med)
  label(g,'就诊对话',197,282,34,T,s,'left')
  for j,line_ in enumerate(('“my left wrist and hand','has been bothering me”')):
   mark(g,line_,195,376+j*60,39,t-c.at('起草记录')-.12*j,'#E8EEEC','left',op=s)
  if read:
   path(g,[(277,482),(547,482),(650,436),(750,436)],read,T,2.5);point(g,mix(343,750,read),mix(482,436,read),6,T,read)
  faithful=c.at('忠实写进病历');decision=c.at('后一项');endtake=c.at('越像实际岗位')
  if faithful-.50<t<decision+.67:
   ph=enter(t,faithful-.41,.54);fade=1-phase(t,decision+.16,decision+.67)
   path(g,[(272,410),(527,410)],ph,T,2.6,fade);path(g,[(note_x-265,note_y+79),(note_x+97,note_y+86)],ph,T,2.6,fade)
  if decision+.15<t<endtake-.30:
   dt=decision+.27;tent=enter(t,dt,.58)*(1-phase(t,endtake-.73,endtake-.30))
   label(g,'另一种验收',405,677,30,V,tent)
   path(g,[(526,674),(688,674),(730,665),(858,665)],tent,V,1.95,tent)
  if d:
   visible=1-phase(t,echo+.18,echo+.85)
   label(g,'记录：忠实整理',1059,610,29,T,d*visible);label(g,'决策：另行评估',1059,664,29,V,d*visible)
  if t>echo:
   m=c.at('材料');work=c.at('操作');verify=c.at('验收标准');close=c.at('贴近程度')
   eff=enter(t,verify-.05,.65);def_=enter(t,close-.17,.63)
   u1=enter(t,m-.17,.55);u2=enter(t,work-.12,.57);u3=enter(t,verify-.08,.74)
   if t<m+.47:
    q0=phase(t,echo,m+.37);x,y=transit((533,452),(849,417),q0,29)
    ring(g,x,y,11,O,sin(pi*q0),2.1)
   # Track three parts of the real conversation to the same three parts of the
   # note. A correct record supports this task; it says nothing about a diagnosis.
   words=(('左侧',300,822),('腕部',392,908),('手部',533,1062))
   for j,(nm,sx,tx) in enumerate(words):
    x=674+j*207;uu=enter(t,m-.14+j*.105,.48)
    if uu:label(g,nm,x,622,34,T,uu)
    if u2:
     q0=phase(t,work+.06+j*.15,verify+.48+j*.19);xp,yp=transit((sx,464),(x,653),q0,-47)
     if 0<q0<1:dot(g,xp,yp,6.4,T,sin(pi*q0)**.35)
    if u3:
     q0=phase(t,verify+.12+j*.28,verify+1.08+j*.31);px,py=transit((tx,note_y+82),(x,683),q0,-32)
     if 0<q0<1:dot(g,px,py,6.4,O,sin(pi*q0)**.42)
     if q0>.88:check(g,x,684,12,True,clip((q0-.88)/.12))
   up=phase(t,verify+.42,close+.13)
   if up:path(g,[(526,624),(503,624),(503,681),(526,681)],up,O,2.0)
   if eff:
    label(g,'生态效度',329,650,38,O,eff)
    label(g,'材料、操作、验收贴近工作的程度',821,760,28,M,def_)
NAMES=('青蛙与沸水','能量与质量','烂番茄零分','捷豹驱动形式');PALS=(T,Y,V,C)
PERMS=list(permutations(range(4)));PERMS=[v for v in PERMS if v!=(0,1,2,3)]
# A small language of orderings: draw a first record, then draw from only the records
# still on the table.  Its 24 complete histories have probabilities summing to one.
PAIR=((0,-.3,-1.5,-1.25),(-1.31,0,-.27,-.97),(-1.60,-.79,0,-.39),(-1.73,-.82,-1.22,0))
INITIAL=(.41,.22,.20,.17)
@lru_cache(maxsize=24)
def permval(x):
 value=log(INITIAL[x[0]]);used={x[0]}
 for a,b in zip(x,x[1:]):
  value+=PAIR[a][b]-log(sum(exp(PAIR[a][j]) for j in range(4) if j not in used))
  used.add(b)
 return value
def bundled(g,x,y,i,a,small=1,letters=1):
 ctx=g.c;ctx.save();ctx.translate(x,y);ctx.scale(small,small)
 co=PALS[i];glyph(g,i,-139,0,.80,co,1,a);label(g,NAMES[i],-91,0,31,F,a*letters,'left');line(g,(100,-15),(100,15),co,1.6,a*letters)
 label(g,'题＋答',116,0,22,co,a*letters,'left');ctx.restore()
def order(g,c):
 t=c.t;scram=c.at('只换四道题')-.16;pts=c.at('把这些分数排开')-.14;tail=c.at('注意这个反例')-.16
 if t<c.at('拿这四道题')-.37:
  from order6 import publiccase
  publiccase(g,c,c.at('拿这四道题')-.37)
  return
 if t<pts:
  a=enter(t,c.at('拿这四道题')-.37,.64);flip=enter(t,scram,.68);sc=c.u('整段对数概率')
  from permutation6 import pair,gather
  bank=c.at('许多份')-.04;more=enter(t,bank-.36,.47)
  leave=1-phase(t,pts-.79,pts);a*=leave
  label(g,'原始顺序',415,147,37,T,a);label(g,'保持题干与答案配对',417,204,25,M,a)
  joined=c.at('整道拴在一起');original=c.at('先按公开材料');when=c.at('拿这四道题')
  for i in range(4):
   y=303+i*103;v=enter(t,when-.30+i*.22,.54);bundled(g,408,y,i,a*v,letters=0)
   label(g,NAMES[i],310,y,32,F,a*v,'left')
   link=enter(t,joined-.16+.13*i,.48);pair(g,584,y,PALS[i],a*v*(.42+.58*link),'题答')
   if i<3:
    v0=enter(t,original-.13+.19*i,.54);line(g,(268,y+40),(268,y+66),PALS[i],1.65,v0*a)
   sx=during(t,joined-.14+.16*i,joined+1.05+.16*i,.32);gl=enter(t,joined-.12+.11*i,.47)
   if sx:path(g,[(537,y+27),(537,y+37),(630,y+37),(630,y+27)],gl,PALS[i],2.7,a*sx)
  if sc:
   label(g,f'log P = {permval((0,1,2,3)):.2f}',430,752,32,O,a*sc)
   point(g,422,239,7.8,Y,sc)
  if flip and more<.999:
   op=flip*(1-more)
   u=(t-scram)/2.23;k=max(0,int(u));f=p5(clip((u-k)*2.65));first=(0,1,2,3)if k==0 else PERMS[((k-1)*9+4)%23];second=PERMS[(k*9+4)%23]
   for i in range(4):
    ow,nw=first.index(i),second.index(i)
    q=sin(pi*f)**.65;y=mix(303+103*ow,303+103*nw,f);x=1068+203*q*(1 if nw>ow else -1) if ow!=nw else 1068
    # The question tag and its answer use the same position throughout the swap.
    pair(g,x+25,y,PALS[i],op,'ABCD'[i]+'答')
    glyph(g,i,x-69,y,.77,PALS[i],1,op)
   label(g,'整题换位',1068,147,36,C,op);label(g,'一次排列，一个分数',1063,205,25,M,op)
   label(g,f'{permval(second if f>.65 else first):.2f}',1065,749,35,C,op);label(g,'示意',1170,749,21,M,op)
  gather(g,c,PERMS,PALS,bank)
 else:
  a=enter(t,pts,.58);dots=c.u('排开',.81);gold=c.at('原序点');obs=c.at('可交换性');ct=c.u('按年代',.74)
  # Individual ranks from the 23 alternate orderings of the four fixed items; no made-up p-value.
  values=[permval(p)for p in PERMS];og=permval((0,1,2,3));low=min(values)-.25;hi=max(og,max(values))+.24
  X=lambda v:224+(v-low)/(hi-low)*1166
  path(g,[(185,560),(1420,560),(1407,553)],enter(t,pts+.28,.78),M,2.4)
  from permutation6 import score
  placed=score(g,c,PERMS,PALS,sorted(zip(PERMS,values),key=lambda p:p[1]),X,pts,c.at('许多份')-.04)
  title=enter(t,pts+.72,.64)
  label(g,'23 种其他排列',329,617,29,C,title);label(g,'整组对数概率 · 示意',1361,618,26,M,title,'right')
  d=easepos(t,gold-.17,.92);gx=X(og);xx,yy=transit((422,239),(gx,530),d,31.)
  point(g,xx,yy,mix(7.8,12,d),Y,1);label(g,'公开原序',gx-4,458,30,Y,phase(d,.73,1))
  # One actual difference can be measured with a ruler. The mean in this miniature
  # calculation is over the 23 other orderings; the canonical point keeps its own place.
  alone=c.at('孤零零');cohort=c.at('有了这一排');far=c.at('原序离普通')
  intro=c.at('很具体的前提')-.25
  if alone-.10<t<intro:
   vis=during(t,alone-.10,intro,.41);show=enter(t,cohort-.20,.88);bar=enter(t,far-.15,.97)
   if show<.99:
    # Dim the *other* sample, then return it; the original number never changes.
    rect(g,170,379,X(max(values))-144,168,BLACK,vis*(1-show)*.87)
   mean=sum(values)/len(values);mx=X(mean);zz=show*vis
   if zz:
    line(g,(mx,485),(mx,558),C,2.2,zz);label(g,f'乱序均值  {mean:.2f}',mx,424,30,C,zz)
    label(g,f'{og:.2f}',gx,390,29,Y,zz)
   if bar:
    yy=327;path(g,[(mx,yy+12),(mx,yy),(gx,yy),(gx,yy+12)],bar,O,2.35,vis)
    label(g,f'同一批题  ·  相差 {og-mean:.2f} nat',.5*(mx+gx),yy-43,31,O,bar*vis)
  if t<tail:
   panelnote(g,'可交换性检验','整道题换序，比较整组似然',177,116,t-obs+.13,T)
   if t>obs:swish(g,245,1342,687,t-obs+.08,O,.88)
   aa=c.at('换顺序本不该');bb=c.at('在许多组题上')
   entry=c.at('很具体的前提')-.17;leave=c.at('这叫可交换性')
   if entry<t<leave+.52:
    show=during(t,entry,leave+.52,.47);sw=phase(t,c.at('没见过原序')-.08,aa+.76)
    # Four bound question–answer units move; neither the observed score nor
    # the choices inside one question are being shuffled.
    target=(2,0,3,1)
    for j,col in enumerate(PALS):
     xp=808+97*mix(j,target.index(j),sw);yp=315+(j-1.5)*46*sin(pi*sw)
     box(g,xp-28,yp-19,56,38,col,show,inkcol(col,.33),1.8)
     label(g,'ABCD'[j],xp,yp,23,F,show)
    if show:label(g,'整题换位',674,318,24,M,show)
   if aa<=t<bb:
    # Under the null, the privileged label could have landed on any ordering;
    # move only the open marker, never the observed scores.
    phase_=(t-aa)/.84;jj=int(phase_);frac=phase_-jj;idx=(7+jj*7)%len(placed)
    xx,yy=placed[idx];ring(g,xx,yy,15+7*sin(pi*frac),F,max(.1,sin(pi*frac)),1.8)
    label(g,'看随机抽到的排列',860,216,29,M,during(t,aa,bb,.36))
   if t>=bb:
    it=enter(t,bb-.04,.72);te=c.at('靠右');mag=enter(t,te-.25,.63)
    # Extend the *measurement rule*, not the invented evidence. Additional
    # shards have symbols, not made-up observed effect sizes or a fake p-value.
    xx=838;label(g,'每一组',xx-200,293,31,C,it);label(g,'原序 − 乱序均值',xx+89,293,35,F,it)
    if mag:
     path(g,[(xx-47,343),(xx-47,353),(xx+226,353),(xx+226,343)],mag,C,2.1)
     label(g,'跨组比较',xx+90,389,27,T,mag)
  else:
   from order6 import cause
   cause(g,c,tail,gx)
def geometry(g):
 key='native'
 if key in GRID:return GRID[key]
 rows=[];tokens=[];ys=[168,219,287,339,391,444,518,568]
 for ri,(tag,line_,kind)in enumerate(RAW):
  # Measure complete source runs at a stable em, including punctuation. Designed as a monospace engraving.
  sz=min(29.,1240./max(1,g.measure(line_,29,font=MONO))*29.)
  x0=(228 if ri in (0,2,6) else 247 if ri in (1,7)else 285)
  spans=[(m.start(),m.end())for m in re.finditer(r"[a-z0-9]+(?:[’'][a-z]+)?",line_,re.I)]
  cur=[]
  # Font shaping may proportionally condense at export on systems with hinting: measure prefix against the same layout.
  for l,r in spans:
   xa=x0+(g.measure(line_[:l],sz,font=MONO) if l else 0);xb=x0+g.measure(line_[:r],sz,font=MONO)
   cur.append((xa,xb));tokens.append((ri,xa,xb))
  assert len(cur)==len(ROWS[ri]);rows.append((x0,ys[ri],sz,cur))
 GRID[key]=(rows,tokens);return rows,tokens
GRID={}
def windows(g,c):
 t=c.t;rows,ts=geometry(g);lane=c.at('布隆过滤器')-.26;full=c.at('五十三个窗口');end=c.at('整页拿走');back=c.at('倒回来');restore=c.at('保留通用许可证');mask=c.at('确认撞题');survive=c.at('五十二个位置')
 scan=c.at('亮窗每走一格');source=c.at('连续的十三词');demo=c.at('看这份短文');front=c.at('上面是许多');truth=c.at('下面是跟评测')
 enter_=enter(t,.04,.63);p=phase(t,source-.18,source+.57)
 from window6 import inspect,bands,held_words,chip_state
 idx,settled=inspect(c,t)
 j=int(idx);_,positions,maybe_,fact=observe(j);hide=phase(t,end-.11,end+.93)*(1-phase(t,back-.10,back+.83));wl=c.u('保留通用许可证',.66);ms=c.u('确认撞题',.93);board=enter_
 label(g,'13-gram',159,88,42,Y,enter(t,source-.17,.60),'left');label(g,'公开材料拼接 · 65 词',1471,83,23,M,enter_,'right')
 for ri,((cat,st,kind),(x,y,sz,tr))in enumerate(zip(RAW,rows)):
  fall=clip(hide*1.28-ri*.031);dy=6*fall**2;x+=3*fall*(ri-3);y+=dy;op=(1-.855*fall**1.8)*board;co=(G if wl and kind=='muted' else M if kind=='muted' else T if kind=='code' else F)
  if ri in (0,2,6):label(g,cat,183,y,24,(O,T,V)[(0,2,6).index(ri)],op,'right')
  txt(g,st,x,y,sz,co,op,'left',font=MONO)
  if ms and ri==6:
   for a,b in tr:
    rect(g,a-1.5,y-19,b-a+3,37,BLACK,ms*.83)
    line(g,(a,y+15),(b,y+15),R,2.3,ms)
    for ix in range(1,max(2,int(b-a-8)),15):line(g,(a+ix,y+11),(min(b,a+ix+12),y-11),R,1.1,ms*.75)
  if wl and ri<2:line(g,(x,y+21),(tr[-1][1],y+21),G,1.55,wl*op)
 if p and t<end+.39:
  old=1-phase(t,end-.18,end+.39)
  last_=easepos(t,truth+.46,.37)
  active=(O if front+.12<t<truth-.20 and fact else blend(Y,R,last_) if fact=='题面' else Y)
  bands(g,rows,BASES,RAW,idx,active,p*settled*old)
 if t<lane:
  z=c.u('便于查找',.54);label(g,'一窗十三词',800,681,41,Y,p)
  if z:
   for i in range(13):
    k=enter(t,c.at('便于查找')-.24+.062*i,.48);row,x1,x2=ts[j+i];src=((x1+x2)/2,rows[row][1]+22)
    xx=559+i*40.;yy=742
    px,py=transit(src,(xx,yy),p5(k),18.)
    if k<.998:point(g,px,py,4.8,Y,k)
    else:rect(g,xx-8,yy-6,16,12,C,.83)
  held_words(g,c,j,idx-j,p)
 elif t<end+.51:
  a=enter(t,lane,.62)*(1-phase(t,end-.10,end+.51));cx,cy=204,646
  for n in range(128):
   xx=cx+n%32*18.2;yy=cy+n//32*17.1
   col=T if n in bits else '#333B3C';rect(g,xx,yy,13.0,12.1,col,a)
   if n in positions:box(g,xx-1.1,yy-1.1,15.5,15.1,O if n not in bits else Y if maybe_ else C,a*settled,sw=1.8)
  label(g,'布隆过滤器',cx,751,30,C,a,'left')
  label(g,'命中后再核对原文',cx+189,751,26,M,a*enter(t,c.at('核对原文')-.15,.49),'left')
  rr=ts[j+6][0];start_=(sum(ts[j+6][1:])/2,rows[rr][1]+20)
  neg=c.at('一次阴性');hit=c.at('可能见过');verify=c.at('核对原文')
  for start in (lane+.16,neg-.21,hit-.13,verify-.12):
   for i,n in enumerate(positions):
    v=clip((t-start-.08*i)/.53)
    if v<=0 or v>=1 or settled<.84:continue
    fin=(cx+n%32*18.2+6,cy+n//32*17.1+5);xx,yy=transit(start_,fin,p5(v),34+5*i)
    dot(g,xx,yy,4.0,Y if maybe_ else C,a*sin(pi*v)**.72)
  if t>=full-.14:
   label(g,'53 个窗口',1199,674,38,F,a*c.u('五十三个窗口'));label(g,'2 处精确重合',1199,738,29,O,a*c.u('两处都亮了'))
  else:chip_state(g,c,j,fact,a*settled)
 if t>=end:
  if hide>.02:
   slash=p5(phase(hide,.12,.90));path(g,[(235,567),(1394,174)],slash,R,4.4,hide*.83);label(g,'整页剔除',800,683,43,R,phase(hide,.43,.91))
  v=c.u('确认撞题',.7);u=c.u('五十二个位置',.67)
  explain=enter(t,survive+.65,1.05);cash=c.u('什么角色',.64)
  choice=c.at('这不是多加');last=c.at('少扔掉一整页')
  # This strip changes its unit of comparison. Retire the single explanation
  # before either of the two alternative policies is written in the same band.
  oldcaption=1-phase(t,choice-.43,choice-.08);decision=phase(t,choice+.05,choice+.75)
  if wl and oldcaption:label(g,'通用模板保留',303,702,31,G,wl*oldcaption)
  if v:
   for h in range(65):
    x=634+h*12.4;excluded=48<=h<61;co=R if excluded else T
    wave=phase(t,choice-.12+h*.016,choice+.51+h*.016)
    rect(g,x,669,8,22 if excluded else 14,co,v*(1-wave))
    if wave:line(g,(x,677),(x+8,677),M,1.5,wave*.70)
    if explain and not excluded:
     # Send each kept position, not merely 52 anonymous decorative dots, into
     # the aggregate.  The excluded range retains its holes in the lower ribbon.
     dest=(x,713);s0=(ts[h][1]+ts[h][2])*.5;sy=rows[ts[h][0]][1]+18
     z=clip((t-(survive+.78+h*.052))/.73)
     if 0<z<1:
      xx,yy=lerp((s0,sy),dest,p5(z));dot(g,xx,yy-30*sin(pi*z),3.5,T,explain*.85)
     if z>=1:rect(g,x,713,8,11,T,v*.92)
    elif explain and excluded:
     line(g,(x,722),(x+7,722),E,1.5,v)
   if u and oldcaption:label(g,'52 个仍训练   /   13 个不计损失',1041,760,29,T,u*oldcaption)
   if decision:
    label(g,'整页剔除',428,674,31,M,decision,'right')
    label(g,'仅遮重合',428,722,31,T,decision,'right')
    dz=enter(t,choice+1.1,.51);label(g,'0 / 65',570,674,32,M,dz,'right')
    ll=enter(t,last-.14,.68);label(g,'52 / 65',570,722,32,T,ll,'right')
    if ll:
     # The unmasked real code contributes its own positions; the 13 red ones
     # remain holes. The 53 lookup windows are not the training denominator.
     va=during(t,last-.08,c.d-.18,.40)
     for h in (20,25,30,35,40,45):
      f=clip((t-(last+.04*(h-20)))/1.10)
      if 0<f<1:
       row,a0,a1=ts[h];src=((a0+a1)/2,rows[row][1]+16);dest=(638+12.4*h,713)
       px,py=transit(src,dest,p5(f),-32);dot(g,px,py,4.9,T,va)
  if cash:
   for ri,co,word in [(0,G,'许可证'),(2,T,'代码'),(6,R,'试题')]:
    _,yy,_,_=rows[ri];swish(g,86,183,yy+21,t-c.at('什么角色')-(ri/2)*.35,co,.53,2.1)
def calendar(g,c):
 t=c.t;secret=c.at('一套不公开的题');audit=c.at('专家回头重审');end=c.at('三件事修的')
 if t<secret-.35:
  u=enter(t,.07,.62);size=1340;ll=128;yy=513
  # Follow the 65 slots the audience just saw. With fixed data they keep
  # reappearing; when the proposal becomes chronological those slots make the date ruler.
  fixed=c.at('静态公开');clean=c.at('清洗');change=c.at('出题那一天')
  fold=phase(t,.62,fixed+.62);time_=phase(t,change-.27,change+1.08);clear=1-time_
  if fold<1:endpaper(g,'7-3',0,0,1,1-fold)
  if clear and t>.10:
   for j in range(65):
    # Lift the lower row that was actually on screen. A masked position remains
    # a gap in the ribbon; the new date axis does not restore a discarded loss.
    excluded=48<=j<61;oldx=638+j*12.4;oy=722 if excluded else 718.5;lane=323+j*15.
    x,y=transit((oldx,oy),(lane,441),fold,28+26*(j%11)/10)
    nx=mix(x,ll+size*j/64,time_);ny=mix(y,yy,time_)
    if excluded:line(g,(nx-3.5,ny),(nx+3.5,ny),E,1.55,fold*clear)
    else:rect(g,nx-4,ny-5.5-2*fold,8,11+4*fold,T,fold*clear)
   f=during(t,clean-.22,change+.31,.42)
   if f:
    pos=phase(t,clean-.16,change+.20);xx=323+960*pos
    path(g,[(xx-29,420),(xx-29,413),(xx+29,413),(xx+29,420)],1,Y,2.4,f)
    label(g,'同一批公开题',807,333,34,F,f)
  axisvis=phase(t,change-.37,change+.97)
  label(g,'LiveCodeBench',178,168,50,C,c.u('LiveCodeBench',.6),'left');label(g,'按竞赛日期连续收录',179,225,28,M,c.u('竞赛日期',.55),'left')
  path(g,[(ll,yy),(ll+size,yy),(ll+size-13,yy-7)],axisvis,F,2.15)
  for j,(label_,day,val)in enumerate(HIST['releases']):
   x=ll+193+j*201;v=enter(t,c.at('竞赛日期')-.15+j*.14,.53);ht=158*val/1055
   rect(g,x-8,yy-ht*v,16,ht*v,C,v);label(g,day[:7],x,yy+45,26,M,v);label(g,str(val),x,yy-ht*v-26,27,T,v)
  pivot=c.u('训练截止日期',.62);x0=802
  if pivot:line(g,(x0,yy-246),(x0,yy+10),Y,3.0,pivot);label(g,'训练截止日（示意）',x0,yy-284,31,Y,pivot)
  select=c.u('后来才发布',.69)
  if select:path(g,[(x0,yy+99),(x0+6,yy+110),(1426,yy+110),(1426,yy+99)],select,T,2.1);label(g,'只取截止日之后',1124,yy+167,28,T,select)
 else:
  from calendar6 import shelf
  shelf(g,c,secret-.35)

def orbit(g,c):
 from orbit6 import recap
 recap(g,c)
