import raw from './data/cut.json';

export type Caption=[from:number,to:number,sub:string];
export type ShotKind='body'|'question'|'op'|'chapter'|'end';
export type Hold={kind:'prediction'|'blind';start:number;frames:number};
export type Shot={
  id:string;kind:ShotKind;frames:number;title?:string;chapter?:string;captions:Caption[];cues:Record<string,number>;
  apparatus?:string;stableFrames?:number[];paper?:{source:string;ref:string};
  layout?:'sample-text';
  handoff?:{kind:'carry'|'reset'|'gate';from:string};
  black_head?:number;black_tail?:number;
  opens_into?:{id:string;origin:[number,number]};
  prompt?:string;hold?:Hold;
  examples?:{cue:string;title:string}[];
  beats?:{cue:string;wordFrame:number;kind:'number'|'highlight'}[];
};
export type Cut={
  title:string;lecture:number;fps:60;
  format:'pilot'|'engineering'|'derivation';demo:boolean;
  audioTag:string;speed_clamp:[number,number];scenes:Shot[];
};
export const cut=raw as unknown as Cut;
export const W=1920,H=1080,FPS=60,ART_BOTTOM=890;
export const FORMAT_EXEMPT=new Set<ShotKind>(['op','chapter','end']);
export const rows=Object.fromEntries(cut.scenes.map(s=>[s.id,s]));
export const starts:Record<string,number>={};let n=0;
for(const s of cut.scenes){starts[s.id]=n;n+=s.frames;}
export const durationInFrames=n;
export const captionAt=(s:Shot,f:number)=>s.captions.find(([a,b])=>a<=f&&f<b)?.[2];
