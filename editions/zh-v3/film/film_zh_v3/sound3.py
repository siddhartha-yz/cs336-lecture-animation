"""A continuous score on the locked Drama 3 sample clock. Seven overlaps, no scene-by-scene gates."""
from pathlib import Path
import argparse,json,subprocess
import numpy as np
from functools import lru_cache
from scipy.signal import sosfilt,butter,resample_poly,lfilter
from scipy.ndimage import gaussian_filter1d,maximum_filter1d
import soundfile as sf
from timeline3 import W,OLD,starts,TOTAL,S,clock
from music_layout import TRACKS,layout
sr=48000
FILES=tuple(q[0] for q in TRACKS);NAMES=tuple(q[1] for q in TRACKS)
@lru_cache(2)
def mus(i):
 raw=subprocess.check_output(['/usr/bin/ffmpeg','-nostdin','-v','error','-threads','1','-i',str(W/'media'/(FILES[i]+'.mp3')),'-f','f32le','-ar',str(sr),'-ac','2','-'])
 v=np.frombuffer(raw,'<f4').reshape(-1,2);return sosfilt(butter(2,54,fs=sr,btype='highpass',output='sos').astype('f8'),v,axis=0).astype('f4')
def bell():
 # One isolated struck attack in a licensed score: compact transient, unlike the older piano cue.
 st=round(5.531*sr);n=round(.365*sr);base=mus(0)[st:st+round(n*2.37)].mean(axis=1)
 # Split the real marimba strike into its wooden body and a higher mallet partial.
 # It is a single strike with a tail, not a two-note notification tune.
 z=np.arange(n);ind=np.arange(len(base));root=np.interp(z*2.25,ind,base);edge=np.interp(z*1.5,ind,base)
 body=sosfilt(butter(3,(870,4300),fs=sr,btype='bandpass',output='sos'),root)
 attack=sosfilt(butter(3,(1400,6400),fs=sr,btype='bandpass',output='sos'),edge)
 sig=body+.31*attack
 # Two very short early reflections lengthen the recognition window without a reverberant wash.
 a=int(.031*sr);b=int(.058*sr);sig[a:]+=.28*sig[:-a].copy();sig[b:]+=.13*sig[:-b].copy()
 sig=np.tanh(2.15*sig/(np.max(np.abs(sig))+.00001))
 t=z/sr;env=np.minimum(1,t/.006)*np.exp(-np.maximum(0,t-.078)/.092)*np.clip((n/sr-t)/.055,0,1)
 v=sig*env;return np.asarray(v/(np.max(np.abs(v))+1e-9),dtype='f4')
def db(a):return 10*np.log10(np.maximum(a,1e-12))
def amp(g):return np.power(10.,g/20.)
def soft(x):
 u=np.clip(x,0.,1.);return u*u*(3.-2.*u)
@lru_cache(2)
def score_source(i):
 # A broad, fixed 1.8 dB recess gives diction space without pumping the whole orchestra.
 a=amp(-1.8/2);ww=2*np.pi*2250/sr;aa=np.sin(ww)/(2*.79)
 bb=np.array([1+aa*a,-2*np.cos(ww),1-aa*a]);dd=np.array([1+aa/a,-2*np.cos(ww),1-aa/a])
 return lfilter(bb,dd,mus(i),axis=0).astype('f4')
def music_power(x):
 # One tenth-second point, expressed per stereo channel, measured from the actual take.
 hop=4800;sub=np.mean(x[::8]**2,axis=1)
 y=np.pad(sub,(0,(-len(sub))%(hop//8)),mode='edge')
 return y.reshape(-1,hop//8).mean(1)
def cue_plan():
 cs=layout()
 for c in cs:
  a,e,p=[round(c[k]*sr)for k in ('start','end','source')];song=score_source(c['i'])
  if not 0<=p<p+e-a<=len(song):raise ValueError(f"{c['title']}: recording does not cover edit")
  x=song[p:p+e-a];power=music_power(x)
  # A slow, bounded phrase ride, not syllabic compression. Keep the natural last note.
  broad=db(gaussian_filter1d(power,25.,mode='nearest'))
  middle=float(np.median(broad));c['_gain_db']=c['target_db']-middle+np.clip(.38*(middle-broad),-3.3,4.1)
  c.update(a=a,b=e,p=p)
 return cs
def cues():return cue_plan()
def locked_voice(path):
 tmp=path.with_name(path.stem+'.part.wav')
 with sf.SoundFile(tmp,'w',samplerate=sr,channels=1,subtype='PCM_24')as dry:
  for k,d in S.items():
   y,rr=sf.read(W/'scenes'/(k+'.wav'),dtype='f4');assert rr==44100
   v=(resample_poly(y,160,147)*.962).astype('f4');assert len(v)==d['frames']*1600;dry.write(v)
 tmp.replace(path)
def voice_rider(path,frames):
 rows=[]
 with sf.SoundFile(path)as f:
  if f.channels!=1 or f.samplerate!=sr or len(f)!=frames:raise ValueError('Dry master is not on the film clock')
  for y in f.blocks(blocksize=480*800,dtype='f4'):
   z=np.pad(y,(0,(-len(y))%480)).reshape(-1,480);rows.append(np.sqrt(np.mean(z*z,axis=1)))
 lev=np.concatenate(rows)
 # Bridge little breaths; even full voice changes the music level by only two decibels.
 act=gaussian_filter1d(maximum_filter1d(np.clip((lev-.012)/.062,0,1),size=67),27,mode='nearest')
 return -2.*act
def stage(root=None,dry=None,proof=False):
 dest=Path(root) if root else W;dest.mkdir(parents=True,exist_ok=True);(dest/'audio').mkdir(exist_ok=True)
 if dry is None:
  dry=dest/'master-dry.wav';locked_voice(dry)
 dry=Path(dry);nn=round(TOTAL*sr);ride=voice_rider(dry,nn);cs=cue_plan()
 beats=[]
 for k,d in S.items():
  for q in d['questions']:
   end=starts[k]+q['time'];beats.append(dict(id=k,take=q['take'],q=end,next=starts[k]+q['next'],tap=end+.143))
 b=bell();qa=[];meter=[];part=dest/'master-mix.part.wav';dst=dest/'master-mix.wav'
 arc=starts['6-1']+clock('6-1').at('填好第四张')+.36
 with sf.SoundFile(dry) as rd,sf.SoundFile(part,'w',samplerate=sr,channels=2,subtype='PCM_24')as wr:
  for n0 in range(0,nn,6*sr):
   n=min(nn-n0,6*sr);ticks=n0+np.arange(n);t=ticks/sr;v=rd.read(n,dtype='f4')
   bed=np.zeros((n,2),'f4')
   for c in cs:
    a,e,p,i=[c[k] for k in ('a','b','p','i')];l=max(n0,a);h=min(n0+n,e)
    if l>=h:continue
    jj=np.arange(l-a,h-a);x=jj/sr;fin=c['fade_in'];fout=c['fade_out']
    # Adjacent entries share the actual same interval. cos²+sin² = 1 in power.
    env=np.sin(np.minimum(1,x/fin)*np.pi/2)*np.sin(np.minimum(1,(e-a-jj)/(sr*fout))*np.pi/2)
    g=amp(np.interp(x*10,np.arange(len(c['_gain_db'])),c['_gain_db']))
    bed[l-n0:h-n0]+=score_source(i)[p+l-a:p+h-a]*(env*g)[:,None]
   gain=np.interp(ticks/480,np.arange(len(ride)),ride)
   # The audience gets time to think; the underlying string resonance stays present.
   gain-=1.8*soft((t-arc+.36)/.65)*(1-soft((t-arc-2.1)/.85))
   sfx=np.zeros(n,'f4')
   for hit in beats:
    q=hit['q'];pos=round(hit['tap']*sr)-n0
    if q<t[0]-2.8 or q>t[-1]+.7:continue
    gain-=2.9*soft((t-q+.35)/.40)*(1-soft((t-min(hit['next']-.11,q+.75))/1.02))
    lo=max(0,pos);hi=min(n,pos+len(b))
    if hi>lo:sfx[lo:hi]+=b[lo-pos:hi-pos]*.259
   bed*=amp(gain).astype('f4')[:,None]
   mix=v[:,None]+bed+sfx[:,None];peaks=np.abs(mix)>.855
   mix[peaks]=np.sign(mix[peaks])*(.855+.063*np.tanh((np.abs(mix[peaks])-.855)/.063))
   wr.write(mix)
   if proof:
    # Actual music after all faders. True quiet at the final decay is kept, not artificially filled.
    for i0 in range(0,n,sr//2):
     z=bed[i0:i0+sr//2:4]
     meter.append(round(float(db(np.mean(z**2))),3))
   # Measure the central portion of the original cue with a sample-weighted range across chunk boundaries.
   for hit in beats:
    p=round(hit['tap']*sr)+int(.010*sr);e0=p+int(.145*sr);lo=max(n0,p);hi=min(n0+n,e0)
    if hi>lo:
     z=slice(lo-n0,hi-n0);qa.append((hit['id'],hi-lo,float(np.mean(bed[z]**2)),float(np.mean(sfx[z]**2)),float(np.mean(v[z]**2))))
 assert sf.info(part).frames==nn
 part.replace(dst)
 def hit_stat(h):
  sel=[q for q in qa if q[0]==h['id']];n=sum(x[1]for x in sel)
  assert n==int(.145*sr)
  vals=[round(float(db(sum(x[1]*x[j] for x in sel)/n)),2) for j in (2,3,4)]
  return dict(id=h['id'],take=h['take'],time=h['q'],gap=h['next']-h['q'],music_rms=vals[0],tone_rms=vals[1],voice_tail_rms=vals[2])
 meta=dict(edition='v3.1-continuous',sources=FILES,cues=[{k:v for k,v in c.items() if k not in ('_gain_db','a','b','p')} for c in cs],questions=beats,sfx=dict(track=NAMES[0],time=5.531,length=len(b)/sr,processing='upper harmonics, small transposition, decay'),stats=[hit_stat(h)for h in beats])
 f=dest/'audio/cuebook.json';tmp=f.with_suffix('.tmp');tmp.write_text(json.dumps(meta,ensure_ascii=False,indent=2));tmp.replace(f)
 if proof:np.save(dest/'music-half-seconds.npy',np.array(meter))
 print('Continuous score:',len(cs),'passages;',nn,'stereo samples;',len(beats),'question strikes.',flush=True)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path);ap.add_argument('--dry',type=Path);ap.add_argument('--proof',action='store_true');opt=ap.parse_args();stage(opt.root,opt.dry,opt.proof)
