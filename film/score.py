"""四格之外 — original instrumental score. Notes, synthesis and soundtrack mix."""
import json,math,subprocess
from pathlib import Path
from functools import lru_cache
import numpy as np
import soundfile as sf
from scipy.ndimage import uniform_filter1d,gaussian_filter1d
from scipy.signal import resample_poly,butter,sosfilt
R=Path(__file__).resolve().parent
SR=48000
T=1200
F=np.float32
CHORDS=[
 # (bass, inside voices); score begins in D, then common tones keep the transitions soft.
 [(38,(53,57,60,64)),(34,(53,57,60,62)),(41,(53,55,57,62)),(36,(52,55,57,62)),
  (38,(53,57,59,64)),(43,(53,57,58,62)),(40,(52,55,57,62)),(45,(52,55,59,64))],
 [(41,(53,57,60,64)),(36,(52,55,60,62)),(38,(53,57,60,64)),(34,(53,57,60,62)),
  (43,(53,57,58,62)),(36,(52,55,57,62)),(41,(53,57,60,67)),(45,(52,55,59,64))],
 [(38,(53,57,59,64)),(41,(53,57,62,64)),(43,(55,57,59,62)),(36,(52,55,57,62)),
  (38,(53,57,60,64)),(33,(52,55,57,59)),(36,(52,55,57,62)),(45,(55,57,59,64))],
 [(34,(53,57,60,62)),(41,(53,57,62,64)),(36,(52,55,57,62)),(38,(53,57,59,64)),
  (43,(53,57,58,62)),(34,(53,57,60,62)),(45,(52,55,59,64)),(38,(53,57,64,69))]
]
BPM=[67,74,78,64]
# The two model voices answer one another even when they disagree. The coda
# plays the incomplete four-note cell once more, then gives its final D.
MOTIF_CORE=(65,69,64,67)
PATTERNS=(
 ((.0,0,.9), (1.7,2,.46), (3.18,1,.49)),
 ((.52,1,.59), (2.15,3,.60)),
 ((.00,0,.78), (1.38,2,.50), (2.78,3,.48)),
 ((.56,3,.53), (2.52,1,.52)),
)
RNG=np.random.default_rng(33612)
def freq(note):return 440*2**((note-69)/12)
@lru_cache(256)
def note(instrument,midi,durkey):
    dur=durkey/100
    t=np.linspace(0,dur,round(dur*SR),endpoint=False,dtype=np.float32)
    ff=freq(midi); phase=np.float32(math.tau*ff)*t
    if instrument=='felt':
        env=(1-np.exp(-t*144))*(.66*np.exp(-t/1.18)+.34*np.exp(-t/.31))
        h=np.sin(phase)+.50*np.sin(phase*1.0026+.11)+.17*np.sin(phase*2.002)*np.exp(-t/.68)+.08*np.sin(phase*3.015+.48)*np.exp(-t/.27)
        h+=.045*np.sin(phase*5.02)*np.exp(-t/.10)
        v=h*env*.64
    elif instrument=='glass':
        env=(1-np.exp(-t*173))*(.22*np.exp(-t/.85)+.78*np.exp(-t/.24))
        h=np.sin(phase)+.18*np.sin(phase*2.018+.27)+.11*np.sin(phase*3.983-.15)*np.exp(-t/.32)
        v=h*env*.91
    elif instrument=='cello':
        env=np.minimum(1,t/.9)**1.8*np.minimum(1,(dur-t)/1.28)**1.65
        q=phase+.10*np.sin(2*np.pi*4.3*t)+.024*np.sin(2*np.pi*.65*t)
        h=np.sin(q)+.39*np.sin(2*q+.45)+.125*np.sin(3*q-.4)+.04*np.sin(4*q+.1)
        v=h*env*.67
    else:
        env=(1-np.exp(-t*19))*np.exp(-t/.88)*np.minimum(1,(dur-t)/.29)
        v=(np.sin(phase)+.26*np.sin(2*phase+.2))*env*.74
    ending=min(round(SR*.085),len(v))
    v[-ending:]*=np.linspace(1,0,ending,dtype=F)
    v.flags.writeable=False
    return v.astype(F,copy=False)
def add(y,start,instr,midi,dur,amp,pan):
    if start<0:return
    i=round(start*SR);n=min(len(y)-i,round(dur*SR))
    if n<=0:return
    snd=note(instr,midi,round(dur*100))[:n]
    n=len(snd)
    y[i:i+n,0]+=snd*(amp*math.cos((pan+1)*math.pi/4))
    y[i:i+n,1]+=snd*(amp*math.sin((pan+1)*math.pi/4))
def section(y,start,end,act):
    beat=60/BPM[act]; bsz=4*beat
    stage=CHORDS[act]
    for bar in range(math.ceil((end-start)/bsz)):
        at=start+bar*bsz
        if at+1.5>end:break
        b,vo=stage[bar%len(stage)]
        fade=min(1,(at-start+6)/10,(end-at)/8)
        phrase=bar//8; order=(bar+act)%4
        space=0.67+.23*math.sin(bar*.29+.42*act)+.09*math.sin(bar*.09)
        z=fade*space
        if bar%2==0:
            add(y,at,'cello',b,7.45*beat,.058*z,-.06)
            if act in (2,3) or phrase%3==1:
                add(y,at+.85,'cello',vo[2]-12,5.7*beat,.022*z,.32)
        if bar%8 not in (3,7):
            add(y,at+RNG.uniform(0,.027),'bass',b+12,2.06*beat,.075*z,-.16)
        if bar%8 in (0,4) and phrase%3!=2:
            for j,q in enumerate(vo[:3]):
                add(y,at+.58*beat+j*.031,'felt',q,3.2*beat,(.038-j*.004)*z,(-.38,.12,.29)[j])
        elif bar%8 in (1,3,6):
            for j,q in enumerate((vo[0],vo[2])):
                add(y,at+(1.15+.94*j)*beat,'felt',q,2.35*beat,(.036-.009*j)*z,(-.26,.18)[j])
        if bar%8 in (2,5,6) or (act==2 and bar%8 in (1,4)):
            for k,(atb,voice,amp) in enumerate(PATTERNS[order]):
                transpose=12 if (act==2 and k==1 and bar%4==3) else 0
                add(y,at+atb*beat+RNG.uniform(-.016,.03),'glass' if (k+act)%3==0 else 'felt',
                   vo[voice]+transpose,(1.8-.21*k)*beat,.084*amp*z, -.38 if k%2==0 else .32)
        if bar%8==7:
            for k, q in ((0,vo[0]),(1,vo[1])):
                add(y,at+(k*.32+.15)*beat,'felt',q,2.14*beat,.039*z,(-.29,.26)[k])
def master_score(rows):
    y=np.zeros((T*SR,2),dtype=F)
    begins=[next(r['start']/30 for r in rows if r['act']==x) for x in range(1,5)]
    starts=[12.5]+begins[1:]
    tails=begins[1:]+[1182.2]
    for a,(start,end) in enumerate(zip(starts,tails)):section(y,start,end,a)
    # cold-open pencil marks and the moment the wrong answer appears
    add(y,.40,'felt',53,2.7,.086,-.24); add(y,2.94,'glass',65,1.42,.037,-.28)
    add(y,5.47,'felt',57,2.48,.080,.18); add(y,7.43,'felt',64,2.4,.063,.32)
    add(y,9.70,'cello',38,5.2,.053,.0)
    for i,t in enumerate(begins[1:],1):
        add(y,t-.14,'felt',(60,62,65)[i-1],2.38,.056,-.24)
        add(y,t+.54,'glass',(67,69,72)[i-1],1.84,.044,.28)
    # Coda mirrors the four opening tones without a hard music cut.
    for i,q in enumerate(MOTIF_CORE):
        add(y,1182.65+2.64*i,'felt',q,4.1,.073, (-.34,.27,-.20,.19)[i])
    add(y,1193.86,'felt',62,5.85,.090,-.11)
    add(y,1194.10,'felt',69,5.55,.040,.22)
    add(y,1192.25,'cello',38,6.3,.052,0.)
    # Short stereo room image. The taps use the dry signal, not recursive feedback.
    rv=np.zeros_like(y)
    for ms,l,r,cross in ((71,.114,.092,False),(113,.073,.096,True),(181,.049,.043,False),(239,.036,.033,True),(326,.027,.032,True),(467,.016,.013,False)):
        k=round(ms*SR/1000)
        rv[k:,0]+=l*y[:-k,int(cross)]
        rv[k:,1]+=r*y[:-k,1-int(cross)]
    y+=rv
    y[-SR*3:]*=np.linspace(1,0,SR*3,dtype=F)[:,None]
    return y
def mix(y):
    audio,sr=sf.read(R/'voice_master.wav',dtype='float32')
    assert sr==24000 and len(audio)==T*sr and y.shape==(T*SR,2)
    # Very gentle depth ducking, keyed to speech activity rather than a beat grid.
    blocks=audio.reshape(-1,240)
    rms=np.sqrt((blocks*blocks).mean(axis=1))
    env=gaussian_filter1d(np.clip((rms-.003)/.037,0,1),sigma=13)
    gain_curve=.56-.31*env
    music_gain=np.interp(np.arange(T*SR,dtype=F)/F(480),np.arange(len(env),dtype=F),gain_curve).astype(F)
    voice=resample_poly(audio,2,1).astype(F)
    voice*=.80
    for k in range(2):
        y[:,k]*=music_gain
        y[:,k]+=voice
    y*=10**(2.15/20)
    maxp=np.max(np.abs(y))
    if maxp>.91:y*=.91/maxp
    sf.write(R/'mixed.wav',y,SR,'PCM_24')
    print(f'original score + narration, peak {float(np.max(np.abs(y))):.3f}, RMS {float(np.sqrt(np.mean(y*y))):.4f}',flush=True)

if __name__=='__main__':
    rows=json.loads((R/'timeline.json').read_text())
    s=master_score(rows)
    # Score lives with the source; the finished video uses the ducked variation under speech.
    sf.write(R/'score_original.wav',s,SR,'PCM_16')
    mix(s)
