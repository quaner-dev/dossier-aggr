# GA/T 1400 Implementation Map

若本文与本地 `.protocol/` 原始协议冲突，以 `.protocol/` 为准。

| 领域 | 路由 | Service | Repository | Task |
| --- | --- | --- | --- | --- |
| System | `api/system/*.py` | `APSService`, `SystemTimeService` | `repo/collection/aps.py` | `tasks/collection/aps.py` |
| APS | `api/collection/aps.py` | `APSService` | `repo/collection/aps.py` | `tasks/collection/aps.py` |
| APE | `api/collection/ape.py` | `APEService` | `repo/collection/ape.py` | `tasks/collection/ape.py` |
| Person | `api/person/person.py` | `PersonService` | `repo/person/person.py` | `tasks/person/person.py` |
| Face | `api/face/face.py` | `FaceService` | `repo/face/face.py` | `tasks/face/face.py` |
| Subscribe | `api/subscribe/subscribe.py` | `SubscribeService` | `repo/subscribe/subscribe.py` | `tasks/subscribe/subscribe.py` |
| SubscribeNotification | `api/subscribe/subscribe_notification.py` | `SubscribeNotificationService` | `repo/subscribe/subscribe_notification.py` | `tasks/subscribe/subscribe_notification.py` |
