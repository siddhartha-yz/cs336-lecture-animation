// Frame-driven artwork, drawn by the Remotion Canvas composition.
import {min,max,sum,len,range,zip,enumerate,round,getattr,any,all,at,slice,repeat,contains,fmt,printf,isclose,bisect_left,bisect_right} from '../values';
import {BLACK, WHITE, MUTED, DIM, RULE, INK, BLUE, GOLD, TEAL, GREEN, RED, PURPLE, YELLOW, PAPER, AXIS, CYAN, SKY, ORANGE, MAGENTA, PINK, ease, sine, between, pulse, solidBlock, sample, label, term, note, sampleLines, rule, bracket, slash, arc_arrow, highlight, chip, axis, question, ink_label, paperCutout, countdown, layeredBlock, lock, layer, aperture, phase_card, picture, mathform, form_segment, move_segment, blend, mix, clamp} from '../stage';
import {mask_frame} from './packing';
import {SORTED, TARGET, FIRST_GE, bisect_steps} from './examples';

// Code quality comes from an observable test, then the SFT snapshot becomes an anchor.
export const WRONG = bisect_right(SORTED, TARGET);
export const RIGHT = bisect_left(SORTED, TARGET);
if (!((WRONG !== FIRST_GE) && (RIGHT === FIRST_GE))) throw new Error("WRONG != FIRST_GE and RIGHT == FIRST_GE");
export const [TR_RIGHT] = bisect_steps(SORTED, TARGET, true);
export const [TR_LEFT] = bisect_steps(SORTED, TARGET);
export function test_input(g, a=1) {
  let i, v, x;
  label(g, "target",345,287,29,WHITE,a);
  chip(g, String(TARGET), 345, 348, GOLD, 89, 59, a, true);
  for (const item of enumerate(SORTED)) {
    [i, v] = item;
    x = (580 + (i * 121));
    label(g, String(i), x, 276, 24, WHITE, a, undefined, "math");
    chip(g, String(v), x, 348, BLUE, 104, 72, a, (v === TARGET));
  }
}
export function source_example(g, b) {
  const code=[
    ["async function f() {"],
    ["  return ","await"," Promise.resolve('A');"],
    ["}"],
    ["f()",".then","(a => console.log(a, 'B'));"],
  ];
  const details=["await + .then()","node -e …","A B","A → B"];
  const cues=[b.at("nemotron"),b.at("tool_call"),b.at("trace"),b.at("trace")+.59];
  const dock=sine(between(b.t,cues[0]-.20,cues[0]+.96));
  const erase=1-sine(between(b.t,b.at("tests")-.68,b.at("tests")-.40));
  const test=b.fade("tests",.60);
  const stage=layer(g,b.gone());
  try{
    if(erase){
      // Keep this exact program on screen as the trace opens above it. No
      // preview of the later Python bug while the voice is on JavaScript.
      const trace=layer(g,erase);
      try{
        const move=layer(g,1,106*(1-dock),-162*(1-dock),mix(1.33,1,dock),[600,565]);
        try{
          const bright=b.fade("code",.55);
          for(const [i,parts] of code.entries()){
            const hue=blend(WHITE,i===1?SKY:GOLD,.55+.45*bright);
            g.rawRun(parts.map((part,j)=>[part,j===1?hue:WHITE]),236,488+48*i,37);
          }
        }finally{move();}
        const trailY=414-60*b.fade("sandbox",.57);
        const items=[["输入", BLUE], ["调用", GOLD], ["返回", PURPLE], ["续写", TEAL]];
        for(const [i,[name,hue]] of items.entries()){
          const x=293+338*i,a=b.ent(.58,cues[i]);
          if(!a)continue;
          label(g,name,x,trailY-54,25,hue,a);
          const traceSize=35;
          sample(g,details[i],x,trailY+8,traceSize,hue,a,"center","mono");
          if(i<3){
            const u=b.ent(.50,cues[i+1]-.08);
            const left=x+g.measure(details[i],traceSize,"mono")/2+18;
            const right=x+338-g.measure(details[i+1],traceSize,"mono")/2-18;
            g.arrow(left,trailY+7,mix(left,right,u),trailY+7,AXIS,2.2,u,11);
          }
        }
        note(g,"NVIDIA · Nemotron-SFT-OpenCode-v1",1410,697,b.fade("nemotron",.72),WHITE,"right");
      }finally{trace();}
    }
    if(test)test_input(g,test);
  }finally{stage();}
}
export function test_code(g, b) {
  let a, c, des, expect, fail, first, h, h0, hi, i, j, l, l0, lo, m, m0, middle, old, passed, path, redo, retry, stat, u, v, when, x, x0, x1;
  first = b.fade("first", 0.5);
  fail = b.fade("fail", 0.55);
  expect = b.fade("expected", 0.44);
  retry = b.at("fix");
  redo = b.ent(0.54, (retry + 0.46));
  old = (1 - b.ent(0.3, (retry - 0.03)));
  passed = b.fade("pass", 0.53);
  stat = b.fade("passat", 0.55);
  when = b.fade("not", 0.5);
  des = b.fade("problem", 0.52);
  { const restore = layer(g, b.gone());
    try {
      test_input(g, max(0.66, des));
      label(g, "min { i : aᵢ ≥ 3 }",1020,216,43,BLUE,des,undefined,"math");
      for (const item of range(len(SORTED))) {
        i = item;
        x = (580 + (i * 121));
        if ((i === WRONG)) {
          g.arrow(x, 429, x, 396, RED, 2.7, (fail * old), 10);
        }
        if ((i === RIGHT)) {
          g.arrow(x, 429, x, 396, TEAL, 2.7, max((expect * old), passed), 10);
        }
      }
      for (const item of [[TR_RIGHT, (b.at("first") + 0.67), (b.at("fail") - 0.12), RED], [TR_LEFT, (retry + 2.18), (b.at("pass") - 0.09), TEAL]]) {
        [path, lo, hi, c] = item;
        if ((!(lo < b.t && b.t < hi))) {
          continue;
        }
        v = (between(b.t, lo, hi) * len(path));
        j = min((len(path) - 1), Math.trunc(v));
        u = sine(between((v - j), 0, 0.48));
        [l, m, h] = at(path, j);
        [l0, m0, h0] = at(path, max(0, (j - 1)));
        a = (sine(between(b.t, lo, (lo + 0.25))) * (1 - sine(between(b.t, (hi - 0.18), hi))));
        x0 = ((580 + (121 * mix(l0, l, u))) - 52);
        x1 = ((580 + (121 * (mix(h0, h, u) - 1))) + 52);
        bracket(g, x0, x1, 308, c, a, (-1));
        middle = (580 + (121 * mix(m0, m, u)));
        g.rect((middle - 48), 317, 96, 62, undefined, c, 3.05, undefined, a);
        g.circle(middle, 406, 4.5, c, undefined, undefined, a);
      }
      rule(g, 286, 458, 1314, RULE, first);
      label(g, "bisect_right(nums, target)", 261, 518, 41, WHITE, (first * old), "left", "mono");
      label(g, `${WRONG}  ≠  ${RIGHT}`, 1160, 521, 59, RED, (fail * old), undefined, "math");
      label(g, "FAIL", 1399, 521, 44, RED, (expect * old), undefined, "math");
      label(g, "bisect_left(nums, target)", 261, 518, 41, TEAL, redo, "left", "mono");
      label(g, `${RIGHT}  =  ${FIRST_GE}`, 1160, 521, 59, TEAL, passed, undefined, "math");
      label(g, "PASS", 1399, 521, 43, TEAL, passed, undefined, "math");
      if (stat) {
        label(g, "Pass@1", 800, 635, 44, GOLD, stat, undefined, "math");
        label(g, "first attempt", 657, 696, 28, WHITE,stat,undefined,"math");
        g.check(825,696,false,14,when);
      }
    } finally { restore(); }
  }
}
export function referenceMark(g,x,y,scale=1,a=1,show=true){
  const restore=layer(g,a,0,0,scale,[x,y]);
  try{
    layeredBlock(g,x-102,y-55,204,110,14,BLUE);
    lock(g,x,y,WHITE,1,1.22);
    if(show)mathform(g,"reff",x,y+103,53,169,SKY);
  }finally{restore();}
}
export function frozen(g,b){
  const m=b.fade("marin",.64),size=b.fade("size",.55),sft=b.fade("sft",.6);
  const ckpt=b.fade("ckpt",.72),ref=b.fade("ref",.74),shift=b.fade("transition",.62);
  const restore=layer(g,b.gone());
  try{
    // Begin with a single checkpoint at screen scale; move the same
    // object left to make room only when the instruction version is due.
    const travel=sine(between(b.t,b.at("sft")-1.02,b.at("sft")-.04));
    const enter=b.ent(.60,.21),body=layer(g,enter,467*(1-travel),0,mix(2.28,1,travel),[333,421]);
    try{
      label(g,"Marin 8B",333,mix(305,246,travel),42,SKY,m,undefined,"math");
      note(g,"deeper-starling-05-15",333,mix(531,585,travel),m);
      layeredBlock(g,185,337,296,168,16,BLUE,"Base",size>.7?"80 亿参数":"");
      if(travel<1){
        for(const y of [356,368,484])g.line(203,y,463,y,SKY,1.0,.28*(1-travel));
      }
    }finally{body();}
    if(travel>.9&&shift&&sft<1){
      const ghost=shift*(1-sft)*sine(between(travel,.9,1));
      g.line(509,421,628,421,AXIS,2,ghost,[6,7]);
      g.rect(660,337,294,168,null,GOLD,1.8,0,ghost*.62);
    }
    g.arrow(510,421,632,421,GOLD,3,sft,13);
    layeredBlock(g,660,337,294,168,16,GOLD,"SFT","指令版",sft);
    g.arrow(982,421,1101,421,BLUE,2.8,ckpt,12);
    layeredBlock(g,1128,360,224,122,15,BLUE,"","",ckpt*(1-ref));
    referenceMark(g,1240,421,1.1,ref,false);
    if(ref)mathform(g,"reff",1240,570,51,184,SKY,ref);
    label(g,"冻结",1240,632,32,SKY,ref);
  }finally{restore();}
}
export function question2(g, b) {
  let c, i, masks, one, p, pass_alpha, prior, two, w, x;
  p = b.fade("question", 0.53);
  one = b.fade("one", 0.56);
  two = b.fade("two", 0.56);
  prior = b.at("prior");
  pass_alpha = (one * (1 - b.ent(0.35, (prior - 0.26))));
  masks = b.ent(0.68, (prior + 0.13));
  { const restore = layer(g, (mix(1, 0.22, p) * b.gone()), undefined, undefined, (1 + (0.025 * p)));
    try {
      if (pass_alpha) {
        label(g, "bisect_left(…, 3)", 473, 325, 42, WHITE, pass_alpha, undefined, "mono");
        rule(g, 310, 377, 651, TEAL, (pass_alpha * 0.78), 2.0);
        label(g, "1 = 1", 442, 435, 47, TEAL, pass_alpha, undefined, "math");
        g.check(581, 435, true, 21, pass_alpha);
      }
      if (two) {
        { const restore = layer(g, two, 340, (-39), 0.46, [800, 414]);
          try {
            mask_frame(g, undefined, true);
          } finally { restore(); }
        }
      }
      if (masks) {
        { const restore = layer(g, masks);
          try {
            label(g, "损失掩码", 466, 226, 36, TEAL);
            label(g, "注意力掩码", 1140, 226, 36, BLUE);
            g.line(798, 263, 798, 661, RULE, 1.45);
            for (const item of enumerate(["用户", "煮", "蛋", "沸水", "冰水"])) {
              [i, w] = item;
              x = (272 + (95 * i));
              c = ((i < 3) ? BLUE : GOLD);
              chip(g, w, x, 370, c, 84, 66);
              label(g, ((i < 3) ? "0" : "1"), x, 468, 43, ((i < 3) ? WHITE : TEAL), undefined, undefined, "math", "bold");
            }
            bracket(g, 511, 698, 530, TEAL, undefined, (-1));
            note(g, "计入损失", 600, 559, 1, TEAL);
            note(g, "样本边界", 1140, 586, 1, BLUE);
          } finally { restore(); }
        }
      }
    } finally { restore(); }
  }
}
