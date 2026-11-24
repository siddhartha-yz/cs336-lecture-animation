# 配乐与素材

课程出处：[Stanford CS336 · Spring 2025 · Lecture 12: Evaluation](https://cs336.stanford.edu/spring2025/)。本项目用自行绘制的几何动画和讲解重建课程中的问题。课程讲义全文、作为美术参照的第三方视频和录音不随仓库分发。

## 精剪版配乐

音乐及录音：**Blue Dot Sessions**。使用作者提供的三首 MP3 的片段，按镜头截取、淡入淡出、在问句处留白，并与旁白混音。

- [Tuck and Point](https://app.sessions.blue/browse?trackId=408156)
- [A Certain Lightness](https://app.sessions.blue/browse?trackId=408158)
- [One Little Triumph](https://app.sessions.blue/browse?trackId=408157)

这些曲目随本个人、非商业教育项目按 [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) 使用。[作者的使用说明](https://www.sessions.blue/licensing/)。再分享带配乐的影片或剪辑混音时保留署名、链接和剪辑说明；商业使用须按作者许可办理。需要重编配乐时从曲目页取得原曲。两部早期 20 分钟版用项目自己的程序配乐，代码在 [score.py](../film/score.py) 和 [soundtrack.py](../film/v2/soundtrack.py)。

## 数据与声音

公开榜单是制作时的固定快照。Artificial Analysis 的分数与成本、Arena 的偏好与区间、OpenRouter 的词元用量、NanoGPT 的耗时各有自己的分母和日期。[Beat 0–1 逐项来源与署名](../film/beats_final/sources.md) · [Beat 2 复算口径与来源](../film/beat2/sources.md)。图表按数据重绘；Arena 的盲选故事用原创线稿和改写片段表示。

精剪成片使用 [Qwen3-TTS CustomVoice](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice) 内置声线（英语 Aiden、中文 Dylan）。模型权重由原作者发布，仓库只附项目录制的旁白、成片混音和制作文件。公开仓库本身不改变曲目、数据集、模型或其他素材的原许可。
