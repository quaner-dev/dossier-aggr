# AI Directory Restructure Design

**更新时间:** 2026-04-25

## 1. 目标

为仓库建立统一的 `.ai/` 目录，用于沉淀 AI/代码代理需要读取的项目上下文、执行规范、协议导航、测试说明和任务流程。

迁移前，仓库中与 AI 协作相关的内容分散在：

- `AGENTS.md`
- 旧架构/协议/测试文档目录
- 旧历史计划目录

本设计的目标是先定义迁移后的目录结构和内容边界。待审核通过后，再分步骤迁移、拆分和改写现有文档。

## 2. 现状

迁移前结构：

```text
/
  AGENTS.md
  README.md
  legacy-docs/
    ARCHITECTURE.md
    PROTOCOL_1400.md
    PROTOCOL_2350.md
    TESTING.md
  legacy-plans/
    plans/
  .protocol/
    1400/
    2350/
```

现有问题：

- `AGENTS.md` 是代理入口，但内容较重，后续不利于扩展。
- 旧架构/协议/测试文档中单文件内容较多，架构、协议、测试信息混在较大的 Markdown 文件中。
- 旧历史计划目录中的历史计划文档与 AI 协作资料相关，但不在统一入口下。
- `.protocol/` 是原始协议资料，必须保留权威地位，但不应继续作为仓库提交内容维护。
- `.protocol/` 缺少 AI 友好的索引和阅读导航。

## 3. 设计原则

1. `.protocol/` 保持为本地原始协议资料目录，不迁入 `.ai/`。
2. `.ai/` 只保存可维护的 AI 协作上下文，不保存本地密钥、缓存、运行产物或聊天临时文件。
3. 根目录保留 `AGENTS.md` 作为薄入口，便于不同 AI 工具自动发现。
4. 完整代理执行规范迁入 `.ai/AGENTS.md`。
5. 旧架构/协议/测试文档迁入 `.ai/` 时按主题拆分，不原样平移成大文件。
6. 协议正文不复制进 `.ai/`，只在 `.ai/` 中保存协议简介、源文件索引、实现映射和差异清单。
7. `.protocol/` 加入 `.gitignore`，并从 Git 跟踪中移除；本地原始文件保留。
8. 若 `.ai/` 文档与本地 `.protocol/` 原始协议冲突，以 `.protocol/` 为准。

## 4. 目标目录结构

建议结构：

```text
.ai/
  README.md
  AGENTS.md

  project/
    README.md
    overview.md
    architecture.md
    layers.md
    runtime.md
    deployment.md
    observability.md
    data-models.md
    domain-status.md

  protocols/
    README.md
    1400/
      README.md
      source-files.md
      interface-index.md
      implementation-map.md
      model-index.md
      testing-map.md
      known-gaps.md
    2350/
      README.md
      source-files.md
      interface-index.md
      implementation-map.md
      model-index.md
      testing-map.md
      known-gaps.md

  testing/
    README.md
    environment.md
    layers.md
    api-matrix.md
    protocol-checklist.md
    baseline-cases.md
    pytest.md
    report-template.md

  workflows/
    README.md
    add-api-endpoint.md
    protocol-change.md
    database-migration.md
    async-task-change.md
    pre-commit-checklist.md

  plans/
    README.md
    archive/
```

根目录保留：

```text
AGENTS.md
```

根 `AGENTS.md` 只保留入口级内容：

- 提醒先阅读 `.ai/README.md`。
- 指向完整执行规范 `.ai/AGENTS.md`。
- 声明本地 `.protocol/` 是协议最高权威。
- 声明不得提交 secrets、本地配置、缓存和运行产物。

## 5. 各目录职责

### 5.1 `.ai/README.md`

AI 总入口。

建议包含：

- 仓库一句话说明。
- AI 阅读顺序。
- 关键目录索引。
- 文档优先级。
- 协议资料权威性说明。

### 5.2 `.ai/AGENTS.md`

完整代理执行规范。

建议从当前根 `AGENTS.md` 迁入并扩展：

- 仓库事实基线。
- 分层边界。
- 标准开发命令。
- 测试与验证要求。
- 文档同步规则。
- 禁止事项。
- 输出约定。

### 5.3 `.ai/project/`

项目结构和运行时导航。

来源主要是旧架构文档，但拆成多个小文件：

- `overview.md`: 系统定位和技术栈。
- `architecture.md`: 总体架构。
- `layers.md`: `api/services/repo/tasks/models/core` 分层说明。
- `runtime.md`: FastAPI、Taskiq、lifespan、broker、数据库配置。
- `deployment.md`: Docker、Helm、worker、探针。
- `observability.md`: Prometheus、HTTP、ORM、Layer、Task 指标。
- `data-models.md`: 表模型、协议模型、JSON 字段、迁移元数据。
- `domain-status.md`: 各领域模块实现状态矩阵。

### 5.4 `.ai/protocols/`

协议导航和实现映射。

不保存协议全文，不替代本地 `.protocol/`。

每个协议目录包含：

- `source-files.md`: 原始协议 PDF/Word 文件位置和用途。
- `interface-index.md`: 协议接口索引，包含章节、路径、方法和业务域。
- `implementation-map.md`: 协议接口到 `api/`、`services/`、`repo/`、`tasks/` 的映射。
- `model-index.md`: 协议对象到 `models/` 的映射。
- `testing-map.md`: 协议相关测试文件入口。
- `known-gaps.md`: 当前实现与协议原文之间的已知差异。

协议目录中的每个文件都应声明：

```text
若本文与本地 .protocol/ 原始协议冲突，以 .protocol/ 为准。
```

### 5.5 `.ai/testing/`

测试说明拆分目录。

来源主要是旧测试文档：

- `environment.md`: 依赖、启动方式、环境变量、测试数据策略。
- `layers.md`: 健康、接口、协议、异步一致性、分层边界、监控测试。
- `api-matrix.md`: 当前接口测试矩阵。
- `protocol-checklist.md`: 协议符合性检查清单。
- `baseline-cases.md`: 建议最小基线用例。
- `pytest.md`: 自动化落地方式。
- `report-template.md`: 测试报告模板。

### 5.6 `.ai/workflows/`

AI 执行任务时的流程卡。

建议先建立以下文件：

- `add-api-endpoint.md`: 新增接口流程。
- `protocol-change.md`: 协议相关变更流程。
- `database-migration.md`: schema 变更和 Alembic 流程。
- `async-task-change.md`: Taskiq 写链路变更流程。
- `pre-commit-checklist.md`: 提交前检查清单。

### 5.7 `.ai/plans/archive/`

归档历史设计和实施计划。

建议承接旧历史计划目录中的已有文件。迁移后保留索引：

- 按日期列出历史计划。
- 标记设计文档和实施计划。
- 不要求 AI 默认全量读取，只在需要追溯时查阅。

## 6. 协议文档处理策略

### 6.1 原始协议

本地保留在：

```text
.protocol/1400/
.protocol/2350/
```

这些文件是最高权威，不迁移、不拆分、不改写。

仓库处理规则：

- `.protocol/` 加入 `.gitignore`。
- 已经被 Git 跟踪的 `.protocol/` 文件从索引中移除。
- 不删除开发机上的本地协议原始文件。
- 若其他开发环境没有 `.protocol/`，需要由维护者单独提供原始协议资料。

### 6.2 AI 协议简介

放在：

```text
.ai/protocols/1400/
.ai/protocols/2350/
```

AI 协议简介的目标是让 AI 快速知道：

- 原始协议文件在哪里。
- 某个接口属于哪个协议章节。
- 本项目中对应的路由、模型、服务、任务和测试在哪里。
- 当前实现有哪些已知差异。
- 修改时必须检查哪些文件。

### 6.3 不做的事情

- 不把 PDF/Word 转成完整 Markdown 协议正文。
- 不在 `.ai/` 中维护第二份协议权威文本。
- 不用当前代码行为覆盖协议原意。

## 7. 迁移策略

建议分阶段执行：

### 阶段 1: 清理原始协议跟踪状态

- 将 `.protocol/` 加入 `.gitignore`。
- 使用 `git rm --cached` 从仓库索引移除已跟踪的 `.protocol/` 原始文件。
- 验证本地 `.protocol/` 文件仍存在。
- 验证 `git ls-files .protocol` 无输出。

### 阶段 2: 建立 `.ai/` 骨架

- 创建 `.ai/README.md`。
- 创建 `.ai/AGENTS.md`。
- 创建 `.ai/project/`、`.ai/protocols/`、`.ai/testing/`、`.ai/workflows/`、`.ai/plans/archive/`。
- 根 `AGENTS.md` 改为薄入口。

### 阶段 3: 拆分旧架构文档

- 迁入 `.ai/project/`。
- 按架构、分层、运行时、部署、观测、数据模型、领域状态拆分。

### 阶段 4: 拆分旧测试文档

- 迁入 `.ai/testing/`。
- 按测试环境、测试分层、接口矩阵、协议检查、基线用例、pytest、报告模板拆分。

### 阶段 5: 整理协议简介

- 将旧 1400/2350 协议整理文档转成 `.ai/protocols/*/` 下的简介、索引、映射和差异清单。
- 不复制协议全文。
- 每个协议目录明确指向 `.protocol/` 原始文件。

### 阶段 6: 迁移历史计划

- 将旧历史计划目录迁入 `.ai/plans/archive/`。
- 建立索引文件。

### 阶段 7: 清理旧文档位置

- 不保留旧文档目录下的跳转文件。
- 迁移完成后删除旧文档目录。
- 迁移时同步更新所有旧文档路径引用。

## 8. 文档优先级

迁移后建议文档优先级为：

1. 本地 `.protocol/` 原始协议文件。
2. `.ai/AGENTS.md` 和根 `AGENTS.md`。
3. `.ai/project`、`.ai/protocols`、`.ai/testing`、`.ai/workflows` 中的整理文档。
4. 当前代码实现。

如果协议原文、AI 整理文档和代码实现冲突，AI 必须先回到 `.protocol/` 查证。

## 9. 验证方式

实施拆分时建议验证：

- `git status --short` 确认迁移范围。
- 检查旧文档路径引用是否需要更新。
- 检查旧历史计划路径引用是否需要更新。
- `git ls-files .protocol` 确认原始协议文件不再被 Git 跟踪。
- `git ls-files -ci --exclude-standard` 确认没有被忽略文件仍被 Git 跟踪。
- `pytest -q` 按仓库约定尝试运行。

如果当前环境缺少 `pytest`，需要在结果中说明。

## 10. 已确认审核结论

已确认：

1. 根 `AGENTS.md` 作为薄入口，完整规则迁入 `.ai/AGENTS.md`。
2. 原始协议保持为本地 `.protocol/` 独立目录，不迁入 `.ai/`；同时加入 `.gitignore` 并从 Git 跟踪中移除。
3. `.ai/protocols/` 只放协议简介、索引、映射和差异清单，不复制完整协议正文。
4. 不保留旧文档跳转文件；迁移完成后直接删除旧文档目录。
5. 旧历史计划目录迁入 `.ai/plans/archive/`。

## 11. 本次设计结论

推荐建立 `.ai/` 作为 AI 协作资料的统一目录，并保持根 `AGENTS.md` 作为自动发现入口。

本地 `.protocol/` 继续保存原始协议，但不再作为仓库跟踪内容；`.ai/protocols/` 只保存 AI 可读的协议导航和实现映射。旧架构/协议/测试文档内容应在迁移时按主题拆分，避免大文件平移；迁移完成后删除旧文档目录。
