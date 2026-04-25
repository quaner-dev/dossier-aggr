# GA/T 2350.5 Implementation Map

若本文与本地 `.protocol/` 原始协议冲突，以 `.protocol/` 为准。

| 条款 | 路由 | Service | Repository | Task |
| --- | --- | --- | --- | --- |
| A.5 | `api/library/archive_library.py` | `ArchiveLibraryService` | `repo/library/archive_library.py` | `tasks/library/archive_library.py` |
| A.6 | `api/task/archive_task.py` | `ArchiveTaskService` | `repo/task/archive_task.py` | `tasks/task/archive_task.py` |
| A.7 | `api/subscribe/subscribe.py` | `SubscribeService` | `repo/subscribe/subscribe.py` | `tasks/subscribe/subscribe.py` |
| A.8 | `api/subscribe/subscribe_notification.py` | `SubscribeNotificationService` | `repo/subscribe/subscribe_notification.py` | `tasks/subscribe/subscribe_notification.py` |
| A.9/A.10 | `api/archive/archives.py` | `ArchiveService` | `repo/archive/archives.py` | `tasks/archive/archives.py` |
| A.11/A.12 | `api/vehicle/vehicle_archive.py` | `VehicleArchiveService` | `repo/vehicle/vehicle_archive.py` | `tasks/vehicle/vehicle_archive.py` |
| A.13/A.14 | `api/archive/archive_subject.py` | `ArchiveSubjectService` | `repo/archive/archive_subject.py` | `tasks/archive/archive_subject.py` |
| A.15/A.16 | `api/vehicle/vehicle_archive_subject.py` | `VehicleArchiveSubjectService` | `repo/vehicle/vehicle_archive_subject.py` | `tasks/vehicle/vehicle_archive_subject.py` |
| A.17/A.18 | `api/verify/*.py` | `ArchiveConfidenceService`, `VehicleArchiveConfidenceService` | `repo/verify/*.py` | `tasks/verify/*.py` |
