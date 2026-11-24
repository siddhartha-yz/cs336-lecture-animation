"""Local, deterministic plain-text ranking example for the Beat 2 lesson.

Run with a Python containing PyTorch & Transformers:
    python measure_tradeoff.py --base PATH --instruct PATH
The two documented artifacts use the same token IDs on every selected line.
BOS is supplied as context; all displayed tokens, including the answer, are scored.
"""
from pathlib import Path
from dataclasses import dataclass
import argparse, json, math

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

R = Path(__file__).resolve().parent
MODELS = (
    {"model":"HuggingFaceTB/SmolLM2-135M", "revision":"93efa2f097d58c2a74874c7e644dbc9b0cee75a2",
     "source":"https://huggingface.co/HuggingFaceTB/SmolLM2-135M", "name":"SmolLM2-135M · base"},
    {"model":"HuggingFaceTB/SmolLM2-135M-Instruct", "revision":"12fd25f77366fa6b3b4b768ec3050bf629380bac",
     "source":"https://huggingface.co/HuggingFaceTB/SmolLM2-135M-Instruct", "name":"SmolLM2-135M · instruct"},
)
EXTRA={
    "360base": {"model":"HuggingFaceTB/SmolLM2-360M", "revision":"f8027fd0eaeea54caa13c31d31b9fdc459c38b49",
                "source":"https://huggingface.co/HuggingFaceTB/SmolLM2-360M", "name":"SmolLM2-360M · base"},
    "360chat": {"model":"HuggingFaceTB/SmolLM2-360M-Instruct", "revision":"a10cc1512eabd3dde888204e902eca88bddb4951",
                "source":"https://huggingface.co/HuggingFaceTB/SmolLM2-360M-Instruct", "name":"SmolLM2-360M · instruct"},
}
WORDS="zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen".split()
TEMPLATES = (
    ("add","Take {a} to start. Add {b} more and you will get {c}"),
    ("add","For this problem, simply add {a} and {b}. The answer is {c}"),
    ("add","As a simple example, the sum of {a} and {b} is {c}"),
    ("add","Lena has {a} apples and gets {b} more. She now has {c}"),
    ("add","You have {a} coins and pick up {b} more, making a total of {c}"),
    ("add","A quick example: if you add {a} and {b}, the result is {c}"),
    ("sub","Take {a} to start. Remove {b} and you are left with {c}"),
    ("sub","Lena has {a} coins and gives away {b}. She now has {c}"),
    ("sub","A quick example: if you subtract {b} from {a}, the result is {c}"),
    ("sub","For this problem, subtract {b} from {a}. The answer is {c}"),
    ("add","Choose the right answer: {a} plus {b} equals {left} or {right}. It is {c}"),
    ("add","If I add {a} to {b}, do I get {left} or {right}? {c}"),
    ("add","Choose one: {a} plus {b} is either {left} or {right}. Answer: {c}"),
    ("sub","Choose one: {a} minus {b} is either {left} or {right}. Answer: {c}"),
    ("sub","If I take {b} away from {a}, am I left with {left} or {right}? {c}"),
)
PAIRS = ((2,3),(1,4),(3,3),(3,4),(2,5),(4,4),(3,5),(4,5),(2,7),(1,8),
         (5,3),(6,3),(7,3),(5,2),(6,2),(7,2),(8,2),(8,3),(9,3),(9,4),
         (9,2),(7,5),(8,4),(7,6),(8,5),(9,5),(8,6),(9,6),(6,6),(9,7))

@dataclass
class Item:
    text: str
    ids: list
    answer: str
    prompt: str
    template: int

def candidates(ts):
    out=[]
    for ti,(op,tmpl) in enumerate(TEMPLATES):
        before=tmpl.removesuffix("{c}")
        for a,b in PAIRS:
            n=a+b if op=="add" else a-b
            if not 0<n<19: continue
            for verbal in (True,False):
                word=(lambda j: WORDS[j]) if verbal else str
                left,right=sorted((n,n+(1 if ti%2 else -1)))
                args={"a":word(a),"b":word(b),"c":word(n),"left":word(left),"right":word(right)}
                text=tmpl.format(**args)
                prefix=before.format(**args).rstrip()
                ids=ts[0].encode(text,add_special_tokens=False)
                if not 12<=len(ids)<=15 or ts[0].decode(ids[-1]).strip()!=word(n):
                    continue
                if any(t.encode(text,add_special_tokens=False)!=ids for t in ts[1:]):continue
                prefids=ts[0].encode(prefix,add_special_tokens=False)
                if prefids not in (ids[:-1],ids[:-2]): continue
                # A trailing stand-alone space is part of the presented prefix.
                assert ts[0].decode(ids[:-1]).strip()==prefix
                out.append(Item(text,ids,word(n),prefix,ti))
    return out

def from_logits(logits, expected):
    lp=logits.double().log_softmax(dim=-1)
    probs=lp.gather(-1,expected.unsqueeze(-1)).squeeze(-1).exp()
    loss=-lp.gather(-1,expected.unsqueeze(-1)).squeeze(-1)
    return probs,loss,lp

def measure(model, items, ts, bos):
    N=len(items);wid=max(len(x.ids) for x in items)
    arr=torch.full((N,wid),int(bos),dtype=torch.long)
    expected=torch.full_like(arr,int(bos))
    for j,x in enumerate(items):
        size=len(x.ids)
        arr[j,1:size]=torch.tensor(x.ids[:-1])
        expected[j,:size]=torch.tensor(x.ids)
    with torch.no_grad():
        # The causal mask makes right-padding irrelevant on all scored positions.
        logits=model(arr,use_cache=False).logits
        probs,loss,lp=from_logits(logits,expected)
    out=[]
    for j,x in enumerate(items):
        size=len(x.ids);p=probs[j,:size].tolist()
        L=loss[j,:size].tolist();m=math.fsum(L)/size
        row=lp[j,size-1,:]
        ii=row.topk(8).indices.tolist()
        top=[{'id':k,'token':ts.decode(k),'p':float(row[k].exp())} for k in ii]
        out.append(dict(probabilities=p,nll=L,mean_nll=m,ppl=math.exp(m),top=top))
    return out

def quality(a,b,x):
    save=b["mean_nll"]-a["mean_nll"]
    gap=a["nll"][-1]-b["nll"][-1]
    smooth=sum(p<q for p,q in zip(a["nll"][:-1],b["nll"][:-1]))
    wrong=a["top"][0]["token"].strip()
    if wrong==x.answer or not (wrong.isdecimal() or wrong in WORDS):
        return None
    if b["top"][0]["id"]!=x.ids[-1] or save<.035 or gap<.15:
        return None
    # Prefer a decisive full-line win, clear answer loss, and consistent prefix.
    return save+.25*gap+.058*smooth, smooth

def main():
    cli=argparse.ArgumentParser();cli.add_argument('--base',type=Path,required=True)
    cli.add_argument('--instruct',type=Path,required=True);cli.add_argument('--threads',type=int,default=5)
    cli.add_argument('--extra',action='append',default=[],metavar='KEY=DIR')
    cli.add_argument('--cap',type=int,default=0);cli.add_argument('--output',type=Path,default=R/'tradeoff_case.json')
    args=cli.parse_args()
    torch.set_num_threads(args.threads)
    extra=[x.split('=',1) for x in args.extra]
    model_info=(*MODELS,*(EXTRA[k] for k,_ in extra))
    dirs=(args.base,args.instruct,*(Path(p) for _,p in extra))
    ts=[AutoTokenizer.from_pretrained(str(d),local_files_only=True) for d in dirs]
    separator="<|endoftext|>"
    assert all(separator in t.get_vocab() for t in ts)
    bos=ts[0].convert_tokens_to_ids(separator)
    assert all(bos==t.convert_tokens_to_ids(separator) for t in ts)
    docs=candidates(ts)
    docs=docs[:args.cap or len(docs)]
    print(f'{len(docs)} token-aligned candidates',flush=True)
    ms=[AutoModelForCausalLM.from_pretrained(str(d),local_files_only=True,dtype=torch.float32).eval().cpu() for d in dirs]
    best=None; goods=0; improvements=0; relevant=[]
    for i in range(0,len(docs),12):
        group=docs[i:i+12]
        both=[measure(m,group,t,bos) for m,t in zip(ms,ts)]
        for j,x in enumerate(group):
            versions=[z[j] for z in both]
            goods+=sum(z["top"][0]["id"]==x.ids[-1] for z in versions)
            for ai,aa in enumerate(versions):
              for bi,bb in enumerate(versions):
                if ai==bi:continue
                order=(ai,bi)
                cut=quality(aa,bb,x)
                if cut is not None and (best is None or cut[0]>best[0]):
                    best=(cut[0],x,aa,bb,order,cut[1])
                    print('candidate',x.text,aa['ppl'],bb['ppl'],aa['top'][0],order,flush=True)
                if bb["top"][0]["id"]==x.ids[-1] and aa["top"][0]["id"]!=x.ids[-1]:
                    gap=bb['mean_nll']-aa['mean_nll']
                    if gap>0:
                        improvements+=1
                        relevant.append((gap,x.text,aa['top'][0],order,aa['ppl'],bb['ppl']))
        if i%60==0 or i+len(group)==len(docs):
            print('scanned',i+len(group),'best',None if best is None else (best[1].text,best[2]['ppl'],best[3]['ppl'],best[2]['top'][0],best[-1]),flush=True)
    if best is None:
        print('correct top-1 count',goods,'any rank reversal',improvements)
        for row in sorted(relevant,key=lambda x:x[0],reverse=True)[:8]:print('open',row)
        raise SystemExit('No strict numeric full-vocabulary top-1 rank reversal found.')
    _,x,aa,bb,order,win=best
    q=dict(text=x.text,prefix=x.prompt,answer=x.answer,tokens=[ts[0].decode(k) for k in x.ids],
           token_ids=x.ids,bos_id=bos,answer_index=len(x.ids)-1,sampled_lines=len(docs),
           preceding_positions_a_lower=win,
           models=[dict(model_info[j],**m) for m,j in zip((aa,bb),order)],
           selection="Illustrative selected continuation, not a benchmark over the models. Both orderings searched on the same set of template-generated simple arithmetic lines; require wrong numeric open argmax for lower full-line perplexity and correct open argmax for the other model.",
           protocol="Same literal plain text and token IDs, common <|endoftext|> document separator as initial context, no chat template, causal teacher-forced token likelihood, float32 CPU forward and float64 log softmax, natural logarithm, all visible tokens scored, full-vocabulary top-1 next token.")
    args.output.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
    print(q['text'],q['token_ids'], flush=True)
    for m in q['models']:
        print(m['name'],m['mean_nll'],m['ppl'],m['nll'][-1],m['top'][0],flush=True)

if __name__=='__main__':main()
