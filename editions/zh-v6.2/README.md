# 能力的影子 · v6.2 复剪工程

Stanford CS336 第十二讲｜31:45.5 · 35 镜 · 1920 × 1080 / 60 fps

看一个镜头的起止、画出一帧，再决定改哪里。在本目录运行：

```sh
python3 复剪.py --list
/usr/bin/python3 复剪.py --still door2 2.35 --out build/困惑度过渡.png
```

`2.35` 是镜头内的秒数。画单帧只用系统 Python 和绘图库，不用显卡。

## 把改过的一镜接回全片

从 [v6.2.0 分镜包](https://github.com/siddhartha-yz/cs336-lecture12-evaluation/releases/download/v6.2.0/cs336-l12-zh-editing-kit.zip) 解压，35 个干净切片已放在 `film/film_zh_v6/shots/`。也可以把这一个目录复制到仓库的同一位置。在含有 `复剪.py` 的工程根目录运行：

```sh
/usr/bin/python3 复剪.py --draw door2 --with-next
python3 复剪.py --assemble-silent --out build/无声修订版.mp4
```

第一条把问句的一镜和它接入的困惑度镜头写到 `build/shots/`。第二条优先使用重画切片，其余原样拼接，保留九章和可切换的中文字幕。只用现成的 35 镜装配时，跳过第一条。重画视频需要 NVIDIA NVENC、CUDA 和 libass；拼接已有 MP4 只需要 FFmpeg 和 ffprobe。

如果你手上有同一版本的本地双音轨母版，可改用 `python3 复剪.py --assemble /路径/双音轨母版.mp4 --out build/有声修订版.mp4` 接回同长度的两条音轨。公开版本只带无声画面和配乐时间表。

| 想改哪里 | 打开 |
|---|---|
| 手写片头、片尾落款 | [opening_carriage6.py](film/film_zh_v6/opening_carriage6.py) |
| 问句留白和下一镜的入口 | [question_doors6.py](film/film_zh_v6/question_doors6.py) |
| 单镜字级时钟、字幕及章节 | [scene-clocks/](film/film_zh_v6/scene-clocks) · [字幕](film/film_zh_v6/edition/CS336-L12-能力的影子-v6.2.srt) · [逐字稿与章节](film/film_zh_v6/edition/CS336-L12-能力的影子-v6.2-逐字稿与章节.md) |
| 曲目、淡变和问句提示音的时码 | [cuebook.json](film/film_zh_v6/audio/cuebook.json) |
| 实测数据、图片与音乐归属 | [数据与配乐](film/film_zh_v6/edition/CS336-L12-能力的影子-v6.2-数据与配乐.md) |

重画依赖：系统 Python 3、PyCairo、PyGObject、PangoCairo、librsvg，及 Noto Serif CJK SC、Noto Sans CJK、Latin Modern、DejaVu 字体。随附组件的许可见 [licenses/](licenses)。
