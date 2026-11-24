from pathlib import Path
import json
R=Path(__file__).parent
SCENES={
'g':('opening2',0,55,.90,[
("Start right here, with the probabilities a model assigns to the actual tokens as it reads from left to right.","就从眼前这排概率接着看：模型从左往右读，给原文词元逐一分配概率。"),
("Multiply those probabilities and the product shrinks with length. Eventually, ordinary floating-point arithmetic can even round it to zero.","把概率连乘，序列越长，乘积通常越小。用普通浮点数计算，最后甚至会舍入成零。"),
("So take the negative log probability of each token instead. Average those losses across the test set, then exponentiate. That number is perplexity.","换个做法：逐词元取负对数概率，求整个测试集的平均，再取指数。这就是困惑度。"),
("There is a neat way to picture it: an effective number of choices. With a vocabulary of a hundred thousand tokens, uniform guessing gives you a perplexity of a hundred thousand.","它可以想成一个等效的候选数。词表有十万项时，均匀乱猜的困惑度就是十万。"),
("Bring it down to ten and you pay the same average loss as a model guessing uniformly among ten options at each step. The actual number of plausible options can change from word to word.","把它降到十，平均损失就相当于每步在十项里均匀猜。实际的候选数可以随词变化。")]),
'h':('opening2',1,50,.80,[
("Before comparing two models on perplexity, watch what happens to the exact same sentence under two tokenizers. The words stay put; only the cuts move.","拿困惑度比两个模型之前，看看同一句话进了两套分词器。字一个没动，变的是切的位置。"),
("Hold the total surprise fixed and split the passage into more pieces. The per-token average falls, even though the score for the text as a whole hasn't changed.","固定总信息量，把句子切得更碎。每个词元的平均损失就降了，整句话的总损失却没变。"),
("Count bits, divide by the raw UTF-eight bytes, and you have bits per byte. Same text, same denominator. The models can still give it different probabilities.","用总比特数除以原文的 UTF-8 字节数，得到每字节比特数。分母一样，模型给出的概率仍可能不同。"),
("For a long time, language modeling benchmarks asked you to train and test on splits of the same corpus, like Penn Treebank or WikiText one oh three.","早期语言模型基准常让你在同一语料的不同划分上训练和测试，比如 Penn Treebank 或 WikiText-103。"),
("GPT-two took a different route: pretrain on broad web text, then measure zero-shot perplexity on those benchmark corpora, without fitting a model to each one.","GPT-2 换了一条路：先在广泛的网页文本上预训练，再直接到这些基准语料上测零样本困惑度。")]),
'i':('tradeoff',0,60,1.20,[
("If perplexity sits at the heart of pretraining, is driving it down enough to capture everything we mean by capability?","既然困惑度是预训练的核心，把它降下去，就能量到我们在意的所有能力吗？"),
("Imagine for a moment that your model knew the true joint distribution of questions and answers. Conditioning on a question would give you the right probabilities for its answers. With a rule for what counts as a good decision, you could act on those probabilities.","先想一个理想情况：模型知道题目和答案的真实联合分布。给定题目，就拿到了答案的真实条件概率；再按得分规则作决策。"),
("There is a big distance between that ideal and the models we can actually build. Perplexity puts the same weight on every target token. A predictable bit of grammar takes up exactly as much room in the average as the answer does.","但真实模型离这个理想还很远。困惑度平均时给每个词元同样的权重。一处词法和一道题的答案，在平均数里占的份额一样。"),
("Look at this one arithmetic sequence. One model saves enough loss on the earlier tokens to win on the whole line. But at the answer slot it gives the wrong choice its highest probability. The other model loses on the average and gets that one decision right.","看这条算术题序列。一个模型在前面省下的损失，足以赢下整行的平均分；可到了答案格，它概率最高的选择是错的。另一个模型平均分输了，这一步却答对了。")]),
'j':('domains',0,55,.80,[
("A global average can hide trouble across domains, too. A model can do well on one kind of writing and turn out to be much less sure somewhere else.","总平均也会遮住领域差异。模型在一类文本上很有把握，换一种写法，表现可能就变了。"),
("Paloma keeps those slices visible. Give each domain its own column and you can see where the probability assignments hold up, and where they don't. A pooled score puts that detail back into one number.","Paloma 把这些切片保留下来。每个领域各占一列，就看得到模型在哪儿预测得稳，在哪儿掉下去。合在一起，这些差别又进了一个数。"),
("There is another problem when the only thing a leaderboard receives is a score. The bars are supposed to be probabilities, and all their mass together has to be exactly one. A claimed score gives you no way to check that.","如果榜单只收一个分数，还有个问题。预测的柱子应该是概率，加起来必须是 1。光看提交的分数，验不了这一点。"),
("So run the forward pass in a controlled sandbox, apply softmax to the logits, and check the total probability mass. Then compute the loss yourself. Checking the sum is a useful guard, but the score still has to come from the actual model.","所以要在受控沙箱里独立前向，用 softmax 把 logits 化为概率，检查总和，再自行计算损失。归一化是一道检查，分数还必须来自实际模型。")]),
'k':('domains',1,35,1.40,[
("Even with the units aligned, the domains split out, and the probabilities verified, perplexity still grades the whole stream of text. A hard question often has just one spot where the answer matters.","单位对齐、分领域看过、概率也核验了，困惑度判的仍是一整段文。遇到难题，决定对错的往往只是一个答案格。"),
("Standardized exams put that spot at the center: a known answer, automatic grading, and questions across dozens of subjects. That gives us a different ruler.","标准化考试把答案格放到中心：有标准答案，能自动评分，也能覆盖几十门学科。这样我们就换了一把尺。"),
("For a while, the ruler gave us clear steps upward. But as the strongest models crowded toward the top, the gaps became harder to read. That's benchmark saturation.","一开始，这把尺能看出进步。但最强的模型都挤到顶端之后，差距越来越难量。这就是基准饱和。")]),
}
for i,(module,beat,duration,hold,parts) in SCENES.items():
    r=dict(id=i,module=module,beat=beat,duration=duration,hold=hold,parts=parts)
    if i=='i':r['thinking']=dict(after_part=0,seconds=1.65)
    p=R/f'script_{i}.partial'
    p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');p.replace(R/f'script_{i}.json')
    print(i,len(' '.join(e for e,_ in parts).split()),duration)
