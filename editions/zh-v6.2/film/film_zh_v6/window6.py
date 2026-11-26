"""The 13-word aperture has a real moving boundary even when it folds around a line break."""
from rig4 import *
from studio_corpus import DOC,observe,bits

@lru_cache(4)
def pass_clock(c):
 a=c.at('亮窗每走一格');b=c.at('布隆过滤器')-.26
 return FlowClock([a-.20,b+.24],[0.,11.0])
def inspect(c,t):
 lane=c.at('布隆过滤器')-.26;maybe=c.at('可能见过');example=c.at('看这份短文');qu=c.at('六十五个词')
 f=c.at('上面是许多');s=c.at('下面是跟评测')
 if t<lane+.24:return pass_clock(c)(t),1.
 if t<maybe-.97:return 11.,1.
 if t<maybe-.13:
  k=easepos(t,maybe-.97,.84)
  return mix(11.,48.,k),1.-.82*sin(pi*k)**.74
 if t<example-.28:return 48.,1.
 if t<f-.71:
  # Finish looking across the example page before returning to its two findings.
  return mix(48.,52.,easepos(t,example-.28,qu-example+1.08)),1.
 if t<f+.19:
  q=easepos(t,f-.71,.90)
  return mix(52.,0.,q),1.-.63*sin(pi*q)**.75
 if t<s-.21:return 0.,1.
 if t<s+.64:
  q=easepos(t,s-.21,.85)
  return 48.*q,1.-.57*sin(pi*q)**.69
 return 48.,1.


def held_words(g,c,j,frac,opacity):
 t=c.t;start=c.at('换进一个词');next_=c.at('也放走一个词');lane=c.at('布隆过滤器')-.26
 a=during(t,start-.24,lane,.40)*opacity
 if a:
  # Only two changing words get an enlarged view. The other twelve stay inside
  # the original window; these are its actual two neighbours at this step.
  k=min(len(DOC)-14,j);left=DOC[k];right=DOC[k+13]
  u=enter(t,next_-.16,.49)
  for x,txt_,tag,co,v,sign in ((275,left,'移出',O,u,-1),(1323,right,'移入',T,1.,1)):
   xx=x+sign*23*(1-frac);h=13+5*(1-frac);lab=a*v
   label(g,txt_,xx,664,40,co,lab,limit=207)
   label(g,tag,xx,724,26,co,lab)
   p=[(xx+sign*(88+h),669),(xx+sign*(121+h),669),(xx+sign*(110+h),658)]
   if sign>0: p=[(xx-75-h,669),(xx-119-h,669),(xx-108-h,658)]
   path(g,p,enter(t,(next_ if sign<0 else start)-.16,.60),co,2.9,lab)


def chip_state(g,c,j,fact,base):
 t=c.t;neg=c.at('一次阴性');maybe=c.at('可能见过');verify=c.at('核对原文');ok=c.at('词序真的一样');end=c.at('看这份短文')
 draw_a=enter(t,neg-.18,.53)*(1-phase(t,maybe-.96,maybe-.59))*base
 if draw_a:
  _,sites,possible,_=observe(j)
  if not possible:
   h=enter(t,neg-.15,.64);w=next(n for n in sites if n not in bits);x=204+w%32*18.2+6;y=646+w//32*17.1+6
   ring(g,x,y,12.,O,draw_a*h,2.45)
   label(g,'有一位为 0',1144,667,33,O,draw_a*h)
   label(g,'这窗跳过',1144,721,29,M,draw_a*enter(t,c.at('可以跳过')-.15,.52))
 water=during(t,maybe-.21,end-.08,.50)*base
 if water and all(n in bits for n in observe(j)[1]):
  v=easepos(t,verify-.22,.86);match=enter(t,ok-.12,.57)
  cap=water*(1-v)
  if cap:
   label(g,'三位皆为 1',1135,670,34,O,cap)
   label(g,'可能见过',1135,722,29,M,cap)
  if v:
   air=water*v;w=29;start=958;co=O if fact=='模板' else T
   for row,y in enumerate((666,710)):
    label(g,('原文','索引')[row],start-29,y,22,M,air,'right')
    for i in range(13):
     k=enter(t,verify-.10+.039*i+.18*row,.48)
     col=blend(co,Y,match)
     rect(g,start+w*i,y-9,17,18,inkcol(col,.87),air*k)
     if not row and match:line(g,(start+w*i+8,y+10),(start+w*i+8,y+31),col,1.25,air*match*.83)
   label(g,'十三词顺序相同',1143,752,26,Y,match*air)
 return max(draw_a,water)
def bands(g,rows,starts,raw,k,palette,alpha):
 for ri,(_,yy,fs,r) in enumerate(rows):
  base=starts[ri];tail=base+len(r)
  a=max(k,base);b=min(k+13,tail)
  if b-a<.002:continue
  def corner(j,is_last):
   j=clip((j-base)/len(r))*len(r);i=min(len(r)-1,int(j));m=j-i
   lo,hi=r[i];prev=r[i-1][1] if i else lo
   # Move the endpoint to the next glyph on the SAME baseline. Whitespace is
   # included only when two neighbours are simultaneously inside the aperture.
   if is_last and m<.0001 and i:return prev
   return mix(lo,hi,m)
  left=corner(a,False)-5;right=corner(b,True)+5
  if right-left<2.:continue
  rect(g,left,yy-19,right-left,38,inkcol(palette,.35),.74*alpha)
  line(g,(left,yy+19),(right,yy+19),palette,2.55,alpha)
  ctx=g.c;ctx.save();ctx.rectangle(left,yy-19,right-left,38);ctx.clip()
  from studio_examples import MONO
  txt(g,raw[ri][1],rows[ri][0],yy,fs,F,alpha,'left',font=MONO)
  ctx.restore()
