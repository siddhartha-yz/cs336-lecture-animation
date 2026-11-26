"""Two real byte segmentations and a two-step geometric mean, each with a physical denominator."""
from termnotes import hint
from ink import *
from motion import *
from pathlib import Path
DATA=json.loads((Path(__file__).parent/'art2'/'data'/'tokenizers.json').read_text())
def five_twenty(g,z=1,labels=1,equ=1,op=1,clock=0.):
 # Each group is a *different time step*; every group carries unit probability mass.
 for j,(x,c,N,h,label) in enumerate(((470,C,5,146,'第一步'),(1125,T,20,36.5,'下一步'))):
  a=op; span=490;left=x-span*.5; base=435.;dx=span/N
  txt(g,label,x,210,32,F,a*labels);line(g,(left-12,base),(left+span+12,base),M,1.8,a)
  for i in range(N):
   k=phase(z,i*.23/N,.72+i*.23/N)
   xx=left+dx*(i+.5);ww=min(50,dx*.68)
   rect(g,xx-ww/2,base-h*k,ww,h*k,Y if i==(2,8)[j] else c,a*(1 if i==(2,8)[j] else .82))
   if 0<k<1:line(g,(xx-ww/2,base-h*k),(xx+ww/2,base-h*k),F,2,a*sin(pi*k))
  txt(g,f'1 / {N}',x,494,39,c,a*labels)
 if equ>0:
  formula(g,'geometric',800,626,335,op*equ)
  txt(g,'两步各占一半权重',800,706,25,M,op*equ)
def choice_variation(g,t,d,var):
 from opening2 import choice_stage
 c=g.clock; start=c.at('实际的候选数');five=c.at('这一步五选一');twenty=c.at('下一步二十选一');both=c.at('两步合起来')
 q=phase(t,start-.17,start+.90)
 if q<1:curtain(g,1-phase(q,0,.55),lambda:choice_stage(g,trace=-10).draw())
 if q:
  z=phase(t,five-.42,max(twenty+.8,five+1.55));equ=phase(t,both-.09,both+.50)
  five_twenty(g,z=z,labels=phase(q,.20,.90),equ=equ,op=q)
def tokenizer(g,c):
 from opening2 import transfer_stage
 t=c.t;tw=c.at('两套分词器');blue=c.at('蓝色切了九块');gold=c.at('黄色切了十一块');loss=c.at('总损失一样');spread=c.at('摊给更多词元');bpb=c.at('换个分母');bytes_=c.at('UTF-8 字节数');actual=c.at('模型实测的概率');history=c.at('早期语言模型基准');gt=c.at('GPT-2');zero=c.at('零样本困惑度')
 if t<1.5:
  q=phase(t,.20,1.38);old=1-phase(t,.03,.42)
  if old:five_twenty(g,labels=old,equ=old,op=old)
  # Carry both *measuring lines*, not the choices or their numerical values.
  for j,(oldx,newy,col) in enumerate(((470,362,C),(1125,463,Y))):
   x0,y0=transit((oldx-245,435),(312,newy),q,[-22,26][j]);x1,y1=transit((oldx+245,435),(1225,newy),q,[-22,26][j])
   line(g,(x0,y0),(x1,y1),col,1.55,phase(t,.13,.47)*(1-phase(t,1.1,1.5)))
 a=phase(t,.65,1.35);leave=phase(t,history-.40,history+1.45);oldtxt=1-phase(t,history-.45,history+.02)
 if a and leave<1:
  cl=a*oldtxt;ll=a*(1-leave)
  title(g,'同一句话，两把分词刀',103,cl,sub='切的是边界，比较的是预测')
  # Render one naturally kerned sentence. The reading mark has its own lane, below the ink.
  txt(g,DATA['text'].strip(),800,224,45,F,cl,font=SERIF)
  pr=phase(t,.8,blue+.30);xx=mix(335,1270,pr)
  if 0<pr<1:
   line(g,(335,267),(xx,267),C,1.5,cl*.62);dot(g,xx,267,3.8,C,cl)
  rail=(310,1218);x0,x1=rail;unit=(x1-x0)/DATA['bytes']; br=phase(t,bpb-.15,bpb+.78);ex=phase(t,bytes_-.20,bytes_+1.02);real=phase(t,actual-.18,actual+.72)
  equal=phase(t,loss-.22,loss+.72);spl=phase(t,spread-.25,spread+.90)
  for j,(m,yy,col,tag,begin) in enumerate(zip(DATA['models'],(362,463),(C,Y),('GPT-2','SmolLM2'),(blue,gold))):
   k=phase(t,tw-.26+j*.45,tw+.75+j*.45);edges=m['boundaries'];n=len(edges)-1
   txt(g,tag,x0-31,yy,28,col,k*cl,'right')
   line(g,(x0,yy+19),(x1,yy+19),col,1.6,ll*k)
   for i,(u,v,raw) in enumerate(zip(edges,edges[1:],m['raw_tokens'])):
    p=phase(t,begin-.35+i*.052,begin+.38+i*.052);l=x0+unit*u;r=x0+unit*v
    if p:
     h=39*settle(p);b=1 if i in ((0,6) if j==0 else (0,1,7,8)) else .73
     box(g,l+.7,yy+19-h,max(2,r-l-1.4),h,col,ll*p*b,fill=inkcol(col,.102),sw=1.45)
     label=raw.strip() or '␠';txt(g,label,(l+r)/2,yy,22,col,cl*p, width=max(6,r-l-5))
   txt(g,f'{n} 个词元',1246,yy,27,col,cl*phase(t,begin,begin+.68),'left')
   if 0<spl<1 and j==1:guide(g,[(x0,yy+23),(x1,yy+23)],spl,Y,cl,3,.24)
  if equal and cl:
   h_y=(591,647);draw=equal*(1-br)
   if draw>.001:
    txt(g,'示例：同为 89 bit',284,619,26,F,cl*equal*reletter(br)[0],'right')
    smaller=c.at('每个词元分到的就少了');down=c.at('算出的困惑度自然更低')
    for j,(m,y,col) in enumerate(zip(DATA['models'],h_y,(C,Y))):
     n=len(m['raw_tokens']);sx=313;sw=565
     # Same length equals same 89 bits. Separate the segments slightly so their
     # width, NOT the number printed after them, first reveals the new denominator.
     opening=phase(t,spread-.19+j*.18,smaller+.32+j*.14)
     for k in range(n):
      q=phase(opening,.08*k/n,.83+.13*k/n)
      left=sx+sw*k/n;right=sx+sw*(k+1)/n
      shift=(k-(n-1)*.5)*3.4*q
      rect(g,left+shift,y-5,(right-left)*equal,10,col,draw*cl)
      if k:line(g,(left+shift,y-9),(left+shift,y+9),BLACK,2.55,cl*q*draw)
     # Compare ONE actual share from each equal-total strip on the same vertical datum.
     compare=phase(t,smaller-.12,smaller+.9)
     if compare:
      orig=(sx+sw*(n-.5)/n+(n-1)*1.7,y)
      target=(947+sw/2/n,y)
      cx,cy=transit(orig,target,compare,(-1 if j else 1)*14)
      span=sw/n
      line(g,(cx-span/2,cy),(cx+span/2,cy),col,6.5,draw*cl*compare)
      line(g,(947,y-12),(947,y+12),F,1.25,draw*cl*compare)
     showval=phase(t,down-.18+j*.19,down+.50+j*.19)
     if showval:txt(g,f'{89/n:.2f} bit  →  PPL {2**(89/n):.1f}',1063,y,26,col,showval*cl*(1-br),'left')
   if br:
    # Keep the numerator visible as the spoken unit changes underneath it.
    # The acronym first appears as the definition is spoken, not five seconds early.
    num=phase(t,c.at('用总比特数')-.23,c.at('用总比特数')+.45)
    term=phase(t,c.at('每字节比特数')-.14,c.at('每字节比特数')+.54)
    if num:
     nvis=cl*num*(1-phase(t,c.at('两行都是')-.40,c.at('两行都是')+.11))
     txt(g,'89 bit',254,541,27,Y,nvis,'right')
     x=243;# The numerator remains a count of bits; link it to the common byte ruler.
     if nvis and ex:guide(g,[(x,554),(x,566),(309,566)],phase(t,bytes_-.16,bytes_+.88),Y,nvis,1.75,.50)
    txt(g,'BPB',255,607,43,T,term*cl,'right');txt(g,hint('BPB'),800,713,27,M,term*cl)
    for i in range(DATA['bytes']):
     p=phase(ex,.25*i/45,.65+.25*i/45);l=x0+i*unit
     if p:box(g,l+1.1,570+10*(1-p),unit-2.2,30*p,C,cl*.85,fill=inkcol(C,.08),sw=1.2)
    txt(g,'45 字节（含开头空格）',x0,641,25,M,ex*cl,'left')
    # UTF-8 has two bytes here even though the sentence has one printed ï.
    ub=DATA['text'].encode('utf-8');v=ub.index('ï'.encode('utf-8'))
    if ex>.5:
     l=x0+v*unit;r=l+2*unit
     line(g,(l,605),(r,605),Y,2.5,cl*ex);txt(g,'ï  ·  C3 AF',(l+r)*.5,551,20,Y,cl*ex)
    # Both tokenizers are mapped to one physical byte ruler (including the initial space).
    together=phase(t,c.at('两行都是')-.13,c.at('四十五个字节')+.74)
    if 0<together<1:
     for j,(yy,co) in enumerate(((362,C),(463,Y))):
      edge=x0+unit*DATA['bytes']*together
      line(g,(edge,yy+24),(edge,568),co,1.25,cl*.66*sin(pi*together))
     dot(g,edge,568,4.6,Y,cl*sin(pi*together))
    for j,(m,col) in enumerate(zip(DATA['models'],(C,Y))):
     val=mix(89/45,m['bpb'],real);x=905+j*289
     txt(g,f'{val:.3f}',x,640,40,col,ex*cl)
     txt(g,('GPT-2','SmolLM2')[j],x,686,21,M,ex*cl)
    if 0<real<1:guide(g,[(839,663),(1256,663)],real,T,cl,2.7,.26)
    txt(g,'模型实测' if real>.54 else '等损失示例',1418,578,23,T if real>.54 else M,ex*cl,'right')
 if leave:
  # A single training stream fans out to three held-out corpora. Use the published GPT-2 scores.
  q0=phase(t,history+.3,history+1.7);q1=phase(t,gt-.08,gt+2.15)
  if q0:
   w=transfer_stage(g,q0,1,q1,focus=mix(-1,3,phase(t,zero-.3,zero+2.8)),walk=mix(-1,3.8,phase(t,history+.8,gt-.1)));w.draw()
