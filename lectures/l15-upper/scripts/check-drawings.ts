import assert from 'node:assert/strict';
import {drawFrame} from '../src/Scenes';
import {rows,cut,atFrame,FRAMES,captionAt,type Shot} from '../src/timeline';
import policy from '../src/data/visual-policy.json';
import {PALETTE} from '../src/theme/palette';
import * as math from '../src/scene/examples';
import {role_pose,SIZE_PROFILE} from '../src/scene/ppo';
import {blockInk} from '../src/stage';
import type {Board} from '../src/board';

const ctx={save(){},restore(){},beginPath(){},rect(){},clip(){},moveTo(){},lineTo(){},closePath(){},arc(){},setLineDash(){}};
const finite=(...a:unknown[])=>assert.ok(a.every(x=>Number.isFinite(x)),JSON.stringify(a));
let opacity=1,dx=0,dy=0,scale=1;
type Geometry={x:number;y:number;size:number};
const screen=new Map<string,Geometry>();
let yEdge=0,subject:Shot,start=0,captions='';const paperStarts=new Map<string,number>();
const painted=new Set<string>();
const words=(s:unknown,x:number,y:number,size:number,a=1,raw=false,glossary=false)=>{
  finite(x,y,size);
  if(!s||opacity*a<=1e-9)return;
  const text=String(s).trim();
  if(!text)return;
  painted.add(text);
  if(opacity*a<.13)return;
  const yScreen=dy+y*scale;
  const height=scale*size*.40;
  yEdge=Math.max(yEdge,yScreen+height);
  const han=(text.match(/\p{Script=Han}/gu)??[]).length;
  if(raw||!han)return;
  assert.ok(han<=(glossary?16:policy.maxHanInSentence),`Long screen string: ${text}`);
  const xScreen=dx+x*scale;
  screen.set(`${text}:${Math.round(xScreen/18)}:${Math.round(yScreen/18)}`,{x:xScreen,y:yScreen,size:han});
};
const board={
  c:ctx,
  layer(a=1,x=0,y=0,k=1,pivot=[800,400]) {
    const old=[opacity,dx,dy,scale];
    opacity*=a;dx+=scale*(x+pivot[0]*(1-k));dy+=scale*(y+pivot[1]*(1-k));scale*=k;
    return ()=>{[opacity,dx,dy,scale]=old;};
  },
  line(x:number,y:number,b:number,c:number){finite(x,y,b,c);},
  rect(x:number,y:number,w:number,h:number,fill?:string,_?:string,_w?:number,r=0,a=1){
    finite(x,y,w,h);
    if(opacity*a>=.13&&fill===PALETTE.PAPER&&subject&&!policy.formatExempt.includes(subject.id)&&!paperStarts.has(subject.id))
      paperStarts.set(subject.id,start);
    if(!policy.formatExempt.includes(subject.id))assert.ok(r<4,'rounded rectangle');
  },
  circle(x:number,y:number,r:number){finite(x,y,r);},
  arrow(x:number,y:number,b:number,c:number){finite(x,y,b,c);},
  poly(a:number[][]){for(const p of a)finite(...p);},
  arc(x:number,y:number,r:number,a:number,b:number){finite(x,y,r,a,b);},
  image(name:string,x:number,y:number,w:number,h:number,a=1){
    finite(x,y,w,h);
    if(opacity*a>=.13&&name.startsWith('math-'))yEdge=Math.max(yEdge,dy+(y+h)*scale);
  },
  measure(s:unknown,size=36){return String(s??'').length*size*.7;},
  text(s:string,x:number,y:number,size:number,color:string,a=1){words(s,x,y,size,a,false,color===PALETTE.MUTED);},
  rawText(s:string,x:number,y:number,size:number,color:string,a=1){words(s,x,y,size,a,true);},
  rawRun(parts:[string,string][],x:number,y:number,size:number){words(parts.map(p=>p[0]).join(''),x,y,size,1,true);},
  write_text(_:string,x:number,y:number,size:number){finite(x,y,size);},
  floatLine(s:string,x:number,y:number,size:number,u:number,_color:string,a=1){
    if(u>=1)words(s,x,y,size,a,true);
  },
  check(x:number,y:number){finite(x,y);},
} as unknown as Board;
if(process.argv.includes('--release')){
  assert.equal(FRAMES,62284);
  assert.equal(cut.scenes.length,38);
  assert.equal(atFrame.c04,atFrame.title+5*cut.fps,'OP should open directly into the first paper');
  assert.deepEqual(cut.scenes.filter(r=>r.chapter).map(r=>r.id),['c01','c04','card2','card3','card4']);
  assert.equal(rows.c10.handoff?.kind,'clean','Mid-training and SFT must never composite');
  assert.ok(!rows.c09.keep_exit);
  assert.equal(rows.c09.black_tail!+rows.c10.black_head!+1,24,'Keep the 0.4s stage reset');
}
assert.equal(Object.keys(rows).length,cut.scenes.length,'Repeated shot id');
for(const id of policy.unrelatedResets){
  const next=rows[id],seam=next.handoff;
  assert.equal(seam?.kind,'clean',id+' begins a new apparatus');
  const previous=rows[seam!.from!];
  assert.ok(!previous.keep_exit&&atFrame[previous.id]+previous.frames===atFrame[id],id+' outgoing board did not release');
  const quiet=(previous.black_tail??0)+(next.black_head??0);
  assert.ok(quiet>=.4*cut.fps-1&&quiet<=.4*cut.fps,id+' does not reserve the 0.4s reset');
}
assert.deepEqual(cut.speed_clamp,[.97,1.04]);
for(const swatch of [PALETTE.GOLD,PALETTE.SKY])assert.equal(blockInk(swatch),PALETTE.BLACK);
for(const swatch of [PALETTE.BLUE,PALETTE.TEAL,PALETTE.PURPLE,PALETTE.RED,PALETTE.ORANGE])
  assert.equal(blockInk(swatch),PALETTE.WHITE,'Colored glass must use white ink');
assert.deepEqual(math.attention(4),[0,0,0,.5,.5,0,0]);
assert.equal(math.sft_nll([.5,.25,.8]).toFixed(3),'2.303');
assert.equal(math.sft_nll([.7,.25,.8]).toFixed(3),'1.966');
assert.ok(Math.abs(math.bt(1.1,2.1)-math.bt(3.1,4.1))<1e-12);
assert.equal((math.sft_nll([.9,.2])/2).toFixed(3),'0.857');
assert.equal((math.sft_nll([.9,.6])/2).toFixed(3),'0.308');
assert.equal(math.kl([.6,.4],[.8,.2]).toFixed(3),'0.105');
assert.equal(math.kl([.68,.32],[.8,.2]).toFixed(3),'0.040');
assert.equal(math.expected_score([.6,.3,.1],[4,2,0]),3);
for(let j=0;j<=200;j++){
  const u=j/200;
  const shapes=SIZE_PROFILE.map((s,i)=>{
    const [x,y,w,h,d]=role_pose(i,u);
    const offset=Math.min(8,d*.28)*2;
    return [x,y-offset*s,x+(w+offset)*s,y+h*s];
  });
  for(let i=0;i<shapes.length;i++)for(let k=i+1;k<shapes.length;k++){
    const [x1,y1,x2,y2]=shapes[i],[u1,v1,u2,v2]=shapes[k];
    assert.ok(Math.min(x2,u2)<=Math.max(x1,u1)||Math.min(y2,v2)<=Math.max(y1,v1),
      `Checkpoint bodies overlap at ${u}: roles ${i}, ${k}`);
  }
}
for(const r of cut.scenes){
  let end=0;
  for(const [begin,next,title] of r.captions){
    assert.ok(end<=begin&&begin<next&&next<=r.frames&&title);
    if(r.pause_frames)assert.ok(next<=r.speech_end!);
    end=next;
  }
  subject=r;
  const exempt=policy.formatExempt.includes(r.id);
  for(let f=0;f<r.frames;f++){
    try{
      screen.clear();painted.clear();yEdge=0;opacity=1;dx=dy=0;scale=1;
      captions=captionAt(r.captions,f)??'';
      drawFrame(board,r,f,cut.fps);
      if(r.id==='c22'){
        const pair=painted.has('立刻放进冰水。')||painted.has('关火，留在热水里。');
        const table=painted.has('胜')||painted.has('负');
        assert.ok(!(pair&&table),'The two-answer pose and the table must not overlap');
        if(f>r.cues.many-.38*cut.fps&&f<=r.cues.many)assert.ok(!pair&&!table,'Pair exit still visible during the reset');
      }
      if(f===Math.round(1.5*cut.fps)&&r.id.startsWith('card')){
        const question={
          card2:'把微调搬进产线，工程上卡在哪两道关口？',
          card3:'光靠模仿标准答案，模型还能变得更强吗？',
          card4:'如何拴住策略不跑偏？代价又是什么？',
        }[r.id];
        if(question)assert.ok(painted.has(question),'The chapter question must be a single full-width run');
      }
      if(!exempt){
        const han=[...screen.values()].reduce((a,v)=>a+v.size,0);
        assert.ok(han<=policy.maxHanPerFrame,`Screen Han ${han}: ${[...screen.keys()].join(' | ')}`);
        if(captions){
          const upper=1080-52-72*captions.split('\n').length;
          assert.ok(yEdge*1.2<upper-policy.minCaptionMarginPx,`Text or math at y=${(yEdge*1.2).toFixed(1)} vs subtitle y=${upper}`);
        }
      }
    }catch(e){throw new Error(`${r.id}, frame ${f}`,{cause:e});}
  }
  start+=r.frames;
  if(r.opens_into)assert.ok(rows[r.opens_into.id]);
  process.stdout.write(`${r.id}:${r.frames} `);
}
assert.deepEqual([...paperStarts.keys()],policy.papers);
console.log(`\nNative drawing: ${FRAMES.toLocaleString('en-US')} frames passed text budget, subtitle clearance, geometry and the six numerical checks.`);
