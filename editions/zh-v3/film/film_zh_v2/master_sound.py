"""Mix the full native Mandarin cut on the shared word clock. All voices are the personal Drama 3 takes."""
from pathlib import Path
from functools import lru_cache
import json,subprocess,math,os,sys
import numpy as np,soundfile as sf
from scipy.signal import resample_poly,butter,sosfilt,find_peaks
from scipy.ndimage import maximum_filter1d,gaussian_filter1d
from edition import S,starts,TOTAL,W
SR=48000;LIB=W.parent/'beats_lively/music';FILES=('tuck-and-point','a-certain-lightness','one-little-triumph');NAMES=('Tuck and Point','A Certain Lightness','One Little Triumph')
# Anchor long licensed musical phrases to their narrative purpose. Densest mathematical comparisons
# periodically use voice alone; consecutive scenes are not independent short loops.
def wall(id,point):
 d=S[id]
 if isinstance(point,str):
  from edition import canon
  k=d['chars'].find(canon(point))
  if k<0:raise ValueError((id,point))
  return starts[id]+d['starts'][k]
 return starts[id]+point
def when(tag):
 id,x,*offset=tag;return wall(id,x)+(offset[0] if offset else 0.)
score=[
 (('0-1',0),('1-1',2.92),0,.0,-29.1,'投影与追分'),
 (('1-1',2.18),('1-3',8.2),1,.34,-29.0,'成本、投票与四把尺'),
 (('1-3',7.12),('2-1','取负对数'),2,.20,-30.0,'比较方法，再走进速训赛'),
 (('2-1','这个数怎么看'),('2-3','先想一个理想情况',.24),1,90.0,-30.3,'从等效分支到分词尺度'),
 (('2-3','先想一个理想情况',-.38),('2-4','各占一列'),0,65.0-(wall('2-3','给定题目')-wall('2-3','先想一个理想情况')+.38),-30.5,'算术答案与两列语料'),
 (('2-4','合在一起'),('3-1','五十七个学科'),2,44.1,-30.3,'六域合成与自动批改'),
 (('3-1','历史题'),('3-3','非本领域的人'),1,136.4,-28.8,'余量、改题与检索'),
 (('3-3','两位同领域博士'),('3-4','日常用大模型'),0,16.1,-30.0,'专家的两道筛网'),
 (('3-4','数据清洗脚本'),('4-2','先看两人的分差'),2,18.2,-29.3,'一票只约束一对'),
 (('4-2','积分完全相同'),('4-3','位置偏见'),1,28.8,-30.5,'分差分出胜率，再换裁判'),
 (('4-3','互换位置'),('4-4','长度差设成零'),0,45.3,-29.7,'位置、写法与长度'),
 (('4-4','每道题都这样算'),('5-2','运行依赖'),2,41.5,-29.4,'把回复放进真正的仓库'),
 (('5-2','第一道叫'),('5-3','工程脚手架'),1,174.2,-30.7,'红绿灯与重复采样'),
 (('5-3','工具调用循环'),('6-1','抽象变换规则'),0,47.6,-29.8,'工具包与无文字的网格'),
 (('6-1','几何对称'),('6-3','第一句是拒绝'),2,60.8,-30.7,'搜索候选，读完整回答'),
 (('6-3','分成两组'),('6-4','第一个模型出了八次'),1,83.9,-31.1,'分开分母，观察条件'),
 (('6-4','逐张翻过来'),('7-1','尺子和真实工作'),0,68.2,-30.4,'同样三张，再问外部效度'),
 (('7-2',.4),('7-3','连续十三个词'),1,123.6,-30.4,'公开原序与随机排列'),
 (('7-3','哈希集合'),('7-5','第一道是'),2,56.0,-30.7,'窗口、复核与掩码'),
 (('7-5','九月底停止训练'),('8-1','开放对话'),0,64.2,-29.4,'按时间出题，把尺子串起来'),
 (('8-1','开放对话'),('8-2',S['8-2']['duration']),2,None,-28.5,'回到第一帧的几何体')]
@lru_cache(None)
def music(i):
 path=LIB/(FILES[i]+'.mp3')
 raw=subprocess.check_output(['/usr/bin/ffmpeg','-v','error','-nostdin','-threads','1','-i',str(path),'-ar',str(SR),'-ac','2','-f','f32le','-'])
 return sosfilt(butter(2,62,fs=SR,output='sos',btype='highpass'),np.frombuffer(raw,'<f4').reshape(-1,2),axis=0).astype('f4')
def planned():
 cue=[]
 for start,end,i,into,level,job in score:
  a=round(when(start)*SR);b=min(round(when(end)*SR),round(TOTAL*SR));n=b-a;assert n>3*SR
  m=music(i);p=round((len(m)/SR-n/SR-.06 if into is None else into)*SR)
  if p+n>len(m):
   # Choose a single earlier excerpt; never loop, stretch, or ask the reader for missing samples.
   p=len(m)-n-round(.12*SR)
  assert 0<=p<p+n<=len(m),(job,n/SR,p/SR)
  rms=np.sqrt(np.mean(m[p:p+n:5]**2));gain=10**(level/20)/max(.001,rms)
  cue.append(dict(a=a,b=b,i=i,p=p,gain=gain,label=job))
 return cue
def click_sample():
 # One real upright-piano attack from One Little Triumph. Its naturally decaying partials make
 # a quiet cue which belongs to the score, rather than a synthesizer jingle.
 m=music(2);p=round(.461*SR);dur=round(.405*SR);y=m[p:p+dur].mean(axis=1)
 y=sosfilt(butter(2,(370,5400),fs=SR,btype='bandpass',output='sos'),y).astype('f4')
 t=np.arange(len(y))/SR;env=np.minimum(1,t/.008)*np.exp(-np.maximum(0,t-.055)/.082)*np.minimum(1,(len(y)/SR-t)/.075);v=y*env
 return (v/(np.max(abs(v))+.000001)).astype('f4')
def main():
 cue=planned();hits=[]
 for id,d in S.items():
  for q in d['questions']:
   if q['marked']:
    a=starts[id];hits.append({'id':id,'q':a+q['time'],'next':a+q['next'],'tap':a+q['time']+.15})
 qfx=click_sample();meta=[]
 for c in cue:meta.append(dict(start=c['a']/SR,end=c['b']/SR,title=NAMES[c['i']],source=c['p']/SR,purpose=c['label']))
 (W/'music-cues.json').write_text(json.dumps({'music':meta,'questions':hits,'sfx_source':'One Little Triumph · approximately 0:00.46 · single piano attack · filtered and shortened'},ensure_ascii=False,indent=2))
 mark=[];cur=0
 with sf.SoundFile(W/'master-mix.wav','w',samplerate=SR,channels=2,subtype='PCM_24') as mix,sf.SoundFile(W/'master-dry.wav','w',samplerate=SR,channels=1,subtype='PCM_24') as dry:
  for id,s in S.items():
   y,sr=sf.read(W/'scenes'/(id+'.wav'),dtype='f4');assert sr==44100
   y=resample_poly(y,160,147).astype('f4');n=s['frames']*1600;assert len(y)==n
   voice=y*.967;bed=np.zeros((n,2),'f4')
   for j,c in enumerate(cue):
    a,b,i,ofs,gn=[c[k] for k in ('a','b','i','p','gain')];u,v=max(a,cur),min(b,cur+n)
    if u>=v:continue
    t=np.arange(u-a,v-a)/SR;dur=(b-a)/SR
    ri=0.74 if j==0 else 1.12;ro=.65 if j==len(cue)-1 else 1.37
    env=(np.sin(np.minimum(1,t/ri)*np.pi/2)**2*np.sin(np.clip((dur-t)/ro,0,1)*np.pi/2)**2).astype('f4')
    bed[u-cur:v-cur]+=music(i)[ofs+u-a:ofs+v-a]*(env*gn)[:,None]
   frames=np.pad(voice,(0,(-n)%480)).reshape(-1,480);loud=np.sqrt(np.mean(frames**2,axis=1));active=gaussian_filter1d(maximum_filter1d(np.clip((loud-.009)/.082,0,1),size=13),6.3)
   env=np.interp(np.arange(n)/480,np.arange(len(active)),1-.50*active).astype('f4')
   clock=(cur+np.arange(n))/SR
   sfx=np.zeros(n,'f4')
   for hit in hits:
    t0=hit['q'];t1=max(t0+.81,hit['next']-.21)
    # The music keeps its own resonance while the person thinks. It never jumps to digital silence.
    v=np.minimum(1,np.maximum(0,(clock-t0)/.74));z=np.clip((clock-t1)/.66,0,1)
    env*=1-.62*(v*v*(3-2*v))*(1-z*z*(3-2*z))
    first=round(hit['tap']*SR)-cur;left=max(0,first);right=min(n,first+len(qfx))
    if right>left:sfx[left:right]+=qfx[left-first:right-first]*.107
   bed*=env[:,None];summed=bed+voice[:,None]+sfx[:,None]
   # A soft peak guard operates only on isolated summation peaks, never on the regular syllables.
   peak=float(np.max(np.abs(summed)));mask=np.abs(summed)>.88
   if np.any(mask):summed[mask]=np.sign(summed[mask])*(.88+.04*np.tanh((np.abs(summed[mask])-.88)/.04))
   dry.write(voice);mix.write(summed)
   row=dict(scene=id,mix_peak=round(peak,4),bed_rms_db=round(20*np.log10(np.mean(bed**2)**.5+1e-12),2),voice_rms_db=round(20*np.log10(np.mean(voice**2)**.5+1e-12),2),sfx=float(np.max(abs(sfx))))
   mark.append(row)
   for x in hits:
    if x['id']==id:
     # Store only the five critical local listening excerpts, not a giant redundant isolated stem.
     lo,hi=map(int,[max(0,(x['q']-starts[id]-2.5)*SR), min(n,(x['q']-starts[id]+2.0)*SR)])
     sf.write(W/'notes'/('question-'+x['id']+'-'+str(round(x['q']))+'.wav'),summed[lo:hi],SR)
   print(id,round(cur/SR,3),row['mix_peak'],row['bed_rms_db'],flush=True);cur+=n
 assert cur==round(TOTAL*SR)
 (W/'notes/mix-readings.json').write_text(json.dumps(mark,indent=2,default=float))
if __name__=='__main__':main()
