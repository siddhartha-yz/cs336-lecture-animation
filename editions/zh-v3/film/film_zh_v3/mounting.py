"""Ink belongs to the object. The typesetting level used for slides has no counterpart on this stage."""
from ink import *
from timeline3 import clock
# Phrases which supplied a chapter name in the earlier master, never an object in the shot.
# This list is shared by animated outlines and the ordinary glyph path -- no ghost first frame.
DISCARD=set('''示意数据|几何示意|同一句话，两把分词刀|切的是边界，比较的是预测|同一道算术题|在代码里领先，换成数学呢？|提交的概率 · 示意|独立前向，重新计分|只判最后的选择|整句平均值，把这一步也平均进去了|一次均匀盲猜|开放式任务|为同一个机器人，写个短故事|一票只比较一对|三场对局可以绕成一圈|把票交给人|追踪同一份回答|改写示意 · 语义保留|扩写示意 · 信息不增|同一题 · 模型中的长度差|把代码交给测试|在同一个仓库里跑两轮|候选补丁|一次通过的测试|换成一张陌生的网格|先读第一句|同一策略，两种代价|同一协议下的行为发生率|同一道题，在两次测量之间|考卷上的一格，车间里的一件东西|原序与置换|在语料里查原题|命中以后|同一份样本|按日期把新题留出来|两种复核，守的是两件事|一把尺，看见一种东西|一把尺，看见同一种东西|每换一次评测，把上一次看不见的东西加进来|从单一投影，到多维测量|模型评测|从分差读胜率|按语料，分开读|只看同样的开头，会把这两种结果混在一起。|两次都出问题的三条，还在这里。|任务分开测，交付物也分开看。'''.split('|'))
# Retire old department names printed at the edge of the screen. A name at a column head, a
# document quotation, or on a physical object in the composition is a different use, and stays.
OFFSTAGE=set('''困惑度（PPL）|把平均负对数概率还原成等效选项数|十万个等可能选项|十个等可能选项|GPT-2 · WebText|示例分布|Paloma|按语料领域分别衡量语言模型|MMLU|-Pro|覆盖 57 门学科的四选一考试|侧重多步推理，每题最多十个选项|GPQA|Diamond|专家复核、外行也难查到答案的科学题|HLE|专家出的学术难题，有些还必须看图|Bradley–Terry|从两两胜负估计相对实力|LLM-as-a-Judge|让模型当裁判，比较开放式回答|位置偏见|长度偏见|自我偏好|AlpacaEval 2.0|控制回答长度，估计偏好胜率|SWE-bench|在真实软件仓库中解决报告的问题|Docker|3ed7590ed|pass@k|尝试 k 次，至少一次做对的概率|脚手架|模型外的工具、检索与状态管理|ARC-AGI|从少量网格示例推断变换规则|HarmBench|用整份回答判断有害行为是否发生|GCG|用梯度构造的压力测试条件|三种 GCG 条件取平均|20 道配对用例 · 示意|生态效度|考题与实际工作有多像|GDPval|用真实职业交付物评测模型|MedHELM|按临床工作任务评测语言模型|可交换性检验|比较原题序和乱序的对数概率|公开材料拼接的工作样本|一窗连续十三个词|13-gram|布隆过滤器：命中后仍要核对原文|LiveCodeBench|按竞赛发布日期滚动更新的编程测试'''.split('|'))
def omit(k,s,x,y,fs):
 if k=='8-2' and fs==27 and s in ('取舍','词元概率','考卷','偏好','行动','推理与安全','效度与污染'):return True
 if s=='同一代码版本 · 同一环境':return True
 if s in DISCARD or s.startswith('modded-nanogpt · '):return True
 if s in OFFSTAGE and y<220:return True
 if s=='GPT-6 Luna' and fs>39:return True
 if s=='NanoGPT 速训挑战':return True
 if s in ('候选题','原来的题序，有多特别？'):return True
 return False
def etch(g,s,x,y,fs,col,op=1,align='left',w=None):
 # For ink newly mounted on a marked object. It shares the object's local transform, even in a rack-in.
 g._attached=True
 try:txt(g,s,x,y,fs,col,op,align,w)
 finally:g._attached=False
def tether(g,p,tip,term,definition,col,op,side='left',sz=30):
 if op<=.005:return
 x,y=tip;dx=(1 if side=='left' else -1);ex=x-10*dx
 path(g,[p,((ex+p[0])*.5,p[1]),(ex,y)],1,col,1.24,op*.76)
 dot(g,*p,3.7,col,op)
 etch(g,term,x,y,sz,col,op,side)
 if definition:etch(g,definition,x,y+36,23,M,op,side)
def raw_legacy(g,k,s,x,y,fs,col,al,align,font,weight):
 # A handful of type draws from the old world coordinates stand for an actual instrument.
 # Move them on the same clock, attached to its projection. Other narrative lettering is removed.
 if al<.003:return False
 if k=='0-1'and s=='训练更新':
  etch(g,'训练更新 · 示意',x,y,fs,col,al,align);return True
 if k in ('1-2','1-3')and s=='GPT-6 Luna'and fs>39:
  # A name tag at the split between four actual readings, not a new slide.
  tether(g,(800,389),(841,377),'GPT-6 Luna','',C,al,sz=24);return True
 if k in ('1-3','1-4')and s in ('方法','系统')and fs>31:
  # Lower the mark into its experimental fixture; the old group scales as one with its border.
  return True
 if k=='1-4'and s=='NanoGPT 速训挑战':
  if fs>45:tether(g,(1390,178),(1342,125),'NanoGPT','速训计时',O,al,'right',29)
  else:pass
  return True
 if k in ('1-4','2-1')and s=='困惑度（PPL）':
  tether(g,(1401,369),(1440,220),'困惑度 · PPL','每步等效的候选数',T,al,'right',27);return True
 if k=='2-1'and s in ('十万个等可能选项','十个等可能选项'):
  n='100,000' if '十万' in s else '10'
  y0=346;path(g,[(165,y0+13),(165,y0),(1426,y0),(1426,y0+13)],1,C,1.5,al)
  etch(g,'n = '+n,790,y0-22,28,C,al,'center');return True
 if k in ('2-2','2-3')and s=='GPT-2 · WebText':
  tether(g,(368,216),(298,139),'GPT-2 · WebText','网页预训练',C,al,sz=28);return True
 if k=='2-4'and s=='Paloma':
  tether(g,(353,313),(264,224),'Paloma','按语料领域分栏',T,al,'right',29);return True
 if k=='3-1'and s=='MMLU'and y<215:
  # Printed on the common subject/score bracket, away from the bars and their values.
  tether(g,(1429,654),(1422,708),'MMLU · 57 门学科 · 四选一','',C,al,'right',26);return True
 return False

def place(g,k,c):
 # Local engravings and specimen labels. There is deliberately no universal 'title location'.
 t=c.t
 def a(q):return c.at(q)
 def win(q,end=None,p=.65):
  start=a(q);stop=a(end)if end else c.d+1
  return phase(t,start-.19,start+.34)*(1-phase(t,stop-.44,stop-.07))
 def cap(p,tip,s,d,col,op,side='left',sz=30):tether(g,p,tip,s,d,col,op,side,sz)
 if k=='3-2':
  # The fork mark belongs to the edited exam. It moves onto the answer rail with the new options.
  z=phase(t,a('第二刀')-.32,a('第二刀')+.35);op=z*(1-phase(t,a('第三刀')-.48,a('第三刀')-.11))
  x,y=lerp((548,458),(224,373),z);ex,ey=lerp((342,234),(172,273),z)
  cap((x,y),(ex,ey),'MMLU-Pro','最多十选一，增加多步推理题',C,op,sz=28)
 elif k=='4-2':
  al=1-phase(t,a('极大似然')-.48,a('极大似然')+.61)
  cap((355,632),(295,395),'Bradley–Terry','用成对胜负估计相对实力',C,al*win('Bradley'),sz=27)
 elif k=='4-4':
  op=win('AlpacaEval','论文比较');cap((729,319),(778,202),'AlpacaEval 2.0','在相同长度下读胜率',C,op,sz=26)
 elif k=='5-1':
  op=win('SWE-bench','完整的代码库');cap((421,387),(198,204),'SWE-bench','用真实仓库里的故障检验补丁',T,op,sz=30)
 elif k=='5-2':
  op=win('Docker','两道测试');cap((1162,488),(1089,558),'Docker · 3ed7590ed','运行环境与代码版本固定',C,op,sz=27)
 elif k=='5-3':
  op=win('pass@1','先把中间');z=phase(t,a('允许交两份')-.22,a('允许交两份')+.62)
  px,py=lerp((665,637),(1169,647),z); xx,yy=lerp((516,600),(1001,641),z)
  if op:etch(g,'pass@k',xx,yy,30,C,op);etch(g,'至少一份通过',xx,yy+38,21,M,op)
  op=win('工具可以换');cap((543,374),(591,290),'脚手架','模型外的工具和检索',O,op,'left',27)
 elif k=='6-1':
  op=phase(t,a('肖莱设计')-.28,a('肖莱设计')+.40);v=phase(t,a('没有文字题干')-.69,a('没有文字题干')+.28)*(1-phase(t,a('三到五个')-.63,a('三到五个')+.33));cap((177-71.5*v,258-18.5*v),(176,159),'ARC-AGI · 67a3c6ac','看几组示例，推一条变换规则',C,op,sz=27)
 elif k=='6-3':
  op=win('HarmBench','一道无害')
  cap((577,408),(466,276),'HarmBench','按完整回答判定有害行为',C,op,'right',28)
 elif k=='6-4':
  op=win('HarmBench','二十道题')
  if op:etch(g,'HarmBench · 三种 GCG 条件的均值',484,263,26,M,op)
  op=win('二十道题')
  if op:etch(g,'配对示意 · 每条线是一道题',328,671,24,M,op)
 elif k=='7-1':
  op=win('斯坦福')
  if op:cap((609,442),(538,211),'MedHELM','按临床工作任务分别评测',T,op,sz=30)
 elif k=='7-2':
  ear=win('原始顺序','随机打乱')
  if ear:cap((452,446),(224,652),'可交换性检验','比较原序和乱序的概率',O,ear,sz=27)

