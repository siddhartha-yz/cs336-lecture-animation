import {AbsoluteFill, cancelRender, continueRender, delayRender, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {useEffect,useLayoutEffect,useRef,useState} from 'react';
import {Board,clamp,type Bitmaps} from './board';
import {PALETTE} from './theme/palette';
import {Beat, aperture, layer, phase_card} from './stage';
import policy from './data/visual-policy.json';
import {cut,rows,captionAt,type Shot} from './timeline';
import * as A from './scene/opening';
import * as B from './scene/engineering';
import * as C from './scene/packing';
import * as D from './scene/preference';
import * as E from './scene/ppo';
import dims from './data/dimensions.json';

type Paint=(g:Board,b:Beat)=>void;
export const painters:Record<string,Paint>={
  c01:A.intro,c02:A.records,c03:A.question0,title:A.opener_title,c04:A.flan,c05:A.evolution,c06:A.style,
  c07:A.lima,c08:A.blind_spot,c09:A.safety_and_mid,c10:A.loss_mask,c11:A.question1,c12:B.source_example,
  c13:B.test_code,c14:B.frozen,c15:C.padding,c16:C.packing,c17:C.mask_frame,c18:B.question2,
  c19:D.mimic,c20:D.landscape,c21:D.gv_gap,c22:D.compare_pair,c23:D.rm_loss,c24:D.blind_test,
  c25:D.judge,c26:D.goodhart,c27:D.question3,c28:E.kl_tether,c29:E.innocuous,c30:E.memory,c31:E.rollout,
  c32:E.critic,c33:E.goal,c34:E.hook,
};
const questions:Record<string,[string,string,string]>={
  card2:['二','工业微调的硬门槛','把微调搬进产线，工程上卡在哪两道关口？'],
  card3:['三','超越模仿的上限','光靠模仿标准答案，模型还能变得更强吗？'],
  card4:['四','橡皮筋与四模型泥潭','如何拴住策略不跑偏？代价又是什么？'],
};

export function drawClean(g:Board,shot:Shot,f:number,fps:number){
  if(f<(shot.black_head??0)||f>=shot.frames-(shot.black_tail??0))return;
  const b=new Beat(shot,f,fps);
  const q=questions[shot.id];
  if(q){
    const r=shot.opens_into;
    phase_card(g,b,...q,r?[r.mode,r.origin,()=>drawClean(g,rows[r.id],0,fps)]:undefined);
    return;
  }
  const normalTail=shot.speech_end!==undefined&&!shot.pause_frames&&
    !policy.formatExempt.includes(shot.id)&&!policy.questionLeads.includes(shot.id);
  const u=normalTail?clamp((f-(shot.speech_end??0)-7)/Math.max(1,(shot.frames-(shot.speech_end??0)-8))):0;
  const carry=shot.handoff?.kind==='pose'&&shot.handoff?.from&&
    !policy.formatExempt.includes(shot.handoff.from)&&!policy.questionLeads.includes(shot.handoff.from)
    ?(1-clamp(f/(.40*fps)))**3:0;
  const camera=1+.028*(u*u*(3-2*u)+carry);
  const restore=layer(g,shot.id==='c17'?b.gone():1,0,0,camera,[800,443]);
  try{painters[shot.id](g,b);}finally{restore();}
  if(shot.id==='title'&&shot.opens_into&&b.t>=b.d-.36){
    const {id,mode,origin}=shot.opens_into;
    g.c.save();
    aperture(g,mode,origin,clamp((b.t-b.d+.36)/.33));
    try{drawClean(g,rows[id],0,fps);}finally{g.c.restore();}
  }

}

export function drawFrame(g:Board,shot:Shot,f:number,fps:number){
  drawClean(g,shot,f,fps);
  const seam=shot.handoff;
  if(seam?.kind!=='edge'||f>=seam.frames!||!seam.from)return;
  const old=rows[seam.from];
  const c=g.c;c.save();
  if(f)aperture(g,seam.mode??'left',seam.origin??0,f/seam.frames!,true);
  g.rect(0,0,1600,900,PALETTE.BLACK);
  drawClean(g,old,old.frames-1,fps);
  c.restore();
}

let assets:Promise<Bitmaps>|undefined;
export function loadBoardAssets(){
  assets??=Promise.all([
    ...([
      ['Film Chinese','noto-serif-sc.woff'],
      ['Film Latin','latin-modern.otf'],
      ['Film Mono','mono.ttf'],
    ] as const).map(async ([family,file])=>{
      const font=await new FontFace(family,`url(${staticFile(`fonts/${file}`)})`).load();
      document.fonts.add(font);
    }),
    ...Object.keys(dims).map(async file=>{
      const img=new Image();img.src=staticFile(`plates/${file}`);await img.decode();
      return [file,img] as const;
    }),
  ]).then(values=>Object.fromEntries(values.filter(Boolean) as [string,HTMLImageElement][]));
  return assets;
}

function Caption({text}:{text:string}){
  const {width,height}=useVideoConfig();
  return <AbsoluteFill style={{color:PALETTE.WHITE,alignItems:'center',justifyContent:'end',pointerEvents:'none',paddingBottom:height/20}}>
    <div style={{fontFamily:'Film Chinese, serif',fontSize:width*(64/1920),fontWeight:700,textAlign:'center',
      whiteSpace:'pre-wrap',lineHeight:1.12,maxWidth:'91%',textShadow:`0 1px 3px ${PALETTE.BLACK}, 0 0 2px ${PALETTE.BLACK}`}}>{text}</div>
  </AbsoluteFill>;
}

export function ShotClip({id,showCaps=true}:{id:string;showCaps?:boolean}){
  const shot=rows[id];
  const raw=useCurrentFrame(),f=Math.max(0,Math.min(shot.frames-1,raw));
  const {width,height,fps}=useVideoConfig();
  const canvas=useRef<HTMLCanvasElement>(null),board=useRef<Board|null>(null);
  const [images,setImages]=useState<Bitmaps|null>(null);
  const [handle]=useState(()=>delayRender(`Preparing ${id}`));
  const completed=useRef(false);
  useEffect(()=>{
    let registered=true;
    loadBoardAssets().then(a=>{if(registered)setImages(a);},cancelRender);
    return ()=>{
      registered=false;
      if(!completed.current){continueRender(handle);completed.current=true;}
    };
  },[handle]);

  useLayoutEffect(()=>{
    if(!images||!canvas.current)return;
    try {
      board.current??=new Board(canvas.current.getContext('2d',{alpha:false})!,images);
      board.current.begin(width,height);
      drawFrame(board.current,shot,f,fps);
      if(!completed.current){continueRender(handle);completed.current=true;}
    } catch(e) {cancelRender(e instanceof Error?e:new Error(String(e)));}
  },[images,shot,f,width,height,fps,handle]);
  const text=showCaps&&images?captionAt(shot.captions,f):null;
  return <AbsoluteFill style={{background:PALETTE.BLACK}}>
    <canvas ref={canvas} width={width} height={height} style={{width:'100%',height:'100%',display:'block'}}/>
    {text?<Caption text={text}/>:null}
  </AbsoluteFill>;
}

export const fps=cut.fps;
