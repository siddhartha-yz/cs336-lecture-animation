# 用一个 PR 做完一讲

开一个 **Draft PR**，把 Gemini 的规划、ChatGPT 的实现、每轮审片和返工接在同一条讨论里。新讲和已成片返修用同一流程；更换候选不换 PR。

| 人 | 输入 | 交回 PR 的东西 |
| --- | --- | --- |
| Gemini · 规划 | 原讲与来源、交稿模板、本讲约束 | 字幕/送读、分镜、音乐方向；返修时给可验证的修复范围 |
| ChatGPT · 实现 | 已确认的规划、原工程与上轮反馈 | Remotion 源码提交、当前候选、关键实帧和未解决问题 |
| Gemini · 审片 | 这版完整私有 MP4、镜表、确切版号 | 带时间码的必修项与可选项，画面、声音、数学分开 |
| 你 · 验收 | Gemini 意见与同一版实际视频 | 接受、返工或可合并的决定 |

## 1. 草稿 PR：先定范围

推一个制作分支，使用 [制片 PR 模板](../.github/PULL_REQUEST_TEMPLATE/film.md) 建 Draft PR。GitHub 比较页可加 `template=film.md` 选它，或在仓库根目录执行：

~~~bash
gh pr create --draft --title 'Lecture 16 · 制作' \
  --template .github/PULL_REQUEST_TEMPLATE/film.md
~~~

模板里新讲用 `work: "new"`，返修用 `"revision"` 并写上一版和必修项。新讲用 [Gemini 交稿模板](../intake/)；允许公开的源稿入 `intake/<讲次>/`，不公开的材料私下传给两端。返修把受影响的镜头、接缝以及必须保留的旁白、配乐或时码写清。普通仓库改动不用制片模板，仍然走源码检查。

你确认规划后，把 PR 的 `plan` 改成 `ready`。有收稿目录的新讲，核准源稿后还要把 `brief.json` 标为 `ready`，按[制作流程](production-flow.md)检查再开工。

## 2. ChatGPT：实现到能看片

把 **PR 链接** 交给有本地工程和既有授权的 ChatGPT/Codex：

> 读取这个 Draft PR 的计划、镜表和最新反馈，在同一分支实现。按仓库 AGENTS 与视觉约束先核事实；用 Remotion 实画，从授权环境沿用或生成「科普声音」与配乐。用实际成片复核改动和接缝。提交源代码，向同一 PR 交回可看片的候选和仍待审的时间码。不要代填审片通过、合并或发布。

私有音频只走既有课题组设置。没有新声音授权，或旧声音已经签核时，不在 CI 或别处补生成。普通 GitHub Actions 只检查源、帧钟与公开可渲染素材。

## 3. 登记审片候选

**先提交源码，再从这次提交导出审片 MP4。** 每次重导升版（包括只改混音的重导），保留旧文件。用实际文件生成同版记录：

~~~bash
python3 pipeline/film_pr.py candidate l16 R02 '/私有目录/下集-整片审片-R02.mp4' \
  > /tmp/cs336-l16-R02.json
~~~

把输出对象放进 PR 描述里的 `candidate`。命令核对当前已提交的镜表与 MP4 的尺寸、帧率和帧数，只输出版号、提交、文件名、总帧数。**文件本身、内部路径、私有链接、参考音色和试听轨不放公开 GitHub。**

每轮用相同四字段来识别候选（也用这份 JSON 生成回执）。审片者看的是你单独交给他的 MP4，不是从 PR 下载的资产。

## 4. Gemini 初审，你复审

把该版 MP4、镜表和 PR 链接私下交给 Gemini，并附上：

> 先复述你实际收到的版号和文件名。只审这个视频；清楚区分实听、实帧与推测。按「必须修 / 可选」给时间码、现象、验收办法；声音、画面与数学分开。例：有轮廓书写要求时看字形的中间帧，不能把裁切擦除当 Write。不要替我批准合并或上传。

将精简后的具体结果放在 PR **Conversation**。仓库所有者先贴 Gemini 回执，再亲看同版后贴本人回执。将命令输出作为新评论，代码块下可以写时间码与结论：

~~~bash
python3 pipeline/film_pr.py receipt gemini pass /tmp/cs336-l16-R02.json
python3 pipeline/film_pr.py receipt owner pass /tmp/cs336-l16-R02.json
~~~

有必修项就用 `changes`，维持 Draft（已转 Ready 就先转回 Draft），让 ChatGPT 从同一个 PR 按时间码返工。把时间落到具体镜和帧，用[反馈定位工具](production-flow.md#3-审片同一版号听和看分别诊断)。旧回执留在讨论里；不用编辑成新版本的签收。无需让 Gemini 加入仓库或设置 API 密钥。

## 5. 只有同版通过才转 Ready

`Film handoff` 读取当前 PR、实际镜表及仓库所有者的公开回执。新提交、换候选文件名或升版后，旧回执不再匹配；同版也要求本人通过晚于最后一次 Gemini 通过。草稿的待处理状态列在检查摘要，转 **Ready for review** 会重新检查；提前转 Ready 会标红。仅发评论不会触发重新检查，Draft 期间读评论即可；最后转 Ready 时会读最新回执。

`Production check` 在 PR 新提交和更新 main 时跑收稿与 Remotion 实帧检查，并对 PR 改到的其他讲次另查源码和项目帧门禁。需要在开 PR 前跑 CI 时，可手动运行该工作流。它和 `Film handoff` 各负责一件事：一个验证工程，一个验证交接，均不能代替实际音画验收。两项通过后，由你合并；发布成片仍是单独一步。

如果要由 GitHub **强制**等这两项通过再合并，在 [main 的分支保护](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches#require-status-checks-before-merging)选实际跑过的 `Film handoff` 和 `source-and-render`。不勾原生「至少一人 Approve」来代替本人回执：个人仓库经常由你开 PR，再由你亲自签收。
