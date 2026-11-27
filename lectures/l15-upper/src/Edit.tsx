import {AbsoluteFill,Series,getStaticFiles,staticFile,useVideoConfig} from 'remotion';
import {Audio} from '@remotion/media';
import {ShotClip} from './Scenes';
import {PALETTE} from './theme/palette';
import {cut} from './timeline';

export type EditProps={showCaps:boolean;audioMode:'mix'|'dialogue'|'silent'};

export const audioFile=(name:string)=>`audio/${cut.audioTag?`${cut.audioTag}/`:''}${name}.m4a`;
export const availableAudio=(name:string)=>getStaticFiles().some(f=>f.name===audioFile(name));

export function Edit({showCaps,audioMode}:EditProps){
  const {fps}=useVideoConfig();
  return <AbsoluteFill style={{background:PALETTE.BLACK}}>
    <Series>
      {cut.scenes.map(row=>(
        <Series.Sequence key={row.id} durationInFrames={row.frames} premountFor={fps}
          name={`${row.id} · ${row.title??row.chapter??'片名'}`}>
          <ShotClip id={row.id} showCaps={showCaps}/>
        </Series.Sequence>
      ))}
    </Series>
    {audioMode!=='silent'&&availableAudio(audioMode)?<Audio src={staticFile(audioFile(audioMode))}/>:null}
  </AbsoluteFill>;
}
