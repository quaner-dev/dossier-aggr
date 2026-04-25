# Test Environment

## 依赖与启动

```bash
pip install -r requirements.txt
alembic upgrade head
uvicorn main:app --host 0.0.0.0 --port 8000
taskiq worker core.brokers:broker
```

说明：

- 写接口通过 `dispatch_and_wait` 触发 `.kiq(...)` 并等待任务结果；真实 broker 场景需启动 worker。
- 默认 `ENV=dev` 使用 `InMemoryBroker`；非 `dev` 需要 RabbitMQ 配置。

## 必要环境变量

- `ENV`
- `DATABASE_URL`
- 非 dev：`RABBITMQ_USERNAME`
- 非 dev：`RABBITMQ_PASSWORD`
- 非 dev：`RABBITMQ_IP`
- 非 dev：`RABBITMQ_PORT`

## 测试数据策略

- 使用独立测试库，例如临时 sqlite 文件，避免污染开发数据。
- 每个测试用例执行前后清理表数据，保证可重复执行。
