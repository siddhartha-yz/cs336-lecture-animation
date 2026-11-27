import {spawnSync} from 'node:child_process';
import assert from 'node:assert/strict';

function call(bin,args){
 const r=spawnSync(bin,args,{encoding:'utf8',maxBuffer:24*1024*1024});
 if(r.status!==0)throw Error(`${bin}: ${r.error?.message??r.stderr}`);
 return r;
}

function inspect(file){
 return JSON.parse(call('ffprobe',['-v','error','-show_streams','-of','json',file]).stdout)
  .streams.filter(s=>s.codec_type==='audio');
}
function check(audio,ch,duration){
 assert.ok(audio?.codec_name==='aac'&&audio.channels===ch&&audio.sample_rate==='48000'&&
  Math.abs(Number(audio.duration)-duration)<=.022,
  `需要 ${ch} 声道 AAC / 48 kHz，且长度和视频 ${duration.toFixed(3)}s 同钟`);
}
export function quietIntervals(file,track,duration){
 const txt=call('ffmpeg',['-nostdin','-hide_banner','-i',file,'-map','0:a:'+track,
   '-af','silencedetect=noise=-48dB:d=0.25','-f','null','-']).stderr;
 const silence=[];let open;
 for(const m of txt.matchAll(/silence_(start|end):\s*([\d.]+)/g)){
  if(m[1]==='start')open=Number(m[2]);
  else if(open!==undefined){silence.push([open,Number(m[2])]);open=undefined;}
 }
 if(open!==undefined)silence.push([open,duration]);
 return silence;
}
export function validateSound({mix,dialogue,master,duration,exempt,holds,events,fps=60}){
 let file=dialogue,track=0;
 if(master){
  const audio=inspect(master);
  assert.equal(audio.length,2,'母版必须是混音和干旁白两轨');
  check(audio[0],2,duration);check(audio[1],1,duration);
  file=master;track=1;
 }else{
  const m=inspect(mix),v=inspect(dialogue);
  assert.equal(m.length,1);assert.equal(v.length,1);
  check(m[0],2,duration);check(v[0],1,duration);
 }
 const silence=quietIntervals(file,track,duration);
 for(const [id,a,b] of holds)assert.ok(silence.some(([x,y])=>x<=a+.05&&y>=b-.05),
  id+': 实际干声进入了思考时窗');
 const windows=[...exempt].sort((a,b)=>a[0]-b[0]);
 for(const [a,b] of silence){
  let p=a;
  for(const [x,y] of windows){
   if(y<=p||x>=b)continue;
   if(x>p)assert.ok(x-p<=2.2+.5/fps,`非白名单静音：${p.toFixed(2)}–${x.toFixed(2)} 秒`);
   p=Math.max(p,y);
  }
  if(p<b)assert.ok(b-p<=2.2+.5/fps,`非白名单静音：${p.toFixed(2)}–${b.toFixed(2)} 秒`);
 }
 for(const [label,t] of events)
  assert.ok(!silence.some(([a,b])=>a+.12<t&&t<b-.12),label+': 标记的实际词首落在干声的静默里');
 return silence;
}
