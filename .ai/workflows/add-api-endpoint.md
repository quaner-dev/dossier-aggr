# Add API Endpoint Workflow

1. 查 `.ai/protocols/`，确认接口路径、方法、请求体、响应体和协议来源。
2. 在 `api/` 增加路由函数，只做 HTTP 编排。
3. 判断请求/响应是否需要 Pydantic/SQLModel 模型：协议包装、请求体、响应体、嵌套结构和跨层复杂对象使用模型；少量简单路径/查询参数可直接使用显式参数。
4. 在 `services/` 增加业务逻辑。
5. 需要数据访问时在 `repo/` 增加函数。
6. 涉及异步写入时在 `tasks/` 增加 Taskiq 任务。
7. 复用 `models/` 中的现有协议对象，模型转换优先使用 `model_validate`。
8. 更新 `tests/` 中对应接口或协议测试。
9. 同步更新 `.ai/project/`、`.ai/protocols/`、`.ai/testing/` 中相关文档。
10. 按 `.ai/workflows/pre-commit-checklist.md` 完成验证。
