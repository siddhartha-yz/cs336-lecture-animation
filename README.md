# cs336-lecture 动画

把 Stanford CS336 做成可复剪的中文数学动画。正片、片源、口播和声音各有自己的入口；下一讲可以从同一套帧钟、门禁和复剪方法开工。

| 讲次 | 从这里进 |
| --- | --- |
| **Lecture 12 · 能力的影子** | [原说明与复剪命令](LECTURE12.md) · [v6.2.0 发布页](https://github.com/siddhartha-yz/cs336-lecture-animation/releases/tag/v6.2.0) |
| **Lecture 15 上 · 后训练的困局** | [Remotion 工程](lectures/l15-upper/) · [镜表](lectures/l15-upper/docs/镜表.csv) · [来源](lectures/l15-upper/sources.md) |

## 开一讲

~~~bash
python3 pipeline/lecture.py new l16 --title '本讲片名' --format engineering
~~~

把 Gemini 给的字幕稿、送读稿、分镜和配乐方案放进 `intake/l16/`。整理并核完内容后：

~~~bash
python3 pipeline/lecture.py check l16
python3 pipeline/lecture.py bootstrap l16
~~~

生成 `lectures/l16/` 后，先替换一段最能说明机制的样片，再逐镜制作。新讲用 Remotion；Lecture 12 的 Cairo 入口、Git 历史和 Release 保留。

- [从 Gemini 底稿到审片返工](docs/production-flow.md)
- [视觉宪法 v2](production/cs336-lecture-animation/references/VISUAL_CONSTITUTION_v2.md)
- [已验证的镜头做法](production/cs336-lecture-animation/references/shot-study.md)

GitHub 检查源稿、帧钟和渲染。Drama 3「科普声音」和 Stable Audio 3 Medium 在课题组服务器私有运行；模型、参考音频、声纹码及审片音视频不进 Git。
