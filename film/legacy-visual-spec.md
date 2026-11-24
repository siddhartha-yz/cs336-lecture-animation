Rendering logical 1600 × 900. No on-screen chapter headings, corner bugs, progress bars, or page labels; chapter markers are carried only in MP4 player metadata. Captions below y=790. Keep science content mainly within x=94..1506 and y=125..747. Use a flat pure-black background (#000000), no colored or gradient atmosphere. Shared foreground palette uses official ManimGL BLUE_C #58C4DD, PURPLE_B #B189C6, YELLOW_D #F4D345, GREEN_C #83C167, RED_C #FC6255. Use gold = task / decisive evidence; cyan and lavender always denote the two models (or their descendants); green and coral denote passed/failed or confirmed problem. A/C labels, axis annotations, numbers, short meaningful phrases only. Use negative space, no luminous UI card walls.

In your work/act*.py, `from visual import *` and define draw(g, i, t, duration). Global exported constants BG INK MUTED GRID BLUE PURPLE GOLD GREEN RED, aliases A=BLUE B=PURPLE W=INK. Colors are hex strings. Exported functions clamp(x,lo=0,hi=1), mix(a,b,t), ease(t) (smoothstep), step(u,a,b) (smooth ease between); blend(color1,color2,t) -> hex.
g.c = scaled raw cairo.Context. All drawing operations are in logical pixels:
- g.text(s,x,y,size=36,color=INK,alpha=1,align='center',font='sans',weight='normal') x is anchor, y is CENTER vertically. align 'left'/'center'/'right'. font 'sans' (Noto Sans CJK SC), 'serif' (Linux Libertine + Chinese Noto Serif fallback), 'math' (DejaVu Serif), or family name; weight 'bold'/'medium'/'normal'/'light'. Supports mixed Chinese/math; formulas can use segment layout.
- g.line(x1,y1,x2,y2,color=INK,width=2,alpha=1,dash=None).
- g.poly(points,color=INK,width=2,alpha=1,close=False,fill=None,fill_alpha=1).
- g.rect(x,y,w,h,fill=None,stroke=None,width=2,r=0,alpha=1) (top left).
- g.circle(x,y,r,fill=None,stroke=None,width=2,alpha=1).
- g.arrow(x1,y1,x2,y2,color=MUTED,width=2,alpha=1,head=11).
- g.arc(x,y,r,a,b,color=INK,width=2,alpha=1), radians clockwise.
- g.check(x,y,ok=True,r=15,alpha=1) geometric ✓/×.
- g.disk(x,y,color,r=53,label='',alpha=1); restrained luminous outline with model color.
- g.tile(x,y,w=68,h=62,label='',color=GOLD,alpha=1,selected=False) centered. 
- g.anchor(alpha=1, scale=1, y=420) model disks x=530,1070 and empty gold task tile x=800; central act bridge applies cropped fades. Ideally use at start/end act or animate your local equivalents.
- g.measure(s,size=36,font='sans',weight='normal') -> logical width.
- g.source(color,alpha=1) sets cairo source. Access raw context for curves/clipping.
Mix native visual continuity on beat boundaries. Narration and captions are added by me, no subtitles in your scene. draw receives full duration speech+hold; use last 1.5–2 sec to settle where appropriate. First/last beat is normal content, please do not insert empty standalone title card. Can use python3 work/preview.py act_index beat_index fraction out.png once available, work/actN.py filename (act_index 1..4, beat_index 0-based).
