# cs336-lecture动画

把 Stanford CS336 做成可复剪的中文数学动画。正片、片源、口播和声音各有自己的入口；下一讲可以从同一套帧钟、门禁和复剪方法开工。

| 讲次 | 从这里进 |
| --- | --- |
| **Lecture 12 · 能力的影子** | [原说明与复剪命令](LECTURE12.md) · [v6.2.0 发布页](https://github.com/siddhartha-yz/cs336-lecture-animation/releases/tag/v6.2.0) |
| **Lecture 15 上 · 后训练的困局** | [Remotion 工程](lectures/l15-upper/) · [镜表](lectures/l15-upper/docs/镜表.csv) · [来源](lectures/l15-upper/sources.md) |

## 开一讲或返修一版

[用同一个 Draft PR 跑完整轮制作](docs/pr-workflow.md)：Gemini 给规划、审实际成片；ChatGPT 实现、渲染和返工；你确认通过后再合并。一个讲次的一轮工作留在同一个 PR，换审片版就更新候选，不另开讨论。

新讲先建收稿目录：

~~~bash
python3 pipeline/lecture.py new l16 --title '本讲片名' --format engineering
~~~

用[交稿模板](intake/)让 Gemini 分开给字幕、送读、分镜与配乐。核完事实和素材，把 `brief.json` 的 `status` 改成 `ready`，再运行：

~~~bash
python3 pipeline/lecture.py check l16
python3 pipeline/lecture.py bootstrap l16
~~~

- [从底稿到成片的制作流程](docs/production-flow.md) · [视觉宪法 v2](production/cs336-lecture-animation/references/VISUAL_CONSTITUTION_v2.md) · [已验证的镜头做法](production/cs336-lecture-animation/references/shot-study.md)

GitHub 检查源码和交接。Drama 3「科普声音」、Stable Audio 3 Medium 和实际审片文件留在私有制作环境。
