# 来源与许可说明

本仓库是已安装技能的整理快照，不声称拥有第三方原作。除明确注明的本地适配外，套件内部文件均来自对应上游；转发或修改时请保留原作者署名、许可和第三方声明。不同套件许可不同，不能将整个仓库笼统标为 MIT 或 Apache。

| 本仓库目录 | 上游来源 | 许可/说明 |
| --- | --- | --- |
| `academic-research-suite/` | [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills)；另含 [experiment-agent](https://github.com/Imbad0202/experiment-agent) | 本机 Codex 适配版 3.22.2；`ars/LICENSE`、`ars/LICENSE.academic-research-skills`、`ars/experiment-agent/LICENSE` 及 `ars/NOTICE.md`、`ars/THIRD_PARTY.md` 保留在包内。主套件为 CC BY-NC 4.0，使用前请阅读具体文件。 |
| `supervisor-skills/` | [HKUSTDial/Supervisor-Skills](https://github.com/HKUSTDial/Supervisor-Skills) | CC BY-NC-SA 4.0；`source/LICENSE`。只为使套件自包含而修改了顶层路由中的相对路径，原模块保留在 `source/skills/`。 |
| `science-skills/` | [google-deepmind/science-skills](https://github.com/google-deepmind/science-skills) | Apache 2.0；`source/LICENSE`。顶层路由的相对路径已适配。 |
| `nature-skills/` | [Yuan1z0825/nature-skills](https://github.com/Yuan1z0825/nature-skills) | Apache 2.0；`source/LICENSE`。个别模块含另行注明的第三方素材（如 `THIRD_PARTY_NOTICES.md`）；顶层路由的相对路径已适配。 |
| `computer-science-conference-suite/` | [Awesome-Journal-Skills / Computer-Science-Conference-Skills](https://github.com/brycewang-stanford/Awesome-Journal-Skills/tree/main/Computer-Science-Conference-Skills) | 上游仓库 MIT；`source/LICENSE`。本地保留 156 个会议模块与 `resources/`，顶层路由路径已适配。 |
| `chinese-socialscience-journal-suite/` | [Awesome-Journal-Skills / Chinese-SocialScience-Journal-Skills](https://github.com/brycewang-stanford/Awesome-Journal-Skills/tree/main/Chinese-SocialScience-Journal-Skills) | 上游仓库 MIT；`source/LICENSE`。本地保留 103 个期刊模块与 `resources/`，顶层路由路径已适配。 |
| `humanizer/` | [blader/humanizer](https://github.com/blader/humanizer) | MIT；包内 `LICENSE`。 |
| `mineru/` | [opendatalab/MinerU 的 mineru Skill](https://github.com/opendatalab/MinerU/tree/master/skills/mineru) | 包内 `LICENSE.md` 为 MinerU Open Source License；仅收录 Skill，不含解析程序或模型。 |
| `ai-literature-manager/` | 本机现有的独立本地 Skill | 未发现可核实的公开上游许可；不要把它归为其他套件或假称已按 MIT 开源。分享版只将操作示例中的个人绝对路径替换为通用占位路径，不含文献数据库与 PDF。 |

上游引用文件可能在本地安装之后更新。本仓库保留的是本地快照及可核实的来源链接，不保证与当前上游 `main` 分支完全相同。对于需要最新行为的工作流，应到上游仓库和官方研究资源核对。
