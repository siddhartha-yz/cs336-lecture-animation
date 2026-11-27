# 从底稿到审片

先用一段真正会变的装置过关，再铺整集。配乐只有放在说话底下听，才知道它有没有抢戏。

## 1. 收稿：Gemini 给材料，ChatGPT 核准后锁稿

用户把 Gemini 的 `sub` / `tts`、粗分镜、音乐方向和一手出处放到 [intake/讲次](../intake/)；先查数字、前提、单位、论文版本和朗读，再按 [视觉宪法 v2](../production/cs336-lecture-animation/references/VISUAL_CONSTITUTION_v2.md) 拆意群。事实改动在对应版本记明，语言维持原稿语感。临时图不能替代成片里的真实关系。

标记 `ready` 可以开始制片，不代表成片已签收。用 `check` 验格式与送读；`bootstrap` 复制已实跑的 Remotion 模板。模板仍是 `demo: true`，未替换内容和干声前不能导出正式版。

## 2. 私有制作：人声、配乐和原生画面

| 工序 | 用哪套工具 | 通过时留下什么 |
| --- | --- | --- |
| **旁白** | `python3 pipeline/lecture.py voice-queue l16 --out "$PRIVATE_JOB/queue.json"`；在已授权 GPU 环境运行 [Drama 3 runner](../production/cs336-lecture-animation/scripts/drama3_takes.py) | 只用「科普声音」。关键问句和反转四选一；记录实际选 take、时长、罕见词读法、字级帧位 |
| **配乐** | 用下面的试听及长轨命令，在 Stable Audio 3 Medium 的既有 GPU 环境执行 | 每乐段 30 秒 × 3，不循环短样。用户可送 Gemini 复听；选种子后才出长轨。锁动机和调性、记录每段实际入点。 |
| **动画** | 进 `lectures/<id>/`：Remotion Studio、静帧、逐镜渲染 | 已选人声的一份 60fps 时钟给画面数值、字幕和节奏。上下或左右两区用同一数据；无关镜头净切，章节末帧接真实下一镜 |
| **混音** | [声音与实录帧钟](../production/cs336-lecture-animation/references/voice-and-mix.md) 中的读回和 v2 混音器；已批准的干声、音乐分轨接入 | 保留可切的纯旁白，不重生已验收的声音；锁定问题铃、预测静默和片尾余韵 |

Stable Audio 3 Medium 只读取课题组已安装的授权缓存。先把版本化的 runner 和锁定的 `music.json` 放在私有任务目录，在服务器的既有 Python 环境中运行：

~~~bash
python3 pipeline/score.py check --project intake/l16/music.json
CUDA_VISIBLE_DEVICES="$ASSIGNED_GPU" HF_HUB_OFFLINE=1 \
  python3 pipeline/score.py previews --project "$PRIVATE_JOB/music.json" --out "$PRIVATE_JOB/score"
CUDA_VISIBLE_DEVICES="$ASSIGNED_GPU" HF_HUB_OFFLINE=1 \
  python3 pipeline/score.py masters --project "$PRIVATE_JOB/music.json" --out "$PRIVATE_JOB/score" \
  --choices "$PRIVATE_JOB/score-choices.json"
~~~

`score-choices.json` 形如 `{"m1":[32301],"m2":[32501]}`，用实际试听时间和观感决定。超过单次长度上限的乐章先按画面节拍拆为同调性乐段，不能用短轨循环或默默截断。精确时长取已经锁定的成片帧号，不用预估时间反推字词。

## 3. 审片：同一版号，听和看分别诊断

先运行工程内 `npm run typecheck` 和 `node scripts/lint-visuals.mjs`；有声交付加 `--release`。实际解码并看手机宽度、章门末帧、密文字、思考窗、碰撞和片尾。按 [样片案册](../production/cs336-lecture-animation/references/shot-study.md) 看动作是否真的在解释变化。

一版审片对应一个源码提交和一个实际视频。用户把这一版交 Gemini 做音画检查，再做自己的判断。记“时间码/实际帧 → 看见或听见了什么 → 采用哪条改动 → 新版结果”。ChatGPT 按实际反馈返工，再交下一版。版本变了，旧的“通过”只覆盖未动部分。GitHub CI 的通过不能代替人听、人看。

## 4. 交付：看、听、剪有各自入口

交付压印字幕的分享版、带软字幕的双音轨母版、封面和可从源复剪的工程。用交付包解压到新目录，重画受影响的镜与接缝，再合片；只有真正从零画完全程才能称全片源回编。对外发成片、原声和审片素材，分别听用户的授权。

公共 CI 不登录服务器，不保存音频；模型许可、私有 runner 执行和发布是不同的事。
