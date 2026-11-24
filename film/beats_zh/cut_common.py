"""The shared camera and object grammar of the continuous six-chunk cut."""
from spatial import *
from spatial import ShotCanvas as _ShotCanvas, World as _World
from visual import Pango, PangoCairo, desc
from functools import lru_cache
import json
import re
from pathlib import Path
BG='#000000'
CYAN='#58C4DD'
GOLD='#FFFF00'
TEAL='#5CD0B3'
GREEN='#83C167'
CORAL='#FC6255'
PURPLE='#A56CFF'
WHITE='#FFFFFF'
MILD='#CDCDCD'
AXIS='#D6D6D6'
EDGE='#626262'
BOX='#0B0B0B'
SERIF='Latin Modern Roman'
CJK='Noto Serif CJK SC'
HAN=re.compile(r'[\u3400-\u9fff\u3000-\u303f\uff01-\uff60]')
MONO='JetBrainsMono Nerd Font Mono'  # Only source-code excerpts use this face.
AX0=(-3.95,-1.85,0.)
AXT=(-3.95,2.20,0.)
AXR=(4.63,-1.85,0.)
RING_POINT=(0,0,.10)
RING_RADIUS=.42


class ShotCanvas(_ShotCanvas):
    # Shape each string once at a fixed em. Keep that em in world space:
    # a zoom changes the transform, never Pango's layout or hinted advances.
    EM=128.0

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self._glyph_ctx=cairo.Context(cairo.ImageSurface(cairo.FORMAT_A8,1,1))
        opts=cairo.FontOptions()
        opts.set_hint_style(cairo.HINT_STYLE_NONE)
        opts.set_hint_metrics(cairo.HINT_METRICS_OFF)
        self._glyph_ctx.set_font_options(opts)
        self._glyph_options=opts
        self._outline=lru_cache(maxsize=768)(self._build_outline)

    def _build_outline(self,s,font,weight):
        c=self._glyph_ctx
        c.new_path()
        c.move_to(0,0)
        layout=PangoCairo.create_layout(c)
        context=layout.get_context()
        PangoCairo.context_set_resolution(context,96)
        PangoCairo.context_set_font_options(context,self._glyph_options)
        context.set_round_glyph_positions(False)
        if HAN.search(s):
            family={'sans':'Noto Sans','serif':SERIF,'math':'Latin Modern Math','mono':MONO}.get(font,font)
            font=f'{family}, {CJK}' if family not in (CJK,'Noto Sans') else f'{CJK}, {SERIF}'
        layout.set_font_description(desc(self.EM,font,weight))
        layout.set_text(s,-1)
        PangoCairo.layout_path(c,layout)
        ink,_=layout.get_extents()
        return c.copy_path(),tuple(v/Pango.SCALE for v in (ink.x,ink.y,ink.width,ink.height))

    def packet(self,r):
        super().packet(r)
        self.zh_cue_override=r.get('zh_cue_override',{})

    def cue(self,phrase,default,occurrence=0):
        q=getattr(self,'zh_cue_override',{})
        if not occurrence and (phrase_key:=flatkey(phrase)) in q:
            return q[phrase_key]
        return super().cue(phrase,default,occurrence)

    def measure(self,s,size=36,font='sans',weight='normal'):
        _,(_,_,width,_)=self._outline(str(s),font,weight)
        return width*size/self.EM

    def text(self,s,x,y,size=36,color=WHITE,alpha=1,align='center',font='sans',weight='normal'):
        if not s or alpha<=0 or size<=0:return
        path,(left,top,width,height)=self._outline(str(s),font,weight)
        c=self.c
        c.save()
        c.translate(x,y)
        c.scale(size/self.EM,size/self.EM)
        c.translate(-left-{'center':width*.5,'right':width}.get(align,0),-top-height*.5)
        c.new_path()
        c.append_path(path)
        self.source(color,alpha)
        c.fill()
        c.restore()


class World(_World):
    def text(self,s,p,size=33,c=WHITE,alpha=1,align='center',font='serif',weight='normal',depth_bias=.015):
        if alpha<.002 or not s:return
        x,y,z,k=self.project(p)
        family={'serif':'Latin Modern Roman','math':'Latin Modern Math','sans':'Noto Sans'}.get(font,font)
        self.items.append((z+depth_bias,3,str(s),x,y,size*k*math.sqrt(self.zoom),c,alpha,align,family,weight))

    def ink(self,s,p,plane,size=32,c=WHITE,alpha=1,align='center',weight='normal',sort_depth=None):
        if alpha<.002 or not s:return
        x,y,z,k=self.project(p)
        dx=.035
        px,py=self.pos(add(p,trans((dx,0,0),plane)))
        ux,uy=self.pos(add(p,trans((0,-dx,0),plane)))
        m=128*self.zoom*k*dx
        mat=((px-x)/m,(py-y)/m,(ux-x)/m,(uy-y)/m)
        if mat[0]*mat[3]-mat[1]*mat[2]<.038:return
        self.items.append((z+.032 if sort_depth is None else sort_depth,7,str(s),x,y,
                          size*k*math.sqrt(self.zoom),c,alpha,align,weight,mat))

def stage(g):
    g.c.save()
    g.rect(0,0,1600,900,fill=BG)
    g.c.restore()

def pin(w,p,c=CYAN,r=.054,alpha=1,spread=10):
    # A datum is a flat pigment mark; no light effects or bloom.
    w.dot(p,c,r,alpha)

def lit_path(w,pts,c=CYAN,width=3.15,alpha=1,progress=1):
    w.path(pts,c,width,alpha,progress=progress)

def vertical(g,alpha=1):
    """Shared benchmark ruler after the X measure rotates; no AA label yet."""
    w=World(g)
    if alpha>.002:
        w.path((AX0,AXT),AXIS,2.25,alpha,arrow=True)
        for k in range(6):
            y=mix(AX0[1],AXT[1]-.08,k/5)
            w.segment((AX0[0]-.065,y,0),(AX0[0]+.065,y,0),AXIS,1.49,alpha*.82)
        pin(w,(AX0[0],AXT[1]-.18,.05),GOLD,.057,alpha,8)
    return w

def handoff_ring(g,alpha=1):
    """A sampled score pin becomes an open viewport into its construction."""
    w=World(g)
    q=RING_POINT
    ring=tuple((q[0]+RING_RADIUS*math.cos(j*math.tau/64),q[1]+RING_RADIUS*math.sin(j*math.tau/64),q[2]) for j in range(65))
    w.path(ring,CYAN,2.0,alpha)
    w.dot(q,GOLD,.057,alpha)
    return w

def note(w,anchor,title,lines,c=CYAN,al=1):
    if al<.002:return
    x,y,z=anchor
    x+=.12*(1-al)
    depth=z+.12
    w.segment((x-.19,y+.24,depth),(x-.19,y-.35-.27*(len(lines)-1),depth),c,2.4,al)
    w.text(title,(x,y,depth),30,WHITE,al,align='left',font=SERIF,weight='normal')
    for j,s in enumerate(lines):
        w.text(s,(x,y-.33-.28*j,depth),24,MILD,al,align='left')


TOKEN_LEFT=-4.63
TOKEN_RIGHT=4.63
TOKEN_Y=-.58
TOKEN_BASELINE=.01
TOKEN_WIDTH=.99
TOKEN_HEIGHT=.43
TOKEN_SCALE=1.26

@lru_cache(maxsize=1)
def token_metadata():
    p=Path(__file__).with_name('token_packet.json')
    return json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}

@lru_cache(maxsize=1)
def token_data():
    raw=token_metadata()
    if not raw:
        # Rehearse the composition before a real model packet arrives.
        return tuple((f'x{sub}',None,()) for sub in '₁₂₃₄₅₆₇₈')
    seq=raw.get('tokens',[])
    ps=raw.get('probabilities',[])
    alt=raw.get('alternatives',[()]*len(seq))
    if not seq or len(ps)!=len(seq) or len(alt)!=len(seq):
        raise ValueError('One probability and alternative group per target token are required.')
    data=[]
    for token,prob,choices in zip(seq,ps,alt):
        ptrue=float(prob)
        if not 0<=ptrue<=1:
            raise ValueError('Conditional token probabilities must lie in [0,1].')
        alts=[]
        for a in choices:
            pa=float(a['p'])
            if not 0<=pa<=1:
                raise ValueError('Candidate probabilities must lie in [0,1].')
            alts.append((a['token'],pa))
        data.append((str(token),ptrue,tuple(alts[:2])))
    return tuple(data)


def token_positions():
    n=len(token_data())
    span=(TOKEN_RIGHT-TOKEN_LEFT)/n
    return tuple(TOKEN_LEFT+span*(i+.5) for i in range(n))


def token_stage(g,alpha=1,progress=1,center=(0,0,0),zoom=1):
    """Canonical F/G pose. Geometry and heights are in shared world units."""
    w=World(g,target=center,zoom=zoom)
    rows=token_data()
    xs=token_positions()
    for i,(x,(s,ptrue,alts)) in enumerate(zip(xs,rows)):
        k=step(progress,max(0,.022*i),.55+.020*i)
        if not k:continue
        z=.105
        half=min(TOKEN_WIDTH*.5,(TOKEN_RIGHT-TOKEN_LEFT)/len(rows)*.439)*k
        y=TOKEN_Y
        p=((x-half,y-TOKEN_HEIGHT/2,z),(x+half,y-TOKEN_HEIGHT/2,z),
           (x+half,y+TOKEN_HEIGHT/2,z),(x-half,y+TOKEN_HEIGHT/2,z))
        w.path((*p,p[0]),GOLD,1.37,alpha*k*.79)
        w.text(s.strip() or s,(x,y,z+.025),29,GOLD,alpha*step(k,.48,.98),font=SERIF)
        b=step(progress,.42+.010*i,.87+.014*i)
        if b and ptrue is not None:
            w.text(f'{100*ptrue:.3g}%',(x,TOKEN_Y-.39,z+.022),22,GOLD,alpha*b,font=SERIF)
            siblings=tuple(a[1] for a in alts)
            values=(ptrue,*siblings)
            sw=min(.128,.33*half)
            n=len(values)
            c0=x-(n-1)*.102
            w.segment((x-half*.89,TOKEN_BASELINE-.017,z),(x+half*.89,TOKEN_BASELINE-.017,z),
                      EDGE,1.16,alpha*b)
            for j,q in enumerate(values):
                bx=c0+j*.204
                h=TOKEN_SCALE*q*b
                col=GOLD if not j else CYAN
                if h>.0002:
                    w.face(((bx-sw/2,TOKEN_BASELINE,z),(bx+sw/2,TOKEN_BASELINE,z),
                            (bx+sw/2,TOKEN_BASELINE+h,z),(bx-sw/2,TOKEN_BASELINE+h,z)),
                           col,alpha*b,1.0,0)
    title=step(progress,.70,.99)*alpha
    m=token_metadata()
    # Typeset the capital subscript explicitly rather than painting a literal underscore.
    if title>.002:
        cx,cy,depth,k=w.project((0,1.75,.142))
        factor=k*math.sqrt(w.zoom)
        family='Latin Modern Math'
        seg=(('P(x₁, x₂, …, x',65,0),('T',39,17),('| prefix)' if m else ')',65,0))
        size=[sz*factor for _,sz,_ in seg]
        lengths=[g.measure(txt,sz,family) for (txt,_,_),sz in zip(seg,size)]
        # Ink bounds omit leading spaces. Give the conditional bar actual
        # mathematical spacing between outlines rather than a text space.
        pads=(0,0,11.3*factor if m else 0)
        x=cx-(sum(lengths)+sum(pads))/2
        for (txt,_,dy),sz,ww,pad in zip(seg,size,lengths,pads):
            x+=pad
            w.items.append((depth+.015,3,txt,x,cy+dy*factor,sz,WHITE,title,'left',family,'normal'))
            x+=ww
    if m:
        if m.get('prefix'):
            w.text('前文：“'+m['prefix']+'”',(TOKEN_LEFT,-1.62,.14),24,MILD,title,
                   align='left',font=SERIF)
        if m.get('model'):
            w.text(m['model'].rsplit('/',1)[-1],(TOKEN_RIGHT,-1.62,.14),24,MILD,title,
                   align='right',font=SERIF)
    return w
