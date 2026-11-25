"""One clock: embedded chapters, complete Mandarin SRT and readable transcript."""
from pathlib import Path
import json,re,sys
from timeline3 import W,OLD,S,starts,TOTAL,IDS,CH,mm
from music_layout import MUSIC_CREDIT
sys.path.insert(0,str(OLD))
from edition import captions,stamp,clean,width,secs
from chapters_zh import TITLE
O=W/'edition';O.mkdir(exist_ok=True)
BASE='CS336-L12-模型评测-全片中文-v3'
chap={s['beat']:starts[k]for k,s in S.items()if k.endswith('-1')}
picture_credits='Regina’s Tombstone — Abigail Baker and Alison Cooley, CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/)，裁切与局部放大。原故事对战取自 Arena Human Preference 140k，节译与重绘，CC BY 4.0。'
credits=f'旁白：Drama 3 · 用户提供参考音色。配乐：{MUSIC_CREDIT}，节选、交叉淡变、采样移调与混音；CC BY-NC 4.0 (https://creativecommons.org/licenses/by-nc/4.0/)。'+picture_credits
titles={'0-1':'分数涨了，新题反而错得更多','0-2':'两个盒子，同一个影子','1-1':'加上每题预算','1-2':'一张选票与一次调用','1-3':'方法实验与黑盒系统','1-4':'同一条训练流，谁先过线','2-1':'从真实词元到等效候选数','2-2':'按词元，还是按字节','2-3':'决定答案的那一步','2-4':'把领域拆开，重新验算','3-3':'GPQA：一道题过两道关','3-4':'HLE：从投稿到公开题','4-1':'留住这张选票','4-2':'从分差读胜率','4-4':'把回归中的长度差设为零','5-2':'修复一个缺陷，保住原有功能','5-3':'十种配对与工具脚手架','6-4':'同一道题，两次压力测试','7-2':'把四道题排二十四次','7-4':'删整篇与遮一段','7-5':'用训练截止日划出新题','8-1':'让七件测量工具排成一圈','8-2':'再看开头那个盒子'}
def title(k):return titles.get(k,TITLE.get(k,S[k]['title']))
def make():
 caps=[(a+starts[k],b+starts[k],s)for k,d in S.items()for a,b,s in captions(d)]
 for j,(a,b,_)in enumerate(caps):assert 0<=a<b<=TOTAL and (not j or a>=caps[j-1][1]-.0001)
 subs='\n\n'.join(f'{j}\n{stamp(a)} --> {stamp(b)}\n{tt}'for j,(a,b,tt)in enumerate(caps,1))+'\n'
 (O/(BASE+'.srt')).write_text(subs)
 ff=';FFMETADATA1\ntitle=模型评测与基准测试 · Stanford CS336 第 12 讲\ncomment='+credits+'\n'
 for i,t in chap.items():ff+=f'[CHAPTER]\nTIMEBASE=1/1000\nSTART={round(1000*t)}\nEND={round(1000*chap.get(i+1,TOTAL))}\ntitle=Beat {i} · {CH[i]}\n'
 (W/'master.ffmeta').write_text(ff)
 scores=json.loads((W/'audio/cuebook.json').read_text());timeline=dict(duration=TOTAL,chapters=[dict(beat=i,title=CH[i],time=t)for i,t in chap.items()],scenes=[dict(id=k,title=title(k),time=starts[k],duration=S[k]['duration'])for k in IDS],questions=scores['questions'])
 (W/'timeline.json').write_text(json.dumps(timeline,ensure_ascii=False,indent=2))
 md=f'# 模型评测与基准测试｜中文逐字稿\n\n**{mm(TOTAL)} · Stanford CS336，第 12 讲。** 无声画面和本地有声剪辑共用以下章节时码。可在播放器里按章跳转；这里的时码按整秒就近取整。\n\n'
 for i,t in chap.items():md+=f'- {mm(t)}　{CH[i]}\n'
 for i,t in chap.items():
  md+=f'\n## {mm(t)}　{CH[i]}\n\n'
  for k in IDS:
   if int(k[0])!=i:continue
   md+=f'### {mm(starts[k])}　{title(k)}\n\n'
   paras=[]
   for row in S[k]['groups']:
    text=clean(row['text'])
    if paras and (len(paras[-1])<31 or paras[-1].endswith(('，','：','、'))):paras[-1]+=text
    else:paras.append(text)
   md+='\n\n'.join(paras)+'\n\n'
 (O/(BASE+'-逐字稿与章节.md')).write_text(md.rstrip()+'\n')
 return len(caps)
if __name__=='__main__':print(make(),'captions')
