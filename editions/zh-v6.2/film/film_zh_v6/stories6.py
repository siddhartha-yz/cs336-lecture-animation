"""A word-count shot based on the two unchanged Arena texts."""
from rig4 import *
from studio_preference import material,weft

def shed(g,c,start,end):
 t=c.t;cut=1-phase(t,end-.52,end-.06)
 nearby=[c.at(x)for x in ('接近八百词','两百多词')]
 reflective=c.at('确实写得好');more=c.at('多绕了几圈')
 f=phase(t,reflective-.32,reflective+.84);door=phase(t,more-.14,more+.62)
 # One strip = one word, with the same wrap width for both documents. We
 # preserve letter shapes as material grows rather than retypesetting them.
 x0s=(182,906);y0s=(260,349);plate=((C,'A','734 号擦亮黄铜路灯。'),(V,'B','维修机器人驶过空商场。'))
 for j,(co,tag,quote) in enumerate(plate):
  t0=nearby[j];start_0=start+.16*j
  slope=phase(t,t0-.58,t0+1.38);u=enter(t,start_0,.58)
  pos=phase(t,start_0-.03,start_0+.78);x=x0s[j]+44*(1-pos);y=y0s[j]-53*(1-pos)
  al=cut*u
  if not al:continue
  label(g,tag,x,y-83,37,co,al,'left')
  mark(g,quote,x,y,42,t-start_0,F,'left','wave',.45,al)
  width=517;origin=y+94
  path(g,[(x,y+42),(x+width,y+42)],pos,co,2.15,al)
  spans,rows=weft(j)
  swipe_ix=(len(spans)-1)*slope
  bump=sin(pi*slope)**.52 if abs(slope-1)>.001 else 0.
  pulse=phase(t,reflective-.2,more+.06)
  for k,(xx,i,ww) in enumerate(spans):
   reveal=clip(pos*1.62-.62*k/len(spans))
   yy=origin+i*13.
   d=math.exp(-((k-swipe_ix)/max(8.,.047*len(spans)))**2)*bump
   # During the count only the words under the reading head rise; the actual
   # line breaks, strokes, and total answer length do not change.
   hue=blend(co,Y,d*.92)
   if reveal:
    rect(g,x+xx,yy-d*5.,ww,6.55+d*1.6,hue,reveal*al*(.70+.22*(k%7<3)+d*.08))
  if slope>.01:
   yy=origin+(rows-1)*13.
   right=x+width+24
   pull=easepos(t,t0-.25,1.05)
   path(g,[(right-10,origin-6),(right,origin-6),(right,yy+14),(right-10,yy+14)],pull,co,2.6,al*.97)
   ty=max(665,yy+65)
   if slope<.993:
    label(g,str(round(swipe_ix)+1),x,ty,45,co,al*slope,'left')
   else:
    n=len(spans)
    mark(g,f'{n} 词',x,ty,48,t-t0-.43,co,'left','pen',.51,al)
  if f and not j:
   # Competing explanations connect to the same LONG response without
   # asserting either explanation about the recorded pair.
   p=enter(t,reflective-.23,.61)*al
   e=enter(t,more-.17,.51)*al
   leg0=[(x+335,664),(x+456,644),(740,644),(801,597)]
   leg1=[(x+330,692),(x+425,719),(735,719),(800,736)]
   for q,pts,ca,label_ in ((p,leg0,T,'写得详实'),(e,leg1,O,'绕远了')):
    if q:
     path(g,pts,min(1,q*1.23),ca,1.9,q*.80)
     label(g,label_,pts[-1][0]+21,pts[-1][1],27,ca,q,'left')
 bias=c.at('长度偏见')
 if t<reflective+.76:
  p=enter(t,bias+.40,.59)*cut*(1-phase(t,reflective+.11,reflective+.76))
  if p:
   # This inscription belongs to the two measured word counts.
   x,y=876,732
   path(g,[(644,698),(658,734),(746,734)],p,O,1.9,p*.83)
   mark(g,'长度偏见',x,y,35,t-bias-.36,O,mode='wave',dur=.51,op=p)
