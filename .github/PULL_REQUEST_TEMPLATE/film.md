<!-- cs336-film-pr:v1 -->
```json
{
  "lecture": "l16",
  "work": "new",
  "plan": "draft",
  "candidate": null
}
```

## 本轮要解决什么

- 类型：新讲，或把上面 `work` 改为 `revision`。
- 新讲的源稿：`intake/l16/`。返修写明上一版文件名、时间码和要保留的画面或音轨。
- Gemini 规划：留下底稿路径或本 PR 的评论链接。
- ChatGPT 实作：记录这轮改变了什么，和哪几处实帧需要复核。

先开 **Draft PR**。核准制作范围后把 `plan` 改成 `ready`。发布审片候选时只填上面的 `candidate`，**不上传 MP4、音频或私有链接**。Gemini 审完和本人验收后，各用 Review changes → Comment 提交同版回执，再转 Ready for review。

[回执格式和命令](https://github.com/siddhartha-yz/cs336-lecture-animation/blob/main/docs/pr-workflow.md)
