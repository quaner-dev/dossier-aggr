# ARCHITECTURE

更新时间：2026-02-14  
范围：仅基于当前仓库代码（不引用 `llm/` 目录）

## 1. 系统定位

`dossier-aggr` 是一个 VIID 协议服务，当前包含两类能力：

- GA/T 1400 相关：系统注册/保活/注销、采集系统与设备、人员、人脸、订阅与通知。
- GA/T 2350.5（聚档）相关：档案库、档案、档案明细接口骨架与模型，部分尚未落地实现。

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
              -> tasks/*       # 查询与写任务定义
                  -> models/*  # SQLModel 实体 + 协议模型
                      -> database.py (engine/session)
```

分层边界现状：

- `api/` 不直接操作数据库，主要依赖 `services`。
- `services/` 主要调用 `tasks`，做轻量业务编排。
- `tasks/` 承担绝大多数数据访问逻辑（`AsyncSession(engine)`）。

## 4. 启动与生命周期

入口：`main.py`

- `taskiq_fastapi.init(brokers.broker, "main:app")` 绑定 FastAPI 与 Taskiq。
- `app = FastAPI(lifespan=brokers.lifespan)`，在 lifespan 中管理 broker startup/shutdown。
- `app.include_router(api.router)` 聚合全量路由。
- 注册异常处理器：
  - `DataNotFoundError`
  - `DataAlreadyExistsError`

路由聚合：`api/__init__.py`

- `system`、`health`、`collection`、`face`、`person`、`subscribe`、`library`、`archive`

## 5. 请求处理模式

### 5.1 同步查询链路

典型路径：`API -> Service -> Task(直接 await) -> DB`

示例：

- `GET /VIID/APEs` -> `APEService.list_apes()` -> `list_apes_task()`
- `GET /VIID/Persons` -> `PersonService.list_persons()` -> `list_persons_task()`
- `GET /VIID/Faces` -> `FaceService.list_faces()` -> `list_faces_task()`

### 5.2 异步写入链路

典型路径：`API -> Service -> task_fn.kiq(...) -> Broker -> Worker 执行 -> DB`

示例：

- `PUT /VIID/APEs` -> `update_apes_task.kiq(...)`
- `POST /VIID/Faces` -> `create_faces_task.kiq(...)`
- `POST /VIID/Persons` -> `create_persons_task.kiq(...)`
- `POST /VIID/Subscribes` -> `create_subscribes_task.kiq(...)`

### 5.3 特例

- `System Register/UnRegister/Keepalive` 使用 `APSService.update_aps()`，内部直接 `await update_aps_task(...)`（不是 `.kiq`）。
- 健康探针 `/ready` 在 `api/health/probes.py` 中直接执行 `SELECT 1` 检查数据库连通性。

## 6. 领域模块状态矩阵

| 领域 | API 文件 | Service | Task | 状态 |
| --- | --- | --- | --- | --- |
| 系统注册/保活/注销 | `api/system/*.py` | `APSService` | `update_aps_task` | 已实现 |
| 采集系统 APS | `api/collection/aps.py` | `APSService` | `list_apss_task` | 已实现 |
| 采集设备 APE | `api/collection/ape.py` | `APEService` | `list_apes_task` + `update_apes_task` | 已实现 |
| 人脸 Face | `api/face/face.py` | `FaceService` | `tasks/face/face.py` | 已实现 |
| 人员 Person | `api/person/person.py` | `PersonService` | `tasks/person/person.py` | 已实现 |
| 订阅 Subscribe | `api/subscribe/subscrbe.py` | `SubscribeService` | `tasks/subscribe/subscribe.py` | 已实现 |
| 订阅通知 | `api/subscribe/subscribe_notification.py` | `SubscribeNotificationService` | `create_subscribe_notifications_task` | 已实现 |
| 档案库 ArchiveLibrary | `api/library/archive_library.py` | `ArchiveLibraryService` | 无 | 接口占位 |
| 档案 Archive | `api/archive/archives.py` | `ArchiveService`（部分） | 无 | 接口占位 |
| 档案明细 ArchiveSubject | `api/archive/archive_subject.py` | `ArchiveSubjectService`（占位） | 无 | 接口占位 |

## 7. 数据模型与持久化

### 7.1 已建表实体（SQLModel table=True）

- `APS`, `APE`
- `Person`, `Face`
- `Subscribe`, `SubscribeNotification`
- `ArchiveLibrary`, `Archive`

对应迁移：`alembic/versions/a272a22d0455_init.py`

### 7.2 协议/聚合模型（非表）

- 响应封装：`ResponseStatus`, `ResponseStatusList`, `ResponseStatusListSchema`
- 系统消息：`RegisterSchema`, `UnRegisterSchema`, `KeepaliveSchema`
- 档案查询：`ArchiveQuery*`, `ArchiveSubjectQuery*` 等
- 档案明细对象 `ArchiveSubject`（当前为协议结构，不是数据库表）

### 7.3 结构特征

- 多个实体使用 JSON 字段承载嵌套对象（如 `SubImageList`, `FaceObjectList`, `PersonObjectList`）。
- 时间字段通过 `models/common/enums.py` 中 `VIIDDateTime` + `utils.parse_datetime/serialize_datetime` 做协议时间格式转换。
- `alembic/env.py` 使用 `sqlmodel.SQLModel.metadata` 作为迁移元数据来源。

## 8. 异常与响应约定

- 自定义异常：`exceptions.py`
- `DataNotFoundError`（HTTP 200）
- `DataAlreadyExistsError`（HTTP 200）
- `InvalidParameterError`（HTTP 400）
- `main.py` 将部分异常统一包装为 `ResponseStatusList` 返回。
- API 普遍返回 VIID 风格对象（`*ListSchema` 或 `ResponseStatus*`）。

## 9. 部署与运维

- 镜像：`Dockerfile`（`python:3.12-alpine`）。
- Helm Chart：`dossier-aggr/`。
- 默认容器启动命令（`values.yaml`）：`uvicorn main:app --host 0.0.0.0 --port 8000`。
- 探针路径：
  - `startup`: `/startup`
  - `liveness`: `/live`
  - `readiness`: `/ready`

## 10. 测试现状

- 当前仓库测试集中在 `tests/test_api_ape.py`（APE API 的函数级测试）。
- 尚缺：
  - 多模块 API 回归测试
  - service/task 分层测试
  - Broker/worker 端到端写入验证

## 11. 当前架构结论

- 主链路（collection/person/face/subscribe）已具备 API -> service -> task -> DB 的可运行骨架。
- 写入路径大量采用 `.kiq` 异步投递，需依赖 worker 进程保证最终落库。
- 聚档（Archive*）模块当前以模型与接口骨架为主，尚未形成完整业务闭环。
