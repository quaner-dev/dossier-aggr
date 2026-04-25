# PROTOCOL 2350

更新时间：2026-03-11  
适用范围：`dossier-aggr` 仓库内 GA/T 2350.5-2025 协议契约

## 1. 文档目的

本文描述 2350 正式版协议要求，并标注当前仓库实现现状与已确认差异。  
协议基线优先级遵循仓库约束：`.protocol/2350/*` > `.docs/*` > 当前代码行为。

说明：2026-03-11 协议基线已切换到正式版标准；当前仓库仍存在若干接口与对象偏差，本文件用于明确正式版要求与当前实现的差距。
补充：`/metrics` 为运维监控端点，不属于 2350 协议接口集合。

协议原始依据：

- `.protocol/2350/GA-T 2350.5-2025.pdf`
  - 封面信息：`2025-10-13` 发布，`2026-02-01` 实施

## 2. 协议范围

### 2.1 GA/T 2350.5-2025（接口）

覆盖接口条目（附录 A）：

- A.5 目标档案库增加、查询、更新、删除接口
- A.6 聚档任务增加、查询、更新、删除接口
- A.7 档案和轨迹订阅接口
- A.8 档案和轨迹通知接口
- A.9 人员基础信息查询接口
- A.10 人员基础信息增加、更新、删除接口
- A.11 车辆基础信息查询接口
- A.12 车辆基础信息增加、更新、删除接口
- A.13 人员明细信息查询接口
- A.14 人员明细信息增加、更新、删除接口
- A.15 车辆明细信息查询接口
- A.16 车辆明细信息增加、更新、删除接口
- A.17 人员核验接口
- A.18 车辆核验接口

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
- 查询请求包装使用 `ArchiveQueryObject` / `ArchiveSubjectQueryObject`。
- 查询结果包装使用 `ArchiveQueryResultObject` / `ArchiveSubjectQueryResultObject`。
- 批量写操作默认返回 `ResponseStatusListSchema`。
- A.17/A.18 为正式版例外：返回体应为 `ArchiveList` / `VehicleArchiveList`，而不是状态列表。

### 3.3 时间格式

- 协议时间字段统一格式：`YYYYMMDDHHMMSS`。
- 典型字段：`BeginTime`、`EndTime`、`CreateTime`、`UpdateTime`。

### 3.4 枚举编码

- `IntEnum` 字段使用整数语义值。
- `StrEnum` 字段使用字符串语义值。

## 4. 接口契约（附录 A 映射）

说明：下表左侧为正式版协议要求，右侧记录当前仓库状态与已确认差异。

| 条款 | URL | 当前仓库状态 |
| --- | --- | --- |
| A.5 | `/VIID/ArchiveLibraries` | 已基本对齐（同一路径承载批量 GET/POST/PUT/DELETE；GET 支持 `ArchiveLibrary` 属性键值对查询，DELETE 使用 `IDList`） |
| A.6 | `/VIAS/Tasks` | 未实现（当前交付范围不包含 VIAS 接口） |
| A.7 | `/VIID/Subscribes` | 复用 1400 路由，接口路径已暴露；2350 扩展语义仍需结合正式版对象继续核对 |
| A.8 | `/VIID/SubscribeNotifications` | 已基本对齐：当前仍复用 1400 路由，但通知对象已补齐 `ArchiveObjectList`、`VehicleArchiveObjectList`、`ArchiveSubjectList` 三类 2350 扩展列表；同时保留 1400 的 face/person 列表以兼容共享接口 |
| A.9 | `/VIID/ArchivesQuerySync` | 已基本对齐：当前已使用 `POST /VIID/ArchivesQuerySync` + `<ArchiveQuery>`，且 `ArchiveQuery` 字段集合已补齐正式版 B.6；当前已支持部分 `Fields` 以及 `PictureQueryCondition.SubjectID -> Archive.SourceIDList` 的筛查，但尚未实现图片相似度、时间、区域、设备等正式版检索语义 |
| A.10 | `/VIID/Archives` | 已基本对齐：批量增改删已实现；DELETE 已使用 `IDList`，`Archive` 对象字段已切换到正式版 B.3 形态 |
| A.11 | `/VIID/VehicleArchivesQuerySync` | 已基本对齐：当前已使用 `POST` + `<ArchiveQuery>` -> `<ArchiveQueryResult>`；当前已支持部分 `Fields` 以及 `PictureQueryCondition.SubjectID -> VehicleArchive.SourceIDList` 的筛查，但尚未实现图片相似度、时间、区域、设备等正式版检索语义 |
| A.12 | `/VIID/VehicleArchives` | 已基本对齐（VehicleArchive 批量增改删主链路；DELETE 使用 `IDList`，对象字段已切换到正式版 B.4 形态） |
| A.13 | `/VIID/ArchiveSubjectQuerySync` | 已基本对齐：当前已接收 `POST` + `<ArchiveSubjectQuery>` 并返回查询结果包装；当前已支持 `ArchiveIDList` 与 `PictureQueryCondition.SubjectID`，其中 `SubjectID` 会匹配 person/face/gait/motor/non-motor 五类 ID 列表，但仍未覆盖时间、区域、设备等正式版查询语义 |
| A.14 | `/VIID/ArchiveSubjects` | 已基本对齐：批量增改删已实现；DELETE 已支持正式版五类删除键（`ArchiveID`、`FaceIDList`、`PersonIDList`、`MotorVehicleIDList`、`NonMotorVehicleIDList`） |
| A.15 | `/VIID/VehicleArchiveSubjectQuerySync` | 已基本对齐：当前已接收 `POST` + `<ArchiveSubjectQuery>` 并返回查询结果包装；车辆明细对象已补齐 person/face/gait/motor/non-motor 五类 ID/Object 列表，当前已支持 `ArchiveIDList` 与 `PictureQueryCondition.SubjectID`，但仍未覆盖时间、区域、设备等正式版查询语义 |
| A.16 | `/VIID/VehicleArchiveSubjects` | 已基本对齐：批量增改删已实现；DELETE 已支持正式版五类删除键（`ArchiveID`、`FaceIDList`、`PersonIDList`、`MotorVehicleIDList`、`NonMotorVehicleIDList`） |
| A.17 | `/VIID/ArchiveConfidence` | 已基本对齐：当前已使用 `POST <ArchiveList>` 并返回 `<ArchiveList>`；`Archive` 对象字段已贴合正式版 B.3 |
| A.18 | `/VIID/VehicleArchiveConfidence` | 已基本对齐：当前已使用 `POST <VehicleArchiveList>` 并返回 `<VehicleArchiveList>`；`VehicleArchive` 对象字段已贴合正式版 B.4 |

## 5. 对象契约（附录 B 摘要）

### 5.1 已基本对齐对象

- `ArchiveLibrary`：当前字段集合与 B.2 基本一致（`ArchiveLibraryID`、`Name`、`CreateTime`、`Memo`）。
- `Archive`、`VehicleArchive`：当前字段集合已覆盖正式版 B.3/B.4，`SourceIDList`、`CenterFeatureList`、`Similaritydegree`、`Confidence`、`SubImageList` 等字段已纳入协议模型。
- `ArchiveSubject`：当前字段集合已覆盖正式版 B.5 的五类 ID/Object 列表；`VehicleArchiveSubject` 也已同步补齐对应 person/face/gait/motor/non-motor 列表字段。
- `ArchiveQuery`、`ArchiveSubjectQuery`：当前字段集合已覆盖正式版 B.6/B.9，`PictureQueryCondition` 与 `Fields` 均已纳入模型。
- `Fields`：当前字段集合与正式版 B.14 一致（`ArchiveLibraryID`、`ArchiveIDList`、`PlaceCode`、车辆相关筛查字段）。
- `SubscribeNotification`：当前共享通知模型已补齐正式版 B.11 的 `ArchiveObjectList`、`VehicleArchiveObjectList`、`ArchiveSubjectList` 扩展列表。
- `FeatureInfo`：字段集合与 B.15 基本一致（`Vendor`、`AlgorithmVersion`、`FeatureData`）。
- `Gait`：当前字段集合已覆盖正式版 B.16（`GaitID`、`SourceID`、出现/消失时间、角度、人数、身高、`SubImageList`）。
- `GeoRectangle`、`DeviceSelector`：字段名与正式版保持一致。

### 5.2 已确认对象差异

- `ArchiveSubject` / `VehicleArchiveSubject`：机动车、非机动车对象列表当前使用宽松 JSON 容器承载，仓库内尚未引入 1400 的正式机动车/非机动车对象模型。
- `SubscribeNotification`：当前通知对象为了兼容 1400 仍保留 `FaceObjectList` / `PersonObjectList`，属于“1400 + 2350 扩展并存”的共享模型，而非纯 2350 专用对象。

## 6. 错误响应契约

- 批量写操作接口返回 `ResponseStatusListSchema` 风格状态对象。
- `ResponseStatusListObject.ResponseStatusObject` 统一为数组结构。
- 错误语义应包含 `StatusCode`、`StatusString`，并保持协议包装结构一致。
- A.17/A.18 不应使用状态列表作为成功响应体；正式版成功返回应分别为 `ArchiveList` 与 `VehicleArchiveList`。

## 7. 协议一致性检查清单

1. 路径与条款 A.5-A.18 一一对应。  
2. HTTP 方法、请求体和返回体与附录 A 保持一致。  
3. 对象字段与附录 B 保持一致，禁止仅以当前代码行为代替协议原意。  
4. 时间字段格式为 `YYYYMMDDHHMMSS`。  
5. 枚举字段取值符合模型定义。  
6. 包装对象命名与大小写保持一致。  

## 8. 当前已确认差异列表

- A.6 `/VIAS/Tasks` 当前明确不纳入本服务实现范围。
- A.9/A.11/A.13/A.15 当前查询行为仍未覆盖正式版全部检索语义；目前仅实现部分 `Fields` 和 `PictureQueryCondition.SubjectID` 路径。
- `ArchiveSubject` / `VehicleArchiveSubject` 的机动车、非机动车对象列表仍使用宽松 JSON 容器。

## 9. 关联文档

- 架构总览：`.docs/ARCHITECTURE.md`
- 测试规范：`.docs/TESTING.md`
- 1400 协议契约：`.docs/PROTOCOL_1400.md`
