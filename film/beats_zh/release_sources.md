# CS336 第 12 讲 · Beat 0–1 中文试听版出处

片中数字按下列快照重绘。示例预算为每任务 1 美元，基准、价格、偏好和用量各按其自身口径比较。

## 00:59 · Artificial Analysis：智能指数与每任务成本

[真实散点图](https://artificialanalysis.ai/models?cost=intelligence-vs-cost-per-task)，快照：2026-11-24，Intelligence Index v5.0.1。[计算口径](https://artificialanalysis.ai/methodology)：横轴是同一评测组合的加权每任务美元成本，使用对数刻度。26 个默认配置有完整数据，画面选出 20 个，并保留这 26 个配置中的全部六个非支配点。

| 配置 | 智能指数 | 美元/任务 | 帕累托前沿 |
|---|---:|---:|:---:|
| Muse Ember (Max) | 36.0213 | 0.135936 | 是 |
| GPT-6 Luna (Max) | 27.8552 | 0.151956 | — |
| MiMo-V2.6-Pro | 29.8898 | 0.257180 | — |
| Beam 1.0 | 17.7307 | 0.284407 | — |
| Claude Haiku 5.5 (Max) | 36.4845 | 0.411007 | 是 |
| Nemotron 3.5 Super VL | 13.6203 | 0.481809 | — |
| DeepSeek V4.1 Flash 1017 (Max) | 32.5896 | 0.602105 | — |
| GPT-6.1 Terra (Max) | 51.3265 | 0.961108 | 是 |
| GPT-6.2 Sol (Max) | 57.2576 | 1.014380 | 是 |
| Tencent Hy4 | 34.5552 | 1.031106 | — |
| Gemini 4 Hydrogen (Xhigh) | 53.9192 | 3.160159 | — |
| Qwen4 Max | 42.8915 | 3.268133 | — |
| Kimi K3.1 Pro | 46.4526 | 3.681200 | — |
| GPT-6.2 Astra (Max) | 62.1388 | 3.997906 | 是 |
| GLM-5.3 (Max) | 31.6534 | 5.009265 | — |
| Gemini 4 Neon (Xhigh) | 61.3982 | 6.444838 | — |
| Gemini 4 Carbon (High) | 60.0257 | 7.755546 | — |
| Grok 4.7 (Xhigh) | 35.4850 | 7.771539 | — |
| Claude Opus 5.5 (Max, Default Fallback) | 59.1060 | 10.036410 | — |
| Claude Fable 5.2 (Max, Default Fallback) | 64.5636 | 26.538558 | 是 |

## 01:37 · Arena：一次盲投与总体榜单

[Arena Human Preference 140k · 第 162 行](https://huggingface.co/datasets/lmarena-ai/arena-human-preference-140k/viewer/default/train?row=162)（[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)）。2025-07-08 对战：`305a4d3b-1e1c-4b38-b48e-84d87ed78b46`。提示要求写机器人短篇故事；画面用原创线稿与改写片段表示两篇故事。读者选择 B（Claude Opus 4 Thinking 16K），A 是 Gemini 2.5 Pro。投票网络示意成对比较的汇集；之后展示的是另一个日期的 [Text Arena overall 快照](https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset)。

中文旁白用「类似 Elo 的评级」解释成对偏好怎样变成分数。Arena 起初使用 Elo，画面所示较新快照用的是同样建立在成对比较上的 Bradley–Terry 模型。[Arena 官方方法](https://arena.ai/blog/arena-rank) · [Elo 到 Bradley–Terry 的迁移记录](https://arena.ai/blog/chatbot-arena-update)。

## Arena 画面中的八行

模型分数和区间来自同一份 Text Arena overall 快照。区间展示估计的不确定性；[Arena-Rank 的成对比较方法](https://arena.ai/blog/arena-rank)可查看计算细节。

| 名次 | 配置 | 分数 | 公布区间 |
|---:|---|---:|:---|
| 1 | Gemini 4 Carbon (High) | 1538.9 | 1529.3–1548.4 |
| 2 | Gemini 4 Argon (High) | 1527.7 | 1522.7–1532.7 |
| 3 | Gemini 4 Neon (High) | 1522.9 | 1514.5–1531.3 |
| 4 | Claude Opus 5.5 (High) | 1514.1 | 1508.5–1519.8 |
| 5 | Claude Fable 5.1 (Max) | 1511.8 | 1506.5–1517.0 |
| 6 | Claude Opus 5 (Max) | 1506.2 | 1501.5–1510.9 |
| 7 | Muse Wonder (Max) | 1503.7 | 1498.0–1509.3 |
| 8 | Claude Opus 5 (High) | 1502.2 | 1498.6–1505.8 |

## 02:08 · OpenRouter：公开 API 词元用量

[OpenRouter Today](https://openrouter.ai/rankings?view=daily)（CC BY 4.0），访问于 2026-11-24，页面数据截至 2026-11-23。比例以表中前六名显示值之和 **23.83 万亿词元** 为分母。用量合计输入与输出词元，统计的是用量而非金额；私人请求不在公开统计内。

| 名次 | 端点显示名 | 万亿词元 | 占画面六项 |
|---:|---|---:|---:|
| 1 | DeepSeek V4.1 Flash 1017 | 11.3 | 47.4% |
| 2 | Hy4 flash | 5.8 | 24.3% |
| 3 | DeepSeek V4.1 Flash | 2.36 | 9.9% |
| 4 | GLM 5.3 Flash | 2.06 | 8.6% |
| 5 | GPT-6 Luna | 1.3 | 5.5% |
| 6 | Claude Opus 5.5 | 1.01 | 4.2% |

## 与 OpenRouter 同段 · 用四把尺看 GPT‑6 Luna

蓝点依次是抽样的智能指数 **#18/20**、从便宜到贵的成本 **#2/20**、Arena 文本总榜 **#176**，以及 OpenRouter 当日用量 **#5**。前两项与 Arena 按 Max 配置展示，OpenRouter 汇总该模型端点。各项就其本身的样本、单位与统计期读数，画面不使用统一排名刻度。Intelligence Index 是综合评分；流量为公开词元用量，不是金额，也不是分别核定的付费请求数。

## 02:17 · 比较方法与比较系统

共享数据划分能统一一部分条件。把分差归因于架构或优化器，还要保持其余会影响结果的因素不变。画面左边是一项只改方法的对照实验；右边是在同一测试条件下比较两套成品。公开训练流程、控制变量的基础模型研究同样可以做方法比较。

## 03:06 · modded-nanogpt：到达同一条线的耗时

使用[主赛道公开记录](https://github.com/KellerJordan/modded-nanogpt/blob/master/README.md#world-record-history)第 1–20 条（2024-05-28 至 2025-01-16），在[计时协议后来调整](https://github.com/KellerJordan/modded-nanogpt/blob/master/README.md#timing-change-after-record-21)之前止步。按[规则](https://github.com/KellerJordan/modded-nanogpt/blob/master/README.md#rules)比较固定词元流和同类硬件下，在 FineWeb 验证集达到 **3.28** 交叉熵所用的墙钟时间。片中「固定」指规则要求沿用底层训练与验证词元流；实际消耗的训练词元数随记录变化。工作台上的单趟验证损失曲线是机制示意。阶梯纵轴是各次刷新纪录的分钟数，**45 → 2.992 分钟**；下方的 3.28 是共同验证目标。

中间里程碑取自 [2024-11-03 的第 8 条日志](https://github.com/KellerJordan/modded-nanogpt/blob/master/records/track_1_short/2024-11-03_UntieEmbed/d6b50d71-f419-4d26-bb39-a60d55ae7a04.txt)：取消输入嵌入与输出头的权重共享，记录为 **10.8 分钟**。


## 片尾的八个词元

前文为 `The room was quiet.`；续写为 `The small cat sat on the mat.`。使用 [HuggingFaceTB/SmolLM2-135M](https://huggingface.co/HuggingFaceTB/SmolLM2-135M) 基座模型与原生分词器。将原文前缀送给模型，在每一步从完整词表分布读取原文词元的条件概率。动画的条长使用同一比例，不按每格单独缩放。

| 词元 | 条件概率 |
|---|---:|
| `The` | 11.378953% |
| `small` | 0.334709% |
| `cat` | 0.044875% |
| `sat` | 10.703619% |
| `on` | 33.024360% |
| `the` | 57.329133% |
| `mat` | 0.251435% |
| `.` | 6.958633% |
 
## 旁白与配乐

中文旁白按六个场景分段录制，每个场景使用完整的一条普通话合成口播（Qwen3‑TTS 原生 Dylan 音色）。字幕与动画按中文词级时间重对齐，两处推演问句留有思考时间。

配乐由 **Blue Dot Sessions** 创作、录制。使用作者提供的 MP3，按段落截取、淡入淡出并混音：

- 00:00–00:57 · [Tuck and Point](https://app.sessions.blue/browse?trackId=408156) by Blue Dot Sessions
- 00:59–02:23 · [A Certain Lightness](https://app.sessions.blue/browse?trackId=408158) by Blue Dot Sessions
- 02:26–03:48 · [One Little Triumph](https://app.sessions.blue/browse?trackId=408157) by Blue Dot Sessions

授权：[Blue Dot Sessions 官方说明](https://www.sessions.blue/licensing/) · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)。非商业分享时请保留以上署名与授权信息；商业用途需另行获许可。
