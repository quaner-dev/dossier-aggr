# Plans

本目录只保留计划规则和必要的历史摘要。详细实施计划默认是个人或当前分支的工作产物，不作为主线长期文档。

当前没有默认需要读取的活跃计划。

详细计划文件使用 `.ai/plans/YYYY-MM-DD-topic-plan.md` 命名，并由 `.gitignore` 忽略，避免误提交到 GitHub。需要团队评审的计划优先放在 GitHub Issue、PR description 或讨论区。

历史摘要规则在 `archive/README.md`。若某个计划的结论具有长期价值，应迁移到对应 `.ai/project/`、`.ai/protocols/`、`.ai/testing/` 或 `.ai/workflows/` 文档，而不是依赖详细计划。

## 计划生命周期

1. 需要复杂实施计划时，可在当前分支或本地新建 `.ai/plans/YYYY-MM-DD-topic-plan.md`。
2. 执行过程中可以更新该计划，用于跟踪任务状态和关键决策。
3. PR 合并前删除详细计划文件，除非团队明确要求保留。
4. 若需要保留历史记录，新增 `.ai/plans/archive/YYYY-MM-DD-topic-summary.md`，只写日期、主题、结果、关键影响和后续风险/入口。
5. 不把详细任务步骤、完整测试输出或长代码片段提交到 `.ai/plans/`。
