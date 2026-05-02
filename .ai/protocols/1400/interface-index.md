# GA/T 1400 Interface Index

若本文与本地 `.protocol/` 原始协议冲突，以 `.protocol/` 为准。

## System

| 方法 | 路径 | 请求模型 | 响应模型 |
| --- | --- | --- | --- |
| POST | `/VIID/System/Register` | `RegisterSchema` | `ResponseStatusList` |
| POST | `/VIID/System/UnRegister` | `UnRegisterSchema` | `ResponseStatus` |
| POST | `/VIID/System/Keepalive` | `KeepaliveSchema` | `ResponseStatus` |
| GET | `/VIID/System/Time` | 无 | `SystemTime` |

## Collection

| 方法 | 路径 | 请求模型 | 响应模型 |
| --- | --- | --- | --- |
| GET | `/VIID/APSs` | 无 | `APSListSchema` |
| GET | `/VIID/APEs` | 无 | `APEListSchema` |
| PUT | `/VIID/APEs` | `APEListSchema` | `ResponseStatusListSchema` |

## Person

| 方法 | 路径 | 请求模型 | 响应模型 |
| --- | --- | --- | --- |
| GET | `/VIID/Persons` | 无 | `PersonListObjectSchema` |
| POST/PUT | `/VIID/Persons` | `PersonListObjectSchema` | `ResponseStatusListSchema` |
| DELETE | `/VIID/Persons` | `IDList` | `ResponseStatusListSchema` |
| GET/PUT/DELETE | `/VIID/Persons/{person_id}` | 路径参数或 `Person` | `Person` / `ResponseStatus` |

## Face

| 方法 | 路径 | 请求模型 | 响应模型 |
| --- | --- | --- | --- |
| GET | `/VIID/Faces` | `Face` 属性键/值对；当前已实现 `RecordStartNo`、`PageRecordNum` 分页参数 | `FaceListObjectSchema` |
| POST/PUT | `/VIID/Faces` | `FaceListObjectSchema` | `ResponseStatusListSchema` |
| DELETE | `/VIID/Faces` | `IDList` | `ResponseStatusListSchema` |
| GET/PUT/DELETE | `/VIID/Faces/{face_id}` | 路径参数或 `Face` | `Face` / `ResponseStatus` |

## Subscribe

| 方法 | 路径 | 请求模型 | 响应模型 |
| --- | --- | --- | --- |
| GET/POST/PUT/DELETE | `/VIID/Subscribes` | `SubscribeListSchema` 或 `IDList` | `SubscribeListSchema` / `ResponseStatusListSchema` |
| PUT | `/VIID/Subscribes/{subscribe_id}` | `Subscribe` | `ResponseStatus` |

## SubscribeNotification

| 方法 | 路径 | 请求模型 | 响应模型 |
| --- | --- | --- | --- |
| POST | `/VIID/SubscribeNotifications` | `SubscribeNotificationListSchema` | `ResponseStatusListSchema` |
| GET | `/VIID/SubscribeNotifications` | 查询字符串 | `SubscribeNotificationListSchema` |
| DELETE | `/VIID/SubscribeNotifications` | `IDList` | `ResponseStatusListSchema` |
