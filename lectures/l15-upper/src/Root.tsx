import {Composition,Folder,Still} from 'remotion';
import {Edit} from './Edit';
import {ShotClip} from './Scenes';
import {Cover} from './Cover';
import {cut, FRAMES} from './timeline';
const size={width:1920,height:1080,fps:cut.fps} as const;
export const Root=()=> <>
  <Composition id="Lecture15Upper" component={Edit} durationInFrames={FRAMES}
    {...size} defaultProps={{showCaps:true,audioMode:'mix'}}/>
  <Still id="Cover" component={Cover} width={1920} height={1080}/>
  <Folder name="Shots">
    {cut.scenes.map(r=><Composition key={r.id} id={r.id} component={ShotClip}
      durationInFrames={r.frames} {...size} defaultProps={{id:r.id,showCaps:false}}/>)}
  </Folder>
</>;
