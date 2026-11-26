"""Build the offline screening companion from the same scene and subtitle clocks as the master."""
from pathlib import Path
import base64,json,html,re,argparse
from edition4 import W,STEM,DEST,book,mm,chapters
TITLES=(('分数的影子','同样是 82 分，两个模型可以长得完全不同。'),('四把尺子','预算、偏好和用量，能把同一颗模型点带到不同位置。'),('困惑度','沿着原文读，再单独看最后一个答案。'),('换一张考卷','从选中一个字母，到给专家也不容易的题设一道关。'),('一封催办信','选一封你愿意寄出去的，再看一张票如何进入天梯。'),('补丁进仓库','修好眼前的问题，还要保住原本正常的 45 项测试。'),('网格与安全','先把第四张图填好；接下来，读完一份回答再判。'),('考场之外','一份图纸怎样验收，一段试题何时混进训练材料。'),('再看八十二分','转到盒子的另一面，把刚才那根标尺再量一次。'))
SHELF=(('21_05','困惑度','把一百条路排成十乘十'),('42_01','埃洛评分','丙偶尔还反杀甲'),('4-1','匿名投票','选一封你愿意发出的邮件'),('5-1','SWE-bench','跟一份真实修复走进仓库'),('6-1','ARC-AGI','把第四张图留给自己'),('7-3','13-gram','跟着十三个词穿过一页材料'))
CLOSEUPS=((189.6,'选票落下','看一次匿名选择怎样连起两点'),
          (442.7,'分词换尺','从一百条路接到同一句原文'),
          (1579.5,'音乐接缝','两首原曲在此处交叠'),
          (1831.6,'结尾回线','从整段概率移到最后的答案'))
QUESTION_STOPS=(('opening','CS336 Lecture 12','看片名和五组图形写入黑底'),
                ('door2','困惑度','从一整串词元看模型如何分配概率'),
                ('door3','考卷','把眼光从整段文字移到最后一项'),
                ('door4','盲测','从选标准答案到选一份回复'),
                ('door5','代码沙箱','把补丁放进同一个仓库检验'),
                ('door6','效度与污染','从考场进到真实工作现场'))
def jd(x):return json.dumps(x,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
def display(t):return mm(t,1) if abs(t-round(t))>.0004 else mm(t)
def voice_deck(config):
 if config is None:return ''
 d=json.loads(Path(config).read_text());q=lambda s:html.escape(s,quote=True);asset=q(Path(d['file']).name)
 trs=[]
 for pair in d['pairs']:
  title=q(pair['title']);time=display(pair['time']);inner=[]
  for label,part in zip(('原版','本版'),pair['parts']):
   inner.append(f'<button type="button" aria-label="听{label}：{title}" data-voice-from="{part["from_"]:.3f}" data-voice-to="{part["to"]:.3f}">{label}</button>')
  trs.append(f'<div class="take"><time>{time}</time><span>{title}</span>{"".join(inner)}</div>')
 return ('<section class="voicebox" aria-labelledby="dial"><h2 id="dial">同一句话，听两个版本</h2>'
         '<p>点一段比较语气。两版只留旁白，按段对齐响度。</p>'+''.join(trs)+
         f'<audio id="voices" controls preload="none" src="{asset}" aria-label="人声对照"></audio></section>')


def build(out,comparison=None):
 ss=(DEST/(STEM+'.srt')).read_text().strip();caps=[]
 def ticks(x):h,m,s,ms=map(int,re.split('[:,]',x));return h*3600+m*60+s+ms/1000
 for s in re.split(r'\n\s*\n',ss):
  num,se,*txt=s.splitlines();a,b=se.split(' --> ');caps.append((ticks(a),ticks(b),' '.join(txt)))
 stops=json.loads((DEST/'performance.json').read_text());rests=[[r['start'],r['end'],r['name']]for r in stops if r['kind']=='pause' and r['end']-r['start']>=1.8]
 rows=book();names={r['id']:r for r in rows};qt=lambda s:html.escape(s,quote=True)
 tl=[dict(t=t,name=n,caption=cap)for (t,_,_),(n,cap) in zip(chapters(),TITLES)]
 for row in rows:
  card=json.loads((W/'scene-clocks'/f'{row["id"]}.json').read_text())
  for rec in card['groups_meta']:
   names[rec['id']]={'t0':row['t0']+rec['start']}
 nav=''.join(f'<button class="chapter" type="button" data-ch="{i}" data-t="{v["t"]:.3f}"><time>{display(v["t"])}</time><b>{v["name"]}</b><span class="mark" aria-hidden="true"></span></button>'for i,v in enumerate(tl))
 def clips(items):return ((names[k]['t0'],term,label)for k,term,label in items)
 def marker(t,term,label):return f'<button class="excerpt" type="button" data-t="{t:.3f}"><span class="term">{qt(term)}</span><span class="explain">{qt(label)}</span><time>{display(t)}</time></button>'
 ex=''.join(marker(*x)for x in (*CLOSEUPS,*clips(SHELF)))
 questions=''.join(marker(*x)for x in clips(QUESTION_STOPS))
 li=''.join(f'<a href="{qt(STEM+path)}">{label}<span aria-hidden="true"> ↗</span></a>'for path,label in (('.mp4','可切换字幕的全片'),('-逐字稿与章节.md','逐字稿与章节'),('-数据与配乐.md','数据与配乐出处'),('.srt','中文字幕 SRT'),('-人声导演记录.md','人声导演记录'),('-复剪工程.zip','可复剪工程')))
 tmpl=(W/'package/看片模板.html').read_text()
 for k,x in [('length',f'{int(sum(r["duration"] for r in rows))//60} 分 {sum(r["duration"] for r in rows)%60:04.1f} 秒'),('poster','data:image/jpeg;base64,'+base64.b64encode((W/'assets/poster.jpg').read_bytes()).decode()),('movie',qt(STEM+'-字幕版.mp4')),('chapters',nav),('examples',ex),('question-stops',questions),('links',li),('voice',voice_deck(comparison)),('timeline',jd(tl)),('scenes',jd([dict(t=r['t0'],id=r['id'],label=r['title'])for r in rows])),('words',jd(caps)),('rests',jd(rests))]:tmpl=tmpl.replace('@@'+k+'@@',x)
 if '@@' in tmpl:raise ValueError('unfilled marker')
 out=Path(out);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(tmpl);print(out)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--comparison',type=Path);a=p.parse_args();build(a.out,a.comparison)
