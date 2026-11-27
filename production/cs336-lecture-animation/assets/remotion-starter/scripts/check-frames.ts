import assert from 'node:assert/strict';
import {writeFileSync} from 'node:fs';
import {posesFor} from '../src/story';
import {ART_BOTTOM,captionAt,cut,FPS,FORMAT_EXEMPT,H,rows,W} from '../src/timeline';
import {PALETTE as P,PAPER_EDGE} from '../src/theme/palette';
import {plates} from '../src/plates';
import type {Camera, Mark} from '../src/stage';

const banned=/(教学示意|教学算例|教学例|读图约值|示意图形|不按比例|核心结论|本节小结|关键洞察|来源口径|复剪包|讲义|课程幻灯|课堂举例|第[一二三四五六七八九十\d]+笔账|\b(?:Slide|Stage\s*\d+|Step\s*\d+|Phase\s+[A-Z])\b)/iu;
const han=(s:string)=>(s.match(/\p{Script=Han}/gu)??[]).length;
const cjk=/[\p{Script=Han}\u3000-\u303F\uFF01-\uFF60]/gu;
const glyphs=new Set<string>();
const glyph=(s:string)=>{for(const c of s.match(cjk)??[])glyphs.add(c);};
const swatches=new Set<string>(Object.values(P));
let clock=0,formulaAlone=0;
const geometryErrors:string[]=[];
function visibility(m:Mark){return m.a>=.13;}
function transform(x:number,y:number,c?:Camera){
  return c?[c.pivot[0]+c.dx+(x-c.pivot[0])*c.scale,c.pivot[1]+c.dy+(y-c.pivot[1])*c.scale]:[x,y];
}

for(const row of cut.scenes){
  if(row.opens_into){
    const target=rows[row.opens_into.id];
    const entry=posesFor(target,0).filter(p=>p.marks.length);
    assert.ok(entry.some(p=>p.marks.some(visibility)),row.id+' 门后第 0 帧没有可见正文；不要再从黑渐入');
    const landing=posesFor(row,row.frames-1).filter(p=>p.marks.length).map(({iris,...p})=>{
      if(iris){
        const {x,y,radius}=iris;
        const corner=Math.hypot(Math.max(x,W-x),Math.max(y,H-y));
        assert.ok(radius>=corner,row.id+' 最后一帧的开门遮罩未退出画布');
      }
      return p;
    });
    assert.deepEqual(landing,entry,row.id+' 最后一帧必须落到下一镜实际第 0 帧，不留章门文字或仿制画面');
  }
  let paperFrames=0, captionWithoutArt=0, glossary=new Map<string,number>();
  const stable=new Set(row.stableFrames??[]);
  const exempt=FORMAT_EXEMPT.has(row.kind);
  for(const [,,t] of row.captions)glyph(t);
  for(let frame=0;frame<row.frames;frame++){
    const poses=posesFor(row,frame),at=`${row.id}+${frame}`;
    const inHold=!!row.hold&&row.hold.start<=frame&&frame<row.hold.start+row.hold.frames;
    const clearing=frame<(row.black_head??0)||frame>=row.frames-(row.black_tail??0);
    const hasArt=poses.some(p=>p.marks.some(visibility));
    captionWithoutArt=!exempt&&!clearing&&!hasArt&&captionAt(row,frame)?captionWithoutArt+1:0;
    assert.ok(captionWithoutArt<=24,at+' 字幕已经进来，但正文画面连续空了超过 0.4 秒');
    let budget=0, timer=0, paper=0, question=0, sampleLines=0, hasFormula=false, subject=[Infinity,Infinity,-Infinity,-Infinity];
    const notes=new Set<string>();
    const put=(x:number,y:number,w:number,h:number,c?:Camera)=>{
      const [a,b]=transform(x,y,c),[d,e]=transform(x+w,y+h,c);
      subject=[Math.min(subject[0],a),Math.min(subject[1],b),Math.max(subject[2],d),Math.max(subject[3],e)];
    };
    for(const pose of poses)for(const m of pose.marks){
      if(m.kind==='text')glyph(m.value);
      if(exempt)continue;
      assert.ok(!pose.iris,at+' 正文不可借章门豁免');
      assert.ok(m.a>=0&&m.a<=1&&Number.isFinite(m.a),at+' 透明度');
      if(m.kind==='text'){
        const {value,color}=m;
        assert.ok(swatches.has(color),at+' 文字没有走色板：'+value);
        assert.ok(!banned.test(value),at+' 内部字样：'+value);
        assert.ok(m.role!=='format',at+' 正文禁止章卡文字');
        if(m.role==='question')assert.ok(row.kind==='question'&&++question===1,at+' 正文多了一个屏上问句');
        else assert.ok(m.size>=(m.role==='source'?18:20),at+' 辅助字号低于底线：'+value);
        assert.ok(Number.isFinite(m.x)&&Number.isFinite(m.y)&&Number.isFinite(m.size),at+' 字形坐标无效');
        if(!visibility(m))continue;
        if(m.role==='sample')sampleLines++;
        if(m.role==='formula')hasFormula=true;
        for(const box of pose.marks){
          if(box.kind!=='rect'||!box.material||box.material==='paper'||!visibility(box))continue;
          const [x,y,w,h]=box.box;
          if(!(x<=m.x&&m.x<=x+w&&y<=m.y&&m.y<=y+h))continue;
          if(box.material==='glass')assert.equal(color,P.white,at+' 载字琉璃上用白字：'+value);
          else{
            assert.ok(!han(value)&&['number','formula'].includes(m.role),at+' 实心数据体不载结构文字');
            if(color===P.bg)assert.ok((box.fill===P.gold||box.fill===P.lightCyan),at+' 深色实心块上不能写黑字');
          }
        }
        if(m.role==='gloss'){
          assert.ok(Array.from(value).length<=16&&!value.includes('\n')&&color===P.gloss,at+' 术语注解越界');
          notes.add(value);
        }else assert.ok(color!==P.gloss,at+' 灰色注解色只给新术语');
        if(m.role==='anchor')assert.ok(han(value)<=12&&!/[。！!？?]/.test(value),at+' 结构锚点不是复述句：'+value);
        if(m.role==='formula'||m.role==='number')assert.equal(han(value),0,at+' 解释不能藏进公式或数值区');
        if(m.role!=='sample'&&m.role!=='formula'&&m.role!=='number'&&m.role!=='question')budget+=han(value);
        const [,py]=transform(m.x,m.y,pose.camera);
        assert.ok(py+m.size*.63*(pose.camera?.scale??1)<=ART_BOTTOM,at+' 字或公式进了字幕缓冲区：'+value);
        if(m.role==='source'&&row.paper){
          assert.equal(value,row.paper.source,at+' 纸面出处不一致');
          assert.equal(m.font,'serif',at+' 纸面出处请用衬线');
        }
      }else if(m.kind==='rect'){
        assert.ok(m.box.every(Number.isFinite)&&m.box[2]>0&&m.box[3]>0,at+' 矩形非法');
        if(m.fill)assert.ok(swatches.has(m.fill),at+' 形状用了非法填色');
        if(m.line)assert.ok(swatches.has(m.line)||(m.material==='paper'&&m.line===PAPER_EDGE),at+' 非法描边颜色');
        if(m.material==='paper'){
          assert.ok(row.paper&&++paper===1,at+' 纸面只能用于带真实来源的切面');
        }else assert.ok(m.fill!==P.paper,at+' 米白只用于文献切面');
        if(visibility(m)){
          assert.ok(transform(0,m.box[1]+m.box[3]+m.st/2,pose.camera)[1]<=ART_BOTTOM,at+' 结构块侵入字幕缓冲区');
        }
        if(m.main&&visibility(m)){
          put(...m.box,pose.camera);
        }
      }else if(m.kind==='plate'){
        const src=plates[m.id],k=pose.camera?.scale??1;
        assert.ok(src,at+' 图板未声明：'+m.id);
        const [x,y,w,h]=m.box;
        assert.ok(w>0&&h>0&&m.box.every(Number.isFinite),at+' 图板尺寸错误');
        if(src.kind==='raster')
          assert.ok(w*k<=src.pixels[0]+.001&&h*k<=src.pixels[1]+.001,at+' 位图必须从原材料高分重裁，不能放大：'+m.id);
        assert.ok(Math.abs(w/h-src.pixels[0]/src.pixels[1])/(w/h)<.018,at+' 图板比例被拉伸');
        assert.ok(transform(x+w,y+h,pose.camera)[1]<=ART_BOTTOM,at+' 图板进了字幕缓冲');
        if(m.main&&visibility(m))put(x,y,w,h,pose.camera);
        if(m.role==='formula'&&visibility(m))hasFormula=true;
      }else if(m.kind==='line'||m.kind==='arc'||m.kind==='path'||m.kind==='dot'){
        assert.ok(swatches.has(m.color),at+' 路径没有走色板');
        if(visibility(m)){
          if(m.kind==='path'||m.kind==='line'){
            const points=m.kind==='line'?[[m.dots[0],m.dots[1]],[m.dots[2],m.dots[3]]]:m.points;
            for(const [x,y] of points){
              assert.ok(Number.isFinite(x)&&Number.isFinite(y)&&transform(x,y+m.st/2+(m.kind==='line'&&m.arrow?10:0),pose.camera)[1]<=ART_BOTTOM,at+' 路径进了字幕缓冲');
              if(m.main)put(x,y,0,0,pose.camera);
            }
          }else{
            assert.ok(transform(0,m.y+m.r+(m.kind==='arc'?m.st/2:0),pose.camera)[1]<=ART_BOTTOM,at+' 点或圆弧进了字幕缓冲');
            if(m.kind==='dot'&&m.main)put(m.x-m.r,m.y-m.r,2*m.r,2*m.r,pose.camera);
          }
        }
        if(m.kind!=='arc'||!m.timer)continue;
        assert.ok(m.color===P.gold&&m.x===W/2&&m.y>=760&&++timer===1,at+' 需要底部中央金色圆弧');
      }
    }
    assert.ok(budget<=20,at+' 正文解释汉字 '+budget+'/20');
    assert.equal(Boolean(timer),inHold,at+' 金色进度弧和观众思考时钟不相符');
    if(paper)paperFrames++;
    for(const s of notes)glossary.set(s,(glossary.get(s)??0)+1);
    formulaAlone=(!exempt&&hasFormula&&!Number.isFinite(subject[0]))?formulaAlone+1:0;
    if(cut.format==='derivation')assert.ok(formulaAlone<=25*FPS,at+' 超过25秒没有联动的数值/几何装置');
    if(stable.has(frame)){
      if(row.layout==='sample-text'){
        assert.ok(sampleLines>=4&&!inHold,at+' 为四行以上真实样本选完整稳定帧；不要把计时弧算入构图');
      }else{
        const [x,y,X,Y]=subject,w=(X-x)/W,h=(Y-y)/ART_BOTTOM;
        if(!(w>=.65&&w<=.80&&h>=.55&&h<=.75&&x>=0&&X<=W&&y>=0&&Y<=ART_BOTTOM))
          geometryErrors.push(at+` 主装置占幅宽 ${(w*100).toFixed(1)}%，高 ${(h*100).toFixed(1)}%`);
      }
    }
  }
  assert.equal(Boolean(paperFrames),Boolean(row.paper),row.id+' 纸面标注与实际渲染不一致');
  for(const [s,count] of glossary)assert.ok(count>=4*FPS,row.id+' 术语注解不足四秒：'+s);
  clock+=row.frames;
}
assert.equal(geometryErrors.length,0,geometryErrors.join('\n'));
writeFileSync(process.argv[2],JSON.stringify([...glyphs]));
console.log(`Frame contract: ${clock} frames, ${glyphs.size} distinct CJK/full-width glyphs.`);
