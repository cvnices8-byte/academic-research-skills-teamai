# 数据与修订合同

库格式 `ai-literature-v1`，SQLite 是事实来源，Markdown/CSV/JSON 是快照。命令返回 JSON；成功 `ok=true`，失败 `ok=false` 并以非零状态退出。`--library` 必须显式给定。

## 文献身份

`paper_id` 是库内唯一标识，默认 `p_<SHA256前16位>`。每条记录包含 `sha256`、`sources`（绝对路径数组）、`metadata`、`reading_status`、`notes`、`tags`、`fields`、`experiments`、`issues`、`coverage`、`revision`。路径指向原件；库不包含 PDF 副本，迁移或备份须另带原件。元数据由 `add --metadata` 首次提供，后续修改使用 `metadata` 命令，不通过 AI 字段更新暗改。

元数据允许 `title`、`title_zh`、`authors`（字符串数组）、`year`（整数或 null）、`version`、`doi`、`paper_language`、`data_language`、`page_count`（正整数）、`metadata_source`。来源可为 PDF 页、用户提供记录或检索链接；文件名不能冒充已核验题名。

## 保存一批 AI 拆解

`apply --input` 接收以下 JSON。未提供的字段不改；同名字段只替换 AI 层。提供 `experiments`、`issues` 时替换各自完整列表，操作前读取旧记录并合并需保留内容。`coverage` 记录实际阅读过程。

```json
{
  "fields": {
    "research_question": {
      "value": {"zh": "有原文依据的中文概括", "en": null},
      "origin": "author",
      "status": "extracted",
      "evidence": [
        {"pdf_page": 1, "page_label": null, "locator": "Introduction", "quote": "必须替换为实际原文短片段", "check": "located"}
      ]
    }
  },
  "coverage": {"mode": "selected_pages", "pages_read": [1], "unread": "其余页面尚未读", "parser": "实际工具", "failures": []},
  "experiments": [],
  "issues": []
}
```

这段 JSON 仅为结构示意，不是可当真实证据导入的样本。

- `value` 可为字符串、数值、数组或对象；推荐文字字段使用 `{zh, en}`，数值保留原值/单位及转换依据。
- `origin`：`author`、`ai_inference`。用户修订通过 `edit` 写人工层。
- `status`：`extracted`、`not_reported`、`not_applicable`、`unavailable`、`conflicting`。没有证据的作者事实不能用 `extracted`；先标 `unavailable` 并写明缺什么。AI 推断注明依据与限定。
- `evidence`：原文短片段、正整数 `pdf_page`，可附 `page_label`、`locator`、`check`、`translation_zh`。页序号不得超过已知 `page_count`。`check` 可为 `unverified`、`located`、`text_matched`、`visual_checked`；均不等于用户语义核验。脚本检查结构和页界，不自动证明引文存在或支持结论。
- `conflicting` 作者字段至少两条来源，原值及差异写进 `value`/`issues`；跨表或跨页来源均可。
- `coverage.mode`：`metadata_only`、`abstract_only`、`selected_pages`、`full_text`；`pages_read` 必须是真实读取页。

## 用户层和核验

每个字段保存 `generated`（AI 最新草稿）、可选 `human`（用户明确指定的值）、`review`（`pending/verified/rejected`）、`review_note`。有效值优先取 `human`。`edit` 不删除底下 AI 草稿；AI 重跑保留人工层。有效内容改变后核验回到 `pending`；若仅隐藏的 AI 草稿改变，人工层核验保留。

`review verified` 只用于用户明确核验或明确授权登记的结果，不能因脚本校验通过或找到文字就设置。阅读状态为 `unrecorded/to_read/reading/read/archived`，仅按用户信息更新。个人笔记不进入作者结论。全部更新写历史快照，`history` 可检查旧版本；不提供自动回滚/删除命令。

## 实验子记录

每条须有独立 `experiment_id`、`study`、`model`、`setting`、`subset`、`n`（正整数或 null）、`metric`、`value`、`unit`、`evidence`。单位保留原表示，`setting` 包含 oracle/gold evidence、RAG、局部 pack 或全文等输入条件。结构检查不能代替核对表格行列。原文未报告样本量用 null，不借用别的表。

## 导出与并发

JSON 保留全部字段、证据和人工层；CSV 是宽表，Markdown 包含总表、逐篇拆解、证据及实验详情。总表单元格是预览，不能替代详情。CSV 文本以 `= + - @` 起始时加单引号防止当作公式；JSON 保持原值。

所有变更在 `BEGIN IMMEDIATE` 事务中读取和提交；AI 的 `apply` 必须提供 `--expected-revision`。旧 revision 拒绝写入，不自动覆盖。导出以一个数据库读取快照形成；文件通过临时文件原子替换。内容未变的重复写入不额外产生修订。
