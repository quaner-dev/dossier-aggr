# Deployment

## 镜像

- 镜像定义：`Dockerfile`
- 基础镜像：`python:3.12-alpine`

## Helm

Helm Chart 位于 `dossier-aggr/`。

默认 API 启动命令位于 `dossier-aggr/values.yaml`：

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

worker 可选启动命令：

```bash
taskiq worker core.brokers:broker
```

## 探针

- `startup`: `/startup`
- `liveness`: `/live`
- `readiness`: `/ready`

## 修改约束

未明确要求时，不修改：

- `dossier-aggr/templates/`
- `dossier-aggr/values.yaml`
