import dimensions from './data/dimensions.json';
import paths from './data/ink-paths.json';

export const W=1600, H=900;
import {PALETTE} from './theme/palette';
export const clamp=(x:number,lo=0,hi=1)=>Math.max(lo,Math.min(hi,x));
export const mix=(a:number,b:number,t:number)=>a+(b-a)*t;
const parse=(str:string)=>{
  if(!/^#[\da-f]{6}$/i.test(str)) throw Error(`Expected a hex color: ${str}`);
  return [1,3,5].map(i=>parseInt(str.slice(i,i+2),16));
};
const colorCache=new Map<string,number[]>();
const rgb=(c:string)=>{
  let value=colorCache.get(c);
  if(!value){value=parse(c);colorCache.set(c,value);}
  return value;
};
export const blend=(a:string,b:string,f:number)=>'#'+rgb(a).map((v,i)=>Math.round(mix(v,rgb(b)[i],clamp(f))).toString(16).padStart(2,'0')).join('');
type Pt=readonly [number,number];
type Align='left'|'center'|'right';
type Font='sans'|'math'|'serif'|'mono';
type Box=[number,number,number,number];
type Contour=[Pt[],number[]];
type Ink=[Box,Array<[Contour[],number]>];
const inkPaths=paths as unknown as Record<string,Ink>;
const fonts={
  sans:'"Film Latin", "Film Chinese", serif',
  math:'"Film Latin", "Film Chinese", serif',
  serif:'"Film Chinese", "Film Latin", serif',
  mono:'"Film Mono", "Film Chinese", monospace',
};
export type Bitmaps=Record<string,HTMLImageElement>;

export class Board {
  readonly c:CanvasRenderingContext2D;
  private bitmaps:Bitmaps;
  private inkCache=new Map<string,HTMLCanvasElement>();
  constructor(c:CanvasRenderingContext2D,bitmaps:Bitmaps){
    this.c=c; this.bitmaps=bitmaps;
  }

  begin(width:number,height:number){
    const c=this.c;
    c.setTransform(width/W,0,0,height/H,0,0);
    c.globalAlpha=1;c.globalCompositeOperation='source-over';c.setLineDash([]);
    c.lineCap='round';c.lineJoin='round';c.fillStyle=PALETTE.BLACK;
    c.fillRect(0,0,W,H);
  }

  layer(a=1,dx=0,dy=0,scale=1,pivot:Pt=[800,400],angle=0){
    const c=this.c; c.save();c.globalAlpha*=clamp(a);
    if(dx||dy)c.translate(dx,dy);
    if(scale!==1||angle){
      c.translate(...pivot);
      if(angle)c.rotate(angle*Math.PI/180);
      c.scale(scale,scale);
      c.translate(-pivot[0],-pivot[1]);
    }
    return ()=>c.restore();
  }

  private paint(color:string,a:number,stroke=false,w=1){
    const c=this.c;
    c.save();
    c.globalAlpha*=clamp(a);
    if(stroke){c.strokeStyle=color;c.lineWidth=w;c.stroke();}
    else{c.fillStyle=color;c.fill();}
    c.restore();
  }

  rect(x:number,y:number,w:number,h:number,fill:string|null=null,stroke:string|null=null,width=2,r=0,alpha=1){
    if(w<=0||h<=0||alpha<=0)return;
    const c=this.c;c.beginPath();
    if(r)c.roundRect(x,y,w,h,Math.min(w/2,h/2,r));else c.rect(x,y,w,h);
    if(fill)this.paint(fill,alpha);
    if(stroke&&width)this.paint(stroke,alpha,true,width);
  }

  circle(x:number,y:number,r:number,fill:string|null=null,stroke:string|null=null,width=2,alpha=1){
    if(r<=0||alpha<=0)return;
    const c=this.c;c.beginPath();c.arc(x,y,r,0,Math.PI*2);
    if(fill)this.paint(fill,alpha);
    if(stroke&&width)this.paint(stroke,alpha,true,width);
  }

  line(x1:number,y1:number,x2:number,y2:number,color:string=PALETTE.WHITE,width=2,alpha=1,dash?:number[]){
    if(alpha<=0||width<=0)return;
    const c=this.c;c.beginPath();c.moveTo(x1,y1);c.lineTo(x2,y2);
    if(dash){c.save();c.setLineDash(dash);}
    this.paint(color,alpha,true,width);
    if(dash)c.restore();
  }

  poly(points:readonly Pt[],color:string=PALETTE.WHITE,width=2,alpha=1,close=false,fill:string|null=null,fillA=1){
    if(alpha<=0||points.length<2)return;
    const c=this.c;
    c.beginPath();c.moveTo(...points[0]); for(const p of points.slice(1))c.lineTo(...p);
    if(close)c.closePath();
    if(fill)this.paint(fill,alpha*fillA);
    if(color&&width>0)this.paint(color,alpha,true,width);
  }

  arrow(x1:number,y1:number,x2:number,y2:number,color:string=PALETTE.MUTED,width=2,alpha=1,head=11){
    const dx=x2-x1,dy=y2-y1,d=Math.hypot(dx,dy);
    if(d<.01||alpha<=0)return;
    this.line(x1,y1,x2,y2,color,width,alpha);
    const p=Math.atan2(dy,dx), k=Math.min(d*.45,head);
    this.poly([[x2-k*Math.cos(p-.51),y2-k*Math.sin(p-.51)],[x2,y2],
      [x2-k*Math.cos(p+.51),y2-k*Math.sin(p+.51)]],color,width,alpha);
  }

  arc(x:number,y:number,r:number,a:number,b:number,color:string=PALETTE.WHITE,width=2,alpha=1){
    if(alpha<=0||r<=0)return;
    this.c.beginPath();this.c.arc(x,y,r,a,b);this.paint(color,alpha,true,width);
  }

  check(x:number,y:number,ok=true,r=15,a=1){
    const w=Math.max(2,r*.16);
    if(ok)this.poly([[x-r*.63,y],[x-r*.17,y+r*.53],[x+r*.83,y-r*.57]],PALETTE.GREEN,w,a);
    else {
      this.line(x-r*.65,y-r*.65,x+r*.65,y+r*.65,PALETTE.RED,w,a);
      this.line(x-r*.65,y+r*.65,x+r*.65,y-r*.65,PALETTE.RED,w,a);
    }
  }

  private face(font:Font,weight:string) {
    return `${weight==='bold'?700:weight==='medium'?500:400} 128px ${fonts[font]??font}`;
  }

  measure(s:unknown,size=36,font:Font='sans',weight='normal'){
    this.c.font=this.face(font,weight);
    const m=this.c.measureText(String(s??''));
    return (m.actualBoundingBoxLeft+m.actualBoundingBoxRight || m.width)*size/128;
  }

  text(s:unknown,x:number,y:number,size=36,color:string=PALETTE.WHITE,a=1,align:Align='center',font:Font='sans',weight='normal'){
    if(!s||a<=0||size<=0)return;
    const c=this.c;c.save();c.translate(x,y);c.scale(size/128,size/128);
    c.font=this.face(font,weight);
    c.textBaseline='alphabetic';c.textAlign='left';c.globalAlpha*=clamp(a);c.fillStyle=color;
    const str=String(s),m=c.measureText(str),w=m.actualBoundingBoxLeft+m.actualBoundingBoxRight || m.width;
    c.fillText(str,m.actualBoundingBoxLeft-({left:0,center:w/2,right:w}[align]),
      (m.actualBoundingBoxAscent-m.actualBoundingBoxDescent)/2);
    c.restore();
  }

  rawText(...args:Parameters<Board['text']>){this.text(...args);}

  rawRun(parts:readonly (readonly [string,string])[],x:number,y:number,size:number,font:Font='mono'){
    const c=this.c;
    c.save();c.translate(x,y);c.scale(size/128,size/128);
    c.font=this.face(font,'normal');c.textBaseline='alphabetic';c.textAlign='left';
    const m=c.measureText(parts.map(([s])=>s).join(''));
    const baseline=(m.actualBoundingBoxAscent-m.actualBoundingBoxDescent)/2;
    let prefix='';
    for(const [s,color] of parts){
      c.fillStyle=color;
      c.fillText(s,c.measureText(prefix).width,baseline);
      prefix+=s;
    }
    c.restore();
  }

  // The entire line defines the baseline. Punctuation keeps its advance and
  // its native position; inking each glyph around its own centre erases both.
  floatLine(s:string,x:number,y:number,size:number,u:number,color:string,a=1){
    if(!s||a<=0||u<=0)return;
    const c=this.c;
    c.save();c.translate(x,y);c.scale(size/128,size/128);
    c.font=this.face('serif','normal');
    c.textBaseline='alphabetic';c.textAlign='left';c.fillStyle=color;
    const line=c.measureText(s),left=-line.width/2;
    const baseline=(line.actualBoundingBoxAscent-line.actualBoundingBoxDescent)/2;
    const alpha=c.globalAlpha*clamp(a);
    if(u>=1){
      c.globalAlpha=alpha;
      c.fillText(s,left,baseline);
    }else{
      const start=Math.min(.47,Math.max(0,Array.from(s).length-1)*.04);
      const glyphs=Array.from(s);
      let prefix='';
      for(const [i,ch] of glyphs.entries()){
        const delay=start*i/Math.max(1,glyphs.length-1);
        const on=1-(1-clamp((u-delay)/(1-start)))**3;
        if(on){
          c.globalAlpha=alpha*on;
          c.fillText(ch,left+c.measureText(prefix).width,baseline+128*.15*(1-on));
        }
        prefix+=ch;
      }
    }
    c.restore();
  }

  image(name:string,x:number,y:number,w:number,h:number,a=1,tint?:string,reveal=1){
    if(a<=0||reveal<=0)return;
    const img=this.bitmaps[name];
    if(!img)throw Error(`Missing drawing plate ${name}`);
    const c=this.c;c.save();c.globalAlpha*=clamp(a);
    if(reveal<1){c.beginPath();c.rect(x-1,y-1,w*reveal+2,h+2);c.clip();}
    let plate:CanvasImageSource=img;
    if(tint){
      const id=`${name}:${tint}`;
      let stamp=this.inkCache.get(id);
      if(!stamp){
        stamp=document.createElement('canvas');stamp.width=img.naturalWidth;stamp.height=img.naturalHeight;
        const q=stamp.getContext('2d')!;
        q.drawImage(img,0,0);q.globalCompositeOperation='source-in';q.fillStyle=tint;
        q.fillRect(0,0,stamp.width,stamp.height);
        this.inkCache.set(id,stamp);
      }
      plate=stamp;
    }
    c.drawImage(plate,x,y,w,h);c.restore();
  }

  write_text(s:string,x:number,y:number,size:number,color:string,a:number,p:number,mode='pen'){
    if(p<=0||a<=0)return;
    const data=inkPaths[s];
    if(!data){
      if(p>=1){this.text(s,x,y,size,color,a,'center','serif');return;}
      // An edited phrase remains readable without regenerating title contours.
      const w=this.measure(s,size,'serif');
      this.c.save();this.c.beginPath();this.c.rect(x-w/2-2,y-size,w*p+4,2*size);this.c.clip();
      this.text(s,x,y,size,color,a,'center','serif');this.c.restore();
      return;
    }
    const [[left,top,w,h],groups]=data;
    const c=this.c;c.save();c.translate(x,y);c.scale(size/128,size/128);c.translate(-left-w/2,-top-h/2);
    for(let i=0;i<groups.length;i++){
      const [contours,len]=groups[i],u=clamp((p-.38*i/Math.max(1,groups.length-1))/.62);
      if(!u)continue;
      const glow=mode==='wave'?1-(1-u)**3:clamp((u-.46)/.54);
      if(glow){
        c.beginPath();
        for(const [pts] of contours){c.moveTo(...pts[0]);for(const q of pts.slice(1))c.lineTo(...q);c.closePath();}
        this.paint(color,a*glow);
      }
      if(mode==='pen'&&u<1){
        let budget=len*Math.min(1,u/.68);c.beginPath();
        for(const [pts,ls] of contours){
          if(budget<=0)break;
          c.moveTo(...pts[0]);
          let j=1;while(j<ls.length&&ls[j]<=budget){c.lineTo(...pts[j]);j++;}
          if(j<ls.length){
            const z=(budget-ls[j-1])/Math.max(.001,ls[j]-ls[j-1]);
            c.lineTo(mix(pts[j-1][0],pts[j][0],z),mix(pts[j-1][1],pts[j][1],z));
          }
          budget-=ls.at(-1)!;
        }
        this.paint(color,a*(1-.85*glow),true,132/size);
      }
    }
    c.restore();
  }
}
export const plateSize=(name:string):[number,number]=>{
  const res=(dimensions as Record<string,number[]>)[name];
  if (!res)throw Error(`Unknown plate ${name}`);
  return [res[0],res[1]];
};
