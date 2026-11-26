"""Public-facing captions, chapter clocks, source notes, and lossless-picture edit list."""
import re,json,math,bisect,unicodedata,subprocess
from pathlib import Path
W=Path(__file__).resolve().parent;O=W/'exports';O.mkdir(exist_ok=True)
BASE='CS336-L12-模型评测-全片中文-v2'
S={p.stem:json.loads(p.read_text()) for p in sorted((W/'scenes').glob('*.json'))}
from chapters_zh import CH,TITLE
for k,d in S.items():
 if k in TITLE:d['title']=TITLE[k]
starts={};chap={};cur=0.
for k,d in S.items():
 starts[k]=cur
 if k.endswith('-1'):chap[d['beat']]=cur
 cur+=d['frames']/30
TOTAL=cur
def stamp(t):
 ms=round(t*1000); s,z=divmod(ms,1000);h,r=divmod(s,3600);m,s=divmod(r,60);return f'{h:02}:{m:02}:{s:02},{z:03}'
def secs(st):
 h,m,s=re.split('[:,]',st)[:3];return int(h)*3600+int(m)*60+int(s)+int(st[-3:])/1000
def at(t):
 m,s=divmod(round(t),60);return f'{m:02}:{s:02}'
def canon(s):return re.sub(r'[^a-z0-9\u3400-\u9fff]','',unicodedata.normalize('NFKC',s).lower())
def width(s):return sum(.55 if ord(c)<128 else 1 for c in s)
gloss=r'（(?:Test-Time Compute|Ecological Validity|Data Contamination|Exchangeability|Scaffold)）'
def clean(s):return re.sub(gloss,'',s).strip()
def captions(d):
 s=d['text']; pos=[0]
 for ch in s:pos.append(pos[-1]+len(canon(ch)))
 words=d['chars']; assert pos[-1]==len(words)
 # Take times refer to real phonemes. Keep the optional English gloss out of the timed language.
 no={i for m in re.finditer(gloss,s) for i in range(m.start(),m.end())}
 idx=[i for i in range(len(s)) if i not in no];rep=''.join(s[i] for i in idx);L=len(idx)
 editorial=set()
 if d['id']=='7-4':
  for after in ['海量高质量代码文件开头','因此，成熟的数据流水线']:
   if after in rep:editorial.add(rep.index(after)+len(after))
 def a(j):return d['starts'][min(len(words)-1,pos[idx[j]])]
 def b(j):return d['ends'][max(0,pos[idx[j-1]+1]-1)]
 # Break at clause boundaries, strongly prefer the end of a complete thought. Do not slice model names.
 hard='。！？；';soft='，、：——'
 spots={0,L}
 for j in range(1,L):
  q,rr=rep[j-1],rep[j]
  if q in hard+soft or rr in '“' or q.isspace():spots.add(j)
  elif q.isascii() and rr.isascii():continue
  elif q not in '（“' and rr not in '，。：？！”、；）' and not q.isspace():spots.add(j)
 nodes=sorted(spots);memo={0:(0,None)}
 for v in nodes[1:]:
  best=(float('inf'),None)
  if v<L and rep[v] in '。，？！；、：）”——':continue
  for u in reversed(nodes[:bisect.bisect_left(nodes,v)]):
   phrase=rep[u:v].strip();weight=width(phrase)
   if weight>29:break
   if u not in memo or not canon(phrase):continue
   dur=b(v)-a(u)
   if dur<=.08:continue
   inside=sum(1 for ch in phrase[:-1] if ch in hard)
   # Internal full stops are costly unless both thoughts are exceptionally short.
   cost=(max(0,12-weight)*.45+max(0,weight-24)*.37+3.7*max(0,1.1-dur)**2+2.2*max(0,dur-5.7)**2+inside*8.5)
   if v!=L:
    cost+=0 if phrase[-1] in hard or v in editorial else 1.45 if phrase[-1] in '，：—' else 3.1 if phrase[-1]=='、' else 12.8
   if phrase in ('因此，','所以，','然而，','但是，','于是，'):cost+=35
   cost+=1.2+(.7 if phrase[0] in '，' else 0)
   cand=memo[u][0]+cost
   if cand<best[0]:best=(cand,u)
  if best[1] is not None:memo[v]=best
 assert L in memo,d['id']
 nodes=[];i=L
 while i: j=memo[i][1];nodes.append((j,i));i=j
 caps=[]
 for j,i in reversed(nodes):
  cap=rep[j:i].strip()
  if not canon(cap):continue
  caps.append([a(j),b(i),cap])
 # A half-second discourse marker is not a reading unit. Keep it with its own claim.
 for j in range(len(caps)-2,-1,-1):
  if caps[j][2]=='问题来了。' and width(caps[j][2]+caps[j+1][2])<=28:
   caps[j:j+2]=[[caps[j][0],caps[j+1][1],caps[j][2]+caps[j+1][2]]]
 for j,k in enumerate(caps):
  # Keep the question in view through the listening pause, never under the first syllable of the answer.
  tail=.85 if k[2].endswith(('？','？）','？”')) else .13
  k[1]=min(k[1]+tail,caps[j+1][0]-.009 if j+1<len(caps) else d['duration']-.03)
  # ASR intervals for silent punctuation can coincide around technical names.
  if j and k[0]<caps[j-1][1]:k[0]=caps[j-1][1]+.001
  assert k[1]>k[0],(d['id'],k)
 assert canon(''.join(c[2] for c in caps))==canon(rep)
 return caps
def make():
 allcaps=[]
 for k,d in S.items():
  off=starts[k];new=captions(d);allcaps.extend([(a+off,b+off,txt) for a,b,txt in new])
 for j,(a,b,txt) in enumerate(allcaps):
  assert 0<=a<b<=TOTAL and (not j or a>=allcaps[j-1][1]-.0001),(j,a,b)
 st='\n\n'.join(f'{j}\n{stamp(a)} --> {stamp(b)}\n{txt}' for j,(a,b,txt) in enumerate(allcaps,1))+'\n'
 (O/(BASE+'.srt')).write_text(st)
 comment='配乐：Tuck and Point / A Certain Lightness / One Little Triumph — Blue Dot Sessions；节选、淡变及混音。CC BY-NC 4.0：https://creativecommons.org/licenses/by-nc/4.0/'
 md=';FFMETADATA1\ntitle=模型评测与基准测试 · Stanford CS336 第 12 讲\ncomment='+comment+'\n'
 for b,t in chap.items():
  md+=f'[CHAPTER]\nTIMEBASE=1/1000\nSTART={round(1000*t)}\nEND={round(1000*chap.get(b+1,TOTAL))}\ntitle=Beat {b} · {CH[b]}\n'
 (W/'master.ffmeta').write_text(md)
 lst='ffconcat version 1.0\n'
 for f,dur in [(W/'shots'/(k+'.mp4'),x['frames']/30) for k,x in S.items()]:
  lst+=f"file '{f.resolve()}'\nduration {dur:.9f}\n"
 (W/'video.ffconcat').write_text(lst)
 (W/'timeline.json').write_text(json.dumps({'duration':TOTAL,'chapters':[{ 'beat':b,'title':CH[b],'start':t} for b,t in chap.items()],'scenes':[{ 'id':k,'title':s['title'],'start':starts[k],'duration':s['duration']} for k,s in S.items()]},ensure_ascii=False,indent=2))
 guide=f'# 模型评测与基准测试｜中文逐字稿\n\n全片 {at(TOTAL)}。时间点对应本次中文成片；播放器里可按 Beat 跳转。默认音轨是旁白与配乐，第 2 条是纯旁白。\n\n'
 for b,t in chap.items():guide+=f'- **{at(t)}**　Beat {b} · {CH[b]}\n'
 for b,t in chap.items():
  guide+='\n## '+at(t)+f'　Beat {b} · '+CH[b]+'\n\n'
  for k,d in S.items():
   if d['beat']!=b:continue
   paras=[]
   for g in d['groups']:
    para=clean(g['text'])
    if paras and (width(paras[-1])<32 or paras[-1][-1:] in '，、：'):paras[-1]+=para
    else:paras.append(para)
   guide+=f"### {at(starts[k])}　{d['title']}\n\n"+'\n\n'.join(paras)+'\n\n'
 (O/(BASE+'-逐字稿与章节.md')).write_text(guide.strip()+'\n')
 print('duration',TOTAL,'chapters',[(i,at(t)) for i,t in chap.items()],'captions',len(allcaps),flush=True)
if __name__=='__main__':make()
