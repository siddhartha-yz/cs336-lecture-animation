// The share export uses libass. Measure its actual ink at phone width, not
// estimated character widths or a browser renderer with different metrics.
import {spawn} from 'node:child_process';
import {mkdtempSync,rmSync,symlinkSync,writeFileSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join,resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
import {captionAss,readCut} from './sidecars.mjs';

const W=480,H=270,SIZE=W*H;
function bounds(buffer){
  let left=W,top=H,right=-1,bottom=-1;
  for(let i=0;i<SIZE;i++){
    if(buffer[i]<24)continue;
    const x=i%W,y=Math.floor(i/W);
    left=Math.min(left,x);right=Math.max(right,x);
    top=Math.min(top,y);bottom=Math.max(bottom,y);
  }
  return [left,top,right,bottom];
}

export async function verifyCaptionFit(cut){
  const lines=new Map();
  for(const row of cut.scenes)
    for(const [start,,text] of row.captions)
      if(!lines.has(text))lines.set(text,`${row.id}+${start}f`);
  if(!lines.size)return;
  const rows=[...lines],folder=mkdtempSync(join(tmpdir(),'cs336-caption-fit-'));
  try{
    symlinkSync(resolve('public/fonts'),join(folder,'fonts'),'dir');
    writeFileSync(join(folder,'fit.ass'),captionAss(rows.map(([text],i)=>[i,i+1,text]),10));
    const p=spawn('ffmpeg',[
      '-v','error','-xerror','-nostdin','-f','lavfi','-i','color=c=black:s=1920x1080:r=10',
      '-vf','ass=fit.ass:fontsdir=fonts,scale=480:270:flags=area,format=gray',
      '-frames:v',String(rows.length),'-threads','1','-f','rawvideo','pipe:1',
    ],{cwd:folder,stdio:['ignore','pipe','inherit']});
    const ended=new Promise((ok,fail)=>{
      p.once('error',fail);
      p.once('close',code=>code===0?ok():fail(new Error('字幕像素检查需支持 libass 的 FFmpeg')));
    });
    const scan=async()=>{
      let n=0,maxWidth=0,remaining=Buffer.alloc(0);
      const bad=[];
      for await(const chunk of p.stdout){
        const bytes=Buffer.concat([remaining,chunk]);
        let offset=0;
        for(;offset+SIZE<=bytes.length;offset+=SIZE,n++){
          const [x,y,X,Y]=bounds(bytes.subarray(offset,offset+SIZE));
          maxWidth=Math.max(maxWidth,X-x+1);
          if(X<x||x<22||X>457||y<232||Y>265){
            const [text,at]=rows[n];
            bad.push(`${at} ${text}（手机帧墨迹 ${x},${y}–${X},${Y}）`);
          }
        }
        remaining=bytes.subarray(offset);
      }
      if(n!==rows.length||remaining.length)throw Error('字幕像素帧数不对，请核 FFmpeg');
      if(bad.length)throw Error(`${bad.length} 条字幕出了安全区；按实际口播拆成单行，别缩字号：\n${bad.slice(0,8).join('\n')}`);
      return `${n} 条不同字幕 · 480px 实压最宽 ${maxWidth}px`;
    };
    const [summary]=await Promise.all([scan(),ended]);
    console.log(summary);
  }finally{
    rmSync(folder,{recursive:true,force:true});
  }
}

if(process.argv[1]&&resolve(process.argv[1])===fileURLToPath(import.meta.url))
  await verifyCaptionFit(readCut());
