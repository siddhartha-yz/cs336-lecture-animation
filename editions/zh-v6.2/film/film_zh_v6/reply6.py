"""Read the complete reply. A controlled matte reveals safe/unsafe categories without depicting harmful instructions."""
from rig4 import *
from motion import guide

def branch(g,c,stop):
 t=c.t;a=c.at;room=c.rest('拒答陷阱');st=room['end']
 pre=a('开头只有一句')-.27;read=a('现在往下读')-.16;safe=a('甲停在');unsafe=a('乙却在后文');both=a('开头一模一样');whole=a('验收安全必须')
 enter_=enter(t,pre,.61);u=easepos(t,read,.82)
 limit=1-phase(t,stop-.62,stop-.09)
 begin=a('只看它开场');serious=a('安全性')
 # The screen shows a long response from the beginning; its leading slice is
 # isolated only as the eye narrows to the opening. Nothing past the slit
 # gives away which reply it will turn into.
 make=enter(t,.17,.74);ap=easepos(t,begin-.22,1.29)
 clear=1-phase(t,pre-.45,pre+.38);stretch=easepos(t,serious-.22,.93)
 if make and clear:
  center=802-39*stretch;span=1126-147*stretch;Y0=290-32*stretch
  edge=inkcol(C,.88)
  for j,n in enumerate((55,66,59,50,61,44,55,29)):
   r=enter(t,.12+.092*j,.64)
   yy=Y0+46*j
   if r:
    a0=make*r*clear*(1.-.82*ap) if j else make*r*clear
    tx=center-span*.5+7*j+32*sin(.45*j)
    ty=yy+12*sin(.75*(j+.22))*(1-stretch)
    for i in range(n):
     w=9.+(i*13+(j+5)*23)%9;gate=enter(t,.17+.011*i+.095*j,.49)
     if gate:
      x=tx+15*i
      # The lower rows are unread, not rows of attack symbols.
      col=(edge if not j else M)
      rect(g,x,ty,w,10.5,col,a0*gate*(.74 if i%7==0 else .48+.10*((i+j)%3)))
  lo=center-span*.5-25;hi=center+span*.5+25
  top=Y0-21;barrier=Y0+27.
  lip=mix(676,barrier,ap)
  line(g,(lo,top),(hi,top),edge,2.450,make*clear*.59)
  line(g,(lo,lip),(hi,lip),edge,2.4,make*clear*.73)
  guide(g,[(lo,lip),(hi,lip)],easepos(t,begin-.15,1.27),Y,make*clear,3.6,.24)
 from readout6 import in_
 in_(g,t)
 w=mix(1153,741,u);left=801-w/2;right=left+w
 y=mix(406,207,u)
 if enter_:
  op=enter_*limit
  # The reader's aperture is horizontal; trailing ink is deliberately unread
  # until the view goes down the page.
  vein=1-phase(t,whole-.18,whole+.61)
  rect(g,left,y-43,w,86,inkcol(T,.09),op*vein*.76)
  line(g,(left,y-46),(right,y-46),M,1.65,op*.71)
  line(g,(left,y+47),(right,y+47),T,2.15,op*.81)
  mark(g,'“这个忙我帮不了。”',800,y,53,t-pre+.05,F,mode='wave',dur=.59,op=op)
  gleam=phase(t,a('留在心里')-.17,room['start']-.05)
  if gleam and not u:
   head=(left+18+(w-37)*gleam,y+48);dot(g,*head,4.7,Y,op*(1-.69*gleam))
 if room['start']<=t<st:
  z=(t-room['start'])/(st-room['start'])
  line(g,(626,589),(974,589),E,1.6,limit)
  line(g,(626,589),(626+348*z,589),O,2.9,limit)
  # While the audience decides, there is no answer or lead-in tucked into the picture.
 if not u:return
 for j,(name,co,at,x) in enumerate((('甲',T,safe,454),('乙',R,unsafe,1150))):
  k=easepos(t,at-.24,.72);hint=u*limit
  lane=340+j*42;Y0=433+j*24
  spine=[(799,y+49),(799,y+102),(x,lane),(x,lane+32)]
  path(g,spine,u,co,2.6,hint*.84)
  width=mix(4,510,k);Y1=Y0+225
  if not k:continue
  ku=enter(t,at-.21,.52);op=hint*ku
  p0=x-width/2;p1=x+width/2
  label(g,name,p0+8,Y0-31,37,co,op,'left')
  # Only benign example text is drawn. Captioned coral blocks mark withheld harmful passage.
  ctx=g.c;ctx.save()
  ctx.rectangle(p0-8,Y0-9,width+16,123);ctx.clip()
  if not j:
   for i,ss in enumerate(('“我可以帮你整理资料，','换个安全的办法。”')):
    mark(g,ss,p0+7,Y0+19+i*55,40,t-at-.19*i,F,'left','wave',.46,op)
  else:
   lengths=(457,400,487)
   for i,ww in enumerate(lengths):
    yy=Y0+3+i*37;v=enter(t,at+.11+i*.13,.53)
    rect(g,p0+8,yy,ww*v,19,R,op*v*.50)
  ctx.restore()
  if k:
   # A reading head traverses the continuation, then parks on the observed result.
   hi=phase(t,at+.30,whole+.54)
   yy=mix(Y0,Y0+112,hi);path(g,[(p0-5,Y0),(p0-5,yy),(p0+13,yy)],k,co,2.05,op*.72)
   if 0<hi<1:point(g,p0-5,yy,4.0,co,op*.85)
  stamp=enter(t,(both if not j else unsafe+.57)-.11,.54)
  if stamp:
   txt(g,('安全替代','给出有害帮助')[j],p0+8,Y0+188,35,co,op*stamp,'left')
   check(g,p1-13,Y0+183,14,not j,op*stamp)
