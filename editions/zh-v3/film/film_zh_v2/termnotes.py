"""The actual one-line annotations on the blackboard, shared by drawings and by the screening checks."""
from pathlib import Path
import json
TERMS=json.loads(Path(__file__).with_name('glossary.json').read_text(encoding='utf-8'))
def hint(term):
 return TERMS[term]

# A real spoken phrase under a fully legible instance of each inscription.
# The film's word clock supplies its timestamp; the copies on the desk and
# in the viewing index do not carry a separate hand-maintained list of seconds.
WHERE={
 '帕累托前沿':('1-1','比它更强的'),'FineWeb':('1-4','顺序固定'),
 '困惑度（PPL）':('2-1','模型从左往右读'),'BPB':('2-2','两行都是四十五个字节'),
 'Paloma':('2-4','每个领域各占一列'),'六域等权 PPL':('2-4','看右边'),
 'MMLU':('3-1','大规模多任务语言理解'),'MMLU-Pro':('3-2','第一刀是清噪'),
 'GPQA Diamond':('3-3','考的还是检索'),'HLE':('3-4','人类最后考试'),
 'Bradley–Terry':('1-2','谁的分数更稳'),'Elo':('1-2','谁的分数更稳'),
 'LLM-as-a-Judge':('4-3','迅速普及'),'AlpacaEval 2.0':('4-4','一个统计解法'),
 'SWE-bench':('5-1','它写的代码'),'脚手架（Scaffold）':('5-3','底层模型'),
 'pass@k':('5-3','这五份一共能配出十对'),'ARC-AGI':('6-1','肖莱设计了'),
 'HarmBench':('6-3','要读完整份回答'),'GCG':('6-4','是一种基于梯度的'),
 '生态效度':('7-1','要看真实行业交付'),'GDPval':('7-1','一份卷筒参数'),
 'MedHELM':('7-1','则把评测拆到'),'可交换性检验':('7-2','想法非常直觉'),
 '13-gram':('7-3','也叫 13-gram'),'布隆过滤器':('7-3','清洗海量预训练文档'),
 'LiveCodeBench':('7-5','左边这题')}
