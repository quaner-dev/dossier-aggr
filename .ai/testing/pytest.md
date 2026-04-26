# Pytest Guidance

建议目录：

- `tests/api/`：接口行为测试。
- `tests/protocol/`：协议结构与格式测试。
- `tests/e2e/`：含 worker 的最终一致性测试。

每个接口至少覆盖：

- happy path
- 参数缺失/格式错误
- 资源不存在
- 重复写入

协议测试建议使用 `model_validate` 对响应进行结构校验，避免只做字符串断言。

相关参考：

- `tests/services/test_subscribe_layering.py`
- `tests/services/test_person_face_layering.py`
- `tests/services/test_collection_archive_layering.py`
- `tests/services/test_subject_verify_layering.py`
- `tests/test_api_metrics.py`
- `tests/helm/test_chart.py`
- `tests/protocol/test_protocol_matrix_guard.py`

2350 查询回归建议覆盖 `PictureQueryCondition.SubjectID`，并验证其在 `Archive.SourceIDList`、`VehicleArchive.SourceIDList` 以及档案明细五类 ID 列表上的命中行为。

Helm Chart 变更至少运行 `pytest -q tests/helm/test_chart.py`，确认默认生产 values、开发覆盖 values、API/worker selector 隔离和迁移 Job 渲染符合预期。
