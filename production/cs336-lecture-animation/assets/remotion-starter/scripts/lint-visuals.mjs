// Run from the generated project root. Source gates before rendering, and
// optionally the actual dry voice / mix clock before a production release.
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import assert from 'node:assert/strict';
import {build} from 'esbuild';
import ts from 'typescript';
import {validateSound} from './audio-gate.mjs';

const release=process.argv.includes('--release');
const arg=(name)=>process.argv.slice(2).find(s=>s.startsWith(name+'='))?.slice(name.length+1);
const expected={
 bg:'#000000',paper:'#F2F1EC',white:'#FFFFFF',axis:'#666666',gloss:'#B0B8C4',
 cyan:'#19B5FE',blue:'#29ABCA',lightCyan:'#58C4DD',gold:'#FFD43B',yellow:'#FFFF00',
 green:'#2EC492',orange:'#F25C3B',coral:'#E84C5C',magenta:'#DF5296',pink:'#F462C0',purple:'#B87BFF',
};
const FILE='src/theme/palette.ts';
const swatches=fs.readFileSync(FILE,'utf8');
const colors=[...swatches.matchAll(/\b([A-Za-z]+)\s*:\s*['"](#[\dA-Fa-f]{6})['"]/g)];
assert.ok(swatches.includes('Object.freeze'),
 '锁定 src/theme/palette.ts 中的色板');
assert.equal(colors.length,Object.keys(expected).length,'v2 色板项数');
assert.equal(new Set(colors.map(x=>x[1])).size,colors.length,'色板键重复');
for(const [,name,hex] of colors)assert.equal(hex,expected[name],name+' 不在 v2 色板');
assert.match(swatches,/const PAPER_EDGE\s*=\s*['"]#C8C6BE['"]/);
assert.ok(fs.existsSync('VISUAL_CONSTITUTION_v2.md'),'工程根目录缺 VISUAL_CONSTITUTION_v2.md，请用技能入口创建');
const cut=JSON.parse(fs.readFileSync('src/data/cut.json','utf8'));
const {scenes,fps}=cut,errors=[];
const guard=(cond,label)=>{if(!cond)errors.push(label);};
const walkFiles=dir=>fs.readdirSync(dir,{withFileTypes:true}).flatMap(entry=>
 entry.isDirectory()?walkFiles(path.join(dir,entry.name)):[path.join(dir,entry.name)]);
const banned=/(教学示意|教学算例|教学例|读图约值|示意图形|不按比例|核心结论|本节小结|关键洞察|来源口径|复剪包|讲义|课程幻灯|课堂举例|第[一二三四五六七八九十\d]+笔账|\b(?:Slide|Stage\s*\d+|Step\s*\d+|Phase\s+[A-Z])\b)/iu;
for(const f of walkFiles('src').filter(n=>/\.[tj]sx?$/.test(n)&&n!==FILE)){
 const format=f===path.join('src','format.ts');
 const source=ts.createSourceFile(f,fs.readFileSync(f,'utf8'),ts.ScriptTarget.Latest,true);
 const fail=(node,label)=>errors.push(`${f}:${1+source.getLineAndCharacterOfPosition(node.getStart()).line} ${label}`);
 function visit(n){
  if(!format&&(ts.isStringLiteralLike(n)||ts.isTemplateLiteralToken(n))){
   const s=n.text;
   if(/#(?:[\dA-Fa-f]{8}|[\dA-Fa-f]{6}|[\dA-Fa-f]{4}|[\dA-Fa-f]{3})\b|rgba?\s*\(|(?:slate-|zinc-|gray-[89]00)|(?:linear|radial)-gradient/i.test(s))fail(n,'裸色值、灰色系或背景渐变');
   if(/className|tw\s/.test(n.parent?.getText(source).slice(0,24)??'')&&/\brounded(?:-|\b)|\bshadow(?:-|\b)/.test(s))fail(n,'PPT 圆角或浮层样式');
  }
  const name=n.name?.getText(source)?.replace(/['"]/g,'');
  if(!format&&['boxShadow','backdropFilter','box-shadow','backdrop-filter'].includes(name))fail(n,'PPT 浮层样式');
  if(!format&&name==='fontSize'&&/\b(?:interpolate|lerp|mix)\s*\(/.test((n.initializer??n.value)?.getText(source)??''))fail(n,'缩放用 transform，不插值 fontSize');
  const rectRadius=name==='rx'&&ts.isJsxAttribute(n)&&
    n.parent.parent.tagName?.getText(source)==='rect';
  if(!format&&(rectRadius||['borderRadius','border-radius'].includes(name))){
   const v=(n.initializer??n.value)?.getText(source)?.replace(/[{}'"px]/g,'')??'';
   if(Number(v)>=4)fail(n,'正文圆角不得达到 4px');
  }
  if(ts.isCallExpression(n)){
   const name=n.expression.getText(source);
   if(!format&&/(?:^|\.)(?:prism|IsoCube|Badge|TakeawayBanner|SlideTitle)$/i.test(name))fail(n,'禁止等轴测模型和 PPT 控件');
   if(!format&&/(?:^|\.)Write$/.test(name)&&/\p{Script=Han}/u.test(n.arguments.map(a=>a.getText(source)).join('')))fail(n,'禁止给汉字用 Write');
  }
  ts.forEachChild(n,visit);
 }
 visit(source);
}
guard(fps===60,'60 fps 是项目帧钟，修改规格前先锁全片交付');
guard(cut.speed_clamp?.join(',')==='0.97,1.04','调速范围须为 0.97–1.04');
guard(Array.isArray(scenes)&&scenes.length>0,'无镜表');
const fpsFrame=(n)=>Number.isInteger(n)&&n>=0;
let at=0,lastPaper=-Infinity,nOP=0;
const idSet=new Set(),exemptWindows=[],holds=[],audioEvents=[];
const exempt=new Set(['op','chapter','end']);
for(const [i,r] of scenes.entries()){
 const id=r.id,old=scenes[i-1],next=scenes[i+1];
 guard(/^[a-z][a-z0-9-]*$/.test(id)&&!idSet.has(id),id+': 镜号无效或重复');idSet.add(id);
 guard(['body','question',...exempt].includes(r.kind),id+': 段类无效');
 guard(Number.isInteger(r.frames)&&r.frames>0,id+': 镜长必须为正整数帧');
 const lo=r.black_head??0,tail=r.black_tail??0;
 guard(fpsFrame(lo)&&fpsFrame(tail)&&lo+tail<r.frames,id+': 清场超出镜长');
 if(r.kind==='op'){
  nOP++;
  guard(nOP===1&&!scenes.slice(0,i-1).some(s=>s.kind==='question')&&old?.kind==='question'&&next?.kind==='body'&&r.frames===5*fps,id+': 首问 → 五秒 OP → Act 1');
 }
 if(r.kind==='chapter'){
  guard(nOP===1&&old?.kind==='question'&&next?.kind==='body'&&r.frames===4*fps,id+': 仅 Act 2 起允许问句后的四秒章卡');
 }
 if(r.kind==='end')guard(!next,id+': END 只能落在片尾');
 if(['op','chapter'].includes(r.kind)){
  guard(r.opens_into?.id===next?.id&&r.opens_into?.origin?.length===2&&r.opens_into.origin.every(Number.isFinite),id+': 章门须开到正文真实首帧');
 }
 if(exempt.has(r.kind))exemptWindows.push([at/fps,(at+r.frames)/fps]);
 if(r.kind==='body'){
  guard(typeof r.apparatus==='string'&&r.apparatus,id+': 为主装置命名');
  guard(r.stableFrames?.length&&r.stableFrames.every(n=>fpsFrame(n)&&n>=lo&&n<r.frames-tail),id+': 指定有效正式帧做占幅验收');
 }
 if(r.layout!==undefined)guard(r.kind==='body'&&r.layout==='sample-text'&&!r.paper,id+': 纯样本正文才以实际墨迹量占幅');
 if(r.kind==='question')guard(!!r.prompt&&/[？]$/.test(r.prompt),id+': 核心问句用全角问号');
 if(r.paper){
  guard(r.kind==='body'&&typeof r.paper.source==='string'&&r.paper.source.trim()&&!/fig\.|eq\.|讲义|slide/i.test(r.paper.source)&&r.paper.ref,id+': 切面需要纯净的学术出处与真实出处记录');
  guard(at-lastPaper>=360*fps,id+': 两处文献切面至少相隔六分钟');
  lastPaper=at;
 }
 if(old){
  guard(r.handoff?.from===old.id,id+': 接点类型必须回指实际上一镜');
  if(r.handoff?.kind==='carry'){
   guard(!exempt.has(old.kind)&&!exempt.has(r.kind)&&Boolean(r.apparatus)&&r.apparatus===old.apparatus,id+': 只有同一装置才能共姿态续演');
   guard(lo===0&&(old.black_tail??0)===0,id+': 共姿态不能带清屏黑帧');
  }else if(r.handoff?.kind==='reset'){
   guard(!exempt.has(old.kind)&&!exempt.has(r.kind)&&r.apparatus!==old.apparatus,id+': reset 仅用于无关装置');
   guard(lo+(old.black_tail??0)===24,id+': 非同装置接点预留 24 帧纯黑');
  }else{
   guard(r.handoff?.kind==='gate'&&(exempt.has(old.kind)||exempt.has(r.kind)),id+': 必须声明 carry、reset 或正式章门');
  }
 }
 let prev=0;
 for(const [a,b,t] of r.captions){
  guard(fpsFrame(a)&&fpsFrame(b)&&prev<=a&&a<b&&b<=r.frames&&typeof t==='string'&&t.trim(),id+': 字幕边界、文字或顺序错误');
  guard(!banned.test(t)&&!/\\(?:frac|theta|text)\b|\b[prv]\([^)]*_[^)]*\)/.test(t),id+': 字幕混入元数据或公式源码：'+t);
  if(r.hold)guard(b<=r.hold.start||a>=r.hold.start+r.hold.frames,id+': 思考静默不是延长字幕');
  prev=b;
 }
 if(r.hold){
  const h=r.hold;
  guard(r.kind==='body'&&fpsFrame(h.start)&&fpsFrame(h.frames)&&h.start+h.frames<=r.frames&&
   (h.kind==='prediction'?h.frames===270:h.kind==='blind'&&h.frames>=390&&h.frames<=450),id+': 预测 4.5s 或多行 A/B 6.5–7.5s');
  holds.push([id,(at+h.start)/fps,(at+h.start+h.frames)/fps]);
  exemptWindows.push([(at+h.start)/fps,(at+h.start+h.frames)/fps]);
 }
 // A recording can end exactly at the next picture's opening. Only that
 // right-open boundary may equal the shot length; onsets need a visible frame.
 for(const [key,value] of Object.entries(r.cues))
  guard(fpsFrame(value)&&(key==='speechEnd'?value<=r.frames:value<r.frames),id+': 镜内 cue 超界 '+key);
 for(const {cue,wordFrame,kind} of r.beats??[]){
  guard(['number','highlight'].includes(kind)&&fpsFrame(wordFrame)&&wordFrame<r.frames&&Math.abs(r.cues[cue]-wordFrame)<=9,id+': 视觉事件距离实际词首超过 150ms：'+cue);
  audioEvents.push([id+': '+cue,(at+wordFrame)/fps]);
 }
 for(const {cue,title} of r.examples??[]){
  guard(r.cues[cue]!==undefined&&title&&r.captions.some(([a,b])=>a-9<=r.cues[cue]&&r.cues[cue]<b+9),id+': 数值算例不能脱开口播：'+cue);
  guard(r.beats?.some(b=>b.cue===cue&&b.kind==='number'),id+': 数值算例缺真实词首帧 '+cue);
 }
 at+=r.frames;
}
if(release){
 guard(nOP===1,'正式片必须有唯一 OP');
 guard(cut.demo===false,'模板示范不能发成正片；先替换内容、声音与时钟');
 const length=cut.format==='engineering'?[16,20]:cut.format==='derivation'?[22,26]:[];
 guard(length.length&&at/fps>=length[0]*60&&at/fps<=length[1]*60,'正式片长：动机工程 16–20 分钟 / 数理推导 22–26 分钟');
 guard(/^[\w-]+$/.test(cut.audioTag),'音轨目录名无效');
}
if(errors.length){console.error(errors.join('\n'));process.exit(1);}

const run=(bin,args)=>{
 const r=spawnSync(bin,args,{encoding:'utf8',maxBuffer:24*1024*1024});
 if(r.status!==0)throw Error(`${bin} failed: ${r.error?.message??r.stderr}`);
 return r;
};
for(const [id,p] of Object.entries(JSON.parse(fs.readFileSync('src/data/plates.json','utf8')))){
 assert.ok(/^[A-Za-z0-9][A-Za-z0-9._-]*$/.test(p.file)&&['raster','vector'].includes(p.kind)&&
  p.pixels?.length===2&&p.pixels.every(n=>Number.isInteger(n)&&n>0)&&typeof p.source==='string'&&p.source.trim(),
  id+': 图板需要本地文件、正宽高和真实出处');
 const file=path.join('public/plates',p.file);
 assert.ok(fs.existsSync(file),id+': 缺本地图板文件 '+p.file);
 if(p.kind==='raster'){
  assert.ok(/\.(png|jpg|jpeg|webp)$/i.test(p.file),id+': 光栅图板类型');
  const res=JSON.parse(run('ffprobe',['-v','error','-select_streams','v:0','-show_entries','stream=width,height','-of','json',file]).stdout);
  const actual=res.streams?.[0];
  assert.deepEqual([actual?.width,actual?.height],p.pixels,id+': 图板实际像素和申报不符');
 }else assert.ok(/\.svg$/i.test(p.file),id+': 矢量图板须为 SVG');
}
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'cs336-frames-'));
try{
 const out=path.join(tmp,'frames.cjs'),letters=path.join(tmp,'han.json');
 await build({entryPoints:['scripts/check-frames.ts'],bundle:true,platform:'node',format:'cjs',outfile:out,logLevel:'silent'});
 const exec=run(process.execPath,[out,letters]);process.stdout.write(exec.stdout);
 const fonts=run('fc-scan',['--format=%{charset}','public/fonts/noto-serif-sc.woff']).stdout.trim();
 if(!fonts)throw Error('缺可用的宋体字符表；检查公用字体包');
 const ranges=fonts.split(/\s+/).map(r=>r.split('-').map(x=>parseInt(x,16)));
 assert.ok(ranges.every(r=>r.every(Number.isFinite)),'字体字符表错误');
 const missing=JSON.parse(fs.readFileSync(letters,'utf8')).filter(c=>!ranges.some(([a,b=a])=>a<=c.codePointAt(0)&&c.codePointAt(0)<=b));
 if(missing.length)throw Error('字体缺字：'+missing.map(c=>c+' U+'+c.codePointAt(0).toString(16)).join(' '));
}finally{fs.rmSync(tmp,{recursive:true,force:true});}

if(release){
 const base=path.join('public/audio',cut.audioTag);
 validateSound({
  mix:arg('--mix')??path.join(base,'mix.m4a'),dialogue:arg('--dialogue')??path.join(base,'dialogue.m4a'),
  master:arg('--master'),duration:at/fps,exempt:exemptWindows,holds,events:audioEvents,fps
 });
}
console.log('Visual constitution v2: 0 errors'+(release?' (source, frame and dry-voice gates).':' (source and frame gates).'));
