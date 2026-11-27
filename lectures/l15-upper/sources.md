# Lecture 15 上集 · 资料与画面口径

课程：[Stanford CS336 · Spring 2026](https://cs336.stanford.edu/)；Tatsunori Hashimoto，2026-05-18。[原讲课视频](https://www.youtube.com/watch?v=2oH6PWPrYFo) · [原幻灯](https://github.com/stanford-cs336/lectures/blob/main/lecture_15.pdf)。上集覆盖用户讲义第 15.1–15.4 节，终点是带 KL 惩罚的固定提示目标；DPO 仅留作片尾悬念。

| 镜头 | 来源与读法 |
|---|---|
| C01–03 基座续写、知识边界 | 煮蛋续写是教学例，候选条没有数值刻度；选中的开头接回同一行。曲线来自 [Gekhman et al., EMNLP 2024](https://aclanthology.org/2024.emnlp-main.444/) 的 Fig. 3a：PaLM 2-S 封闭式事实问答，横轴是微调样本中 SliCK 判为 Unknown 的比例，纵轴是测试准确率；只取早停与训练至收敛两列，数据点用纵坐标刻线校准原图栅格、按作者线色读曲线中心，精度受源图限制。 |
| C04–06 SFT 谱系、两种包装 | 从 [Ouyang et al., 2022, Fig. 2](https://arxiv.org/abs/2203.02155) 直接从论文 PDF 高分辨率裁取示范微调栏的三个图形片段：提示、示范和监督训练；例句保留在实际图形中。情感分类问法来自 [FLAN 2021 的 SST-2 模板](https://github.com/google-research/FLAN/blob/main/flan/templates.py)，影评短片段及标签来自 [Stanford SST-2 train](https://huggingface.co/datasets/stanfordnlp/sst2) 第 15、16、17、18、22 行（数据集 idx），FLAN 问法为中文呈现。数据集顺序据课程幻灯第 9 页。长度效应见 [Dubois et al., Length-Controlled AlpacaEval](https://arxiv.org/abs/2404.04475)。 |
| C07–09 LIMA、知识与行为 | [LIMA (Zhou et al., 2023)](https://arxiv.org/abs/2305.11206) 的 65B LLaMA + 1,000 条示范支持浅层对齐假说的讨论。六类条长以该论文表 1 训练集 200/200/200/150/50/200 条为准；后续四行是图 4 测试提示词与实际输出的中文摘意。安全小样本变化据课程幻灯第 26 页；约 500 条是例子，拒答/正常回答的文字是示意。 |
| C10 损失掩码 | 目标索引对齐到真实答案词元。提示词位置不单列损失；答案损失可以经由上下文计算图影响提示词相关表征。三个目标概率 0.50、0.25、0.80 是算例。 |
| C12–14 开放数据与参考策略 | [NVIDIA Nemotron-SFT-OpenCode-v1](https://huggingface.co/datasets/nvidia/Nemotron-SFT-OpenCode-v1) 公布合成指令与工具轨迹。C12 的异步代码是自写最小例，实际运行输出为 `A B`，不是数据集原行。C13 用自写的二分查找单测演示失败、返回输出和重试；原数据集的指标不从该例推算。[Marin 开放记录](https://marin.community/blog/2025/05/19/announcement/) 公布 8B Base → Instruct；冻结 SFT 检查点指 [InstructGPT 风格的 RLHF](https://arxiv.org/abs/2203.02155)。 |
| C15–17 选格与打包 | [Krell et al., Sequence Packing](https://arxiv.org/abs/2107.02027) 与本片 PyTorch 实例。长度 [3,2,2]、每槽长 7，先占 7/21 格，打包后 7/7。格数比不等同于速度比。第二处浅米白切面是针对该算例的实代码，True 为可见，False 转 −∞。 |
| C18 两种掩码 | 损失掩码选的是哪些目标位置计损失；分块因果注意力掩码选的是哪些位置可互相作为上下文。左图的 0 不切断右图意义下的注意力。 |
| C19–25 拟合、验证、偏好 | 分布、奖励曲面、胜率滑块和 A/B 盲测是教学算例。Bradley–Terry 与奖励模型负对数似然见 [Ouyang et al., §3.5](https://arxiv.org/abs/2203.02155)。G–V 的任务依赖见原课第 33 页。评审模型有时偏好长文：[Zheng et al., 2023](https://arxiv.org/abs/2306.05685)。 |
| C26–28 过度优化与 KL | 金/青双轨来自 [Stiennon et al. (2020) Fig. 5](https://arxiv.org/abs/2009.01325)：改变 PPO 的 KL 惩罚力度，比较摘要相对参考摘要被选中的比例；横轴为相对监督基线的 KL，按原图的 log(1+KL) 间距展示。数据点从论文 PDF 第 8 页图形的两条矢量折线和印刷刻线恢复；横轴的七个刻度不是折线的七个采样点。口播中客套长文是教学例，不当作该实验样本。[Gao et al. (2022)](https://arxiv.org/abs/2210.10760) 另用固定金标准奖励模型得到相关证据。橡皮筋表现惩罚方向；KL 衡量概率分布的偏离。 |
| C29–34 PPO 与结尾 | 第三处纸面取 [Ouyang et al., Eq. (2)](https://arxiv.org/abs/2203.02155) 的 PPO-ptx 方程。原 PDF 第 9 页按 480 dpi 输出；在图层中保留 2586×417 的原式字形、把白纸底融入画面底色。红线下的英文短句来自讲者评语（原幻灯 p.51）。C30 用四块表示常驻权重，并分出训练角色的梯度和优化器状态；只演示相对大小和两处放置，不引用特定模型的显存数。片尾回到固定提示目标，[Rafailov et al., 2023](https://arxiv.org/abs/2305.18290) 是续讲引线。 |

上集配乐来自本项目的 CS336-L15-Part1-OST，保留 M1-C、M2-A、M3-A、M4-B、M5-C 五首原声与 SFX-C 铃音。四次铃音贴问句落点；乐章入点与精修参数在 src/data/ost.json。旁白在课题组服务器上用 Drama 3 合成，沿用 Lecture 12 的《科普声音》。两条声轨从母版提取，操作见 README。

C20 两种答法的得分固定为 2、8；改变生成概率，平均得分由 3.2 变为 6.5。C32 的三种后续回报是条件期望示例；估值偏差让单次估计的优势变号，不代表一次偏差就会造成模式崩溃。

## 镜头参照

片头的两行写入、过门清屏与下一镜首帧的开启，参照 [Lecture 12《能力的影子》v6.2.0](https://github.com/siddhartha-yz/cs336-lecture-animation/releases/tag/v6.2.0) 的 `opening_carriage6.py`、`question_doors6.py` 和 `splice4.py`。选择一行、把分数移到归一化结果的展示顺序，参照 3Blue1Brown 的 [《Attention in transformers, step-by-step》](https://www.3blue1brown.com/lessons/attention/) 和[原分镜](https://github.com/3b1b/videos/blob/master/_2024/transformers/attention.py)。本片采用行表示查询、列表示被读取位置；原片的展示约定相反。

片头让选中的续写开头接回原句，参照 3Blue1Brown [《Transformers, the tech behind LLMs》01:37–02:25](https://www.youtube.com/watch?v=wjZofJX0v4M&t=97s) 的续写循环，以及 [候选条与标签的分镜源码](https://github.com/3b1b/videos/blob/master/_2024/transformers/network_flow.py#L612-L667)。

正文的主体、配色和连续动作另参照《压缩即智能 Part 1：重新发明熵》：00:12–01:54 反复使用同一台仪表，08:47–09:08 保持分区图不动、让选择亮起来。本片沿用这种关系；期望回报的面积装置参照 26:37–27:17 的宽度×高度示范。配色表在 src/theme/palette.ts，画法见 ART-DIRECTION.md。

公开仓库不复制 arXiv:2203.02155v1 的图 2 和方程图板；按 [工程说明](README.md) 从官方 PDF 原位裁出四张。还原配方保留已定几何，Poppler 版本间可能有字边栅格差。
