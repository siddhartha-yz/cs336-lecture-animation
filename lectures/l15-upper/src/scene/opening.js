// Frame-driven artwork, drawn by the Remotion Canvas composition.
import {min,max,sum,len,range,zip,enumerate,round,getattr,any,all,at,slice,repeat,contains,fmt,printf,isclose,bisect_left,bisect_right} from '../values';
import {BLACK, WHITE, MUTED, DIM, RULE, INK, BLUE, GOLD, TEAL, GREEN, RED, PURPLE, YELLOW, PAPER, AXIS, CYAN, SKY, ORANGE, MAGENTA, PINK, ease, sine, between, pulse, solidBlock, sample, label, term, note, sampleLines, rule, bracket, slash, arc_arrow, highlight, chip, axis, question, ink_label, floatHan, glassBlock, paperCutout, countdown, layeredBlock, lock, layer, aperture, phase_card, picture, mathform, form_segment, move_segment, blend, mix, clamp} from '../stage';
import DATA from '../data/gekhman-fig3a.json';
import {SFT_TARGET_PROBS, sft_nll} from './examples';
import {OVEROPT,kl_position} from './preference';
import {GROUP} from './examples';

// Cold open and the first pass from example to mechanism.
export const EGG = "怎么煮一颗溏心蛋？";
export const FOUR = ["2.茶叶蛋怎么煮？", "3. 溏心和全熟有什么区别？", "4. 蛋白质变性是什么？", "5. 怎么剥一颗溏心蛋？"];
export const CANDIDATES = ["水…", "2.", "先…", "答：…", "溏…", "Q：", "如果…", "其他"];
export const CHOICE_LENGTHS = [0.68, 0.49, 0.3, 0.25, 0.2, 0.18, 0.15, 0.13];
export const CORPUS = ["蛋白质在热水里变性。", "煮好的蛋可以放进冰水。", "水被加热时，温度会上升。"];
export function intro(g, b) {
  let accent, active, again, ask, bar_x, caret, choose, clr, color, confidence, end_y, example, i, initial_x, intro, label_x, n, on, p, pick, pos, pre, prompt, retake, row_y, s, size, start, stride, take, undo, v, why, word, x, y, yy;
  intro = b.ent(0.58);
  why = b.at("fail");
  ask = b.at("question");
  choose = b.at("follow");
  again = b.at("repeat");
  prompt = b.ent(0.54, (ask - 0.44));
  example = (1 - sine(between(b.t, (why - 0.1), (ask - 0.53))));
  take = sine(between(b.t, (choose - 0.12), (choose + 0.42)));
  undo = sine(between(b.t, (again - 0.42), (again - 0.1)));
  retake = sine(between(b.t, again, (again + 0.55)));
  confidence = b.ent(0.5, (ask + 0.19));
  bar_x = 1085;
  label_x = 1050;
  row_y = 239;
  stride = 54;
  { const restore = layer(g, b.gone());
    try {
      label(g, "基座模型", 152, 156, 24, BLUE, (intro * 0.88), "left");
      sample(g, EGG, 152, 228, 53, BLUE, (intro * mix(0.84, 1, prompt)), "left");
      rule(g, 152, 294, 807, RULE, intro);
      for (const item of enumerate(CORPUS)) {
        [i, s] = item;
        p = (b.ent(0.45, (b.at("internet") + (0.32 * i))) * example);
        sample(g, s, 152, (358 + (58 * i)), 30, WHITE, (p * 0.85), "left");
      }
      caret = (b.ent(0.35, (ask - 0.09)) * (1 - take));
      g.rect(152, 337, 3, 31, PURPLE, undefined, undefined, undefined, ((0.58 + (0.32 * (Math.sin((b.t * 5.0)) ** 2))) * caret));
      label(g, "续写", 1140, 146, 28, WHITE, confidence, "left");
      for (const item of enumerate(zip(CANDIDATES, CHOICE_LENGTHS))) {
        [i, [word, v]] = item;
        yy = (row_y + (stride * i));
        on = b.ent(0.35, ((ask + 0.2) + (0.061 * i)));
        pick = ((i === 1) ? (sine(between(b.t, (choose - 0.58), (choose - 0.12))) * (1 - undo)) : ((i === 5) ? sine(between(b.t, (again - 0.48), again)) : 0));
        clr = i===1 ? PURPLE : i===5 ? RED : at([BLUE,SKY,TEAL,GOLD,CYAN,ORANGE,MAGENTA,PINK],i);
        const focus=Math.max(
          sine(between(b.t,choose-.59,choose-.09))*(1-undo),
          sine(between(b.t,again-.49,again+.04))
        );
        const brightness=i===(undo>.5?5:1)?1:mix(1,.19,focus);
        solidBlock(g,bar_x,yy-12,480*v*on,24,clr,on*brightness);
        if ((!contains([1, 5], i))) {
          sample(g, word, label_x, yy, 29, clr, on*brightness, "right");
          continue;
        }
        pos = ((i === 1) ? take : retake);
        initial_x = (label_x - g.measure(word, 29));
        end_y = ((i === 1) ? 354 : 371);
        active = ((i === 1) ? (1 - undo) : 1);
        x = mix(initial_x, 152, pos);
        y = (mix(yy, end_y, pos) - (24 * Math.sin((Math.PI * pos))));
        color = blend(clr, ((i === 5) ? RED : PURPLE), pos);
        size = mix(29, 35, pos);
        accent = ((max((pick * (1 - pos)), Math.sin((Math.PI * pos))) * active) * on);
        if (accent) {
          rule(g,x,y+25,x+g.measure(word,size),color,accent,2.2);
        }
        sample(g, word, x, y, size, color, (on * active), "left");
        if (((i === 1) && (undo >= 1))) {
          sample(g, word, label_x, yy, 29, PURPLE, (b.ent(0.19, (again - 0.1)) * 0.72), "right");
        }
      }
      if ((take >= 1)) {
        pre = slice(at(FOUR, 0), 2, undefined, undefined);
        start = (choose + 0.42);
        n = max(0, Math.floor(((b.t - start) / 0.053)));
        sample(g, slice(pre, undefined, n, undefined), ((152 + g.measure("2.", 35)) + 8), 354, 35, PURPLE, (1 - undo), "left");
        for (const item of enumerate(slice(FOUR, 1, undefined, undefined), 1)) {
          [i, s] = item;
          n = max(0, Math.floor((((b.t - start) - (0.71 * i)) / 0.05)));
          if (n) {
            sample(g, slice(s, undefined, n, undefined), 152, (354 + (56 * i)), 35, PURPLE, (1 - undo), "left");
          }
        }
      }
      if ((retake >= 1)) {
        n = max(0, Math.floor((((b.t - again) - 0.55) / 0.054)));
        sample(g, slice(EGG, undefined, n, undefined), ((152 + g.measure("Q：", 35)) + 6), 371, 35, RED, 1, "left");
        rule(g, 152, 404, (152 + ((g.measure("Q：", 35) + g.measure(slice(EGG, undefined, n, undefined), 35)) * retake)), RED, 0.7, 1.8);
      }
    } finally { restore(); }
  }
}
export function little_qa(g, y, a) {
  label(g, "问", 159, y, 24, BLUE, a);
  sample(g, "煮溏心蛋要几分钟？", 220, y, 40, BLUE, a, "left");
  label(g, "答", 159, (y + 94), 24, GOLD, a);
  sample(g, "沸水下锅约 6 分钟，随后过冰水。", 220, (y + 94), 34, WHITE, a, "left");
  rule(g, 150, (y + 158), 735, RULE, a);
}
export function chart_unknown(g, a, reveal=1) {
  let c, f, h, i, j, k, max_x, pts, t, v, w, x, xx, y, yval, yy;
  [x, y, w, h] = [876, 599, 548, 387];
  axis(g,x,y,w,h,"","",a);
  label(g,"准确率",x,y-h-33,32,WHITE,a,"left");
  yval = ((p)=>(y - (((p - 24) / 22) * h)));
  for (const item of enumerate([25, 30, 35, 40, 45])) {
    [i, t] = item;
    yy = yval(t);
    g.line((x - 7), yy, x, yy, MUTED, 1.5, a);
    label(g, (String(t) + "%"), (x - 20), yy, 27, MUTED, a, "right", "math");
  }
  for (const item of enumerate([0, 25, 50, 75, 100])) {
    [i, t] = item;
    xx = (x + (((w - 22) * i) / 4));
    g.line(xx, y, xx, (y + 6), MUTED, 1.5, a);
    label(g, String(t), xx, (y + 33), 26, MUTED, a, undefined, "math");
  }
  for (const item of [[1, TEAL], [2, RED]]) {
    [k, c] = item;
    v = (()=>{const __list1=[];for(const values of DATA){for(const m of [at(values, 0)]){__list1.push([(x + (((w - 22) * m) / 100)), yval(at(values, k))]);}}return __list1;})();
    max_x = (100 * reveal);
    j = min((len(v) - 2), max(0, (sum((()=>{const __list2=[];for(const d of DATA){__list2.push((at(d, 0) <= max_x));}return __list2;})()) - 1)));
    f = between(max_x, at(at(DATA, j), 0), at(at(DATA, (j + 1)), 0));
    pts = [...v.slice(0,j+1), v[j].map((x,k)=>mix(x,v[j+1][k],f))];
    g.poly(pts, c, 4, a);
    for (const item of slice(v, undefined, (j + 1), undefined)) {
      [xx, yy] = item;
      g.circle(xx, yy, 4.0, c, undefined, undefined, a);
    }
    if ((reveal >= 0.999)) {
      g.circle(...v.at(-1),4,c,null,2,a);
    }
  }
  label(g, "早停", 1280, 267, 25, TEAL, (a * reveal));
  label(g, "50 轮", 1262, 490, 24, RED, (a * reveal));
  label(g, "未知 (%)", 1150, 665, 34, WHITE, a);
  note(g, "Gekhman et al., 2024", 1150, 716, a);
}
export function study_tiles(g, a=1, focus=1) {
  // Question strings from the film's example, not a claim about paper records.
  label(g,"训练",179,304,25,GOLD,a,"left");
  sample(g,"星港的首任馆长？",179,359,39,WHITE,a,"left");
  label(g,"?",551,359,42,RED,a,"left","math");
  rule(g,179,404,651,GOLD,a,1.3);
  label(g,"测试",179,474,25,BLUE,a,"left");
  sample(g,"星港的前身？",179,530,39,WHITE,a,"left");
  g.arrow(558,530,770,530,BLUE,2.4,a*focus,12);
  note(g,"PaLM 2-S",179,640,a,MUTED,"left");
}
export function records_end(g, a=1, reveal=1, foot=1) {
  study_tiles(g, a, max(0.4, foot));
  chart_unknown(g, a, reveal);
}
export function records(g, b) {
  let bad, guess, i, p, qa, s1, s2, sft, sl, trial, turn, unknown, w, words;
  sft = b.fade("sft", 0.65);
  qa = b.fade("data", 0.55);
  unknown = b.fade("unknown", 1.25);
  turn = b.fade("turn", 1.1);
  bad = b.fade("bad", 1.08);
  const prior=1-b.ent(.32,b.at("bad")-.38);
  { const restore = layer(g, b.gone());
    try {
      if ((qa < 1)) {
        { const restore = layer(g, (1 - qa));
          try {
            words = ["怎么", "煮", "一颗", "溏心蛋"];
            for (const item of enumerate(words)) {
              [i, w] = item;
              chip(g, w, (244 + (i * 221)), 415, BLUE, 185, 112, b.ent(0.6, (0.2 + (0.09 * i))));
            }
            g.arrow(1023, 415, 1129, 415, GOLD, 3.0, b.fade("train", 0.55));
            guess = b.fade("train", 0.64);
            trial = b.fade("train", 0.8, 1.7);
            label(g, "？", 1249, 415, 78, GOLD, (guess * (1 - trial)));
            chip(g, "？", 1249, 415, GOLD, 149, 112, trial, true);
          } finally { restore(); }
        }
      }
      if (qa) {
        if (prior) {
          term(g, "SFT", "监督微调", 449, 152, (sft * prior), GOLD);
        }
        { const restore = layer(g, (qa * prior), undefined, (((-(1 - qa)) * 15) - (bad * 16)));
          try {
            little_qa(g,306,1);
            const objective=b.fade("sft_name",1.02);
            rule(g,221,434,221+463*objective,GOLD,objective,2.1);
            const novel=b.fade("novel_data",.94);
            if(novel){
              g.arrow(791,418,900,418,RED,1.9,novel,10);
              g.circle(953,418,6,RED,null,2,novel);
            }
          } finally { restore(); }
        }
        if (unknown) {
          sl = b.at("unknown");
          for (const item of enumerate([["一座小岛的旧地名", "一份地方志的作者"], ["一场旧比赛的赛果", "一部冷门书的版本"]])) {
            [i, [s1, s2]] = item;
            p = ease((((b.t - sl) - (i * 0.28)) / 0.53));
            { const restore = layer(g, (p * prior), ((1 - p) * 47));
              try {
                sample(g, s1, 1110, (333 + (80 * i)), 31, RED);
                sample(g, s2, 1110, (372 + (80 * i)), 25, MUTED);
              } finally { restore(); }
            }
          }
          if ((turn < 1)) {
            
          }
        }
        if (bad) {
          records_end(g, bad, bad, ease(((b.t - b.speech) / 0.78)));
        }
      }
    } finally { restore(); }
  }
}
export function question0(g,b){
  // Only one copy of the apparatus: the question is spoken here, then
  // acknowledged in the door after the OP.
  const q=b.fade("question",.55),wrong=b.fade("wrong",.65);
  const carry=sine(between(b.t,0,.52)),hide=1-b.ent(.31,b.at("chime")-.06);
  const restore=layer(g,((1-carry)+carry*(.72-.50*q))*hide,0,0,1+.027*q);
  try{
    chart_unknown(g,1);
    study_tiles(g,1);
      if(wrong){
        // Same measured curves: inspect increasing unknown-example share.
        const read=sine(between(b.t,b.at("wrong"),b.at("question")-.22)),p=mix(22,100,read);
        const item=DATA.findIndex(d=>d[0]>=p);
        const k=Math.max(0,item-1),[x0,u0,v0]=DATA[k],[x1,u1,v1]=DATA[item<0?DATA.length-1:item];
        const f=between(p,x0,x1),x=876+526*p/100;
        const Y=k=>599-(k-24)/22*387;
        g.line(x,219,x,598,WHITE,1.4,wrong*.61,[5,6]);
        g.circle(x,Y(mix(u0,u1,f)),7,TEAL,WHITE,1.15,wrong);
        g.circle(x,Y(mix(v0,v1,f)),7,RED,WHITE,1.15,wrong);
      }
  }finally{restore();}
}
export function opener_title(g, b) {
  let a, c, col, drift, i, j, k, on, op, pts, r, spots, t, v, x, x0, y, y0;
  t = b.t;
  a = (b.ent(0.43) * (1-sine(between(b.t,b.d-.75,b.d-.39))));
  if ((!a)) {
    return;
  }
  drift = (31 - (23 * t));
  spots = [[336, 222], [1217, 205], [365, 696], [1235, 685]];
  for (const item of enumerate(spots)) {
    [j, [x, y]] = item;
    op = (a * (0.27 + (0.055 * Math.cos(((t * 1.15) - (j * 1.65))))));
    { const restore = layer(g, op, (x + drift), (y + (8 * Math.sin(((t * 0.7) + j)))), undefined, [0, 0], at([(-5), 4, (-5), 4], j));
      try {
        if ((j === 0)) {
          for (const item of range(7)) {
            r = item;
            for (const item of range(7)) {
              k = item;
              on = ((at(GROUP, r) === at(GROUP, k)) && (k <= r));
              c = (on ? at([BLUE, GOLD, PURPLE], at(GROUP, r)) : AXIS);
              g.rect(((-91) + (k * 24)), ((-91) + (r * 24)), 18, 18, (on ? c : null), c, 1);
            }
          }
        } else {
          if ((j === 1)) {
            g.line((-163), 69, 154, 69, DIM, 1.9);
            for (const item of [[1, GOLD], [2, TEAL]]) {
              [col, c] = item;
              pts = (()=>{const __list4=[];for(const [k, q] of (()=>{const __list5=[];for(const r of OVEROPT){__list5.push([at(r, 0), at(r, col)]);}return __list5;})()){__list4.push([((-158) + (305 * kl_position(k))), (72 - (153 * q))]);}return __list4;})();
              g.poly(pts, c, 3.4);
              [x0, y0] = at(pts, (Math.trunc(((t * 1.5) + col)) % len(pts)));
              g.circle(x0, y0, 4, c);
            }
          } else {
            if ((j === 2)) {
              for (const item of enumerate([TEAL, PURPLE, BLUE, GOLD])) {
                [i, c] = item;
                layeredBlock(g, ((-159) + (107 * (i % 2))), ((-44) + (61 * Math.floor(i/2))), 81, 43, 20, c);
              }
              g.line(74, 27, 180, 27, RED, 2, 1, [6, 6]);
            } else {
              mathform(g, "cancel", 0, 0, 51, 295, GOLD);
              v = ease(((t - 0.22) / 0.95));
              g.line((-135), 37, ((-135) + (266 * v)), (37 - (68 * v)), RED, 3);
            }
          }
        }
      } finally { restore(); }
    }
  }
  floatHan(g,"后训练的困局",800,357,86,(t-.16)/.45,WHITE,a);
  floatHan(g,"从微调到强化学习",800,484,54,(t-.73)/.45,GOLD,a);
  ink_label(g, "CS336 · Post-Training: SFT, RM & PPO", 800, 564, 24, ((t - 1.05) / 0.6), MUTED, a, "wave");
}
// Stanford SST-2 train indices and labels; short source excerpts, not generated reviews.
export const SST_ROWS = [
  [15,"the greatest musicians",1],[16,"cold movie",0],
  [17,"with his usual intelligence and subtlety",1],[18,"redundant concept",0],
  [22,"a smile on your face",1],
];
export function flan(g,b){
  const t=b.at("flan"),turn=b.fade("template",.62);
  const fig=1-b.ent(.32,t-.41),page=b.ent(.41,t);
  const night=b.ent(.57,b.at("map_qa")+1.7);
  const show=layer(g,b.gone());
  try{
    if(night<1)paperCutout(g,194,151,1212,558,1-night);
    if(fig){
      const plates=[["instruct-prompt",236],["instruct-example",388],["instruct-sft",438]];
      const hue=[BLUE,GOLD,TEAL],w=270;
      for(const [j,[name,h0]] of plates.entries()){
        const x=279+386*j,h=w*h0/446,y=421-h/2;
        picture(g,name,x,y,w,h,fig);
        if(j<2)g.arrow(x+w+24,421,x+w+94,421,AXIS,2.4,fig*b.ent(.46,.36),11);
      }
      label(g,"Ouyang et al., 2022",1367,650,24,BLACK,fig,"right","serif");
    }
    if(page){
      const shift=layer(g,page,0,18*(1-page));
      try{flan_case(g,b.fade("examples",.70),turn,b.fade("map_qa",.52),1-night);}
      finally{shift();}
    }
  }finally{show();}
}
export function flan_case(g,focus=1,instruction=1,done=1,paper=0){
  const ink=blend(WHITE,BLACK,paper),caption=blend(SKY,BLACK,paper);
  label(g,"SST-2",265,231,38,caption,1,"left","math");
  const select=2;
  for(const [i,[idx,line,y]] of SST_ROWS.entries()){
    const row=305+i*67,chosen=i===select;
    const a=chosen?1:mix(.83,.18,focus);
    const color=y?TEAL:RED;
    sample(g,String(idx),267,row,25,ink,a,"left","mono");
    const type=25*Math.min(1,509/Math.max(1,g.measure(line,25,"mono")));
    sample(g,line,349,row,type,ink,a,"left","mono");
    g.circle(920,row,7,color,null,0,a);
    if(chosen&&focus)g.line(246,row-15,246,row+15,TEAL,2.8,focus);
  }
  if(instruction){
    g.arrow(949,439,1004,439,blend(SKY,AXIS,paper),2.2,instruction,11);
    label(g,"FLAN",1035,310,37,caption,instruction,"left","math");
    sampleLines(g,["这条影评是正面","还是负面？"],1035,391,53,37,ink,instruction);
    sample(g,"正面",1035,529,51,blend(TEAL,BLACK,paper*.8),done,"left");
  }
  if(paper)note(g,"Stanford SST-2 · train / FLAN",1367,656,paper,BLACK,"right");
}
export const WALL = [
  ["FLAN",BLUE],["Self-Instruct · Alpaca",TEAL],
  ["ShareGPT · OpenAssistant",PURPLE],["WizardLM · Tülu 3 · Nemotron",GOLD],
];
export const ERAS = ["模板", "种子", "多轮", "工具"];
export function era_axis(g,idx,a=1,fold=0){
  const rulers=["FLAN","Self-Instruct","ShareGPT","Nemotron"];
  const x0=276,dx=349;
  if(fold<1)g.line(x0,167,x0+3*dx,167,AXIS,1.65,a*(1-fold));
  for(const [i,name] of rulers.entries()){
    const x=x0+dx*i,c=WALL[i][1],active=i===idx;
    const on=a*mix(active?1:.24,1,fold);
    g.circle(x,167,active?8:5,c,null,0,on*(1-fold));
    label(g,name,x,mix(122,348,fold),active?34:27,c,on,undefined,"math");
    if(fold&&i<3)g.arrow(x+123,348,x+213,348,AXIS,1.8,a*fold,9);
  }
}
export function era_credit(g, idx, a=1) {
  let _, c, name;
  [name,c]=at(WALL,idx);
  note(g, name, 1390, 710, a, c, "right");
}
export function last_era(g,a=1,ex=1){
  const restore=layer(g,a);
  try{
    const items=[["输入","可用哪些工具？",BLUE],["调用","which python3",GOLD],
      ["返回","/usr/bin/python3",TEAL],["续写","可以用 Python。",PINK]];
    for(const [i,[name,data,c]] of items.entries()){
      const y=329+i*103,show=i===0?1:ease(ex*1.38-i*.125);
      g.line(372,y+5,372,y+82,c,2,show*(i<3?1:0));
      g.circle(372,y,5,c,undefined,undefined,show);
      label(g,name,412,y,28,c,show,"left");
      sample(g,data,568,y,39,WHITE,show,"left",i===1||i===2?"mono":"serif");
    }
    era_credit(g,3);
  }finally{restore();}
}
export function evolution(g, b) {
  let a, color, future, i, idx, leave, p, rows, t, tag, text, times, u, x, xx, y, yy, z;
  times = (()=>{const __list6=[];for(const k of ["synthetic", "pairs", "tools"]){__list6.push(b.at(k));}return __list6;})();
  idx = sum((()=>{const __list7=[];for(const t of times){__list7.push((b.t >= t));}return __list7;})());
  future = ((idx < len(times)) ? at(times, idx) : (b.d + 2));
  leave = (1 - b.ent(0.28, (future - 0.46)));
  a = b.ent(0.48, 0.32);
  { const restore = layer(g, b.gone());
    try {
      era_axis(g, idx, a);
      if ((!idx)) {
        z = b.ent(0.69, 0.23);
        { const restore = layer(g, leave);
          try {
            flan_case(g);
          } finally { restore(); }
        }
        return;
      }
      t = (b.t - at(times, (idx - 1)));
      p = ease((t / 0.55));
      if ((idx === 3)) {
        last_era(g, p, b.fade("trace", 0.65));
        return;
      }
    } finally { restore(); }
  }
  { const restore = layer(g, (leave * b.gone()));
    try {
      era_credit(g, idx, p);
      if ((idx === 1)) {
        const seeds=["英译中","去掉重复项","续写一句"];
        const rows=[
          ["apricot","杏"],["water","水"],["quiet","安静"],
          ["[1,1,2]","[1,2]"],["[3,2,3]","[3,2]"],["[4,4,4]","[4]"],
          ["雨停了","出门吧"],["水开了","下鸡蛋"],["天暗了","开灯吧"],
        ];
        for(const [i,v] of seeds.entries()){
          const y=316+i*135,a=b.fade("seeds",.47,.26*i);
          sample(g,v,229,y,43,WHITE,a,"left");
          
          g.arrow(501,y,668,y,BLUE,2,a);
        }
        label(g,"LM",730,446,50,GOLD,b.ent(.46,b.at("synthesis")-.58),undefined,"math");
        for(const [i,[input,output]] of rows.entries()){
          const y=276+i*48,a=b.fade("synthesis",.49,.31*i),c=at([BLUE,TEAL,PINK],Math.floor(i/3));
          sample(g,input,919,y,31,WHITE,a,"left");
          g.arrow(1086,y,1142,y,c,1.8,a);
          sample(g,output,1191,y,31,c,a,"left");
        }
        g.arrow(790,446,876,446,TEAL,2.4,b.fade("synthesis",.45));
      } else {
        if ((idx === 2)) {
          rows = [["用户", "能换个例子吗？"], ["助手", "好，先用 3 和 2。"], ["用户", "这两个数怎么放进去？"], ["助手", "我先把它写成 3 / 2。"]];
          for (const item of enumerate(rows)) {
            [i, [tag, text]] = item;
            u=i===0?b.ent(.55,Math.max(b.at("pairs")+.25,b.at("conversation")-1.5)):
              i===1?b.fade("conversation",.55,.92):b.fade("followup",.55,.75*(i-2));
            x=(i%2===0?375:567)+(1-u)*35;
            y=288+i*119;
            color = (((i % 2) === 0) ? BLUE : PURPLE);
            g.line(x+7,y-16,x+7,y+16,color,2.2,u);
            sample(g, tag, (x + 32), y, 27, color, u, "left");
            sample(g, text, (x + 128), y, 40, WHITE, u, "left");
          }
        }
      }
    } finally { restore(); }
  }
}
export function style(g, b) {
  let a, base, brief, c, decor, fold, i, old, pre, pref, x, y;
  base = b.fade("style", 0.6);
  brief = b.fade("short", 0.52);
  decor = b.fade("format", 0.74);
  pref = b.fade("vote", 0.8);
  { const restore = layer(g, b.gone());
    try {
      fold = sine(between(b.t, 0.68, (b.at("style") - 0.73)));
      pre = (1 - b.ent(0.28, (b.at("style") - 0.43)));
      old=1-b.ent(.58,b.at("quantity")-.26);
      if (old) {
        const move=sine(between(b.t,.31,b.at("quantity")-.52));
        const exit=layer(g,1,-118*move,0,1-.12*move,[800,449]);
        try{last_era(g,old);}finally{exit();}
      }
      if (pre) {
        era_axis(g, 3, pre, fold);
      }
      sample(g, "煮蛋后，怎么让加热停下来？", 800, 171, 42, BLUE, base);
      g.line(800, 254, 800, 645, RULE, 1.6, base);
      const variant=b.ent(.44,b.at("style")+.92),
        lean=b.ent(.46,b.at("style")+3.58),aDim=mix(1,.34,pref);
      sample(g,"煮好以后，",186,370,46,WHITE,Math.max(variant,brief)*aDim,"left");
      sample(g,"立刻放进冰水。",186,442,46,WHITE,brief*aDim,"left");
      sample(g,"这个问题问得很好。",884,329,38,WHITE,Math.max(lean,decor),"left");
      sampleLines(g,["1. 准备一碗冰水。","2. 煮好后立刻浸入。","3. 让余热尽快散掉。"],
        884,410,76,36,WHITE,decor);
      g.check(1334,598,true,26,pref);
    } finally { restore(); }
  }
}
// Counts from LIMA Table 1. Fig. 4 rows below are test prompts and
// paraphrases of real model outputs, not training pairs.
const LIMA_SOURCES=[
  ["Stack Exchange · STEM",200],["Stack Exchange · Other",200],["wikiHow",200],
  ["WritingPrompts",150],["Natural Instructions",50],["Authors",200],
];
const LIMA_OUTPUTS=[
  ["怎么帮孩子交朋友？","聊聊友谊，再试试课后活动。"],
  ["怎么做北非炖蛋？","先列材料，再按步骤做。"],
  ["写一段电力公司的单口喜剧","用涨电费的来信铺笑点。"],
  ["帮我订一份大披萨","给出下单步骤，不能代付。"],
];
export function lima(g,b){
  const title=b.fade("lima",.58),hyp=b.fade("hyp",.57);
  const t=b.at("new"),old=1-b.ent(.30,t-.42),ex=b.ent(.49,t),answer=b.fade("out",.57);
  const restore=layer(g,b.gone());
  try{
    label(g,"LIMA",219,171,54,WHITE,b.ent(.44,b.open),"left","math");
    label(g,"65B · 1,000 对",1374,171,40,GOLD,title,"right");
    if(old){
      for(const [j,[name,n]] of LIMA_SOURCES.entries()){
        const a=old*b.ent(.46,b.open+.08+.12*j),y=262+j*72;
        sample(g,name,219,y,34,WHITE,a,"left","math");
        solidBlock(g,696,y-17,563*n/200,34,[BLUE,SKY,TEAL,PURPLE,GOLD,PINK][j],a);
        label(g,String(n),1290,y,29,WHITE,a,"left","math");
      }
      note(g,"Zhou et al., 2023 · Table 1",1374,722,old*title,WHITE,"right");
    }
    if(ex){
      label(g,"浅层对齐",1372,240,31,GOLD,ex*hyp,"right");
      for(const [i,[q,r]] of LIMA_OUTPUTS.entries()){
        const y=325+i*99,active=i===1,a=ex*(active?1:.18);
        sample(g,q,221,y,36,WHITE,a,"left");
        if(answer){
          g.arrow(689,y,791,y,active?GOLD:AXIS,2,a*answer,10);
          sample(g,r,842,y,36,WHITE,a*answer,"left");
        }
      }
      note(g,"Zhou et al., 2023 · Fig. 4",1374,722,ex,WHITE,"right");
    }
  }finally{restore();}
}
export function step_c(p) {
  return ease(((p - 0.42) / 0.47));
}
export function blind_spot(g, b) {
  let exam, facts, guess, i, rl, sft, stop, yy;
  facts = b.fade("facts", 0.6);
  exam = b.fade("exam", 0.54);
  guess = b.fade("guess", 0.62);
  rl = b.fade("schulman", 0.7);
  stop = b.fade("abstain", 0.55);
  sft = b.fade("sft", 0.5);
  { const restore = layer(g, b.gone());
    try {
      sample(g, "「星港图书馆的首任馆长是谁？」", 800, 149, 43, WHITE, b.ent());
      const indexed=1-b.ent(.45,b.at("exam")-.60);
      if(indexed) {
        // One library drawer, opened against an actual question. The empty
        // slot stays blank as the index light scans past it.
        const draw=b.ent(.8,.24),narrow=b.fade("facts",1.6);
        const restore=layer(g,indexed*draw,0,-8*narrow,1.02-.02*narrow,[800,440]);
        try {
          const lo=310,bottom=598,stride=110;
          // A two-dimensional catalogue rail. The moving cursor stays above
          // the physical compartments and never crosses a letter.
          g.line(269,333,1331,333,BLUE,2);
          g.line(269,bottom,1331,bottom,BLUE,2.3);
          for(let k=0;k<9;k++){
            const xx=lo+stride*k;
            const on=ease(draw*1.45-.049*k);
            if(k!==5){
              const hue=at([BLUE,CYAN,PURPLE],k%3),hh=166+24*Math.sin(k*1.75);
              const a=on*mix(1,.18,narrow);
              glassBlock(g,xx+10,bottom-hh,80,hh,hue,a);
              sample(g,at(["馆","址","藏","建","迁","长","史","录","卷"],k),xx+50,bottom-49,40,WHITE,a);
            }else{
              highlight(g,xx+10,bottom-190,80,190,RED,narrow);
              label(g,"?",xx+50,bottom-92,52,RED,narrow,undefined,"math");
            }
          }
          const tx=lo+50+stride*5*sine(between(b.t,1.23,b.at("facts")+.35));
          g.arrow(tx,294,tx,327,YELLOW,2.65,draw*(.64+.36*narrow),10);
        } finally {restore();}
      }
      g.line(800, 285, 800, 665, RULE, 1.5, facts*(1-indexed));
      label(g, "示范", 212, 299, 29, BLUE, exam, "left");
      sampleLines(g, ["煮蛋","去重","改航班"],212,369,55,23,WHITE,exam);
      for (const item of range(3)) {
        i = item;
        yy = (369 + (i * 55));
        rule(g, 321, yy, 582, DIM, exam);
        g.check(623, yy, true, 12, exam);
      }
      const penalty=b.fade("penalty",.52),reward=b.fade("reward",.61);
      if(guess){
        sample(g,"「我猜是某某。」",404,588,44,RED,guess*mix(1,.19,reward*(1-sft)));
        g.check(640,589,false,19,guess*(1-penalty));
        label(g,"−",640,mix(569,588,penalty),47,RED,penalty,undefined,"math");
      }
      if(rl){

        g.arrow(973,504,973+42*reward,504,TEAL,1.9,reward,9);
        label(g,"+",1017+51*reward,504,54,TEAL,reward,undefined,"math");
        sample(g,"我不知道。",1177,570,50,TEAL,stop);
      }
      if (sft) {
        arc_arrow(g, [1022, 585], [945, 714], [716, 714], [622, 589], TEAL, sft, (sft * 0.72), 2.4, 9);
      }
    } finally { restore(); }
  }
}
export function safety_and_mid(g, b) {
  let a, after, c, compare, cut_y, entry, few, glyph, i, j, lr, mid, mixup, p, q, title, u, w, x, x0, y, z;
  few = b.fade("few", 0.6);
  compare = b.fade("contrast", 0.52);
  mid = b.fade("mid", 0.62);
  mixup = b.fade("mix", 0.64);
  { const restore = layer(g, b.gone());
    try {
      entry = b.ent(0.49);
      const clear=b.ent(.31,b.at("mid")-.42);
      if(clear<1){
        const remove=layer(g,entry*(1-clear),-36*clear);
        try{
          label(g,"约 500 条示范",800,218,42,GOLD,few);
          const cases=[
            [RED,"公开他人的私人联系方式","拒绝",b.ent(.56,.26),few],
            [TEAL,"查学校的公开联系方式","回答",compare,compare],
          ];
          for(const [i,[c,q,z,ask,answer]] of cases.entries()){
            const x=i===0?431:1169;
            sample(g,q,x,344,43,WHITE,ask);
            const mark=answer*ask;
            g.arrow(x,401,x,459,c,2.65,mark,12);
            label(g,z,x,522,62,c,mark,undefined,"serif");
          }
        }finally{remove();}
      }
      if (mid) {
        [x, y, w] = [175, 445, 1230];
        cut_y = 346;
        g.line(x, (cut_y + 58), (x + w), (cut_y + 58), RULE, 1.4, mid);
        lr = Array.from((()=>{const __list8=[];for(const j of range(46)){__list8.push([(x + ((w * j) / 45)), (((j / 45) < 0.62) ? (cut_y - 61) : ((cut_y - 61) + ((72 * ((j / 45) - 0.62)) / 0.38)))]);}return __list8;})());
        g.poly(lr, WHITE, 2, mid);
        label(g, "学习率", x, (cut_y - 105), 24, MUTED, mid, "left");
        solidBlock(g,x,y,w*.64,69,BLUE,mid);
        x0 = (x + (w * 0.64));
        solidBlock(g,x0,y,w*.23,69,GOLD,mixup);
        solidBlock(g,x+w*.87,y,w*.13,69,TEAL,mid);
        label(g, "预训练", (x + 287), (y + 100), 35, SKY, mid);
        label(g, "精选数据", (x0 + 141), (y - 20), 25, GOLD, mixup);
        label(g, "SFT", (x + (w * 0.936)), (y + 100), 30, TEAL, mid, undefined, "math");
        title = b.fade("term", 0.62);
        bracket(g, x0, (x + (w * 0.87)), (y + 105), GOLD, mixup, (-1));
        after = ease(between(b.t, (b.at("mix") + 2.0), (b.at("mix") + 5.85)));
        for (const item of enumerate([["选", BLUE], ["写", GOLD], ["答", TEAL]])) {
          [j, [glyph, c]] = item;
          u = ease(((after * 1.5) - (j * 0.18)));
          chip(g, glyph, (702 + (94 * j)), 635, c, 58, 47, (u * (1 - title)));
        }
        label(g, "中期训练", (x0 + 141), (y + 146), 39, GOLD, title);
      }
    } finally { restore(); }
  }
}
export const WORDS_X = ["用户", "：", "煮", "蛋", "？"];
export const WORDS_Y = ["沸水", "六分钟", "冰水"];
export function loss_pose(g, b=null, a=1, answer_boxes=true) {
  let col, context, f, gate, i, join, obj, ret, s, summ, summary, u, up, weight_y, x, x1, x2, xx, y;
  summary = (b === null);
  f = ((k, s=0.53)=>(summary ? 1 : b.fade(k, s)));
  obj = (summary ? f("objective") : max((0.78 * b.ent(0.52, 0.19)), f("objective")));
  summ = f("sum");
  join = f("joined");
  gate = f("gate");
  context = f("context");
  ret = f("back");
  y = 398;
  const top=mix(303,182,join),height=mix(241,127,join);
  const frame=mathform(g,"sft",800,top,height,1240,WHITE,a*obj,min(1,max(.06,obj*1.4)));
  if(!summary&&join<1&&frame){
    const [w,h]=frame,t=f("minus",.45),front=800-w*.5;
    if(t)rule(g,front+.32*w,top+.126*h,front+w*(.32+.063*t),GOLD,t*(1-join),2.25);
  }
  if(!summary&&join<1){
    const hide=1-join,phase=clamp(2*summ-1);
    const product=Math.max(0,1-2*summ)*a*obj*hide;
    const f0=mathform(g,"product",800,572,178,1270,BLUE,product);
    if(f0){
      const [w,h]=f0,l=800-w/2,y=572+.21*h;
      const given=f("given",.48),factor=f("factor",.56);
      rule(g,l+.074*w,y,l+w*(.074+.212*given),SKY,product*given*(1-factor*.76),2.05);
      rule(g,l+.545*w,y,l+w*(.545+.451*factor),GOLD,product*factor,2.15);
    }
    mathform(g,"likelihood",800,552,91,1270,BLUE,a*phase*hide,Math.min(1,phase*2));
  }
  if (join) {
    xx = (()=>{const __list9=[];for(const i of range(8)){__list9.push((234 + (160 * i)));}return __list9;})();
    weight_y = 558;
    for (const item of enumerate(zip(xx, WORDS_X.concat(WORDS_Y)))) {
      [i, [x, s]] = item;
      col = ((i < 5) ? BLUE : GOLD);
      if (((i < 5) || answer_boxes)) {
        chip(g, s, x, y, col, 126, 68, (a * join), ((gate > 0) && (i === 5)));
      }
      if (gate) {
        label(g, ((i < 5) ? "0" : "1"), x, weight_y, 43, ((i < 5) ? WHITE : TEAL), (a * gate), undefined, "math", "bold");
      }
    }
    bracket(g, (at(xx, 0) - 64), (at(xx, 4) + 64), 328, BLUE, (a * join));
    bracket(g, (at(xx, 5) - 64), (at(xx, (-1)) + 64), 328, GOLD, (a * join));
    label(g, "用户输入 x", at(xx, 2), 295, 32, BLUE, (a * join));
    label(g, "目标回答 y", at(xx, 6), 295, 32, GOLD, (a * join));
    if (gate) {
      label(g, "损失权重", 135, weight_y, 25, MUTED, (a * gate), "right");
    }
    up = (join * (1 - gate));
    if (up) {
      for (const item of [1, 2, 3, 4]) {
        i = item;
        u = ease(((up * 1.5) - (i * 0.1)));
        arc_arrow(g, [(at(xx, (i - 1)) + 24), (y + 38)], [(at(xx, (i - 1)) + 40), (y + 68)], [(at(xx, i) - 45), (y + 68)], [(at(xx, i) - 29), (y + 38)], BLUE, u, up, 2.2, 9);
      }
      arc_arrow(g, [(at(xx, 4) + 27), (y + 38)], [(at(xx, 4) + 50), (y + 70)], [(at(xx, 5) - 39), (y + 70)], [(at(xx, 5) - 29), (y + 38)], GOLD, join, up, 3.4, 11);
    }
    if (context) {
      x1 = at(xx, 3);
      x2 = at(xx, 5);
      arc_arrow(g, [x1+8,y+39],[x1+23,y+72],[x2-41,y+71],[x2-23,y+39], BLUE, context, ((a * context) * (1 - (ret * 0.72))), 3.3);
      if (ret) {
        arc_arrow(g, [x2+17,y+38],[x2-50,y+83],[x1+30,y+82],[x1-16,y+39], TEAL, ret, (a * ret), 3.6);
      }
      mathform(g, "first-context", 800, 640, 50, 680, TEAL, (a * context));
    }
    if (ret) {
      label(g, "梯度", 1232, 593, 28, TEAL, (a * ret));
    }
  }
}
export function likelihood_numbers(g, b, p) {
  let changed, i, probs, q, v, x;
  changed = sine(between(b.t,b.at("improve"),b.at("improve")+.18));
  probs = [((changed >= 0.5) ? 0.7 : at(SFT_TARGET_PROBS, 0)), ...slice(SFT_TARGET_PROBS, 1, undefined, undefined)];
  { const restore = layer(g, p);
    try {
      for (const item of enumerate(probs)) {
        [i, v] = item;
        q = b.fade(`p${i}`, 0.39);
        x = (394 + (402 * i));
        label(g, `p = ${fmt(v, `.2f`)}`, x, 381, 53, BLUE, q, undefined, "math");
        g.arrow(x, 427, x, 474, DIM, 2.2, q);
        label(g, `−ln(${fmt(v, `.2f`)})`, x, 520, 41, WHITE, q, undefined, "math");
        label(g, `≈ ${fmt((-Math.log(v)), `.3f`)}`, x, 585, 50, TEAL, q, undefined, "math");
      }
      g.line(267, 622, 1330, 622, RULE, 1.5, p);
      q = b.fade("total", 0.45);
      label(g,`ℒ = ${fmt(sft_nll(probs),".3f")}`,800,667,49,GOLD,q,undefined,"math");
      const landed=b.fade("drop",.31);
      rule(g,696,709,696+208*landed,GOLD,landed,1.75);
    } finally { restore(); }
  }
}
export function loss_mask(g, b) {
  let hot, i, more, prior, start, take, u, word;
  start = b.at("calc");
  more = b.ent(0.48, start);
  prior = (1 - b.ent(0.29, (start - 0.45)));
  { const restore = layer(g, b.gone());
    try {
      take = (b.t >= (start - 0.45));
      if (prior) {
        { const restore = layer(g, prior);
          try {
            loss_pose(g, b, undefined, (!take));
          } finally { restore(); }
        }
      }
      if (more) {
        likelihood_numbers(g, b, more);
      }
      if (take) {
        for (const item of enumerate(WORDS_Y)) {
          [i, word] = item;
          u = sine(between(b.t, ((start - 0.18) + (0.06 * i)), ((start + 0.52) + (0.06 * i))));
          hot = ((i === 0) && ((u < 0.6) || (b.t >= b.at("improve"))));
          chip(g, word, mix((1034 + (160 * i)), (394 + (402 * i)), u), mix(398, 267, u), GOLD, mix(126, 171, u), mix(68, 62, u), 1, hot);
        }
      }
    } finally { restore(); }
  }
}
export function question1(g, b) {
  let a, dim;
  a = b.fade("question", 0.48);
  dim = mix(1, 0.22, a);
  { const restore = layer(g, (dim * b.gone()), undefined, undefined, (1 + (0.028 * a)));
    try {
      mathform(g, "sft", 800, 327, 147, 1000, WHITE, b.ent(0.55, 0.14));

    } finally { restore(); }
  }
}
