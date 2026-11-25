from termnotes import hint
from ink import *
from cut_common import stage
from importlib import import_module
NAMES={3:('exams','saturation mmlu_pro gpqa hle'),4:('judges','arena rating bias length'),5:('machines','repo docker scaffolds abstract'),6:('reason','arcgrid search behavior transfer'),7:('validity','realwork shuffle ngrams masks rolling'),8:('finale','orbit return_home')}
def draw(g,id,c):
 b,n=map(int,id.split('-'));mod,names=NAMES[b];getattr(import_module(mod),names.split()[n-1])(g,c)
def carry(g,id,t):
 """Carry the identities of the actual objects between chapters, not just their colours."""
 if id not in ('4-1','6-1') or t>=2.20:return False
 p=phase(t,0,2.20);op1=1-phase(t,0,.70);op2=phase(t,.84,2.10)
 stage(g)
 if id=='4-1':
  # Last shot of HLE: three tasks. Fold the first two documents into the anonymised pair.
  txt(g,'一个答案，还是一份作品？',800,182-13*p,46,F,op1)
  txt(g,'字符串匹配',800,703,28,M,op1*.40)
  title(g,'Chatbot Arena',104,op2,sub='一张选票，约束一对模型')
  for j,(x0,y0,col) in enumerate(((375,375,C),(800,340,V),(1225,375,O))):
   lab=('清洗脚本','商务邮件','食谱')[j]
   if j==2:
    q=phase(t,.1,1.05);x=x0+173*q;y=y0+.10*173*q
    docs(g,x-100,y,200,190,col,1-q,6,j);txt(g,lab,x,y+242,32,col,op1);continue
   x,y=curve((x0,y0),((570,1025)[j],337),p,34 if j==0 else 22)
   sw=mix(200,265,p);h=mix(190,178,p)
   docs(g,x-sw/2,y,sw,h,col,1,0)
   for m in range(6):
    oldfrac=.39+.37*((11*m+3*j)%13)/12
    newfrac=.39+.36*((m*11+j*3)%13)/12
    grow=phase(t,1.1+j*.65,20+j*.3)
    newq=phase(grow,.115*m,.53+.115*m) if m<5 else 0
    length=sw*mix(oldfrac,newfrac*newq,p)
    yy=y+h*mix(.21+m*.124,.20+m*.145,p);lx=x-sw*.375
    if length>.1:line(g,(lx,yy),(lx+length,yy),col,2.7,.55+.15*p)
   txt(g,lab,x,y+242,32,col,op1);txt(g,'回答 '+('A','B')[j],x,y-37,32,col,op2)
 else:
  from machines import grid,ARC
  title(g,'修过旧仓库，就会解新题吗？',125,op1,sub='把熟悉的题材拿走，只留下可观察的变换')
  title(g,'ARC-AGI',110,op2,sub=hint('ARC-AGI'))
  ar=ARC['train'][0]
  for j,field in enumerate(('input','output')):
   xx,yy=curve(((515,1132)[j],443),((262,435)[j],350),p,(-1)**j*46)
   grid(g,ar[field],xx,yy,mix(227,121,p),1,mix((.85,1)[j],1,p))
   txt(g,('输入','输出')[j],(515,1132)[j],637,30,(C,Y)[j],op1)
  arrow(g,(mix(663,335,p),mix(439,350,p)),(mix(911,357,p),mix(439,350,p)),1,Y,1,mix(2.4,1.7,p))
  txt(g,'1',345,446,24,M,op2)
  for j in (1,2):
   pair=ARC['train'][j];xx=345+j*453;q=phase(t,.45+j*.75,2.4+j*.75)
   if q:
    grid(g,pair['input'],xx-83,350,121,q);grid(g,pair['output'],xx+90,350,121,phase(t,2+j*.8,4+j*.8))
    arrow(g,(xx-10,350),(xx+12,350),q,Y,1,1.7);txt(g,str(j+1),xx,446,24,M,q)
  source(g,'ARC-AGI-1 · 公开训练题 67a3c6ac · 原始网格',op2)
 return True
