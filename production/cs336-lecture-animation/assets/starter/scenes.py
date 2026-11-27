"""Editable example: shifting every logit by the same amount leaves softmax fixed."""
import math
from visual import BLUE, GOLD, blend, clamp, step, smooth_tail

LOGITS = (1.4, 0.7, -0.3)
COLORS = (BLUE, "#5CD0B3", "#C58AF9")
weights = tuple(math.exp(x) for x in LOGITS)
PROBS = tuple(x / sum(weights) for x in weights)

def draw(g, scene, frame, fps):
    key = scene["id"]
    cue = scene["cues"]
    if key == "read":
        before = [smooth_tail((frame - cue["logits"] - 10*i) / 45) for i in range(3)]
        after = [smooth_tail((frame - cue["distribution"] - 12*i) / 50) for i in range(3)]
        delta, proof = 0.0, 0.0
    elif key == "shift":
        before = after = [1.0] * 3
        shift = cue["shift"]
        delta = 2.0 * step(frame, shift, shift + 1.45 * fps)
        proof = step(frame, cue["same"], cue["same"] + .65*fps)
    else:
        raise ValueError(f"在 scenes.py 为 {key} 添加实际画面")

    # The same coordinate systems survive the cut. No full-screen title.
    left, right, y = 215, 902, 600
    g.text("logits", 400, 162, 46, "#ECECEC")
    g.text("softmax", 1101, 162, 46, "#ECECEC")
    for x in (left, right):
        g.line(x, y, x+396, y, "#8B8B8B", 2)
    for i, (z, p, color) in enumerate(zip(LOGITS, PROBS, COLORS)):
        xa, xb = left+83+i*115, right+83+i*115
        za, pa = before[i], after[i]
        value = z + delta
        ya, yb = y-95*value*za, y-465*p*pa
        if za > .001:
            g.rect(xa-35, min(y,ya), 70, abs(y-ya),
                   fill=blend("#000000",color,.62), stroke=color, width=2.5, alpha=za)
            g.text(f"{value:+.1f}",xa,ya+(-25 if value>=0 else 28),31,color,za)
        if pa > .001:
            g.rect(xb-35, yb, 70, y-yb, fill=blend("#000000",color,.62),
                   stroke=color, width=2.5, alpha=pa)
            g.text(f"{100*p:.1f}%",xb,yb-27,32,color,pa)
        g.text("abc"[i],xb,y+48,33,color)

    link = after[0]
    g.arrow(668,438,832,438,GOLD,2.5,link)
    if delta > .02:
        g.text(f"+{delta:.1f}",676,527,40,GOLD,clamp(delta*2))
    if proof:
        # Match the unchanged columns before the colour accent leaves.
        g.line(902,687,1298,687,GOLD,3.5,proof)
        g.text("概率不变",1100,739,35,GOLD,proof)
