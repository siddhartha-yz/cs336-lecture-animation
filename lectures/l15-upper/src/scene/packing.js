// Frame-driven artwork, drawn by the Remotion Canvas composition.
import {min,max,sum,len,range,zip,enumerate,round,getattr,any,all,at,slice,repeat,contains,fmt,printf,isclose,bisect_left,bisect_right} from '../values';
import {BLACK, WHITE, MUTED, DIM, RULE, INK, BLUE, GOLD, TEAL, GREEN, RED, PURPLE, YELLOW, PAPER, AXIS, CYAN, SKY, ORANGE, MAGENTA, PINK, ease, sine, between, pulse, solidBlock, sample, label, term, note, sampleLines, rule, bracket, slash, arc_arrow, highlight, chip, axis, question, ink_label, paperCutout, countdown, layeredBlock, lock, layer, aperture, phase_card, picture, mathform, form_segment, move_segment, blend, mix, clamp} from '../stage';
import {TOKENS as TOKS, GROUP, PACK_LENGTHS as SIZES, OFFSETS as ACC, SHOW_QUERY as DEMO_ROW, SHOW_KEY as DEMO_KEY, attention} from './examples';

// Movement comes from seven tokens, not a generic 2D mask wipe.
export const PC = [BLUE, GOLD, PINK];
export const [X0, W] = [225, 135];
export const TRAY_Y = [253, 418, 583];
export const [PACK_X, PACK_W, PACK_Y] = [260,180,330];
const CELL_W=116,CELL_H=94,PACK_CELL_W=156,PACK_CELL_H=106;
const START=X0-CELL_W*.5, END=X0+6*W+CELL_W*.5;
const STACK_TOP=TRAY_Y[0]-CELL_H*.5, STACK_BOTTOM=TRAY_Y[2]+CELL_H*.5;
export const PROMPTS = ["煮蛋", "去重", "改航班"];
export function pack_x(i) {
  return (PACK_X + (i * PACK_W));
}
export function padding(g, b) {
  let a, bx, c, content, frac, inspect, j, k, n, p, pad, q, right_x, x, y;
  a = b.ent(0.52, 0.03);
  content = b.fade("tokens", 0.78, undefined, 2);
  pad = b.fade("pad", 0.7, undefined, 6);
  inspect = b.fade("count", 0.72, undefined, 15);
  const overview=.44*b.ent(.47,.61);
  for (const item of enumerate(SIZES)) {
    [k, n] = item;
    y = at(TRAY_Y, k);
    c = at(PC, k);
    label(g, ("样本 " + at("ABC", k)), 90, (y - 15), 28, c, (a * Math.max(overview,content)));
    label(g, at(PROMPTS, k), 90, (y + 21), 22, MUTED, (a * Math.max(overview,content)));
    for (const item of range(7)) {
      j = item;
      bx = (X0 + (j * W));
      g.rect(bx-CELL_W/2,y-CELL_H/2,CELL_W,CELL_H, undefined, RULE, 1.25, undefined, a);
      if ((j < n)) {
        chip(g, at(TOKS, (at(ACC, k) + j)), bx,y,c,CELL_W,CELL_H, a*Math.max(overview,ease(content*1.5-.16*j)));
      } else {
        p = (a * ease(((pad * 1.5) - (0.085 * (j - n)))));
        g.rect(bx-CELL_W/2+1,y-CELL_H/2+1,CELL_W-2,CELL_H-2,BLUE,undefined,undefined,0,.16*p);
        for (const item of range(5)) {
          q = item;
          g.line(((bx - 36) + (q * 17)), (y + 30), ((bx - 15) + (q * 17)), (y - 30), BLUE,1.2,.20*p);
        }
        label(g, "PAD", bx, y, 22, WHITE, p, undefined, "mono");
      }
    }
  }
  if (inspect) {
    frac = ((b.t - b.at("count", 15)) / 2.22);
    if ((0 < frac && frac < 1)) {
      x = mix(START,END,frac);
      q = (a * (Math.sin((Math.PI * frac)) ** 0.43));
      for (const item of range(10, 0, (-1))) {
        j = item;
        g.rect((x - (j * 6)), STACK_TOP,((j * 6) + 1),STACK_BOTTOM-STACK_TOP, TEAL, undefined, undefined, undefined, (0.016 * q));
      }
      g.line(x,STACK_TOP-4,x,STACK_BOTTOM+4, TEAL, 2.15, q);
      label(g, String(1+Math.trunc(frac*7)), min(END,max(START,x)),173,26,TEAL,q,undefined,"math");
    }
  }
  right_x = 1282;
  bracket(g,START,END,177, DIM, a);
  label(g, "L = 7",(START+END)/2,137,33, MUTED, a);
  g.line(1110,209,1110,632, RULE, 1.3, a);
  label(g, "有效", right_x, 284, 25, MUTED, (a * inspect));
  label(g, "7 / 21", right_x, 380, 96, TEAL, (a * inspect), undefined, "math");
  label(g, "PAD = 14", right_x, 487, 27, MUTED, (a * inspect));
}
export function packed_pose(g, labels=1, red=1, h=1, alpha=1) {
  let a, c, i, k, name;
  for (const item of enumerate(TOKS)) {
    [i, name] = item;
    chip(g, name, pack_x(i), PACK_Y, at(PC, at(GROUP, i)),PACK_CELL_W,PACK_CELL_H,alpha, ((red > 0.6) && (contains([DEMO_ROW, DEMO_KEY], i))));
  }
  for (const item of range(3)) {
    k = item;
    [a, c] = [at(ACC, k), (at(ACC, (k + 1)) - 1)];
    bracket(g, (pack_x(a)-PACK_CELL_W/2), (pack_x(c)+PACK_CELL_W/2), 251, at(PC,k), (alpha * labels));
    label(g, at(PROMPTS, k), ((pack_x(a) + pack_x(c)) / 2), 211,31,at(PC,k), (alpha * labels));
  }
  if (red) {
    arc_arrow(g, [pack_x(DEMO_ROW),PACK_Y+PACK_CELL_H/2+5], [(pack_x(DEMO_ROW) - 30),555], [(pack_x(DEMO_KEY) + 20),555], [pack_x(DEMO_KEY),PACK_Y+PACK_CELL_H/2+5], RED, h, (alpha * red), 4.2);
  }
}
export function packing(g, b) {
  let a, bx, groups, i, j, k, leak, n, name, old, one_row, p, phrase, q, recognize, start, u, waste, word, y;
  start = b.fade("join", 1.26, undefined, 4);
  word = b.fade("pack", 0.56, undefined, 4);
  leak = b.fade("leak", 1.05, undefined, 20);
  phrase = b.fade("count", 0.64, undefined, 13);
  waste = b.fade("waste", 0.75, undefined, 12);
  groups = b.fade("three", 0.63, undefined, 24);
  recognize = b.at("recognize", 28);
  one_row = b.ent(0.47, recognize);
  if ((start < 0.999)) {
    { const restore = layer(g, (1 - start));
      try {
        bracket(g,START,END,177, DIM);
        label(g, "L = 7",(START+END)/2,137,33, MUTED);
        for (const item of enumerate(SIZES)) {
          [k, n] = item;
          y = at(TRAY_Y, k);
          label(g, ("样本 " + at("ABC", k)), 90, (y - 15), 28, at(PC, k));
          label(g, at(PROMPTS, k), 90, (y + 21), 22, MUTED);
          for (const item of range(7)) {
            j = item;
            bx = (X0 + (j * W));
            g.rect(bx-CELL_W/2,y-CELL_H/2,CELL_W,CELL_H, undefined, RULE, 1.25);
            if ((j >= n)) {
              g.rect(bx-CELL_W/2+1,y-CELL_H/2+1,CELL_W-2,CELL_H-2,BLUE,undefined,undefined,0,.16);
              for (const item of range(5)) {
                q = item;
                g.line(((bx - 36) + (q * 17)), (y + 30), ((bx - 15) + (q * 17)), (y - 30), BLUE,1.2,.20);
              }
              label(g, "PAD", bx, y, 22, WHITE, undefined, undefined, "mono");
            }
          }
        }
        g.line(1110,209,1110,632, RULE, 1.3);
        label(g, "有效", 1282, 284, 28, MUTED);
        label(g, "7 / 21", 1282, 380, 98, TEAL, undefined, undefined, "math");
        label(g, "PAD = 14", 1282, 487, 30, MUTED);
      } finally { restore(); }
    }
    for (const item of enumerate(TOKS)) {
      [i, name] = item;
      k = at(GROUP, i);
      j = (i - at(ACC, k));
      u = sine(start);
      chip(g, name, mix((X0 + (j * W)), pack_x(i), u), mix(at(TRAY_Y, k), PACK_Y, u), at(PC, k), mix(CELL_W,PACK_CELL_W,u),mix(CELL_H,PACK_CELL_H,u));
    }
  } else {
    if (leak) {
      packed_pose(g, 1, ease((leak * 2)), leak);
    } else {
      packed_pose(g, 1, 0, 0);
    }
    old = ((1 - b.ent(0.3, (b.at("three") - 0.48))) * (1 - leak));
    label(g, "Sequence Packing",800,500,35, TEAL, ((word * old) * (1 - waste)), undefined, "math");
    if (waste) {
      label(g, "7 / 21", 639, 620, 49, MUTED, (waste * old), undefined, "math");
      g.arrow(727, 620, 852, 620, TEAL, 2.5, (waste * old));
      label(g, "7 / 7", 956, 620, 61, TEAL, (waste * old), undefined, "math");
      note(g, "有效", 800, 693, ((max(0.54, phrase) * waste) * old));
    }
    if ((groups && (leak < 1))) {
      a = (groups * (1 - leak));
      for (const item of range(3)) {
        k = item;
        [p, q] = [at(ACC, k), (at(ACC, (k + 1)) - 1)];
        bracket(g, (pack_x(p)-PACK_CELL_W/2), (pack_x(q)+PACK_CELL_W/2), 422, at(PC,k), (a * (1 - one_row)), (-1));
      }
      if (one_row) {
        y = 433;
        bracket(g, (pack_x(0)-PACK_CELL_W/2), (pack_x(6)+PACK_CELL_W/2), y, GOLD, (a * one_row), (-1));
      }
    }
  }
}
export const [GX, GY, CELL] = [252, 212, 64];
export function grid_items(g, grid, mask, marked, highlight_i=(-1), paper=null) {
  let a, a0, c, e, fill, i, j, k, past, same, stroke, x, y;
  if ((grid <= 0)) {
    return;
  }
  for (const item of range(7)) {
    i = item;
    for (const item of range(7)) {
      j = item;
      c = at(PC, at(GROUP, i));
      same = (at(GROUP, i) === at(GROUP, j));
      past = (j <= i);
      [x, y] = [(GX + (j * CELL)), (GY + (i * CELL))];
      if(same&&past){
        const focused=highlight_i<0||GROUP[i]===highlight_i;
        solidBlock(g,x+1.8,y+1.8,CELL-3.6,CELL-3.6,c,grid*(focused?1:.19));
      }else{
        g.rect(x+1.8,y+1.8,CELL-3.6,CELL-3.6,null,AXIS,1.15,0,.50*grid);
        if(past&&mask<1)solidBlock(g,x+1.8,y+1.8,CELL-3.6,CELL-3.6,RED,grid*(1-mask));
      }
      if ((past && same)) {
        g.circle((x + (CELL / 2)), (y + (CELL / 2)), 2.9, BLACK, undefined, undefined, (grid * (.54+.46*marked)));
      } else {
        if ((mask > 0)) {
          label(g, "−∞", (x + (CELL / 2)), (y + (CELL / 2)), 18, WHITE, (grid * mask), undefined, "math");
        }
      }
      if (((i === DEMO_ROW) && ((j === DEMO_KEY) || (j === 3)))) {
        stroke = (((j === DEMO_KEY) && (mask < 0.95)) ? RED : ((j === 3) ? c : AXIS));
        g.rect((x + 1.3), (y + 1.3), (CELL - 2.6), (CELL - 2.6), undefined, stroke, 2, undefined, grid);
      }
    }
  }
  a0 = (grid * mask);
  for (const item of [3, 5]) {
    k = item;
    x = (GX + (k * CELL));
    y = (GY + (k * CELL));
    g.line(x, (GY - 2), x, (GY + (7 * CELL)), WHITE, 1.5, (a0 * 0.6));
    g.line((GX - 2), y, (GX + (7 * CELL)), y, WHITE, 1.5, (a0 * 0.6));
  }
  if ((highlight_i >= 0)) {
    [a, e] = [at(ACC, highlight_i), at(ACC, (highlight_i + 1))];
    c = at(PC, highlight_i);
    g.rect((GX + (a * CELL)), (GY + (a * CELL)), ((e - a) * CELL), ((e - a) * CELL), undefined, c, 3.3, undefined, grid);
  }
}
/** @param {import("../stage").Beat|null} b */
export function mask_frame(g, b=null, as_icon=false) {
  let a, bad, c, cod, code, code_clear, cross, fs, grid, hint, i, idx, k, masked, matrix, mv, name, open_old, p, paint_new, response, row_demo, sample, soft, span, text_fade, x, y, z;
  if (as_icon) {
    { const restore = layer(g, undefined, 320, (-20), 1.25, [484, 432]);
      try {
        grid_items(g, 1, 1, 1);
      } finally { restore(); }
    }
    return;
  }
  matrix = b.at("dims", b.at("matrix", 2));
  text_fade = (1 - sine(between(b.t, matrix, (matrix + 0.17))));
  mv = ease((((b.t - matrix) - 0.16) / 1.0));
  cross = b.at("cross", 12);
  masked = b.fade("cross", 0.65, undefined, 12);
  open_old = (1 - ease(((b.t - cross) / 0.19)));
  paint_new = ease((((b.t - cross) - 0.23) / 0.42));
  soft = b.fade("softmax", 0.72, undefined, 19);
  code = b.at("code", 29);
  cod = b.fade("code", 0.59, 0.17, 29);
  idx = (-1);
  if ((b.t >= b.at("loop", (b.d + 0.2)))) {
    fs = b.at("loop", (b.d + 0.2));
    span = max(2.2, ((b.speech + (max(0, (b.d - b.speech)) * 0.55)) - fs));
    idx = min(2, Math.trunc((((b.t - fs) / span) * 3)));
  }
  if ((b.t < matrix)) {
    packed_pose(g);
    hint = (b.fade("term", 0.59, undefined, 4) * (1 - b.ent(0.37, (matrix - 0.42))));
    for (const item of range(3)) {
      k = item;
      [a, z] = [at(ACC, k), (at(ACC, (k + 1)) - 1)];
      bracket(g, (pack_x(a)-PACK_CELL_W/2), (pack_x(z)+PACK_CELL_W/2), 200, at(PC, k), hint);
    }
    return;
  }
  { const restore = layer(g, (1 - mv));
    try {
      for (const item of range(3)) {
        k = item;
        [a, c] = [at(ACC, k), (at(ACC, (k + 1)) - 1)];
        bracket(g, (pack_x(a)-PACK_CELL_W/2), (pack_x(c)+PACK_CELL_W/2), 251, at(PC,k), text_fade);
        label(g, at(PROMPTS, k), ((pack_x(a) + pack_x(c)) / 2), 211,31,at(PC,k), text_fade);
      }
      arc_arrow(g, [pack_x(DEMO_ROW),PACK_Y+PACK_CELL_H/2+5], [(pack_x(DEMO_ROW) - 30),555], [(pack_x(DEMO_KEY) + 20),555], [pack_x(DEMO_KEY),PACK_Y+PACK_CELL_H/2+5], RED, 1, text_fade, 4.2);
    } finally { restore(); }
  }
  for (const item of enumerate(TOKS)) {
    [i, name] = item;
    chip(g, name, mix(pack_x(i), (GX + (CELL * (i + 0.5))), mv), mix(PACK_Y, (GY - 41), mv), at(PC, at(GROUP, i)), mix(PACK_CELL_W,55,mv),mix(PACK_CELL_H,48,mv), 1, ((mv < 0.3) && (contains([DEMO_ROW, DEMO_KEY], i))));
    chip(g, name, mix(pack_x(i), (GX - 45), mv), mix(PACK_Y, (GY + (CELL * (i + 0.5))), mv), at(PC, at(GROUP, i)), 53, 50, mv);
  }
  grid = between(mv, 0.16, 0.8);
  response = b.fade("calc", 0.53);
  code_clear = (1 - b.ent(0.28, (b.at("calc") - 0.44)));
  { const restore = layer(g, (1 - (0.23 * response)));
    try {
      grid_items(g, grid, masked, soft, ((response > 0.35) ? 1 : idx));
    } finally { restore(); }
  }
  row_demo = ((!response) ? (b.fade("self", 0.62) * (1 - b.fade("softmax", 0.48))) : 0);
  if (row_demo) {
    c = at(PC, 1);
    y = (GY + (DEMO_ROW * CELL));
    g.rect((GX + (3 * CELL)), y, (2 * CELL), CELL, undefined, c, 2.9, undefined, (row_demo * 0.88));
    p = ((b.fade("border", 0.56) * (1 - masked)) * row_demo);
    if (p) {
      g.rect(GX, y, (3 * CELL), CELL, undefined, RED, 2.65, undefined, p);
    }
  }
  if (response) {
    g.rect(GX, (GY + (DEMO_ROW * CELL)), (7 * CELL), CELL, undefined, GOLD, 2.5, undefined, (response * 0.9));
  }
  label(g, "键", (GX + (CELL * 3.5)), 119, 29, MUTED, grid);
  label(g, "查询", (GX - 46), 122, 23, MUTED, grid);
  label(g, "分块因果掩码", (GX + (CELL * 3.5)), 708, 27, MUTED, (grid * paint_new));
  x = 1130;
  a = (grid * (1 - ease(((b.t - code) / 0.2))));
  if (a) {
    if (masked) {
      label(g, "A₂ ← B₂", x, 316, 40, RED, (a * paint_new), undefined, "math");
    }
    if (soft) {
      mathform(g, "expzero", x, 473, 67, 390, GOLD, (a * soft));
      
    }
    if ((masked < 1)) {
      sample = b.fade("local", 0.64);
      bad = b.fade("border", 0.54);
      label(g, "A₂ ← B₂", x, 409, 47, RED, ((a * open_old) * bad), undefined, "math");
      label(g, "B₁、B₂ ← B₂", x, 309, 43, GOLD, ((a * open_old) * sample), undefined, "math");
    }
  }
  if (cod) {
    if (code_clear) {
      mask_code(g, (cod * code_clear), idx, b.fade("prefix", 0.58));
    }
    if (response) {
      prob_demo(g, b, response);
    }
  }
}
export function prob_demo(g, b, a) {
  let c, cx, ghost, h, i, lift, name, score, score_left, start, u, val, vals, visible, weight, x;
  visible = b.fade("visible", 0.55);
  score = b.fade("zeroes", 0.47);
  weight = b.fade("weight", 0.58);
  score_left = (1 - b.ent(0.21, (b.at("weight") - 0.27)));
  cx = 1117;
  vals = attention(DEMO_ROW);
  { const restore = layer(g, a);
    try {
      label(g, "B₂", cx, 241, 46, GOLD, 1, undefined, "math");
      for (const item of enumerate(zip(TOKS, vals))) {
        [i, [name, val]] = item;
        x = (847 + (i * 91));
        c = (val ? GOLD : WHITE);
        if (val) {
          start = [(GX + (CELL * (i + 0.5))), (GY + (CELL * (DEMO_ROW + 0.5)))];
          u = sine(between(b.t, (b.at("visible") + (0.09 * (i - 3))), ((b.at("visible") + 0.81) + (0.09 * (i - 3)))));
          lift = (Math.sin((Math.PI * u)) * 95);
          if (u) {
            ghost = Math.sin((Math.PI * u));
            g.line(at(start, 0), at(start, 1), mix(at(start, 0), x, u), (mix(at(start, 1), 604, u) - lift), c, 1.6, (0.56 * ghost));
            sample(g, name, mix(at(start, 0), x, u), (mix(at(start, 1), 604, u) - lift), 28, c, visible, undefined, "mono");
          }
        } else {
          sample(g, name, x, 604, 28, c, (visible * 0.75), undefined, "mono");
        }
        if ((score && score_left)) {
          label(g, (val ? "0" : "−∞"), x, 459, 36, c, (score * score_left), undefined, "math");
        }
        h = (((146 * weight) * val) / 0.5);
        if (h) {
          solidBlock(g,x-34,564-h,68,h,c);
        }
        label(g, `${fmt(val, `.1f`)}`, x, ((550 - h) - 8), 32, c, weight, undefined, "math");
      }
      rule(g, 820, 564, 1425, DIM, visible);
      label(g, "e⁰ / (e⁰ + e⁰) = 0.5", cx, 679, 39, WHITE, weight, undefined, "math");
    } finally { restore(); }
  }
}
export function mask_code(g, a, i, prefix) {
  let code, h, head, k, line, offset, w, x, y;
  [x, y, w, h] = [750, 166, 759, 459];
  { const restore = layer(g, a, ((1 - a) * 65), ((1 - a) * 21), undefined, [(x + (w / 2)), (y + (h / 2))], (1.35 * (1 - (0.75 * a))));
    try {
      paperCutout(g, x, y, w, h);
      label(g, "PyTorch", (x + 32), (y + 65), 30, INK, undefined, "left", "math");
      rule(g, (x + 32), (y + 91), ((x + w) - 34), AXIS);
      head = "cu_seqlens = [0, 3, 5, 7]; L = 7";
      g.rect((x + 27), (y + 107), (g.measure(head, 30, "mono") + 12), 39, SKY, undefined, undefined, undefined, (prefix * (i < 0)));
      sample(g, head, (x + 32), (y + 126), 30, BLACK, undefined, "left", "mono");
      code = ["keep = torch.zeros(L, L).bool()", "for i in range(len(cu_seqlens) - 1):", "    s, e = cu_seqlens[i:i + 2]", "    low = torch.ones(e-s, e-s).tril()", "    keep[s:e, s:e] = low.bool()"];
      if ((i >= 0)) {
        g.rect((x + 78), (y + 309), (w - 115), 37, GOLD);
      }
      for (const item of enumerate(code)) {
        [k, line] = item;
        offset = ((len(line) - len(line.trimStart())) * 16.9);
        sample(g, line.trimStart(), ((x + 31) + offset), ((y + 174) + (k * 38)), 28, INK, undefined, "left", "mono");
      }
      if ((i >= 0)) {
        label(g, `i = ${i}   →   [${at(ACC, i)}, ${at(ACC, (i + 1))})`, (x + 32), (y + 385), 30, BLACK, undefined, "left", "mono");
      }
      
    } finally { restore(); }
  }
}
