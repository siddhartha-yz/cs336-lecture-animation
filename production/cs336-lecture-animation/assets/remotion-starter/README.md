# 先看短片，再换成本讲自己的对象

模板里的两个分数会一起变，概率不动。它含五秒 OP、同物续演、一处 4.5 秒预测、四秒章门和一次 0.4 秒清场。模板是显影用短片，无旁白，不是课程成片。

```bash
npm ci
node scripts/lint-visuals.mjs
npm run studio -- --port=3096
```

在浏览器打开 `http://127.0.0.1:3096/Lecture`；单看一镜用 Studio 的 **Shots**。需 Node.js、Chromium/Chrome、FFmpeg/ffprobe（分享版需有 libass）、Fontconfig 的 `fc-scan`。仍用本机浏览器，不自动下载另一支 Chromium；可用 `REMOTION_BROWSER` 指定可执行文件；Node 依赖若已缓存，可执行 `npm ci --offline`。字幕、正文和随工程三套字体共用字库。

## 用一镜换掉样例

1. `src/data/cut.json` 是唯一时钟：60fps，所有字幕与 cue 都是镜内整数帧，字幕区间左闭右开。先用实际选好的录音把词位标入 `beats`，再写数值或高亮变化。换话筒或重录时只改受影响的词位。
2. `src/story.ts` 根据镜号与帧输出 `Stage` 里的物件，`src/stage.ts` 提供两类材质和金色计时弧。正文为主装置命名，在 `stableFrames` 选实际讲解的稳定帧；同一装置用 `carry`，换不相干装置用 `reset`（相邻尾、头共 24 帧空场）。章门开到下一镜原生第一帧，不借图屏。面向观众的字都从 `Stage.text` 走，逐帧检查才看得到。
3. `sources.md` 保留上屏数据、原图出处与量纲。画面、旁白和标题不互相复印。完整约束在 [视觉宪法 v2](VISUAL_CONSTITUTION_v2.md)。

```bash
npm run still -- shift build/shift.png --frame=80
npm run render:shots -- shift --with-joins --replace
npm run render:shots -- --workers=4
npm run export -- silent
npm run captions:check
node scripts/review-frames.mjs build/lecture-silent.mp4
```

结果 `build/lecture-silent.mp4` 带可切换字幕和章节；各镜干净 MP4 在 `build/native-shots/`。重画某镜时，用 `--with-joins` 也重画借该镜首/尾姿态的镜头。替换图片、公式、字体时，按实际引用范围重画。手改代码而没有重画的旧片不算新成片。分享版自动用实际烧字幕的 libass 在 480px 宽检查每条字幕，正文被换行侵占时按口播拆句，不缩字。

### 公式和文献图本地载入

将裁好的 PNG 或排好的 SVG 放在 `public/plates/`，在 `src/data/plates.json` 登记镜头要用的图板：

```json
{"formula":{"file":"equation.png","pixels":[2560,420],"kind":"raster","source":"来源、公式页或复算记录"}}
```

`g.plate('formula', [320, 300, 1280, 210], 'formula')` 以 1080p 的像素坐标画它。保住宽高比；检查会核实际像素、推进后的最大尺寸和字幕缓冲。论文物证放在真实浅白切面，用 `'source'` 并在镜表填 `paper` 与归属。文字不会从原图里自动识别，必须在实际成片上验清晰度和图号；出处细节写进 `sources.md`。

## 交有声成片和复剪源

切换 `demo: false`，选 `engineering` 或 `derivation`。先把与成片同长度、48kHz 的立体声混音和单声道干旁白写成 `public/audio/locked/mix.m4a` 与 `dialogue.m4a`（目录名以 `audioTag` 为准）。已拿到同版双轨母版就按两条 AAC 取出，用 `-map 0:a:0` 和 `-map 0:a:1`、`-c:a copy`；别用单轨分享版假装有干声。

```bash
node scripts/lint-visuals.mjs --release
npm run render:shots -- --replace
npm run export -- master
npm run export -- share
```

母版两轨加软字幕，分享版一轨加实压中文字幕。需要更新镜表、章节和算例索引时跑 `npm run sidecars`。 `python3 scripts/pack-edit.py build/edit.zip` 打源码包；另加 `--shots build/native-shots` 才装已核对的清片。用 `review-frames.mjs` 从实际合成 MP4 量画面清场、验章门末帧确实接上正文首帧，并抽思考的前中后帧；`--ids=镜号,镜号` 限定检查。实际看片，手机宽度核正文、角标和字幕。复剪交付带工程、素材和必要清片；默认排除 `local/`、`public/audio/`、TTS 参考声音和声纹码。用交付的包另解一份，不拿原工作区代验。

`lint-visuals` 的 0 errors 只说明机器能判的项通过：色板、素材/段类、逐帧字数和字形覆盖、稳定帧占幅、思考弧、时钟及正式干声中的长静默。镜头动机、语音表演、术语读法、几何碰撞和真实来源仍以看成片、听成片和原材料为准。
