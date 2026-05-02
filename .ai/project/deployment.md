# Deployment

## 镜像

- 镜像定义：`Dockerfile`
- 基础镜像：`python:3.12-alpine`

## Helm

Helm Chart 位于 `dossier-aggr/`。

当前 Kubernetes 部署内容已集中到该 Chart：

- API Deployment：`dossier-aggr/templates/deployment.yaml`
- Worker Deployment：`dossier-aggr/templates/worker-deployment.yaml`
- Alembic 迁移 Job：`dossier-aggr/templates/migration-job.yaml`
- Service、Ingress、HPA、ServiceMonitor、PrometheusRule 和 Grafana Dashboard 模板位于 `dossier-aggr/templates/`
- 默认运行参数、探针、镜像、环境变量和 worker 开关位于 `dossier-aggr/values.yaml`

默认 `values.yaml` 面向生产部署：

- `ENV=prod`
- `RABBITMQ_IP=rabbitmq`，使用集群内默认 RabbitMQ 服务名
- `DATABASE_URL=postgresql+asyncpg://postgres:postgres@postgresql:5432/dossier_aggr`，使用集群内默认 PostgreSQL 服务名
- `TASKIQ_RESULT_BACKEND_URL=redis://redis:6379/0`，使用集群内默认 Redis 服务名保存 Taskiq 任务结果
- 数据库连接池默认参数：`DB_POOL_SIZE=10`、`DB_MAX_OVERFLOW=20`、
  `DB_POOL_TIMEOUT_SECONDS=30`、`DB_POOL_RECYCLE_SECONDS=1800`、
  `DB_POOL_PRE_PING=true`
- API 和 worker 通过 `app.kubernetes.io/component` 标签隔离，Service 只选择 API Pod
- 安装和升级前通过 Helm hook 执行 `alembic upgrade head`
- Alembic 迁移读取 `DATABASE_URL`，并在运行迁移前将异步驱动 URL 转换为同步驱动 URL

生产集群需要提前提供可解析的 `rabbitmq`、`postgresql` 与 `redis` Service，
或通过 `values.yaml` 覆盖上述环境变量指向已有中间件。非 `dev` 环境如果未配置
`TASKIQ_RESULT_BACKEND_URL`，应用会启动失败，避免写接口在没有共享任务结果后端时
错误地返回成功。
API、worker 和 migration Job 支持通过全局 `envFrom` 引用外部
Kubernetes Secret/ConfigMap 注入运行时配置；worker 和 migration 也保留各自的
`worker.envFrom`、`migration.envFrom` 扩展项。生产凭据优先通过 Secret 注入，
不要写入仓库跟踪的 values 文件。
生产 schema 只由 Alembic migration Job 管理；repository 中保留的 `create_all`
兼容兜底仅在 `ENV=dev` 生效。

低资源开发环境可使用 `dossier-aggr/values-dev.yaml`：

```bash
helm template dossier-aggr-dev dossier-aggr -f dossier-aggr/values-dev.yaml
```

该覆盖文件设置 `ENV=dev`、SQLite 数据库，并关闭独立 worker 和迁移 Job，用于本地或轻量测试；生产不要使用该覆盖文件。

默认 API 启动命令位于 `dossier-aggr/values.yaml`：

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

worker 可选启动命令：

```bash
taskiq worker core.brokers:broker tasks
```

## 探针

- `startup`: `/startup`
- `liveness`: `/live`
- `readiness`: `/ready`

## 修改约束

未明确要求时，不修改：

- `dossier-aggr/templates/`
- `dossier-aggr/values.yaml`

## 升级注意

当前 API Deployment 的 selector 包含 `app.kubernetes.io/component=api`。如果已有旧版本 Release 使用不带 component 的 selector，Kubernetes 不允许原地修改 Deployment selector；升级时需要先删除旧 API Deployment 或重新安装 Release。
