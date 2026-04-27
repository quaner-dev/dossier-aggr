# dossier-aggr / VIID Service

<p align="center">
  <img src="docs/assets/dossier-aggr-overview.svg" alt="dossier-aggr VIID service overview" width="860">
</p>

<p align="center">
  <a href="https://www.python.org/downloads/release/python-3120/"><img alt="Python 3.12" src="https://img.shields.io/badge/python-3.12-3776AB?logo=python&logoColor=white"></a>
  <a href="https://fastapi.tiangolo.com/"><img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-API-009688?logo=fastapi&logoColor=white"></a>
  <a href="https://docs.pydantic.dev/"><img alt="Pydantic v2" src="https://img.shields.io/badge/Pydantic-v2-E92063?logo=pydantic&logoColor=white"></a>
  <a href="https://docs.pytest.org/"><img alt="pytest" src="https://img.shields.io/badge/tests-pytest-0A9EDC?logo=pytest&logoColor=white"></a>
  <a href="https://github.com/astral-sh/ruff"><img alt="ruff" src="https://img.shields.io/badge/lint-ruff-261230"></a>
  <a href="LICENSE"><img alt="License MIT" src="https://img.shields.io/badge/license-MIT-blue"></a>
</p>

`dossier-aggr` 是一个基于 FastAPI 的视频图像信息数据库（VIID）接口服务，面向公安视频图像协议接口实现、后端服务部署和系统集成联调。当前仓库交付 API 服务、Taskiq worker、数据库迁移和 Helm Chart，不包含独立前端应用。

## Highlights

- GA/T 1400-2017/2018 试行链路：系统注册、保活、注销、校时、采集系统、采集设备、人员、人脸、订阅与通知。
- GA/T 2350.5-2025 目标聚档链路：目标档案库、聚档任务、人员/车辆档案、档案明细和档案核验。
- 自动生成 OpenAPI，并通过 Swagger UI 与 ReDoc 提供交互式接口文档。
- 开发环境默认 SQLite + Taskiq InMemoryBroker；生产环境支持 PostgreSQL + RabbitMQ。
- 提供 Dockerfile、Helm Chart、Kubernetes 探针、Prometheus 指标和 Grafana Dashboard 模板。

## Compatibility

| Item | Current target |
| --- | --- |
| Python | 3.12 |
| API framework | FastAPI |
| Data model | SQLModel / Pydantic v2 |
| Migration | Alembic |
| Task queue | Taskiq |
| Dev database | SQLite |
| Production database | PostgreSQL |
| Production broker | RabbitMQ |

> 仓库当前没有 GitHub Actions 工作流，因此 README 不展示远端 CI 通过徽章。质量状态以本地执行 `ruff check .`、`pyright`、`pytest -q` 的结果为准。

## Protocol References

本仓库不分发标准原文。`.protocol/` 是本地原始协议资料目录，已被 `.gitignore` 忽略；协议判断先查 `.ai/protocols/` 的索引，必要时回到本地 `.protocol/` 文件核验。

| Protocol | Local source path | Public reference |
| --- | --- | --- |
| GA/T 1400.1-2017 通用技术要求 | `.protocol/1400/GA-T 1400.1-2017 公安视频图像信息应用系统 第1部分：通用技术要求.doc` | [国家数字标准馆](https://www.ndls.org.cn/standard/detail/f71a4415fcb5553126a987f4c79415c9) |
| GA/T 1400.2-2017 应用平台技术要求 | `.protocol/1400/GA-T 1400.2-2017 公安视频图像信息应用系统 第2部分：应用平台技术要求.doc` | [国家数字标准馆](https://www.ndls.org.cn/standard/detail/764238571834b42cfbeb6fc31a47204c) |
| GA/T 1400.3-2017 数据库技术要求 | `.protocol/1400/GA-T 1400.3-2017 公安视频图像信息应用系统 第3部分：数据库技术要求.doc` | [国家数字标准馆](https://www.ndls.org.cn/standard/detail/87eccff00012e165e1ae34d25c3747f6) |
| GA/T 1400.4-2017 接口协议要求 | `.protocol/1400/GA-T 1400.4-2017 公安视频图像信息应用系统 第4部分：接口协议要求.doc` | [国家数字标准馆](https://www.ndls.org.cn/standard/detail/4ac5697f21cc24610b6f66da80722c1e) |
| GA/T 1400 试行资料 | `.protocol/1400/20180521 视图库对接技术要-试行.pdf` | 本地资料 |
| GA/T 2350.5-2025 目标聚档服务 | `.protocol/2350/GA-T 2350.5-2025.pdf`、`.protocol/2350/GA-T 2350.5-2025.docx` | [国家数字标准馆关联条目](https://www.ndls.org.cn/standard/detail/e9bd6546ff969e6a6335c973e1271738)、[公安部标准公告转载](https://www.secrss.com/articles/84327) |

## Feature Matrix

状态说明：`√` 表示当前仓库已有对应 API/模型/服务主链路；`×` 表示当前仓库未实现。带备注的 `√` 代表接口已存在，但仍有字段、查询语义或正式版细节需要继续核对。

### GA/T 1400

| Protocol area | Typical path | Status | Notes |
| --- | --- | --- | --- |
| System register | `/VIID/System/Register` | √ | Digest 鉴权；返回协议状态对象 |
| System unregister | `/VIID/System/UnRegister` | √ | 返回协议状态对象 |
| System keepalive | `/VIID/System/Keepalive` | √ | 返回协议状态对象 |
| System time | `/VIID/System/Time` | √ | 返回系统时间对象 |
| VIID server resource | `/VIID/VIIDServers` | × | 未实现 |
| APE collection device | `/VIID/APEs` | √ | 已实现查询和修改主链路 |
| APS collection system | `/VIID/APSs` | √ | 已实现查询主链路 |
| Tollgate | `/VIID/Tollgates` | × | 未实现 |
| Lane | `/VIID/Lanes` | × | 未实现 |
| Video slice metadata/data | `/VIID/VideoSlices` | × | 未实现 |
| Image metadata/data | `/VIID/Images` | × | 未实现 |
| File metadata/data | `/VIID/Files` | × | 未实现 |
| Person | `/VIID/Persons` | √ | 支持批量和单项查询、增加、修改、删除 |
| Face | `/VIID/Faces` | √ | 支持批量和单项查询、增加、修改、删除 |
| Motor vehicle | `/VIID/MotorVehicles` | × | 未实现 |
| Non-motor vehicle | `/VIID/NonMotorVehicles` | × | 未实现 |
| Thing | `/VIID/Things` | × | 未实现 |
| Scene | `/VIID/Scenes` | × | 未实现 |
| Case | `/VIID/Cases` | × | 未实现 |
| Disposition | `/VIID/Dispositions` | × | 未实现 |
| Disposition notification | `/VIID/DispositionNotifications` | × | 未实现 |
| Subscribe | `/VIID/Subscribes` | √ | 支持订阅查询、创建、更新、删除、取消 |
| Subscribe notification | `/VIID/SubscribeNotifications` | √ | 支持通知上报、查询和删除 |
| Analysis rule | `/VIID/AnalysisRules` | × | 未实现 |
| Video label | `/VIID/VideoLabels` | × | 未实现 |
| VIAS system/capability | `/VIAS/System*`、`/VIAS/SystemCapability/*` | × | 未实现 |

### GA/T 2350.5

| Clause | Protocol area | Path | Status | Notes |
| --- | --- | --- | --- | --- |
| A.5 | Target archive library | `/VIID/ArchiveLibraries` | √ | 已基本对齐 |
| A.6 | Archive task | `/VIAS/Tasks` | √ | 主链路已实现；`Task` 字段仍需结合 GA/T 1399-2017 继续核对 |
| A.7 | Subscribe | `/VIID/Subscribes` | √ | 复用 1400 路由；2350 扩展语义仍需核对 |
| A.8 | Subscribe notification | `/VIID/SubscribeNotifications` | √ | 复用 1400 路由；已补齐部分 2350 扩展列表 |
| A.9 | Person archive query | `/VIID/ArchivesQuerySync` | √ | 查询行为尚未覆盖正式版全部检索语义 |
| A.10 | Person archive write | `/VIID/Archives` | √ | 批量增加、修改、删除主链路 |
| A.11 | Vehicle archive query | `/VIID/VehicleArchivesQuerySync` | √ | 查询行为尚未覆盖正式版全部检索语义 |
| A.12 | Vehicle archive write | `/VIID/VehicleArchives` | √ | 批量增加、修改、删除主链路 |
| A.13 | Person archive subject query | `/VIID/ArchiveSubjectQuerySync` | √ | 查询行为尚未覆盖正式版全部检索语义 |
| A.14 | Person archive subject write | `/VIID/ArchiveSubjects` | √ | 删除支持正式版五类删除键 |
| A.15 | Vehicle archive subject query | `/VIID/VehicleArchiveSubjectQuerySync` | √ | 查询行为尚未覆盖正式版全部检索语义 |
| A.16 | Vehicle archive subject write | `/VIID/VehicleArchiveSubjects` | √ | 删除支持正式版五类删除键 |
| A.17 | Person archive confidence | `/VIID/ArchiveConfidence` | √ | 成功响应使用 `ArchiveList` |
| A.18 | Vehicle archive confidence | `/VIID/VehicleArchiveConfidence` | √ | 成功响应使用 `VehicleArchiveList` |

## Quick Start

Create a Python 3.12 environment and install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run migrations and start the API service:

```bash
ENV=dev alembic upgrade head
ENV=dev uvicorn main:app --host 0.0.0.0 --port 8000
```

Open the interactive documentation:

| UI | URL |
| --- | --- |
| Swagger UI | http://127.0.0.1:8000/docs |
| ReDoc | http://127.0.0.1:8000/redoc |
| OpenAPI JSON | http://127.0.0.1:8000/openapi.json |
| Health probes | `/startup`、`/live`、`/ready` |
| Metrics | `/metrics` |

## API Examples

The OpenAPI schema is the easiest way to inspect request/response models:

```bash
curl http://127.0.0.1:8000/openapi.json
```

GA/T 1400 keepalive:

```bash
curl -X POST http://127.0.0.1:8000/VIID/System/Keepalive \
  -H 'Content-Type: application/json' \
  -d '{"KeepaliveObject":{"DeviceID":"APS-003"}}'
```

## Development Commands

```bash
ruff check .
pyright
pytest -q
```

Database migrations:

```bash
alembic upgrade head
alembic revision --autogenerate -m "describe change"
```

Taskiq worker:

```bash
taskiq worker core.brokers:broker
```

## Docker

Build and run the API container:

```bash
docker build -t dossier-aggr:local .
docker run --rm -p 8000:8000 -e ENV=dev dossier-aggr:local
```

The default container command is:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Helm Deployment

Helm Chart is located in `dossier-aggr/`.

Render the production-oriented default chart:

```bash
helm template dossier-aggr dossier-aggr
```

Render the low-resource development profile:

```bash
helm template dossier-aggr-dev dossier-aggr -f dossier-aggr/values-dev.yaml
```

Default production values expect resolvable `postgresql` and `rabbitmq` Services, or equivalent overrides in values:

- `ENV=prod`
- `DATABASE_URL=postgresql+asyncpg://postgres:postgres@postgresql:5432/dossier_aggr`
- `RABBITMQ_IP=rabbitmq`

The chart includes API Deployment, optional worker Deployment, Service, Ingress, HPA, ServiceMonitor, PrometheusRule, Grafana Dashboard, and an Alembic migration Job.

## Project Layout

```text
api/              FastAPI routes and protocol entry points
services/         Business orchestration
tasks/            Taskiq async tasks
repo/             Data access
models/           SQLModel/Pydantic protocol and database models
alembic/          Database migrations
core/             Config, database, broker and shared infrastructure
observability/    Metrics and observability setup
dossier-aggr/     Helm Chart
tests/            Unit, protocol, service, repository, Helm and migration tests
.ai/              AI collaboration context, protocol indexes and workflow docs
.protocol/        Local protocol source files, ignored by git
```

## Roadmap

- Continue aligning GA/T 2350.5-2025 fields, query constraints and response details with the official baseline.
- Add stronger RabbitMQ worker end-to-end regression coverage.
- Refine appendix extension-field filtering and query constraints.
- Add contribution, security and release process documents as the project opens to more collaborators.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
