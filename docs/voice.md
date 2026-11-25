# v0.1.0：中文开头试听记录

下文保留早期选声的输入与命令。当前的中文逐字稿和字级时钟见 [v3 工程](../editions/zh-v3/README.md)。

**输入**是本人录制的普通话参考音和它的准确转写；**输出**是 Drama 3 按参考音朗读既有中文稿。到这个检查点为止，中文成片仍用 Dylan，真人参考音未选定。此前用 Drama 3 做的原创合成音色试听是另一条实验，不是成片，也不是本轮要选的声源。

先听 [Home Assistant 的普通话捐录 chaowen](https://raw.githubusercontent.com/OHF-Voice/voice-datasets/master/zh_CN/chaowen/0000000001.mp3)；[社区明确将这组为 TTS 募集的原始录音以 CC0 发布](https://github.com/OHF-Voice/voice-datasets)。想比较说话方式，可听 [MSceneSpeech 的 Dataset demo → Chat](https://speechai-demo.github.io/MSceneSpeech/) 或 [voice-zero-zh → aishell1](https://iamyb.github.io/voice-zero-zh/)。试听页和每位说话人的使用条件分开看，选作参考时保留来源、适用授权与原文。

用本地 [Fish Speech v3.0.0-beta](https://github.com/fishaudio/fish-speech/tree/v3.0.0-beta)，模型是 [fishaudio/drama-3 的固定版本](https://huggingface.co/fishaudio/drama-3/tree/78e5ab79e49aa9a25abe8799eff2c4d73a1c3216)。[上游安装说明](https://github.com/fishaudio/fish-speech/blob/v3.0.0-beta/docs/zh/install.md) 包括 CUDA、权重和共用的 S2-Pro codec。无需 Fish 商城 ID 或付费 API。

在 Fish Speech 的已配置环境中运行。下列三个变量分别指向影片仓库、获准使用的原声、原声实际说的话；待生成的课程正文是第四个独立文件，已经随仓保存。

```bash
# 在 fish-speech 源码根目录，使用分配给自己的 GPU
python fish_speech/models/text2semantic/inference.py \
  --checkpoint-path checkpoints/drama-3 \
  --prompt-audio "$REF_WAV" --prompt-text "$(cat "$REF_TXT")" \
  --text "<|speaker:0|>$(cat "$FILM_ROOT/film/drama3/opening-zh.txt")" \
  --single-chunk --device cuda:0 --output opening-audition.wav
```

按整段生成，听第一句“分数上去了，模型做新题却更差了”的转折，再听后面的长句有没有突然断气。约 30 秒是试听长度，不为卡秒改词或把声音拉慢。试听选定前不覆盖现有音轨。
