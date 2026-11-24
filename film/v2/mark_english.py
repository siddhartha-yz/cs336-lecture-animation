"""Align the spoken English take to its authored bilingual phrase pairs."""
from pathlib import Path
import argparse,json,time
import soundfile as sf,numpy as np
from scipy.signal import resample_poly
from faster_whisper import WhisperModel
R=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--device',default='cpu');p.add_argument('--only',nargs='+');p.add_argument('--watch',action='store_true');a=p.parse_args()
m=WhisperModel(str(R.parent/'asr_model'),device=a.device,compute_type='float16' if a.device=='cuda' else 'int8',cpu_threads=7,local_files_only=True)
d=R/'marks';d.mkdir(exist_ok=True)
while True:
 pending=0
 allids=[f'{j}-{i:02d}' for j in range(1,5) for i in range(len(json.loads((R/f'act{j}.json').read_text())))]
 for key in allids:
    if a.only and key not in a.only:continue
    f=R/'voice'/f'{key}.wav'; dest=d/f'{key}.json'
    if not f.exists():pending+=1;continue
    if dest.exists() and dest.stat().st_mtime>=f.stat().st_mtime:continue
    st=time.monotonic()
    x,sr=sf.read(f,dtype='float32')
    x=resample_poly(x,16000,sr).astype('float32')
    rs,_=m.transcribe(x,language='en',task='transcribe',word_timestamps=True,beam_size=2,condition_on_previous_text=False,no_repeat_ngram_size=5,
                      initial_prompt='A lecture about language-model evaluation. Perplexity, MMLU-Pro, GPQA, AlpacaEval, SWE-bench, ARC-AGI, HarmBench, LiveCodeBench, GDPval, MedHELM.')
    rs=list(rs);words=[dict(start=w.start,end=w.end,word=w.word) for s in rs for w in (s.words or [])]
    tx=''.join(s.text for s in rs)
    tmp=dest.with_suffix('.tmp');tmp.write_text(json.dumps(dict(words=words,heard=tx,duration=len(x)/16000),ensure_ascii=False));tmp.replace(dest)
    print(f'{key} in {time.monotonic()-st:.1f}s · {tx}',flush=True)
 if not a.watch or not pending:break
 time.sleep(4)
