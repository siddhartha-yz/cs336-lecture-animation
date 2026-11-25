"""Shared vector vocabulary for the CS336 Evaluation film, in 1600×900 logical units."""
import math,re,unicodedata
from functools import lru_cache
import cairo, gi
from pathlib import Path
if (Path(__file__).resolve().parent/'vendor/pango-cairo-gi').exists():
    gi.__path__.append(str(Path(__file__).resolve().parent/'vendor/pango-cairo-gi'))
gi.require_foreign('cairo')
gi.require_version('Pango','1.0')
gi.require_version('PangoCairo','1.0')
from gi.repository import Pango, PangoCairo

BG='#000000'; INK='#FFFFFF'; MUTED='#BBBBBB'; GRID='#333333'
BLUE='#58C4DD'; PURPLE='#B189C6'; GOLD='#F4D345'; GREEN='#83C167'; RED='#FC6255'
A=BLUE; B=PURPLE; W=INK
TAU=math.tau

def clamp(x,lo=0,hi=1): return max(lo,min(hi,x))
def mix(a,b,t): return a + (b-a)*t
def ease(t):
    t=clamp(t)
    return t*t*(3-2*t)
def step(u,a,b): return ease((u-a)/(b-a))
def smooth_tail(t): return 1-(1-clamp(t))**3

@lru_cache(maxsize=512)
def rgb(color):
    if isinstance(color,tuple): return color
    color=color.lstrip('#')
    return tuple(int(color[i:i+2],16)/255 for i in (0,2,4))
def blend(a,b,t):
    return '#'+''.join(f'{round(255*mix(x,y,clamp(t))):02x}' for x,y in zip(rgb(a),rgb(b)))

@lru_cache(maxsize=128)
def desc(size,font,weight):
    family={'sans':'Noto Sans CJK SC, Noto Sans','serif':'Noto Serif CJK SC, DejaVu Serif','math':'DejaVu Serif, Noto Serif CJK SC','mono':'DejaVu Sans Mono, Noto Sans CJK SC'}.get(font,font)
    d=Pango.FontDescription()
    d.set_family(family)
    d.set_weight({'bold':Pango.Weight.BOLD,'medium':Pango.Weight.MEDIUM,'normal':Pango.Weight.NORMAL,'light':Pango.Weight.LIGHT}.get(weight,Pango.Weight.NORMAL))
    d.set_absolute_size(size*Pango.SCALE)
    return d

def roundpath(c,x,y,w,h,r):
    if not r:
        c.rectangle(x,y,w,h); return
    r=min(w/2,h/2,r)
    c.new_sub_path()
    c.arc(x+w-r,y+r,r,-math.pi/2,0)
    c.arc(x+w-r,y+h-r,r,0,math.pi/2)
    c.arc(x+r,y+h-r,r,math.pi/2,math.pi)
    c.arc(x+r,y+r,r,math.pi,3*math.pi/2)
    c.close_path()

class Canvas:
    def __init__(self,c,width=1600,height=900):
        self.c=c
        self.c.scale(width/1600,height/900)
        self.c.set_line_cap(cairo.LINE_CAP_ROUND)
        self.c.set_line_join(cairo.LINE_JOIN_ROUND)
        self.layouts={}
        self.cues_text=''
        self.cues=[]
    def cue(self,phrase,default,occurrence=0):
        phrase=re.sub(r'[^㐀-鿿\da-z]+','',unicodedata.normalize('NFKC',phrase).casefold())
        if not phrase:return default
        start=-1
        for _ in range(occurrence+1):
            start=self.cues_text.find(phrase,start+1)
            if start<0:return default
        return self.cues[start] if start<len(self.cues) else default

    def source(self,color,alpha=1):
        self.c.set_source_rgba(*rgb(color),clamp(alpha))
    def prepare(self,s,size,font,weight):
        key=(str(s),size,font,weight)
        if key in self.layouts: return self.layouts[key]
        layout=PangoCairo.create_layout(self.c)
        PangoCairo.context_set_resolution(layout.get_context(),96)
        layout.set_font_description(desc(float(size),font,weight))
        layout.set_text(str(s),-1)
        if len(self.layouts)>1250:self.layouts.clear()
        item=(layout,layout.get_extents()[1])
        self.layouts[key]=item
        return item
    def measure(self,s,size=36,font='sans',weight='normal'):
        return self.prepare(s,size,font,weight)[1].width/Pango.SCALE
    def text(self,s,x,y,size=36,color=INK,alpha=1,align='center',font='sans',weight='normal'):
        if alpha<=0 or not s: return
        layout,rc=self.prepare(s,size,font,weight)
        c=self.c
        w,h=rc.width/Pango.SCALE,rc.height/Pango.SCALE
        x-= {'center':w/2,'right':w}.get(align,0)
        self.source(color,alpha)
        c.move_to(x-rc.x/Pango.SCALE,y-h/2-rc.y/Pango.SCALE)
        PangoCairo.show_layout(c,layout)
    def line(self,x1,y1,x2,y2,color=INK,width=2,alpha=1,dash=None):
        if alpha<=0 or width<=0: return
        c=self.c; c.new_path(); c.move_to(x1,y1); c.line_to(x2,y2)
        self.source(color,alpha); c.set_line_width(width)
        if dash: c.set_dash(dash)
        c.stroke()
        if dash: c.set_dash([])
    def poly(self,points,color=INK,width=2,alpha=1,close=False,fill=None,fill_alpha=1):
        if alpha<=0 or len(points)<2: return
        c=self.c; c.new_path(); c.move_to(*points[0])
        for p in points[1:]: c.line_to(*p)
        if close: c.close_path()
        if fill:
            self.source(fill,fill_alpha*alpha)
            if width and color: c.fill_preserve()
            else: c.fill()
        if width and color:
            self.source(color,alpha); c.set_line_width(width); c.stroke()
    def rect(self,x,y,w,h,fill=None,stroke=None,width=2,r=0,alpha=1):
        if w<=0 or h<=0 or alpha<=0: return
        c=self.c; c.new_path(); roundpath(c,x,y,w,h,r)
        if fill:
            self.source(fill,alpha)
            if stroke: c.fill_preserve()
            else: c.fill()
        if stroke:
            self.source(stroke,alpha); c.set_line_width(width); c.stroke()
    def circle(self,x,y,r,fill=None,stroke=None,width=2,alpha=1):
        if alpha<=0 or r<=0: return
        c=self.c; c.new_path(); c.arc(x,y,r,0,TAU)
        if fill:
            self.source(fill,alpha)
            if stroke: c.fill_preserve()
            else: c.fill()
        if stroke:
            self.source(stroke,alpha); c.set_line_width(width); c.stroke()
    def arrow(self,x1,y1,x2,y2,color=MUTED,width=2,alpha=1,head=11):
        if alpha<=0: return
        d=math.hypot(x2-x1,y2-y1)
        if d<.01:return
        self.line(x1,y1,x2,y2,color,width,alpha)
        phi=math.atan2(y2-y1,x2-x1); h=min(d*.45,head)
        self.poly([(x2-h*math.cos(phi-.51),y2-h*math.sin(phi-.51)),(x2,y2),(x2-h*math.cos(phi+.51),y2-h*math.sin(phi+.51))],color,width,alpha)
    def arc(self,x,y,r,a,b,color=INK,width=2,alpha=1):
        if alpha<=0 or r<=0: return
        c=self.c; c.new_path(); c.arc(x,y,r,a,b); self.source(color,alpha); c.set_line_width(width); c.stroke()
    def check(self,x,y,ok=True,r=15,alpha=1):
        w=max(2,r*.16)
        if ok: self.poly([(x-r*.63,y),(x-r*.17,y+r*.53),(x+r*.83,y-r*.57)],GREEN,w,alpha)
        else:
            self.line(x-r*.65,y-r*.65,x+r*.65,y+r*.65,RED,w,alpha)
            self.line(x-r*.65,y+r*.65,x+r*.65,y-r*.65,RED,w,alpha)
    def disk(self,x,y,color,r=53,label='',alpha=1):
        self.circle(x,y,r+9,stroke=color,width=1,alpha=alpha*.20)
        self.circle(x,y,r,fill=blend(BG,color,.145),stroke=color,width=2.7,alpha=alpha)
        if label: self.text(label,x,y,r*.78,color,alpha,font='math')
        else: self.circle(x,y,max(3,r*.12),fill=color,alpha=alpha)
    def tile(self,x,y,w=68,h=62,label='',color=GOLD,alpha=1,selected=False):
        self.rect(x-w/2,y-h/2,w,h,fill=blend(BG,color,.18 if selected else .09),stroke=color,width=2.6 if selected else 1.8,r=7,alpha=alpha)
        if label:self.text(label,x,y,min(w*.55,h*.52,34),color,alpha,weight='medium')
    def anchor(self,alpha=1,scale=1,y=420):
        self.disk(800-270*scale,y,BLUE,53*scale,'A',alpha)
        self.disk(800+270*scale,y,PURPLE,53*scale,'B',alpha)
        self.tile(800,y,68*scale,62*scale,'',GOLD,alpha,True)

def background(g):
    g.source(BG)
    g.c.paint()
