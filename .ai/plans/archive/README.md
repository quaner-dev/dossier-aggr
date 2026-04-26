# Archived Plans

本目录只保存历史设计和实施计划摘要，不保存详细实施计划。

默认不需要读取本目录；只有在追溯某次协议对齐、接口调整、重构或测试策略时再查阅。

详细逐步计划是个人或当前分支工作产物，不作为主线长期文档。需要团队评审的计划优先放在 GitHub Issue、PR description 或讨论区。

新增历史记录时，优先创建独立的 `YYYY-MM-DD-topic-summary.md` 文件，减少多人协作时对同一个 README 的冲突。摘要只写日期、主题、结果、关键影响和后续风险/入口；不要写详细任务步骤、完整测试输出或长代码片段。

## 既有摘要索引

- 2026-03-01：建立 GA/T 1400 与 GA/T 2350 契约矩阵，规划协议完整性、接口覆盖、模型、迁移和测试基线。
- 2026-03-02：补齐 GA/T 1400 API 测试入口和协议 guard。
- 2026-03-09：集中处理协议命名和接口纠偏，包括 Person、APE/APS、ArchiveLibrary、Archives、ArchiveSubject、Subscribe notification、VIAS Tasks、显式 ASC 排序和 Face 更新测试。
- 2026-03-10：完成 `repositories` 到 `repo` 的命名迁移，以及 `core` 包职责重组。
- 2026-03-11：同步 2350 正式版基线文档，并处理 Taskiq `dispatch_and_wait` 类型推导问题。
- 2026-04-25：重组 `.ai/` 目录，建立项目、协议、测试、流程和历史计划的分区。
- 2026-04-25：沉淀协议优先、编码风格、runtime chain 规则，并将 GA/T 2350.5 A.6 `/VIAS/Tasks` 纳入完整实现链路。
