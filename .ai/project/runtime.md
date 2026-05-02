# Runtime

入口：`main.py`

## FastAPI 与 Taskiq

- `taskiq_fastapi.init(brokers.broker, "main:app")` 绑定 FastAPI 与 Taskiq。
- `app = FastAPI(lifespan=brokers.lifespan)` 在 lifespan 中管理 broker startup/shutdown。
- `app.include_router(api.router)` 聚合全量路由。

## Broker

Broker 选择位于 `core/brokers.py`：

- `ENV=dev` 使用 `InMemoryBroker`。
- 其他环境使用 `AioPikaBroker`，依赖 RabbitMQ 配置。
- 非 `dev` 环境必须设置 `TASKIQ_RESULT_BACKEND_URL`，当前使用 Redis
  result backend 保存跨进程任务返回值，支撑 `dispatch_and_wait` 等待 worker 执行结果。

## 数据库

数据库配置位于 `core/settings.py`：

- `DATABASE_URL` 默认值为 `sqlite+aiosqlite:///db.sqlite3`。
- 应用运行时使用异步 SQLAlchemy URL。
- 非 SQLite 数据库可通过 `DB_POOL_SIZE`、`DB_MAX_OVERFLOW`、
  `DB_POOL_TIMEOUT_SECONDS`、`DB_POOL_RECYCLE_SECONDS`、`DB_POOL_PRE_PING`
  配置 SQLAlchemy 连接池；SQLite 会忽略这些池参数。
- 迁移使用 `Alembic`，并通过 `core.database_urls.make_sync_database_url` 将 `DATABASE_URL` 转换为同步驱动 URL。

## 异常处理

异常处理注册在 `api/error_handlers.py`：

- `DataNotFoundError` -> HTTP 404
- `DataAlreadyExistsError` -> HTTP 409
- `InvalidParameterError` -> HTTP 400
- `TaskExecutionError` -> HTTP 503
- `RequestValidationError`、`HTTPException`、`Exception`

错误响应统一包装为 VIID 风格状态对象。
