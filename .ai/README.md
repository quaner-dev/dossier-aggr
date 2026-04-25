# AI Workspace

本目录保存仓库内 AI/代码代理需要读取和维护的共享上下文。

## 阅读顺序

1. `.ai/AGENTS.md`：执行约束、分层边界、验证要求。
2. `.ai/project/README.md`：项目结构、运行时、部署、观测和数据模型。
3. `.ai/protocols/README.md`：GA/T 1400 与 GA/T 2350 协议导航。
4. `.ai/testing/README.md`：测试环境、测试分层和基线用例。
5. `.ai/workflows/README.md`：常见任务流程。

## 权威顺序

当需求、代码实现与文档存在冲突时，优先级如下：

1. 本地 `.protocol/` 原始协议文件。
2. `.ai/AGENTS.md` 与根 `AGENTS.md`。
3. `.ai/project`、`.ai/protocols`、`.ai/testing`、`.ai/workflows` 中的整理文档。
4. 当前代码实现。

`.ai/protocols/` 只提供导航、索引、实现映射和差异清单，不替代本地 `.protocol/` 原始协议。

## 目录索引

- `.ai/project/`：项目结构和运行时导航。
- `.ai/protocols/`：协议源文件索引、接口索引、实现映射和已知差异。
- `.ai/testing/`：测试说明和验证清单。
- `.ai/workflows/`：新增接口、协议变更、迁移、异步任务等流程卡片。
- `.ai/plans/archive/`：历史设计和实施计划归档。
