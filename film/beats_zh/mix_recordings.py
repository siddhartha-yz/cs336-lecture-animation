"""Edit cue-sheet recordings against the locked narration; keep the diagram's rests."""
from pathlib import Path
import json
import subprocess
import numpy as np
import soundfile as sf
from scipy.ndimage import gaussian_filter1d,maximum_filter1d
from scipy.signal import resample_poly,sosfiltfilt,butter

R=Path(__file__).resolve().parent
S=48000
voice,rate=sf.read(R/'audio'/'dry.wav',dtype='float32')
assert rate==24000
speech=resample_poly(voice,2,1)
n=len(speech)
rows={r['id']:r for r in json.loads((R/'timeline.json').read_text())}
bed=np.zeros((n,2),np.float32)
q=json.loads((R/'music'/'cueplan.json').read_text())
one=rows['e']; end=n/S
h0,h1=one['pause_at']
abs0,abs1=one['start']/30+h0,one['start']/30+h1
# The score follows the two cuts of thought, not the English speech clock.
q[0]['end']=rows['b']['end']/30-2.14
q[1]['begin']=rows['b']['end']/30-.38
q[1]['end']=abs0+.075
q[2]['begin']=abs1+.075
q[2]['end']=end-.16
(R/'music'/'fitted.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
for cue in q:
    title=cue['title']
    a,b=cue['begin'],cue['end']
    sec=b-a
    sr0=cue['in']
    f=R/'music'/cue['file']
    assert 0<=a<b<=n/S+1/S and f.is_file()
    raw=subprocess.check_output(['ffmpeg','-nostdin','-v','error','-ss',str(sr0),'-i',str(f),
                                '-t',str(sec),'-f','f32le','-ar',str(S),'-ac','2','-'])
    decoded=np.frombuffer(raw,np.float32).reshape(-1,2)
    assert len(decoded)/S>=sec-.05,(title,len(decoded)/S,sec)
    hi=sosfiltfilt(butter(2,61,fs=S,output='sos',btype='highpass'),decoded,axis=0).astype('float32')
    level=np.sqrt(np.mean(hi*hi))
    x=hi*float((10**(cue.get('rms_db',-28.0)/20))/level)
    na,nb=(int(S*cue.get(k,v)) for k,v in [('fade_in',.60),('fade_out',1.20)])
    if na:x[:na]*=np.sin(np.linspace(0,np.pi*.5,na,dtype='float32'))[:,None]**2
    if nb:x[-nb:]*=np.sin(np.linspace(np.pi*.5,0,nb,dtype='float32'))[:,None]**2
    i=round(a*S)
    cap=min(n-i,len(x))
    bed[i:i+cap]+=x[:cap]
    print(title,f'{a:.2f}→{b:.2f}s, source +{sr0:.2f}s')

# The entry of each voice phrase ducks the cue, but leave room to hear its
# transient and harmony between phrases. Do not write any new phonemes.
block=S//100
p=np.pad(speech,(0,(-len(speech))%block)).reshape(-1,block)
rms=np.sqrt(np.mean(p*p,axis=1))
act=np.clip((rms-.007)/.068,0,1)
act=gaussian_filter1d(maximum_filter1d(act,size=17),9)
gain=np.interp(np.arange(n)/block,np.arange(len(act)),1-.66*act).astype('float32')
bed*=gain[:,None]

def hush(a,b,fade=.19):
    lo,hi=round(a*S),round(b*S)
    z=round(fade*S)
    bed[lo-z:lo]*=np.linspace(1,0,z,dtype='float32')[:,None]
    bed[lo:hi]=0
    bed[hi:hi+z]*=np.linspace(0,1,z,dtype='float32')[:,None]
for r in rows.values():
    if r.get('pause_at'):
        offset=r['start']/30
        a,b=r['pause_at']
        hush(a+offset,b+offset)
mix=bed+speech[:,None]
peak=np.max(np.abs(mix))
if peak>.91: mix*=.91/peak
sf.write(R/'music'/'bed.wav',bed,S,'PCM_16')
sf.write(R/'audio'/'mix.wav',mix,S,'PCM_24')
print(f'mix peak {20*np.log10(np.max(np.abs(mix))):.1f} dBFS')
