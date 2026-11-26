"""Expose the measured loss of each original token on its own interval; then reuse the same 45-byte denominator."""
from ink import *
from mounting import etch
from timeline3 import OLD
D=json.loads((OLD/'art2/data/tokenizers.json').read_text())
def compare(g,c):
 t=c.t;a=c.at;real=a('模型实测的概率');gap=a('两个结果');why=a('预测本身');cut=a('早期语言模型基准')
 see=phase(t,real-.20,real+.64)*(1-phase(t,cut-.50,cut+.06))
 if see:
  bx=310;unit=(1218-bx)/45
  for j,(m,base,co) in enumerate(zip(D['models'],(333,435),(C,Y))):
   for i,(lo,hi,val)in enumerate(zip(m['boundaries'],m['boundaries'][1:],m['bits'])):
    q=phase(t,real-.18+j*.18+i*.073,real+.30+j*.18+i*.073)
    w=unit*(hi-lo);xx=bx+unit*lo;hh=val*2.50*q
    rect(g,xx+2,base-hh,w-4,hh,co,see*q*.83)
   if j==0:etch(g,'实测损失 / bit',bx-22,base-38,24,C,see,'right')
  if gap-.10<t<cut:
   q=phase(t,gap-.08,why+.85)
   # An actual byte boundary differs inside naïve; trace it down to the shared ruler.
   x=bx+32*unit
   path(g,[(x,476),(x,510),(x,564)],q,T,2.2,see)
   if 0<q<1:dot(g,x,mix(476,564,q),5,T,see)
 zero=a('零样本困惑度');transfer=a('再直接到');gate=phase(t,transfer-.44,transfer+.20)*(1-phase(t,zero+.83,zero+1.43))
 if gate:
  for j,xx in enumerate((331,800,1269)):
   p=phase(t,transfer-.23+j*.23,zero+.31+j*.23)
   if 0<p<1:dot(g,xx,mix(227,345,p),8,Y,gate*sin(pi*p)**.50)
