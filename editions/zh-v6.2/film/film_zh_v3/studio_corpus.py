"""The same thirteen-word window is used to draw geometry, set bits and verify original text."""
from ink import *
from motion import transit,guide,out3
from ink_words import letter,swish,carryword
from studio_examples import pstep,silk,mark,area,MONO,VIO,BLUE,AQUA
from timeline3 import W,OLD,clock,S
from functools import lru_cache
import re,json
def words(s):return re.findall(r"[a-z0-9]+(?:[’'][a-z]+)?",s.lower().replace("'","’"))
MIT='Permission is hereby granted, free of charge, to any person obtaining a copy'
janet=json.loads((W/'source/gsm8k-first.json').read_text())['question']
J13=' '.join(words(janet)[:13])
# A composite, labeled as such. Real code lines are copied directly from the upstream patch.
RAW=[
 ('许可证',MIT,'muted'),('', 'of this software and associated documentation files','muted'),
 ('Sphinx','def _parse_other_parameters_section(self, section: str) -> List[str]:','code'),
 ('','if self._config.napoleon_use_param:','code'),
 ('','fields = self._consume_fields(multiple=True)','code'),
 ('','return self._format_docutils_params(fields)','code'),
 ('GSM8K',J13,'question'),('',' '.join(words(janet)[13:17]),'question')]
ROWS=[words(s)for _,s,_ in RAW];DOC=tuple(w for r in ROWS for w in r);BASES=[];n=0
for r in ROWS:BASES.append(n);n+=len(r)
N=len(DOC)-12
# Two signatures in this tiny index: a benchmark question and an incidental boilerplate phrase.
# The same 64-bit base-257 fingerprint is reused across windows. Indexing, not file verification.
MOD=1<<64
@lru_cache(None)
def power(n):return pow(257,n,MOD)
@lru_cache(None)
def polynomial(bs):
 h=0
 for b in bs:h=(h*257+b+1) % MOD
 return h
def seeded(bs):return (19*power(len(bs))+polynomial(bs))%MOD
def index3(h):
 h2=(((h>>32)^h)*0x9e3779b97f4a7c15)&(MOD-1)
 return tuple(((h>>16)+j*((h2>>25)|1)+j*j*37)%128 for j in range(3))
def sites(x):return index3(seeded(' '.join(x).encode()))
def window_signatures(doc,k=13):
 # Remove the departing word and its space; append one space and the arriving word.
 # After token lengths are cached the moving window never rereads its twelve shared words.
 if len(doc)<k:return
 data=[w.encode()for w in doc];initial=b' '.join(data[:k])
 length=len(initial);p=polynomial(initial)
 yield (19*power(length)+p)%MOD
 for i,new in enumerate(data[k:]):
  left=data[i]+b' ';right=b' '+new
  length-=len(left);p=(p-polynomial(left)*power(length))%MOD
  p=(p*power(len(right))+polynomial(right))%MOD;length+=len(right)
  yield (19*power(length)+p)%MOD
SIGNATURES=tuple(window_signatures(DOC))
corpus=[(tuple(words(MIT)),'模板'),(tuple(words(J13)),'题面')];indices={a:b for a,b in corpus};bits=set(q for a,b in corpus for q in sites(a))
def observe(j):
 group=DOC[j:j+13];bs=index3(SIGNATURES[j]);maybe=all(z in bits for z in bs);return group,bs,maybe,indices.get(tuple(group)) if maybe else None
HITS=[i for i in range(N)if observe(i)[-1]]
def bp(b):return (114+(b%32)*23.2,607+(b//32)*24)
def line_design(g,width,s,fs,ranges):
 # This underline is measured at one stable em size, then scaled using the parent transform.
 scale=min(1,width/max(1,g.measure(s,fs,font=MONO)));fs*=scale;wordw=[g.measure(v,fs,font=MONO) for v in ranges]
 advance=g.measure('00',fs,font=MONO)-g.measure('0',fs,font=MONO)
 return fs,advance or fs*.6
LL=(186,201,189,222,250,250,186,201)
def desk(g,select=None,show=1,erase=0,wl=0,tilt=0,mask=0,hit=None,accent=-1,status=0):
 if show<=.001:return
 # Eight lines are one object. Text is real and legible; the moving window supplies the parsing.
 for j,(category,text,kind)in enumerate(RAW):
  yy=224+j*39.;x0=LL[j];co=(M if kind=='muted' else T if kind=='code' else F)
  # An entire sheet removed from training actually takes every line with it. Restore the
  # same ink in reverse before masking only the thirteen matching words.
  slip=clip(erase*1.28-j*.039)
  yy+=(197+17*j)*slip*slip
  x0+=(j-3)*7*slip
  original=show*(1-slip**1.8);a=original
  if wl and kind=='muted':co=blend(co,G,wl)
  if status and j==6:co=R
  if j in (0,2,6):txt(g,category,140,yy,20,(O,T,Y)[(0,2,6).index(j)],a,'right')
  if a<.004:continue
  fs,_=line_design(g,1265,text,26,ROWS[j])
  # In normal reading the unmodified program keeps source punctuation and indentation.
  txt(g,text,x0,yy,fs,co,a*(.74 if kind=='muted' else .94),'left',font=MONO)
  if wl and j<2:line(g,(x0-10,yy+17),(x0+g.measure(text,fs,font=MONO)+5,yy+17),G,1.5,a*wl)
  if mask and j==6:
   width=g.measure(text,fs,font=MONO)+12;rect(g,x0-5,yy-17,width,35,BLACK,a*mask*.86)
   for ix in range(0,round(width)-22,19):
    line(g,(x0+ix,yy+16),(x0+ix+20,yy-15),R,1.5,a*mask*.86)
 if select is not None and show>.01:
  k=int(select);frac_=select-k;col=Y if hit is None else R if hit=='题面' else O
  for row,(cat,text,kind) in enumerate(RAW):
   start=BASES[row];L=len(ROWS[row]);a=max(start,select);b=min(start+L,select+13)
   if b<=a:continue
   fs,_=line_design(g,1265,text,26,ROWS[row]);xx=LL[row];yy=224+row*39
   tokens=list(re.finditer(r"[a-z0-9]+(?:[’'][a-z]+)?",text,re.I));lspace=g.measure('00',fs,font=MONO)-g.measure('0',fs,font=MONO)
   def p(i,end=False):
    if i<=0:return 0.
    if i>=len(tokens):return float(len(text))
    j=int(i);u=i-j;return mix(tokens[j].start(),tokens[min(len(tokens)-1,j+1)].start() if j+1<len(tokens) else len(text),u)
   l=xx+p(a-start)*lspace-4;r=xx+p(b-start)*lspace-4
   if r-l<2:continue
   rect(g,l,yy-16,r-l,32,inkcol(col,.24),show*(1-erase)*.76)
   # Repaint the selected original letters above the fill; no double-labelled tokens.
   ctx=g.c;ctx.save();ctx.rectangle(l,yy-20,r-l,42);ctx.clip();txt(g,text,xx,yy,fs,F,show*(1-erase),'left',font=MONO);ctx.restore()
   line(g,(l,yy+17),(r,yy+17),col,2.5,show*(1-erase));line(g,(l,yy-16),(r,yy-16),col,1,show*(1-erase)*.76)
def comb(g,t,index,op,picked=1):
 # The reading tray is a magnified view of this very window. Twelve words keep their place
 # relative to one another; the first leaves the lens just as the fourteenth enters it.
 if op<.002:return
 j=max(0,min(N-1,int(index)));a=index-j
 ctx=g.c;ctx.save();ctx.rectangle(99,543,1402,209);ctx.clip()
 pitch=105;yy=637
 for z in range(-1,14):
  loc=j+z
  if not 0<=loc<len(DOC):continue
  x=153+(z-a)*pitch;vis=clip(min((x-69)/83,(1534-x)/83))*op
  if vis<.003:continue
  v=DOC[loc];alpha=vis*(.5+.5*picked);wid=min(96,g.measure(v,24,font=MONO)+13)
  rect(g,x-wid/2,yy-19,wid,38,inkcol(C,.17+.10*(z in(0,12))),alpha)
  txt(g,v,x,yy,25,F,alpha,width=87,font=MONO)
  if 0<=z<=12:txt(g,str(z+1),x,yy+69,20,Y if z in(0,12)else M,alpha)
 ctx.restore()
 path(g,[(106,661),(106,674),(1492,674),(1492,661)],1,Y,1.8,op)
 txt(g,'13-gram · 连续 13 词',800,568,33,Y,op)
def filters(g,t,op,idx,built=1,hit=None,ping=0,verify=0,count=None):
 if op<.002:return
 group,bs,maybe,match=observe(idx); col=R if match=='题面' else O if match=='模板' else C
 for k in range(128):
  xx,yy=bp(k);on_=k in bits;act=k in bs
  rect(g,xx,yy,17.8,14.8,('#3F839D' if on_ else '#252525'),op*(.65+.35*built))
  if on_:rect(g,xx+3,yy+3,11.8,8.8,BLUE,op*built)
  if act and built:box(g,xx-1.0,yy-1.0,19.8,16.8,col,op,sw=2.1)
  if act and ping and built:line(g,(xx-1,yy+20),(xx+19,yy+20),Y,2,op*ping)
 txt(g,'布隆过滤器',111,553,30,C,op,'left');txt(g,'128 位 · 每窗查三位',312,555,22,M,op,'left')
 if count is not None:
  xx=1036;txt(g,'精确重合窗口',xx,560,27,F,op,'left')
  txt(g,f'{count} / {N}',xx,628,48,Y if count else M,op,'left')
  txt(g,'此例：重合窗数 / 全部窗口',xx,702,22,M,op,'left')
 elif verify:
  txt(g,'一位为 0 → 排除' if not maybe else '三位皆 1 → 复核原文',1024,632,32,T if not maybe else O,op,'left')
def register(g,checked,op=1):
 # Sequence of *windows*, unlike the 65-token training-loss tray in the next shot.
 # Only exact matches from the lookup appear amber (licence) or coral (benchmark).
 x0=116;step=13.7;y=740;marked=0
 for j in range(N):
  p=clip(checked-j)
  co=(O if j==HITS[0] else R if j==HITS[-1] else T)
  hh=21 if j in HITS and p else 9
  rect(g,x0+j*step,y-hh*.5,9.0,hh,co if p else E,op*(.90 if p else .20))
 if op:txt(g,f'{min(N,int(checked))} 窗已查',x0+N*step+20,y,22,M,op,'left')
def scan(g,c):
 t=c.t;name=c.at('连续十三个词');lab=c.at('13-gram');bench=c.at('GSM8K');all_=c.at('十三个词相连');idx=c.at('提前算出');bloom=c.at('布隆过滤器');advance=c.at('滑动窗口');hit=c.at('过滤器报了命中');verify=c.at('核对原片段');same=c.at('真的相同');measure=c.at('重合计数');finish=c.at('整篇文档')
 intro=phase(t,.0,.63);w=pstep(t,name-.15,.60);be=phase(t,bloom-.65,bloom+.12);x=phase(t,advance-.34,hit+.18);show=pstep(t,idx-.3,.62);check_=phase(t,verify-.23,verify+.45)
 silk(g,'13-gram',131,96,53,t-lab+.30,C,intro,'pen','left',.71)
 if t<lab-.19:txt(g,'在语料里查原题',136,96,48,F,intro*(1-phase(t,lab-.65,lab-.19)),'left')
 yy='一窗连续十三个词' if not be else '布隆过滤器：命中后仍要核对原文'
 alt=1-phase(t,bloom-.74,bloom-.34)if t<bloom-.32 else phase(t,bloom-.32,bloom+.22)
 if w:txt(g,yy,135,151,26,M,intro*w*alt,'left')
 txt(g,'公开材料拼接的工作样本',1465,106,23,M,intro,'right')
 # The index is built before the actual document sweep. Hold the real thirteen English words under the pen.
 if x<.001:
  at=BASES[6] if t>=bench else 0;u=phase(t,bench-.55,bench+.20)
  target=mix(0,BASES[6],u) if w else None
  if t>all_-.15 and t<idx-.15:target=BASES[6]+phase(t,all_-.08,all_+.85)
  target=(target if w else None)
 else:
  target=mix(0,BASES[6],x)
 if be and not x:target=mix(BASES[6],0,phase(t,bloom+.25,advance-.30))
 idx0=min(N-1,max(0,int(target if target is not None else 0)));group,bits_,has,hitname=observe(idx0)
 desk(g,target,intro,hit=(hitname if x>.999 and check_ else None))
 early=1-phase(t,idx-.53,idx-.12)
 if early:
  if w:comb(g,t,target or 0,intro*w*early)
  else:
   # A line passes through the workbench before the ruler has a name.
   v=pstep(t,.43,.74);xx,yy=836,632
   line(g,(176,yy),(1437,yy),E,1.5,intro*v)
   for j in range(13):
    vj=pstep(t,.49+j*.055,.55);rect(g,176+j*98,yy-10,21+7*(j*5%8),16,BLUE,intro*vj)

 if show:
  built=phase(t,idx-.1,bloom+.55);v=pstep(t,advance-.23,.55);tick=(x*(BASES[6]-3))%1
  filters(g,t,show,idx0,built,hitname,(1-tick)*v,be,count=(len(HITS)if t>measure+.25 else None))
  # The window is a query, not a scalar. Three distinct bit reads are made for this window.
  if be and not v and t>bloom-.1:
   for z,bb in enumerate(bits_):
    r=pstep(t,bloom-.08+.16*z,.46);xx,yy=bp(bb)
    if r:box(g,xx-3,yy-3,23.8,20.8,Y,r,sw=1.6)
  if v and 0<x<1:
   j=idx0;row=max(z for z,b in enumerate(BASES)if b<=j)
   for a,b in enumerate(bits_):
    xx,yy=bp(b);f=clip((tick-a*.09)/.74)
    if f>0:
     pts=[(772,242+row*39),(812,527),(xx+9,yy-4)]
     q=guide(g,pts,f,C,.78,1.8,.20)
  if check_ and t<measure+.08:
   s=pstep(t,same-.28,.50)
   txt(g,'样本  '+ ' '.join(ROWS[6][:3])+'…',1004,677,24,F,check_,'left',400)
   txt(g,'索引  '+ ' '.join(ROWS[6][:3])+'…',1004,717,24,Y,s,'left',400)
   if s>.01:check(g,1432,698,11,True,s)
 if show and v:
  # The lookup holds the matched question for the viewer; the scan continues to the last window.
  scanned=1+x*max(0,BASES[6])
  if x>=.999:scanned=BASES[6]+1+(N-BASES[6]-1)*phase(t,measure-.12,finish+.37)
  register(g,scanned,pstep(t,advance-.05,.54))
 if t>finish-.25:swish(g,1036,1225,665,t-finish+.15,Y,.65)
def loss_tray(g,start,local,wh,t,x0=180,y=603):
 # One cell per actual WORD POSITION in this worked example, not 65 native model tokens.
 for j in range(len(DOC)):
  x=x0+j*18.8;study=BASES[6]<=j<BASES[6]+13;keep=(1-start)*(1-(local if study else 0))
  cc=R if study and local else G if j<13 and wh else T
  hh=28*(.40+.60*keep);rect(g,x,y+28-hh,12.4,hh,cc,.25+.73*keep)
  if study and local:line(g,(x-1,y+29),(x+13,y+15),R,1.75,local)
 nf=round(sum((1-start)*(1-(local if BASES[6]<=z<BASES[6]+13 else 0))for z in range(len(DOC))))
 if start>.999 or local>.995:
  txt(g,f'{nf} / {len(DOC)} 词位参与损失（示意）',794,y+78,33,M,1)
@lru_cache(1)
def shared_licenses():
 rows=json.loads((W/'source/shared-mit-headers.json').read_text())
 assert all(tuple(r['excerpt'])==DOC[:13] for r in rows)
 return rows
def _license_threads(g,c,layout,restore):
 """One literal 13-word MIT phrase is printed by three actual open-source projects.
    Their licenses are evidence of boilerplate, not three contaminated programs."""
 from mounting import etch
 t=c.t;a=c.at;boil=a('许可证声明');wrong=a('容易误伤');same=a('代码开头');drop=a('扔掉它');valuable=a('有用的代码');white=a('白名单');test=a('重合的试题');separate=a('分开处理')
 x0=127;y0=173;s=.65
 fs,_=line_design(g,1265,RAW[0][1],26,ROWS[0]);right=LL[0]+g.measure(RAW[0][1],fs,font=MONO)
 anchor=(x0+s*(right-x0)+3,y0+s*(224-y0)-11)
 per=(1-phase(t,white-.35,white+.49))*phase(t,wrong+.45,wrong+.91)
 if layout>.005 and per:
  for i,row in enumerate(shared_licenses()):
   first=(wrong,same,boil-.38)[i];q=pstep(t,first-.11,.61);co=(C,VIO,T)[i];yy=186+90*i;x=1026+(i%2)*28;h=q*per*layout
   if h>.001:
    path(g,[anchor,(max(anchor[0]+7,944),anchor[1]),(x-44,yy),(x-16,yy)],q,co,2.3,h*.73)
    etch(g,row['repo'],x,yy-11,30,co,h);etch(g,'LICENSE',x+150,yy-10,19,M,h)
    for j,tok in enumerate(row['excerpt']):
     f=pstep(t,first-.01+j*.024,.29);v=1-phase(abs(j-12*phase(t,boil-.12,boil+.81)),.1,1.6)
     # Width depends on the actual word length; the little phrase below all three names is identical.
     width=8+len(tok)*1.75;xx=x+sum(12+len(v)*1.75 for v in row['excerpt'][:j])
     rect(g,xx,yy+22,width*f,8,blend(co,Y,v*phase(t,boil-.14,boil+.06)),h*f*.92)
  old=phase(t,drop-.12,drop+.39)*(1-phase(t,white-.57,white+.01))
  if old:
   n=BASES[6]-BASES[2];xx=977;yy=434
   etch(g,'若按文件头整篇删',xx,yy-3,25,M,old)
   for j in range(n):
    q=pstep(t,drop+.16+j*.050,.51);row,col=divmod(j,14);px=xx+col*22;py=yy+21+row*22
    rect(g,px,py+q*q*14,14,12,blend(T,R,q),old*(.99-.74*q))
   etch(g,f'另丢 {n} 个代码词位',xx+10,yy+95,27,O,old*pstep(t,valuable-.17,.63))
 if restore:
  for i,(src,yy,co,lab,tip) in enumerate(((0,240,T,'文件头','模板豁免'),(6,420,R,'试题片段','遮住这 13 词'))):
   edge=(white,test)[i];d=pstep(t,edge-.10,.72);k=restore*d
   if not k:continue
   x1=x0+s*(LL[src]-x0);sy=y0+s*(224+src*39-y0)
   path(g,[(x1+11,sy+17),(850,sy+17),(984,yy),(1050,yy)],d,co,2.1,k)
   dot(g,1050,yy,6.7,co,k);etch(g,lab,1073,yy-6,29,co,k)
   e=pstep(t,edge+.21,.59);etch(g,tip,1074,yy+44,26,F,k*e)
   if i==0 and t>a('文件头')-.13:swish(g,1071,1195,yy+64,t-a('文件头')+.12,T,.58)
   if i==1 and t>separate-.12:swish(g,1072,1269,yy+64,t-separate+.12,R,.58)

def unmask(g,c):
 t=c.t;clear=c.at('整篇都删');back=c.at('拿回来');loc=c.at('只跳过');loss=c.at('重合片段的损失');wrong=c.at('容易误伤');boil=c.at('许可证声明');valuable=c.at('有用的代码');white=c.at('白名单');test=c.at('重合的试题');separate=c.at('分开处理')
 a=1
 # At the cut the document, the matched thirteen words and its bit array are identical.
 # Only the old names recede; the source lines never crossfade or disappear by accident.
 h=phase(t,.0,.62)
 if h<1:
  txt(g,'13-gram',131,96,53,C,1-h,'left');txt(g,'布隆过滤器：命中后仍要核对原文',135,151,26,M,1-h,'left')
  txt(g,'公开材料拼接的工作样本',1465,106,23,M,1-h,'right')

 start=phase(t,clear-.17,clear+.83);rev=phase(t,back-.28,back+.60);erase=start*(1-rev);local=phase(t,loc-.17,loss+.38);wh=phase(t,white-.17,white+.64)
 silk(g,'命中以后',137,95,48,t-.40,F,a*h,align='left')
 txt(g,'同一份样本',1459,104,26,M,a*h,'right')
 # These are the same lines at the same coordinates. Erasing the code has a visible cost.
 layout=phase(t,wrong-.24,wrong+.72);ctx=g.c;ctx.save();ctx.rectangle(0,166,1600,377);ctx.clip()
 # Move the same words into the left half. The other halves of this comparison belong
 # to real LICENSE passages and to the cost of discarding the 28 unrelated code words.
 ctx.translate(127,173);xx=mix(1,.65,layout);ctx.scale(xx,xx);ctx.translate(-127,-173)
 desk(g,BASES[6] if erase<.025 and not local else None,a,erase=erase,wl=wh,mask=local,hit='题面',status=local)
 if layout:
  y=224+2*39;x=LL[2]-10;opacity=phase(t,c.at('扔掉它')-.11,c.at('扔掉它')+.39)*(1-phase(t,white-.29,white+.48))
  if opacity:
   path(g,[(x+8,y-13),(x,y-13),(x,y+3*39+13),(x+8,y+3*39+13)],opacity,O,2.8,opacity)
 ctx.restore()
 if layout:_license_threads(g,c,layout,wh)
 if 0<erase<1:
  y=210+306*erase;line(g,(177,y),(1435,y),R,2.4,a*math.sin(math.pi*erase))
 if erase>.87:
  txt(g,'训练样本已移除',800,392,46,R,phase(erase,.87,1))
 last=1-phase(t,clear-.41,clear-.12)
 if last:
  filters(g,t,last,BASES[6],1,count=len(HITS));register(g,N,last)
 tray=phase(t,clear-.12,clear+.12)
 if tray and local<.999:
  # The retained count and restoring document share the very same progress.
  loss_tray(g,erase,local,wh,t)
 if local:
  if local>=.999:loss_tray(g,0,local,wh,t)
  # A brace closes on exactly the 13 character-normalised WORD POSITIONS in the dataset fragment.
  lo=180+BASES[6]*18.8;hi=lo+13*18.8-5;op=phase(t,loc-.12,loc+.47)
  path(g,[(lo,586),(lo,575),(hi,575),(hi,586)],op,R,2.1,op)
  if wh:
   xx=180+6*18.8;line(g,(180,581),(180+13*18.8-6,581),G,2.4,wh)
   txt(g,'通用文件头豁免',xx+17,550,26,G,wh)
  if t>valuable-.12:
   bx=180+BASES[2]*18.8;tx=180+BASES[6]*18.8-8
   swish(g,bx,tx,642,t-valuable+.10,T,.64)
HIST=json.load((OLD/'data/livecode-history.json').open())
from datetime import date
def dx(s):
 a=date.fromisoformat(s[:10]if len(s)>7 else s+'-28');return 156+1273*(a-date(2023,5,1)).days/(date(2025,4,30)-date(2023,5,1)).days
def newtests(g,c):
 t=c.t;train=c.at('训练结束以后');name=c.at('LiveCodeBench');dates=c.at('竞赛日期');aug=c.at('八月出的');jan=c.at('隔年一月');cut=c.at('九月底停止');pick=c.at('右边这题');secret=c.at('机构内部');hold=c.at('最终校验');audit=c.at('专家二次审计');refine=c.at('高可信度')
 fir=1-phase(t,secret-.51,secret+.28);dx0=dx(HIST['example_cutoff'])
 if fir:
  op=fir;silk(g,'按日期把新题留出来',131,92,46,t-.12,F,op*(1-phase(t,name-.46,name-.13)),align='left')
  silk(g,'LiveCodeBench',132,92,51,t-name+.14,C,op,'pen','left')
  if t>name-.1:silk(g,'按竞赛发布日期滚动更新的编程测试',133,148,25,t-name-.20,M,op,align='left')
  y=548;line(g,(156,y),(1435,y),M,1.7,op)
  for j,(v,ds,n)in enumerate(HIST['releases']):
   xx=dx(ds);a=pstep(t,.6+j*.17,.54);h=203*n/1055
   rect(g,xx-15,y-h*a,31,h*a,BLUE,op*a*.86);txt(g,v,xx,y+33,23,M,op*a)
   if j in(0,5):txt(g,str(n),xx,y-h*a-25,28,C,op*a)
  if t<aug-.18:txt(g,'累计收题数',198,479,28,C,op*phase(t,.44,1.11),'left')
  f=phase(t,cut-.40,cut+.36);same=pstep(t,dates-.34,.62)
  for i,(d,ev,co)in enumerate(zip(HIST['contest_examples'],(aug,jan),(O,T))):
   xx=dx(d['day']);a=pstep(t,ev-.21,.58);yy=282-77*i
   if a:
    dot(g,xx,y,8,co,op*a);line(g,(xx,y-5),(xx,yy+40),co,2,op*a);txt(g,d['day'],xx,yy,26,co,op*a)
    txt(g,d['title'],xx,yy-43,27,F,op*a)
  if f:
   rect(g,dx0,326,1435-dx0,222,inkcol(T,.16),op*f*.68);line(g,(dx0,319),(dx0,591),Y,2.8,op*f)
   txt(g,'示例训练截止：2024-09-30',dx0,682,30,Y,op*f);swish(g,dx0+75,dx0+237,611,t-pick+.14,T,.56)
 if fir<1:
  op=1-fir;split=pstep(t,secret-.23,.61);silk(g,'两种复核，守的是两件事',131,99,45,t-secret+.22,F,op,align='left')
  yy=453;x1,x2=372,1116
  # One is about access; the other about the quality of an existing question.
  nh=phase(t,hold-.29,hold+.40)
  for j in range(11):
   xx=x1-133+26*j
   h=28+19*((j*17)%7);rect(g,xx,yy-h/2,15,h,inkcol(C,.81),split)
  a=phase(t,secret-.15,hold+.2)
  for sign in (-1,1):
   xx=x1+sign*(183-37*a);path(g,[(xx-sign*19,yy-96),(xx,yy-96),(xx,yy+96),(xx-sign*19,yy+96)],a,C,3,op)
  txt(g,'留作私测',x1,649,34,C,op*nh)
  rr=pstep(t,audit-.23,.58)
  if rr:
   for j in range(5):
    y=349+j*49;txt(g,('题干','选项','正确答案','评分标准','复核记录')[j],x2-90,y,25,F,op*rr,'left');a=pstep(t,audit-.07+j*.15,.49)
    if j in(1,3):line(g,(x2+52,y+6),(x2+124*a,y-6),R,2,op*a)
    else:check(g,x2+98,y,7.8,True,op*a)
   silk(g,'专家复核',x2,649,34,t-refine+.50,T,op)
