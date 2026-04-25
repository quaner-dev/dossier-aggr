# Add API Endpoint Workflow

1. 查 `.ai/protocols/`，确认接口路径、方法、请求体、响应体和协议来源。
2. 在 `api/` 增加路由函数，只做 HTTP 编排。
3. 在 `services/` 增加业务逻辑。
4. 需要数据访问时在 `repo/` 增加函数。
5. 涉及异步写入时在 `tasks/` 增加 Taskiq 任务。
6. 复用 `models/` 中的现有协议对象，优先使用 `model_validate`。
7. 更新 `tests/` 中对应接口或协议测试。
8. 同步更新 `.ai/project/`、`.ai/protocols/`、`.ai/testing/` 中相关文档。
9. 至少尝试运行 `pytest -q`。
