# 第 12 讲：把 v6.2.0 重新拼出来

**固定输入**：[GitHub v6.2.0](https://github.com/siddhartha-yz/cs336-lecture12-evaluation/releases/tag/v6.2.0) 的 `cs336-l12-zh-editing-kit.zip`（约 794 MB）。35 个干净无声镜头、531 条字幕、九章、114,330 帧，时长 **31:45.5**。用同一份镜表回装，不需要模型、不重画全片。Release 里另有直接看的压印字幕无声 MP4。

## 回装和封面

在新工作区运行，所有路径由调用者给定。已下载 ZIP 时直接用，不要重新拉大文件。

```bash
# 尚未下载时（只取复剪包）
gh release download v6.2.0 -R siddhartha-yz/cs336-lecture12-evaluation \
  -p cs336-l12-zh-editing-kit.zip -D work

/usr/bin/python3 "$SKILL/scripts/replay_l12.py" \
  --kit work/cs336-l12-zh-editing-kit.zip --out outputs/L12-无声复现.mp4
```

`$SKILL` 是本技能目录。若已有 ZIP 解包后的工程根目录，用 `--project 路径` 代替 `--kit`；不依赖原工作目录。若有批准的 **同版双音轨 v6.2 母版**（一轨立体声混音、一轨单声道旁白），在同一命令加 `--master 路径`，原样复制 AAC，仍是可切换字幕。单音轨高清分享版不作为双轨母版。公开包没有原参考录音、干声和曲目音频；想从头演出要另行提供这些授权输入，重新生成的表演不能承诺与原声逐样本一致。

只要复画定版（小号宋体、无副标、31:15 双长方体、5×5 彩格、金阶梯）：

```bash
/usr/bin/python3 "$SKILL/scripts/replay_l12.py" \
  --project 路径/解包根目录 --cover outputs/L12-封面.png
```

封面也可直接用 Git tag 的 `editions/zh-v6.2` 源码目录，不需要 ZIP 里的视频切片。画单帧和封面需 Cairo、PangoCairo 与对应字体；已有镜头的拼装只用 FFmpeg/ffprobe。

如果默认临时目录的额度不够解开约 794 MB，先在工作区建目录，用 `TMPDIR=工作区/临时目录` 运行同一命令；也可以自己解包后走 `--project`。这不改变原包或镜头。

## 从一镜继续

从解包根目录的 `复剪.py` 进入：`--list` 看镜表，`--still door2 2.35 --out build/检查.png` 查看分镜内秒数，`--draw door2 --with-next` 画问句和它接入的下一镜。最后用 `--assemble-silent` 或 `--assemble 本地双音轨母版` 复用未动切片。无字幕镜头和压印字幕母版用途不同，别混到一个剪辑轨里。

| 需要什么 | 固定版位置（相对于解包根目录） |
|---|---|
| 镜头编号和时长 | `film/film_zh_v6/book/scenes.json` |
| 字词时间、口播与留白 | `film/film_zh_v6/scene-clocks/*.json` |
| 显影 / 拼装 | `film/film_zh_v6/shoot4.py` · `mux4.py` |
| 匀速镜头与公式字形 | `film/film_zh_v6/motion6.py` · `outlines5.py` |
| 片头、原片尾和六处问句 | `film/film_zh_v6/opening_carriage6.py` · `question_doors6.py` |
| 原始事实和素材署名 | `film/film_zh_v6/edition/*-数据与配乐.md` |
| 26:25 音乐交叠、提示音、停顿 | `film/film_zh_v6/audio/cuebook.json` |

现场回归：01:35.9 的手写片头只含片名和五组图形；六个问句留白入场无前章残影，字退完才揭开下镜实际首帧；31:42 左右黑底白字的原落款。L12 的这些已验收画面是参照，不是所有新讲都要复用的镜头。
