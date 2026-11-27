// Review the delivered pixels. Full artwork must be black inside declared resets;
// captions are intentionally excluded from that probe.
import fs from 'node:fs';
import path from 'node:path';
import {execFileSync} from 'node:child_process';
import assert from 'node:assert/strict';
import {readCut} from './sidecars.mjs';
import {verifySampleFrame} from './sample-layout.mjs';

const file=process.argv[2];
if(!file||file.startsWith('-'))throw Error('Usage: node scripts/review-frames.mjs FILM.mp4 [--ids=op,code] [--out=build/review]');
const arg=(name)=>process.argv.slice(3).find(v=>v.startsWith(name+'='))?.slice(name.length+1);
const to=arg('--out')??'build/review';
const selected=arg('--ids')?.split(',');
const cut=readCut(), fps=cut.fps;
const meta=JSON.parse(execFileSync('ffprobe',['-v','error','-select_streams','v:0','-show_streams','-of','json',file]));
const v=meta.streams[0],N=cut.scenes.reduce((a,s)=>a+s.frames,0);
assert.ok(v&&Number(v.nb_frames)===N&&v.avg_frame_rate===fps+'/1','审查文件的全片帧钟不同于当前镜表');
if(selected)for(const id of selected)assert.ok(cut.scenes.some(r=>r.id===id),'不认识镜号 '+id);
fs.mkdirSync(to,{recursive:true});
const ff=['-v','error','-nostdin','-xerror'];
const seek=f=>Math.max(0,f/fps-0.000001).toFixed(6);
const stageH=Math.floor(v.height*912/1080/2)*2;
const pixels=640*304;
function artwork(first,count){
 const raw=execFileSync('ffmpeg',[...ff,'-ss',seek(first),'-i',file,'-map','0:v:0','-an','-sn',
   '-vf',`crop=iw:${stageH}:0:0,scale=640:304,format=gray`,
   '-frames:v',String(count),'-threads','1','-f','rawvideo','pipe:1'],{maxBuffer:24*1024*1024});
 assert.equal(raw.length,count*pixels);
 return raw;
}
const report=[];
let at=0;
for(const [i,r] of cut.scenes.entries()){
 const previous=cut.scenes[i-1];
 if(selected?selected.includes(r.id):r.handoff?.kind==='reset'||r.opens_into||r.hold||r.layout==='sample-text'){
  assert.match(r.id,/^[a-z][a-z0-9-]*$/);
  const marks=new Map();
  if(r.handoff?.kind==='reset'){
   const a=at-(previous.black_tail??0),b=at+(r.black_head??0);
   assert.ok(b>a,'未留清场');
   assert.ok(artwork(a,b-a).every(luma=>luma<=2),r.id+'：实片净空里还有画面');
   marks.set('leave',a-10);marks.set('black',Math.floor((a+b)/2));marks.set('arrive',b+15);
   console.log(r.id,b-a,'clear artwork frames');
  }
  if(r.opens_into){
   const edge=at+r.frames,raw=artwork(edge-1,2);
   let lit=0,changed=0,sum=0;
   for(let j=0;j<pixels;j++){
    const a=raw[j],b=raw[pixels+j],d=Math.abs(a-b);
    sum+=d;if(Math.max(a,b)>=12)lit++;if(d>16)changed++;
   }
   // Independently coded scenes can differ slightly in quantization, not in their pose.
   assert.ok(lit>=32&&sum/pixels<=2&&changed/lit<=.06,
     r.id+'：章门末帧和正文首帧不接（跳黑、残字或清片没同步更新）');
   console.log(r.id,'door landing',edge-1,'→',edge,'MAE',(sum/pixels).toFixed(3));
   marks.set('door',at+Math.round(r.frames*.45));
   marks.set('iris',at+r.frames-14);
   marks.set('door-last',edge-1);
   marks.set('entry-zero',edge);
   marks.set('entry',at+r.frames+9);
  }
  if(r.hold){
   marks.set('hold-start',at+r.hold.start);
   marks.set('hold-middle',at+r.hold.start+Math.floor(r.hold.frames*.52));
   marks.set('hold-end',at+r.hold.start+r.hold.frames-2);
  }
  if(r.layout==='sample-text'){
   for(const f of r.stableFrames){
    verifySampleFrame(file,at+f,fps,r.id+'+'+f);
    marks.set('sample-'+f,at+f);
   }
  }
  if(!marks.size){
   marks.set('first',at);marks.set('middle',at+Math.floor(r.frames/2));marks.set('last',at+r.frames-1);
  }
  for(const [label,frame] of marks){
   if(frame<0||frame>=N)continue;
   const name=`${r.id}-${label}-${frame}.png`;
   execFileSync('ffmpeg',[...ff,'-y','-ss',seek(frame),'-i',file,'-map','0:v:0',
     '-frames:v','1','-vf','scale=640:-2','-threads','1',path.join(to,name)]);
   report.push({shot:r.id,phase:label,frame,seconds:+(frame/fps).toFixed(6),still:name});
  }
 }
 at+=r.frames;
}
fs.writeFileSync(path.join(to,'frames.json'),JSON.stringify(report,null,2)+'\n');
console.log(to,report.length,'actual review frames; inspect the stills.');
