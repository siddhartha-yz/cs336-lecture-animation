import {PALETTE as P,PAPER_EDGE} from './theme/palette';
import {FPS,type Shot} from './timeline';

export type Bounds=[x:number,y:number,w:number,h:number];
export type TextRole='formula'|'number'|'anchor'|'sample'|'gloss'|'source'|'question'|'format';
type Font='serif'|'math'|'mono';
// Formats may supply their own ink. Body colors are checked from rendered marks.
type Ink=string;
type Rect={kind:'rect';box:Bounds;fill?:Ink;line?:Ink|typeof PAPER_EDGE;st:number;a:number;main?:boolean;dashed?:boolean;material?:'data'|'glass'|'paper'};
type Line={kind:'line';dots:[number,number,number,number];color:Ink;st:number;a:number;arrow?:boolean};
type Arc={kind:'arc';x:number;y:number;r:number;t:number;color:Ink;st:number;a:number;timer:boolean};
export type Text={kind:'text';value:string;x:number;y:number;size:number;role:TextRole;color:Ink;a:number;align:'left'|'center'|'right';font:Font;rise:number};
type Plate={kind:'plate';id:string;box:Bounds;a:number;main:boolean;role:'formula'|'source'};
export type Mark=Rect|Line|Arc|Text|Plate;
export type Camera={scale:number;dx:number;dy:number;pivot:[number,number]};
export type Pose={marks:Mark[];iris?:{x:number;y:number;radius:number};camera?:Camera};

export const clamp=(x:number)=>Math.min(1,Math.max(0,x));
export const ease=(x:number)=>{const u=clamp(x);return u*u*(3-2*u);};
export const mix=(a:number,b:number,t:number)=>a+(b-a)*t;

export class Clock {
  constructor(readonly row:Shot,readonly frame:number){}
  get head(){return this.row.black_head??0;}
  get tail(){return this.row.frames-(this.row.black_tail??0);}
  get black(){return this.frame<this.head||this.frame>=this.tail;}
  intro(seconds=.4){return ease((this.frame-this.head)/(seconds*FPS));}
  exit(seconds=.3){return ease((this.tail-this.frame)/(seconds*FPS));}
  fade(cue:string,seconds=.45){
    const f=this.row.cues[cue];
    if(f===undefined)throw Error(this.row.id+': unknown cue '+cue);
    return ease((this.frame-f)/(seconds*FPS));
  }
  get remaining(){return this.row.frames-this.frame;}
}
export class Stage {
  readonly pose:Pose={marks:[]};
  get items(){return this.pose.marks;}
  camera(scale:number,dx=0,dy=0,pivot:Camera['pivot']=[960,450]){
    this.pose.camera={scale,dx,dy,pivot};
  }
  rect(box:Bounds,line:Ink=P.axis,width=2,a=1,main=false,dashed=false){
    if(a>0)this.items.push({kind:'rect',box,line,st:width,a,main,dashed});
  }
  data(box:Bounds,fill:Ink,a=1){
    if(a>0)this.items.push({kind:'rect',box,fill,line:P.white,st:1.25,a,main:true,material:'data'});
  }
  glass(box:Bounds,fill:Ink,a=1){
    if(a>0)this.items.push({kind:'rect',box,fill,line:fill,st:2,a,main:true,material:'glass'});
  }
  paper(box:Bounds,a=1){
    if(a>0)this.items.push({kind:'rect',box,fill:P.paper,line:PAPER_EDGE,st:1,a,main:true,material:'paper'});
  }
  plate(id:string,box:Bounds,role:Plate['role'],a=1,main=false){
    if(a>0)this.items.push({kind:'plate',id,box,a,main,role});
  }
  line(dots:Line['dots'],color:Ink=P.axis,st=2,a=1,arrow=false){
    if(a>0)this.items.push({kind:'line',dots,color,st,a,arrow});
  }
  text(value:string,x:number,y:number,size:number,role:TextRole,
       {color=P.white,a=1,align='center',font='serif',rise=1}:
       Partial<Pick<Text,'color'|'a'|'align'|'font'|'rise'>>={}){
    if(a>0&&rise>0&&value)this.items.push({kind:'text',value,x,y,size,role,color,a,align,font,rise});
  }
  countdown(frame:number,hold:Shot['hold'],y=843){
    if(!hold||frame<hold.start||frame>=hold.start+hold.frames)return;
    const t=(frame-hold.start+1)/hold.frames;
    this.items.push({kind:'arc',x:960,y,r:34,t:1,color:P.axis,st:1.4,a:1,timer:false});
    this.items.push({kind:'arc',x:960,y,r:34,t,color:P.gold,st:4.2,a:1,timer:true});
  }
}
