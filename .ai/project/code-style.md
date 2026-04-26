# Code Style And Protocol Rules

## 协议优先

- 开发必须按 `.protocol/` 原始协议规范处理，不能凭空想象接口、字段、请求体或响应体。
- 当前代码行为不能覆盖协议原意。若代码、`.ai/` 文档和协议冲突，先回到 `.protocol/` 查证。
- 协议接口变更必须同步检查路径、HTTP 方法、请求消息体、返回消息体、字段名、时间格式和状态对象。
- 当前暂未完全支持的协议点必须写入 `.ai/protocols/*/known-gaps.md`，不能让代码或文档暗示已经完整实现。

## 命名规则

- 文件和目录使用协议领域名词，采用 `snake_case`，不允许拼写错误。
- `api/` 路由函数采用“协议资源名词 + 动作”的形式：
  - 集合查询：`resources_query`
  - 集合新增：`resources_create`
  - 集合更新：`resources_update`
  - 集合删除：`resources_delete`
  - 单资源查询：`resource_query`
  - 单资源更新：`resource_update`
  - 单资源删除：`resource_delete`
  - 查询同步：`resources_query_sync`
  - 核验接口：`resource_confidence_verify`
- `services/` 类名采用 `ResourceService`，方法采用动词开头，例如 `create_archives`、`delete_archive_subjects`。
- `tasks/` 函数采用动词开头并以 `_task` 结尾，例如 `create_archives_task`。
- `repo/` 函数采用动词开头并以 `_repo` 结尾，例如 `query_archives_repo`。
- 协议模型名、包装对象名和字段名以协议为准，例如 `ArchiveTaskListSchema`、`ArchiveIDList`，不为了 Python 风格改写协议字段。
- 命名重构不得改变 URL、协议字段、请求模型或响应模型。

## Pydantic 和参数模型边界

- 协议请求体、响应体、顶层包装对象、嵌套对象和跨层传递的复杂数据结构优先使用 Pydantic/SQLModel 模型表达。
- 边界层收到的协议对象应尽量通过现有模型校验，模型之间转换优先使用 `model_validate`。
- 少量简单参数不强制新建 Pydantic 模型；例如只有一个或两个路径/查询参数，且没有复用、嵌套校验、协议包装或跨层组合需求时，可以直接使用显式函数参数。
- 是否新增参数模型以维护成本为判断标准：若模型能降低重复校验、命名漂移、响应包装错误或跨层传参混乱，应使用模型；若模型只增加文件、类名和跳转成本，应保持简单参数。
- 不为了“统一都用模型”而创建只包装少量标量字段的临时模型；但协议已经定义的包装对象除外，必须按协议建模。

## 注释和 Docstring

- 项目统一使用 Google style docstring，不使用 Sphinx/reST 的 `:param:`、`:return:` 风格，也不自造固定注释块格式。
- Docstring 可使用中文；协议对象名、字段名、路径、错误类名和模型名保持代码/协议原文。
- 简单函数不强制写 docstring。协议模型、API 路由、复杂 service/repo/task 编排、非显然查询语义和兼容/缺口逻辑必须写。
- 协议模型 docstring 写协议号、章节和对象名；字段级语义优先通过 `Field(description=..., examples=...)` 进入 OpenAPI/JSON Schema。
- API 路由 docstring 只写接口级语义：协议来源、协议包装、成功/错误语义、兼容行为和边界约束；不要在路由 docstring 中重复完整字段表。
- Service、repo、task docstring 解释业务编排、查询语义和异步边界，不重复代码表面行为。
- 行内注释只解释“为什么”，例如协议例外、路径参数优先级、兼容原因和临时缺口；不要写“查询数据库”“执行删除”“导入对象”等无信息量注释。
- TODO 必须说明原因；若属于协议缺口，同步写入 `.ai/protocols/*/known-gaps.md`，若属于工程计划，写入对应计划或 workflow 文档。
- 暂不引入自动化无意义注释检查，代码评审时按上述原则人工把关。

## 查询语义

- 查询过滤、排序、分页、limit、空结果语义属于 `repo/` 责任。
- `api/` 只负责接收协议参数并交给 `services/`，不在路由函数中内联 SQL 查询或临时过滤逻辑。
- `services/` 只做业务编排，不拼 SQL。
- 若调整查询 SQL 形态，必须用测试确认 `WHERE`、`ORDER BY`、`LIMIT` 和空结果行为仍符合协议和既有约定。

## Runtime Chain

- 一个协议接口应尽量形成完整链路：`api -> services -> tasks -> repo -> models/database`。
- 同步读取可以由 `services/` 直接调用 `repo/`。
- 写路径优先由 `services/` 通过 `dispatch_and_wait` 投递 `tasks/`，再由 `tasks/` 委托 `repo/`。
- `tasks/` 不内联数据库访问逻辑。
- `repo/` 不处理 HTTP 编排和协议响应包装。

## 死代码和错误协议代码

- 如果接口不属于当前交付范围，不能只隐藏 route 后保留误导性的 runtime chain；应删除或明确标记未实现。
- 如果接口属于协议范围但实现错误，应按协议修正完整链路，而不是保留错误接口做默认兼容。
- 只有明确存在外部兼容需求时，才允许保留旧接口；保留时必须在 `.ai/protocols/*/known-gaps.md` 写明原因和风险。
- 数据模型和 Alembic 迁移历史不等同于 runtime chain。删除接口链路时，迁移历史通常需要保留。

## TDD 策略

- 行为变更先写失败测试，再做最小实现。
- 优先运行 targeted tests，确认本次变更对应行为。
- targeted tests 通过后，按 `.ai/workflows/pre-commit-checklist.md` 完成质量检查、类型检查和测试。
- 若环境缺少质量检查、类型检查或测试依赖，必须记录具体命令和失败原因。
