import {bundle} from '@remotion/bundler';
import {openBrowser, renderMedia, selectComposition} from '@remotion/renderer';
import {spawnSync} from 'node:child_process';
import {renameSync, mkdirSync, existsSync, readFileSync} from 'node:fs';
import {resolve} from 'node:path';
import browserTools from './local-browser.cjs';

const lint=spawnSync(process.execPath,['scripts/lint-visuals.mjs'],{stdio:'inherit'});
if(lint.status!==0)process.exit(lint.status??1);
const cut=JSON.parse(readFileSync('src/data/cut.json','utf8'));
const args=process.argv.slice(2);
const flag=(name)=>args.find(x=>x.startsWith('--'+name+'='))?.split('=')[1];
const root=resolve(flag('out-dir')??'build/native-shots');mkdirSync(root,{recursive:true});
const laneText=flag('lane')??'0/1';
const [lane,lanes]=laneText.split('/').map(Number);
const workers=Number(flag('workers')??8);
const encoder=Number(flag('encoder-threads')??0);
if(!Number.isInteger(lane)||!Number.isInteger(lanes)||!Number.isInteger(workers)||!Number.isInteger(encoder)||
   lane<0||lane>=lanes||workers<1||encoder<0)throw Error('Invalid render lane/workers/encoder threads');
const replace=args.includes('--replace');
const selected=args.filter(x=>!x.startsWith('--'));
const active=new Set(selected);
for(const id of selected)if(!cut.scenes.find(r=>r.id===id))throw Error(`Unknown shot ${id}`);
if(args.includes('--with-joins')){
  const requested=new Set(active);
  for(const row of cut.scenes){
    if(requested.has(row.handoff?.from)&&row.handoff?.kind==='carry')active.add(row.id);
    if(requested.has(row.opens_into?.id))active.add(row.id);
  }
}
const jobs=cut.scenes.filter((r,i)=>i%lanes===lane&&(!active.size||active.has(r.id)));
const priority=(flag('priority')??'').split(',').filter(Boolean);
const rank=id=>{const i=priority.indexOf(id);return i<0?priority.length:i;};
jobs.sort((a,b)=>rank(a.id)-rank(b.id));

const browserExecutable=browserTools.localBrowser();
const serveUrl=await bundle({entryPoint:resolve('src/index.ts'),enableCaching:false,onProgress:()=>{}});
const browser=await openBrowser('chrome',{browserExecutable,logLevel:'warn'});
function inspect(file){
  const p=spawnSync('ffprobe',['-v','error','-select_streams','v:0','-show_streams','-of','json',file],{encoding:'utf8'});
  if(p.status!==0)throw Error(p.stderr);
  return JSON.parse(p.stdout).streams[0];
}
function check(file,row){
  const s=inspect(file);
  if(s.nb_frames!==String(row.frames)||s.avg_frame_rate!==`${cut.fps}/1`||s.width!==1920||s.height!==1080) {
    throw Error(`${row.id} has a different frame clock: ${s.nb_frames}/${s.avg_frame_rate}`);
  }
  return s;
}
try{
  for(const row of jobs){
    const out=resolve(root,`${row.id}.mp4`);
    if(!replace&&existsSync(out)){
      check(out,row);console.log(new Date().toISOString(),'REUSE',row.id);continue;
    }
    const temp=resolve(root,`.${row.id}.${process.pid}.mp4`);
    const inputProps={id:row.id,showCaps:false};
    const comp=await selectComposition({serveUrl,id:row.id,inputProps,puppeteerInstance:browser,
      logLevel:'warn',timeoutInMilliseconds:180000});
    const start=Date.now();
    let last=0;
    console.log(new Date().toISOString(),'BEGIN',row.id,row.frames);
    await renderMedia({serveUrl,composition:comp,inputProps,puppeteerInstance:browser,outputLocation:temp,
      codec:'h264',muted:true,concurrency:workers,overwrite:true,timeoutInMilliseconds:180000,
      imageFormat:'jpeg',jpegQuality:96,crf:17,x264Preset:'veryfast',pixelFormat:'yuv420p',colorSpace:'bt709',
      ffmpegOverride:encoder?({type,args})=>type==='pre-stitcher'
        ?['-threads:v','1','-filter_threads','2',...args.slice(0,-1),'-threads:v',String(encoder),args.at(-1)]
        :args:undefined,
      logLevel:'warn',onProgress:({renderedFrames})=>{
        if(renderedFrames-last>=180||renderedFrames===row.frames&&last!==row.frames){
          console.log(new Date().toISOString(),row.id,renderedFrames,'/',row.frames,
            Math.round(renderedFrames*1000/(Date.now()-start)),'fps');
          last=renderedFrames;
        }
      }});
    const s=check(temp,row);
    renameSync(temp,out);
    console.log(new Date().toISOString(),'DONE',row.id,((Date.now()-start)/1000).toFixed(1)+'s',s.color_space,s.color_range);
  }
}finally{await browser.close({silent:true});}
