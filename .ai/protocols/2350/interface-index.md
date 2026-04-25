# GA/T 2350.5 Interface Index

若本文与本地 `.protocol/` 原始协议冲突，以 `.protocol/` 为准。

| 条款 | URL | 当前状态 |
| --- | --- | --- |
| A.5 | `/VIID/ArchiveLibraries` | 已基本对齐 |
| A.6 | `/VIAS/Tasks` | 已实现 GET/POST/PUT/DELETE 主链路，Task 字段仍需结合 GA/T 1399-2017 继续核对 |
| A.7 | `/VIID/Subscribes` | 复用 1400 路由，2350 扩展语义仍需核对 |
| A.8 | `/VIID/SubscribeNotifications` | 复用 1400 路由，已补齐部分 2350 扩展列表 |
| A.9 | `/VIID/ArchivesQuerySync` | 使用 `POST /VIID/ArchivesQuerySync` + `ArchiveQuery` |
| A.10 | `/VIID/Archives` | 批量增改删已实现，DELETE 使用 `IDList` |
| A.11 | `/VIID/VehicleArchivesQuerySync` | 使用 `POST` + `ArchiveQuery` -> `ArchiveQueryResult` |
| A.12 | `/VIID/VehicleArchives` | 批量增改删主链路已实现 |
| A.13 | `/VIID/ArchiveSubjectQuerySync` | 使用 `POST` + `ArchiveSubjectQuery` |
| A.14 | `/VIID/ArchiveSubjects` | 批量增改删已实现，DELETE 支持正式版五类删除键 |
| A.15 | `/VIID/VehicleArchiveSubjectQuerySync` | 使用 `POST` + `ArchiveSubjectQuery` |
| A.16 | `/VIID/VehicleArchiveSubjects` | 批量增改删已实现，DELETE 支持正式版五类删除键 |
| A.17 | `/VIID/ArchiveConfidence` | 使用 `ArchiveList` 请求/响应 |
| A.18 | `/VIID/VehicleArchiveConfidence` | 使用 `VehicleArchiveList` 请求/响应 |
