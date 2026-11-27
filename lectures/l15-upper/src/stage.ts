export * from './scene/primitives';
import {between,sine,ink_label,rule,GOLD,MUTED,WHITE,YELLOW} from './scene/primitives';
import {Board,clamp,mix,plateSize} from './board';
import anchors from './data/math-anchors.json';
import type {Shot} from './timeline';

export class Beat {
  readonly f:number; readonly fps:number; readonly t:number; readonly d:number; readonly speech:number;
  readonly open:number; readonly close:number; readonly extend:number; readonly extended_lead:number;
  private row:Shot;
  constructor(row:Shot,i:number,fps:number){
    this.row=row;this.f=i;this.fps=fps;this.t=i/fps;this.d=row.frames/fps;
    this.open=(row.black_head??0)/fps;this.close=this.d-(row.black_tail??0)/fps;
    this.speech=(row.speech_end??row.frames)/fps;
    this.extend=row.add_seconds??0;this.extended_lead=row.extended_lead??0;
  }
  at(name:string,otherwise?:number){
    const n=this.row.cues[name];
    if(n!==undefined)return n/this.fps;
    if(otherwise!==undefined)return otherwise;
    throw Error(`${this.row.id} has no cue '${name}'`);
  }
  fade(name:string,span=.5,delay=0,otherwise?:number){
    return 1-(1-clamp((this.t-this.at(name,otherwise)-delay)/Math.max(.001,span)))**3;
  }
  ent(duration=.46,start=0){
    return 1-(1-clamp((this.t-Math.max(start,this.open))/duration))**3;
  }
  gone(d=.40){return this.row.keep_exit?1:sine((this.close-this.t)/d);}
  tick(){return clamp((this.f-Math.round(this.speech*this.fps))/Math.max(1,(this.row.pause_frames??0)-1));}
}
type Pt=readonly [number,number];
type Aperture=number|Pt;
export function layer(g:Board,a=1,dx=0,dy=0,scale=1,pivot:Pt=[800,400],angle=0) {
  return g.layer(a,dx,dy,scale,pivot,angle);
}
export function aperture(g:Board,mode:string,anchor:Aperture,u:number,keepOld=false){
  const c=g.c,z=clamp(u),p=z**3*(z*(6*z-15)+10);
  c.beginPath();
  if(keepOld)c.rect(-5,-5,1610,910);
  if(mode==='iris'){
    if(typeof anchor==='number')throw Error('Iris needs an x,y anchor');
    const [x,y]=anchor,r=Math.hypot(Math.max(x,1600-x),Math.max(y,900-y))+10;
    c.moveTo(x+r*p,y);c.arc(x,y,Math.max(.001,r*p),0,Math.PI*2);
  }else if(mode==='baseline'){
    const y=Number(anchor);c.rect(-5,y-(y+5)*p,1610,910*p);
  }else if(mode==='split'){
    const x=Number(anchor),l=x-(x+5)*p,r=x+(1605-x)*p;c.rect(l,-5,r-l,910);
  }else if(mode==='leaf'){
    const x=mix(-125,1722,p);
    c.moveTo(-5,-5);c.lineTo(x+95,-5);c.lineTo(x-70,905);c.lineTo(-5,905);c.closePath();
  }else c.rect(-5,-5,1610*p,910);
  c.clip(keepOld?'evenodd':'nonzero');
}
// Fade complete Chinese glyphs into place; preserve their shapes throughout.
export function floatHan(g:Board,text:string,x:number,y:number,size:number,u:number,color:string=WHITE,a=1){
  if(!a||u<=0)return;
  const glyphs=Array.from(text),gap=size*.018;
  const widths=glyphs.map(ch=>g.measure(ch,size,'serif')+gap);
  const travel=Math.max(0,glyphs.length-1)*.04;
  const span=1-Math.min(.47,travel);
  let left=x-widths.reduce((v,w)=>v+w,0)/2;
  for(const [i,glyph] of glyphs.entries()){
    const delay=travel?Math.min(.47,travel)*i/(glyphs.length-1):0;
    const u0=clamp((u-delay)/span);
    const on=1-(1-u0)**3;
    g.text(glyph,left+widths[i]/2,y+size*.15*(1-on),size,color,a*on,'center','serif');
    left+=widths[i];
  }
}
export function phase_card(g:Board,b:Beat,number:string,title:string,questionText:string,nextPose?:[string,Aperture,()=>void]){
  // Hold the genuine question, clear every glyph, then reveal the actual native next scene.
  const a=b.ent(.27,.33)*(1-sine(between(b.t,b.d-.79,b.d-.50)));
  if(a){
    floatHan(g,`${number} · ${title}`,800,393,65,(b.t-.34)/.45,WHITE,a);
    const u=b.ent(.59,.37);
    rule(g,800-14*u,460,800+14*u,GOLD,a*u,1.65);
    g.floatLine(questionText,800,522,38,(b.t-.71)/.45,WHITE,a*.91);
  }
  if(nextPose&&b.t>b.d-.45){
    const [mode,anchor,draw]=nextPose,u=between(b.t,b.d-.45,b.d-.05);
    g.c.save();if(u<1)aperture(g,mode,anchor,u);draw();g.c.restore();
  }
}
export function picture(g:Board,name:string,x:number,y:number,w:number,h?:number|null,a=1){
  const file=name.endsWith('.png')?name:`${name}.png`;
  const [iw,ih]=plateSize(file);g.image(file,x,y,w,h??w*ih/iw,a);
}
export function mathform(g:Board,key:string,x:number,y:number,height=55,limit=1360,c:string=WHITE,a=1,p=1,align:'left'|'center'|'right'='center'){
  if(a<=0||p<=0)return;
  const file=`math-${key}.png`,[sw,sh]=plateSize(file);
  const scale=Math.min(height/sh,limit/sw),w=sw*scale,h=sh*scale;
  g.image(file,x-({left:0,center:w/2,right:w}[align]),y-h/2,w,h,a,c,Math.min(1,p));
  return [w,h];
}
export function form_segment(base:string,tag:string,x:number,y:number,height:number,limit:number){
  const [w,h]=plateSize(`math-${base}.png`),s=Math.min(height/h,limit/w);
  const [l,t,r,b]=(anchors as Record<string,number[]>)[tag];
  return [x+(l+r-w)*s/2,y+(t+b-h)*s/2,s];
}
export function move_segment(g:Board,tag:string,source:number[],end:number[],t:number,color:string){
  const [w,h]=plateSize(`math-${tag}-highlight.png`);
  const [x,y,s]=source.map((v,i)=>mix(v,end[i],t));
  const [l,a,r,b]=(anchors as Record<string,number[]>)[tag];
  mathform(g,`${tag}-highlight`,x+(w-l-r)*s/2,y+(h-a-b)*s/2,s*h,s*w,color);
}
