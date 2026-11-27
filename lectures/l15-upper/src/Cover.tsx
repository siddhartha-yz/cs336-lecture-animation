import {AbsoluteFill,delayRender,continueRender,cancelRender,staticFile,useVideoConfig} from 'remotion';
import {useEffect,useRef,useState} from 'react';
import {Board,H,W} from './board';
import {PALETTE} from './theme/palette';
import {loadBoardAssets} from './Scenes';
import {MODEL_C,role_pose,SIZE_PROFILE} from './scene/ppo';
import cover from './data/cover.json';

const {WHITE,BLACK}=PALETTE;

function head(g:Board,text:string,x:number,y:number,size:number,color:string){
  const c=g.c;
  c.save();
  c.font=`700 ${size}px "Cover Song", serif`;
  c.textBaseline='alphabetic';
  c.textAlign='left';
  c.fillStyle=color;
  const m=c.measureText(text);
  c.fillText(text,x+m.actualBoundingBoxLeft,y+(m.actualBoundingBoxAscent-m.actualBoundingBoxDescent)/2);
  c.restore();
}

function compactRole(g:Board,i:2|3,name:string){
  const [x,y,baseW,baseH,d]=role_pose(i,0);
  const factor=SIZE_PROFILE[i],w=baseW*factor,h=baseH*factor,step=d*.28*factor,c=MODEL_C[i];
  g.rect(x-3,y-2*step-3,w+2*step+6,h+2*step+6,BLACK);
  for(const k of [2,1])g.rect(x+k*step,y-k*step,w,h,null,c,1.15*factor,0,k===2?.22:.43);
  g.rect(x,y,w,h,c,null,0,0,.38);
  g.rect(x,y,w,h,null,c,1.85);
  g.text(name,x+w/2,y+h*.40,37,WHITE,1,'center','math');
  g.text('冻结',x+w/2,y+h*.74,24,WHITE,1,'center','serif');
}

export function Cover(){
  const canvas=useRef<HTMLCanvasElement>(null);
  const {width,height}=useVideoConfig();
  const [h]=useState(()=>delayRender('Cover artwork and fonts'));
  useEffect(()=>{
    const art=new Image();
    art.src=staticFile(cover.artwork);
    const bold=new FontFace('Cover Song',`url(${staticFile('fonts/noto-serif-sc-cover-bold.woff')})`,{weight:'700'});
    Promise.all([loadBoardAssets(),art.decode(),bold.load()]).then(([assets,,font])=>{
      if(!canvas.current)return;
      document.fonts.add(font);
      const g=new Board(canvas.current.getContext('2d',{alpha:false})!,assets);
      g.begin(width,height);
      const restore=g.layer(1,W*cover.shiftX,H*cover.shiftY,cover.scale,[W/2,H/2]);
      g.c.imageSmoothingQuality='high';
      g.c.drawImage(art,0,0,W,H);
      // At 14:41 the rig is at its final unsplit pose. Adapt only the two
      // frozen labels and the threshold ink for thumbnail scale.
      compactRole(g,2,'Ref');
      compactRole(g,3,'RM');
      g.line(1165,397,1377,397,cover.coral,3.5,1,[7,6]);
      g.rect(1393,353,75,37,BLACK);
      g.text('上限',1396,374,28,cover.coral,1,'left','serif');
      restore();
      head(g,cover.headline,95,124,105,WHITE);
      head(g,cover.subtitle,95,218,49,cover.coral);
      continueRender(h);
    }).catch(cancelRender);
  },[h,width,height]);
  return <AbsoluteFill style={{background:BLACK}}>
    <canvas ref={canvas} width={width} height={height} style={{width:'100%',height:'100%'}}/>
  </AbsoluteFill>;
}
