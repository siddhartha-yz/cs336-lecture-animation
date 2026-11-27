import {staticFile} from 'remotion';
import {PALETTE as P} from './theme/palette';
import {plates} from './plates';
import {H,W} from './timeline';
import {clamp,type Pose,type Text} from './stage';

const fonts={
  math:'"Film Latin", "Film Chinese", serif',
  serif:'"Film Chinese", "Film Latin", serif',
  mono:'"Film Mono", "Film Chinese", monospace',
};
const images=new Map<string,HTMLImageElement>();
let ready:Promise<unknown>|undefined;
export function loadAssets(){
  const fonts=[
    ['Film Chinese','noto-serif-sc.woff'],
    ['Film Latin','latin-modern.otf'],
    ['Film Mono','mono.ttf'],
  ];
  return ready??=Promise.all([
    ...fonts.map(async ([family,file])=>{
      const f=await new FontFace(family,`url(${staticFile('fonts/'+file)})`).load();
      document.fonts.add(f);
    }),
    ...Object.entries(plates).map(async ([id,p])=>{
      const image=new Image();
      image.src=staticFile('plates/'+p.file);
      await image.decode();
      if(p.kind==='raster'&&(image.naturalWidth!==p.pixels[0]||image.naturalHeight!==p.pixels[1]))
        throw Error('Unexpected plate dimensions for '+id);
      images.set(id,image);
    }),
  ]);
}

function text(g:CanvasRenderingContext2D,m:Text){
  const {value,x,y,size,align,font,a,rise,color}=m;
  g.save();g.translate(x,y);g.scale(size/128,size/128);
  g.font=`${m.weight} 128px ${fonts[font]}`;
  g.textAlign='left';g.textBaseline='alphabetic';g.fillStyle=color;
  const line=g.measureText(value);
  const l=-line.width*({left:0,center:.5,right:1}[align]);
  const y0=(line.actualBoundingBoxAscent-line.actualBoundingBoxDescent)*.5;
  const alpha=g.globalAlpha*clamp(a);
  if(rise>=1){
    g.globalAlpha=alpha;
    g.fillText(value,l,y0);
  }else{
    const glyphs=Array.from(value),delay=Math.min(.47,.04*(glyphs.length-1));
    let prefix='';
    for(const [i,char] of glyphs.entries()){
      const on=1-(1-clamp((rise-delay*i/Math.max(1,glyphs.length-1))/(1-delay)))**3;
      g.globalAlpha=alpha*on;
      if(on)g.fillText(char,l+g.measureText(prefix).width,y0+128*.15*(1-on));
      prefix+=char;
    }
  }
  g.restore();
}

export function paint(g:CanvasRenderingContext2D,poses:Pose[],width:number,height:number){
  g.setTransform(width/W,0,0,height/H,0,0);
  g.globalAlpha=1;g.fillStyle=P.bg;g.fillRect(0,0,W,H);
  g.lineCap='round';g.lineJoin='round';
  for(const p of poses){
    g.save();
    if(p.iris){
      g.beginPath();g.arc(p.iris.x,p.iris.y,p.iris.radius,0,2*Math.PI);g.clip();
    }
    if(p.camera){
      const {scale,dx,dy,pivot:[x,y]}=p.camera;
      g.translate(x+dx,y+dy);g.scale(scale,scale);g.translate(-x,-y);
    }
    for(const m of p.marks){
      if(m.kind==='text'){g.globalAlpha=1;text(g,m);continue;}
      if(m.kind==='plate'){
        const image=images.get(m.id);
        if(!image)throw Error('Undeclared artwork: '+m.id);
        g.globalAlpha=clamp(m.a);
        if(m.reveal<1){
          const [x,y,w,h]=m.box;
          g.save();g.beginPath();g.rect(x,y,w*m.reveal,h);g.clip();
          g.drawImage(image,...m.box);g.restore();
        }else g.drawImage(image,...m.box);
        continue;
      }
      g.globalAlpha=clamp(m.a);
      if(m.kind==='dot'){
        g.beginPath();g.arc(m.x,m.y,m.r,0,2*Math.PI);
        g.fillStyle=m.color;g.fill();continue;
      }
      g.lineWidth=m.st;
      if(m.kind==='rect'){
        if(m.fill){
          g.fillStyle=m.fill;
          g.globalAlpha=clamp(m.a)*(m.material==='glass'?.38:1);g.fillRect(...m.box);
        }
        if(m.line){
          g.strokeStyle=m.line;g.globalAlpha=clamp(m.a);
          g.setLineDash(m.dashed?[11,9]:[]);
          g.strokeRect(...m.box);g.setLineDash([]);
        }
      }else if(m.kind==='line'){
        const [x,y,a,b]=m.dots;
        g.beginPath();g.moveTo(x,y);g.lineTo(a,b);
        if(m.arrow&&Math.hypot(a-x,b-y)>6){
          const q=Math.atan2(b-y,a-x);
          g.moveTo(a-10*Math.cos(q-.53),b-10*Math.sin(q-.53));g.lineTo(a,b);
          g.lineTo(a-10*Math.cos(q+.53),b-10*Math.sin(q+.53));
        }
        g.setLineDash(m.dashed?[11,9]:[]);g.strokeStyle=m.color;g.stroke();g.setLineDash([]);
      }else if(m.kind==='path'){
        g.beginPath();
        for(const [i,[x,y]] of m.points.entries()){if(i)g.lineTo(x,y);else g.moveTo(x,y);}
        g.setLineDash(m.dashed?[11,9]:[]);g.strokeStyle=m.color;g.stroke();g.setLineDash([]);
      }else{
        g.beginPath();g.arc(m.x,m.y,m.r,-Math.PI/2,2*Math.PI*m.t-Math.PI/2);
        g.strokeStyle=m.color;g.stroke();
      }
    }
    g.restore();
  }
}
