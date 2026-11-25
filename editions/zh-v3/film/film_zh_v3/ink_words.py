"""One fixed-em outline per label. Handwriting is for a mathematical discovery, not for subtitles."""
from functools import lru_cache
import math,bisect,unicodedata
from ink import *
from cut_common import cairo,SERIF,CJK
from visual import Pango,PangoCairo,desc
def out(p):
 p=max(0.,min(1.,p));return 1-(1-p)**3
def _l(g,txt_,size,font):
 if not hasattr(g,'_letter_shape'):g._letter_shape=lru_cache(maxsize=144)(lambda s,ft:_prep(g,s,ft))
 return g._letter_shape(txt_,font)
def _prep(g,s,font):
 full,b=g._outline(s,font,'normal');fac='Noto Serif CJK SC' if any('\u3400'<=c<='\u9fff' for c in s)and font==CJK else font
 if any('\u3400'<=c<='\u9fff'for c in s)and fac!=CJK:fac=f'{fac}, {CJK}'
 cc=g._glyph_ctx;lay=PangoCairo.create_layout(cc);pc=lay.get_context();pc.set_round_glyph_positions(False);PangoCairo.context_set_resolution(pc,96);PangoCairo.context_set_font_options(pc,g._glyph_options)
 lay.set_font_description(desc(g.EM,fac,'normal'));lay.set_text(s,-1)
 groups=[];key='';jx=0
 for ch in s:
  if unicodedata.combining(ch):continue
  if not ch.isspace():
   rc=lay.index_to_pos(jx);groups.append((rc.x/Pango.SCALE+max(0,rc.width/Pango.SCALE)*.5,ch))
  jx+=len(ch.encode())
 centers=[x for x,_ in groups]or [0];outlines=[[]for _ in centers];cc.new_path();cc.append_path(full);cc.set_tolerance(.25)
 p=[]
 def finish():
  if len(p)<3:return
  cx=(min(z[0]for z in p)+max(z[0]for z in p))/2
  k=min(range(len(centers)),key=lambda i:abs(centers[i]-cx)); lengths=[0.]
  for a,bb in zip(p,p[1:]):lengths.append(lengths[-1]+math.hypot(a[0]-bb[0],a[1]-bb[1]))
  outlines[k].append((tuple(p),tuple(lengths)))
 for tp,xy in cc.copy_path_flat():
  if tp==cairo.PathDataType.MOVE_TO:finish();p=[xy]
  elif tp==cairo.PathDataType.LINE_TO:p.append(xy)
  elif tp==cairo.PathDataType.CLOSE_PATH:
   if p:p.append(p[0])
   finish();p=[]
 finish()
 return full,b,tuple((v,sum(lengths[-1] for pts,lengths in v))for v in outlines if v)
def letter(g,s,x,y,sz,t,mode='wave',col=F,op=1,align='center',font=SERIF,dur=.56):
 if op<.003 or t<0 or g.no_text or (hasattr(g,"outside") and g.outside(s,x,y,sz)):return
 if t>=dur:return txt(g,s,x,y,sz,col,op,align,font=font)
 path0,(le,top,ww,h),groups=_l(g,s,sz,font);ctx=g.c;ctx.save();ctx.translate(x,y);ctx.scale(sz/g.EM,sz/g.EM);ctx.translate(-le-{'center':ww*.5,'right':ww}.get(align,0),-top-h*.5)
 tail=.32 if mode=='pen' else .40
 for i,(outlines,total) in enumerate(groups):
  p=clip((t/dur-tail*i/max(1,len(groups)-1))/(1-tail))
  if p<.001:continue
  ctx.save()
  if mode=='wave':
   ctx.translate(0,9*g.EM/sz*(1-out(p)));limit=1.;alpha=out(p)
  elif mode=='step':
   if p<.5:ctx.restore();continue
   limit=1.;alpha=1.
  else:limit=min(1,p/.63);alpha=phase(p,.47,1)
  if alpha>0:
   ctx.new_path()
   for pts,_ in outlines:
    ctx.move_to(*pts[0])
    for q in pts[1:]:ctx.line_to(*q)
    ctx.close_path()
   g.source(col,op*alpha);ctx.fill()
  if mode=='pen' and p<.995:
   length=total*limit;ctx.new_path()
   for pts,lens in outlines:
    if length<=0:break
    idx=min(len(pts)-1,bisect.bisect_right(lens,length)-1);ctx.move_to(*pts[0])
    for q in pts[1:idx+1]:ctx.line_to(*q)
    if idx<len(pts)-1:
     u=(length-lens[idx])/max(.001,lens[idx+1]-lens[idx]);ctx.line_to(*lerp(pts[idx],pts[idx+1],clip(u)))
    length-=lens[-1]
   ctx.set_line_width((1.25-.45*alpha)*g.EM/sz);ctx.set_line_cap(cairo.LINE_CAP_ROUND);ctx.set_line_join(cairo.LINE_JOIN_ROUND);g.source(col,op*(1-alpha*.8));ctx.stroke()
  ctx.restore()
 ctx.restore()
def swish(g,x0,x1,y,t,col=Y,dur=.48,w=2.8):
 if 0<t<dur:
  z=t/dur;a=out(max(0,(z-.41)/.59));b=out(min(1,z/.62));line(g,(mix(x0,x1,a),y),(mix(x0,x1,b),y),col,w,math.sin(math.pi*z)**.45)
def carryword(g,s,fr,to,k,fs0,fs1,col=F,lift=36,op=1):
 x,y=lerp(fr,to,k);y-=lift*math.sin(k*math.pi);txt(g,s,x,y,mix(fs0,fs1,k),col,op)
