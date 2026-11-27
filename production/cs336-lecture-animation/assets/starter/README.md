# 一个可以直接改的双镜头工程

三根 logits 柱一起上移，右边三项概率一格不动。两个镜头共用同一套几何和镜号时钟。替换 `scenes.py` 的画面和 `cut.json` 的镜表，留用字幕与拼装入口。

```bash
python3 render.py list
/usr/bin/python3 render.py still shift 165 --width 1280 --out build/检查.png
nice -n 12 /usr/bin/python3 render.py shot all --width 1280
python3 render.py assemble --width 1280 --silent --burn --out build/字幕样片.mp4
```

`shift 165` 表示该镜第 165 帧（从 0 起，不是整片秒数）。一镜更新用 `shot shift`，只替换对应宽度的输出。全尺寸省略 `--width`（默认 1920×1080）。要带软字幕，去掉 `--burn`。有铺好的 48 kHz PCM WAV 时，用 `--mix local/screening.wav` 代替 `--silent`；另带纯旁白则加 `--dialogue local/dialogue.wav`。检查接缝时，先分别看前镜末帧和后镜首帧，再决定是否一起重画。

只发一镜审阅时，加 `assemble --scene shift --width 1280 --silent --burn --out build/单镜.mp4`。单镜字幕从 0 起，主镜表和整片字幕不动。

## 运行环境

系统 Python、FFmpeg/ffprobe。绘图要有 PyCairo、PyGObject（含 Cairo 桥接）、PangoCairo、Latin Modern Roman 和 Noto Serif CJK SC。默认视频编码是 NVENC，显式选择 `--codec cpu` 才走低优先级 x264。改 FFmpeg 路径用 `CS336_FFMPEG`。拼接已有切片不用显卡，压印字幕需要 libass。

如果报缺 `gi._gi_cairo`，优先用系统与当前 Python ABI 一致的 `python3-gi-cairo`。只有当前 ABI 与旧工程桥接一致时，可以走：

```bash
export CS336_GI_BRIDGE="/你的v6.2工程根/film/vendor/pango-cairo-gi"
```

可用归档源码 `v6.2.0` tag 下的 `editions/zh-v6.2` 作工程根，不用下载影片。该库是已存档项目的依赖，许可在其 `licenses/pygobject/`。这条环境变量只影响当前绘制，不改系统 Python。所有音轨、参考录音和私人配置放本项目 `local/` 或外部私有路径。
