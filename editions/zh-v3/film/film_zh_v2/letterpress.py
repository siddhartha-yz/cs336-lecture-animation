"""Letters belong in their own lower reading lane; chapter-local ASS is fed from the exact caption clock."""
from pathlib import Path
from edition import captions
def timing(t):
 cs=max(0,round(100*t));h,x=divmod(cs,360000);m,x=divmod(x,6000);s,f=divmod(x,100);return f'{h}:{m:02}:{s:02}.{f:02}'
def ass(rows,path):
 lines=['[Script Info]','ScriptType: v4.00+','PlayResX: 1920','PlayResY: 1080','ScaledBorderAndShadow: yes','WrapStyle: 2','','[V4+ Styles]','Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding','Style: Chinese,Noto Serif CJK SC,54,&H00EEEEEE,&H00EEEEEE,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,1.1,0,2,105,105,76,1','','[Events]','Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text']
 for a,b,txt in rows:lines.append(f'Dialogue: 0,{timing(a)},{timing(b)},Chinese,,0,0,0,,'+txt.replace('{','｛').replace('}','｝').replace('\n',r'\N'))
 path=Path(path);path.write_text('\n'.join(lines)+'\n',encoding='utf-8')
