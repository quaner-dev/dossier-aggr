# PROTOCOL 2350

更新时间：2026-02-14  
适用范围：`dossier-aggr` 仓库内 GA/T 2350.5-2025 协议契约

## 1. 文档目的

本文仅描述 2350 协议契约，不包含实现差距、修复建议或工程执行策略。

## 2. 协议范围

### 2.1 GA/T 2350.5-2025（接口）

覆盖接口条目：

- A.5 档案库查询
- A.6 档案库增加
- A.7 档案库更新
- A.8 档案库删除
- A.9 人员档案查询
- A.10 人员档案增改删
- A.13 人员档案明细查询
- A.14 人员档案明细增改删

### 2.2 GA/T 2350.5-2025（对象）

覆盖对象条目：

- B.2 `ArchiveLibrary`
- B.3 `Archive`
- B.5 `ArchiveSubject`
- B.6 `ArchiveQuery`
- B.7 `PictureQueryCondition`
- B.8 `ArchiveQueryResult`
- B.9 `ArchiveSubjectQuery`
- B.10 `ArchiveSubjectQueryResult`
- B.12 `GeoRectangleType`
- B.13 `DeviceSelector`

## 3. 通用契约规则

### 3.1 URL 常量

协议路径（`constants.py`）：

- `/VIID/ArchiveLibraryQuerySync`
- `/VIID/ArchiveLibraries`
- `/VIID/ArchivesQuerySync`
- `/VIID/Archives`
- `/VIID/ArchiveSubjectQuerySync`
- `/VIID/ArchiveSubjects`

### 3.2 字段命名与包装

- 字段命名保持协议风格（驼峰，大小写敏感）。
- 查询请求包装使用 `ArchiveQueryObject` / `ArchiveSubjectQueryObject`。
- 查询结果包装使用 `ArchiveQueryResultObject` / `ArchiveSubjectQueryResultObject`。
- 写操作状态返回使用 `ResponseStatusListSchema`。

### 3.3 时间格式

- 协议时间字段统一格式：`YYYYMMDDHHMMSS`。
- 典型字段：`BeginTime`、`EndTime`、`CreateTime`、`UpdateTime`。

### 3.4 枚举编码

- `IntEnum` 字段使用整数语义值。
- `StrEnum` 字段使用字符串语义值。

## 4. 接口契约

### 4.1 ArchiveLibrary

| 方法 | 路径 | 请求模型 | 响应模型 | 说明 |
| --- | --- | --- | --- | --- |
| GET | `/VIID/ArchiveLibraryQuerySync` | `TBD（代码签名未显式声明）` | `TBD（代码签名未显式声明）` | A.5 档案库查询 |
| POST | `/VIID/ArchiveLibraries` | `TBD（代码签名未显式声明）` | `ResponseStatusListSchema` | A.6 档案库增加 |
| PUT | `/VIID/ArchiveLibraries` | `TBD（代码签名未显式声明）` | `ResponseStatusListSchema` | A.7 档案库更新 |
| DELETE | `/VIID/ArchiveLibraries` | `id_list: str` | `ResponseStatusListSchema` | A.8 档案库删除 |

### 4.2 Archives

| 方法 | 路径 | 请求模型 | 响应模型 | 说明 |
| --- | --- | --- | --- | --- |
| GET | `/VIID/ArchivesQuerySync` | `TBD（代码签名未显式声明）` | `TBD（代码签名未显式声明）` | A.9 人员档案查询 |
| POST | `/VIID/Archives` | `TBD（代码签名未显式声明）` | `ResponseStatusListSchema` | A.10 人员档案增加 |
| PUT | `/VIID/Archives` | `TBD（代码签名未显式声明）` | `ResponseStatusListSchema` | A.10 人员档案更新 |
| DELETE | `/VIID/Archives` | `TBD（代码签名未显式声明）` | `ResponseStatusListSchema` | A.10 人员档案删除 |

### 4.3 ArchiveSubject

| 方法 | 路径 | 请求模型 | 响应模型 | 说明 |
| --- | --- | --- | --- | --- |
| POST | `/VIID/ArchiveSubjectQuerySync` | `TBD（代码签名未显式声明）` | `TBD（代码签名未显式声明）` | A.13 人员档案明细查询 |
| POST | `/VIID/ArchiveSubjects` | `ArchiveSubjectSchema` | `ResponseStatusListSchema` | A.14 人员档案明细增加 |
| PUT | `/VIID/ArchiveSubjects` | `ArchiveSubjectSchema` | `ResponseStatusListSchema` | A.14 人员档案明细更新 |
| DELETE | `/VIID/ArchiveSubjects` | `archive_id` / `face_id_list` / `person_id_list` / `motor_vehicle_id_list` / `non_motor_vehicle_id_list` | `ResponseStatusListSchema` | A.14 人员档案明细删除 |

## 5. 对象契约（摘要）

### 5.1 档案库与档案对象

- `ArchiveLibrary`
  - `ArchiveLibraryID`
  - `Name`
  - `CreateTime`
  - `Memo`

- `Archive`
  - `ArchiveID`
  - `ArchiveLibraryID`
  - `IDType` / `IDNumber`
  - `Name`
  - `BirthTime`
  - `CreateTime` / `UpdateTime`
  - `ImageID`

### 5.2 档案明细对象

- `ArchiveSubject`
  - `ArchiveID`
  - `PersonIDList`
  - `FaceIDList`
  - `PersonObjectList`
  - `FaceObjectList`
  - `ImageID`

### 5.3 查询与结果对象

- `ArchiveQuery`
  - `QueryID`
  - `MaxNumRecordReturn` / `PageRecordNum` / `RecordStartNo`
  - `BeginTime` / `EndTime`
  - `GeoRectangle`
  - `DeviceSelected`
  - `Sort`
  - `Fields`

- `ArchiveQueryResult`
  - `QueryID`
  - `RecordStartNo`
  - `PageRecordNum`
  - `TotalNum`
  - `ArchiveListObject`

- `ArchiveSubjectQuery`
  - 继承 `ArchiveQuery`
  - `ArchiveIDList`
  - `ResultSubjectDetailDeclare`

- `ArchiveSubjectQueryResult`
  - 继承 `ArchiveQueryResult`
  - `ArchiveSubjectInfoList`

### 5.4 通用查询对象

- `PictureQueryCondition`
  - `SubImage`
  - `Threshold`
  - `SubjectID`

- `GeoRectangleType`
  - `LeftTopLongitude` / `LeftTopLatitude`
  - `RightBtmLongitude` / `RightBtmLatitude`

- `DeviceSelector`
  - `DeviceIDs`
  - `DevicePlaceCode`

- `FieldsType`
  - `ArchiveLibraryID`
  - `IDNumbers`
  - `Names`
  - `ArchiveIDList`
  - `OnlyRealNameArchive`
  - `PlaceCode`
  - `GenderCode`
  - `AgeUpLimit` / `AgeLowerLimit`
  - `PlateNos` / `PlateColor`
  - `VehicleClass` / `VehicleBrand` / `VehicleModel` / `VehicleColor` / `VehicleStyles`

## 6. 错误响应契约

- 写操作接口使用 `ResponseStatusListSchema` 返回状态信息。
- 业务错误场景应返回协议状态对象（含 `StatusCode`、`StatusString`）。
- 查询接口在代码签名未显式声明响应模型时，响应模型标注为 `TBD`。

## 7. 协议一致性检查清单

1. 路径与方法匹配上表定义。  
2. 请求/响应可被对应模型校验（或标注为 `TBD`）。  
3. 时间字段格式为 `YYYYMMDDHHMMSS`。  
4. 枚举字段取值符合模型定义。  
5. 写操作返回包含状态对象。  
6. 包装对象命名与大小写保持一致。

## 8. 协议待定项（TBD）

以下接口在当前代码签名中未显式声明完整请求/响应模型，按 `TBD` 处理：

- `GET /VIID/ArchiveLibraryQuerySync`（请求/响应）
- `GET /VIID/ArchivesQuerySync`（请求/响应）
- `POST /VIID/ArchiveSubjectQuerySync`（请求/响应）
- `POST /VIID/ArchiveLibraries`（请求）
- `PUT /VIID/ArchiveLibraries`（请求）
- `POST /VIID/Archives`（请求）
- `PUT /VIID/Archives`（请求）
- `DELETE /VIID/Archives`（请求）

## 9. 关联文档

- 架构总览：`.docs/ARCHITECTURE.md`
- 测试规范：`.docs/TESTING.md`
- 1400 协议契约：`.docs/PROTOCOL_1400.md`
