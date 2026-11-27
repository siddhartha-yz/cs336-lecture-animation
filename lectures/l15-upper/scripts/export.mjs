import {join,resolve} from 'node:path';
import {spawnSync} from 'node:child_process';
import {writeFileSync,mkdirSync,existsSync,renameSync} from 'node:fs';
import {readCut,writeSidecars} from './sidecars.mjs';

const arg=(name)=>process.argv.slice(2).find(s=>s.startsWith(name+'='))?.slice(name.length+1);
const kind=process.argv[2]??'master';
if(!['master','share','silent'].includes(kind))throw Error('Usage: node scripts/export.mjs master|share|silent [--out=...] [--master=...]');

const shotDir=resolve(arg('--shots')??'build/native-shots');
const out=resolve(arg('--out')??`build/L15-remotion-${kind}.mp4`);
const temp=out+`.${process.pid}.mp4`;
const master=resolve(arg('--master')??'build/L15-remotion-master.mp4');
const lint=spawnSync(process.execPath,['scripts/lint-visuals.mjs'],{stdio:'inherit'});
if(lint.status!==0)process.exit(lint.status??1);
const cut=readCut();
const audioRoot=cut.audioTag?join('public/audio',cut.audioTag):'public/audio';
const inMix=resolve(arg('--mix')??join(audioRoot,'mix.m4a'));
const inDialogue=resolve(arg('--dialogue')??join(audioRoot,'dialogue.m4a'));
const sidecars=`build/sidecars.${process.pid}`;
const {frames:total,chapters}=writeSidecars(cut,sidecars);
const fps=cut.fps,frameTicks=256,timeScale=fps*frameTicks;
if(existsSync(out))throw Error(`Output already exists: ${out}`);
mkdirSync('build',{recursive:true});
const escaped=(name)=>{
  if(/[\r\n]/.test(name))throw Error('Newline in asset path');
  return "'"+name.replaceAll("'","'\\''")+"'";
};
function run(exe,args,{read=false}={}){
  const p=spawnSync(exe,args,{encoding:'utf8',stdio:read?['ignore','pipe','inherit']:'inherit',
    maxBuffer:30_000_000});
  if(p.status!==0)throw Error(p.error??`${exe} exited with ${p.status??p.signal}`);
  return p.stdout;
}
function inspect(file,...args){
  return JSON.parse(run('ffprobe',['-v','error',...args,'-of','json',file],{read:true}));
}
function finish(){
  const info=inspect(temp,'-show_streams','-show_chapters');
  const [video]=info.streams.filter(x=>x.codec_type==='video');
  const audio=info.streams.filter(x=>x.codec_type==='audio');
  if(!video||video.nb_frames!==String(total)||video.avg_frame_rate!==`${fps}/1`||
     video.width!==1920||video.height!==1080)throw Error(`Broken output frame clock: ${JSON.stringify(video)}`);
  if(video.color_space!=='bt709'||video.color_transfer!=='bt709'||video.color_primaries!=='bt709'||video.color_range!=='tv'){
    throw Error('Expected Rec.709 limited-range video');
  }
  if(info.chapters?.length!==chapters)throw Error('Chapter map incomplete');
  if(audio.length!==({master:2,share:1,silent:0}[kind]))throw Error('Wrong number of audio tracks');
  if(audio.some((a,i)=>a.channels!==([2,1][i])||a.sample_rate!=='48000'||
       Math.abs(Number(a.duration)-total/fps)>.022))throw Error('Audio tracks do not share the cut clock');
  if(info.streams.filter(x=>x.codec_type==='subtitle').length!==(kind==='share'?0:1))throw Error('Subtitle track missing/extra');
  const {packets}=inspect(temp,'-select_streams','v:0','-show_packets','-show_entries','packet=pts,dts,duration');
  const pts=packets.map(p=>p.pts).sort((a,b)=>a-b);
  if(pts.length!==total||pts.some((p,i)=>p!==i*frameTicks))throw Error('Presentation clock jumped');
  const d0=packets[0].dts;
  if(packets.some((p,i)=>p.dts!==d0+i*frameTicks||p.duration!==frameTicks))throw Error('Decode clock jumped');
  renameSync(temp,out);
  console.log(out,`${total} frames / ${chapters} chapters / ${audio.length} audio tracks`);
}
const common=['-v','error','-nostdin'];
let maps=[],codec=['-c:v','copy'];
let inputs=[];
if(kind==='share'){
  inputs=['-i',master];maps=['-map','0:v:0','-map','0:a:0','-map_metadata','0','-map_chapters','0'];
  codec=['-vf',`ass=${sidecars}/captions.ass:fontsdir=public/fonts`,'-c:v','libx264','-crf','18','-preset','medium','-threads','6','-pix_fmt','yuv420p',
    '-profile:v','high','-colorspace','bt709','-color_trc','bt709','-color_primaries','bt709','-color_range','tv','-c:a','copy'];
}else{
  let frames=0,last=0;
  const startOrder=[];
  const lines=['ffconcat version 1.0'];
  for(const row of cut.scenes){
    const source=join(shotDir,`${row.id}.mp4`);
    if(!existsSync(source))throw Error(`Missing Remotion shot: ${source}`);
    const {streams:[v],packets:[p]}=inspect(source,'-select_streams','v:0','-show_streams','-show_packets','-read_intervals','%+#1');
    if(v.nb_frames!==String(row.frames)||v.avg_frame_rate!==`${fps}/1`||v.width!==1920||v.height!==1080||
       p.pts!==0||v.codec_name!=='h264')throw Error(`Incompatible clean shot ${row.id}`);
    const [a,b]=v.time_base.split('/').map(Number);
    startOrder.push(Math.round(-p.dts*a/b*timeScale));
    frames+=row.frames;
    const next=Math.round(frames*1e6/fps);
    lines.push('file '+escaped(source),'duration '+((next-last)/1e6).toFixed(6));
    last=next;
  }
  const concat=resolve(`build/cut.${process.pid}.ffconcat`);
  writeFileSync(concat,lines.join('\n')+'\n');
  inputs=['-f','concat','-safe','0','-i',concat];maps=['-map','0:v:0'];
  const mixed=kind==='master';
  if(mixed){
    inputs.push('-i',inMix,'-i',inDialogue);
    maps.push('-map','1:a:0','-map','2:a:0',
      '-metadata:s:a:0','handler_name=旁白与配乐','-metadata:s:a:1','handler_name=纯旁白',
      '-metadata:s:a:0','language=zho','-metadata:s:a:1','language=zho','-disposition:a:1','0');
    codec.push('-c:a','copy');
  }
  const sub=mixed?3:1;
  inputs.push('-i',join(sidecars,'captions.srt'),'-f','ffmetadata','-i',join(sidecars,'chapters.ffmeta'));
  maps.push('-map',`${sub}:s:0`,'-map_metadata',String(sub+1),'-map_chapters',String(sub+1),
    '-metadata:s:s:0','language=zho');
  codec.push('-c:s','mov_text');
  // When different versions of x264 use different prerolls, keep PTS and
  // normalize decoding order only. Stable inputs take the copy path.
  if(new Set(startOrder).size>1){
    const unit=inspect(join(shotDir,`${cut.scenes[0].id}.mp4`),'-select_streams','v:0','-show_streams').streams[0].time_base;
    const [a,b]=unit.split('/').map(Number),t=Math.round(b/(a*fps));
    codec.push('-bsf:v',`setts=pts=PTS:dts=N*${t}-${Math.round(Math.max(...startOrder)*t/frameTicks)}:duration=${t}`);
  }
}
run('ffmpeg',[...common,...inputs,...maps,...codec,'-video_track_timescale',String(timeScale),'-movflags','+faststart+write_colr',temp]);
finish();
