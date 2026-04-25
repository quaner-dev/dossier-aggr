# Async Task Change Workflow

1. 确认接口是否属于写路径。
2. `api/` 只做请求/响应编排。
3. `services/` 使用 `dispatch_and_wait` 投递任务并等待结果。
4. `tasks/` 定义 Taskiq 任务函数。
5. `repo/` 执行实际数据访问。
6. 测试覆盖任务成功、任务失败/超时和写后查询。
7. 真实 broker 场景需要启动：

```bash
taskiq worker core.brokers:broker
```

8. 同步更新 `.ai/project/architecture.md` 和 `.ai/testing/layers.md` 中相关说明。
