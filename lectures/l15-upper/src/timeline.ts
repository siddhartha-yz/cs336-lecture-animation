import data from './data/cut.json';
export type CaptionCue=[number,number,string];
type Seam={kind:string;from?:string;mode?:string;origin?:number|[number,number];frames?:number};
export type Shot={
  id:string;frames:number;cues:Record<string,number>;captions:CaptionCue[];
  chapter?:string;title?:string;speech_end?:number;pause_frames?:number;black_head?:number;black_tail?:number;keep_exit?:boolean;
  add_seconds?:number;extended_lead?:number;handoff?:Seam;opens_into?:{id:string;mode:string;origin:number|[number,number]};
};
export const cut=data as unknown as {title:string;fps:number;scenes:Shot[];speed_clamp:[number,number];audioTag?:string};
export const rows=Object.fromEntries(cut.scenes.map(r=>[r.id,r]));
export const atFrame:Record<string,number>={};let end=0;
for(const row of cut.scenes){atFrame[row.id]=end;end+=row.frames;}
export const FRAMES=end;
export function captionAt(captions:CaptionCue[],f:number){
  let a=0,b=captions.length;
  while(a<b){const m=(a+b)>>1;if(captions[m][0]<=f)a=m+1;else b=m;}
  const c=captions[a-1];return c&&f<c[1]?c[2]:null;
}
