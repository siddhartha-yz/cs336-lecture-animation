"""Joins whose *actual* common object matters: exam name, submitted diff, verified text span."""
from termnotes import hint
from ink import *
from motion import *
from cut_common import stage

def crop(g,x,y,w,h,draw):
 if w<=0 or h<=0:return
 c=g.c;c.save();c.rectangle(x,y,w,h);c.clip();draw();c.restore()

def masked(g,fn,n):
 old=getattr(g,n,False);setattr(g,n,True)
 try:fn()
 finally:setattr(g,n,old)

def exam(g,t,prev,w,raster,raw):
 """Open the new edition of the exam. MMLU never disappears or doubles."""
 end=1.35
 if t>=end:return False
 stage(g);progress=phase(t,.12,1.14)
 src=lambda:raster(g,prev,w)
 # The graphic changes pages under one title. No comparison is implied between
 # the height of GPT-4.1's point and the number of response options on a question.
 edge=mix(18,1582,progress);gap=(10+25*sin(pi*progress)) if 0<progress<1 else 0
 if progress<1:crop(g,max(0,edge+gap) if progress else 0,205,1600-(max(0,edge+gap) if progress else 0),575,src)
 if progress>0:crop(g,0,205,(edge-gap) if progress<1 else 1600,575,lambda:raw(g,'3-2',t))
 pw=g.measure('MMLU',47,font=SERIF);fw=g.measure('MMLU-Pro',47,font=SERIF)
 dist=phase(t,.06,.75);x=800-mix(pw,fw,dist)/2;y=mix(111,110,dist)
 reveal=phase(t,.21,1.01)
 if t<.15:txt(g,'MMLU',x,y,47,F,1,'left')
 else:crop(g,x-2,65,pw+2+(fw-pw+3)*reveal,84,lambda:txt(g,'MMLU-Pro',x,y,47,F,1,'left'))
 a0=1-phase(t,.02,.32);a1=phase(t,.78,1.23)
 txt(g,hint('MMLU'),800,167,24,M,a0)
 txt(g,hint('MMLU-Pro'),800,166,24,M,a1)
 return True

# Sphinx PR 8713. The same glyphs leave the repository and become five signed
# strokes in the margin of the sandbox. They are not executed until it is time.
PATCH=(('−  return self._format_fields(...)',R),('+  if self._config.napoleon_use_param:',G),('+      fields = self._consume_fields(',G),('+          multiple=True)',G),('+      return self._format_docutils_params(fields)',G))
def patch_code(g,j,x,y,a=1):
 s,col=PATCH[j];txt(g,s,x,y,24,col,a,'left',700,'DejaVu Sans Mono')
def packet_pose(t,c):
 enter=c.at('补丁打进沙箱');p=phase(t,enter-.30,enter+1.04)
 x,y=transit((161,482),(754,517),p,56)
 return x,y,p
def patch_sheet(g,x,y,a=1,frame=1):
 w,h=110,96
 if frame:docs(g,x-w/2,y-h/2,w,h,T,a*frame,0)
 for j,(s,col) in enumerate(PATCH):
  yy=y-24+12*j;xx=x-35
  width=69*(.71*min(g.measure(s,24,font='DejaVu Sans Mono'),700)/700+.22)
  line(g,(xx,yy),(xx+width,yy),col,2.65,a)
def repository(g,t,prev,w,raster,raw):
 if t>=1.91:return False
 if t<.006:raster(g,prev,w);return True
 stage(g);end=1-phase(t,.08,.85)
 if end:
  raster(g,prev,w,end);rect(g,727,400,750,203,BLACK,1)
 new=lambda:masked(g,lambda:raw(g,'5-2',t),'carry_patch')
 # The text of the traveling diff owns the centre until it docks. Reveal the
 # right-hand suite first; its left-hand neighbour waits until the code has passed.
 a=phase(t,.69,1.43)
 if a:
  crop(g,0,0,1600,204,lambda:curtain(g,a,new))
  crop(g,849,204,751,587,lambda:curtain(g,a,new))
 left=phase(t,1.43,1.82)
 if left:crop(g,0,204,849,587,lambda:curtain(g,left,new))
 # Move the five rows as a SINGLE affine shape until a student need only
 # recognize the signed change. Then hand each row to its own same-colour stroke.
 p=phase(t,.10,1.76);x,y=transit((1088,501),(161,482),p,66)
 mag=mix(1,.19,p);a_text=1-phase(p,.40,.76);a_ink=phase(p,.42,.78)
 if a_text:
  c=g.c;c.save();c.translate(x,y);c.scale(mag,mag);c.translate(-1088,-501)
  for j in range(5):patch_code(g,j,738,423+39*j,a_text)
  c.restore()
 if a_ink:
  for j,(s,col) in enumerate(PATCH):
   r=min(g.measure(s,24,font='DejaVu Sans Mono'),700)
   xx=mix(x-350*mag,x-35,p);yy=y+(j-2)*mix(39*mag,12,p);wid=mix(r*mag,69*(.71*r/700+.22),p)
   line(g,(xx,yy),(xx+wid,yy),col,mix(1.3,2.65,p),a_ink)
 frame=phase(t,1.09,1.72)
 if frame:docs(g,x-55,y-48,110,96,T,frame,0)
 txt(g,'候选补丁',x,552,23,T,phase(t,1.53,1.86))
 return True

def match(g,t,prev,w,raster,raw):
 """A verified run of 13 words folds into the matching lines of ONE document."""
 if t>=1.46:return False
 from validity import WORDS,WIDTH
 if t<.008:raster(g,prev,w);return True
 stage(g);out=1-phase(t,.04,.82)
 if out:
  raster(g,prev,w,out)
  # Replace just the moving window's content; the rest of the old board remains in place.
  rect(g,282,280,1010,92,BLACK,1)
 new=lambda:masked(g,lambda:raw(g,'7-4',t),'carry_gram')
 page=phase(t,.31,1.05);headline=phase(t,.75,1.28)
 if page:crop(g,0,205,1600,581,lambda:curtain(g,page,new))
 if headline:crop(g,0,0,1600,205,lambda:curtain(g,headline,new))
 p=phase(t,.08,1.38);start=200+(9-.83*9)*78
 locs=[]
 for j,word in enumerate(WORDS[-WIDTH:]):
  row,n=divmod(j,7);nr=(7,6)[row];total=132+((4+row)*19%47);ww=total/nr
  q=phase(t,.07+.012*j,1.11+.012*j)
  xx,yy=transit((start+j*78,331),(224+(n+.5)*ww,436+row*25),q,41+12*row)
  width=mix(46,ww,q);vis=1-phase(q,.33,.70)
  if vis:txt(g,word,xx,yy,29,Y,vis)
  col=blend(E,R,phase(q,.18,.86));y=yy+32*(1-q)
  # The small separation between glyphs closes as the two complete lines settle.
  sep=.65*sin(pi*q)
  line(g,(xx-width*.5+sep,y),(xx+width*.5-sep,y),col,mix(1.1,3.75,q),1)
  locs.append((xx,yy))
 # The bracket was a 13-word window. Retire it as its contents enter the page.
 bracket=1-phase(t,.02,.50)
 if bracket:g.poly([(start-32,351),(start-32,289),(start+12*78+32,289),(start+12*78+32,351)],Y,2.35,bracket)
 return True
