# Domain Status

| 领域 | API 文件 | Service | Task/Repo | 状态 |
| --- | --- | --- | --- | --- |
| 系统注册/保活/注销/系统时间 | `api/system/*.py` | `APSService` + `SystemTimeService` | `update_aps_task` | 已实现 |
| 采集系统 APS | `api/collection/aps.py` | `APSService` | `repo/collection/aps.py` + `tasks/collection/aps.py` | 已实现 |
| 采集设备 APE | `api/collection/ape.py` | `APEService` | `repo/collection/ape.py` + `tasks/collection/ape.py` | 已实现 |
| 人脸 Face | `api/face/face.py` | `FaceService` | `repo/face/face.py` + `tasks/face/face.py` | 已实现 |
| 人员 Person | `api/person/person.py` | `PersonService` | `repo/person/person.py` + `tasks/person/person.py` | 已实现 |
| 订阅 Subscribe | `api/subscribe/subscribe.py` | `SubscribeService` | `repo/subscribe/subscribe.py` + `tasks/subscribe/subscribe.py` | 已实现 |
| 订阅通知 | `api/subscribe/subscribe_notification.py` | `SubscribeNotificationService` | `repo/subscribe/subscribe_notification.py` + `tasks/subscribe/subscribe_notification.py` | 已实现 |
| 档案库 ArchiveLibrary | `api/library/archive_library.py` | `ArchiveLibraryService` | `repo/library/archive_library.py` + `tasks/library/archive_library.py` | 已实现 |
| 聚档任务 ArchiveTask | `api/task/archive_task.py` | `ArchiveTaskService` | `repo/task/archive_task.py` + `tasks/task/archive_task.py` | 已实现主链路，Task 字段仍需继续核对 |
| 档案 Archive | `api/archive/archives.py` | `ArchiveService` | `repo/archive/archives.py` + `tasks/archive/archives.py` | 部分实现 |
| 车辆档案 VehicleArchive | `api/vehicle/vehicle_archive.py` | `VehicleArchiveService` | `repo/vehicle/vehicle_archive.py` + `tasks/vehicle/vehicle_archive.py` | 部分实现 |
| 档案明细 ArchiveSubject | `api/archive/archive_subject.py` | `ArchiveSubjectService` | `repo/archive/archive_subject.py` + `tasks/archive/archive_subject.py` | 部分实现 |
| 车辆档案明细 VehicleArchiveSubject | `api/vehicle/vehicle_archive_subject.py` | `VehicleArchiveSubjectService` | `repo/vehicle/vehicle_archive_subject.py` + `tasks/vehicle/vehicle_archive_subject.py` | 部分实现 |
| 档案核验 Confidence | `api/verify/*.py` | `ArchiveConfidenceService` / `VehicleArchiveConfidenceService` | `repo/verify/*.py` + `tasks/verify/*.py` | 已基本对齐 |

当前待增强点集中在：

- GA/T 2350.5-2025 正式版剩余对齐。
- RabbitMQ 真实 worker 场景端到端回归。
- 附录扩展字段的精细化检索约束。
