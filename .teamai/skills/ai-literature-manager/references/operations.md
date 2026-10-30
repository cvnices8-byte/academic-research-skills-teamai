# Agent 操作接口

以本技能安装路径为基准设置 `LIT`，不依赖当前工作目录。下面示例中 `LIT` 指脚本绝对路径，`LIB` 指用户项目的文献库目录。执行前替换示例路径；传入动态文本时用参数数组/结构化进程调用，避免拼接 shell 命令。

```sh
LIT=/absolute/path/to/ai-literature-manager/scripts/literature.py
LIB=/absolute/path/to/your-project/文献库
python3 "$LIT" --library "$LIB" init
python3 "$LIT" --library "$LIB" add --pdf /absolute/path/paper.pdf --metadata /absolute/path/metadata.json
python3 "$LIT" --library "$LIB" scan --folder /absolute/path/papers
python3 "$LIT" --library "$LIB" list --query CFQA
python3 "$LIT" --library "$LIB" list --status to_read --tag 财报问答
python3 "$LIT" --library "$LIB" show --id paper_id
python3 "$LIT" --library "$LIB" check-sources
```

`scan` 只扫描指定目录内的 PDF，按文件名建立未核验元数据，返回逐文件结果和失败信息，不自动抽取全文。`add` 接收可选 `--id`，相同哈希重复导入返回已有 ID，且不会覆盖既有元数据或拆解。`check-sources` 检查原件存在性/哈希；`problems>0` 时不能把变更后的 PDF 当原记录的证据。它检查文件身份，不验证内容语义。

## 写入

先 `show` 获取 revision；按[字段合同](data-contract.md)写 JSON 文件，再调用：

```sh
python3 "$LIT" --library "$LIB" apply --id paper_id --expected-revision 1 --input /absolute/path/extraction.json
python3 "$LIT" --library "$LIB" metadata --id paper_id --input /absolute/path/metadata-patch.json
python3 "$LIT" --library "$LIB" edit --id paper_id --field research_question --input /absolute/path/user-edit.json
python3 "$LIT" --library "$LIB" review --id paper_id --field research_question --value verified --text '用户已逐项核对'
python3 "$LIT" --library "$LIB" status --id paper_id --value reading
python3 "$LIT" --library "$LIB" tags --id paper_id --value 财报问答 精读候选
python3 "$LIT" --library "$LIB" note --id paper_id --text '用户明确提供的个人笔记'
python3 "$LIT" --library "$LIB" history --id paper_id
```

示例 `review/status/note/edit` 仅在用户表达了相应内容时执行，不在示范时凭空登记。`edit` 输入至少包含 `value` 和 `status`，可附证据；`origin` 由命令设为 user。`apply` 没有用户层写权限。其他写入也可加 `--expected-revision`，避免用过期内容改写。

`tags` 替换该文献完整标签列表；`note` 追加；`metadata` 按键更新；不提供的键不修改。元数据修改可能影响证据页界，非法页数修改会整体拒绝。

## 输出

```sh
python3 "$LIT" --library "$LIB" export --format md --output "$LIB/文献总表.md"
python3 "$LIT" --library "$LIB" export --format csv --output "$LIB/文献总表.csv"
python3 "$LIT" --library "$LIB" export --format json --output "$LIB/文献库.json"
```

CSV 是可筛选预览；完整证据、实验、人工修订和问题在 Markdown/JSON 中。SQLite 自带修订历史，JSON 是当前快照，不含所有历史。移动原件后需再次 `add` 新路径登记；旧路径仍保留，`check-sources` 会指出缺失路径。要备份时在没有写任务运行时复制整个文献库目录，并另备份原 PDF。

## 迁移本项目调研

`scripts/migrate_pilot.py` 仅接受 `schema_version=pilot-reading-v0.1`，用于已存在的六篇试读记录，不是通用外部导入器：

```sh
python3 /absolute/path/ai-literature-manager/scripts/migrate_pilot.py --library "$LIB" --input /absolute/path/六篇论文结构化拆解.json
```

迁移会逐份检查 PDF 哈希、映射字段、保留旧引文/冲突/语言信息，把 AI 范围提醒放到独立 `ai_appraisal`。原有核查声明保留为 inherited 属性，当前引文检查设 unverified，用户核验设 pending、阅读状态保持未记录。原样重跑会跳过已有迁移；已有其他拆解时拒绝覆盖。整个批次在同一事务中，任一失败不留下半批记录。
