# 从一个镜头接着剪

想改 GPQA 的博士出题镜头，先看第 3-3 镜的第 28 秒，再打开 [studio_science.py](film/film_zh_v3/studio_science.py) 里的 `gpqa`。所有镜头按同一份逐字时钟绘制，全片共 9 章、33 镜，21 分 28 秒。

在本目录运行：

```bash
/usr/bin/python3 复现.py --list
/usr/bin/python3 复现.py --still 3-3 28.0 --width 1280
```

第二条命令会生成 `build/3-3-28.00.png`。这里的 28 秒是镜头内时间。只看单帧不用 GPU。

## 把新镜头接回全片

从 [v3.1.0 的分镜包](https://github.com/siddhartha-yz/cs336-lecture12-evaluation/releases/download/v3.1.0/cs336-l12-zh-editing-kit.zip) 解压后，可以直接重画并装配：

```bash
/usr/bin/python3 复现.py --draw 3-3 --with-next
/usr/bin/python3 复现.py --assemble-silent --out build/无声修订版.mp4
```

新切片在 `build/shots/`，原来的 33 个切片在 `film/film_zh_v3/shots/`。装配时优先使用新切片，其余直接拼回；成片保留九章和可切换的中文字幕，没有音轨。单改中段不用重画下一镜；如果改了镜尾，用 `--with-next` 更新下一镜的入口。直接从 Git 克隆时，代码和字级时钟已经齐全；把分镜包中的 `shots/` 放到上述路径，就能沿用其余镜头。

手边有本地双音轨母版时，仍可用 `/usr/bin/python3 复现.py --assemble /路径/母版.mp4 --out build/有声修订版.mp4` 原样接回两条音轨；`--burn build/有声修订版.mp4 --out build/有声修订版-字幕版.mp4` 可把字幕印在画面上。

## 顺着口播找画面

| 想改什么 | 去哪儿 |
|---|---|
| 某个词出现时谁动 | `film/film_zh_v3/scenes/镜头.json` 的实际字起止；`timeline3.py` 的 `clock(k).at('原词')` |
| 镜头归属、着色、原笔画路径 | `stage3.py`、`pigments.py`、`ink_words.py`；`stage3.CUSTOM` 指向每个专门场景 |
| 摄影机和两镜的衔接 | `lens.py`、`v3joins.py`；旧画面的字体变换随镜头，不重新测量字号 |
| 试卷与人物、胜率与长度控制 | `studio_saturation.py`、`studio_science.py`、`studio_examples.py`、`studio_votes.py`、`studio_preference.py` |
| 真补丁、ARC、行为评测与语料窗口 | `studio_engineering.py`、`studio_tests.py`、`studio_behaviors.py`、`studio_corpus.py` |
| 中文排字 | `press3.py`、`edition3.py` |
| 配乐与六个问句的提示音 | `music_layout.py` 标出四个乐章中八首曲子的起止与交叠；`sound3.py` 控制人声下的音量，实际时码在 `audio/cuebook.json` |
| 开头延续下来的原工程 | `film/film_zh_v2/`、`film/beats_zh/` 等目录是被 v3 直接调用的基础画面和数学矢量 |

## 工作环境与资料

Linux 系统 Python 3，Cairo、PyGObject（含 Cairo 桥接）、Pango、librsvg；字体为 Noto Serif CJK SC、Noto Sans CJK、DejaVu 和 Latin Modern。Ubuntu 对应软件包包括 `python3-cairo python3-gi python3-gi-cairo gir1.2-pango-1.0 gir1.2-rsvg-2.0 fonts-noto-cjk fonts-lmodern`。重画视频使用带 CUDA、NVENC 和 libass 的 FFmpeg；拼接已有切片只需要 FFmpeg 与 ffprobe。

[逐字稿与章节](逐字稿与章节.md) · [中文字幕](中文字幕.srt) · [问句与镜头蓝图](问句精简与动效蓝图.md) · [数据与配乐来源](数据与配乐.md)。本地旁白使用 Drama 3。配乐表保留八首曲子的入点、交接和六处提示音落点；音频素材留在本地。
