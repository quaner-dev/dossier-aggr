# Layer Boundaries

本文件是分层职责和禁止事项的唯一来源。总体组件关系见 `.ai/project/architecture.md`；接口级链路图见 `.ai/project/runtime-chain.md`。

## `api/`

- 定义 HTTP 路由。
- 编排请求模型、响应模型和路径/查询参数。
- 不直接操作数据库。
- 不内联业务逻辑。

## `services/`

- 承担业务校验与业务编排。
- 同步读取优先调用 `repo/`。
- 异步写入通过 `tasks/` 投递，不直接绕过任务边界实现写链路。
- 统一使用 `dispatch_and_wait` 等共享任务调度能力。

## `repo/`

- 承担数据访问逻辑。
- 使用 `AsyncSession(engine)`、`select/delete`、持久化异常语义。
- 不处理 HTTP 协议编排。

## `tasks/`

- 作为 Taskiq 异步入口层。
- 任务函数委托 `repo/` 执行实际数据访问。
- 不处理 HTTP 协议编排。
- 不把查询、过滤、分页或持久化细节直接内联在任务函数中。

## `models/`

- 保存协议模型与数据模型。
- 模型变更优先复用现有对象和校验方式。
- 新建或修改模型时优先使用 `model_validate` 做转换。

## `core/`

- 保存配置、数据库、异常、常量、认证、broker 和工具函数。
- 不承载具体协议业务逻辑。
