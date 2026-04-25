# Test Layers

## 健康与可用性

- `GET /startup`
- `GET /live`
- `GET /ready`，数据库可用性检查。

## 接口功能测试

- 按资源域覆盖 CRUD/查询能力。
- 对批量接口验证输入条数与返回状态条数一致。
- 对查询接口验证列表包装对象名与字段完整性。

## 协议符合性测试

- URL 与方法匹配 `core/constants.py`。
- 顶层包装对象命名正确。
- 时间字段为 `YYYYMMDDHHMMSS`。
- 枚举字段编码符合模型定义。
- 错误场景返回约定协议对象。

## 异步一致性测试

- 写接口调用后轮询查询接口确认最终一致性。
- 未启动 worker 时的行为作为负向用例保留。

## 分层边界测试

- `services` 同步读取路径不直接调用 `tasks`。
- `tasks` 作为异步入口层，不直接内联数据库访问。
- `collection`、`archive`、`archive_subject`、`task`、`vehicle`、`person`、`face`、`subscribe`、`verify` 域保留分层约束回归用例。

## 监控指标测试

- `/metrics` 必须可访问并返回 Prometheus 文本格式。
- 至少覆盖 HTTP 请求、HTTP 时延、ORM 查询等关键指标族。
