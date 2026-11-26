"""Conform text and chapters to the finished narration, including time reserved for the audience."""
from pathlib import Path
import json,re
W=Path(__file__).resolve().parent
DEST=W/'edition'
STEM='CS336-L12-能力的影子-v6.2'
CH=(('0-1','序 · 分数涨了，模型却退步'),('door1','一 · 价值的尺子与归因边界'),('door2','二 · 困惑度的理想与盲区'),('door3','三 · 考卷饱和与去饱和'),('door4','四 · 盲测天梯与裁判去偏'),('door5','五 · 走出聊天框：代码沙箱与脚手架'),('inter','六 · 纯粹推理与安全底线'),('door6','七 · 生态效度与数据污染'),('8-1','尾声 · 再看八十二分的影子'))
def book():return json.loads((W/'book/scenes.json').read_text())
def mm(t,places=0):
 t=round(t,places);m,s=divmod(t,60)
 return f'{int(m):02}:{int(s):02}' if not places else f'{int(m):02}:{s:0{3+places}.{places}f}'
def stamp(t):
 n=round(t*1000);h,n=divmod(n,3600000);m,n=divmod(n,60000);s,n=divmod(n,1000);return f'{h:02}:{m:02}:{s:02},{n:03}'
def chapters():
 s=book();ts={r['id']:r['t0']for r in s};end=s[-1]['t0']+s[-1]['duration']
 return [(ts[k],ts[CH[i+1][0]] if i+1<len(CH) else end,name)for i,(k,name)in enumerate(CH)]
def quip():
 x=json.loads((W/'audio/cuebook.json').read_text())
 titles=list(dict.fromkeys(r['title']for r in x['passages']))
 return ' / '.join(titles)+' — Blue Dot Sessions. Creative Commons Attribution-NonCommercial 4.0. Edited excerpts and mix. https://www.sessions.blue/licensing/'
def make():
 from shoot4 import caprows,cue,norm
 DEST.mkdir(exist_ok=True)
 scenes=book();cap=[];ms=chapters();ch=dict(CH);lines=['# 能力的影子',f'**Stanford CS336 第十二讲 · 模型评估指标与基准测试评测** 　中文长剪｜{mm(ms[-1][1],1)}','', '画面和口播共用下列时码。圆括号内的静默段留给观众，旁白不念。','']
 for a,b,n in ms:lines.append(f'- **{mm(a)}**　{n}')
 lines.append('');anchors=[]
 for r in scenes:
  k=r['id'];c=cue(k);d=c.s;a,b=r['t0'],r['t0']+r['duration']
  if k in ch:lines+=['',f'## {mm(a)}　{ch[k]}','']
  if k=='opening':lines+=[f'*{mm(a,1)}–{mm(b,1)}　片头：五个仪器围绕片名浮现。*',''];continue
  if not r['groups']:continue
  lines+=['',f"### {mm(a,1) if a%1 else mm(a)}　{r['title']}",'']
  for take in d['groups_meta']:
   lines.extend([take['text'],''])
   for pause in d['rests']:
    if pause['take']==take['id'] and pause['end']-pause['start']>=1.8:
     lines.extend([f"*（{mm(a+pause['start'],1)}–{mm(a+pause['end'],1)}　{pause['name']}）*",''])
  rows=caprows(d)
  assert norm(''.join(p[2] for p in rows))==norm(d['text']),k
  for x,y,text in rows:
   row=(round((a+x)*1000),round((a+y)*1000),text,k)
   assert row[0]<row[1] and (not cap or row[0]>=cap[-1][1]),(row,cap[-1]if cap else None)
   cap.append(row)
  anchors.extend(dict(kind='pause',scene=k,name=v['name'],start=a+v['start'],end=a+v['end'])for v in d['rests'])
  anchors.extend(dict(kind='question',scene=k,time=a+v['time'])for v in d['questions'])
 (DEST/(STEM+'-逐字稿与章节.md')).write_text('\n'.join(lines).rstrip()+'\n')
 (DEST/(STEM+'.srt')).write_text('\n\n'.join(f'{i}\n{stamp(x/1000)} --> {stamp(y/1000)}\n{ss}'for i,(x,y,ss,k)in enumerate(cap,1))+'\n')
 mm0=';FFMETADATA1\ntitle=能力的影子 · Stanford CS336 第十二讲\nartist=CS336 模型评测中文动画\ncomment='+quip()+'\n'
 for a,b,n in ms:mm0+=f'[CHAPTER]\nTIMEBASE=1/1000\nSTART={round(a*1000)}\nEND={round(b*1000)}\ntitle={n}\n'
 (DEST/'chapters.ffmeta').write_text(mm0);(DEST/'performance.json').write_text(json.dumps(anchors,ensure_ascii=False,indent=1))
 print(f"{len(cap)} subtitles · {len(ms)} chapters · {len(scenes)} cuts · {ms[-1][1]:g}s")
if __name__=='__main__':make()
