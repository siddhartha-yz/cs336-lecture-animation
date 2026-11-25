"""Actual Paloma slices: the rank reversal is carried into the equal-domain readout."""
from termnotes import hint
from ink import *
from motion import *
from pathlib import Path
P=json.loads((Path(__file__).parent/'art2/data/paloma-slices.json').read_text())
def table(g,c,board):
 from tradeoff import answer_stage
 t=c.t;pal=c.at('Paloma');look=c.at('看这两列');py=c.at('读代码');ma=c.at('数学文章');sep=c.at('各占一列');pool=c.at('合在一起');logs=c.at('对数困惑度');right=c.at('看右边');back=c.at('回头看代码')
 old=1-phase(t,.12,.60);hinge=phase(t,.23,1.40)
 if old:curtain(g,old,lambda:answer_stage(g).draw())
 if t>board+.8:return
 exit=phase(t,board-.56,board-.16);line_exit=phase(t,board-.20,board+.64);alpha=1-exit
 for j,col in enumerate((C,V)):
  aa=phase(t,.34+j*.08,1.1+j*.08)*(1-line_exit)
  y=mix(395,370+j*99,hinge);line(g,(mix(288,375,hinge),y),(mix(1290,1220,hinge),y),col,1.25,.58*aa)
 # The last wrong choice is just one term in a sentence average. The SAME marks then
 # collect into articles and separate into two subject columns. No new measurements are invented.
 if t<look+.30:
  accent=c.at('答错的那一步');several=c.at('几种文章');hidden=c.at('也会藏住偏科')
  alpha0=phase(t,.22,.90)*(1-phase(t,look-.46,look+.30))
  fold=phase(t,several-.14,several+1.12);unstack=phase(t,hidden-.3,look-.30)
  tokens=('Choose','one',':','nine','minus','seven','is','either','two','or','three','.','Answer',':','two')
  for j,token in enumerate(tokens):
   x0=245+j*78.7;y0=434
   cl=Y if j==14 else M
   bx,by=transit((x0,y0),(611+(j%5)*90,351+(j//5)*67),fold,24+4*(j%3))
   xx,yy=transit((bx,by),((630 if j<8 else 1022)+(j%3-1)*35,347+(j%5)*31),unstack,19)
   ww=mix(68,25,fold);hh=mix(52,10,fold)
   box(g,xx-ww/2,yy-hh/2,ww,hh,cl,alpha0,fill=inkcol(cl,.10),sw=1.65)
   if fold<.58:txt(g,token,xx,yy,21,cl,alpha0*(1-phase(fold,.02,.55)),width=ww-6)
   if j==14:
    flag=phase(t,accent-.22,accent+.44)*(1-fold)
    if flag:
     check(g,xx,yy+56,8,False,alpha0*flag)
     txt(g,'基座选错',xx,yy+100,22,R,alpha0*flag)
  for j,(lab,tx,col) in enumerate((('代码',630,C),('数学',1022,V))):
   txt(g,lab,tx,274,30,col,alpha0*unstack*(1-phase(t,look-.55,look-.16)))
 small=phase(t,look-.4,look+.61);expand=phase(t,sep-.66,sep+1.30)
 title(g,'Paloma',105,phase(t,pal-.12,pal+.40)*alpha,sub=hint('Paloma'))
 if t<pal-.16:txt(g,'在代码里领先，换成数学呢？',800,114,40,F,small*(1-phase(t,pal-.74,pal-.17)))
 xx=(401,545,689,833,977,1121);ys=(359,462);labels=('Python','数学','arXiv','WikiText','网页','图书')
 wait=phase(t,look-.33,look+.62)
 for j,(nm,y,col) in enumerate(zip(P['models'],ys,(C,V))):
  txt(g,nm,mix(413,280,expand),y,35,col,wait*alpha,'right')
 for i,dom in enumerate(P['domains']):
  if i<2:
   xx0=[628,1023][i];x=mix(xx0,xx[i],expand);vis=wait
   wid=mix(230,136,expand)
  else:
   vis=phase(t,sep+.65+(i-2)*.14,sep+1.23+(i-2)*.14);x=xx[i];wid=136
  if not vis:continue
  x=mix(x,1324,line_exit);width=wid*(1-line_exit)
  txt(g,labels[i],x,268,29,F,vis*alpha)
  vals=dom['values'];cue=py if i==0 else ma if i==1 else sep+.4+i*.12
  r=phase(t,cue-.12,cue+.68)
  attention=sin(pi*r) if 0<r<1 else 0
  lookback=phase(t,back-.21,back+.45)*(1-phase(t,board-.96,board-.36))
  returning=lookback if i==0 else 0
  for j,y in enumerate(ys):
   low=vals[j]<vals[1-j];col=T if low else R;v=vis*alpha*(1-(.46 if i else 0)*lookback)
   box(g,x-width/2,y-39,width,77,E,vis*(1-line_exit),fill=inkcol(col,(.075 if not low else .24)*(.75+.25*v)),sw=1.25)
   txt(g,f'{vals[j]:.2f}',x,y,39,F,v)
   if low:
    line(g,(x-width*.24,y+25),(x+width*.24,y+25),col,2.7,min(1,.46+.54*attention+.58*returning)*v)
    if returning>.01:emphasize(g,x,y,width-5,71,phase(t,back-.13,back+.97),Y)
    elif attention and r<1:emphasize(g,x,y,width-5,71,r,col)
 agg=phase(t,pool-.10,pool+.72);final=phase(t,logs-.19,logs+.87);xs=1350
 if agg:
  for j,(y,col) in enumerate(zip(ys,(C,V))):
   for i,x in enumerate(xx):
    q=phase(t,pool+.08+i*.12,pool+.98+i*.12)
    points=[transit((x,y+31),(xs-61,y+2),k/40,(-31 if j==0 else 40)*(1-i*.11)) for k in range(41)]
    if 0<q<1:guide(g,points,q,col,alpha*.95,2.4,.2)
   box(g,xs-75,y-39,150,77,col,agg*(1-line_exit),fill=inkcol(col,.10),sw=1.4)
   txt(g,f"{P['aggregate']['values'][j]:.2f}",xs,y,42,col,final*alpha)
   if j==1:
    win=phase(t,right-.17,right+.65)
    line(g,(xs-36,y+26),(xs-36+72*win,y+26),T,2.7,win*alpha)
  txt(g,'六域等权 PPL',xs,268,28,Y,agg*alpha)
  formula(g,'domain_mean',xs,552,211,final*alpha)
  txt(g,hint('六域等权 PPL'),800,667,27,M,final*alpha)
  if right< t <right+1.15:
   guide(g,[(1246,310),(1246,508),(1424,508)],phase(t,right,right+1.15),Y,alpha,2.5,.42)
 else:
  txt(g,'同一列，低者更好',800,649,26,M,small*alpha)
 source(g,'xLSTM 论文表 8、10 · 仅这六列等权重算',phase(t,pal,pal+.7)*alpha)
