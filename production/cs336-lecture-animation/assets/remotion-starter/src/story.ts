import {PALETTE as P} from './theme/palette';
import {Clock,Stage,ease,mix,type Pose} from './stage';
import {rows,W,H,FPS,type Shot} from './timeline';
import {paintFormat} from './format';

const point2=Math.log(3);
const probabilities=(k:number)=>[k,k+point2].map(z=>Math.exp(z)/(Math.exp(k)+Math.exp(k+point2)));
const model=(g:Stage,b:Clock)=>{
  const {row:r}=b;
  const k=r.id==='shift'?2*b.fade('shift',.76):['q2','guess','cancel'].includes(r.id)?2:0;
  // Cover the output before moving the score. The prediction comes before the reveal.
  const ready=r.id==='shift'?1-ease((b.frame-b.row.cues.shift+26)/20):
    ['q2','guess'].includes(r.id)?0:r.id==='cancel'?b.fade('cancel',.42):1;
  const alpha=r.id==='q1'?b.intro():r.id==='cancel'?b.exit():1;
  const focus=r.id==='cancel'?b.fade('cancel',.45):0;
  const [a0,a1]=probabilities(k);
  for(const [i,p] of [a0,a1].entries()){
    const y=254+380*i,c=i===0?P.lightCyan:P.green;
    g.glass([235,y,430,160],c,alpha);
    g.text(i===0?'A':'B',291,y+82,42,'anchor',{a:alpha,font:'math'});
    g.text((k+i*point2).toFixed(2),481,y+82,59,'number',{a:alpha,font:'math'});
    g.line([710,y+80,1052,y+80],c,2.2,alpha,true);
    // Missing values are honest blanks during the prediction; no separate answer layer.
    if(ready)g.data([1120,y,600*p,160],c,ready*alpha);
    if(ready<1)g.rect([1120,y,450,160],P.gold,2,(1-ready)*alpha,true,true);
    g.text(p.toFixed(2),1120+600*p+43,y+82,47,'number',
      {a:alpha*ready,align:'left',color:c,font:'math'});
    g.text('？',1613,y+82,47,'number',{a:alpha*(1-ready),align:'left',color:P.gold});
  }
  g.text('分数',235,215,28,'anchor',{a:alpha,align:'left'});
  g.text('概率',1120,215,28,'anchor',{a:alpha,align:'left'});
  g.text('pᵢ = exp(zᵢ) / ∑ exp(zⱼ)',960,136,51,'formula',{a:alpha*(1-Math.min(1,focus*2)),font:'math'});
  g.text('e² / e² = 1',960,136,51,'formula',{a:alpha*Math.max(0,2*focus-1),color:P.gold,font:'math'});
  if(r.prompt)g.text(r.prompt,960,842,43,'question',{a:alpha*b.fade('ask'),rise:b.fade('ask')});
  g.countdown(b.frame,r.hold);
};

const paper=(g:Stage,b:Clock)=>{
  const a=b.intro(.45)*b.exit(.24);
  g.paper([285,214,1350,542],a);
  const code=['z = torch.tensor([0., log(3)])','x = torch.stack((z, z + 2))','x.softmax(dim=1)'];
  code.forEach((s,i)=>g.text(s,383,310+76*i,48,'sample',{color:P.bg,a,align:'left',font:'mono'}));
  [0,2].map(probabilities).forEach((row,i)=>{
    const p=row.map(x=>x.toFixed(2)).join(', ');
    const label=i===0?'[['+p+'],':' ['+p+']]';
    g.text(label,383,574+i*64,48,'number',{font:'mono',color:P.bg,align:'left',a:a*b.fade('report',.25)});
  });
  g.text(b.row.paper!.source,1556,716,25,'source',{color:P.bg,a,align:'right'});
};

export function posesFor(r:Shot,f:number):Pose[]{
  const b=new Clock(r,f),g=new Stage();
  if(b.black)return [];
  if(r.kind==='op'||r.kind==='chapter'){
    paintFormat(g,b);
    const out=[g.pose];
    if(r.opens_into){
      const p=ease((f-(r.frames-.45*FPS))/(.40*FPS));
      if(p>0){
        const [x,y]=r.opens_into.origin;
        const radius=p*(Math.hypot(Math.max(x,W-x),Math.max(y,H-y))+2);
        // Native state at literal next frame 0. Cue clock doesn't start in the aperture.
        for(const pose of posesFor(rows[r.opens_into.id],0))out.push({...pose,iris:{x,y,radius}});
      }
    }
    return out;
  }
  if(r.kind==='end'){
    paintFormat(g,b);
    return [g.pose];
  }
  if(r.apparatus==='scores')model(g,b);
  else if(r.apparatus==='softmax-check')paper(g,b);
  else throw Error(`Missing painter for ${r.id} (${r.apparatus})`);
  return [g.pose];
}
