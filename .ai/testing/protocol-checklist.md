# Protocol Checklist

## URL 与资源命名

- 路径必须使用 `core/constants.py` 中定义值。
- 资源命名保持协议复数形式。

## 消息包装结构

- 批量对象必须使用 `<Domain>ListObject` 包装。
- 状态返回优先使用 `ResponseStatusListSchema`。
- A.17/A.18 正式版成功响应为 `ArchiveList` / `VehicleArchiveList`。
- 字段名保持协议风格，大小写敏感。

## 日期时间格式

- 协议时间按 `YYYYMMDDHHMMSS` 处理。
- 重点字段：`BeginTime`、`EndTime`、`LocalTime`、`CreateTime`、`UpdateTime`。

## 枚举值

- `IntEnum` 字段使用整数语义值。
- `StrEnum` 字段使用协议约定字符串值。

## 错误语义

- `DataNotFoundError`：HTTP 404 + 协议状态对象。
- `DataAlreadyExistsError`：HTTP 409 + 协议状态对象。
- `InvalidParameterError` / 请求校验错误：HTTP 400 + 协议状态对象。
- `TaskExecutionError`：HTTP 503 + 协议状态对象。

协议测试应同时断言 HTTP 状态码、`StatusCode` / `StatusString` 和响应包装对象形状。
