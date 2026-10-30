# 抽取、阅读与跨篇比较

## 按论文类型选字段

先建立通用字段，再增加实际适用字段；不为了填满表格伪造研究设计。字段 ID 是保存与导出的稳定接口。

| 层 | 建议字段 ID | 需要保留的内容 |
|---|---|---|
| 通用 | `research_type`, `research_question`, `gap`, `framework`, `data`, `method`, `findings`, `contribution`, `author_limitations`, `resources` | 作者问题与背景分开、贡献为作者声称、资源记录核查状态 |
| 基准/数据集 | `task`, `construction`, `annotation`, `benchmark_evidence`, `evaluation_sample`, `settings`, `metrics` | 输入输出、构造阶段、专家审核范围、全库/公开/实测分母、评分规则 |
| 经管实证 | `hypotheses`, `variables`, `sample`, `identification`, `estimation`, `robustness`, `heterogeneity`, `mechanisms` | 分析单位、测量方式、因果主张及识别假设、不同规格归属 |
| 经管理论/质性 | `propositions`, `case_selection`, `qualitative_material`, `analysis_process` | 不强迫填回归系数；资料与解释区分 |
| 计算机算法/系统 | `task`, `architecture`, `data_split`, `baselines`, `ablations`, `failure_cases`, `compute` | 训练/测试划分、模块用途、比较条件、消融及资源 |
| 读者分析 | `ai_appraisal`, `research_ideas` | `origin=ai_inference`，明确依据，不能承诺发现全领域空白 |

## 阅读与证据

先核对身份页、摘要、研究问题，再按任务阅读方法、数据、实验、局限和相关附录。用户要全文拆解时覆盖全文并如实记录未解析部分；不把抽样阅读标 full_text。每个证据对应同一文件哈希，以 1 开始记录 PDF 页序号。

数值核对表头、行名、列名、单位、模型、设置和分母；查看原页处理双栏、合并单元格、脚注和 OCR 歧义。原文内部不一致时并列保存，可附独立算术检查；没有读取更正版本就不声称已修正。

引文原样保留，必要时多个短片段覆盖不同事实；翻译存独立属性。不为了匹配改写原句，也不把去空格/OCR文本当作出版社原排版。`text_matched` 只说明字符匹配，不说明语义支持。

## 双语

默认中文概括，保留原题名、英文专词和缩写。主文语言和研究数据语言分别保存。中英文表述的数字、否定词、条件和范围保持一致；原文缺失不能在翻译里补足。显示语言切换使用已存表述，不重跑覆盖人工内容。

## 比较

结论附口径说明：任务、样本、输入、数据划分、指标定义、单位、裁判/容差、版本是否相同。不能直接把检索 Recall@10、答案 Accuracy、证据 F1、因果回归效应或不同分母的人工表现放同一排名。

说明“可比”“部分可比”“不可直接比较”的理由。相同任务和指标仍核对基线及输入条件；oracle 与普通 RAG 不混作一组。总表用于发现差异，结论回到实验子记录和原页。

## 失败与完成

单篇失败保留已完成记录，列出文件与原因；下一次从已有覆盖和修订号继续。解析失败不自动启用收费 OCR 或上传第三方。来源与覆盖可说明、内容归属分清、修订落库、请求的导出可打开，才算当前任务完成。
