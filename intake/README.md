# 待制作讲次

从仓库根目录执行：

~~~bash
python3 pipeline/lecture.py new l16 --title '本讲片名' --format engineering
~~~

将输入填进生成的目录：

| 文件 | 放什么 |
| --- | --- |
| `brief.json` | 讲次、片名、时长类型；核完后把 `status` 从 `draft` 改成 `ready` |
| `narration.json` | 按意群排列的 `sub`、`tts`、情绪、候选数与种子 |
| `storyboard.md` | 对应意群号的物件、动作、停顿、切点与来源 |
| `music.json` | 各乐段提示词、关系调、3 个试听种子和预估长轨 |
| `sources.md` | 讲义、论文、页码、真实数据/代码和素材许可 |

[小型输入例](../pipeline/example-intake/) 只示范格式。公开仓库只放可公开的文字与源；暂不公开的稿件放在私有工作副本。参见 [制作流程](../docs/production-flow.md)。

## 发给 Gemini 的交稿模板

附上原讲材料、这次的范围和[视觉宪法 v2](../production/cs336-lecture-animation/references/VISUAL_CONSTITUTION_v2.md)，再发这段：

> 按文件分别交稿，所有分镜和音乐入口引用同一个意群号。
>
> - **narration.json**：JSON 数组。每项写 `id`、屏幕字幕 `sub`、独立送读 `tts`、`kind`、`emotion`、`N` 和整数 `seed`。字幕保留公式的可读写法，送读展开数字与符号。核心问句和反转各写一条正文、设四候选，不写四套台词。
> - **storyboard.md**：每个意群写清「物件是什么、哪一个量动、什么始终不动」。用口播原词标记动作，秒数只作粗估。正文不加标题或解释贴片；标出首问、OP、内部问句后的章门、观众思考窗和 END。
> - **music.json**：顶层 `model` 为 `stabilityai/stable-audio-3-medium`，另有相配的 `global_musical_key` 和 `tracks`。每段给 `id`、整数秒 `duration_seconds`、三个不同的 `preview_seeds` 和以 `TrackType: Music, VocalType: Instrumental` 开头的 `prompt`。长乐章拆开写，不用短段循环。
> - **sources.md**：关键数字对应原表、论文版本和页码；自己编的算例给出输入与算式。把尚未查明的说法单列，不当作已核准事实写入旁白。

`brief.json` 留给制作者锁定范围。先核准再把 `status` 改成 `ready`，随后运行 `python3 pipeline/lecture.py check <讲次>`。
