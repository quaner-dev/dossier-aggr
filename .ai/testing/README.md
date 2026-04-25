# Testing Docs

本目录保存测试说明和验证清单。

## 阅读顺序

1. `environment.md`：依赖、启动方式、环境变量和测试数据策略。
2. `layers.md`：测试分层。
3. `api-matrix.md`：接口测试矩阵。
4. `protocol-checklist.md`：协议符合性检查。
5. `baseline-cases.md`：建议最小基线用例。
6. `pytest.md`：自动化落地建议。
7. `report-template.md`：测试报告模板。

每次修改后至少尝试运行：

```bash
pytest -q
```
