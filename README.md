# dossier-aggr / VIID 服务系统

<p align="center">
  <img src="docs/assets/dossier-aggr-overview.svg" alt="dossier-aggr VIID 服务系统总览" width="860">
</p>

<p align="center">
  <a href="https://www.python.org/downloads/release/python-3120/"><img alt="Python 3.12" src="https://img.shields.io/badge/python-3.12-3776AB?logo=python&logoColor=white"></a>
  <a href="https://fastapi.tiangolo.com/"><img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-API-009688?logo=fastapi&logoColor=white"></a>
  <a href="https://docs.pydantic.dev/"><img alt="Pydantic v2" src="https://img.shields.io/badge/Pydantic-v2-E92063?logo=pydantic&logoColor=white"></a>
  <a href="https://docs.pytest.org/"><img alt="pytest" src="https://img.shields.io/badge/tests-pytest-0A9EDC?logo=pytest&logoColor=white"></a>
  <a href="https://github.com/astral-sh/ruff"><img alt="ruff" src="https://img.shields.io/badge/lint-ruff-261230"></a>
  <a href="LICENSE"><img alt="MIT License" src="https://img.shields.io/badge/license-MIT-blue"></a>
</p>

`dossier-aggr` 是一个基于 FastAPI 的视频图像信息数据库（VIID）接口服务，面向 GA/T 1400、GA/T 2350.5 等国内公共安全行业标准的协议实现、后端部署和系统集成联调。

当前仓库交付 API 服务、Taskiq worker、数据库迁移和 Helm Chart，不包含独立前端应用。

## 项目能力

- 覆盖 GA/T 1400-2017 与 2018 试行资料中的系统注册、保活、注销、校时、采集系统、采集设备、人员、人脸、订阅与通知等主链路。
- 覆盖 GA/T 2350.5-2025 目标聚档服务中的目标档案库、聚档任务、人员/车辆档案、档案明细和档案核验主链路。
- 自动生成 OpenAPI，并通过 Swagger UI 与 ReDoc 提供接口调试页面。
- 开发环境默认使用 SQLite 和 Taskiq 内存 broker；生产环境支持 PostgreSQL 和 RabbitMQ。
- 提供 Dockerfile、Helm Chart、Kubernetes 探针、Prometheus 指标和 Grafana Dashboard 模板。

## 运行环境

| 项目 | 当前目标 |
| --- | --- |
| Python | 3.12 |
| API 框架 | FastAPI |
| 数据模型 | SQLModel / Pydantic v2 |
| 数据库迁移 | Alembic |
| 异步任务 | Taskiq |
| 开发数据库 | SQLite |
| 生产数据库 | PostgreSQL |
| 生产消息队列 | RabbitMQ |

> 仓库当前没有 GitHub Actions 工作流，因此 README 不展示远端 CI 通过徽章。质量状态以本地执行 `ruff check .`、`pyright`、`pytest -q` 的结果为准。

## 协议资料

本仓库不分发标准原文。`.protocol/` 是本地原始协议资料目录，已被 `.gitignore` 忽略；协议判断先查 `.ai/protocols/` 下的索引，必要时回到本地 `.protocol/` 文件核验。

| 协议 | 本地资料路径 | 公开参考 |
| --- | --- | --- |
| GA/T 1400.1-2017 通用技术要求 | `.protocol/1400/GA-T 1400.1-2017 公安视频图像信息应用系统 第1部分：通用技术要求.doc` | [国家数字标准馆](https://www.ndls.org.cn/standard/detail/f71a4415fcb5553126a987f4c79415c9) |
| GA/T 1400.2-2017 应用平台技术要求 | `.protocol/1400/GA-T 1400.2-2017 公安视频图像信息应用系统 第2部分：应用平台技术要求.doc` | [国家数字标准馆](https://www.ndls.org.cn/standard/detail/764238571834b42cfbeb6fc31a47204c) |
| GA/T 1400.3-2017 数据库技术要求 | `.protocol/1400/GA-T 1400.3-2017 公安视频图像信息应用系统 第3部分：数据库技术要求.doc` | [国家数字标准馆](https://www.ndls.org.cn/standard/detail/87eccff00012e165e1ae34d25c3747f6) |
| GA/T 1400.4-2017 接口协议要求 | `.protocol/1400/GA-T 1400.4-2017 公安视频图像信息应用系统 第4部分：接口协议要求.doc` | [国家数字标准馆](https://www.ndls.org.cn/standard/detail/4ac5697f21cc24610b6f66da80722c1e) |
| GA/T 1400 试行资料 | `.protocol/1400/20180521 视图库对接技术要-试行.pdf` | 本地资料 |
| GA/T 2350.5-2025 目标聚档服务 | `.protocol/2350/GA-T 2350.5-2025.pdf`、`.protocol/2350/GA-T 2350.5-2025.docx` | [国家数字标准馆关联条目](https://www.ndls.org.cn/standard/detail/e9bd6546ff969e6a6335c973e1271738)、[公安部标准公告转载](https://www.secrss.com/articles/84327) |

## 功能清单

状态说明：`√` 表示当前仓库已有对应 API、模型和服务主链路；`×` 表示当前仓库未实现。带备注的 `√` 代表接口已存在，但仍有字段、查询语义或正式版细节需要继续核对。

### GA/T 1400

| 协议功能 | 典型路径 | 状态 | 说明 |
| --- | --- | --- | --- |
| 系统注册 | `/VIID/System/Register` | √ | Digest 鉴权；返回协议状态对象 |
| 系统注销 | `/VIID/System/UnRegister` | √ | 返回协议状态对象 |
| 系统保活 | `/VIID/System/Keepalive` | √ | 返回协议状态对象 |
| 系统校时 | `/VIID/System/Time` | √ | 返回系统时间对象 |
| 视图库服务资源 | `/VIID/VIIDServers` | × | 未实现 |
| 采集设备 APE | `/VIID/APEs` | √ | 已实现查询和修改主链路 |
| 采集系统 APS | `/VIID/APSs` | √ | 已实现查询主链路 |
| 卡口 | `/VIID/Tollgates` | × | 未实现 |
| 车道 | `/VIID/Lanes` | × | 未实现 |
| 视频片段元数据/数据 | `/VIID/VideoSlices` | × | 未实现 |
| 图像元数据/数据 | `/VIID/Images` | × | 未实现 |
| 文件元数据/数据 | `/VIID/Files` | × | 未实现 |
| 人员 | `/VIID/Persons` | √ | 支持批量和单项查询、增加、修改、删除 |
| 人脸 | `/VIID/Faces` | √ | 支持批量和单项查询、增加、修改、删除 |
| 机动车 | `/VIID/MotorVehicles` | × | 未实现 |
| 非机动车 | `/VIID/NonMotorVehicles` | × | 未实现 |
| 物品 | `/VIID/Things` | × | 未实现 |
| 场景 | `/VIID/Scenes` | × | 未实现 |
| 案事件 | `/VIID/Cases` | × | 未实现 |
| 布控 | `/VIID/Dispositions` | × | 未实现 |
| 布控告警通知 | `/VIID/DispositionNotifications` | × | 未实现 |
| 订阅 | `/VIID/Subscribes` | √ | 支持订阅查询、创建、更新、删除、取消 |
| 订阅通知 | `/VIID/SubscribeNotifications` | √ | 支持通知上报、查询和删除 |
| 分析规则 | `/VIID/AnalysisRules` | × | 未实现 |
| 视频标签 | `/VIID/VideoLabels` | × | 未实现 |
| VIAS 系统与能力 | `/VIAS/System*`、`/VIAS/SystemCapability/*` | × | 未实现 |

### GA/T 2350.5

| 条款 | 协议功能 | 路径 | 状态 | 说明 |
| --- | --- | --- | --- | --- |
| A.5 | 目标档案库 | `/VIID/ArchiveLibraries` | √ | 已基本对齐 |
| A.6 | 聚档任务 | `/VIAS/Tasks` | √ | 主链路已实现；`Task` 字段仍需结合 GA/T 1399-2017 继续核对 |
| A.7 | 订阅 | `/VIID/Subscribes` | √ | 复用 1400 路由；2350 扩展语义仍需核对 |
| A.8 | 订阅通知 | `/VIID/SubscribeNotifications` | √ | 复用 1400 路由；已补齐部分 2350 扩展列表 |
| A.9 | 人员档案查询 | `/VIID/ArchivesQuerySync` | √ | 查询行为尚未覆盖正式版全部检索语义 |
| A.10 | 人员档案增改删 | `/VIID/Archives` | √ | 批量增加、修改、删除主链路 |
| A.11 | 车辆档案查询 | `/VIID/VehicleArchivesQuerySync` | √ | 查询行为尚未覆盖正式版全部检索语义 |
| A.12 | 车辆档案增改删 | `/VIID/VehicleArchives` | √ | 批量增加、修改、删除主链路 |
| A.13 | 人员档案明细查询 | `/VIID/ArchiveSubjectQuerySync` | √ | 查询行为尚未覆盖正式版全部检索语义 |
| A.14 | 人员档案明细增改删 | `/VIID/ArchiveSubjects` | √ | 删除支持正式版五类删除键 |
| A.15 | 车辆档案明细查询 | `/VIID/VehicleArchiveSubjectQuerySync` | √ | 查询行为尚未覆盖正式版全部检索语义 |
| A.16 | 车辆档案明细增改删 | `/VIID/VehicleArchiveSubjects` | √ | 删除支持正式版五类删除键 |
| A.17 | 人员档案核验 | `/VIID/ArchiveConfidence` | √ | 成功响应使用 `ArchiveList` |
| A.18 | 车辆档案核验 | `/VIID/VehicleArchiveConfidence` | √ | 成功响应使用 `VehicleArchiveList` |

## 快速开始

创建 Python 3.12 环境并安装依赖：

```bash
python -m pip install -r requirements.txt
```

执行数据库迁移并启动 API 服务：

```bash
ENV=dev alembic upgrade head
ENV=dev uvicorn main:app --host 0.0.0.0 --port 8000
```

服务启动后可访问：

| 入口 | 地址 |
| --- | --- |
| Swagger UI | http://127.0.0.1:8000/docs |
| ReDoc | http://127.0.0.1:8000/redoc |
| OpenAPI JSON | http://127.0.0.1:8000/openapi.json |
| 健康检查 | `/startup`、`/live`、`/ready` |
| Prometheus 指标 | `/metrics` |

## 接口示例

获取 OpenAPI 描述：

```bash
curl http://127.0.0.1:8000/openapi.json
```

GA/T 1400 保活接口：

```bash
curl -X POST http://127.0.0.1:8000/VIID/System/Keepalive \
  -H 'Content-Type: application/json' \
  -d '{"KeepaliveObject":{"DeviceID":"APS-003"}}'
```

## 开发命令

```bash
ruff check .
pyright
pytest -q
```

数据库迁移：

```bash
alembic upgrade head
alembic revision --autogenerate -m "describe change"
```

启动 Taskiq worker：

```bash
taskiq worker core.brokers:broker
```

## Docker

构建并运行 API 镜像：

```bash
docker build -t dossier-aggr:local .
docker run --rm -p 8000:8000 -e ENV=dev dossier-aggr:local
```

容器默认启动命令：

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Helm 部署

Helm Chart 位于 `dossier-aggr/`。

渲染默认生产配置：

```bash
helm template dossier-aggr dossier-aggr
```

渲染低资源开发配置：

```bash
helm template dossier-aggr-dev dossier-aggr -f dossier-aggr/values-dev.yaml
```

默认生产配置要求集群内存在可解析的 `postgresql` 和 `rabbitmq` Service，或通过 values 覆盖为实际中间件地址：

- `ENV=prod`
- `DATABASE_URL=postgresql+asyncpg://postgres:postgres@postgresql:5432/dossier_aggr`
- `RABBITMQ_IP=rabbitmq`

Chart 包含 API Deployment、可选 worker Deployment、Service、Ingress、HPA、ServiceMonitor、PrometheusRule、Grafana Dashboard，以及 Alembic migration Job。

## 项目结构

```text
api/              FastAPI 路由与协议入口
services/         业务编排层
tasks/            Taskiq 异步任务
repo/             数据访问层
models/           SQLModel/Pydantic 协议模型与数据库模型
alembic/          数据库迁移
core/             配置、数据库、broker 和通用基础设施
observability/    指标与可观测性
dossier-aggr/     Helm Chart
tests/            单元、协议、服务、仓库、Helm 和迁移测试
.ai/              AI 协作上下文、协议索引和开发流程文档
.protocol/        本地协议原始资料，已被 git 忽略
```

## Roadmap

- 继续对齐 GA/T 2350.5-2025 正式版字段、查询约束和响应细节。
- 补充 RabbitMQ worker 真实场景端到端回归测试。
- 细化附录扩展字段的查询与过滤约束。
- 补充贡献指南、安全策略和发布流程文档。

## License

本项目采用 MIT License，详见 [LICENSE](LICENSE)。
