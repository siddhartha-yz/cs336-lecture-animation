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
