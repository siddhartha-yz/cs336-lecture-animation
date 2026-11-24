"""Native-English performance, a continuous take for each camera passage."""
import os,argparse,json,time,re,sys
from pathlib import Path
os.environ['HF_HUB_OFFLINE']='1';os.environ['TOKENIZERS_PARALLELISM']='false'
import torch,soundfile as sf,numpy as np
from faster_qwen3_tts import FasterQwen3TTS
R=Path(__file__).resolve().parent
MODEL=Path(os.environ["QWEN_TTS_MODEL"])
p=argparse.ArgumentParser();p.add_argument('acts',nargs='*',type=int,default=[1,2,3,4]);p.add_argument('--only',nargs='+');p.add_argument('--take',type=int,default=0);a=p.parse_args()
torch.set_num_threads(4)
m=FasterQwen3TTS.from_pretrained(str(MODEL),device='cuda:0',dtype=torch.bfloat16,attn_implementation='sdpa',local_files_only=True)
base="American English. A curious, warm math professor talking to a student at a blackboard. Conversational and alert, with natural breaths. Take just enough time to let important ideas land. Emphasize surprising contrasts, not every word. An easy, resonant speaking voice."
out=R/'voice';out.mkdir(exist_ok=True)
def pronunciation(s):
    for key,val in [('MMLU-Pro','M M L U Pro'),('MMLU','M M L U'),('GPQA','G P Q A'),('HLE','H L E'),('SWE-bench','S W E Bench'),('pass@k','pass at K'),('pass@2','pass at two'),('pass@1','pass at one'),('ARC-AGI','Arc A G I'),('LiveCodeBench','Live Code Bench'),('GPT-2','G P T two'),('AlpacaEval','Alpaca Eval'),('GDPval','G D P Val'),('MedHELM','Med Helm'),('HarmBench','Harm Bench'),('PPL','perplexity')]:
        s=re.sub(r'(?<![A-Za-z])'+re.escape(key)+r'(?![A-Za-z])',val,s)
    return s
for act in a.acts:
    for j,r in enumerate(json.loads((R/f'act{act}.json').read_text())):
        ident=f'{act}-{j:02d}'
        if a.only and ident not in a.only:continue
        text=pronunciation(r.get('spoken',' '.join(z[0].strip() for z in r['parts'])))
        mode=r.get('delivery','')
        if ident=='1-00':mode+=" Start focused, a quick flash of amusement at the wrong answer, and then a genuinely curious question."
        payload={'text':text,'delivery':mode,'take':a.take,'speaker':'Ryan'}
        fp=out/f'{ident}.wav';meta=fp.with_suffix('.json')
        if fp.exists() and meta.exists() and json.loads(meta.read_text())==payload:continue
        torch.manual_seed(681+act*97+j+1500*a.take)
        st=time.monotonic()
        w,sr=m.generate_custom_voice(text=text,speaker='Ryan',language='English',instruct=base+' '+mode,max_new_tokens=1150,temperature=.73,repetition_penalty=1.065)
        x=np.asarray(w[0],dtype='float32')
        ii=np.flatnonzero(np.abs(x)>.006)
        if not len(ii):raise RuntimeError('No speech in '+ident)
        x=x[max(0,ii[0]-round(.085*sr)):min(len(x),ii[-1]+round(.14*sr))]
        sf.write(fp.with_suffix('.tmp.wav'),x,sr,subtype='PCM_24');fp.with_suffix('.tmp.wav').replace(fp)
        meta.write_text(json.dumps(payload,ensure_ascii=False))
        print(f'{ident} {len(x)/sr:5.2f}s in {time.monotonic()-st:5.2f}s · {text[:82]}',flush=True)
