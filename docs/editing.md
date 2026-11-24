# 从检查点接着剪

三个精剪版本各有自己的 `timeline.json`：`film/beats_zh` 是中文 A–F，`film/beats_final` 是英文 A–F，`film/beat2` 是英文 G–K。时间轴里的 `start`、`end` 是整段的帧号，`duration` 单位是秒；`--still` 的时间从当前镜头起算。中文比英文开头长 4.6 秒，两个时间轴不要互换。

## 先看改动，再出片

以中文开头为例，A/B、C/D、E/F 的画面分别在 `opening.py`、`middle.py`、`tail.py`。下面的命令都从仓库根目录运行：

```bash
/usr/bin/python3 film/beats_zh/film.py --still c 16 build/budget.png --width 960
/usr/bin/python3 film/beats_zh/film.py --pick c --width 960 --dest preview-shots
```

上述操作只生成画面，不需要 GPU。首次合成有声版时，先从 [v0.1.0 的素材](https://github.com/siddhartha-yz/cs336-lecture12-evaluation/releases/tag/v0.1.0) 下载 `beats-edit-audio.zip`。这是剪辑用的无损 FLAC，包含三段成片混音、旁白干声，以及中文 A–F 和英文 G–K 的入选整段录音。可用浏览器下载，也可运行：

```bash
gh release download v0.1.0 --repo siddhartha-yz/cs336-lecture12-evaluation \
  --pattern beats-edit-audio.zip --dir downloads
python3 tools/restore_audio.py beats downloads/beats-edit-audio.zip

/usr/bin/python3 film/beats_zh/film.py --workers 4
/usr/bin/python3 film/beats_zh/film.py --mux master.mp4
```

恢复工具把音轨放回各镜头预期的位置，保留已有 WAV。输出是 `film/beats_zh/master.mp4`。仅改某一镜头时，在已有全套同分辨率镜头的情况下用 `--pick c` 重画它，再运行 `--mux`。低清预览请使用独立的 `--dest`，不要混入 1080p 镜头。

英文两个版本把路径换成 `film/beats_final` 和 `film/beat2` 即可。两段都生成 `master.mp4` 后，运行 `python3 film/beat2/assemble.py`，得到 `film/beat2/complete.mp4`：Beat 2 接在 03:43.800，字幕和章节一并拼接。

## 换旁白，而不重新设计动画

1. 先用[开头试听流程](voice.md)比较声线；只做音频，不动现有成片。
2. 确认换声后，以 `film/beats_zh/script_a.json` 至 `script_f.json` 为中文定稿，每镜头一条连续录音。入选音频放在 `audio/takes/<镜头>.wav`（24 kHz 单声道），相应逐词时间放在 `audio/qa/<镜头>.qa.json`。`align_mandarin.py` 用这些文件重建中文画面提示、字幕与干声，而不是照搬英文节拍。
3. 如需重新混乐，从 [Blue Dot Sessions 的三首曲目页](credits.md)取得 MP3，以 `music/cueplan.json` 中的文件名放在本版的 `music/`；运行 `align_mandarin.py` 后再运行 `mix_recordings.py`。这两步需要 NumPy、SciPy 和 SoundFile。只重画镜头时直接沿用恢复的混音，无须另取原曲。

## 20 分钟底稿

`film/act1–4` 是中文四幕，`film/v2/act1–4` 是英文四幕；每幕的 `.json` 对应口播，`.py` 对应画面。两个时间轴都是 36,000 帧，中文字幕已烧进当时的画面。独立 SRT 也在仓库内。

要恢复这两个版本的整段录音、干声与混音，可按上文将资源名改成 `full-edit-audio.zip`，然后：

```bash
python3 tools/restore_audio.py full downloads/full-edit-audio.zip
/usr/bin/python3 film/render.py --workers 4
/usr/bin/python3 film/mux.py --out master-zh.mp4
/usr/bin/python3 film/v2/render.py --workers 4
/usr/bin/python3 film/v2/mux.py --out master-en.mp4
```

锁定的字幕、时间轴、混音和渲染所需的测量数据已保存。只有重做旧版 Qwen 口播才需要本地 CustomVoice 权重（路径通过环境变量 `QWEN_TTS_MODEL` 指定）；重新识别还需要转换好的 faster-whisper 模型置于 `film/asr_model/`。只看成片、改几何、导出画面或恢复现有旁白都无需这些权重。
