# Protocol Style Runtime Chain VIAS Tasks Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 沉淀协议优先和命名规则，补齐 runtime chain 图，并将 GA/T 2350.5 A.6 `/VIAS/Tasks` 纳入完整实现链路。

**Architecture:** 文档规则进入 `.ai/project/`，协议状态进入 `.ai/protocols/2350/`。代码按既有分层补齐 `api -> services -> tasks -> repo -> models`，并保持 TDD：先写失败测试，再做最小实现。

**Tech Stack:** FastAPI, SQLModel, Taskiq, Alembic, pytest, Markdown Mermaid

---

### Task 1: Tests First

**Files:**
- Modify: `tests/test_api_subscribe.py`
- Create: `tests/test_api_archive_task.py`
- Modify: `tests/protocol/test_2350_routes.py`

- [x] 写测试期望 `api.subscribe.subscribe` 和 `subscribes_create` 存在。
- [x] 写 `/VIAS/Tasks` API direct-call 测试，覆盖查询、创建、更新、删除响应包装。
- [x] 更新 2350 route guard，要求 `/VIAS/Tasks` 出现在 OpenAPI 且支持 GET/POST/PUT/DELETE。
- [x] 运行 targeted tests，确认当前因缺失模块或 route 失败。

### Task 2: Project AI Docs

**Files:**
- Create: `.ai/project/code-style.md`
- Create: `.ai/project/runtime-chain.md`
- Modify: `.ai/project/README.md`

- [x] 记录协议优先、强命名规则、查询语义、死代码/错误协议处理、TDD 策略。
- [x] 使用 Mermaid 描述 `api -> services -> tasks -> repo -> models/database` runtime chain。
- [x] 在项目文档索引中加入新文档入口。

### Task 3: Subscribe Naming

**Files:**
- Rename: subscribe API module to `api/subscribe/subscribe.py`
- Modify: `api/__init__.py`
- Modify: `tests/test_api_subscribe.py`

- [x] 将订阅创建 handler 改为 `subscribes_create`。
- [x] 更新路由聚合和测试导入。
- [x] 不改变 URL、请求体、响应体和服务层行为。

### Task 4: A.6 VIAS Tasks Runtime Chain

**Files:**
- Modify: `core/constants.py`
- Create: `api/task/archive_task.py`
- Create: `services/task/archive_task.py`
- Create: `tasks/task/archive_task.py`
- Create: `repo/task/archive_task.py`
- Modify: `api/__init__.py`
- Modify: `services/__init__.py`
- Modify: `services/task/__init__.py`
- Modify: `tasks/__init__.py`
- Modify: `tasks/task/__init__.py`
- Modify: `repo/task/__init__.py`

- [x] 新增 `ARCHIVE_TASKS_URL = "/VIAS/Tasks"`。
- [x] 实现 GET/POST/PUT/DELETE，协议包装使用 `ArchiveTaskListSchema` 与 `ResponseStatusListSchema`。
- [x] service 读路径走 repo，写路径通过 `dispatch_and_wait` 走 Taskiq task。
- [x] task 只委托 repo。
- [x] repo 执行 SQLModel 数据访问，按 `TaskID` 去重、更新和删除。

### Task 5: Protocol Docs Sync

**Files:**
- Modify: `.ai/protocols/2350/README.md`
- Modify: `.ai/protocols/2350/interface-index.md`
- Modify: `.ai/protocols/2350/implementation-map.md`
- Modify: `.ai/protocols/2350/known-gaps.md`
- Modify: `.ai/testing/api-matrix.md`
- Modify: `.ai/project/domain-status.md`
- Modify: `.ai/project/data-models.md`

- [x] 将 A.6 从“不实现”改为已纳入实现。
- [x] 保留对 GA/T 1399-2017 完整 Task 字段来源的差异说明。
- [x] 更新测试矩阵和领域状态。

### Task 6: Verification

**Files:**
- All modified files

- [x] 运行 targeted tests。
- [x] 运行 `python3 -m compileall` 覆盖新增/修改 Python 文件。
- [x] 尝试 `pytest -q`，若环境缺依赖，记录具体原因。
