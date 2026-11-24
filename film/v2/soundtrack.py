"""New cue arrangement of the original score, mixed for spoken English."""
import json,sys
from pathlib import Path
import numpy as np
import soundfile as sf
from scipy.ndimage import gaussian_filter1d
from scipy.signal import resample_poly
R=Path(__file__).resolve().parent
sys.path.append(str(R.parent))
from score import master_score,add,SR,F
rows=json.loads((R/'timeline.json').read_text())
bed=master_score(rows)
# Three short physical landmark motifs, composed for this spatial version.
for ident,note in (('1-03',67),('2-05',69),('3-07',62),('4-04',65)):
    q=next(x for x in rows if x['id']==ident)
    start=q['start']/30
    at=start+min(.7,q['duration']*.05)
    add(bed,at,'glass',note,2.0,.044,-.25)
    add(bed,at+.25,'felt',note-7,2.1,.031,.24)
sf.write(R/'score_original.wav',bed,SR,subtype='PCM_16')
x,rate=sf.read(R/'dry.wav',dtype='float32')
assert rate==24000 and len(x)*2==len(bed)
z=x.reshape(-1,240)
eng=gaussian_filter1d(np.clip((np.sqrt(np.mean(z**2,axis=1))-.004)/.038,0,1),14)
dyn=(.49-.27*eng).astype(F)
narration=resample_poly(x,2,1).astype(F)*.99
# Chunk the envelope projection so that the 20-minute WAV stays inexpensive.
for k in range(0,len(bed),SR*25):
    j=min(k+SR*25,len(bed)); ii=np.arange(k,j,dtype=np.float64)/480
    gain=np.interp(ii,np.arange(len(dyn),dtype=F),dyn).astype(F)
    bed[k:j,:]*=gain[:,None]
    bed[k:j,:]+=narration[k:j,None]
peak=float(np.max(np.abs(bed)))
if peak>.86: bed*=.86/peak
sf.write(R/'mix.wav',bed,SR,subtype='PCM_24')
print(f'Original score, English voice, peak {float(np.max(np.abs(bed))):.3f}')
