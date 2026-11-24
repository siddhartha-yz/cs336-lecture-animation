"""The same 45 UTF-8 bytes, scored using each model's native byte-level BPE."""
import json, math
from pathlib import Path
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
D=Path(__file__).resolve().parent
torch.set_num_threads(5)
TEXT=' Byte-level tokenizers encode naïve strings.'
PREFIX='Text:'
# canonical byte-level fallback: map the unused bytes above Latin-1
existing=list(range(33,127))+list(range(161,173))+list(range(174,256))
initial=existing.copy();n=0
for b in range(256):
    if b not in initial: existing.append(b);n+=1
lookup={chr(u):b for u,b in zip(initial+list(range(256,256+n)),existing)}
results=[]
for model,label,path in [('openai-community/gpt2','GPT-2',D/'gpt2'),
                          ('HuggingFaceTB/SmolLM2-135M','SmolLM2',D.parent.parent/'beats_next'/'data'/'smollm2')]:
    tok=AutoTokenizer.from_pretrained(path,local_files_only=True)
    m=AutoModelForCausalLM.from_pretrained(path,local_files_only=True,dtype=torch.float32).eval()
    prefix=tok.encode(PREFIX,add_special_tokens=False)
    full=tok.encode(PREFIX+TEXT,add_special_tokens=False)
    assert full[:len(prefix)]==prefix
    ids=full[len(prefix):];raw=[bytes(lookup[c] for c in w) for w in tok.convert_ids_to_tokens(ids)]
    assert b''.join(raw)==TEXT.encode()
    with torch.inference_mode():
        logprobs=m(torch.tensor([full])).logits[0,len(prefix)-1:-1].double().log_softmax(-1)
    bits=[-logprobs[j,w].item()/math.log(2) for j,w in enumerate(ids)]
    results.append(dict(model=model,label=label,raw_tokens=[t.decode() for t in raw],
                        boundaries=[0]+[len(b''.join(raw[:i])) for i in range(1,len(ids)+1)],
                        bits=bits,ppl=2**(sum(bits)/len(ids)),bpb=sum(bits)/len(TEXT.encode())))
    print(label,len(ids),sum(bits),results[-1]['ppl'],results[-1]['bpb'],flush=True)
(D/'tokenizers.json').write_text(json.dumps(dict(text=TEXT,prefix=PREFIX,bytes=len(TEXT.encode()),equal_loss_bits=89,models=results),ensure_ascii=False,indent=2)+'\n')
