// OP, post-question chapter and END are the only format exceptions.
import {PALETTE as P} from './theme/palette';
import {cut,FPS} from './timeline';
import {Clock,Stage,ease} from './stage';

export function paintFormat(g:Stage,b:Clock){
  const r=b.row;
  if(r.kind==='end'){
    g.text('CS336',960,436,56,'format',{font:'math',a:b.intro()*b.exit(.78)});
    return;
  }
  const op=r.kind==='op';
  const u=ease((b.frame-.34*FPS)/(.45*FPS));
  const a=u*(1-ease((b.frame-(r.frames-.79*FPS))/(.29*FPS)));
  if(op){
    for(let i=0;i<5;i++){
      const h=32+i*29;
      g.data([196+39*i-78*b.frame/r.frames,222-h,34,h],i===4?P.gold:P.cyan,a*.24);
      g.data([1570+38*i-78*b.frame/r.frames,915-h*.75,34,h*.75],i%2?P.purple:P.green,a*.24);
    }
  }
  g.text(op?'CS336 Lecture '+cut.lecture:r.title!,960,463,72,'format',
    {a,rise:u,font:op?'math':'serif'});
  const q=ease((b.frame-.70*FPS)/(.45*FPS));
  g.text(op?cut.title:r.prompt!,960,625,op?76:42,'format',{a,rise:q,color:op?P.gold:P.white});
}

