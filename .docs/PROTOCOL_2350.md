# PROTOCOL 2350

更新时间：2026-03-05  
适用范围：`dossier-aggr` 仓库内 GA/T 2350.5-2025 协议契约

## 1. 文档目的

本文仅描述 2350 协议契约，不包含实现差距修复方案。  
协议基线优先级遵循仓库约束：`.protocol/2350/*` > `.docs/*` > 当前代码行为。

说明：2026-03-05 本次调整为分层重构与明细持久化（`services/repo/tasks`），2350 协议契约不变。
补充：`/metrics` 为运维监控端点，不属于 2350 协议接口集合。

协议原始依据：

- `.protocol/2350/附件4-《公安视频图像分析技术要求 第5部分：目标聚档服务》（报批稿）0606 - 修订.docx`

## 2. 协议范围

### 2.1 GA/T 2350.5-2025（接口）

覆盖接口条目（附录 A）：

- A.5 目标档案库增加、查询、更新、删除接口
- A.6 聚档任务增加、查询、更新、删除接口
- A.7 档案和轨迹订阅接口
- A.8 档案和轨迹通知接口
- A.9 人员档案查询接口
- A.10 人员档案增加、更新、删除接口
- A.11 车辆档案查询接口
- A.12 车辆档案增加、更新、删除接口
- A.13 人员档案明细查询接口
- A.14 人员档案明细增加、更新、删除接口
- A.15 车辆档案明细查询接口
- A.16 车辆档案明细增加、更新、删除接口
- A.17 人员档案核验接口
- A.18 车辆档案核验接口

### 2.2 GA/T 2350.5-2025（对象）

覆盖对象条目（附录 B）：

- B.2 `ArchiveLibrary`
- B.3 `Archive`
- B.4 `VehicleArchive`
- B.5 `ArchiveSubject`
- B.6 `ArchiveQuery`
- B.7 `PictureQueryCondition`
- B.8 `ArchiveQueryResult`
- B.9 `ArchiveSubjectQuery`
- B.10 `ArchiveSubjectQueryResult`
- B.11 `SubscribeNotification`
- B.12 `GeoRectangle`
- B.13 `DeviceSelector`
- B.14 `Fields`
- B.15 `FeatureInfo`
- B.16 `Gait`

## 3. 通用契约规则

### 3.1 URL 资源

附录 A 资源路径（含 1400 复用路径）：

- `/VIID/ArchiveLibraries`
- `/VIAS/Tasks`
- `/VIID/Subscribes`
- `/VIID/SubscribeNotifications`
- `/VIID/Archives`
- `/VIID/ArchivesQuerySync`
- `/VIID/ArchiveSubjects`
- `/VIID/ArchiveSubjectQuerySync`
- `/VIID/VehicleArchives`
- `/VIID/VehicleArchivesQuerySync`
- `/VIID/VehicleArchiveSubjects`
- `/VIID/VehicleArchiveSubjectQuerySync`
- `/VIID/ArchiveConfidence`
- `/VIID/VehicleArchiveConfidence`

补充说明（1400 复用路径同步）：

- `/VIID/Subscribes/{subscribe_id}`
- `/VIID/System/Time`

### 3.2 字段命名与包装

- 字段命名保持协议风格（驼峰，大小写敏感）。
- 查询请求包装优先使用 `ArchiveQueryObject` / `ArchiveSubjectQueryObject`。
- 查询结果包装优先使用 `ArchiveQueryResultObject` / `ArchiveSubjectQueryResultObject`。
- 写操作状态返回使用 `ResponseStatusListSchema`。

### 3.3 时间格式

- 协议时间字段统一格式：`YYYYMMDDHHMMSS`。
- 典型字段：`BeginTime`、`EndTime`、`CreateTime`、`UpdateTime`。

### 3.4 枚举编码

- `IntEnum` 字段使用整数语义值。
- `StrEnum` 字段使用字符串语义值。

## 4. 接口契约（附录 A 映射）

说明：方法与消息体细节以附件对应表 A.4-A.17 为准；下表用于仓库实现映射。

| 条款 | URL | 当前仓库状态 |
| --- | --- | --- |
| A.5 | `/VIID/ArchiveLibraries` | 已实现（同一路径承载批量 GET/POST/PUT/DELETE；GET 支持 `ArchiveLibrary` 属性键值对查询，DELETE 使用 `IDList`） |
| A.6 | `/VIAS/Tasks` | 未实现（当前交付范围不包含 VIAS 接口） |
| A.7 | `/VIID/Subscribes` | 复用 1400 路由（含 2350 复用能力） |
| A.8 | `/VIID/SubscribeNotifications` | 复用 1400 路由（含 2350 复用能力） |
| A.9 | `/VIID/ArchivesQuerySync` | 已实现（Archive 查询主链路） |
| A.10 | `/VIID/Archives` | 已实现（Archive 增改删主链路） |
| A.11 | `/VIID/VehicleArchivesQuerySync` | 已实现（`POST` + `<ArchiveQuery>` -> `<ArchiveQueryResult>` 的 VehicleArchive 查询主链路） |
| A.12 | `/VIID/VehicleArchives` | 已实现（VehicleArchive 批量增改删主链路；DELETE 使用 `IDList`） |
| A.13 | `/VIID/ArchiveSubjectQuerySync` | 已实现（ArchiveSubject 查询主链路） |
| A.14 | `/VIID/ArchiveSubjects` | 已实现（ArchiveSubject 增改删主链路；删除仅按 `ArchiveID`） |
| A.15 | `/VIID/VehicleArchiveSubjectQuerySync` | 已实现（VehicleArchiveSubject 查询主链路） |
| A.16 | `/VIID/VehicleArchiveSubjects` | 已实现（VehicleArchiveSubject 增改删主链路） |
| A.17 | `/VIID/ArchiveConfidence` | 已实现（人员档案核验主链路） |
| A.18 | `/VIID/VehicleArchiveConfidence` | 已实现（车辆档案核验主链路） |

## 5. 对象契约（附录 B 摘要）

### 5.1 档案库/档案对象

- `ArchiveLibrary`：档案库标识、名称、创建时间、备注。
- `Archive`：档案标识、档案库标识、身份信息、时间信息、图像标识。
- `VehicleArchive`：车辆档案基础信息对象（字段以附录 B.4 为准）。

### 5.2 档案明细与查询对象

- `ArchiveSubject`：档案明细对象（人员、人脸及关联标识）。
- `ArchiveQuery` / `ArchiveSubjectQuery`：查询条件对象。
- `ArchiveQueryResult` / `ArchiveSubjectQueryResult`：查询结果对象。

### 5.3 通用对象

- `PictureQueryCondition`、`GeoRectangle`、`DeviceSelector`、`Fields`。
- `FeatureInfo`、`Gait`。
- `SubscribeNotification`（含 2350 扩展对象列表时按附件约束处理）。

## 6. 错误响应契约

- 写操作接口返回 `ResponseStatusListSchema` 风格状态对象。
- `ResponseStatusListObject.ResponseStatusObject` 统一为数组结构。
- 错误语义应包含 `StatusCode`、`StatusString`，并保持协议包装结构一致。
- 典型错误状态：
  - HTTP `404`（资源不存在）
  - HTTP `409`（资源冲突/已存在）
  - HTTP `400`（参数校验失败）
  - HTTP `503`（任务执行超时或不可用）

## 7. 协议一致性检查清单

1. 路径与条款 A.5-A.18 一一对应。  
2. 请求/响应可被对应模型校验（未落地项标注 TBD）。  
3. 时间字段格式为 `YYYYMMDDHHMMSS`。  
4. 枚举字段取值符合模型定义。  
5. 批量写操作返回状态对象数量与输入条目语义一致。  
6. 包装对象命名与大小写保持一致。  

## 8. 当前代码待定项（TBD）

除 A.6 按当前交付范围省略外，其余条款已具备接口主链路实现；后续增强点为：

- A.6 `/VIAS/Tasks` 当前明确不纳入本服务实现范围
- A.7/A.8 已增加复用路由与关键字段约束测试（`tests/protocol/test_2350_routes.py`、`tests/protocol/test_2350_subscribe_contract.py`），仍可继续细化附录扩展字段语义
- A.13/A.14 与 A.15/A.16 已切换为 SQLModel 持久化仓储实现，后续可补充更多跨域一致性与性能回归

## 9. 关联文档

- 架构总览：`.docs/ARCHITECTURE.md`
- 测试规范：`.docs/TESTING.md`
- 1400 协议契约：`.docs/PROTOCOL_1400.md`
