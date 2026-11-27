# 后训练的困局 · CS336 Lecture 15（上）

从 Remotion Studio 打开整集，或在 **Shots** 中单看一镜。音频、字幕和配色共用一张 60 fps 帧表，动画在 Chromium 原生画图；可以直接改对象与动效，再单片或整片重导。

```bash
# Install Poppler utilities first (pdftocairo, pdftoppm, pdftotext).
python3 scripts/restore-paper-plates.py --fetch
npm ci
npm run studio
```

本机打开 `http://127.0.0.1:3095/Lecture15Upper`。Studio 默认只监听本机；没有授权 AAC 时只看画面。四个论文图板由 arXiv v1 现场裁出，已持有原 PDF 时用 `--pdf 路径` 代替 `--fetch`。

## 改一镜

- `src/data/cut.json`：帧数、动作锚点和字幕。镜内帧从零起，字幕左闭右开。五章起点和六段算例可在 `docs` 查找。
- `src/Edit.tsx`：按同一张帧表排列 38 个独立镜头；`src/scene` 里是实际绘制和动作；`src/stage.ts` 是章门、镜头公用的几何动作。
- `public/plates` 是静态公式字图与论文图，各镜的动画源不是视频素材。新制作按 [视觉宪法 v2](VISUAL_CONSTITUTION_v2.md)；[本集定版记录](VISUAL_CONSTITUTION.md) 标明已验收的时钟和例外，`ART-DIRECTION.md` 说明镜头之间怎么延续。

以分块注意力 c17 为例：

```bash
node scripts/lint-visuals.mjs
npm run check:frames
npm run still -- c17 build/c17.png --frame=2200
npm run render:shots -- c17 --with-joins --replace
```

`--with-joins` 一起更新借用了该镜首尾的相邻切片。改动横跨两镜的物件时，仍应同时更新两边的画法。Git 中保留原生渲染源码。从源生成全部 38 个干净切片到 `build/native-shots`：`npm run render:shots -- --replace`。在本机安装 FFmpeg/ffprobe 后，可用 `npm run export -- silent` 无损拼接画面并保留字幕与章节。重画与导出会先运行视觉检查；看 Studio 或试渲单帧不受影响。

## 接回有声版

对应的双音轨母版第一轨是旁白加配乐，第二轨是纯旁白。复剪包没有原始参考录音、声纹编码或音频母带。如需在 Studio 听到正片声音，先从同版母版取 AAC：

```bash
mkdir -p public/audio/composition-ost-v1
ffmpeg -i "/路径/CS336-L15-上集-双音轨母版.mp4" -map 0:a:0 -c:a copy public/audio/composition-ost-v1/mix.m4a
ffmpeg -i "/路径/CS336-L15-上集-双音轨母版.mp4" -map 0:a:1 -c:a copy public/audio/composition-ost-v1/dialogue.m4a
```

保持两轨从整片第零帧起。只改画面不改变声轨；若改了镜长，在 cut.json 中先重排字幕、配音与章间接点，再导出。导出命令按当前帧表生成字幕和章表；如需单独更新 docs，运行 npm run sidecars。

```bash
npm run export -- master
npm run export -- share
```

母版可切换旁白与字幕；分享版压印中文字幕。原旁白由课题组服务器的 Drama 3 用《科普声音》生成，六段算例按实际口播落镜，短接录的调速限制为 0.97–1.04×。

资料和图表出处见 `sources.md`。

## 导出封面

`npm run still -- Cover build/cover.png` 单独输出 1920×1080 封面。底图是双音轨母版 14:41.000（整片第 52860 帧）的无字幕画面。位置、标题与副标在 `src/data/cover.json`，不会改动正片。

## 细调原声

复用本集提供的五首独立 WAV 和提问铃音。只改画面或旁白位置不变时，上面的 AAC 复剪步骤就够了。要重新配平音乐，在装有 NumPy、SciPy、SoundFile 和 FFmpeg 的 Python 环境里，直接用同版双音轨母版：

```bash
python3 scripts/mix-ost.py --tracks "/路径/CS336-L15-Part1-OST" \
  --master "/路径/CS336-L15-上集-双音轨母版.mp4" --out build/ost-mix
```

已持有同版 48 kHz 单声道旁白 WAV 时，可用 `--dialogue "/路径/旁白.wav"` 代替 `--master`。精修包络、EQ、四次铃音和乐章接点见 `src/data/ost.json`。脚本只给配乐做分段 EQ 和随人声避让。输出 `mix.wav` 是 48 kHz、24 位立体声；`music-only.wav` 可在剪辑台试听不带人声和铃音的音乐。要导出新混音版，把 `mix.wav` 编成 `public/audio/composition-ost-v1/mix.m4a`，保留同一时钟上的纯旁白，再导出母版。原曲和提示音原文件不包含在复剪包。
