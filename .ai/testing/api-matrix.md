# API Test Matrix

| 域 | 方法 | 路径 | 主要校验点 | 状态 |
| --- | --- | --- | --- | --- |
| System Register | POST | `/VIID/System/Register` | Digest 鉴权、`RegisterSchema`、`ResponseStatusList` | 已实现 |
| System UnRegister | POST | `/VIID/System/UnRegister` | `UnRegisterSchema`、状态返回 | 已实现 |
| System Keepalive | POST | `/VIID/System/Keepalive` | `KeepaliveSchema`、状态返回 | 已实现 |
| System Time | GET | `/VIID/System/Time` | `SystemTime` 与时间格式 | 已实现 |
| APS | GET | `/VIID/APSs` | `APSListSchema` 包装 | 已实现 |
| APE | GET/PUT | `/VIID/APEs` | 查询包装、批量更新状态对齐 | 已实现 |
| Face | GET/POST/PUT/DELETE | `/VIID/Faces`、`/VIID/Faces/{face_id}` | 批量/单条接口、`IDList` 删除 | 已实现 |
| Person | GET/POST/PUT/DELETE | `/VIID/Persons`、`/VIID/Persons/{person_id}` | 批量/单条接口、`IDList` 删除 | 已实现 |
| Subscribe | GET/POST/PUT/DELETE | `/VIID/Subscribes`、`/VIID/Subscribes/{subscribe_id}` | 时间格式、唯一约束、状态回包 | 已实现 |
| SubscribeNotification | GET/POST/DELETE | `/VIID/SubscribeNotifications` | 通知对象批量写入、查询、删除 | 已实现 |
| ArchiveLibrary | GET/POST/PUT/DELETE | `/VIID/ArchiveLibraries` | A.5 主链路 | 已实现 |
| ArchiveTask | GET/POST/PUT/DELETE | `/VIAS/Tasks` | A.6 主链路、`TaskID` 删除、状态回包 | 已实现 |
| Archive | POST/PUT/DELETE | `/VIID/ArchivesQuerySync`、`/VIID/Archives` | A.9/A.10 主链路与查询语义 | 部分实现 |
| VehicleArchive | POST/PUT/DELETE | `/VIID/VehicleArchivesQuerySync`、`/VIID/VehicleArchives` | A.11/A.12 主链路与查询语义 | 部分实现 |
| ArchiveSubject | POST/PUT/DELETE | `/VIID/ArchiveSubjectQuerySync`、`/VIID/ArchiveSubjects` | A.13/A.14 主链路与删除键 | 部分实现 |
| VehicleArchiveSubject | POST/PUT/DELETE | `/VIID/VehicleArchiveSubjectQuerySync`、`/VIID/VehicleArchiveSubjects` | A.15/A.16 主链路与删除键 | 部分实现 |
| ArchiveConfidence | POST | `/VIID/ArchiveConfidence` | `ArchiveList` 请求/响应 | 已基本对齐 |
| VehicleArchiveConfidence | POST | `/VIID/VehicleArchiveConfidence` | `VehicleArchiveList` 请求/响应 | 已基本对齐 |
