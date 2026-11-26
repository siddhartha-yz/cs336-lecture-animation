from pathlib import Path
import sys,json,re,math,bisect,unicodedata
from difflib import SequenceMatcher
from functools import lru_cache
W=Path(__file__).resolve().parent; OLD=W.parent/'film_zh_v2'
def canon(s):return re.sub(r'[^a-z0-9\u3400-\u9fff]','',unicodedata.normalize('NFKC',s).lower())
S={p.stem:json.loads(p.read_text())for p in sorted((W/'scenes').glob('*.json'))}
B={p.stem:json.loads(p.read_text())for p in sorted((OLD/'scenes').glob('*.json'))}
def timebase(rows):
 o={};t=0
 for k,r in rows.items():o[k]=t;t+=r['frames']/30
 return o,t
starts,TOTAL=timebase(S);v2starts,v2total=timebase(B);IDS=list(S);CH=['追分数的模型','给能力加一把尺','平均分里的例外','被考穿的试卷','把一票变成胜率','把补丁交给测试','把规则带到新题','评测走出考场','从影子回到模型']
def mm(t,prec=0):
 sec=round(t,prec);m,s=divmod(sec,60);return f'{int(m):02}:'+ (f'{s:04.1f}'if prec else f'{int(s):02}')
class Clock:
 def __init__(self,d):self.s=d;self.d=d['duration'];self.t=0.
 @lru_cache(None)
 def at(self,token,occ=0):
  needle=canon(token);j=-1
  for _ in range(occ+1):
   j=self.s['chars'].index(needle,j+1)
  return self.s['starts'][j]
 def u(self,t,q,span=1.15,early=.12):
  v=max(0,min(1,(t-self.at(q)+early)/span));return v*v*(3-2*v)
 def clk(self,t):self.t=t;return self
@lru_cache(None)
def clock(k):return Clock(S[k])
def smooth(t,a,b):
 z=min(1,max(0,(t-a)/max(.00001,b-a)));return z*z*(3-2*z)
# Set knots at shared meaningful words, never freeze a drawing because a syllable was dropped.
# The untouched legacy drawings keep their original relationships internally. New set pieces
# (and captions) use the new syllables directly, not this map.
@lru_cache(None)
def knots(k):
 a,b=S[k],B[k]; aa=[0.];bb=[0.];ji=kj=0
 def put(x,y):
  if x>aa[-1]+.023 and y>bb[-1]+.023:aa.append(x);bb.append(y)
 for rg,og in zip(a['groups'],b['groups']):
  s0=canon(rg['text']);s1=canon(og['text']);put(rg['from'],og['from'])
  for m in SequenceMatcher(None,s0,s1,autojunk=False).get_matching_blocks():
   if m.size<3:continue
   js=list(range(0,m.size,4))
   if m.size-1 not in js:js.append(m.size-1)
   for u in js:put(a['starts'][ji+m.a+u],b['starts'][kj+m.b+u])
  put(rg['spoken_end'],og['spoken_end']);ji+=len(s0);kj+=len(s1)
 put(a['duration'],b['duration']);return aa,bb
def remap(k,t):
 a,b=knots(k);j=max(0,min(len(a)-2,bisect.bisect_right(a,t)-1));ff=max(0,min(1,(t-a[j])/(a[j+1]-a[j])));return b[j]*(1-ff)+b[j+1]*ff
def span_group(d,g):
 k=sum(len(canon(x['text']))for x in d['groups'][:d['groups'].index(g)]);return k,k+len(canon(g['text']))
if __name__=='__main__':
 for k,d in S.items():
  print(k,mm(starts[k],1),round(d['duration'],1),len(d['questions']),d['groups'][0]['text'][:15])
 print(mm(TOTAL,1))
