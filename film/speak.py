"""Offline performance of the original Mandarin script; one continuous take per beat."""
import os,argparse,json,time,sys,re
from pathlib import Path
os.environ['HF_HUB_OFFLINE']='1'
os.environ['TOKENIZERS_PARALLELISM']='false'
import torch
import soundfile as sf
import numpy as np
from qwen_tts import Qwen3TTSModel
R=Path(__file__).resolve().parent
M=Path(os.environ["QWEN_TTS_MODEL"])
p=argparse.ArgumentParser()
p.add_argument('acts',nargs='*',type=int,default=[1,2,3,4])
p.add_argument('--sample',action='store_true')
p.add_argument('--fast',action='store_true')
p.add_argument('--only',nargs='+')
p.add_argument('--speaker',default='Dylan')
a=p.parse_args()
torch.set_num_threads(5)
print(torch.__version__,torch.cuda.get_device_name(),flush=True)
if a.fast:
    from faster_qwen3_tts import FasterQwen3TTS
    mdl=FasterQwen3TTS.from_pretrained(str(M),device='cuda:0',dtype=torch.bfloat16,attn_implementation='sdpa',local_files_only=True)
else:
    mdl=Qwen3TTSModel.from_pretrained(str(M),device_map='cuda:0',dtype=torch.bfloat16,attn_implementation='sdpa')
base='用标准普通话，像一位生动的青年大学老师在黑板前跟学生交谈。吐字清楚，情绪从容有变化，轻重分明。短停顿自然，问句像真在问学生，关键处放慢，铺垫利落。'
def voice(text,mode='',speaker=None,seed=201):
    torch.manual_seed(seed)
    st=time.monotonic()
    n=len(re.findall(r'[\w]',text))
    wavs,sr=mdl.generate_custom_voice(text=text,language='Chinese',speaker=speaker or a.speaker,
        instruct=base+mode, max_new_tokens=max(520, min(1500, 5*n+250)),do_sample=True,temperature=.72)
    x=wavs[0].astype('float32')
    active=np.flatnonzero(np.abs(x)>.005)
    if len(active):
        x=x[max(0,active[0]-int(sr*.085)):min(len(x),active[-1]+int(sr*.135))]
    if not len(x): raise RuntimeError('Empty audio')
    print(f'{len(x)/sr:5.2f}s, generated in {time.monotonic()-st:5.2f}s, {text[:35]}',flush=True)
    return x,sr
if a.sample:
    s=R/'voice_samples';s.mkdir(exist_ok=True)
    for j,spk in enumerate(('Dylan','Uncle_Fu')):
        parts=json.loads((R/'act1.json').read_text())
        for k in (0,3):
            x,sr=voice(parts[k]['text'],'开头有点诧异、收住，最后一句真正问出去。' if k==0 else '说得像用手指给学生指一幅图。',spk,221+k)
            sf.write(s/f'{spk}-{k}.wav',x,sr)
    sys.exit(0)
out=R/'voice';out.mkdir(exist_ok=True)
for ac in a.acts:
    for k,b in enumerate(json.loads((R/f'act{ac}.json').read_text())):
        ident=f'{ac}-{k:02d}'
        if a.only and ident not in a.only:continue
        text=b.get('spoken',b['text'])
        if text==b['text']:
            for old,new in (('MMLU-Pro','M M L U Pro'),('MMLU','M M L U'),('GPQA','G P Q A'),('AlpacaEval','Alpaca Eval')):
                text=text.replace(old,new)
        extra=b.get('delivery', ('先压低再抛出问句，像看到了反常结果。' if ac==1 and k==0 else ''))
        wav=out/f'{ident}.wav'; meta=out/f'{ident}.json'
        payload=dict(text=text,speaker=a.speaker,delivery=extra)
        if wav.exists() and meta.exists() and json.loads(meta.read_text())==payload:continue
        print(ident, end=' ',flush=True)
        x,sr=voice(text,extra,seed=300+ac*43+k)
        sf.write(wav.with_suffix('.tmp.wav'),x,sr,subtype='PCM_24')
        wav.with_suffix('.tmp.wav').replace(wav)
        meta.write_text(json.dumps(payload,ensure_ascii=False),encoding='utf-8')
