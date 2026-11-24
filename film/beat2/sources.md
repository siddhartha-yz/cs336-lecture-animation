# Beat 2 · 困惑度的数据与口径

单段片长 04:15。从 Beat 0–2 合辑观看时，本段在 03:43.800 开始。画面时间以下均按 Beat 2 单段计算。

## 00:00 · 同一串真实的词元概率

接用 Beat 1 尾帧 [SmolLM2-135M 基座模型](https://huggingface.co/HuggingFaceTB/SmolLM2-135M) 的八个条件概率。条件前文为 `The room was quiet.`，续写为 ` The small cat sat on the mat.`。平均负对数损失用自然对数，约 **3.5165 nats/词元**，取指数得到困惑度 **33.67**。联合概率约为 **6.060 × 10⁻¹³**。把该数再相乘至四次是 Float32 下溢的数值演示；只计算这条样例，不是数据集平均。

均匀分布的困惑度等于候选数。镜头中把 100,000 个候选画成十组，对数损失的等效候选数不要求每一步猜同样多的选项。

## 00:55 · 同一句原始字节，两套真实分词

在相同的 `Text:` 前文后给两种模型同一段续写 ` Byte-level tokenizers encode naïve strings.`。包含开头空格的续写长度为 **45 个 UTF‑8 字节**。模型仅评分续写，分词使用模型各自提供的原生 ByteLevel BPE。前文分词不会与续写跨界重新合并。使用 float32 CPU 模型前向，随后在 float64 下求 log-softmax。

| 模型 | 词元数 | 实测总损失 (bits) | 实测 PPL | 实测 BPB |
|---|---:|---:|---:|---:|
| [GPT-2](https://huggingface.co/openai-community/gpt2) | 9 | 88.632 | 921.60 | 1.970 |
| [SmolLM2](https://huggingface.co/HuggingFaceTB/SmolLM2-135M) | 11 | 89.081 | 274.04 | 1.980 |

片中先保留真实分词边界、给两行**同样的 89 bits**，只看分母变化；接着换入实测 BPB。真实模型的总损失不必相同。分词比较使用每字节损失 **BPB = 总 bits ÷ 原始 UTF‑8 字节数**；如果原损失以 nats 给出，先除以 ln 2 转成 bits。

较后的 GPT‑2 数字是 [Radford 等（2019），表 3](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf) 的 1,542M 参数模型零样本结果：PTB **35.76**，WikiText‑103 **17.48**，1BW **42.16**。它们不是上表 GPT‑2 小模型对短句的结果。论文说明各基准使用各自的评价口径，数值只用来展示预训练后跨语料直接评估。

## 01:45 · 真实算术反例

题句：`Choose one: nine minus seven is either two or three. Answer: two`。用同一 SmolLM2 分词表示，前置共同 BOS，逐位置评估这 15 个词元（含正确答案）。“下一词元第一名”在整张词表上取 argmax。基座模型整句困惑度 **84.68**，答案却把 `three` 排第一；指令模型整句困惑度 **96.79**，答案格把 `two` 排第一。指令模型的正确答案概率约 **25.18%**，基座约 **14.46%**。这是为说明指标差异筛选出的一个反例，不拿它代表两个模型的整体能力排名。

权重：[SmolLM2-135M](https://huggingface.co/HuggingFaceTB/SmolLM2-135M) 与 [SmolLM2-135M-Instruct](https://huggingface.co/HuggingFaceTB/SmolLM2-135M-Instruct)。数据包给出了具体权重版本、原始逐词元概率和评分方式。

## 02:45 · Paloma 领域拆分与评分复算

六列采用 [Paloma 的领域划分](https://proceedings.neurips.cc/paper_files/paper/2024/hash/760b2d94398aa61468aa3bc11506d9ea-Abstract-Datasets_and_Benchmarks_Track.html) 和 [xLSTM 论文表 8、10](https://papers.nips.cc/paper_files/paper/2024/file/c2ce2f2701c10a2b2f2ea0bfa43cfaa3-Paper-Conference.pdf) 中的 Llama / Mamba（约 1.3B 组别）实测 PPL。两行共用 GPT‑2 分词器；C4 English 是表 8 的 Web 聚合。最右侧若合并六列，使用六域等权的平均对数损失再取指数，结果约 **8.32 / 8.22**；它是对这六列的演示汇总，不是论文报告的 Paloma 全量池化分数。

检查非法概率的画面为数学示意。可信评分由评测端在受控环境中用固定模型权重与输入独立前向，再将 logits 通过 softmax 归一化、校验总概率并自行计分。概率合计为 1 是必要检查之一，不能证明输入身份和计算来源。

## 03:40 · 答案格和天花板

[MMLU 数据集](https://github.com/hendrycks/test) 覆盖 57 个学科。若以 57 根标记表示范围，标记不是这 57 科的成绩。[OpenAI simple‑evals](https://github.com/openai/simple-evals/blob/main/README.md) 报告的同一套零样本思维链评测总准确率示例：GPT‑4（1106 预览）**84.7%**，GPT‑4o（2024‑08‑06）**88.7%**，GPT‑4.1（2025‑04‑14）**90.2%**。此处用来进入“高分扎堆”的问题，不展开下一拍。

## 配音与曲目

英文为 Aiden 声线的五段完整录制，中文字幕可开关。由 Blue Dot Sessions 提供的三首真人录制器乐按段落截取、混音：
- [One Little Triumph](https://app.sessions.blue/browse?trackId=408157)
- [A Certain Lightness](https://app.sessions.blue/browse?trackId=408158)
- [Tuck and Point](https://app.sessions.blue/browse?trackId=408156)

[作者授权说明](https://www.sessions.blue/licensing/) · [CC BY‑NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)。非商业分享时保留曲目、署名及许可信息；商业用途需另行授权。
