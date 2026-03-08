# ARCHITECTURE

更新时间：2026-03-05  
范围：仅基于当前仓库代码（不引用 `llm/` 目录）

## 1. 系统定位

`dossier-aggr` 是一个 VIID 协议服务，当前包含两类能力：

- GA/T 1400 相关：系统注册/保活/注销、采集系统与设备、人员、人脸、订阅与通知。
- GA/T 2350.5（聚档）相关：档案库、档案、档案明细、档案核验等主链路能力。

## 2. 技术栈与运行时

- API 框架：`FastAPI`
- 数据层：`SQLModel` + `SQLAlchemy AsyncSession`
- 任务队列：`Taskiq`
- Broker 选择（`brokers.py`）：
  - `ENV=dev` -> `InMemoryBroker`
  - 其他环境 -> `AioPikaBroker`（RabbitMQ）
- 数据库配置（`settings.py`）：`DATABASE_URL`，默认 `sqlite+aiosqlite:///db.sqlite3`
- 迁移：`Alembic`

## 3. 分层结构

```text
Client
  -> main.py
      -> api/*                 # HTTP 路由、入参/出参组装
          -> services/*        # 业务编排
              -> repositories/*# 数据访问（SQLModel/SQL）
              -> tasks/*       # 异步任务入口（Taskiq）
                  -> repositories/* -> models/* -> database.py
```

分层边界现状：

- `api/` 不直接操作数据库，主要依赖 `services`。
- `services/` 承担校验与业务编排；同步读优先调用 `repositories`，异步写通过 `tasks` 投递。
- `repositories/` 承担数据访问逻辑（`AsyncSession(engine)`、`select/delete`、持久化异常语义）。
- `tasks/` 作为异步入口层，任务函数委托 `repositories` 执行实际数据访问。
- `face` 查询链路中，`api/face/face.py` 仅判断是否传入 `FaceID`；`FaceService` 负责单查/列表读取编排；`repositories/face/face.py` 负责按 `FaceID` 单查与默认 `TOP100` 列表读取。

## 4. 启动与生命周期

入口：`main.py`

- `taskiq_fastapi.init(brokers.broker, "main:app")` 绑定 FastAPI 与 Taskiq。
- `app = FastAPI(lifespan=brokers.lifespan)`，在 lifespan 中管理 broker startup/shutdown。
- `app.include_router(api.router)` 聚合全量路由。
- 注册异常处理器：`register_exception_handlers(app)`（`api/error_handlers.py`）
  - 业务异常：`DataNotFoundError`、`DataAlreadyExistsError`、`InvalidParameterError`、`TaskExecutionError`
  - 框架异常：`RequestValidationError`、`HTTPException`、`Exception`

路由聚合：`api/__init__.py`

- `system`、`health`、`collection`、`face`、`person`、`subscribe`、`library`、`archive`

## 5. 请求处理模式

### 5.1 同步查询链路

典型路径：`API -> Service -> Repository -> DB`

示例：

- `GET /VIID/System/Time` -> `SystemTimeService.get_system_time()`
- `GET /VIID/Subscribes/{subscribe_id}` -> `SubscribeService.get_subscribe()` -> `get_subscribe_repo()`
- `GET /VIID/SubscribeNotifications/{notification_id}` -> `SubscribeNotificationService.get_subscribe_notification()` -> `get_subscribe_notification_repo()`

### 5.2 异步写入链路

典型路径：`API -> Service(dispatch_and_wait) -> task_fn.kiq(...) -> Broker -> Worker -> Repository -> DB`

示例：

- `PUT /VIID/APEs` -> `update_apes_task.kiq(...)`
- `POST /VIID/Faces` -> `create_faces_task.kiq(...)`
- `POST /VIID/Persons` -> `create_persons_task.kiq(...)`
- `POST /VIID/Subscribes` -> `create_subscribes_task.kiq(...)`

说明：

- `services/task_dispatch.py` 统一执行 `.kiq(...)` 并等待任务结果（超时抛出 `TaskExecutionError`）。
- 因此“写请求返回成功”语义与任务实际执行结果绑定，而不是仅完成入队。

### 5.3 特例

- `System Register/UnRegister/Keepalive` 使用 `APSService.update_aps()`，内部与其他写操作一致，通过 `update_aps_task.kiq(...)` 投递异步写任务。
- 健康探针 `/ready` 在 `api/health/probes.py` 中直接执行 `SELECT 1` 检查数据库连通性。

## 6. 监控与可观测性

- 指标协议：Prometheus（`/metrics`）。
- 指标分层：
  - HTTP：请求总量、请求时延、请求/响应体大小、进行中请求数
  - ORM：SQL 次数、SQL 时延、影响行数
  - Layer：`service/task/repository` 执行时长
  - Task enqueue：`.kiq` 入队次数与入队耗时
- Grafana 通过 Prometheus 抓取以上指标后可直接配置请求频率、响应时间、ORM 与分层耗时看板。

## 7. 领域模块状态矩阵

| 领域 | API 文件 | Service | Task | 状态 |
| --- | --- | --- | --- | --- |
| 系统注册/保活/注销/系统时间 | `api/system/*.py` | `APSService` + `SystemTimeService` | `update_aps_task` | 已实现 |
| 采集系统 APS | `api/collection/aps.py` | `APSService` | `repositories/collection/aps.py` + `tasks/collection/aps.py` | 已实现（读走 repository，写走 task） |
| 采集设备 APE | `api/collection/ape.py` | `APEService` | `repositories/collection/ape.py` + `tasks/collection/ape.py` | 已实现（读走 repository，写走 task） |
| 人脸 Face | `api/face/face.py` | `FaceService` | `repositories/face/face.py` + `tasks/face/face.py` | 已实现（读走 repository，写走 task；`GET /VIID/Faces` 支持 `FaceID` 单查与默认 `TOP100` 列表） |
| 人员 Person | `api/person/person.py` | `PersonService` | `repositories/person/person.py` + `tasks/person/person.py` | 已实现（读走 repository，写走 task） |
| 订阅 Subscribe | `api/subscribe/subscrbe.py` | `SubscribeService` | `repositories/subscribe/subscribe.py` + `tasks/subscribe/subscribe.py` | 已实现（读走 repository，写走 task） |
| 订阅通知 | `api/subscribe/subscribe_notification.py` | `SubscribeNotificationService` | `repositories/subscribe/subscribe_notification.py` + `tasks/subscribe/subscribe_notification.py` | 已实现（读走 repository，写走 task） |
| 档案库 ArchiveLibrary | `api/library/archive_library.py` | `ArchiveLibraryService` | `repositories/library/archive_library.py` + `tasks/library/archive_library.py` | 已实现（A.5 主链路；读走 repository，写走 task） |
| 聚档任务 ArchiveTask | `api/task/archive_task.py` | `ArchiveTaskService` | `repositories/task/archive_task.py` + `tasks/task/archive_task.py` | 已实现（A.6 主链路；读走 repository，写走 task） |
| 档案 Archive | `api/archive/archives.py` | `ArchiveService` | `repositories/archive/archives.py` + `tasks/archive/archives.py` | 已实现（A.9/A.10 主链路；读走 repository，写走 task） |
| 车辆档案 VehicleArchive | `api/vehicle/vehicle_archive.py` | `VehicleArchiveService` | `repositories/vehicle/vehicle_archive.py` + `tasks/vehicle/vehicle_archive.py` | 已实现（A.11/A.12 主链路；读走 repository，写走 task） |
| 档案明细 ArchiveSubject | `api/archive/archive_subject.py` | `ArchiveSubjectService` | `repositories/archive/archive_subject.py` + `tasks/archive/archive_subject.py` | 已实现（A.13/A.14 主链路；读走 repository，写走 task） |
| 车辆档案明细 VehicleArchiveSubject | `api/vehicle/vehicle_archive_subject.py` | `VehicleArchiveSubjectService` | `repositories/vehicle/vehicle_archive_subject.py` + `tasks/vehicle/vehicle_archive_subject.py` | 已实现（A.15/A.16 主链路；读走 repository，写走 task） |
| 档案核验 Confidence | `api/verify/*.py` | `ArchiveConfidenceService` / `VehicleArchiveConfidenceService` | `repositories/verify/*.py` + `tasks/verify/*.py` | 已实现（A.17/A.18 主链路；service 同步核验走 repository） |

## 8. 数据模型与持久化

### 8.1 已建表实体（SQLModel table=True）

- `APS`, `APE`
- `Person`, `Face`
- `Subscribe`, `SubscribeNotification`
- `ArchiveLibrary`, `Archive`
- `VehicleArchive`, `ArchiveTask`
- `ArchiveSubject`, `VehicleArchiveSubject`

对应迁移：

- `alembic/versions/a272a22d0455_init.py`
- `alembic/versions/c2a4d9f73c51_add_archive_task_table.py`
- `alembic/versions/ba1f5f1f8b9e_add_vehicle_archive_table.py`
- `ArchiveSubject`、`VehicleArchiveSubject` 当前由 repository 启动阶段懒创建（`SQLModel.metadata.create_all`）

### 8.2 协议/聚合模型（非表）

- 响应封装：`ResponseStatus`, `ResponseStatusList`, `ResponseStatusListSchema`
- 系统消息：`RegisterSchema`, `UnRegisterSchema`, `KeepaliveSchema`
- 档案查询：`ArchiveQuery*`, `ArchiveSubjectQuery*` 等
- 档案查询与核验相关包装对象（`ArchiveQueryResult*`、`ArchiveConfidence*` 等）

### 8.3 结构特征

- 多个实体使用 JSON 字段承载嵌套对象（如 `SubImageList`, `FaceObjectList`, `PersonObjectList`）。
- 时间字段通过 `models/common/enums.py` 中 `VIIDDateTime` + `utils.parse_datetime/serialize_datetime` 做协议时间格式转换。
- `alembic/env.py` 使用 `sqlmodel.SQLModel.metadata` 作为迁移元数据来源。

## 9. 异常与响应约定

- 自定义异常：`exceptions.py`
- `DataNotFoundError`（HTTP 404）
- `DataAlreadyExistsError`（HTTP 409）
- `InvalidParameterError`（HTTP 400）
- `TaskExecutionError`（HTTP 503）
- `api/error_handlers.py` 统一将异常包装为 `ResponseStatusListSchema` 返回。
- `ResponseStatusList.ResponseStatusObject` 统一为 `list[ResponseStatus]`（不再使用“单对象或列表”混合结构）。
- API 普遍返回 VIID 风格对象（`*ListSchema` 或 `ResponseStatus*`）。

## 10. 部署与运维

- 镜像：`Dockerfile`（`python:3.12-alpine`）。
- Helm Chart：`dossier-aggr/`。
- 默认容器启动命令（`values.yaml`）：`uvicorn main:app --host 0.0.0.0 --port 8000`。
- 监控资源（Helm）：
  - Service 注解抓取：`prometheus.io/scrape/path/port`
  - 可选 `ServiceMonitor`（Prometheus Operator）
  - 可选 `PrometheusRule`（告警规则）
  - Grafana Dashboard ConfigMap（sidecar 自动发现）
- Worker 资源（Helm）：可选 `taskiq worker brokers:broker` Deployment。
- 探针路径：
  - `startup`: `/startup`
  - `liveness`: `/live`
  - `readiness`: `/ready`

## 11. 测试现状

- 当前仓库已包含以下自动化测试：
  - `tests/test_api_aps.py`
  - `tests/test_api_ape.py`
  - `tests/test_api_face.py`
  - `tests/test_api_person.py`
  - `tests/test_api_subscribe.py`
  - `tests/test_api_subscribe_notification.py`
  - `tests/test_api_system.py`
  - `tests/test_api_archive_library.py`
  - `tests/test_api_archive_task.py`
  - `tests/test_api_archives.py`
  - `tests/test_api_vehicle_archive.py`
  - `tests/test_api_archive_subject.py`
  - `tests/test_api_vehicle_archive_subject.py`
  - `tests/test_api_archive_confidence.py`
  - `tests/test_api_vehicle_archive_confidence.py`
  - `tests/tasks/test_delete_tasks.py`
  - `tests/protocol/test_protocol_matrix_guard.py`
  - `tests/protocol/test_1400_routes.py`
  - `tests/protocol/test_2350_routes.py`
  - `tests/protocol/test_2350_subscribe_contract.py`
  - `tests/services/test_collection_archive_layering.py`
  - `tests/services/test_person_face_layering.py`
  - `tests/services/test_subscribe_layering.py`
  - `tests/services/test_subject_verify_layering.py`
  - `tests/e2e/test_async_eventual_consistency.py`
  - `tests/test_api_metrics.py`
  - `tests/repositories/test_person_face_delete_repositories.py`
  - `tests/models/test_2350_models.py`
  - `tests/migrations/test_upgrade_head.py`
- 尚缺：
  - 基于 RabbitMQ 的真实 worker 端到端写入一致性验证

## 12. 当前架构结论

- 主链路（1400 + 2350 A.5-A.18）已具备 API -> service -> repository/task -> DB 的可运行实现。
- 写入路径通过 `dispatch_and_wait` 统一封装任务派发与结果等待，失败将返回协议化错误响应。
- 当前待增强点主要集中在 RabbitMQ 真实 worker 场景的端到端回归与附录扩展字段精细化约束。
