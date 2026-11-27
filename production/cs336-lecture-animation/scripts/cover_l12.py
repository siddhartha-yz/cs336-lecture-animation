#!/usr/bin/env python3
"""A cover drawn with v6.2's original 31:15 camera and vector geometry."""
from pathlib import Path
import json,sys,math
from unittest.mock import patch
FILM=Path(sys.argv[1]).resolve(strict=True)/"film/film_zh_v6"
sys.path.insert(0,str(FILM))
from rig4 import cairo,cue,prev,phase
from visual import Pango,PangoCairo,rgb
from studio_tests import AR,PAL
import v4_act0 as final_shot

WHITE='#FFFFFF'
CYAN='#58C4DD'
GOLD='#FFD76A'
TITLE=('大模型','怎么评？')

# The 7×7 ARC-AGI training board from the film, cropped to its central 5×5.
TILES=tuple(tuple(row[1:6]) for row in AR['train'][1]['input'][1:6])
assert len(TILES)==5 and all(len(r)==5 for r in TILES)

DATA=json.loads((FILM/'assets/cost-points.json').read_text())
FR=[]
for m in sorted(DATA,key=lambda m:m['cost']):
    if not FR or m['index']>FR[-1]['index']:
        FR.append(m)

def paint(c,color):
    c.set_source_rgb(*rgb(color))

def glyphs(c,s,cx,cy,size,color,weight,tracking=0,family='Noto Serif CJK SC'):
    layout=PangoCairo.create_layout(c)
    context=layout.get_context()
    context.set_language(Pango.Language.from_string('zh-cn'))
    context.set_round_glyph_positions(False)
    font=Pango.FontDescription(family)
    font.set_weight(weight); font.set_absolute_size(size*Pango.SCALE)
    layout.set_font_description(font)
    layout.set_text(s,-1)
    if tracking:
        attrs=Pango.AttrList()
        attrs.insert(Pango.attr_letter_spacing_new(round(tracking*Pango.SCALE)))
        layout.set_attributes(attrs)
    assert layout.get_unknown_glyphs_count()==0,(s,family)
    ink,_=layout.get_extents()
    b=(ink.x,ink.y,ink.width,ink.height);x,y,w,h=(v/Pango.SCALE for v in b)
    c.new_path();c.move_to(cx-x-w/2,cy-y-h/2)
    PangoCairo.layout_path(c,layout);paint(c,color);c.fill()
    return (cx-w/2,cy-h/2,cx+w/2,cy+h/2)

def hero(g,x,y,zoom,inklift):
    shot=cue('8-2')
    frame=31*60*60+15*60
    time=(frame-round(shot.s['t0']*60))/60
    assert phase(time,shot.at('多量几个方向')-.08,shot.at('多量几个方向')+1.31)==1.
    c=g.c
    pigment=g.source
    text=g.text
    # Keep the double solid and the six web directions. The labels are spoken
    # identifiers in the film; the cover's only type lives in the left column.
    g.text=lambda *_,**__:None
    g.source=lambda col,a=1: pigment(col,1.-(1.-max(0.,min(1.,a)))**inklift)
    c.save()
    c.translate(x,y);c.scale(zoom,zoom);c.translate(-800,-418)
    solid=final_shot.solid
    def cover_solid(world,dims,color,mel=0,al=1):
        # Make each body hold its edge at thumbnail size, retaining the
        # transparent overlaps that let the second body read through the first.
        solid(world,dims,color,mel,min(1,al*(1.45 if color==CYAN else 1.09)))
    try:
        with patch.object(final_shot,'solid',cover_solid):
            final_shot.closing(g,shot,time=time)
    finally:c.restore();g.source=pigment;g.text=text

def arc_tiles(c,cx,cy,size):
    step=size/5.;gap=3.6;x=cx-size*.5;y=cy-size*.5
    for i,row in enumerate(TILES):
        for j,col in enumerate(row):
            paint(c,PAL[col]);c.rectangle(x+j*step+gap/2,y+i*step+gap/2,step-gap,step-gap);c.fill()

def stair(c,x,y,width,height):
    # In this miniature, equal spacing shows the order of configurations;
    # the vertical jumps use the actual six frontier scores.
    lo,hi=FR[0]['index'],FR[-1]['index']
    pts=[(x+i*width/(len(FR)-.38),y-height*(m['index']-lo)/(hi-lo)) for i,m in enumerate(FR)]
    c.save();c.set_line_join(cairo.LINE_JOIN_MITER);c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.new_path();c.move_to(*pts[0])
    for (x0,y0),(x1,y1) in zip(pts,pts[1:]):
        c.line_to(x1,y0);c.line_to(x1,y1)
    c.line_to(x+width,pts[-1][1])
    paint(c,GOLD);c.set_line_width(4.8);c.stroke()
    for i,(a,b) in enumerate(pts):
        if i not in (0,1,3,5):continue
        c.new_sub_path();c.arc(a,b,4.5 if i==5 else 3.2,0,math.tau);c.fill()
    c.restore()

def draw(out,family='Noto Serif CJK SC'):
    width=1920
    surface,g=prev.surface(width);c=g.c
    c.identity_matrix();c.scale(width/1920,width/1920)
    c.set_font_options(cairo.FontOptions(antialias=cairo.ANTIALIAS_GRAY,hint_style=cairo.HINT_STYLE_NONE,hint_metrics=cairo.HINT_METRICS_OFF))
    paint(c,'#000000');c.paint()
    hero(g,1251,519,1.385,1.23)
    arc_tiles(c,1665,154,114)
    stair(c,1563,920,220,117)
    tx=333;tys=(462,575);sizes=(103,99)
    spans=[glyphs(c,part,tx,y,size,WHITE,Pango.Weight.NORMAL,3.,family) for part,y,size in zip(TITLE,tys,sizes)]
    assert all(48<x0<x1<575 and 90<y0<y1<1000 for x0,y0,x1,y1 in spans),spans
    surface.write_to_png(str(out));print([(round(x0),round(y0),round(x1),round(y1)) for x0,y0,x1,y1 in spans])

if __name__=='__main__':
    dest=Path(sys.argv[2])
    dest.parent.mkdir(parents=True,exist_ok=True)
    draw(dest)
