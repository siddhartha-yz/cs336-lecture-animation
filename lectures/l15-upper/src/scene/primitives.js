// Frame-driven artwork, drawn by the Remotion Canvas composition.
import {min,max,sum,len,range,zip,enumerate,round,getattr,any,all,at,slice,repeat,contains,fmt,printf,isclose,bisect_left,bisect_right} from '../values';
import {blend, clamp, mix} from '../board';
import {PALETTE,PAPER_EDGE} from '../theme/palette';
export {blend, clamp, mix};
export const {BLACK, WHITE, MUTED, AXIS, BLUE, CYAN, SKY, GOLD, AMBER, TEAL, GREEN, MINT, RED, ORANGE, MAGENTA, PINK, PURPLE, YELLOW, PAPER} = PALETTE;
export const RULE=AXIS, DIM=AXIS, INK=BLACK;

export function ease(x) {
  x = clamp(x);
  return (1 - ((1 - x) ** 3));
}
export function sine(x) {
  return (0.5 - (0.5 * Math.cos((Math.PI * clamp(x)))));
}
export function between(t, a, b) {
  return clamp(((t - a) / max(0.001, (b - a))));
}
export function pulse(t, a, span=0.42) {
  return Math.sin((Math.PI * between(t, a, (a + span))));
}
// An actual rectangular datum (bin, token, cell or solid), never a UI container.
export function solidBlock(g, x, y, w, h, color=BLUE, a=1) {
  g.rect(x, y, w, h, color, WHITE, 1.15, 0, a);
}
export function label(g, text, x, y, size=31, color=WHITE, a=1, align="center", font="sans", weight="normal") {
  g.text(text,x,y,size,color===MUTED?WHITE:color,a,align,font,weight);
}
export function sample(g, text, x, y, size=31, color=WHITE, a=1, align="center", font="sans") {
  g.rawText(text, x, y, size, color, a, align, font);
}
export function term(g, word, gloss, x, y, a=1, color=GOLD) {
  label(g, word, x, y, 36, color, a);
  glossary(g,gloss,x,y+46,a);
}
export function glossary(g,text,x,y,a=1){
  if(Array.from(text).length>16)throw Error("Glossary text exceeds one line");
  g.text(text,x,y,25,MUTED,a,"center","serif");
}
export function note(g, s, x=800, y=714, a=1, color=MUTED, align="center") {
  label(g, s, x, y, 24, color, a, align);
}
export function sampleLines(g, strings, x, y, gap=42, size=32, color=WHITE, a=1, align="left", font="sans") {
  for (const [i,s] of strings.entries()) sample(g, s, x, y+gap*i, size, color, a, align, font);
}
/** @param {string} c */
export function rule(g, x1, y, x2, c=RULE, a=1, w=1.4) {
  g.line(x1, y, x2, y, c, w, a);
}
export function bracket(g, x1, x2, y, c=GOLD, a=1, side=1) {
  g.poly([[x1, (y + (side * 8))], [x1, y], [x2, y], [x2, (y + (side * 8))]], c, 1.8, a);
}
export function slash(g, x, y, c=RED, a=1, r=10) {
  g.line((x - r), (y + r), (x + r), (y - r), c, 2, a);
}
export function arc_arrow(g, p0, p1, p2, p3, color=RED, p=1, a=1, w=3.5, head=15) {
  let dots, n;
  function pos(t) {
    let u;
    u = (1 - t);
    return Array.from((()=>{const __list29=[];for(const [x, y, z, r] of zip(p0, p1, p2, p3)){__list29.push((((((u ** 3) * x) + ((((3 * u) * u) * t) * y)) + ((((3 * u) * t) * t) * z)) + ((t ** 3) * r)));}return __list29;})());
  }
  if (((p <= 0) || (a <= 0))) {
    return;
  }
  n = max(2, Math.ceil((36 * p)));
  dots = (()=>{const __list30=[];for(const i of range((n + 1))){__list30.push(pos(((i * p) / n)));}return __list30;})();
  g.poly(dots, color, w, a);
  g.arrow(...pos(max(0,p-.035)), ...dots.at(-1),color,w,a,head);
}
export function highlight(g, x, y, w, h, c=GOLD, a=1) {
  g.rect(x,y,w,h,null,c,2.25,0,a);
}
// Text-bearing tokens use colored glass; measured bars and matrix cells stay solid.
export function blockInk(c) {return c===GOLD||c===SKY?BLACK:WHITE;}
export function glassBlock(g,x,y,w,h,c,a=1,hot=false) {
  if(blockInk(c)===BLACK){
    solidBlock(g,x,y,w,h,c,a);
  }else{
    g.rect(x,y,w,h,c,null,0,0,.38*a);
    g.rect(x,y,w,h,null,c,hot?2.6:1.85,0,a);
  }
}
export function chip(g,s,cx,cy,c=BLUE,w=64,h=54,a=1,hot=false) {
  if(a<=0)return;
  glassBlock(g,cx-w/2,cy-h/2,w,h,c,a,hot);
  const base=h>=80?31:25;
  const measured=g.measure(s,base,"mono");
  const size=Math.min(base,base*(w-14)/Math.max(1,measured));
  sample(g,s,cx,cy,size,blockInk(c),a,"center","mono");
}
export function axis(g, x, y, w, h, xlabel="", ylabel="", a=1) {
  g.arrow(x, y, (x + w), y, AXIS, 1.65, a, 9);
  g.arrow(x, y, x, (y - h), AXIS, 1.65, a, 9);
  if (xlabel) {
    label(g, xlabel, (x + w), (y + 26), 27, WHITE, a, "right");
  }
  if (ylabel) {
    label(g, ylabel, x, ((y - h) - 30), 27, WHITE, a, "left");
  }
}
export function question(g, lines, kicker="", a=1, color=GOLD) {
  let i, n, s;
  if (kicker) {
    label(g, kicker, 800, 276, 22, MUTED, a);
  }
  n = len(lines);
  for (const item of enumerate(lines)) {
    [i, s] = item;
    label(g, s, 800, (383 + ((i - ((n - 1) / 2)) * 73)), ((len(s) < 19) ? 55 : 50), WHITE, a);
  }
  rule(g, 765, 489, 835, color, a, 2.6);
}
/** @param {string} color */
export function ink_label(g, s, x, y, size, progress, color=WHITE, a=1, mode="pen") {
  g.write_text(s, x, y, size, color, a, clamp(progress), mode);
}
export function paperCutout(g, x, y, w, h, a=1) {
  g.rect(x,y,w,h,PAPER,PAPER_EDGE,1/1.2,0,a);
}
export function countdown(g, b, y=698, color=GOLD) {
  let r, t, w;
  if ((b.t < b.speech)) {
    return;
  }
  t = b.tick();
  [r,w]=y===698?[29,3.6]:(color===GOLD?[28,3.7]:[24,2.35]);
  g.circle(800, y, r, undefined, AXIS, 1.6);
  if ((t > 0)) {
    g.arc(800, y, r, ((-Math.PI) / 2), (((Math.PI*2) * t) - (Math.PI / 2)), color, w);
  }
}
// This depth is a small 2D offset, not a projected face. Text has its own level plane.
export function layeredBlock(g,x,y,w,h,d,c,name="",small="",a=1) {
  if(a<=0)return;
  const step=Math.min(8,d*.28);
  for(let k=2;k>=1;k--){
    g.rect(x+k*step,y-k*step,w,h,null,c,1.15,0,a*(k===2?.20:.41));
  }
  glassBlock(g,x,y,w,h,c,a);
  const ink=blockInk(c);
  if(name){
    const base=w>=220?40:31;
    const fit=Math.min(base,base*(w-40)/Math.max(1,g.measure(name,base)));
    label(g,name,x+w/2,y+h*(small?.39:.5),fit,ink,a);
  }
  if(small)label(g,small,x+w/2,y+h*.72,25,ink,a);
}
export function lock(g, x, y, c=BLUE, a=1, s=1) {
  solidBlock(g,x-12*s,y-2*s,24*s,18*s,c,a);
  g.arc(x, (y - (2 * s)), (8 * s), Math.PI, (2 * Math.PI), c, (2 * s), a);
}
// One parameter drives arc angle; the white radial edge is the exact split.
export function pieDial(g,x,y,r,p,c0=TEAL,c1=BLUE,a=1) {
  if(a<=0||r<=0)return;
  g.circle(x,y,r,c1,WHITE,1.15,a);
  const fraction=clamp(p);
  if(fraction<=0)return;
  const step=Math.ceil(fraction*80)+1;
  const points=[[x,y],...Array.from({length:step+1},(_,i)=>{
    const ang=-Math.PI/2+i/step*2*Math.PI*fraction;
    return [x+r*Math.cos(ang),y+r*Math.sin(ang)];
  })];
  g.poly(points,WHITE,1.15,a,true,c0,1);
}
