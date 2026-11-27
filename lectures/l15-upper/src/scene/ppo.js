import FORM_ANCHORS from '../data/math-anchors.json';
import OST from '../data/ost.json';
// Frame-driven artwork, drawn by the Remotion Canvas composition.
import {min,max,sum,len,range,zip,enumerate,round,getattr,any,all,at,slice,repeat,contains,fmt,printf,isclose,bisect_left,bisect_right} from '../values';
import {BLACK, WHITE, MUTED, DIM, RULE, INK, BLUE, GOLD, TEAL, GREEN, RED, PURPLE, YELLOW, PAPER, AXIS, CYAN, SKY, ORANGE, MAGENTA, PINK, ease, sine, between, pulse, solidBlock, sample, label, term, glossary, note, sampleLines, rule, bracket, slash, arc_arrow, highlight, chip, axis, question, ink_label, paperCutout, pieDial, countdown, layeredBlock, blockInk, glassBlock, lock, layer, aperture, phase_card, picture, mathform, form_segment, move_segment, blend, mix, clamp} from '../stage';
import {referenceMark} from './engineering';
import {sigmoid} from './preference';
import {REFERENCE, expected_score, kl as calc_kl} from './examples';

// The tether, what PPO needs to run, and the final held question.
export function tether(g, x0, x1, y, travel, a=1) {
  let i, n, points, span, u, yy;
  n = 63;
  span = max(2, (x1 - x0));
  points = [];
  for (const item of range(n)) {
    i = item;
    u = (i / (n - 1));
    yy = (y + ((((1 - (travel * 0.63)) * 15) * Math.sin(((Math.PI * u) * 18))) * (Math.sin((Math.PI * u)) ** 0.7)));
    points.push([(x0 + (u * span)), yy]);
  }
  g.poly(points, blend(GOLD, RED, (0.72 * travel)), 3.8, a);
}
export function kl_tether(g, b) {
  let _, aux, away, begin, beta, box, c, cx, eq, half, kl, left, lim, meter, p, prior, ref, reward, rope, run, s, tag, title, v, x;
  ref = max(0.65, b.fade("ref", 0.47));
  rope = (b.fade("rope", 0.57) * b.fade("ref", 0.39));
  eq = b.fade("eq", 0.57);
  beta = b.fade("beta", 0.95);
  lim = b.fade("limit", 0.69);
  reward = b.fade("reward", 0.5);
  kl = b.fade("kl", 0.59);
  meter = b.fade("meter", 0.71);
  away = b.fade("away", 1.07);
  begin = b.at("calc");
  aux = b.ent(0.48, begin);
  prior=1-b.ent(.28,begin-.68);
  { const restore = layer(g, (prior * b.gone()));
    try {
      left = 324;
      run = b.fade("reward", 3.25);
      x = ((((left + 170) + (580 * run)) - (350 * beta)) + ((68 * away) * (1 - beta)));
      g.poly([[922, 406], [1004, 382], [1091, 358], [1151, 321], [1211, 245], [1298, 315], [1388, 409]], GOLD, 2.2, rope, false);
      g.circle(1211, 245, 6, GOLD, undefined, undefined, rope);
      label(g, "高奖励", 1211, 204, 32, GOLD, rope);
      if (ref) {
        referenceMark(g, left, 362, 0.77, ref);
      }
      g.line((left - 89), 436, (left + 106), 436, BLUE, 1.7, ref);
      g.circle(x,375,30,TEAL,WHITE,1.15,rope);
      mathform(g, "pi", x, 302, 38, 112, TEAL, rope);
      g.circle((left + 67), 375, 4.5, BLUE, undefined, undefined, ref);
      tether(g, (left + 67), mix((left + 69), (x - 31), rope), 375, run, rope);
      mathform(g, "full-rl", 800, 562, 65, 1420, WHITE, eq, min(1, (eq * 1.3)));
      for (const item of [["reward","奖励",GOLD,reward],["penalty","KL",RED,kl]]) {
        [tag, title, c, p] = item;
        if ((!p)) {
          continue;
        }
        [cx, _, s] = form_segment("full-rl", tag, 800, 562, 65, 1420);
        box = at(FORM_ANCHORS, tag);
        half = (((at(box, 2) - at(box, 0)) * s) / 2);
        rule(g, (cx - half), 625, (cx + half), c, p, 2.45);
        label(g, title, cx, 665, 31, c, p);
      }
      if ((meter && (!lim))) {
        v = (meter * (1 - lim));
        bracket(g, (left + 75), max((left + 76), (x - 31)), 451, GOLD, v, (-1));
        label(g,"Dₖₗ",max(left+130,(left+75+x)/2),481,35,GOLD,v,undefined,"math");
      }
      if ((kl && (!lim))) {
        glossary(g,"衡量分布偏离",801,715,Math.min(kl,1-lim));
      }
      if (beta) {
        label(g, "β ↑", 592, 194, 35, GOLD, beta, undefined, "math");
        g.arrow(604, 235, 604, 276, GOLD, 2.1, beta);
      }
    } finally { restore(); }
  }
  if (aux) {
    kl_bars(g, b, (aux * b.gone()));
  }
}
export function kl_bars(g, b, a) {
  let back, c, cur, first, gaps, i, j, k, p, pp, q, q0, ref, result, s, terms, title, u, v, values, vis, w, widths, x, xx, z;
  first=sine(between(b.t,b.at("diff0"),b.at("diff0")+.15));
  back=sine(between(b.t,b.at("diff1"),b.at("diff1")+.18));
  q = ((0.8 - (0.2 * first)) + (0.08 * back));
  pp=[q,1-q];
  k = calc_kl(pp, REFERENCE);
  ref = max((0.59 * b.fade("calc", 0.68)), b.fade("refp", 0.54));
  cur=b.fade("calc",.67);
  result = b.fade("kl0", 0.42);
  { const restore = layer(g, a);
    try {
      for (const item of enumerate([[REFERENCE,BLUE,"reff",ref],[pp,TEAL,"pi",cur]])) {
        [j, [values, c, title, vis]] = item;
        x = (414 + (j * 745));
        axis(g, (x - 208), 577, 445, 298, "", "", vis);
        mathform(g,title,x,217,57,185,c,vis);
        for (const item of enumerate(values)) {
          [i, v] = item;
          xx = ((x - 97) + (192 * i));
          const hue=j===1&&i===1?PINK:c;
          solidBlock(g,xx-60,577-v*282,120,v*282,hue,vis);
          label(g,`${fmt(v,".2f")}`,xx,550-v*282,36,hue,vis,undefined,"math");
          label(g,at(["A","B"],i),xx,612,28,WHITE,vis,undefined,"math");
        }
      }
            pieDial(g,800,270,52,q,TEAL,PINK,result);
      const X=p=>684+(p-.50)/.45*236,Y=div=>548-405*div;
      axis(g,684,548,244,125,"","",result);
      const trajectory=Array.from({length:61},(_,i)=>{
        const p=.50+.45*i/60;
        return [X(p),Y(calc_kl([p,1-p],REFERENCE))];
      });
      g.poly(trajectory,TEAL,2.65,result);
      g.line(X(q),Y(k),X(q),548,GOLD,1.25,result,[4,4]);
      g.circle(X(q),Y(k),6,WHITE,TEAL,1.15,result);
      label(g,`KL = ${fmt(k,".3f")}`,800,373,48,GOLD,result,undefined,"math");
      const glow=b.fade("kl1",.28);
      rule(g,699,410,699+203*glow,GOLD,glow,1.8);
      if (result) {
        [p, q0] = pp;
        [u, v] = REFERENCE;
        terms = [[`${fmt(p, `.2f`)}`, TEAL], ["ln(", WHITE], [`${fmt(p, `.2f`)}`, TEAL], ["/", WHITE], [`${fmt(u, `.2f`)}`, BLUE], [")", WHITE], [" + ", WHITE], [`${fmt(q0, `.2f`)}`, PINK], ["ln(", WHITE], [`${fmt(q0, `.2f`)}`, PINK], ["/", WHITE], [`${fmt(v, `.2f`)}`, BLUE], [")", WHITE]];
        widths = (()=>{const __list19=[];for(const [s, _] of terms){__list19.push(g.measure(s, 40, "math"));}return __list19;})();
        gaps = [14, 4, 4, 4, 5, 24, 24, 14, 4, 4, 4, 5, 0];
        x = (800 - ((sum(widths) + sum(gaps)) / 2));
        for (const item of zip(terms, widths, gaps)) {
          [[s, c], w, z] = item;
          label(g, s, x, 704, 40, c, result, "left", "math");
          x += (w + z);
        }
      }
    } finally { restore(); }
  }
}
export function innocuous(g, b) {
  let before, end, exit_, p, quote;
  p = b.fade("paper", 0.55);
  quote = b.fade("quote", 0.63);
  exit_ = b.fade("bill", 0.47);
  before = (1 - b.ent(0.25, (b.at("paper") - 0.39)));
  end = (1 - b.ent(0.28, (b.at("bill") - 0.43)));
  { const restore = layer(g, b.gone());
    try {
      if (before) {
        { const restore = layer(g, (before * b.ent(0.48)));
          try {
            mathform(g, "full-rl", 800, 350, 81, 1430);
          } finally { restore(); }
        }
      }
      if ((p && end)) {
        { const restore = layer(g, (p * end), (42 * (1 - p)), undefined, (1 + (0.028 * quote)), [800, 414]);
          try {
            paperCutout(g, 205, 148, 1190, 590);
            label(g, "3.5   Reinforcement learning", 277, 214, 48, INK, undefined, "left", "serif");
            rule(g, 277, 263, 1326, AXIS, undefined, 1.45);

            picture(g,"instruct-eq2",272,325,1055);
            label(g, "Ouyang et al., 2022", 1309, 552, 23, BLACK, undefined, "right", "serif");
            label(g, "“this is very innocuous looking”", 791, 627, 37, INK, quote, undefined, "serif");
            rule(g, 552, 659, (552 + (478 * quote)), RED, quote, 2.5);
            label(g, "Tatsunori Hashimoto", 1293, 694, 21, BLACK, quote, "right", "serif");
          } finally { restore(); }
        }
      }
      if (exit_) {
        mem_budget(g,1,0,[0,0,0,0],0,exit_);
      }
    } finally { restore(); }
  }
}
export const MODEL_C = [TEAL, PURPLE, BLUE, GOLD];
export const NAMES = ["Actor", "Critic", "Reference", "Reward Model"];
export const ROLES=["训练","训练","冻结","冻结"];
export const SIZE_PROFILE=[1,.86,.73,.69];
const UNIT_SIZES=[1,1,1,1];

export function stack(g,x,y,w,h,d,c,a,name,role,cost,show_role=1,show_name=1,callouts=false){
  layeredBlock(g,x,y,w,h,d,c,"","",a);
  const ink=blockInk(c),size=Math.min(40,40*(w-40)/Math.max(1,g.measure(name,40)));
  label(g,name,x+w/2,y+h*(show_role>.05?.40:.50),size,ink,a*show_name);
  if(role)label(g,role,x+w/2,y+h*.72,27,ink,a*show_role);
  if(!cost)return;
  const notes=[];
  for(const [i,[word,hue]] of [["梯度",c],["优化器",GOLD]].entries()){
    const u=ease(cost*1.45-i*.36);
    if(!u)continue;
    const yy=y-56-i*53-22*(1-u);
    // Flat storage slices, with padding between them and no interior labels.
    solidBlock(g,x,yy,w,26,hue,u*a);
    for(let j=1;j<=3;j++){
      const xx=x+w*j/4;
      g.line(xx,yy+4,xx,yy+22,blockInk(hue),1.1,.26*u*a);
    }
    notes.push([word,yy+13,hue,u*a]);
  }
  if(callouts){
    for(const [word,cy,hue,opacity] of notes){
      label(g,word,x-41,cy,31,WHITE,opacity,"right");
      g.line(x-32,cy,x-6,cy,hue,2.4,opacity);
      g.circle(x-6,cy,2.3,hue,null,0,opacity);
    }
  }
}
// Shrink in place, then bring each weight through its own corridor.
export function role_pose(i,u){
  const move=(a,b,k,l)=>mix(a,b,sine(between(u,k,l)));
  const shrink=sine(between(u,0,.29));
  const x0=254+441*(i%2),y0=335+226*Math.floor(i/2);
  let x,y;
  if(i===0){
    x=move(x0,186,.29,.58); y=move(y0,310,.29,.58);
  }else if(i===1){
    x=move(x0,1170,.30,.57); y=move(y0,516,.58,.83);
  }else if(i===2){
    x=u<.50?move(x0,490,.31,.49):move(490,1170,.75,1);
    y=move(y0,245,.48,.75);
  }else{
    x=move(x0,1170,.69,1); y=move(y0,380,.46,.66);
  }
  return [x,y,mix(327,217,shrink),mix(143,83,shrink),mix(16,13,shrink)];
}
export function model_rig(g,p=[1,1,1,1],sft=0,cost=1,advance=0,sizes=UNIT_SIZES,labels=1){
  for(const [i,c] of MODEL_C.entries()){
    const [x,base,w,h,d]=role_pose(i,advance);
    if(!i&&sft)stack(g,x,base,327,143,16,BLUE,sft,"SFT","可训练",sft*.65,1,1,true);
    if(!p[i])continue;
    const y=base-(1-p[i])*70*(1-advance);
    const restore=layer(g,1,0,0,sizes[i],[x,y]);
    try{
      stack(g,x,y,w,h,d,c,p[i],NAMES[i],ROLES[i],
        i<2?cost*(1-sine(between(advance,0,.25))):0,labels*(1-advance),labels,i===0);
    }finally{restore();}
  }
}
export function mem_budget(g,one,four,p,cost,a=1,zoom=0,sizes=UNIT_SIZES,split=0){
  if(!one||!a)return;
  // Compute one stack and two possible banks from the same slices.
  const x=mix(660,1196,zoom),w=mix(262,148,zoom),y=250,bottom=y+419;
  const pre=146*(1-four),limit=bottom-272;
  g.line(x-25,bottom,x+w+25+54*split,bottom,AXIS,1.5,one*a);
  g.arrow(x-13,bottom,x-13,y,AXIS,1.5,one*a,8);
  label(g,"显存",x+w/2,y-32,28,WHITE,one*a*(1-sine(between(split,.08,.30))));
  label(g,"GPU 0",x+35,y-30,24,WHITE,sine(between(split,.63,.93))*a,undefined,"math");
  label(g,"GPU 1",x+151,y-30,24,WHITE,sine(between(split,.63,.93))*a,undefined,"math");
  let top=bottom-pre;
  const tanks=[bottom,bottom];
  if(pre>0)solidBlock(g,x,bottom-pre,w,pre,BLUE,one*a);
  function block(i,h,c){
    if(h<=0)return;
    const col=i%2;
    solidBlock(g,mix(x,x-13+116*col,split),
      mix(top-h,tanks[col]-h,split),mix(w,102,split),h,c,a);
    top-=h;tanks[col]-=h;
  }
  for(const [i,c] of MODEL_C.entries()){
    block(i,62*p[i]*four*sizes[i],c);
    if(i<2){
      block(i,34*cost*p[i]*sizes[i],i?PURPLE:TEAL);
      block(i,28*cost*p[i]*sizes[i],GOLD);
    }
  }
  g.line(x-31,limit,x+w+33+20*split,limit,RED,2.3,one*a,[7,6]);
  label(g,"上限",x+w+53,limit-23,24,RED,one*a,"left");
}
export function memory(g,b){
  const one=b.fade("one",.79),four=b.fade("four",.60),cost=b.fade("cost",.94);
  const p=["actor","critic","ref","rm"].map(key=>b.fade(key,.69));
  const slide=sine(between(b.t,b.at("one")-.24,b.at("one")+.65));
  const sizes=SIZE_PROFILE.map(s=>mix(1,s,b.fade("sizes",.85)));
  const split=b.fade("deploy",.85)*(1-b.fade("weights",.75));
  const lens=.117*sine(between(b.t,.23,b.at("memory")+.3))*(1-slide);
  const restore=layer(g,b.gone(),0,0,1+lens,[790,466]);
  try{
    // Keep the original checkpoint on its mark until Actor begins
    // entering. Its label is gone before the replacement appears.
    const original=one*(1-b.ent(.30,b.at("actor")-.39));
    if(slide>.15)model_rig(g,p,original,cost,0,sizes);
    mem_budget(g,1,b.fade("actor",.60),p,cost,1,slide,sizes,split);
  }finally{restore();}
}
export const TOKENS = [["先", "把", "水", "烧", "开"], ["取", "出", "冰", "水", "碗"], ["六", "分", "钟", "停", "火"]];
export function rollout_lanes(g, t, start, batch, batch_start, overlap, a=1) {
  let dx, end, event, i, j, p, q, s, x, y, ys;
  x = 468;
  dx = 149;
  ys = [302, 427, 552];
  for (const item of enumerate(ys)) {
    [i, y] = item;
    q = (a * ((i === 0) ? 1 : batch));
    if ((q <= 0)) {
      continue;
    }
    g.line(231,y,1351,y,RULE,1.5,q);
    chip(g, `回答 ${(i + 1)}`, 248, y, BLUE, 170, 73, q);
    g.arrow(346, y, 404, y, MUTED, 2.0, q);
    event = ((i === 0) ? start : batch_start);
    for (const item of enumerate(at(TOKENS, i))) {
      [j, s] = item;
      p = ease(((((t - event) - (j * 0.62)) - ((i - 1) * 0.17)) / 0.46));
      g.rect(((x + (j * dx)) - 53), (y - 42), 106, 84, undefined, RULE, 1.3, undefined, q);
      chip(g, s, (x + (j * dx)), y, TEAL, 106, 84, (q * p), (j === 4));
    }
    end = ease(((((t - event) - 3.0) - ((i - 1) * 0.14)) / 0.5));
    g.arrow(1126, y, 1212, y, DIM, 2, q);
    chip(g, "终局奖励", 1329, y, GOLD, 173, 73, (q * end), true);
    label(g,"…",1329,y,37,WHITE,q*(1-end),undefined,"math");
  }
}
export function rollout(g, b) {
  let aux, bat, k, lane_in, open_arc, over, p, phase, prev, start, token, waited, x, y;
  token = b.fade("token", 0.6);
  bat = b.fade("batch", 0.6);
  waited = b.fade("wait", 0.65);
  over = b.fade("overlap", 0.68);
  phase = b.at("overlap");
  aux=b.ent(.52,phase-.065);
  prev=1-b.ent(.27,phase-.34);
  open_arc=sine(between(b.t,.45,2.23));
  lane_in=b.ent(.22,b.at("token")-.32);
  const laneShape=b.ent(.38,b.at("token")-.095);
  if ((lane_in < 1)) {
    { const restore = layer(g, (1 - lane_in));
      try {
        // Remove the memory gauge and interior labels before the
        // checkpoints physically take their new places on the wires.
        const labels=max(1-sine(between(b.t,.18,.43)),sine(between(b.t,2.14,2.48)));
        const budget=1-sine(between(b.t,.04,.41));
        mem_budget(g,1,1,[1,1,1,1],1,budget,1,SIZE_PROFILE);
        model_rig(g,undefined,undefined,undefined,open_arc,SIZE_PROFILE,labels);
        const wire=sine(between(b.t,1.93,2.48));
        if(wire){
          x = 1012;
          y = 353;
          g.line(x,279,x,552,DIM,1.75,wire);
          for (const item of [279, 414, 552]) {
            k = item;
            g.arrow(x,k,1141,k,MUTED,1.65,wire);
          }
          g.arrow(446,y,x,y,MUTED,2.15,wire);
          p = b.fade("prompt", 0.6);
          if (p) {
            chip(g, "提示词", 680, 303, BLUE, 165, 59, p);
            g.arrow(591, 303, 452, 303, BLUE, 2.2, p);
          }
        }
      } finally { restore(); }
    }
  }
  { const restore = layer(g, (prev * b.gone()));
    try {
      label(g, "Actor", 690, 201, 37, TEAL, token);
      label(g, "Reward", 1328, 201, 37, GOLD, token);
      g.line(1120,222,1120,246,RULE,2,waited);
      start = b.at("token");
      rollout_lanes(g, b.t, start, bat, (b.at("batch") + 0.25), over, Math.max(token,laneShape));
      if ((!over)) {
        label(g, "Rollout", 299, 655, 29, TEAL, b.fade("rollout", 0.65), undefined, "math");
      }
    } finally { restore(); }
  }
  if (aux) {
    pipeline(g, (b.t - phase), (aux * b.gone()));
  }
}
export function pipeline(g, t, a) {
  let cursor, i, later, p, q, r, x, y, yy;
  p = between(t, 0, 2.75);
  { const restore = layer(g, a);
    try {
      x = 425;
      y = 377;
      for (const item of range(2)) {
        i = item;
        yy = (y + (154 * i));
        label(g, `批次 ${(i + 1)}`, 249, yy, 33, WHITE);
        q = ease(((p - (i * 0.24)) / 0.45));
        solidBlock(g,x+i*195,yy-32,510*q,64,TEAL);
        if ((q > 0.68)) {
          label(g,"生成",x+i*195+241*q,yy-57,31,SKY);
        }
        r = ease((((p - 0.37) - (i * 0.22)) / 0.27));
        if (r) {
          solidBlock(g,x+i*195+510,yy-32,184*r,64,GOLD);
          if ((r > 0.7)) {
            label(g,"评估",x+i*195+601,yy-57,30,GOLD);
          }
        }
      }
      g.arrow(425, 672, 1395, 672, MUTED, 1.8);
      note(g, "时间", 1396, 709, undefined, undefined, "right");
      later = ease(((t - 1.95) / 0.66));
      if (later) {
        cursor = (935 + (103 * sine(between(t, 1.95, 3.0))));
        g.line(cursor, 333, cursor, 603, GOLD, 1.8, later, [7, 7]);
        for (const item of [377, 531]) {
          yy = item;
          g.circle(cursor, yy, 6, YELLOW, undefined, undefined, later);
        }
      }
    } finally { restore(); }
  }
}
export const CRITIC_BRANCHES = [["放鸡蛋", 0.6, 4, TEAL], ["关火", 0.3, 2, GOLD], ["倒掉水", 0.1, 0, RED]];
export const PREFIX = "水开之后，先…";
export function critic_geometry(turn) {
  let leaves, level, rise, rx, ry, spread;
  rise = sine(between(turn, 0, 0.36));
  spread = sine(between(turn, 0.19, 0.87));
  level = sine(between(turn, 0.39, 1));
  rx = mix(371, 800, sine(between(turn, 0.32, 1)));
  ry = ((315 - (96 * rise)) + (14 * level));
  leaves = (()=>{const __list21=[];for(const j of range(3)){__list21.push([mix(1059, (431 + (369 * j)), spread), mix(((247 + (111 * j)) + (55 * rise)), 378, level)]);}return __list21;})();
  return [[rx, ry], leaves];
}
export function critic_tree(g, b, turn, noise) {
  let _, angle, bend_x, bend_y, color, cs, ex, ey, j, leaves, lh, lw, name, opacity, p, rh, root, rw, rx, ry, sn, spread, sx, sy, x, y;
  root=b.ent(.55,.67);
  spread=Math.max(.49*b.ent(.60,1.26),b.fade("paths",1.68));
  [[rx,ry],leaves]=critic_geometry(turn);
  const lens=(1-turn)*(1-sine(between(b.t,2.05,b.at("critic")-.41)));
  rx+=107*lens;
  ry+=39*lens;
  leaves=leaves.map(([x,y],i)=>[x+89*lens,y+(i-1)*49*lens]);
  angle = ((0.5 * Math.PI) * sine(between(turn, 0.09, 0.49)));
  [cs, sn] = [Math.cos(angle), Math.sin(angle)];
  [rw, rh] = [mix(348,344,turn)+144*lens,mix(84,74,turn)+24*lens];
  [lw, lh] = [mix(230,207,turn), mix(77,70,turn)];
  [sx, sy] = [(rx + (((rw / 2) + 14) * cs)), (ry + (((rh / 2) + 6) * sn))];
  for (const item of enumerate(zip(CRITIC_BRANCHES, leaves))) {
    [j, [[name, _, _, color], [x, y]]] = item;
    p = ease(((spread * 1.54) - (j * 0.15)));
    opacity = (p * (1 - ((0.58 * noise) * (1 - turn))));
    [ex, ey] = [(x - (((lw / 2) + 12) * cs)), (y - (((lh / 2) + 17) * sn))];
    bend_x = min(162, max(26, (Math.abs((ex - sx)) * 0.34)));
    bend_y = min(24, max(2, ((ey - sy) * 0.38)));
    arc_arrow(g, [sx, sy], [(sx + (bend_x * cs)), (sy + (bend_y * sn))], [(ex - (bend_x * cs)), (ey - (bend_y * sn))], [ex, ey], color, p, opacity, 2.4, 10);
  }
  for (const item of enumerate(zip(CRITIC_BRANCHES, leaves))) {
    [j, [[name, _, _, color], [x, y]]] = item;
    p = ease(((spread * 1.54) - (j * 0.15)));
    opacity = (p * (1 - ((0.58 * noise) * (1 - turn))));
    if ((turn && p)) {
      g.rect((x - (lw / 2)), (y - (lh / 2)), lw, lh, BLACK);
    }
    chip(g, name, x, y, color, lw, lh, opacity);
  }
  chip(g, PREFIX, rx, ry, blend(TEAL, BLUE, turn), rw, rh, root);
}
export function critic(g, b) {
  let _, adv, c, calc, carry, clear, close, collapse, color, fin, finish, first, i, initial, j, k, noise, p, pieces, prob, pts, q, r, ret, revealed, s, toy, toy_end, turn, v, value, w, worked, ws, x, y, yy;
  c = b.fade("critic", 0.6);
  value = b.fade("value", 0.66);
  adv = b.fade("adv", 0.65);
  noise = b.fade("noise", 1.12);
  const glitch=b.at("glitch");
  collapse=b.ent(.25,glitch+.38);
  const preceding=1-sine(between(b.t,glitch,glitch+.30));
  toy = b.ent(0.58, (b.at("adv") + 1.25));
  toy_end=b.ent(.30,glitch);
  calc = b.at("calc");
  close = b.at("partial");
  clear = (1 - sine(between(b.t, (calc - 0.59), (calc - 0.13))));
  turn = sine(between(b.t,calc,calc+1.20));
  worked = b.ent(0.62, (calc + 0.47));
  carry = (1 - b.ent(0.28, 0.4));
  revealed=ease(between(b.t,glitch+.64,glitch+1.30));
  if (carry) {
    pipeline(g, 3.0, carry);
  }
  { const restore = layer(g, b.gone());
    try {
      if(preceding){
        const before=layer(g,preceding);
        try{critic_tree(g,b,0,noise);}finally{before();}
      }
      if (clear && preceding) {
        { const restore = layer(g, clear*preceding);
          try {
            initial = (1 - sine(between(b.t, (close - 0.38), (close + 0.01))));

            if (initial) {
              { const restore = layer(g, initial);
                try {
                  first = b.fade("paths", 1.7);
                  finish = b.fade("reward_end", 0.6);
                  label(g, "Critic", 371, 452, 44, PURPLE, c, undefined, "math");
                  g.arrow(371, 359, 371, 411, PURPLE, 1.65, c, 9);
                  for (const item of enumerate(CRITIC_BRANCHES)) {
                    [j, [_, _, _, color]] = item;
                    yy = (247 + (111 * j));
                    for (const item of [0, 1]) {
                      i = item;
                      q = ease(((((first * 1.75) - (0.19 * j)) - (0.36 * i)) - 0.36));
                      y = (yy + ((i === 0) ? (-23) : 24));
                      g.poly([[1178, yy], [1192, y], [1244, y]], color, 1.55, (q * 0.77));
                      g.circle(1244, y, 4.5, color, undefined, undefined, q);
                    }
                    if (finish) {
                      q = ease(((finish * 1.52) - (0.17 * j)));
                      g.arrow(1251, yy, 1291, yy, MUTED, 1.65, q, 9);
                      chip(g,at(["4","2","0"],j),1374,yy,GOLD,95,49,q,true);
                    }
                  }
                  label(g, "奖励模型", 1374, 191, 28, GOLD, finish);
                } finally { restore(); }
              }
            }
            if (value) {
              for (const item of enumerate([0.86, 0.41, 0.12])) {
                [j, k] = item;
                color = at(at(CRITIC_BRANCHES, j), 3);
                y = (247 + (111 * j));
                solidBlock(g,1214,y-12,191*k,24,color,value*(1-.81*noise));
              }
              note(g, "终局分数", 1310, 192, value);
              mathform(g, "value", 504, 452, 59, 650, PURPLE, value);

            }
            if ((adv && (!toy))) {
              bracket(g, 245, 781, 506, PURPLE, adv, (-1));
            }
            if ((toy && (toy_end < 1))) {
              { const restore = layer(g, (toy * (1 - toy_end)));
                try {
                  rule(g, 237, 540, 1384, RULE);
                  label(g,"Gₜ",431,577,34,WHITE,1,undefined,"math");
                  label(g,"V(sₜ)",772,577,34,WHITE,1,undefined,"math");
                  label(g,"Aₜ",1112,577,34,WHITE,1,undefined,"math");
                  label(g, "4", 431, 639, 52, GOLD, undefined, undefined, "math");
                  label(g, "−", 594, 639, 39, MUTED, undefined, undefined, "math");
                  label(g, "=", 942, 639, 35, MUTED, undefined, undefined, "math");
                  v = (3 + (2 * noise));
                  label(g, `${fmt(v, `.1f`)}`, 772, 639, 49, PURPLE, undefined, undefined, "math");
                  label(g, `${fmt((4 - v), `+.1f`)}`, 1112, 639, 53, ((v <= 4) ? TEAL : RED), undefined, undefined, "math");
                  label(g, "优势", 1120, 698, 28, ((v <= 4) ? TEAL : RED));
                } finally { restore(); }
              }
            }
          } finally { restore(); }
        }
      }
      const consoleAlpha=collapse*(1-sine(between(b.t,calc-.35,calc-.06)));
      if(consoleAlpha){
        const terminal=layer(g,consoleAlpha);
        try{
          g.line(236,196,236,672,RED,4.3);
          label(g,"Mode Collapse",295,235,57,RED,1,"left","math");
          const rows=[
            "非常感谢您的提问！  非常感谢您的提问！",
            "非常感谢您的提问！  非常感谢您的提问！",
            "非常感谢您的提问！  非常感谢……",
          ];
          for(const [i,line] of rows.entries()){
            const show=clamp((b.t-glitch-.49-i*.22)/.47);
            sample(g,line.slice(0,Math.ceil(show*line.length)),295,348+i*112,49,WHITE,show,"left");
          }
        }finally{terminal();}
      }
      if(b.t>=calc){
        const fresh=layer(g,b.ent(.43,calc));
        try{critic_tree(g,b,turn,0);}finally{fresh();}
      }
      if (worked) {
        for (const item of enumerate(CRITIC_BRANCHES)) {
          [j, [_, prob, r, color]] = item;
          x = (431 + (369 * j));
          p = b.fade(`p${j}`, 0.49);
          ret=b.fade(`ret${j}`,.28);
          label(g, `${fmt(prob, `.2f`)}`, x, 462, 62, color, p, undefined, "math");
          label(g,`r = ${r}`,x,548,39,WHITE,ret,undefined,"math");
        }
        fin = b.fade("mean", 0.51);
        rule(g, 333, 606, 1267, RULE, fin);
        pieces=CRITIC_BRANCHES.flatMap(([,prob,reward,c],i)=>
          [...(i?[["+",WHITE]]:[]),[fmt(prob,".2f"),c],[`× ${reward}`,WHITE]]);
        const score=expected_score(CRITIC_BRANCHES.map(b=>b[1]),CRITIC_BRANCHES.map(b=>b[2]));
        pieces.push(["=",WHITE],[String(score),GOLD]);
        ws = (()=>{const __list23=[];for(const [s, _] of pieces){__list23.push(g.measure(s, 47, "math"));}return __list23;})();
        x = (800 - ((sum(ws) + (18 * (len(ws) - 1))) / 2));
        for (const item of zip(pieces, ws)) {
          [[s, color], w] = item;
          label(g, s, x, 658, 47, color, fin, "left", "math");
          x += (w + 18);
        }
      }
    } finally { restore(); }
  }
}
export function goal_parts(g, a=1, scale=1, dy=0, pull=0) {
  let b, cy, height, i, l, p, points, q, r, s, t, width, x, y;
  { const restore = layer(g, a, undefined, dy, scale, [800, 414]);
    try {
      y = 411;
      if ((pull <= 0)) {
        mathform(g, "fixed-rl", 800, y, 81, 1375);
      } else {
        mathform(g, "goal-rest", 800, y, 81, 1375);
        mathform(g, "goal-highlight", 800, (y - (120 * pull)), 81, 1375, blend(WHITE, GOLD, min(1, (pull * 3.8))), (1 - pull));
        [x, cy, s] = form_segment("fixed-rl", "goal", 800, y, 81, 1375);
        [l, t, r, b] = at(FORM_ANCHORS, "goal");
        width = ((r - l) * s);
        height = ((b - t) * s);
        points = [[((x - (width / 2)) - 6), ((cy - (height / 2)) - 7)], [((x + (width / 2)) + 6), ((cy - (height / 2)) - 7)], [((x + (width / 2)) + 6), ((cy + (height / 2)) + 7)], [((x - (width / 2)) - 6), ((cy + (height / 2)) + 7)]];
        for (const item of range(4)) {
          i = item;
          [p, q] = [at(points, (i - 1)), at(points, i)];
          g.line(...p,...q,GOLD,2.3,pull,[7,6]);
        }
        note(g, "奖励", x, (y + 63), pull, GOLD);
      }
    } finally { restore(); }
  }
}
export function goal(g,b){
  // Reuse the actual terms, not recap cards, then let the expression sit.
  const eq=b.fade("goal",.6);
  const entry=1-sine(between(b.t,b.at("goal")-.29,b.at("goal")+.02));
  if(entry){
    const g0=b.fade("recap",.61),g1=b.fade("judge",.62),g2=b.fade("four",.58);
    // Start with one readable equation on the first voice beat, then
    // move it to its place as the judge and PPO objective come in.
    const split=sine(between(b.t,b.at("recap")-.46,b.at("recap")+.49));
    mathform(g,"sft",mix(800,430,split),mix(371,304,split),
      mix(158,94,split),mix(1065,680,split),blend(WHITE,SKY,split),mix(.84,1,g0)*entry);
    mathform(g,"rm",1141,304,83,666,blend(WHITE,GOLD,.70),g1*entry);
    mathform(g,"full-rl",800,529,68,1350,WHITE,g2*entry);
  }
  if(eq)goal_parts(g,eq);
  countdown(g,b,665);
}
export function hook(g, b) {
  let dpo, left, lift, nx, old, right;
  lift = b.fade("remove", 0.6);
  dpo = b.fade("dpo", 0.64);
  nx = b.fade("next", 0.63);
  { const restore = layer(g,b.gone(OST.coda.fadeToBlackSeconds));
    try {
      goal_parts(g, (1 - (dpo * 0.18)), (1 - (nx * 0.1)), ((-nx) * 44), lift);
      if ((!lift)) {
        old = (1 - ease(between(b.t, (b.at("remove") - 0.47), (b.at("remove") + 0.02))));
        left = (b.fade("reward_leak", 0.53) * old);
        right = (b.fade("sampling", 0.53) * old);
        label(g, "裁判的漏洞", 547, 606, 33, RED, left);
        label(g, "在线采样的账单", 1055, 606, 33, GOLD, right);
      }
      label(g, "DPO", 800, 226, 80, WHITE, dpo, undefined, "math");
      if (nx) {
        label(g, "下集 · 从偏好直接学策略", 800, 607, 51, WHITE, nx);
        note(g, "直接偏好优化：推导与梯度", 800, 684, nx);
      }
    } finally { restore(); }
  }
}
