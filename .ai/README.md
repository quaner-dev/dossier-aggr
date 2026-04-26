# AI Workspace

本目录保存仓库内 AI/代码代理需要读取和维护的共享上下文。

## 默认阅读顺序

1. `.ai/AGENTS.md`：执行约束、分层边界、验证要求。
2. 按任务选择一个入口，不默认全量读取所有目录：
   - 项目结构、运行时或编码规范：`.ai/project/README.md`
   - GA/T 1400 或 GA/T 2350 协议工作：`.ai/protocols/README.md`
   - 测试设计、基线或验证策略：`.ai/testing/README.md`
   - 常见开发流程：`.ai/workflows/README.md`

`.ai/plans/` 是历史计划摘要，不属于默认阅读路径。

## 权威顺序

当需求、代码实现与文档存在冲突时，优先级如下：

1. 本地 `.protocol/` 原始协议文件。
2. `.ai/AGENTS.md` 与根 `AGENTS.md`。
3. `.ai/project`、`.ai/protocols`、`.ai/testing`、`.ai/workflows` 中的整理文档。
4. 当前代码实现。

`.ai/protocols/` 只提供导航、索引、实现映射和差异清单，不替代本地 `.protocol/` 原始协议。

## 目录索引

- `.ai/project/`：项目结构、运行时链路、命名规则和运行时导航。
- `.ai/protocols/`：协议源文件索引、接口索引、实现映射和已知差异。
- `.ai/testing/`：测试说明和验证清单。
- `.ai/workflows/`：新增接口、协议变更、迁移、异步任务等流程卡片。
- `.ai/plans/archive/`：历史设计和实施计划摘要。

## Token 使用约束

- 不为了一般上下文而全量读取 `.ai/`。
- 检索 `.ai/` 时默认排除历史计划摘要，除非明确需要追溯历史决策。
- 常规检索示例：`rg "<keyword>" .ai --glob '!.ai/plans/archive/**'`
