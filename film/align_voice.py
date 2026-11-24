"""Analyze the actual spoken takes to align subtitles and locate any take that needs repair."""
import argparse,json,os,time,re
from pathlib import Path
from faster_whisper import WhisperModel
from opencc import OpenCC
import soundfile as sf
from scipy.signal import resample_poly
os.environ['HF_HUB_OFFLINE']='1'
C=OpenCC('t2s')
R=Path(__file__).resolve().parent
S=Path.home()/'.cache/huggingface/hub/models--Systran--faster-whisper-large-v3/snapshots'
M=R/'asr_model'
p=argparse.ArgumentParser()
p.add_argument('--watch',action='store_true')
p.add_argument('--beams',type=int,default=3)
p.add_argument('--only',nargs='+')
a=p.parse_args()
model=WhisperModel(str(M),device='cpu',compute_type='int8',cpu_threads=8,local_files_only=True)
out=R/'voice_marks';out.mkdir(exist_ok=True)
def transcribe(f,t):
    st=time.monotonic()
    samples,sr=sf.read(f,dtype="float32")
    samples=resample_poly(samples,16000,sr).astype("float32")
    segments, info=model.transcribe(samples,language='zh',task='transcribe',beam_size=a.beams,no_repeat_ngram_size=5,
            word_timestamps=True,condition_on_previous_text=False,
            vad_filter=False,temperature=0.0,
            initial_prompt='语言模型评估。困惑度，词元，脚手架。')
    segments=list(segments)
    words=[dict(start=w.start,end=w.end,word=C.convert(w.word),p=round(w.probability,3)) for s in segments for w in (s.words or [])]
    t.write_text(json.dumps(dict(duration=info.duration,words=words,heard=C.convert(''.join(s.text for s in segments))),ensure_ascii=False),encoding='utf-8')
    print(f'{f.stem} {info.duration:.2f}s in {time.monotonic()-st:.1f}s: '+''.join(s.text for s in segments),flush=True)
def jobs():
    voices=R/'voice'
    expected=[]
    for a in range(1,5):
        expected.extend([f'{a}-{j:02d}' for j in range(len(json.loads((R/f'act{a}.json').read_text())))])
    return [(voices/f'{e}.wav',out/f'{e}.json') for e in expected]
while True:
    pending=0
    for f,t in jobs():
        if a.only and f.stem not in a.only:continue
        if f.exists():
            if not t.exists() or t.stat().st_mtime<f.stat().st_mtime:transcribe(f,t)
        else:pending+=1
    if not a.watch or not pending:break
    time.sleep(2)
