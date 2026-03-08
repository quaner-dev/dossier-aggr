# PROTOCOL 1400

更新时间：2026-03-05  
适用范围：`dossier-aggr` 仓库内 GA/T 1400 协议契约

## 1. 文档目的

本文仅描述 1400 协议契约，不包含代码缺陷与修复建议。  
工程实现差距与 Codex 执行约束请参考：`.docs/PROTOCOL_1400_FOR_CODEX.md`。

说明：2026-03-05 本次调整为分层重构与错误语义收敛（`services/repositories/tasks`），1400 接口 URL 不变。
补充：`/metrics` 为运维监控端点，不属于 1400 协议接口集合。

## 2. 协议范围

### 2.1 GA/T 1400.4-2017（接口）

覆盖接口：

- 7.2.1 注册消息
- 7.2.2 注销消息
- 7.2.3 保活消息
- 7.2.4 系统时间查询
- 7.2.5 采集设备查询/修改
- 7.2.6 采集系统查询
- 7.2.11.1 批量人员增删改查
- 7.2.11.2 单个人员查询
- 7.2.12.1 批量人脸增删改查
- 7.2.20.1 批量订阅创建
- 7.2.20.2 订阅查询/更新/删除
- 7.2.20.3 取消订阅
- 7.2.21.1 通知消息
- 7.2.21.2 单条通知记录查询

### 2.2 GA/T 1400.3-2017（对象）

覆盖对象：

- A.1 `APE`
- A.3 `APS`
- A.8 `Person`
- A.9 `Face`
- A.19 `Subscribe`
- A.20 `SubscribeNotification`
- A.26 `ResponseStatus`
- C.6 `SubImageInfo`
- C.8 `PersonList`
- C.9 `FaceList`
- C.19 `SubscribeList`
- C.20 `SubscribeNotificationList`
- C.25 `ResponseStatusList`
- C.26 `RegisterSchema`
- C.27 `KeepaliveSchema`
- C.28 `UnRegisterSchema`
- C.29 `SystemTime`

## 3. 通用契约规则

### 3.1 URL 常量

协议路径（`constants.py`）：

- `/VIID/System/Register`
- `/VIID/System/UnRegister`
- `/VIID/System/Keepalive`
- `/VIID/System/Time`
- `/VIID/APSs`
- `/VIID/APEs`
- `/VIID/Persons`
- `/VIID/Faces`
- `/VIID/Subscribes`
- `/VIID/SubscribeNotifications`

### 3.2 鉴权

- `Register` 接口使用 Digest 鉴权。
- 其余 1400 接口当前不要求 Digest。

### 3.3 字段命名与包装

- 字段命名保持协议风格（驼峰，大小写敏感）。
- 列表对象使用 `<Domain>ListObject` 包装。
- 状态返回使用 `ResponseStatus` 或 `ResponseStatusList` / `ResponseStatusListSchema`。
- `ResponseStatusListObject.ResponseStatusObject` 统一为数组结构。

### 3.4 时间格式

- 协议时间字段统一格式：`YYYYMMDDHHMMSS`。
- 典型字段：`LocalTime`、`BeginTime`、`EndTime`。

### 3.5 枚举编码

- `IntEnum` 字段使用整数语义值。
- `StrEnum` 字段使用字符串语义值。

## 4. 接口契约

## 4.1 System

| 方法 | 路径 | 请求模型 | 响应模型 | 说明 |
| --- | --- | --- | --- | --- |
| POST | `/VIID/System/Register` | `RegisterSchema` | `ResponseStatusList` | 注册消息 |
| POST | `/VIID/System/UnRegister` | `UnRegisterSchema` | `ResponseStatus` | 注销消息 |
| POST | `/VIID/System/Keepalive` | `KeepaliveSchema` | `ResponseStatus` | 保活消息 |
| GET | `/VIID/System/Time` | 无 | `SystemTime` | 系统时间查询 |

## 4.2 Collection

| 方法 | 路径 | 请求模型 | 响应模型 | 说明 |
| --- | --- | --- | --- | --- |
| GET | `/VIID/APSs` | 无 | `APSListSchema` | 采集系统查询 |
| GET | `/VIID/APEs` | 无 | `APEListSchema` | 采集设备查询 |
| PUT | `/VIID/APEs` | `APEListSchema` | `ResponseStatusListSchema` | 采集设备批量修改 |

## 4.3 Person

| 方法 | 路径 | 请求模型 | 响应模型 | 说明 |
| --- | --- | --- | --- | --- |
| GET | `/VIID/Persons` | 可选查询参数 `person_ids`/`source_id`/`device_id` | `PersonListObjectSchema` | 批量人员查询 |
| POST | `/VIID/Persons` | `PersonListObjectSchema` | `ResponseStatusListSchema` | 批量人员增加 |
| PUT | `/VIID/Persons` | `PersonListObjectSchema` | `ResponseStatusListSchema` | 批量人员修改 |
| DELETE | `/VIID/Persons` | `person_ids`（逗号分隔或列表） | `ResponseStatusListSchema` | 批量人员删除 |
| GET | `/VIID/Persons/{person_id}` | 路径参数 `person_id` | `Person` | 单个人员查询 |

## 4.4 Face

| 方法 | 路径 | 请求模型 | 响应模型 | 说明 |
| --- | --- | --- | --- | --- |
| GET | `/VIID/Faces` | 当前实现仅支持 `FaceID` 单条查询，或无 `FaceID` 时返回默认 `TOP100` 列表；未开放其他 Face 属性过滤键 | `FaceListObjectSchema` | 人脸查询 |
| POST | `/VIID/Faces` | `FaceListObjectSchema` | `ResponseStatusListSchema` | 批量人脸增加 |
| PUT | `/VIID/Faces` | `FaceListObjectSchema` | `ResponseStatusListSchema` | 批量人脸修改 |
| DELETE | `/VIID/Faces` | `id_list`（逗号分隔） | `ResponseStatusListSchema` | 批量人脸删除 |

## 4.5 Subscribe

| 方法 | 路径 | 请求模型 | 响应模型 | 说明 |
| --- | --- | --- | --- | --- |
| POST | `/VIID/Subscribes` | `SubscribeListSchema` | `ResponseStatusListSchema` | 批量订阅创建 |
| GET | `/VIID/Subscribes` | 无 | `SubscribeListSchema` | 订阅查询 |
| PUT | `/VIID/Subscribes` | `SubscribeListSchema` | `ResponseStatusListSchema` | 批量订阅更新 |
| DELETE | `/VIID/Subscribes` | `subscribe_ids`（逗号分隔或列表） | `ResponseStatusListSchema` | 批量订阅删除 |
| PUT | `/VIID/Subscribes/{subscribe_id}` | `Subscribe` | `ResponseStatus` | 取消订阅 |

## 4.6 SubscribeNotification

| 方法 | 路径 | 请求模型 | 响应模型 | 说明 |
| --- | --- | --- | --- | --- |
| POST | `/VIID/SubscribeNotifications` | `SubscribeNotificationListSchema` | `ResponseStatusListSchema` | 通知消息上报 |
| GET | `/VIID/SubscribeNotifications/{notification_id}` | 路径参数 `notification_id` | `SubscribeNotification` | 单条通知记录查询 |

## 5. 对象契约（摘要）

### 5.1 应答对象

- `ResponseStatus`
  - `RequestURL: str`
  - `StatusCode: str`
  - `StatusString: str`
  - `Id: str | None`
  - `LocalTime: VIIDDateTime | None`

- `ResponseStatusList`
  - `ResponseStatusObject: list[ResponseStatus]`

### 5.2 采集设备与系统

- `APS`：`ApsID`、`Name`、`IPAddr`、`Port`、`IsOnline` 等
- `APE`：`ApeID`、位置信息、方向枚举、归属 `OwnerApsID` 等
- `SystemTime`：`LocalTime`（`YYYYMMDDHHMMSS`）

### 5.3 人员与人脸

- `Person` 与 `Face` 均包含：
  - 唯一标识（`PersonID` / `FaceID`）
  - 来源与设备标识（`SourceID`、`DeviceID`）
  - 框选坐标（`LeftTopX`、`LeftTopY`、`RightBtmX`、`RightBtmY`）
  - `SubImageList`（JSON 结构）

### 5.4 订阅与通知

- `Subscribe`：订阅范围、时间窗、状态、结果声明等。
- `SubscribeNotification`：通知标识、触发信息、关联人脸/人员对象列表。

## 6. 错误响应契约

- 业务错误场景返回 `ResponseStatus*` 风格对象。
- 常见语义：
  - 不存在：HTTP `404` + `StatusCode=404`（`DataNotFound`）
  - 已存在：HTTP `409` + `StatusCode=409`（`DataAlreadyExists`）
  - 参数错误：HTTP `400` + `StatusCode=400`（`InvalidParameter`）
  - 任务执行超时/失败：HTTP `503` + `StatusCode=503`（`TaskExecutionError`）

## 7. 协议一致性检查清单

1. 路径与方法匹配上表定义。  
2. 请求/响应可被对应模型校验。  
3. 时间字段格式为 `YYYYMMDDHHMMSS`。  
4. 枚举字段取值符合模型定义。  
5. 批量写操作返回状态对象数量与输入数量一致。  
6. `RequestURL`、`StatusCode`、`StatusString` 在回包中完整出现。

## 8. 关联文档

- 实现差距与 Codex 约束：`.docs/PROTOCOL_1400_FOR_CODEX.md`
- 架构总览：`.docs/ARCHITECTURE.md`
- 测试规范：`.docs/TESTING.md`
