# GA/T 1400 Known Gaps

若本文与本地 `.protocol/` 原始协议冲突，以 `.protocol/` 为准。

当前记录：

- `Register` 使用 Digest 鉴权。
- `/metrics` 是运维监控端点，不属于 1400 协议接口集合。
- `/VIID/Faces` 批量查询已支持 `RecordStartNo`、`PageRecordNum` 分页参数；GA/T 1400.4 所述 `Face` 属性键/值对条件检索仍待补齐。
- 批量删除对外使用协议参数 `IDList`，部分接口仍兼容历史参数名。
- 协议时间字段统一使用 `YYYYMMDDHHMMSS`。
- `ResponseStatusListObject.ResponseStatusObject` 统一为数组结构。
