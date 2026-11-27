import {AbsoluteFill,Composition,Folder,Series,getStaticFiles,staticFile,useCurrentFrame,useVideoConfig,
  cancelRender,continueRender,delayRender} from 'remotion';
import {Audio} from '@remotion/media';
import {useEffect,useLayoutEffect,useRef,useState} from 'react';
import {loadAssets,paint} from './draw';
import {posesFor} from './story';
import {PALETTE} from './theme/palette';
import {captionAt,cut,durationInFrames,FPS,H,rows,type Shot,W} from './timeline';

type ShotProps={id:string;showCaps:boolean};
function ShotCanvas({id,showCaps}:ShotProps){
  const f=useCurrentFrame(),{width,height}=useVideoConfig(),row:Shot=rows[id];
  const can=useRef<HTMLCanvasElement>(null),done=useRef(false);
  const [handle]=useState(()=>delayRender('Loading video assets: '+id));
  const [loaded,setLoaded]=useState(false);
  useEffect(()=>{
    let live=true;
    loadAssets().then(()=>{if(live)setLoaded(true);},cancelRender);
    return ()=>{live=false;if(!done.current){continueRender(handle);done.current=true;}};
  },[handle]);
  useLayoutEffect(()=>{
    if(!loaded||!can.current)return;
    try{
      const ctx=can.current.getContext('2d');
      if(!ctx)throw Error('Canvas 2D is required for '+id);
      paint(ctx,posesFor(row,Math.max(0,Math.min(f,row.frames-1))),width,height);
      if(!done.current){continueRender(handle);done.current=true;}
    }catch(e){cancelRender(e instanceof Error?e:Error(String(e)));}
  },[f,id,row,height,width,handle,loaded]);
  const sub=showCaps&&captionAt(row,f);
  return <AbsoluteFill style={{background:PALETTE.bg}}>
    <canvas width={width} height={height} ref={can}/>
    {loaded&&sub&&<AbsoluteFill style={{
      color:PALETTE.white,pointerEvents:'none',justifyContent:'end',alignItems:'center',paddingBottom:height*52/H,
    }}>
      <div style={{fontFamily:'Film Chinese, serif',fontSize:64*width/W,fontWeight:700,whiteSpace:'pre-wrap',
        textAlign:'center',maxWidth:'90%',lineHeight:1.12,textShadow:`0 1px 3px ${PALETTE.bg}`}}>{sub}</div>
    </AbsoluteFill>}
  </AbsoluteFill>;
}

type EditProps={showCaps:boolean;audioMode:'silent'|'mix'|'dialogue'};
function Edit({showCaps,audioMode}:EditProps){
  const name=`audio/${cut.audioTag}/${audioMode}.m4a`;
  if(audioMode!=='silent'&&!getStaticFiles().some(f=>f.name===name))throw Error('Missing audio input: public/'+name);
  return <AbsoluteFill style={{background:PALETTE.bg}}>
    <Series>{cut.scenes.map(s=><Series.Sequence key={s.id} name={s.title??s.id} durationInFrames={s.frames} premountFor={FPS}>
      <ShotCanvas id={s.id} showCaps={showCaps}/>
    </Series.Sequence>)}</Series>
    {audioMode!=='silent'&&<Audio src={staticFile(name)}/>}
  </AbsoluteFill>;
}

export function Root(){
  return <>
    <Composition id="Lecture" component={Edit} durationInFrames={durationInFrames}
      fps={FPS} width={W} height={H} defaultProps={{showCaps:true,audioMode:'silent'}}/>
    <Folder name="Shots">{cut.scenes.map(s=><Composition key={s.id} id={s.id} component={ShotCanvas}
      durationInFrames={s.frames} fps={FPS} width={W} height={H} defaultProps={{id:s.id,showCaps:false}}/>)}</Folder>
  </>;
}
