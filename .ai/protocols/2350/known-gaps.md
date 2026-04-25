# GA/T 2350.5 Known Gaps

若本文与本地 `.protocol/` 原始协议冲突，以 `.protocol/` 为准。

当前已确认差异：

- A.6 `/VIAS/Tasks` 当前明确不纳入本服务实现范围。
- A.9/A.11/A.13/A.15 当前查询行为仍未覆盖正式版全部检索语义。
- 当前查询主要支持部分 `Fields` 和 `PictureQueryCondition.SubjectID` 路径。
- `ArchiveSubject` / `VehicleArchiveSubject` 的机动车、非机动车对象列表仍使用宽松 JSON 容器。
- `SubscribeNotification` 为兼容 1400 仍保留 `FaceObjectList` / `PersonObjectList`，属于 1400 + 2350 扩展并存的共享模型。

关键对齐点：

- A.17 成功响应应为 `ArchiveList`。
- A.18 成功响应应为 `VehicleArchiveList`。
- 错误响应仍使用协议状态对象。
