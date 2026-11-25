from ink import *
from motion import transit
from studio_examples import pstep,area,VIO,BLUE
from studio_tests import AR,arcboard,PAL,tile
from mounting import etch
from studio_science import polycurve
from timeline3 import OLD
import json
REC=json.loads((OLD/'data/arc-o3-preview-2024.json').read_text())
TRANSFORMS=(lambda m:[r[:]for r in m],lambda m:[r[::-1]for r in m],lambda m:m[::-1],lambda m:[list(r)for r in zip(*m[::-1])])
def comparisons(mat,truth):return sum(x!=y for r,h in zip(mat,truth)for x,y in zip(r,h))
CHECK=[[comparisons(f(q['input']),q['output'])for q in AR['train']]for f in TRANSFORMS]
def compute(g,c):
 t=c.t;a=c.at;hardware=a('光加预训练');cost=a('真正开始');name=a('测试时计算');puz=a('模型拿到新网格');try_=a('假设搜索');prog=a('候选变换');sample=a('三五个示例');prune=a('剪枝');select=a('吻合规则');settle=a('推理评测')
 target=AR['test'][0]
 # The last gold tile of the public question gives way to the *separate* December measurement.
 move=phase(t,.03,.97);record=phase(t,.77,1.55);cut=phase(t,puz+.25,puz+1.27)
 if t<1.28:
  from studio_tests import arc
  from timeline3 import clock,S
  ctx=g.c;ctx.save();ctx.translate(-362*move,-84*move);ctx.scale(1+.24*move,1+.24*move);ctx.push_group()
  arc(g,clock('6-1').clk(S['6-1']['duration']-1/60));ctx.pop_group_to_source();ctx.paint_with_alpha(1-phase(t,.36,1.1));ctx.restore()
 if 1.1<t<cost+.30:
  # A train of coloured examples feeds a fixed matrix; the measured sampling planes enter as
  # that matrix tips away. These are not extra data points on the December trial.
  alpha=phase(t,.85,1.55)*(1-phase(t,cost-.62,cost+.22));zz=phase(t,hardware-.18,hardware+.67)
  for j in range(9):
   xx=237+(j%3)*51;yy=246+(j//3)*44
   rect(g,xx,yy,41,32,inkcol(C,.40+.40*((j*17)%7)/7),alpha)
  for j in range(7):
   u=(.092*t+j*.144)%1;xx=38+169*u;yy=293+(j%3-1)*22
   path(g,[(xx-26,yy),(xx+5,yy)],1,(T,C,O)[j%3],3.2,alpha*u)
  etch(g,'训练数据',75,370,25,T,alpha)
  etch(g,'参数 θ',292,205,29,C,alpha,'center')
 if record and cut<1:
  op=record*(1-cut);m=pstep(t,cost-.25,1.08);n=phase(t,cost+.13,cost+1.6)
  # Exactly the published six and 1024 samples, each with the same 9.2 unit square.
  # Perspective is an affine change of plane applied to every cell equally, not to their values.
  lead=phase(t,hardware-.35,hardware+.54);xx,yy=343,390;pitch=12.75
  z=g.c;z.save();z.translate(xx,yy);z.transform(type(z.get_matrix())(1,-.19,.38,.78,0,0));colors=('#176E8A','#259ABA','#4EBBD3',C)
  for row in range(32):
   for col in range(32):
    j=row*32+col
    if j<6:continue
    u=clip((m-(row+col)*.009)/.44)
    if u>.001:rect(g,pitch*col,pitch*row,9.3,9.3,colors[(2*row+col)%4],op*u)
  for h in range(6):rect(g,h*pitch,0,9.3,9.3,O,op)
  z.restore()
  etch(g,'6 次采样',xx-28,yy-32,31,O,op,'right');line(g,(xx-21,yy-24),(xx+14,yy-3),O,1.8,op)
  if m>.1:etch(g,'1,024 次采样',718,696,35,C,op*m,'center')
  # An enrolled sample can never be mistaken for a solved grid.
  x0=1032;y0=611;xh=1125
  path(g,[(1003,244),(1003,y0),(1492,y0)],1,E,1.8,op);etch(g,'o3 预览版 · 2024.12',1031,201,31,F,op)
  etch(g,'ARC-AGI-1 半私有评测 · 同一组 100 题',1031,249,24,M,op)
  for j,(cfg,h,xv,col)in enumerate(zip(REC['configurations'],(lead,n),(1130,1357),(O,C))):
   zz=cfg['score_percent'];height=zz*2.92
   if h:rect(g,xv-31,y0-height*h,62,height*h,inkcol(col,.85),h*op);etch(g,f'{zz:g}%',xv,y0-height*h-38,38,col,h*op,'center');etch(g,('6','1,024')[j],xv,y0+44,28,col,op*h,'center')
  if n:etch(g,'每题的采样数',1278,699,23,M,n*op,'center')
 if cut:
  op=cut;emit=phase(t,try_-.51,try_+.91);world=phase(t,prog-.35,prog+.79);close=phase(t,select-.20,select+.89)
  inp=target['input'];out=target['output'];cx=mix(560,333,emit);cy=mix(425,429,emit);sz=mix(353,251,emit)
  arcboard(g,inp,cx,cy,sz,op);etch(g,'67a3c6ac · 新输入',cx,cy+sz*.53+29,25,M,op,'center')
  if not emit>=1:
   etch(g,'候选规则演算',cx+sz*.68,cy-37,33,T,(1-emit)*op)
   etch(g,'把猜想拿回三个例子去验',cx+sz*.68,cy+15,25,M,(1-emit)*op)
  # Fan out one concrete input. Each row is an executable geometric transformation of that input.
  coords=[(889,165),(1166,319),(1132,554),(868,674)];names=('不动','左右翻','上下翻','转 90°')
  for j,(xe,ye)in enumerate(coords):
   h=pstep(t,try_-.25+j*.13,.65);v=pstep(t,prog-.18+j*.105,.47);reject=phase(t,prune-.19+j*.13,prune+.48+j*.13);surv=j==1
   aop=op*h*(1-(0 if surv else .94)*reject)*(1-close if not surv else 1)
   if aop<.002:continue
   to=((155 if surv else xe),(210 if surv else ye))
   xx=mix(xe,1094,close)if surv else xe;yy=mix(ye,422,close)if surv else ye
   col=(M,T,VIO,O)[j];x1=cx+sz*.5
   pts=((x1+14,cy),(x1+141,cy),(xx-199,yy),(xx-72,yy));tip=polycurve(g,pts,col,2.8,aop,h)
   if h<.99:dot(g,*tip,5,F,aop)
   size=mix(99,277,close)if surv else 99
   arcboard(g,TRANSFORMS[j](inp),xx,yy,size,aop);etch(g,names[j],xx+size*.58,yy-13,26,col,aop)
   for k,num in enumerate(CHECK[j]):
    ck=pstep(t,sample-.24+k*.28+j*.054,.51)*(1-close)
    if ck:check(g,xx+size*.59+31*k,yy+27,7,num==0,aop*ck)
  if close:
   etch(g,'三个训练例全部吻合',1100,641,27,T,op*close,'center')
   # Re-enact a row of the winning transformation, under the word 想 rather than retelling it.
   unit=phase(t,settle+.18,settle+2.05)
   if .001<unit<.999:
    for j,col in enumerate(inp[0]):
     pp=(cx-sz/2+(j+.5)*sz/3,cy-sz*.3333);qq=(1094-277/2+(2.5-j)*277/3,422-277*.3333)
     xx,yy=transit(pp,qq,unit,104-21*j);tile(g,xx-19,yy-19,38,PAL[col],op*sin(pi*unit))
