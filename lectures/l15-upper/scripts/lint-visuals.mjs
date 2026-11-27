// Compile-time guard for this production; the native frame audit handles dynamic text.
import fs from 'node:fs';
import path from 'node:path';
import ts from 'typescript';
const cut=JSON.parse(fs.readFileSync('src/data/cut.json'));
const policy=JSON.parse(fs.readFileSync('src/data/visual-policy.json'));
const err=[];
const banned=/(教学示意|教学算例|教学例|读图约值|示意图形|不按比例|核心结论|本节小结|关键洞察|来源口径|复剪包|讲义图|课堂举例|第[一二三四五六七八九十\d]+笔账|\b(?:Slide|Stage\s*0?\d+|Step\s*\d+|Phase\s+[A-Z])\b)/iu;
const shell=/^(?:panel|Card|InfoBox|TakeawayBanner|SlideTitle|Badge|FooterNote|theme_rect)$/i;
const palette='src/theme/palette.ts';
// The specification lives outside the artists' color table so an edited
// swatch cannot silently legitimize itself.
const expected={
 BLACK:'#000000', PAPER:'#F2F1EC', WHITE:'#FFFFFF', AXIS:'#666666', MUTED:'#B0B8C4',
 BLUE:'#19B5FE', CYAN:'#29ABCA', SKY:'#58C4DD', GOLD:'#FFD43B', AMBER:'#F5C731',
 YELLOW:'#FFFF00', TEAL:'#2EC492', GREEN:'#3DDC84', MINT:'#5CD0B3',
 ORANGE:'#F25C3B', RED:'#E84C5C', MAGENTA:'#DF5296', PINK:'#F462C0', PURPLE:'#B87BFF',
};
const swatches=fs.readFileSync(palette,'utf8');
const pairs=[...swatches.matchAll(/\b([A-Z]+):['"](#[0-9a-f]{6})['"]/gi)];
if(!swatches.includes('Object.freeze(')||pairs.length!==Object.keys(expected).length||
 new Set(pairs.map(([,role])=>role)).size!==pairs.length||
 pairs.some(([,role,color])=>expected[role]!==color.toUpperCase())||
 !/const PAPER_EDGE\s*=\s*['"]#C8C6BE['"]/.test(swatches))
 err.push(`${palette}: palette does not match the named constitution colors`);

const dirs=(d)=>fs.readdirSync(d,{withFileTypes:true}).flatMap(p=>p.isDirectory()?dirs(path.join(d,p.name)):[path.join(d,p.name)]);
for(const f of dirs('src').filter(f=>/\.[jt]sx?$/.test(f)&&f!==palette)){
 const file=ts.createSourceFile(f,fs.readFileSync(f,'utf8'),ts.ScriptTarget.Latest,true);
 const fail=(n,why)=>err.push(`${f}:${1+file.getLineAndCharacterOfPosition(n.getStart(file)).line} ${why}`);
 const sampleContext=(n)=>{
   for(let k=n.parent;k&&!ts.isSourceFile(k)&&!ts.isBlock(k);k=k.parent){
     if(ts.isCallExpression(k)&&/^(sample|sampleLines|rawText)$/.test(k.expression.getText(file)))return true;
     if(ts.isVariableDeclaration(k)&&/^(B_LINES|CORPUS|CRITIC_BRANCHES|EGG|FOUR|TOKENS)$/.test(k.name.getText(file)))return true;
   }
   return false;
 };
 const walk=(n,exempt=f==='src/Cover.tsx')=>{
   const called=ts.isCallExpression(n)?n.expression.getText(file):'';
   if(ts.isFunctionDeclaration(n)&&['opener_title','hook','phase_card'].includes(n.name?.text))exempt=true;
   const hasName=n.name?.getText?.(file);
   if(f==='src/Scenes.tsx'&&hasName==='questions')exempt=true;
   if(!exempt&&called==='prism')fail(n,'use flat model layers');
   if(shell.test(hasName??'')||shell.test(called))fail(n,'PPT shell');
   if(/\bborderRadius\b|\bbackdropFilter\b|\bboxShadow\b/.test(hasName??''))fail(n,'prohibited UI style');
   if(called==='g.rect'&&Number(n.arguments[7]?.getText(file))>=4&&!exempt)fail(n,'rounded body rectangle');
   if(!exempt&&/^(label|note)$/.test(called)&&n.arguments[1]&&ts.isStringLiteralLike(n.arguments[1])&&
     (n.arguments[1].text.match(/\p{Script=Han}/gu)??[]).length>policy.maxHanInSentence)fail(n,'use geometry instead of an explanation');
   if(ts.isStringLiteralLike(n)||ts.isTemplateLiteralToken(n)){
     const s=n.text;
     if(/#[0-9A-F]{3,8}\b|rgba?\s*\(|\b(?:slate-|zinc-|gray-[89]00)/i.test(s))fail(n,'literal color outside the production palette');
     if(banned.test(s)&&f!=='src/values.ts')fail(n,'editorial heading/watermark');
     if(!exempt&&!sampleContext(n)&&(s.match(/\p{Script=Han}/gu)??[]).length>18)fail(n,'long screen text');
   }
   ts.forEachChild(n,x=>walk(x,exempt));
 };
 walk(file);
}
let frames=0,lastPaper=-Infinity;
for(const s of cut.scenes){
 const f=s.frames-s.speech_end;
 if(policy.papers.includes(s.id)){
   if((frames-lastPaper)/cut.fps<policy.minPaperSeparationSeconds)err.push(`${s.id}: paper cutouts too close`);
   lastPaper=frames;
 }
 if(!policy.formatExempt.includes(s.id)){
   if(policy.holds.includes(s.id)){
     if(s.pause_frames!==4.5*cut.fps||f!==s.pause_frames)err.push(`${s.id}: audience hold must be exactly 4.5s`);
   }else if(!Number.isFinite(f)||f/cut.fps>policy.maxRoomToneTailSeconds||s.pause_frames)
     err.push(`${s.id}: missing narration clock or unplanned silence`);
 }
 if(s.title&&banned.test(s.title))err.push(`${s.id}: stale presentation title`);
 let prev=0;
 for(const [start,end,subtitle] of s.captions){
   if(banned.test(subtitle))err.push(`${s.id}: heading or watermark in captions`);
   if(!policy.formatExempt.includes(s.id)&&(start-prev)/cut.fps>policy.maxRoomToneTailSeconds)
     err.push(`${s.id}: a narration gap before frame ${start}`);
   prev=end;
 }
 frames+=s.frames;
}
if(err.length){console.error(err.join('\n'));process.exitCode=1;}
else console.log('Visual constitution: 0 violations in source and shot clocks.');
