// Text-only datasets already have a real silhouette. Check their decoded
// ink instead of making them carry empty rectangles to satisfy composition.
import {execFileSync} from 'node:child_process';
import assert from 'node:assert/strict';

const W=480,H=222;
export function verifySampleFrame(file,frame,fps,label){
  const t=Math.max(0,frame/fps-.000001).toFixed(6);
  const gray=execFileSync('ffmpeg',['-v','error','-xerror','-nostdin','-ss',t,'-i',file,
    '-map','0:v:0','-vf',`crop=iw:floor(ih*890/2160)*2:0:0,scale=${W}:${H}:flags=area,format=gray`,
    '-frames:v','1','-threads','1','-f','rawvideo','pipe:1']);
  assert.equal(gray.length,W*H,label+' 样本帧没解出来');
  let x=W,y=H,X=-1,Y=-1;
  for(let i=0;i<gray.length;i++){
    if(gray[i]<26)continue;
    const u=i%W,v=Math.floor(i/W);
    x=Math.min(x,u);X=Math.max(X,u);
    y=Math.min(y,v);Y=Math.max(Y,v);
  }
  const w=(X-x+1)/W,h=(Y-y+1)/H;
  const amount=`宽 ${(w*100).toFixed(1)}%，高 ${(h*100).toFixed(1)}%`;
  assert.ok(.65<=w&&w<=.8&&.55<=h&&h<=.75,label+' 真实样本占幅 '+amount+'；调样本间距、机位或取样，不加空框');
  console.log(label+' 真实样本占幅 '+amount);
}

export function verifySampleCut(cut,locate){
  let at=0;
  for(const row of cut.scenes){
    if(row.layout==='sample-text'){
      const {file,offset}=locate(row,at);
      for(const f of row.stableFrames)verifySampleFrame(file,f+offset,cut.fps,row.id+'+'+f);
    }
    at+=row.frames;
  }
}
