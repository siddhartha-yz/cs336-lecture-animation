# 能力的影子：数据与素材
**Stanford CS336 第十二讲 · 中文长剪 v6｜{RUNTIME}**。时码从本版片头第一帧起算。[原课程](https://stanford-cs336.github.io/spring2025/)；中文讲义第 12 讲从印刷页 211 起。片中青、紫通常用来区分比较双方；金色跟着此刻真正计入评测的量走。暖白纸上的片段出自现实资料。

## {START:0-1}　同影异形
82/80/78 和 82/26/20 是两只教学用的盒子。沿第一轴投影，两者都留下 82；第一轴变成 96 时，另外两条边在此例中缩短。这里演的是指标**允许**退步漏检，而不是训练必然让别的能力下降。

## {START:1-1}　一美元买得到哪一个点
- [Artificial Analysis 成本图](https://artificialanalysis.ai/models?cost=intelligence-vs-cost-per-task)和[指数方法](https://artificialanalysis.ai/methodology)：2026-11-24 的 Intelligence Index v5.0.1 快照。取有完整数值的 26 个默认配置；横轴是**完成一项指数任务的平均美元成本**。工程内附未舍入的数值。该组指数最高的是 Claude Fable 5.2，指数 64.6，每题约 26.54 美元。1 美元以内，GPT-6.1 Terra 的 51.3 分、约 0.96 美元/题是这次快照的预算解。
- [OpenRouter 24 小时用量榜](https://openrouter.ai/rankings?view=daily)，2026-11-23 快照。六股流量是处理的词元数。第一股约 11.3 万亿，占**所绘六项**约 23.83 万亿的 47.4%；分母不是全平台总量，也不折算收入。
- [Text Arena 总榜快照](https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset)：前后两次展示都取自 **2026-11-22 overall**。横线是积分的不确定区间，排名可并列。四轴比较只保留三来源里都能匹配的四个家族。每轴组内排序，末位为 0，首位为 100，成本越低位置越高。一个平台上的具体推理档位不等于另一平台的固定部署。

| 同组家族 | 智能指数 | 每题美元 | Arena 积分 | 平台日用量（万亿词元） |
|---|---:|---:|---:|---:|
{COHORT}

- [ImageNet](https://www.image-net.org/) 和 [SQuAD](https://rajpurkar.github.io/SQuAD-explorer/)提供共享的输入与测试标准。只有其他重要设置也固定，才可把方法差异从系统差异里分开。
- [NanoGPT 速训主赛道和纪录](https://github.com/KellerJordan/modded-nanogpt#world-record-history)固定 FineWeb 词元顺序和 8 张 H100，允许跑到不同词元位置，也允许改变网络结构；固定的是数据流、硬件与终点。验证损失 **3.28** 来自 Karpathy/llm.c 的 GPT-2 Small 复现目标。历史镜头画 2024-05-28 至 2025-01-16 的前 20 项，45 分钟到 2.992 分钟，是到同一目标的墙钟时间。

## {START:2-1}　平均分的胜者，为什么没答对九减七
- [SmolLM2-135M](https://huggingface.co/HuggingFaceTB/SmolLM2-135M)在 `The room was quiet.` 之后逐个预测 `The small cat sat on the mat.`。给真正出现的第三个词 `cat` 的条件概率约 **0.0449%**。八个真实词元上的平均负对数概率 3.5165 nat，取指数约 **33.67**。两步各自给原词 1/5、1/20 时，等效候选数是 √(5×20)=10。
- 同一份 45 字节 UTF-8 原文，含前导空格，[GPT-2](https://huggingface.co/openai-community/gpt2)切 9 份，SmolLM2 切 11 份。**89 bit** 是为隔离分母影响而设的等总损失算例，两边同为 1.978 bit/byte。换回真实前向预测，两模型的 BPB 分别约 **1.970、1.980**。[GPT-2 论文表 3](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf)的 WikiText-103 零样本 PPL 17.48 对应 15.42 亿参数模型和另一份语料。
- 算术反例完整原文为 `Choose one: nine minus seven is either two or three. Answer: two`。同一分词器，共 15 个位置。前 14 项的负对数损失和分别为 64.65、67.21 nat；最后的正确词分别为 1.93、1.38 nat。基础版整句 PPL **84.68**，却在两个候选里更偏向 three；[指令版](https://huggingface.co/HuggingFaceTB/SmolLM2-135M-Instruct)整句 **96.79**，在候选中选 two。两端的百分比是原词表概率，不是两选项重新归一化后的百分比。这个从候选文本里挑出的反例用于检验「一定」这两个字，不用来估计两款模型的算术能力。
- [Paloma](https://arxiv.org/abs/2312.10523)按语料领域分别评估语言模型。数值来自 [xLSTM 论文表 8、10](https://papers.nips.cc/paper_files/paper/2024/file/c2ce2f2701c10a2b2f2ea0bfa43cfaa3-Paper-Conference.pdf)：取同为 1.3B、训练 3000 亿词元、GPT-2 分词器的一对模型。最后一列为本片按六域等权重算的 `exp(mean(log(PPL)))`。

| 模型 | Python | 数学 | arXiv | WikiText | C4 | 图书 | 六域等权 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Llama | 2.35 | 12.90 | 5.15 | 11.74 | 13.93 | 13.00 | **8.32** |
| Mamba | 2.39 | 12.51 | 5.28 | 11.76 | 13.35 | 12.44 | **8.22** |

沙箱由评测方执行模型、读取 logits，自己计算规范化概率和原词的损失。图中的四个示意 logits 为 1.14、0.72、−0.13、−0.44；第三个词的概率约为 0.131，对应损失约 2.03 nat。另一组柱子也可以加到一；这项检查单独不能证实概率来自哪台模型。

条件概率小镜头使用一份可验算的教学联合分布：题 A 的两格占 30% 和 10%，题 B 的两格占 12% 和 48%。给定 A，分母缩为 40%，第一种回答的条件概率是 75%。把模型给 A 的两格改成 16% 和 24%，它估计的胜者就反过来；白线的真实分布未变。这四格是示意，随后的“九减七”才是两台模型的实际前向结果。

## {START:3-1}　换卷，也换验收方法
- [MMLU](https://github.com/hendrycks/test)有 57 学科；镜头采用[世界史开发集第 2 题](https://huggingface.co/datasets/cais/mmlu/viewer/high_school_world_history/dev?row=1)与[抽象代数开发集第 1 题](https://huggingface.co/datasets/cais/mmlu/viewer/abstract_algebra/dev?row=0)。[simple-evals](https://github.com/openai/simple-evals)中 GPT-4 1106 Preview、GPT-4o 2024-08-06、GPT-4.1 2025-04-14 的零样本读数是 84.7%、88.7%、90.2%。空隙是到满分的**百分点**，不是误差线。
- [MMLU-Pro，表 3](https://arxiv.org/html/2406.01574#S6.SS2)：至多十个选项。GPT-4o 在新卷直接作答 53.5%，分步作答 72.6%；新旧两卷都用分步作答时，GPT-4o 与 GPT-4 Turbo 的分差从 2.2 增到 8.9 个百分点。
- [GPQA，图 1、表 2](https://arxiv.org/pdf/2311.12022)。图中同行初答 A、B，审阅解析后均认同 B；三名跨领域验证者给出 C、B、A。化学实例的枚举是 4×4=16。非专家获准检索，每题最少 15 分钟，平均 37 分钟；Diamond 子集 198 道。黑板的检索材料参照 [NIST 化合物记录](https://webbook.nist.gov/cgi/inchi?ID=C96399&Units=CAL)。
- [HLE 原论文 §3.2，图 2、4](https://arxiv.org/html/2501.14249v9#S3)。70,000+ 是**尝试次数**，约 13,000 才是正式投稿，约 6,000 进入后续候选；[公开集](https://lastexam.ai/)有 2,500 题，另留私测。流动粒子展示筛选机制；最后的 100 个亮点才采用“一点 25 道公开题”的固定比例。[Regina 墓碑图](https://commons.wikimedia.org/wiki/File:Reginas-Tombstone-a-relief-portrait-with-inscriptions-in-Latin-and-Palmyrene-Copyright.jpg)：Abigail Baker、Alison Cooley，CC BY 4.0，裁切铭文。

## {START:4-1}　先投这一票，再让裁判上场
- [Arena Human Preference 140k，第 771 行](https://huggingface.co/datasets/lmarena-ai/arena-human-preference-140k/viewer/default/train?row=771)：真实的运费发票催办请求。摘录删去机构和路线，两份催办句保留原意节译，原记录中 **A 获选**。片中甲乙匿名；排序解释的是偏好，观众可以选另一份。数据作者 LMArena，CC BY 4.0。
- 与邮件放在同一张桌上的两份材料：[pandas 去重示例](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.drop_duplicates.html)、Fannie Merritt Farmer [《The Boston Cooking-School Cook Book》原版扫描](https://archive.org/details/cu31924087257873)中的 Pop-overs。另一组机器人故事来自[同一 Arena 数据集第 162 行](https://huggingface.co/datasets/lmarena-ai/arena-human-preference-140k/viewer/default/train?row=162)，两份原文分别为 781、241 个按空白切分的英文词。随后给十字中文片段添十一字客套话，是用来分开篇幅与情节的改写示例；进入长度控制估计时，两份真实英文回答保持原样。
- [Chatbot Arena](https://arxiv.org/abs/2403.04132)：图示 Bradley–Terry 模型沿用 Elo 刻度 `P(A胜)=1/(1+10^((E_B−E_A)/400))`。同分时 50%；A 领先 400 分是 **10∶1 的胜算**，胜率 10/11≈90.9%。一次对局不确定一张总榜。
- [AlpacaEval 长度控制](https://arxiv.org/html/2404.04475)：等长反事实把拟合模型的长度差输入设为零，原回答和原票不改，拟合曲线本身不旋平。38 个共有模型的 Spearman 排名相关由 0.94 升至 0.98；这是与人类排行榜的相关性。

## {START:5-1}　修好一处，还要保住原来能用的地方
[SWE-bench 原始集](https://www.swebench.com/original)：12 个 Python 仓库，2,294 个实例。本片取 Sphinx 已关闭的[工单 #5560](https://github.com/sphinx-doc/sphinx/issues/5560)、[修复 PR #8713](https://github.com/sphinx-doc/sphinx/pull/8713)和[基准测试记录](https://huggingface.co/datasets/princeton-nlp/SWE-bench/viewer/default/test?row=1850)。问题在 `napoleon_use_param` 未用于 Other Parameters 分支。实例指定 1 个 FAIL_TO_PASS、45 个 PASS_TO_PASS；第一盏回归灯对应 `NamedtupleSubclassTest::test_attributes_docstring`。回归红灯演的是另一项原有功能被改坏的对照。

五份候选 A–E 中 A、B 过，C、D、E 不过。不放回抽两份，一共 10 对；全错只有 CD、CE、DE，因此这道题的 pass@2 估计为 **7/10**。[pass@k 的无偏估计](https://arxiv.org/abs/2107.03374)。[SWE-bench Verified 实验](https://openai.com/index/introducing-swe-bench-verified/)在同一 500 题、同一 GPT-4o 底座上，SWE-Agent 与 Agentless 的解决总数是 115 和 166。两排珠子分别计数；总数净差 51，不等于后者逐题包含前者的解集。

## {START:6-1}　同一张网格，同一句拒答
[ARC 原题 67a3c6ac](https://github.com/fchollet/ARC-AGI/blob/master/data/training/67a3c6ac.json)的三组例图和测试输入均按原像素重画。规则是每一行左右翻转，换成旋转半圈会被例子排除。[ARC Prize 的 o3 预览实验](https://arcprize.org/blog/oai-o3-pub-breakthrough)对同一组 100 道半私有题给出两档测试时计算：采样预算 6 与 1,024，报告得分 75.7% 与 87.5%。

[HarmBench §6.2 结果与图 7](https://arxiv.org/html/2402.04249v2#S6.SS2)：这里量一份完整输出是否出现指定的有害行为。先展示论文列出的 GCG、GCG (Multi)、GCG (Transfer) 三种测试条件，再取正文单列的标准 GCG 条件：作者报告 Llama 2 13B Chat 为 30.2%，Zephyr 7B + R2D2 为 5.9%。两张百格尺的每格是一个百分点，不是一个测试样本；将它们铺开成同一条百分比坐标，比较两个已训练系统；单凭这两条柱子不能隔离训练因素的因果贡献。正常请求是为解释过度拒绝另设的对照。「整理公开资料」等六项是教学示例。

## {START:7-1}　图纸能不能用，原题有没有见过
- [GDPval 官方样例](https://openai.com/index/gdpval/)展示制造工程师的线缆卷盘夹具。白底图是该任务页的真实材料，右侧转动的卷盘及端视、侧视为同一件教学几何体的两种投影。
- [MedHELM](https://crfm.stanford.edu/helm/medhelm/latest/)按临床任务分开评估。[ACI-BENCH 的公开训练记录 ACI001](https://github.com/wyim/aci-bench/blob/main/data/src_experiment_data/train_aci_asrcorr.csv)是一场模拟就诊：对话说左腕和手部不适，病历的主诉记作 `Left wrist and hand pain.`。对白和记录是节选，整理记录的准确度不能代替临床决策能力。
- [Oren 等的黑盒污染检验](https://arxiv.org/abs/2310.17623)比较整道题目换序后的序列对数似然。在四题的教学模型中，每步从剩余整题中条件抽样，24 个排列概率加和为一；比较 1 个原序和 23 个其余顺序。这个算例中，原序比另 23 种排列的均值高 **1.67 nat**。这是四道示例题在教学模型上的读数。[原论文 §3.2](https://arxiv.org/html/2310.17623v2#S3.SS2)将题集分组，逐组计算原序减去置换均值，再对组间差值做单侧检验。题目本来按年代或难度组织，就是可交换性可能破坏的反例；线索针对数据集层面。
- 语料墙拼接[MIT 许可文本](https://opensource.org/license/mit)、[Sphinx 改动](https://github.com/sphinx-doc/sphinx/pull/8713/files)和[GSM8K 测试集首题](https://github.com/openai/grade-school-math/blob/master/grade_school_math/data/test.jsonl)的节选。归一化后 65 个词，窗口为 **65−13+1=53**。128 位布隆过滤器只报可能命中，再逐词精确核对。第 1 窗是公共许可句，第 49 窗是评测题，保留模板、仅给题面 13 词加掩码，**52** 个位置仍贡献训练损失。窗口数与参与训练的词位数不是同一分母。
- [LiveCodeBench 发布记录](https://github.com/LiveCodeBench/LiveCodeBench)：v1–v6 的累计题量 400、511、612、713、880、1,055。用出题日期隔开旧训练材料、让私题少暴露、请专家重审错标与歧义，处理的是三个不同问题。

## {START:8-1}　回到那两个盒子
片尾的 82 来自最初的几何模型。六根方向追踪概率、推理、对话、行动、安全、生态与清白；六边形是方向示意，不是六个可以直接相加的量。

## 音乐
[Blue Dot Sessions](https://app.sessions.blue/browse) 作曲与录音。以下是每段音乐**开始进入**混音的时刻；相邻录音在切点前后相连。第 1 音轨为配乐版，第 2 音轨是同一场 Drama 3 中文旁白。

| 乐章 | 入场 | 曲目 · 专辑 | 与画面的关系 |
|---|---|---|---|
{MUSIC}

片头两束影子在 **82** 重合时，尺子落下一记短短的木音；片尾回到 **82**，响的是同一记。这个音色与章门的敲击都取自 *The Gran Dias* 的原录音，尺子保留的是较低的木质共鸣。停表只有一次机械回弹。发票盲投的 **4.5 秒**和 ARC 猜图的 **5 秒**留给观众，器乐稍稍后退；发票上的选票声直到揭晓才落下。

同一首 *Denzel Sprak* 有两种摆法：在人类胜率曲线下面，拨弦的起音清楚可辨；到 ARC 彩格，先收住拨弦，让弦音在思考的空隙里延续，画面开始展开候选规则时再带回节奏。

曲目节选并作淡变、混音，按 [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) 署名。公开或商业用途请按 [Blue Dot Sessions 的使用条件](https://www.sessions.blue/licensing/)取得相应授权。
