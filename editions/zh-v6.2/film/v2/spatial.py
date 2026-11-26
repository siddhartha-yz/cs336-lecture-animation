"""World-space props, perspective optics and camera-mounted vector typography."""
from pathlib import Path
import sys,math,re,unicodedata
from functools import lru_cache
ROOT=Path(__file__).resolve().parent
if str(ROOT.parent) not in sys.path:sys.path.append(str(ROOT.parent))
from visual import (Canvas,BG,INK,MUTED,GRID,BLUE,PURPLE,GOLD,GREEN,RED,blend,rgb,step,mix,clamp,ease,background,cairo)
# Saturated pigments for the active diegetic objects. Low-opacity gray
# scaffolding and the black stage stay neutral.
BLUE='#39CDF2'; PURPLE='#BA7EFF'; GOLD='#FFD448'
GREEN='#72E784'; RED='#FF5B68'
A=BLUE; B=PURPLE; W=INK
TAU=math.tau
def vlerp(a,b,u):return tuple(mix(x,y,u) for x,y in zip(a,b))
def add(a,b):return (a[0]+b[0],a[1]+b[1],a[2]+b[2])
def sub(a,b):return (a[0]-b[0],a[1]-b[1],a[2]-b[2])
def mul(a,s):return (a[0]*s,a[1]*s,a[2]*s)
def dot(a,b):return a[0]*b[0]+a[1]*b[1]+a[2]*b[2]
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def norm(a):
    d=math.sqrt(max(1e-12,dot(a,a)));return mul(a,1/d)
def flatkey(s):
    return re.sub(r'[^a-z0-9]+','',unicodedata.normalize('NFKC',s).lower())
@lru_cache(maxsize=4096)
def tint(color,brightness):
    if brightness>1:return blend(color,INK,clamp(brightness-1))
    r,g,b=rgb(color)
    chroma=max(r,g,b)-min(r,g,b)
    if chroma>=.20 and brightness>=.065:
        # Expose pigments, not the background; keep shadow volumes distinct.
        brightness=.97*clamp(brightness)**.59
    return blend(BG,color,clamp(brightness))
def tone(c,v):return tint(c,round(clamp(v,0,1.3)*60)/60)
@lru_cache(maxsize=1024)
def rotation(rot):
    a,b,c=rot
    x,y,z=math.cos(a),math.cos(b),math.cos(c)
    p,q,r=math.sin(a),math.sin(b),math.sin(c)
    return ((y*z,p*q*z-x*r,x*q*z+p*r),(y*r,p*q*r+x*z,x*q*r-p*z),(-q,p*y,x*y))
def trans(p,m):
    return (dot(p,m[0]),dot(p,m[1]),dot(p,m[2]))
LIGHT=norm((-.50,.81,.73))
CZ=(0,0,1)
SIGNS=((-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1))
FACETS=(((4,5,6,7),(0,0,1)),((3,2,1,0),(0,0,-1)),((0,4,7,3),(-1,0,0)),((1,2,6,5),(1,0,0)),((3,7,6,2),(0,1,0)),((0,1,5,4),(0,-1,0)))
CIRCLE=tuple((math.cos(j*TAU/40),math.sin(j*TAU/40)) for j in range(40))
def readable(c,value):
    r,g,b=rgb(tone(c,value))
    return '#0B0C11' if .2126*r+.7152*g+.0722*b>.44 else INK
class ShotCanvas(Canvas):
    def __init__(self,*args,**kw):
        super().__init__(*args,**kw);self.parts=[];self.speech=0.
    def cue(self,phrase,default,occurrence=0):
        q=flatkey(phrase)
        if not q:return default
        k=-1
        for _ in range(occurrence+1):
            k=self.cues_text.find(q,k+1)
            if k<0:return default
        return self.cues[k] if k<len(self.cues) else default
    def part(self,i,default):
        return self.parts[i] if i<len(self.parts) else default
    def check(self,x,y,ok=True,r=15,alpha=1):
        w=max(2.0,r*.17)
        if ok:self.poly([(x-r*.63,y),(x-r*.17,y+r*.53),(x+r*.83,y-r*.57)],GREEN,w,alpha)
        else:
            self.line(x-r*.65,y-r*.65,x+r*.65,y+r*.65,RED,w,alpha)
            self.line(x-r*.65,y+r*.65,x+r*.65,y-r*.65,RED,w,alpha)
    def packet(self,r):
        self.cues_text=r.get('cues_text','');self.cues=r.get('cues',[]);self.parts=r.get('parts_at',[]);self.speech=r.get('speech',0.)
class World:
    def __init__(self,g,yaw=0,pitch=0,zoom=1,target=(0,0,0),distance=13,perspective=1,center=(800,404)):
        self.g=g;self.cx,self.cy=center;self.zoom=zoom;self.scale=128*zoom;self.distance=distance;self.perspective=perspective
        self.target=target
        cy,sy=math.cos(yaw),math.sin(yaw);cp,sp=math.cos(pitch),math.sin(pitch)
        self.right=(cy,0,-sy);self.up=(-sy*sp,cp,-cy*sp);self.depth=(sy*cp,sp,cy*cp)
        self.eye=add(target,mul(self.depth,distance))
        self.items=[]
    def project(self,p):
        r=sub(p,self.target)
        z=dot(r,self.depth)
        k=self.distance/max(.35*self.distance,self.distance-z*self.perspective)
        return (self.cx+self.scale*k*dot(r,self.right),self.cy-self.scale*k*dot(r,self.up),z,k)
    def pos(self,p):
        v=self.project(p);return v[0],v[1]
    def face(self,points,c=MUTED,alpha=1,fill=.18,edge=1.2):
        if alpha<.002 or len(points)<3:return
        pp=[self.project(p) for p in points]
        y=sum(p[2] for p in pp)/len(pp)
        self.items.append((y,0,[(p[0],p[1]) for p in pp],tone(c,.77),float(edge),alpha,tone(c,fill) if fill>0 else None))
    def _face(self,points,n,c,alpha,fill,edge):
        if alpha<.002:return
        if dot(n, sub(self.eye,points[0]))<=.000001:return
        pp=[self.project(p) for p in points]
        k=dot(n,LIGHT)
        intensity=clamp(fill*(.67+.46*k)+.04,.022,1.22)
        z=sum(p[2] for p in pp)/len(pp)
        ps=[(p[0],p[1]) for p in pp]
        shade=.56+.26*max(0,k)
        lw=edge*(1 if fill<=0 else .64+.21*max(0,k))
        self.items.append((z,0,ps,tone(c,shade),lw,alpha,tone(c,intensity) if fill>0 else None))
    def box(self,p,size,c=GOLD,alpha=1,rot=(0,0,0),label='',fill=.26,edge=1.1,label_size=30,label_color=None):
        if alpha<.002 or min(size)<=0:return
        s=mul(size,.5); M=rotation(tuple(rot))
        vs=[add(p,trans((x*s[0],y*s[1],z*s[2]),M)) for x,y,z in SIGNS]
        for ix,n in FACETS:self._face([vs[j] for j in ix],trans(n,M),c,alpha,fill,edge)
        if label:
            face=trans(CZ,M)
            fo=dot(face,self.depth)
            focus=step(fo,.06,.48)
            if focus>0:
                pc=add(p,mul(face,s[2]+.009))
                self.text(label,pc,label_size,label_color or readable(c,fill*(.67+.46*dot(face,LIGHT))+.04),alpha*focus,font='serif',weight='medium')
    def tile(self,p,label='',c=GOLD,size=(.96,.67,.14),rot=(0,0,0),alpha=1,fill=.33,label_size=31):
        """A cut swatch, not a miniature extrusion. The cut has a real plane."""
        if alpha<.002 or min(size)<=0:return
        x,y,z=mul(size,.5);m=rotation(tuple(rot));f=lambda q:add(p,trans(q,m))
        n=trans(CZ,m);q=step(dot(n,self.depth),.035,.40)
        d=min(.075,.27*y,.15*x)
        xy=((-x,-y),(x,-y),(x,y-d),(x-d,y),(-x,y))
        points=[f((xx,yy,z*.18)) for xx,yy in xy]
        light=clamp(fill*(.89+.14*abs(dot(n,LIGHT))),.025,1.0)
        self.face(points,c,alpha,light,.55 if light>.37 else .85)
        if label and q>.01:
            self.ink(label,f((0,0,z*.18)),m,label_size,readable(c,light),alpha*q,
                     weight='medium',sort_depth=self.project(p)[2]+.095)
    def paper(self,p,width,height,c=GOLD,alpha=1,rot=(0,0,0),fill=.74,cut=.23):
        """Uncoated stock and one crease, inked all in the plane of the page."""
        if alpha<.002 or min(width,height)<.01:return
        x,y=width/2,height/2;d=min(cut,width*.24,height*.24);m=rotation(tuple(rot))
        f=lambda q:add(p,trans(q,m));n=trans(CZ,m)
        xy=((-x,-y),(x,-y),(x,y-d),(x-d,y),(-x,y))
        br=clamp(fill*(.85+.18*abs(dot(n,LIGHT))))
        stock=blend('#22242A',blend('#FFFAEC',c,.055),br)
        fold=blend(stock,BG,.20)
        face=[self.project(f((xx,yy,.020))) for xx,yy in xy]
        depth=self.project(p)[2]+.02
        self.items.append((depth,0,[q[:2] for q in face],stock,0.0,alpha,stock))
        crease=[self.project(f((xx,yy,.022)))[:2] for xx,yy in ((x-d,y),(x-d,y-d),(x,y-d))]
        self.items.append((depth+.008,0,crease,fold,0.0,alpha,fold))
    def pin(self,p,c=GOLD,r=.09,alpha=1):
        self.dot(p,c,r,alpha)
    def disk(self,p,c,label='',r=.42,depth=.15,rot=(0,0,0),alpha=1,fill=.34,label_size=34):
        """Model signature: colored letter and an open, projected ink circle."""
        if alpha<.002 or r<=0:return
        m=rotation(tuple(rot));f=lambda q:add(p,trans(q,m))
        n=trans(CZ,m);q=step(abs(dot(n,self.depth)),.035,.34)
        h=depth*.08;points=[f((r*x,r*y,h)) for x,y in CIRCLE]
        pp=[self.project(x) for x in points];z=self.project(p)[2]
        # No fill. A/B stay pigment, so these read even behind other planes.
        self.items.append((z,0,[t[:2] for t in pp],c,1.9,alpha*(.48+.30*q),None))
        if label:
            self.text(label,add(p,mul(n,h+.016)),label_size*1.12,c,alpha*q,weight='bold')
    def segment(self,a,b,c=MUTED,width=2,alpha=1,dash=None,sort_depth=None):
        if alpha<.002 or width<=0:return
        aa=self.project(a);bb=self.project(b)
        dep=.5*(aa[2]+bb[2])-.003 if sort_depth is None else sort_depth
        self.items.append((dep,1,aa[:2],bb[:2],c,width,alpha,dash))
    def path(self,points,c=MUTED,width=2,alpha=1,dash=None,arrow=False,progress=1):
        if len(points)<2 or alpha<.002 or progress<=0:return
        n=len(points)-1;p=clamp(progress)*n; m=min(n,math.ceil(p))
        for j in range(m):
            a,b=points[j],vlerp(points[j],points[j+1],clamp(p-j))
            if arrow and j==m-1:
                aa,bb=self.project(a),self.project(b)
                self.items.append((.5*(aa[2]+bb[2])-.003,2,aa[:2],bb[:2],c,width,alpha,None))
            else:self.segment(a,b,c,width,alpha,dash)
    def curve(self,p0,p1,p2,p3,c=MUTED,width=2,alpha=1,progress=1,arrow=False):
        if alpha<.002 or progress<=0:return
        # Sample a real Bezier in the world, then the eye sees its projection.
        M=13;pts=[]
        for j in range(M+1):
            t=j/M;u=1-t
            pts.append(tuple(u**3*a+3*u*u*t*b+3*u*t*t*d+t**3*e for a,b,d,e in zip(p0,p1,p2,p3)))
        self.path(pts,c,width,alpha,arrow=arrow,progress=progress)
    def grid(self,p,nx,ny,spacing=.5,plane='xz',c=GRID,alpha=.65,width=1.12):
        xx=nx*spacing/2;yy=ny*spacing/2
        def point(x,y):
            if plane=='xy':return (p[0]+x,p[1]+y,p[2])
            if plane=='yz':return (p[0],p[1]+x,p[2]+y)
            return (p[0]+x,p[1],p[2]+y)
        for j in range(nx+1):
            x=j*spacing-xx;self.segment(point(x,-yy),point(x,yy),c,width,alpha)
        for j in range(ny+1):
            y=j*spacing-yy;self.segment(point(-xx,y),point(xx,y),c,width,alpha)
    def text(self,s,p,size=33,c=INK,alpha=1,align='center',font='serif',weight='normal',depth_bias=.015):
        if alpha<.002 or not s:return
        a,b,z,k=self.project(p)
        fs=round(size*k*math.sqrt(self.zoom)*4)/4
        family={'serif':'Latin Modern Roman','math':'Latin Modern Math','sans':'Noto Sans'}.get(font,font)
        self.items.append((z+depth_bias,3,str(s),a,b,fs,c,alpha,align,family,weight))
    def ink(self,s,p,plane,size=32,c=INK,alpha=1,align='center',weight='normal',sort_depth=None):
        """Type follows the projected x-/y-directions of the marked surface."""
        if alpha<.002 or not s:return
        x,y,z,k=self.project(p)
        dx=.035
        px,py=self.pos(add(p,trans((dx,0,0),plane)))
        ux,uy=self.pos(add(p,trans((0,-dx,0),plane)))
        m=(128*self.zoom*k*dx)
        mat=((px-x)/m,(py-y)/m,(ux-x)/m,(uy-y)/m)
        if mat[0]*mat[3]-mat[1]*mat[2]<.038:return
        self.items.append((z+.032 if sort_depth is None else sort_depth,7,str(s),x,y,
                          round(size*k*math.sqrt(self.zoom)*4)/4,c,alpha,align,weight,mat))
    def dot(self,p,c=GOLD,r=.057,alpha=1):
        if alpha<.002 or r<=0:return
        x,y,z,k=self.project(p)
        self.items.append((z+.009,4,x,y,r*self.scale*k,c,alpha,False))
    def sphere(self,p,c=GOLD,r=.20,alpha=1):
        if alpha<.002 or r<=0:return
        x,y,z,k=self.project(p)
        self.items.append((z+.03,4,x,y,r*self.scale*k,c,alpha,True))
    def mark(self,p,ok=True,r=.14,alpha=1):
        if alpha<.002:return
        x,y,z,k=self.project(p)
        self.items.append((z+.025,5,x,y,r*self.scale*k,ok,alpha))
    def anchor(self,alpha=1,scale=1,p=(0,0,0)):
        if alpha<.002:return
        self.disk(add(p,(-2.45*scale,0,0)),A,'A',.42*scale,.15*scale,alpha=alpha,label_size=34*scale)
        self.disk(add(p,(2.45*scale,0,0)),B,'B',.42*scale,.15*scale,alpha=alpha,label_size=34*scale)
        self.tile(p,'',GOLD,(.96*scale,.67*scale,.14*scale),alpha=alpha)
    def draw(self):
        g=self.g
        for a in sorted(self.items,key=lambda j:j[0]):
            i=a[1]
            if i==0:
                _,_,ps,co,w,al,fill=a;g.poly(ps,co,w,al,close=True,fill=fill)
            elif i==7:
                _,_,s,x,y,fs,c,al,align,w,mat=a
                ctx=g.c;ctx.save()
                ctx.transform(cairo.Matrix(*mat,x,y))
                g.text(s,0,0,fs,c,al,align,'Latin Modern Roman',w)
                ctx.restore()
            elif i==1:
                _,_,aa,bb,c,w,al,d=a;g.line(*aa,*bb,c,w,al,d)
            elif i==2:
                _,_,aa,bb,c,w,al,_=a;g.arrow(*aa,*bb,c,w,al,11)
            elif i==3:
                _,_,s,x,y,fs,c,al,align,font,w=a;g.text(s,x,y,fs,c,al,align,font,w)
            elif i==4:
                _,_,x,y,r,c,al,solid=a
                g.circle(x,y,r,fill=c,alpha=al)
            else:
                _,_,x,y,r,ok,al=a;g.check(x,y,ok,r,al)
        self.items.clear()
