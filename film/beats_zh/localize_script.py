"""Mandarin adaptation of the approved A–F narration; map old visual cues to Mandarin phrases."""
import json
from pathlib import Path
R=Path(__file__).resolve().parent
P={
'a':[
'测评分数上去了，模型做新题却更差了。我们常把评测当期末考试：训练结束，看分数，就知道谁赢了。',
'可训练会反过来追分数。评测一旦成了大家的优化目标，成绩单就开始指挥训练。',
'你选哪把尺，就决定了成千上万张 GPU 把算力花在哪儿。'],
'b':[
'把这件事画出来，就好懂了。',
'多步推理、细致对话、自主规划，分别沿三个方向伸开。真实的能力空间，维度还要多得多。',
'可到打分时，我们把整个空间往一根轴上投影，最后只读一个数。',
'看这两个盒子，形状差很多，投出来的影子却一样长。',
'等大家都追着这一个分数跑，古德哈特定律就来了。',
'光去优化影子，盒子就沿尺子的方向拉长。没量到的两个方向呢？在这个例子里，它们反而缩了。'],
'c':[
'那该怎么摆脱一个分数的误导？',
'先把成本摆进来。模型再强，也得看实际用起来要多少钱。',
'把智能指数画在纵轴上，推理成本放在横轴上。横轴取对数，数据外侧就浮出一条边界。',
'预算一落下来，你就不能光挑榜上最高的点了。沿着帕累托前沿找：更便宜的追不上它；比它更强的，也不会更便宜。',
'可有些任务连标准答案都没有，那又该怎么评？'],
'd':[
'比如写文章说服别人，讲清一个复杂的 bug，或者把语气调得柔和一点。',
'这时候，Chatbot Arena 换了个办法。',
'先把模型名字藏起来，不按固定评分表打分，只让人看两份回答，投票选更喜欢的那份。',
'把这些两两对比的结果放在一起拟合，就得到类似 Elo 的评级。你还能从区间看出，谁的分数更稳。',
'现在盯着同一个模型，先看基准测出来的能力，再看预算内的帕累托效率，接着看盲测偏好，最后看实际的 API 用量。',
'每换一把尺，名次就变了。',
'与其问谁最好，不如先问：你在乎的是哪种取舍？'],
'e':[
'就算选对了尺，榜单上还有个更容易看漏的区别。',
'我们评的是一种方法，还是一整套系统？',
'传统机器学习里，基准经常被当作比较方法的实验。',
'拿 ImageNet 和 SQuAD 来说：大家用同一份公开数据训练，也在同一个测试划分上考试。',
'其余条件固定，只换一个零件，比如架构或者优化器。方法 A 赢了，你才知道差距从哪儿来。',
'可换成两个已经训练好的基础模型，事情就不一样了。',
'训练集里有什么，数据怎么筛，花了多少算力，很多商用系统都没公开。',
'它拿了第一，是发现了更好的注意力机制，还是预训练时读了十倍的代码和数学？同一个名次，分不出这两种解释。'],
'f':[
'系统榜单适合拿来选产品，想看算法进步，还得把条件固定下来。',
'这就是 Karpathy 的 NanoGPT 速训赛有意思的地方。',
'FineWeb 的训练词元流顺序固定，至于读到第几个才停，由你。',
'硬件统一用八张 H100，验证损失的目标锁在 3.28。',
'那比什么？从开跑到过线的实际用时。',
'少花一分钟，就说明这份算法或系统的改动，让训练确实快了一点。',
'顺着这条终点线看，大家拼的是谁能更快把验证损失降下来。',
'这个损失背后，藏着语言模型一个最基本的指标：困惑度。'],
}
C={
'a':[
('opening hook','做新题却更差了'),('final exam','期末考试'),('who won','谁赢了'),('But evaluation','可训练'),('optimization target','优化目标'),('Whatever ruler','你选哪把尺')],
'b':[
('multi-step reasoning','多步推理'),('nuanced dialogue','细致对话'),('autonomous planning','自主规划'),('high-dimensional space','真实的能力空间'),('project that entire space','把整个空间'),('exact same shadow','影子却一样长'),('the moment the community','等大家'),("Goodhart's law",'古德哈特定律'),('optimizing directly','光去优化影子')],
'c':[
('cost','成本'),('intelligence against','智能指数'),('logarithmic scale','取对数'),('boundary takes shape','浮出一条边界'),('real-world budget','预算一落下来'),('highest model on the board','最高的点'),('Pareto frontier','帕累托前沿'),('no cheaper model','更便宜的追不上'),('no stronger model','比它更强'),('objective answer key','标准答案')],
'd':[
('drafting a persuasive essay','写文章说服别人'),('explaining a complex bug','讲清一个复杂的'),('adjusting tone','把语气'),('Chatbot Arena changes','Chatbot Arena'),('grading against a rigid rubric','固定评分表'),('blind, pairwise human votes','让人看两份回答'),('human votes','投票选'),('By fitting those binary choices','把这些两两对比'),('Elo rating system','Elo'),('compare the exact same model','同一个模型'),('raw benchmark accuracy','基准测出来的能力'),('budget-constrained Pareto efficiency','帕累托效率'),('blind human preference','盲测偏好'),('actual paid API volume','实际的 API 用量'),('rankings shift','名次就变了'),('which trade-off','哪种取舍')],
'e':[
('single scoreboard','榜单上'),('evaluating a method','评的是一种方法'),('in classical machine learning','传统机器学习'),('on imagenet or squad','ImageNet'),('if model a won','方法 A 赢了'),('in modern foundation models','可换成两个'),('training sets','训练集里'),('brilliant new attention','更好的注意力机制'),('or simply ingested','还是预训练')],
'f':[
('great for procurement','选产品'),('fundamental algorithmic progress','算法进步'),('nanogpt speedrun','NanoGPT'),('training token stream in a fixed order','训练词元流顺序固定'),('eight h100','八张 H100'),('eight h one hundred','八张 H100'),('3.28','3.28'),('three point two eight','3.28'),('wall clock time','实际用时'),('every single minute','少花一分钟'),('genuine algorithmic','算法或系统'),('notice what sits','顺着这条终点线'),('driving down validation loss','验证损失降下来'),('foundational metric','最基本的指标')],
}
if __name__=='__main__':
 for r in json.loads((R/'english_timeline.json').read_text()):
    id_=r['id']; parts=P[id_]
    assert len(parts)==len(r['parts'])
    for _,key in C[id_]: assert key in ''.join(parts),(id_,key)
    out={'id':id_,'duration':r['duration'],'hold':r['hold'],'parts':parts,'text':'\n'.join(parts)}
    p=R/f'script_{id_}.json'; tmp=p.with_suffix('.tmp'); tmp.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n'); tmp.replace(p)
    print(id_,len(''.join(parts)))
