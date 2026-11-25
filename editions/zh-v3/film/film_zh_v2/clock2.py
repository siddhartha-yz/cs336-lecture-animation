"""Lay the edit against real Drama 3 phones, with explicit room for answers and chart reads."""
from pathlib import Path
import json,math,re,subprocess,sys,unicodedata
from difflib import SequenceMatcher
import numpy as np,soundfile as sf
W=Path(__file__).resolve().parent; SR=44100;FPS=30
plan=json.loads((W/'plan.json').read_text()); scenes=json.loads((W/'script.json').read_text())
def canon(s):return re.sub(r'[^a-z0-9\u3400-\u9fff]','',unicodedata.normalize('NFKC',s).lower())
def units(s):return len(re.findall(r'[\u3400-\u9fff]',s))+.49*len(re.findall('[a-zA-Z0-9]',s))
def wordclock(text,words,dur):
 obs='';left=[];right=[]
 for w in words:
  st=canon(w['word']); edges=np.linspace(w['start'],w['end'],len(st)+1)
  obs+=st;left.extend(edges[:-1]);right.extend(edges[1:])
 target=canon(text); m=SequenceMatcher(None,target,obs,autojunk=False)
 blocks=m.get_matching_blocks();ks=[i+k for i,j,n in blocks for k in range(n)];js=[j+k for i,j,n in blocks for k in range(n)]
 if len(ks)<3:raise ValueError(('no reliable words',text))
 keys=[-.5,*ks,len(target)-.5]
 return [np.clip(np.maximum.accumulate(np.interp(np.arange(len(target)),keys,[0,*[u[j] for j in js],dur])),0,dur) for u in (left,right)]
def bounds(y):
 hop=220;n=len(y)//hop;rms=np.sqrt(np.mean(y[:n*hop].reshape(-1,hop)**2,axis=1))
 threshold=max(.0016,np.percentile(rms,88)*.014)
 has=np.where(rms>threshold)[0]
 return max(0,int(has[0])*hop-round(.05*SR)),min(len(y),(int(has[-1])+1)*hop+round(.08*SR))
def lowroom(y,a,b):
 # Return the center and length of a genuine low-energy interval between neighbouring phones.
 hop=round(.005*SR); win=2*hop;av=(a+b)/2;lo=max(0,round((min(a,av)-.11)*SR));hi=min(len(y),round((max(b,av)+.10)*SR))
 grid=np.arange(lo,hi-win,hop,dtype=int)
 if len(grid)<4:return None
 rms=np.array([np.sqrt(np.mean(y[i:i+win]**2)) for i in grid])
 mask=np.r_[False,rms<.006,False]
 runs=[(int(grid[l]),int(grid[r-1])+win) for l,r in zip(np.where(~mask[:-1] & mask[1:])[0],np.where(mask[:-1] & ~mask[1:])[0])]
 if not runs:return None
 a,b=max(runs,key=lambda x:(x[1]-x[0])/SR-.13*abs((sum(x)/2/SR)-av))
 if b-a<.035*SR:return None
 return (a+b)//2,(b-a)/SR
major={'c01':(0,.94),'c03':(0,1.10),'23_01':(0,.87),'31_04':(0,1.12),'44_05':(0,1.05)}
target={'0-1':258,'0-2':253,'1-1':257,'1-2':266,'2-1':259,'2-2':260,'2-3':260,'2-4':256,'3-1':259,'4-2':256,'5-3':256,'6-4':254,'7-2':263,'8-2':247}
ends={'0-1':.38,'0-2':.83,'1-1':1.18,'1-2':.8,'1-3':.50,'1-4':1.18,'2-1':1.70,'2-2':.83,'2-3':.92,'2-4':1.15,'3-1':1.25,'4-4':1.20,'6-4':1.05,'8-2':2.35}
def wave(y,rate):
 if abs(rate-1)<.006:return y
 cmd=['/usr/bin/ffmpeg','-nostdin','-hide_banner','-v','error','-filter_threads','1','-f','f32le','-ar',str(SR),'-ac','1','-i','pipe:','-af',f'atempo={rate:.8f}','-c:a','pcm_f32le','-threads','1','-f','f32le','pipe:']
 data=subprocess.check_output(cmd,input=y.astype('<f4').tobytes());return np.frombuffer(data,'<f4')
def raw(row):
 id=row['id']; y,sr=sf.read(W/'takes'/(id+'.wav'),dtype='float32');assert sr==SR and y.ndim==1
 qa=json.loads((W/'qa'/(id+'.json')).read_text())
 a,b=wordclock(row['text'],qa.get('alignment_words',qa['words']),len(y)/SR)
 left,right=bounds(y);y=y[left:right];a=np.clip(a-left/SR,0,len(y)/SR);b=np.clip(b-left/SR,0,len(y)/SR)
 return y,a,b,qa
def make(s):
 sel=[r for r in plan if r['scene']==s['id']]
 if any(not (W/'qa'/(r['id']+'.json')).exists() or not (W/'takes'/(r['id']+'.wav')).exists() for r in sel):return
 takes=[raw(r) for r in sel];groups=[];extras=[];qs=[]
 hold=ends.get(s['id'],min(.86,max(.54,s['hold']*.81)))
 gaps=[]
 for j,(r,(y,aa,bb,qa)) in enumerate(zip(sel,takes)):
  gap=hold if j==len(sel)-1 else (.065 if r['text'][-1] in '，、；：' else .185)
  integ=[]
  for no,m in enumerate(re.finditer(r'[？?]',r['text'])):
   idx=len(canon(r['text'][:m.start()]))-1
   arm=(r['id'] in major and no==major[r['id']][0])
   expected=major[r['id']][1] if arm else .46
   if idx+1>=len(aa):
    # Speech tail is already retained in the take and the next take has a small head.
    gap=max(gap,expected-.06);integ.append((idx,None,0,arm))
   else:
    rr=lowroom(y,bb[idx],aa[idx+1]); room=rr[1] if rr else 0
    amount=max(0,expected-room) if rr else 0
    integ.append((idx,rr[0] if rr else None,amount,arm))
  extras.append(integ);gaps.append(gap)
 count=units(s['text']);locked=s.get('lock_frames');budget=locked/FPS if locked else 60*count/target.get(s['id'],264)
 all_extra=sum(e[2] for ls in extras for e in ls);native=sum(len(x[0])/SR for x in takes)
 tempo=float(np.clip(native/max(1,budget-sum(gaps)-all_extra),.98,1.24 if s['id']=='2-1' else 1.21))
 parts=[];ss=[];ee=[];offset=0
 for r,(y,a,b,qa),changes,gap in zip(sel,takes,extras,gaps):
  seg=wave(y,tempo); ratio=len(seg)/len(y);l=a*ratio;h=b*ratio
  add=0;fragments=[];pointer=0;qrows=[]
  for idx,cut,dt,arm in changes:
   if cut is not None and dt>.012:
    cp=round(cut*ratio);klen=round(dt*SR)
    fragments.extend([seg[pointer:cp],np.zeros(klen,'f4')]);pointer=cp;add+=klen
    l[idx+1:]+=klen/SR;h[idx+1:]+=klen/SR
   qt=offset/SR+h[idx]
   qrows.append((idx,qt,arm))
  fragments.append(seg[pointer:]);part=np.concatenate(fragments) if len(fragments)>1 else seg
  # Time points lie in the audible word and the subsequent reading pause, not in arbitrary slot boundaries.
  for idx,qt,arm in qrows:
   nq=offset/SR+(l[idx+1] if idx+1<len(l) else len(part)/SR+gap)
   qs.append({'take':r['id'],'word_index':idx,'time':float(qt),'next':float(nq),'marked':arm})
  groups.append({'id':r['id'],'from':offset/SR,'spoken_end':(offset+len(part))/SR,'gap':gap,'rate':tempo,'text':r['text']})
  ss.extend((l+offset/SR).tolist());ee.extend((h+offset/SR).tolist())
  parts += [part,np.zeros(round(gap*SR),'f4')];offset+=len(part)+len(parts[-1])
 nframes=math.ceil(offset/1470)
 if locked:
  # This pickup replaces two utterances inside an exposed scene; the *last
  # room tone* absorbs atempo rounding. Never truncate a word to make an edit.
  tail=round((locked/FPS-groups[-1]['spoken_end'])*SR)
  if not .38*SR<=tail<=1.05*SR:raise ValueError(('unusable final release',s['id'],tail/SR,tempo))
  nframes=locked;parts[-1]=np.zeros(tail,'f4');groups[-1]['gap']=tail/SR;offset=sum(len(v)for v in parts)
 parts.append(np.zeros(nframes*1470-offset,'f4'));y=np.concatenate(parts)
 assert len(ss)==len(canon(s['text'])) and len(ee)==len(ss),(s['id'],len(ss),len(canon(s['text'])))
 # actual script written to the picture even when glyph pronunciation uses an alias
 clock={**s,'duration':nframes/FPS,'frames':nframes,'hold':(len(y)/SR-groups[-1]['spoken_end']),'chars':canon(s['text']),'starts':ss,'ends':ee,'groups':groups,'questions':qs,'tempo':tempo,'speech':groups[-1]['spoken_end']}
 out=W/'scenes';sf.write(out/(s['id']+'.wav'),y,SR,subtype='PCM_16');(out/(s['id']+'.json')).write_text(json.dumps(clock,ensure_ascii=False))
 print(s['id'],round(nframes/FPS,2),round(native,2),round(tempo,3),[(q['take'],round(q['next']-q['time'],2)) for q in qs if q['marked']],flush=True)
if __name__=='__main__':
 for s in scenes:
  if len(sys.argv)>1 and s['id'] not in sys.argv[1:]:continue
  make(s)
