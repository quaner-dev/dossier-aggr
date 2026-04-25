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
- targeted tests 通过后再运行 `pytest -q`。
- 若环境缺少依赖或测试无法执行，必须记录具体命令和失败原因。
