import {readFileSync,mkdirSync,writeFileSync} from 'node:fs';
import {join,resolve} from 'node:path';
import {fileURLToPath} from 'node:url';

const examples={
  c10:'SFT：一个词的概率变大，损失 2.303 → 1.966',
  c17:'注意力掩码：B₁、B₂ 各拿 0.5',
  c22:'Bradley–Terry：两边同加 2，胜率不动',
  c23:'奖励模型：两对样本的平均损失 0.857 → 0.308',
  c28:'KL：答法不变，只换概率，0.105 → 0.040',
  c32:'Critic：三条续写的期望回报是 3',
};
const assHead=`[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Chinese,Noto Serif CJK SC,64,&H00F4F4F4,&H00F4F4F4,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,1.6,0,2,96,96,52,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
`;
const pad=(v,n)=>String(v).padStart(n,'0');
const halfEven=(n,d)=>{
  const q=Math.floor(n/d),r=n-q*d;
  return 2*r===d?q+(q%2):q+(Number(2*r>d));
};
const split=(n,d)=>[Math.floor(n/d),n%d];
function clock(frame,fps,ass=false){
  const unit=ass?100:1000;
  // ASS time steps sit between the preceding frame and each visible boundary.
  const t=ass?halfEven(Math.max(0,2*frame-1)*unit,2*fps):Math.floor(frame*unit/fps);
  const [h,r]=split(t,3600*unit);
  const [m,q]=split(r,60*unit);
  const [s,f]=split(q,unit);
  return ass?`${h}:${pad(m,2)}:${pad(s,2)}.${pad(f,2)}`:`${pad(h,2)}:${pad(m,2)}:${pad(s,2)},${pad(f,3)}`;
}
const brief=(frame,fps)=>{
  const [m,s]=split(halfEven(frame*1000,fps),60000);
  const [a,b]=split(s,1000);
  return `${pad(m,2)}:${pad(a,2)}.${pad(b,3)}`;
};
const ff=(s)=>s.replaceAll('\n',' ').replace(/[;#=\\]/g,'\\$&');
const ass=(s)=>s.replaceAll('{','｛').replaceAll('}','｝').replaceAll('\\','＼').replaceAll('\n','\\N');
const csv=(v)=>/[,"\r\n]/.test(String(v))?'"'+String(v).replaceAll('"','""')+'"':String(v);
const rememberTable=(lines)=>lines.map(r=>r.map(csv).join(',')).join('\r\n')+'\r\n';

export const readCut=()=>JSON.parse(readFileSync('src/data/cut.json','utf8'));

export function writeSidecars(cut,dir,{guide=false}={}){
  const chapters=[],captions=[],scenes=[],caseIndex=[];
  let at=0;
  for(const row of cut.scenes){
    const frames=row.frames;
    if(row.chapter)chapters.push([at,row.chapter]);
    if(examples[row.id]&&row.cues.calc!==undefined)caseIndex.push([at+row.cues.calc,examples[row.id]]);
    scenes.push([row.id,brief(at,cut.fps),row.title??row.chapter??'片头或章卡',frames]);
    let end=0;
    for(const [from,to,text] of row.captions){
      if(from<end||to>frames||from>=to||!text)throw Error(`字幕超出镜长或重叠：${row.id}`);
      captions.push([at+from,at+to,text]);end=to;
    }
    at+=frames;
  }
  const {fps,title}=cut;
  const srt=captions.map(([a,b,t],i)=>`${i+1}\n${clock(a,fps)} --> ${clock(b,fps)}\n${t}`).join('\n\n')+'\n';
  const assText=assHead+captions.map(([a,b,t])=>`Dialogue: 0,${clock(a,fps,true)},${clock(b,fps,true)},Chinese,,0,0,0,,${ass(t)}\n`).join('');
  const ffm=[';FFMETADATA1',`title=${ff(title)}`,...chapters.flatMap(([a,name],i)=>
    ['[CHAPTER]',`TIMEBASE=1/${fps}`,`START=${a}`,`END=${chapters[i+1]?.[0]??at}`,`title=${ff(name)}`])].join('\n')+'\n';
  mkdirSync(dir,{recursive:true});
  const write=(name,text)=>writeFileSync(join(dir,name),text);
  write('captions.srt',srt);write('captions.ass',assText);write('chapters.ffmeta',ffm);
  if(guide){
    write('镜表.csv','\ufeff'+rememberTable([['镜号','绝对入点（分:秒.毫秒）','内容','帧数'],...scenes]));
    const marks=(list)=>list.map(([t,name])=>`${brief(t,fps).replace(/\.\d{3}$/,'')}  ${name}`).join('\n')+'\n';
    write('章节.txt',marks(chapters));write('六段算例.txt',marks(caseIndex));
  }
  return {frames:at,chapters:chapters.length,captions:captions.length};
}
if(process.argv[1]&&resolve(process.argv[1])===fileURLToPath(import.meta.url)){
  const dir=process.argv[2]??'docs';
  const result=writeSidecars(readCut(),dir,{guide:true});
  console.log(dir,result);
}
