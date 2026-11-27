# 先听同一个人的两个意群，再把声音锁到帧

用用户授权的参考音色。指定《科普声音》就沿用这一套，不拿用户本人录音填空，也不以别的 TTS 冒充。同声的悬念和反转应当能明显分辨；先试听关键意群，各找一条自然的读法，再批合成。声音已批过则直接锁定，画面和混音改动分别进行。

## 1. 字幕、送读与表演各存一栏

```json
[
  {"id":"odds","sub":"两个分数都抬高，赢面跟着变吗？",
   "tts":"两个分数都抬高，赢面跟着变吗？",
   "kind":"question","emotion":"E1","N":4,"seed":23084},
  {"id":"water","sub":"把“沸水”这个词的概率提到 0.7。",
   "tts":"把“沸水”这个词的概率提到零点七。",
   "kind":"number","emotion":"E3","N":1,"seed":3101}
]
```

`sub` 不掺表演指令，保留用户已批准的字面；`tts` 只改真实读音、符号展开和断句。把核心提问和反转放到同一说话人的 E1–E5 切片风格中精挑（E1 悬念、E2 互动、E3 讲解、E4 反转、E5 收束），这两类 N=4，常规清楚的数值句 N=1 起。先取关键处，不为整段无谓堆候选。

```bash
python3 "$SKILL/scripts/prepare_narration.py" local/narration.json --out local/queue.json
python3 "$SKILL/scripts/drama3_takes.py" check local/queue.json
```

准备脚本只校验、编译队列；不改 `sub`，不连服务器。保留既有 `{text,say,pronunciation,seed,…}` 队列入口。脚本能拦住若干已踩过的坑：单念“沸水”改“沸水这个词”，拒答→拒绝回答，估抖→估不准，卡在的送读改拦在，`前缀和，也就是 C U seek lens` 分清停顿，`G，V，` 别连读，π 全片写“派”。字幕写原术语，别把便读的英文字母或内部模型指令烧进片。

```bash
# 只有已授权课题组 GPU、已有 Drama 3 权重/codec/模型环境时执行。
HF_HUB_OFFLINE=1 PYTHONPATH="$FISH_REPO" CUDA_VISIBLE_DEVICES="$ASSIGNED_GPU" \
  "$DRAMA3_PYTHON" "$SKILL/scripts/drama3_takes.py" render local/queue.json \
  --weights "$DRAMA3_WEIGHTS" --codec "$DRAMA3_CODEC" \
  --ref-audio "$AUTHORIZED_DRY_VOICE" --ref-text "$EXACT_REFERENCE_TRANSCRIPT" \
  --out local/takes-a
```

原工程用可核验的 Fish Speech Drama 3 `1ff3c3e` 接口，确认当前权重为 `fish_omni`；不要把 S2-Pro 环境当它。已有批准参考码可用 `--ref-tokens`，参考音频和码只经许可路径使用，不入复剪包。远程许可、GPU 配额、作业调度和发布范围各自确认；这个脚本本身只在调用机器读本地输入、生成指定目录。已存在的不同声音或音乐无需为这次验证重生成。

## 2. 让真实词首驱动数值和遮罩

1. **选 take 才锁轨。** 保留句内呼吸，裁没用的首尾静音。目标原生 230–250 字/分，实测调速只许 0.97–1.04 倍。若塞不进既有槽位，优先重选同一意群，别把数字读法拉坏或挤掉思考。
2. 给已经选中、裁好的 WAV 读回字词边界。数字和短分词听一遍前后邻词：识别稿可能误把“零点五”“串味”少算半拍；只用编辑稿开头当锚会让字幕和画面同错。按镜内放入的实际音频偏移复核时间。
3. 用 `lock_timing.py` 更新字幕入退与 cue，不改字幕文字或镜长。`--spoken-cues` 让脚本按 `tts` 对齐，逐条核对 `sub`，再更新指定 cue 和对应 `beats[].wordFrame`。锚词按对齐栏写：送读是「提到零点七」，ASR 若写成「提到 0.7」，听核后可在这条另加 `read`，锚词跟 `read`。锚要完整读回，不能靠一句匹配九成就让错误数字混过去。真实数值、高亮距词首 `±150ms` 以内。局部重录用同一参考、原增益入位，只重算受影响的锚。
4. 公式预测的 4.5s 和多行 A/B 的 6.5–7.5s 在镜表单列。不要在前半把后面的试题答案讲掉。干声必须在窗口内停，音乐可留；字幕退，金色弧走；有口播的数例按实词驱动对象，不把无声停留当长镜头感。

以一条字幕的镜头为例，`local/water-spoken.json` 用 `[{"sub":"把“沸水”这个词的概率提到 0.7。","tts":"把“沸水”这个词的概率提到零点七。"}]`，`local/water-anchors.json` 用 `{"raise":"提到零点七"}`。多条字幕按镜内顺序列全；锚词多次出现可以写 `{"phrase":"提到零点七","occurrence":2}`。

```bash
HF_HUB_OFFLINE=1 "$ASR_PYTHON" "$SKILL/scripts/read_words.py" local/water-chosen.wav \
  --model "$ASR_MODEL_DIR" --strict-model --out local/water-words.json
python3 "$SKILL/scripts/lock_timing.py" --cut src/data/cut.json --scene water \
  --asr local/water-words.json --spoken-cues local/water-spoken.json \
  --anchors local/water-anchors.json --offset-frames 8 --out local/cut-aligned.json
```

用同一修订的本地 ASR 模型和 tokenizer。L15 数值句实测：large-v3 检查点缺 `tokenizer.json` 时，[faster-whisper 的回退](https://github.com/SYSTRAN/faster-whisper/blob/v1.2.1/faster_whisper/transcribe.py#L700-L710)让普通话被译成英文，送读稿再准也对不齐；补齐[同一修订文件](https://huggingface.co/Systran/faster-whisper-large-v3/tree/edaa852ec7e145841d8ffdb056a99866b5f0a478)后，实际母版的这一段六个锚点与定版刻度差最多三帧。不要拿 tiny 的词表补 large-v3。

听核后再采用新 cut。老 Cairo 工程的时间轴在根目录 `cut.json`；送读和显示写法一致时，不传 `--spoken-cues` 仍按原字幕字位锁定。试听至少覆盖改过的字词与前后邻句、音乐起伏最大的地方、最后一拍；最终要听交付音轨，不仅听 WAV。

## 3. 音乐先连成乐章，响度出问题在独立 BGM 上修

**有授权新做音乐时**：先按影片的关系大小调与动机分乐章；只要纯器乐，每轨用 `TrackType: Music, VocalType: Instrumental` 开头。每章先生成 3 条 30 秒种子试听，选对音色与织体后才生成完整版本，不把30秒段循环铺四分钟。冷静压力可用 96–102 BPM 弱音钢琴、低音马林巴与稳底；禁用预告片大鼓、刺耳 riser、哀乐式提琴等 v2 黑名单。曲源、许可、选中 seed、原曲入点和片内长度写入 cuebook。

**已有授权曲子或已验收 M1–M5 时**：不重生成。先拼好等长 48kHz PCM：`dialogue.wav` 单声道，连续 `score.wav` 和对准词尾的 `sfx.wav` 都为立体声、同一起点和样本数。切乐章用约 2.5s 等功率 `cos/sin` 交叠；音乐、提示音和原声分 stem。已混好的作品先比较更动前后音轨，不盲目二次归一化。

```bash
python3 "$SKILL/scripts/mix_audio.py" --profile v2 --plan local/score-plan.json \
  --dialogue local/dialogue.wav --score local/score.wav --sfx local/sfx.wav \
  --out local/screening.wav
```

`score-plan.json` 的秒数都取成片钟，例如：

```json
{
  "movements": [{"start": 0, "end": 70}, {"start": 70, "measureFrom": 72.5, "end": 120}],
  "cuts": [{"start": 88, "end": 104, "db": -3.5}],
  "questions": [{"start": 65.0, "end": 67.6}],
  "lastVoice": 116.3
}
```

v2 混音器对同一乐章按 30 秒窗口读 EBU 短时响度，不把章间换曲错判为爬升；明显超过首个有效窗 +2.5dB 的连续区域自动 −3.5dB，配 120Hz 低架 −2dB、两秒软进软出。人工标注还未识别的密鼓或亮敲击窗用 `cuts`，重叠以较强包络为准。以人声总线 −16 LUFS、BGM −33.5 LUFS 作基准，音乐 2.5kHz/Q1 −3dB，随人声侧链约至多 2.16dB（30/250ms）。回传日志含真实扫描与成品响度、true peak；实听 M2 后半/M4 后半这类段落是否退够，再定稿。

提问前压乐，**铃音在已经对齐的独立 SFX stem 上**，末字 +0.15s，截3.0–3.5s、淡出，再按 v2 混到−12dB。助手找旋律自然入退，不能用白噪声造假钟。尾句后音乐自然走足3.5–4.0秒，`lastVoice` 只是用真实时间校验；请预先安排尾和弦而非给成片追加空片。无 SFX 便省对应参数。未传 `--profile` 保留旧工程的混音行为。

## 4. 给音轨一个能复剪的出口

对批准的混音和干声各编码 AAC（48kHz；混音立体声、干声单声道），写入项目 `public/audio/<audioTag>/mix.m4a` 与 `dialogue.m4a`，再用 Remotion 工程的 `npm run export -- master` / `share`。有同版双轨母版时直接抽两条 AAC，不需要再生成相同句子。分享版压印字幕且只有混音；可切换字幕和纯旁白留在供授权接收者的双轨母版。公开只给当下授权的范围。
