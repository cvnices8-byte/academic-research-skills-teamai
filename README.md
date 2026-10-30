# 科研与论文润色 Skills · TeamAI

这是一个用 [TeamAI CLI](https://github.com/Tencent/teamai-cli) 初始化的 Codex 技能集合，整理自本机已安装的科研、学术写作和文字润色 Skills。六套上游技能库各保留**一个顶层入口**及其完整原始模块目录；没有将内部模块拆成数百个独立顶层 Skill。

| 顶层调用名 | 用途 |
| --- | --- |
| `academic-research-suite` | 文献综述、研究设计、论文写作、审稿与修改、实验规划 |
| `supervisor-skills` | 研究想法评估、论文框架、投稿前检查、rebuttal、学术润色 |
| `science-skills` | 科学数据库检索及生物医学/序列/结构研究工作流 |
| `nature-skills` | Nature 风格写作与润色、图表、统计和同行评议 |
| `computer-science-conference-suite` | 计算机与 AI 会议选会及稿件适配评估 |
| `chinese-socialscience-journal-suite` | 中文经济、管理、社科期刊选刊及稿件适配评估 |
| `ai-literature-manager` | 本地 PDF 论文库、证据定位、阅读记录与跨篇比较 |
| `humanizer` | 去除机械化 AI 文风，同时保留原意 |
| `mineru` | PDF、图片和 Office 文档解析/OCR；需另装 MinerU 工具 |

## 目录与安装

TeamAI 管理的技能位于 `.teamai/skills/`。整套库的路由文件为 `.teamai/skills/<调用名>/SKILL.md`，其原始模块在同一目录下的 `source/` 或 `ars/` 中。`source/` 内含被引用的 `skills/`、`resources/` 与相关说明文件，不应只复制顶层 `SKILL.md`。

在本仓库检出目录中使用 Codex：

```sh
npm install -g teamai-cli
git clone https://github.com/cvnices8-byte/academic-research-skills-teamai.git
cd academic-research-skills-teamai
teamai init . --agent codex
teamai pull --force
teamai doctor
```

`teamai init .` 使用 TeamAI 的单仓库模式，将本仓库里的 Skills 分发到**该检出目录**的 Codex 环境。它不会自动安装 MinerU 程序、科学数据库凭据、Python/R 依赖或其他外部服务。若系统级 npm 安装目录不可写，可按 npm 的用户目录方案安装 CLI。

## 来源、许可与边界

详见 [SOURCES.md](SOURCES.md)。本仓库不以单一许可证重新许可第三方内容；每个套件保留其原有许可及署名要求。`academic-research-suite` 和 `supervisor-skills` 包含非商业许可内容，请先核对用途。论文库数据、原始 PDF、个人笔记和凭据**未纳入**本仓库。

期刊/会议规则、截止时间和数据库信息可能变化；生成投稿建议前应查当年官方来源。公开仓库中的技能指令与脚本应像其他第三方代码一样先审阅再执行。
