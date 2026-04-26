# Data Models

## 表模型

已建表实体：

- `APS`, `APE`
- `Person`, `Face`
- `Subscribe`, `SubscribeNotification`
- `ArchiveLibrary`, `Archive`
- `VehicleArchive`, `ArchiveTask`
- `ArchiveSubject`, `VehicleArchiveSubject`

对应迁移：

- `alembic/versions/a272a22d0455_init.py`
- `alembic/versions/c2a4d9f73c51_add_archive_task_table.py`
- `alembic/versions/ba1f5f1f8b9e_add_vehicle_archive_table.py`
- `alembic/versions/7f7fb248ab04_align_2350_official_models.py`

`ArchiveSubject`、`VehicleArchiveSubject` 仍保留 repository 启动阶段的 `create_all` 兼容兜底，但正式 schema 已纳入 Alembic 迁移。

## 协议/聚合模型

- 响应封装：`ResponseStatus`, `ResponseStatusList`, `ResponseStatusListSchema`
- 系统消息：`RegisterSchema`, `UnRegisterSchema`, `KeepaliveSchema`
- 聚档任务：`ArchiveTask`, `ArchiveTaskList`, `ArchiveTaskListSchema`
- 档案查询：`ArchiveQuery*`, `ArchiveSubjectQuery*`
- 档案查询与核验包装：`ArchiveQueryResult*`, `ArchiveConfidence*`

## 结构特征

- 多个实体使用 JSON 字段承载嵌套对象，例如 `SubImageList`、`FaceObjectList`、`PersonObjectList`。
- 时间字段通过 `models/common/enums.py` 中 `VIIDDateTime` 与 `core/utils.py` 中的 `parse_datetime` / `serialize_datetime` 做协议时间格式转换。
- `alembic/env.py` 使用 `sqlmodel.SQLModel.metadata` 作为迁移元数据来源。

## 唯一性约束

- 资源主标识字段使用唯一约束，例如 `PersonID`、`FaceID`、`ArchiveID`、`VehicleArchive.ArchiveID`、`SubscribeID`、`NotificationID`、`ArchiveLibraryID`、`TaskID`、`ApeID`、`ApsID`。
- `SourceID` 是 GA/T 1400 人员、人脸等对象中的来源标识，当前协议资料将其定义为必填来源引用字段，未要求数据库全局唯一；当前模型不增加 `unique=True`。
- `ImageID` 在当前实现中主要位于 `SubImageInfo` 等嵌套 JSON 对象内，GA/T 2350 正式模型已由 `SourceIDList` 和 `SubImageList` 替代旧迁移中的档案级 `ImageID` 列；当前不在关系表上新增独立唯一约束。
