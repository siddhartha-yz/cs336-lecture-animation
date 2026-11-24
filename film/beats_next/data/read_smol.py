"""Read next-token probabilities from pinned local official base SmolLM2-135M weights."""
import json, math
from pathlib import Path
import torch
from transformers import AutoModelForCausalLM,AutoTokenizer
R=Path(__file__).resolve().parent
torch.set_num_threads(4)
model_dir=R/'smollm2'
m=AutoModelForCausalLM.from_pretrained(str(model_dir),local_files_only=True,dtype=torch.float32).eval()
t=AutoTokenizer.from_pretrained(str(model_dir),local_files_only=True)
prefix="The room was quiet."
text=" The small cat sat on the mat."
base=t.encode(prefix,add_special_tokens=False)
full=t.encode(prefix+text,add_special_tokens=False)
assert full[:len(base)]==base
tokens=full[len(base):]
assert len(tokens)==8,(tokens,[t.decode(i) for i in tokens])
with torch.no_grad():
    y=m(torch.tensor([full])).logits[0]
probs=[];others=[]
for j,k in enumerate(tokens):
    q=y[len(base)+j-1].double().softmax(-1)
    assert math.isclose(q.sum().item(),1,abs_tol=1e-10)
    probs.append(q[k].item())
    selected=[]
    for i in q.topk(8).indices.tolist():
        w=t.decode(i).strip()
        if i==k or not w or not w.isprintable() or w.startswith('<|') or any(a['token']==w for a in selected): continue
        selected.append(dict(token=w,p=q[i].item()))
        if len(selected)==3:break
    others.append(selected)
p=dict(model="HuggingFaceTB/SmolLM2-135M",source="https://huggingface.co/HuggingFaceTB/SmolLM2-135M",
    prefix=prefix,text=text,tokens=[t.decode(i).strip() or '␠' for i in tokens],
    ids=tokens,raw_tokens=[t.decode(i) for i in tokens],probabilities=probs,
    alternatives=others,joint=math.prod(probs),ppl=math.exp(-sum(map(math.log,probs))/len(probs)),
    method="Native tokenizer, float32 CPU logits and float64 softmax, base weights, true continuation shifted one position against logits; no chat template, conditioning prefix excluded from score.")
(R.parent/'token_packet.json').write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
print(p['tokens'],[round(100*x,2) for x in probs],p['ppl'])
