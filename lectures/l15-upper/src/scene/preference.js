// Frame-driven artwork, drawn by the Remotion Canvas composition.
import {min,max,sum,len,range,zip,enumerate,round,getattr,any,all,at,slice,repeat,contains,fmt,printf,isclose,bisect_left,bisect_right} from '../values';
import {BLACK, WHITE, MUTED, DIM, RULE, INK, BLUE, GOLD, TEAL, GREEN, RED, PURPLE, YELLOW, PAPER, AXIS, CYAN, SKY, ORANGE, MAGENTA, PINK, ease, sine, between, pulse, solidBlock, sample, label, term, note, sampleLines, rule, bracket, slash, arc_arrow, highlight, chip, axis, question, ink_label, paperCutout, pieDial, countdown, layeredBlock, lock, layer, aperture, phase_card, picture, mathform, form_segment, move_segment, blend, mix, clamp} from '../stage';
import OVEROPT from '../data/stiennon-fig5.json';
export {OVEROPT};
export const HUMAN_PEAK = OVEROPT.reduce((a,b)=>a[2]<b[2]?b:a);
import {bt, expected_score} from './examples';

// From fitting a distribution to fitting a judge: probabilities and examples stay tangible.
export const HYP = ["样板", "漏条件", "新答法"];
export const BASE = [0.28, 0.37, 0.35];
export const TARGET = [0.67, 0.32, 0.01];
export const P_COL = [BLUE, GOLD, TEAL];
function distribution(g,x,y,values,c,tag,a=1,ghost=null,focus=0){
  rule(g,x,y,x+510,AXIS,a);
  for(const [i,v] of values.entries()){
    const xx=x+105+148*i,h=303*v,on=a*(i===2?1:mix(1,.19,focus)),hue=i===2?TEAL:c;
    if(ghost)g.rect(xx-55,y-303*ghost[i],110,303*ghost[i],null,WHITE,1.15,0,on*.19);
    solidBlock(g,xx-50,y-h,100,h,hue,on);
    label(g,fmt(v,".2f"),xx,y-h-26,mix(23,32,i===2?focus:0),hue,on,undefined,"math");
    label(g,HYP[i],xx,y+30,26,WHITE,on);
  }
  label(g,tag,x+255,y-258,33,c,a);
}
function imitation_state(g,target,fit,miss,novel,lim,a=1){
  const restore=layer(g,a);
  try{
    distribution(g,180,525,TARGET,BLUE,"示范",target,null,novel);
    distribution(g,908,525,BASE.map((v,i)=>mix(v,TARGET[i],fit)),GOLD,"模型",max(.58,target),TARGET,novel);
    g.arrow(702,472,886,472,GOLD,2.5,fit*(1-.81*novel),12);
    if(miss){
      bracket(g,353,490,586,RED,miss*(1-.81*novel),-1);
      bracket(g,1080,1218,586,RED,miss*(1-.81*novel),-1);
    }
    mathform(g,"fit",800,689,63,750,WHITE,fit);
    if(novel)rule(g,1259,573,1259+97*novel,TEAL,novel,2.2);
    if(lim){
      g.line(1309,382,1309,463,AXIS,1.45,lim,[4,5]);
      label(g,"?",1309,354,69,GOLD,lim,undefined,"math");
    }
  }finally{restore();}
}
export function mimic(g,b){
  imitation_state(g,b.fade("target",.75),b.fade("fit",1.65),b.fade("miss",.64),
    b.fade("gen",.83),b.fade("limit",.59),b.gone());
}
export const MPATH = [[200, 575], [286, 547], [431, 572], [552, 526], [629, 511], [715, 379], [799, 347], [879, 303], [974, 461], [1062, 402], [1160, 277], [1305, 220], [1410, 361]];
export const ALTS = [[510, 533], [687, 421], [868, 309], [1025, 426], [1279, 233]];
export function weighted_reward(g,b,alpha) {
  // Width is sampling mass, height is the existing reward. Their areas
  // sum to expected reward; only the common boundary ever moves.
  const restore=layer(g,alpha);
  try {
    const on=b.fade("calc",.53);
    const moved=sine(between(b.t,b.at("again"),b.at("again")+1.57));
    const p=mix(.80,.25,moved), w=1176, left=212, base=538, unit=41;
    const score=[2,8],masses=[p,1-p];
    const border=left+w*p;
    for(const [i,c] of [BLUE,GOLD].entries()){
      const x=i?border:left, width=w*masses[i],h=score[i]*unit;
      const enter=b.fade("calc",.66,.13*i),axisX=x+width/2;
      g.poly([[x,base],[x,base-h*enter],[x+width,base-h*enter],[x+width,base]],WHITE,1.15,enter,true,c,.88);
      label(g,`${i?"B":"A"} · r = ${score[i]}`,axisX,base-h-31,37,c,enter,undefined,"math");
      solidBlock(g,x,base,width,62,c,on);
      label(g,fmt(masses[i],".2f"),axisX,base+30,38,i?BLACK:WHITE,on,undefined,"math");
    }
    g.line(border,base+8,border,base+89,WHITE,1.65,on);
    g.line(left-13,base,left-13,base-334,AXIS,1.35,on);
    for(const n of [2,4,6,8]){
      const y=base-unit*n;
      g.line(left-21,y,left-13,y,AXIS,1.3,on);
      label(g,String(n),left-37,y,24,WHITE,on,"right","math");
    }
    const math=[
      [`${fmt(p,".2f")} × 2`,BLUE],["+",WHITE],
      [`${fmt(1-p,".2f")} × 8`,GOLD],["=",WHITE],
      [fmt(expected_score(masses,score),".1f"),TEAL],
    ];
    for(const [i,[t,c]] of math.entries())label(g,t,[438,633,800,968,1140][i],682,54,c,on,undefined,"math");
    const landed=b.fade("six_point_five",.33);
    rule(g,1082,723,1082+116*landed,TEAL,landed,2.4);
  } finally {restore();}
}
export function landscape(g, b) {
  let carry, i, k, out, p, samp, start, then, toy, up, x, xx, y, yy;
  start = b.fade("agent", 0.58);
  samp = b.fade("sample", 2.8);
  up = b.fade("up", 1.75);
  then = b.at("calc");
  out=1-b.ent(.28,then-.68);
  toy = b.ent(0.51, then);
  carry = (1 - b.ent(0.26, (b.at("agent") - 0.42)));
  if(carry)imitation_state(g,1,1,1,1,1,carry);
  { const restore = layer(g, ((start * b.gone()) * out));
    try {
      axis(g, 167, 656, 1280, 485, "候选回答", "奖励", 1);
      g.poly([[200,656],...MPATH,[1410,656]],WHITE,1.15,1,true,TEAL,.88);
      [x, y] = at(ALTS, 0);
      for (const item of enumerate(ALTS)) {
        [i, [xx, yy]] = item;
        p = ease(((samp * 5.6) - i));
        g.line(xx, 652, xx, yy, ((i === 4) ? GOLD : MUTED), 1.5, p, [6, 8]);
        if (p) {
          g.circle(xx, yy, (6 + (p * 4)), ((i === 4) ? GOLD : TEAL), undefined, undefined, p);
        }
      }
      if (up) {
        k = min((len(ALTS) - 2), Math.trunc((up * (len(ALTS) - 1))));
        [x, y] = (()=>{const __list11=[];for(const v of [0, 1]){__list11.push(mix(at(at(ALTS, k), v), at(at(ALTS, (k + 1)), v), ((up * (len(ALTS) - 1)) - k)));}return __list11;})();
        g.circle(x, y, 15, WHITE, BLACK, 2.0, up);
      }
      mathform(g, "opt", 535, 280, 68, 720, WHITE, up);
    } finally { restore(); }
  }
  if (toy) {
    weighted_reward(g, b, ((toy * b.gone()) * (1 - (0.72 * b.fade("question", 0.43)))));
  }
}
export function gv_gap(g, b) {
  let a, body, build, check, comparing, end, hard, i, k, later, msg, name, p, px, x, y1, y2, yy;
  name = b.fade("term", 0.6);
  build = b.fade("build", 0.67);
  check = b.fade("verify", 0.65);
  hard = b.fade("hard", 0.5);
  end = b.fade("end", 0.5);
  { const restore = layer(g, b.gone());
    try {
      body = max((0.67 * b.ent(0.48)), name);
      label(g, "G–V Gap", 800, 722, 32, GOLD, name, undefined, "math");
      y1 = ((478 + (139 * build)) - (14 * check));
      y2 = ((478 - (139 * build)) + (14 * check));
      g.poly([[788,468],[724,698],[874,698]],WHITE,1.15,body,true,PURPLE,.83);
      g.line(270, y1, 1330, y2, WHITE, 4, body);
      g.circle(800, 478, 9, GOLD, undefined, undefined, body);
      function tray(cx, y) {
        g.line(cx, y, cx, (y + 56), DIM, 2, body);
        g.line((cx - 146), (y + 56), (cx + 146), (y + 56), WHITE, 2.1, body);
      }
      tray(388, (y1 - 30));
      tray(1212, (y2 + 29));
      label(g, "从头解", 388, 373, 32, PURPLE, (body * (1 - build)));
      label(g, "拿来查", 1212, 373, 32, GOLD, ((body * (1 - build)) * (1 - check)));
      if (build) {
        later = b.fade("concurrent", 0.64);
        for (const item of [[258, "数学证明", build], [390, "并发锁", later]]) {
          [px, msg, p] = item;
          yy = ((y1 - 32) - (27 * (1 - p)));
          layeredBlock(g, px, yy, 115, 67, 24, PURPLE, undefined, undefined, p);
          label(g,msg,px+58,yy+34,23,WHITE,p);
        }
      }
      comparing = b.fade("compare", 0.62);
      if(comparing){
        const send=sine(check),y=y2-42;
        chip(g,"候选 A",1106,y,GOLD,127,51,comparing);
        chip(g,"候选 B",1281+111*send,y-22*send,BLUE,127,51,
          comparing*(1-.81*send));
        if(check)g.check(1361+103*send,y-20*send,false,20,check*(1-.40*hard));
      }
      if (end) {
        g.circle(800, 478, 17, undefined, GOLD, 2.25, (end * 0.72));
      }
    } finally { restore(); }
  }
}
export function sigmoid(v) {
  return bt(v, 0);
}
export function pair_strip(g, y, win=1, a=1, scale=1) {
  { const restore = layer(g, a, undefined, undefined, scale, [800, y]);
    try {
      chip(g, "同一个问题 x", 487, y, BLUE, 252, 68);
      g.arrow(617, y, 677, y, MUTED, 2.1);
      chip(g, "y_w", 756, y, TEAL, 133, 68);
      label(g, "＞", 860, y, 36, GOLD, win);
      chip(g, "y_l", 962, y, RED, 133, 68);
      mathform(g, "tuple", 1231, y, 47, 255, WHITE, win);
    } finally { restore(); }
  }
}
export function pair_tutorial(g, b, appear, win, bt) {
  let alpha, asking, c, end, fade_old, gloss, i, j, k, many, number, phase, same, word, x, y;
  // Show the label you actually have before introducing the model score.
  phase = b.at("pair");
  fade_old = ease(between(b.t, (phase - 0.2), (phase + 0.18)));
  asking = b.fade("judge", 0.66);
  if ((fade_old < 1)) {
    { const restore = layer(g, (b.ent(0.55, 0.22) * (1 - fade_old)));
      try {
        sample(g, "立刻放进冰水。", 800, 294, 46, BLUE);
        g.line(490, 431, 1110, 431, MUTED, 2.1, asking);
        for (const item of range(11)) {
          j = item;
          x = (490 + (j * 62));
          g.line(x, 418, x, 444, DIM, 1.4, asking);
        }
        label(g, "0", 490, 482, 37, MUTED, asking, undefined, "math");
        label(g, "10", 1110, 482, 37, MUTED, asking, undefined, "math");
        g.circle(799, 430, 7, undefined, GOLD, 2.5, asking);
      } finally { restore(); }
    }
  }
  if (((!appear) || (bt >= 1))) {
    return;
  }
  same = b.fade("same", 0.56);
  many = b.fade("many", 0.59);
  const gathering=b.at("many");
  // Unrelated poses must not share the board. Leave the caption and voice
  // continuous while the two response texts clear the stage.
  const listed=1-sine(between(b.t,gathering-.64,gathering-.38));
  number = b.fade("estimated", 0.67);
  end = (1 - ease(between(b.t,b.at("bt")-.43,b.at("bt"))));
  { const restore = layer(g, (appear * end));
    try {
      if (listed) {
        { const restore = layer(g, listed);
          try {
            sample(g, "煮好以后，怎么让加热停下来？", 800, 232, 52, BLUE, same);
            for (const item of enumerate([["立刻放进冰水。", TEAL], ["关火，留在热水里。", RED]])) {
              [j, [word, c]] = item;
              x = (428 + (744 * j));
              y = 430;
              sample(g,word,x,y,48,WHITE,max(.46,same));
              label(g, ((j === 0) ? "选中" : "落选"), x, 526, 33, c, win);
            }
            gloss = (b.fade("rlhf", 0.65) * (1 - sine(between(b.t, (b.at("winner") - 0.52), (b.at("winner") - 0.04)))));
            label(g,"RLHF",800,616,54,SKY,gloss,undefined,"math");
            label(g,"人类反馈强化学习",800,679,31,WHITE,gloss);
            label(g, "＞", 800, 435, 41, GOLD, win, undefined, "math");
          } finally { restore(); }
        }
      }
      if (many) {
        { const restore = layer(g, many);
          try {
            for (const item of enumerate(["煮蛋", "去重", "再举个例子"])) {
              [i, k] = item;
              y = 281+i*187;
              alpha = ease(((many * 1.45) - (i * 0.18)));
              chip(g,k,330,y,BLUE,332,86,alpha);
              g.arrow(520,y,630,y,WHITE,1.8,alpha);
              chip(g,"胜",730,y,TEAL,158,86,alpha);
              label(g,"＞",940,y,42,GOLD,alpha);
              chip(g,"负",1152,y,RED,160,86,alpha);
              if (number) {
                g.arrow(1260,y,1301,y,WHITE,1.8,number*alpha);
                label(g,"Δr",1362,y,42,GOLD,number*alpha,undefined,"math");
              }
            }
          } finally { restore(); }
        }
      }
    } finally { restore(); }
  }
}
export function sig_graph(g, val, a=1, progress=1, numbers=1) {
  let X, Y, curve, h, pp, rounded, vv, w, x, xx, y, yy;
  [x, y, w, h] = [225, 675, 780, 319];
  axis(g, x, y, w, h, "", "胜率", a);
  label(g,"Δr",x+w,y-27,25,WHITE,a,"right","math");
  X = ((v)=>(x + (((v + 5) / 10) * (w - 25))));
  Y = ((p)=>(y - (p * (h - 29))));
  for (const item of [0, 0.5, 1]) {
    pp = item;
    yy = Y(pp);
    g.line((x - 9), yy, (x + 1), yy, MUTED, 1.6, a);
    label(g, String(pp), (x - 23), yy, 23, MUTED, a, "right", "math");
  }
  for (const item of [(-5), 0, 5]) {
    vv = item;
    xx = X(vv);
    g.line(xx, y, xx, (y + 7), MUTED, 1.6, a);
    label(g, (vv ? `${fmt(vv, `+d`)}` : "0"), xx, (y + 28), 24, MUTED, a, undefined, "math");
  }
  g.line(X(0), y, X(0), Y(1), DIM, 1.4, a, [5, 6]);
  g.line(x, Y(0.5), X(5), Y(0.5), DIM, 1.4, a, [5, 6]);
  curve = (()=>{const __list12=[];for(const v of (()=>{const __list13=[];for(const i of range(126)){__list13.push(((-5) + (0.08 * i)));}return __list13;})()){__list12.push([X(v), Y(sigmoid(v))]);}return __list12;})();
  g.poly(slice(curve, undefined, max(2, min(126, Math.trunc((progress * 126)))), undefined), TEAL, 4.2, a);
  [xx, yy] = [X(val), Y(sigmoid(val))];
  g.line(xx, yy, xx, y, GOLD, 1.7, a, [4, 6]);
  g.circle(xx, yy, 8, WHITE, TEAL, 2, a);
  g.rect((xx - 12), (y - 8), 24, 15, GOLD, undefined, undefined, undefined, a);
  rounded = ((Math.abs(val) >= 0.05) ? round(val, 1) : 0.0);
  label(g, `${fmt(rounded, `+.1f`)}`, 1259, 478, 53, GOLD, (a * numbers), undefined, "math");
  const probability=sigmoid(val);
  label(g,`${fmt(probability*100,".1f")}%`,1259,549,66,TEAL,a*numbers,undefined,"math");
  solidBlock(g,1128,622,188*probability,31,TEAL,a*numbers);
  solidBlock(g,1128+188*probability,622,188*(1-probability),31,RED,a*numbers);
  pieDial(g,1382,638,37,probability,TEAL,RED,a*numbers);
}
export function pair_key(g, a=1) {
  { const restore = layer(g, a);
    try {
      
      mathform(g,"tuple",232,139,42,253,WHITE,1,1,"left");
    } finally { restore(); }
  }
}
export function score_translation(g, a=1, shift=2, spoken0=1, gap=1) {
  let c, j, val, y;
  { const restore = layer(g, a);
    try {
      g.line(1040,411,1040,682,AXIS,1.25,spoken0);
      label(g,`+${fmt(shift,".1f")}`,1376,408,35,GOLD,shift>.001?1:0,undefined,"math");
      for (const item of enumerate([TEAL, RED])) {
        [j, c] = item;
        y = (469 + (52 * j));
        val = (at([1.1, 2.1], j) + shift);
        label(g, at(["r₁", "r₂"], j), 1144, y, 25, c, spoken0);
        label(g, `${fmt(val, `.1f`)}`, 1311, y, 39, c, spoken0, undefined, "math");
      }
      rule(g,1122,557,1391,RULE,Math.max(spoken0,gap));
      label(g,"Δr = −1",1259,596,37,GOLD,gap,undefined,"math");
      label(g, `${fmt((100 * sigmoid((-1))), `.1f`)}%`, 1259, 658, 35, TEAL, gap, undefined, "math");
    } finally { restore(); }
  }
}
export function compare_pair(g, b) {
  let appear, bt, calc, delta, lo, panel_on, previous, shift, sig, value, win, zero;
  appear = b.fade("pair", 0.6);
  win = b.fade("winner", 0.55);
  bt = b.fade("bt", 0.6);
  sig = b.fade("sig", 0.68);
  lo = b.at("right");
  zero = b.at("zero");
  calc = b.at("calc");
  const rising=3.5*sine(between(b.t,lo,lo+max(.35,min(1.3,(zero-lo)*.59))));
  const equalize=sine(between(b.t,zero-.07,zero+.13));
  const negative=sine(between(b.t,calc,calc+.55));
  value=rising*(1-equalize)*(1-negative)-negative;
  { const restore = layer(g, b.gone());
    try {
      pair_tutorial(g, b, appear, win, bt);
      if (bt) {
        pair_key(g, bt);
      }
      mathform(g, "bt", 800, 241, 66, 1230, WHITE, bt, min(1, (bt * 1.55)));
      if ((bt && (sig < 1))) {
        note(g, "Bradley–Terry", 231, 185, (bt * (1 - sig)), MUTED, "left");
      }
      if (sig) {
        panel_on = b.fade("calc", 0.51);
        previous = (1 - b.ent(0.26, (calc - 0.43)));
        sig_graph(g, value, sig, sig, previous);
        mathform(g, "sigm", 1259, 386, 58, 356, WHITE, (sig * previous));
        if (panel_on) {
          shift = (2 * sine(between(b.t, b.at("pair1"), (b.at("pair1") + .13))));
          score_translation(g, panel_on, shift, b.fade("pair0", 0.37), b.fade("samegap", 0.5));
        }
      } else {
        if ((win && bt)) {
          delta = b.fade("delta", 0.57);
          if (delta) {
            mathform(g, "pair-odds", 800, 512, 112, 735, TEAL, delta);
          }
        }
      }
    } finally { restore(); }
  }
}
export function rm_loss(g, b) {
  let begin, c, calc, clear, dest, diff, drop, extra, i, lab, move, old, p, pre, rest, score, source, t, turn, write, x;
  begin = b.at("loss");
  // Start unbolting the graph during “尽量赢”; complete the log and averaging
  // terms when the narration actually reaches them.
  clear = sine(between(b.t, begin-2.16,begin-1.60));
  drop = sine(between(b.t, begin-1.56,begin-1.13));
  turn = sine(between(b.t, begin-1.46,begin+.04));
  write = sine(between(b.t, begin+.04,begin+.38));
  calc = b.at("calc");
  extra = b.fade("calc", 0.52);
  pre = (1 - b.ent(0.27, (calc - 0.43)));
  score = b.fade("score", 0.65);
  diff = b.fade("differentiable", 0.52);
  { const restore = layer(g, b.gone());
    try {
      if (pre) {
        { const restore = layer(g, pre);
          try {
            if ((clear < 1)) {
              { const restore = layer(g, (1 - clear));
                try {
                  pair_key(g);
                  old = (1 - b.ent(0.27, 0.43));
                  rest = 0;
                  sig_graph(g, (-1), 1, 1, rest);
                  if (old) {
                    score_translation(g, old);
                  }
                  mathform(g, "sigm", 1259, 386, 58, 356, WHITE, rest);
                } finally { restore(); }
              }
            }
            if ((write < 1)) {
              mathform(g, "bt-rest", 800, 241, 66, 1230, WHITE, (1 - drop));
              source = form_segment("bt", "bt", 800, 241, 66, 1230);
              dest = form_segment("rm", "rm", 800, 332, 70, 1335);
              move_segment(g, "bt", source, dest, turn, blend(WHITE, GOLD, Math.sin((Math.PI * turn))));
              mathform(g, "rm-rest", 800, 332, 70, 1335, WHITE, write);
            } else {
              mathform(g, "rm", 800, 332, 70, 1335);
            }
            lab = b.fade("average", 0.6);
            if (lab) {
              rule(g, 557, 381, 1037, GOLD, (lab * (1 - (score * 0.7))), 1.8);
            }
            if (score) {
              label(g, "奖励模型", 785, 556, 36, GOLD, score);
              for (const item of enumerate([["回答 α", TEAL], ["回答 β", BLUE], ["回答 γ", PURPLE]])) {
                [i, [t, c]] = item;
                p = ease(((score * 1.7) - (i * 0.2)));
                x = (349 + (i * 442));
                chip(g, t, x, 642, c, 195, 61, p);
                g.arrow((x + 108), 642, (x + 154), 642, DIM, 2.1, p);
                label(g, at(["+2.41", "+0.18", "−1.87"], i), (x + 222), 642, 32, c, p, undefined, "math");
              }
              if (diff) {
                rule(g, 507, 683, 1092, GOLD, ((diff * score) * 0.62), 1.7);
              }
            }
          } finally { restore(); }
        }
      }
      if (extra) {
        move = b.fade("change", 0.61);
        rm_case(g, extra, ((move > 0.5) ? 0.6 : 0.2), move, b.fade("p0", 0.48), b.fade("p1", 0.48), b.fade("mean", 0.52),b.fade("lower",.32));
      }
    } finally { restore(); }
  }
}
export function rm_case(g, a, q2, move, p0=1, p1=1, mean=1,landed=1) {
  let avg, c, i, p, probs, q, x;
  { const restore = layer(g, a);
    try {
      mathform(g, "rm", 800, 250, 61, 1110);
      probs = [0.9, q2];
      for (const item of enumerate(zip(probs, [p0, p1]))) {
        [i, [q, p]] = item;
        x = (470 + (660 * i));
        c = ((!i) ? TEAL : blend(RED, GOLD, move));
        label(g,at(["A","B"],i),x-192,398,28,WHITE,p,undefined,"math");
        solidBlock(g,x-144,383,288*q,23,c,p);
        label(g, `${fmt(q, `.0%`)}`, x, 432, 69, c, p, undefined, "math");
        label(g, `−ln(${fmt(q, `.2f`)}) = ${fmt((-Math.log(q)), `.3f`)}`, x, 533, 45, WHITE, p, undefined, "math");
      }
      rule(g, 259, 586, 1342, RULE);
      avg = (sum((()=>{const __list14=[];for(const p of probs){__list14.push((-Math.log(p)));}return __list14;})()) / 2);
      label(g,`ℒ = ${fmt(avg,".3f")}`,800,651,56,GOLD,mean,undefined,"math");
      rule(g,697,695,697+206*landed,GOLD,landed,1.75);
    } finally { restore(); }
  }
}
export const B_LINES = ["这是一个非常棒的编程问题！", "在 Python 里，有这几种思路：", "1. 使用集合 set()。", "    代码简洁，但不保证顺序。", "2. 使用循环与新列表。", "    逐个查找，时间可能到 O(n²)。", "3. 总结建议：", "    具体要看业务场景和数据规模。", "    先做个性能测试再决定。"];
export function answer_split(g,alpha=1,show_b=1,focus=0,shrink=0,dim_a=0,under=0,show_a=1){
  let a, c, i, k, length, p, t, w, x, yy;
  { const restore = layer(g, alpha, undefined, ((-shrink) * 67), (1 - (shrink * 0.1)), [800, 392]);
    try {
      sample(g, "怎么用 Python 快速给列表去重，并保持原顺序？", 800, 127, 43, WHITE);
      for (const item of enumerate([[BLUE, 103, "A"], [GOLD, 820, "B"]])) {
        [i, [c, x, t]] = item;
        a=i===0?show_a*mix(1,.20,dim_a):show_b;
        yy = 205;
        w = 677;
        if(!i)g.line(797,235,797,664,AXIS,1.25,max(show_a,show_b));
        label(g, t, (x + 44), (yy + 45), 44, c, a, undefined, "math");
        if ((!i)) {
          sample(g, "list(dict.fromkeys(seq))", (x + 31), (yy + 151), 33, WHITE, a, "left", "mono");
          sampleLines(g, ["Python 3.7+ 字典保序。", "可哈希元素，平均 O(n)。"], (x + 31), (yy + 232), 58, 33, WHITE, a);
          if (focus) {
            rule(g, (x + 31), (yy + 180), (x + 484), BLUE, (a * focus), 2.4);
          }
        } else {
          const size=31;
          const rowY=k=>yy+97+46.5*k+6*[2,4,6].filter(v=>v<=k).length;
          const rowX=k=>x+31+([3,5,7,8].includes(k)?28:0);
          for(const [k,text] of B_LINES.entries()){
            sample(g,text.trim(),rowX(k),rowY(k),size,WHITE,a,"left");
          }
          if (under) {
            for (const item of enumerate([0, 2, 6])) {
              [i, k] = item;
              p = ease(((under * 1.48) - (i * 0.22)));
              length = g.measure(at(B_LINES, k).trim(),31);
              rule(g,rowX(k),rowY(k)+18,rowX(k)+length*p,GOLD,a*p,1.8);
            }
          }
        }
      }
    } finally { restore(); }
  }
}
export function blind_test(g,b){
  const trial=b.at("trial"),arrive=b.ent(.42,trial),pair=b.fade("pairs",.46);
  const last=1-b.ent(.32,trial-.46);
  if(last)rm_case(g,last,.60,1);
  if(arrive){
    const rise=layer(g,1,0,14*(1-arrive));
    try{answer_split(g,arrive,pair,0,0,0,0,pair);}finally{rise();}
    countdown(g,b,698);
  }
}
export function judge(g, b) {
  let alpha, bias, bx, human, j, model, not_, old, s, t, walk;
  alpha = b.fade("a", 0.5);
  bx = b.fade("b", 0.55);
  not_ = b.fade("not", 0.48);
  human = b.fade("human", 0.7);
  model = b.fade("model", 0.7);
  bias = b.fade("bias", 0.63);
  t = b.at("model");
  walk = ease(between(b.t, b.at("human"), (b.at("human") + 1.7)));
  old = (1 - ease(between(b.t, (t - 0.4), (t - 0.08))));
  { const restore = layer(g, b.gone());
    try {
      answer_split(g, undefined, undefined, (alpha * (1 - (bx * 0.75))), max((alpha * 0.54), human), (human * 0.68), (walk * (1 - (bias * 0.18))));
      if (human) {
        s = (human * old);
        rule(g, 352, 631, 467, BLUE, s, 2.3);
        rule(g, 1136, 631, 1251, GOLD, s, 2.3);
        g.check(413, 663, true, 18, s);
        for (const item of range(3)) {
          j = item;
          rule(g, 1144, (654 + (12 * j)), (1205 - (13 * j)), GOLD, s, 2.25);
        }
      } else {
        if (not_) {
          bracket(g, 922, 1358, 661, GOLD, not_, (-1));
        }
      }
      if (model) {
        label(g, "模型裁判", 1178, 656, 30, GOLD, model);
        label(g, "Zheng et al. (2023) · MT-Bench / Chatbot Arena", 1178, 715, 22, MUTED, bias);
      }
    } finally { restore(); }
  }
}
export const OVEROPT_END = at(at(OVEROPT, (-1)), 0);
export const OVEROPT_TICKS = [0, 2, 5, 10, 25, 75, 250];
export function kl_position(kl) {
  return (Math.log1p(kl) / Math.log1p(OVEROPT_END));
}
export function goodhart_graph(g, p, a=1) {
  let H, W, X, Y, ap, aq, c, dash, k0, knots, m, ph, s, stuff, tick, u, v, x, xx, yy;
  [X, Y, W, H] = [236, 641, 1108, 408];
  axis(g,X,Y,W+41,H+9,"","",a);
  label(g,"胜率 (%)",X,Y-H-52,31,WHITE,a,"left");
  u = clamp(p);
  knots = Array.from((()=>{const __list15=[];for(const [x] of OVEROPT){__list15.push(kl_position(x));}return __list15;})());
  for (const item of [0, 0.25, 0.5, 0.75, 1]) {
    v = item;
    yy = (Y - (v * H));
    g.line((X - 8), yy, (X + 1), yy, MUTED, 1.25, a);
    label(g, `${fmt(v, `.0%`)}`, (X - 21), yy, 28, WHITE, a, "right", "math");
  }
  for (const item of OVEROPT_TICKS) {
    tick = item;
    xx = (X + (kl_position(tick) * W));
    g.line(xx, Y, xx, (Y + 7), MUTED, 1.25, a);
    label(g, `${fmt(tick, `g`)}`, xx, (Y + 33), 31, WHITE, a, undefined, "math");
  }
  m = min((len(knots) - 2), max(0, (sum((()=>{const __list16=[];for(const x of knots){__list16.push((x <= u));}return __list16;})()) - 1)));
  ph = between(u, at(knots, m), at(knots, (m + 1)));
  function draw_points(col) {
    let v;
    v = (()=>{const __list17=[];for(const [q, z] of zip(knots, OVEROPT)){__list17.push([(X + (q * W)), (Y - (at(z, col) * H))]);}return __list17;})();
    return [...v.slice(0,m+1),v[m].map((x,k)=>mix(x,v[m+1][k],ph))];
  }
  [ap, aq] = [draw_points(1), draw_points(2)];
  k0 = 3;
  if ((m >= k0)) {
    g.poly([...ap.slice(k0), ...aq.slice(k0).reverse()], RED, 0, a, true, RED, .32);
  }
  g.c.save();
  g.c.setLineDash([17, 8]);
  g.poly(ap, GOLD, 4.5, a);
  g.c.restore();
  g.poly(aq, TEAL, 4.1, a);
  for (const item of [[ap, GOLD], [aq, TEAL]]) {
    [stuff, c] = item;
    for (const item of slice(stuff, undefined, (-1), undefined)) {
      [xx, yy] = item;
      g.circle(xx, yy, 4.7, c, undefined, undefined, a);
    }
    g.circle(...stuff.at(-1),6.2,c,null,2,a);
  }
  for (const item of [[837, "奖励模型", GOLD], [1139, "人工偏好", TEAL]]) {
    [x, s, c] = item;
    dash = ((c === GOLD) ? [14, 7] : null);
    g.line(x, 186, (x + 54), 186, c, 4, a, dash);
    label(g, s, (x + 72), 186, 30, c, a, "left");
  }
  label(g,"KL vs SFT",1350,716,32,WHITE,a,"right","math");
}
export function goodhart(g, b) {
  let c, judgeVis, end, h, i, lab, law, leave, longer, outgoing, p, proxy, q, split, sweep, sx, t0, vis, wrong, x;
  law = b.fade("law", 0.55);
  proxy = b.fade("proxy", 0.64);
  longer = b.fade("long", 0.98);
  t0 = b.at("long");
  split = b.at("split");
  end = b.at("label");
  p = (((0.14 * sine(between(b.t, (b.at("proxy") + 0.32), (t0 - 0.25)))) + (0.33 * sine(between(b.t, t0, min(split, (t0 + 1.7)))))) + (0.53 * sine(between(b.t, split, min((end + 0.8), (split + 2.7))))));
  lab = b.fade("label", 0.55);
  { const restore = layer(g, b.gone());
    try {
      judgeVis = b.fade("card", 0.66);
      wrong = b.fade("wrong", 0.67);
      leave = b.at("proxy");
      outgoing = (1 - ease(between(b.t, (leave - 0.51), (leave - 0.13))));
      if (outgoing) {
        { const restore = layer(g, (outgoing * b.ent(0.62, b.open)), undefined, undefined, (1 + (0.048 * wrong)), [791, 411]);
          try {
            sx = [247, 911];
            sweep = sine(between(b.t, (b.at("law") - 0.12), (leave - 0.34)));
            for (const item of enumerate(zip(sx, [GOLD, TEAL], [max(0.58, judgeVis), wrong]))) {
              [i, [x, c, vis]] = item;
              axis(g,x,641,447,405,"","",vis);
              label(g,at(["奖励模型","读者"],i),x+16,199,37,c,vis,"left");
              h=!i?188+121*sweep:204-83*sweep;
              solidBlock(g,x+118,641-h,210,h,c,vis);
              g.circle(x+223,641-h,6,c,undefined,undefined,vis);
            }
            note(g, "古德哈特定律", 800, 705, law, GOLD);
          } finally { restore(); }
        }
      }
      if (proxy) {
        goodhart_graph(g, max(0.002, p), proxy);
      }
      if (lab) {
        goodhart_labels(g, lab, b.ent(0.55, (b.at("label") + 0.28)));
      }
    } finally { restore(); }
  }
}
export function goodhart_labels(g, lab=1, focus=1) {
  let x, y;
  label(g, "奖励黑客", 1114, 439, 38, RED, lab);
  label(g, "Stiennon et al., 2020", 800, 728, 21, MUTED, lab);
  if (focus) {
    x = (236 + (1108 * kl_position(at(HUMAN_PEAK, 0))));
    y = (641 - (at(HUMAN_PEAK, 2) * 408));
    g.circle(x, y, 13, undefined, TEAL, 2.3, focus);
    g.line(x, 641, x, y, TEAL, 1.6, focus, [5, 6]);
    label(g, "峰值", (x - 137), (y + 47), 26, TEAL, focus);
  }
}
export function question3(g, b) {
  let dim, q;
  q = b.fade("question", 0.55);
  dim = mix(1, 0.22, q);
  { const restore = layer(g, (dim * b.gone()), undefined, undefined, (1 + (0.028 * q)), [801, 458]);
    try {
      goodhart_graph(g, 1);
      goodhart_labels(g, (1 - q), (1 - q));
    } finally { restore(); }
  }
}
