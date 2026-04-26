# dossier-aggr / VIID 服务系统

基于 FastAPI 的视频图像信息数据库（VIID）接口服务，覆盖 GA/T 1400-2017、GA/T 1400-2018 试行，以及 GA/T 2350.5-2025 目标聚档相关实现。

本项目面向协议接口实现、后端服务部署和系统集成联调。当前仓库交付 FastAPI API 服务、Taskiq worker、数据库迁移和 Helm Chart，不包含独立前端应用。

## 项目简介

VIID 服务系统提供标准化的视频图像数据采集、管理、查询、订阅通知和目标聚档接口。系统采用异步 Python 技术栈构建，核心链路按 `api -> services -> tasks -> repo -> models/database` 分层组织。

## 当前状态

- GA/T 1400 主体接口已实现，包含系统注册、保活、注销、采集系统与设备、人员、人脸、订阅与通知等能力。
- GA/T 2350.5 目标聚档主流程已具备，包含档案库、档案、档案明细、档案核验等链路。
- GA/T 2350.5 与正式版协议仍有部分字段、查询约束和细节需要继续对齐；这些内容作为后续 Roadmap 推进。
- API 默认暴露 FastAPI OpenAPI 文档，服务启动后可访问 `/docs` 和 `/openapi.json`。

## 技术栈

- 后端框架：FastAPI
- 数据模型：SQLModel / Pydantic
- 数据库访问：SQLAlchemy AsyncSession
- 数据库迁移：Alembic
- 任务队列：Taskiq
- 开发/轻量测试数据库：SQLite
- 生产数据库：PostgreSQL
- 生产任务队列：RabbitMQ
- 部署：Docker / Kubernetes / Helm

## 快速开始

安装依赖：

```bash
python -m pip install -r requirements.txt
```

开发环境默认使用 `ENV=dev`，任务队列使用内存 broker，数据库默认使用 SQLite：

```bash
ENV=dev alembic upgrade head
ENV=dev uvicorn main:app --host 0.0.0.0 --port 8000
```

服务启动后可访问：

- API 文档：`http://127.0.0.1:8000/docs`
- OpenAPI JSON：`http://127.0.0.1:8000/openapi.json`
- 健康检查：`/startup`、`/live`、`/ready`
- Prometheus 指标：`/metrics`

## 数据库迁移

应用运行时使用异步数据库 URL，例如 `sqlite+aiosqlite://` 或 `postgresql+asyncpg://`。Alembic 迁移会自动转换为同步驱动 URL 执行迁移。

执行现有迁移：

```bash
alembic upgrade head
```

创建新的迁移文件：

```bash
alembic revision --autogenerate -m "describe change"
```

## 任务队列

- `ENV=dev`：使用 Taskiq `InMemoryBroker`，适合本地开发和轻量测试。
- 非 `dev` 环境：使用 RabbitMQ，对应 `RABBITMQ_USERNAME`、`RABBITMQ_PASSWORD`、`RABBITMQ_IP`、`RABBITMQ_PORT`。

生产 worker 启动命令：

```bash
taskiq worker core.brokers:broker
```

## Helm 部署

Helm Chart 位于 `dossier-aggr/`。默认 `values.yaml` 面向生产环境：

- `ENV=prod`
- `DATABASE_URL=postgresql+asyncpg://postgres:postgres@postgresql:5432/dossier_aggr`
- `RABBITMQ_IP=rabbitmq`
- 包含 API Deployment、worker Deployment、Service、Ingress、HPA、监控资源和 Alembic migration Job
- 安装和升级前通过 Helm hook 执行 `alembic upgrade head`

生产集群需要提前提供可解析的 `postgresql` 与 `rabbitmq` Service，或通过 values 覆盖为已有中间件地址。部署前通常还需要覆盖镜像仓库和镜像 tag。

渲染生产配置：

```bash
helm template dossier-aggr dossier-aggr
```

低资源开发环境可使用 `values-dev.yaml`，该配置会启用 SQLite，并关闭独立 worker 和迁移 Job：

```bash
helm template dossier-aggr-dev dossier-aggr -f dossier-aggr/values-dev.yaml
```

## 项目结构

```text
api/              FastAPI 路由与协议入口
services/         业务编排层
tasks/            Taskiq 异步任务
repo/             数据访问层
models/           SQLModel/Pydantic 协议与数据库模型
alembic/          数据库迁移
core/             配置、数据库、broker 和通用基础设施
observability/    指标与可观测性
dossier-aggr/     Helm Chart
tests/            单元、协议、仓库、服务、Helm 和迁移测试
.ai/              项目上下文、协议索引、开发约束和计划文档
```

## 协议资料与开源边界

`.protocol/` 是本地原始协议资料目录，已被 `.gitignore` 忽略，不随开源仓库分发。README 和代码只描述协议名称、接口行为和实现状态，不提交原始协议文件。

## Roadmap

- 继续对齐 GA/T 2350.5-2025 正式版字段、约束和响应细节。
- 补充 RabbitMQ 真实 worker 场景的端到端回归。
- 细化附录扩展字段的查询和过滤约束。
- 后续补充贡献指南、安全策略和更完整的开源协作流程。

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
