# VIID 服务系统

基于 FastAPI 的 VIID (Video Image Information Database) 协议实现，提供视频图像信息数据库的标准接口服务。

## 项目简介

VIID 服务系统实现了公安部视频图像信息数据库（VIID）协议，提供标准化的视频图像数据采集、管理和查询接口。系统采用现代 Python 技术栈构建，支持高并发处理和异步任务队列。

## 核心功能

- ✅ **系统管理**：注册、注销、心跳检测
- ✅ **数据上报**：人脸、车辆等结构化数据上报
- ✅ **订阅管理**：数据订阅和通知推送
- ✅ **异步处理**：基于 RabbitMQ 的任务队列
- ✅ **多数据源**：支持多种数据库和存储系统

## 技术栈

- **后端框架**: FastAPI + SQLModel
- **任务队列**: Taskiq + RabbitMQ
- **数据库**: SQLite (开发) / PostgreSQL (生产)
- **部署**: Kubernetes + Docker
- **认证**: HTTP Digest Authentication

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 启动服务

```bash
# 开发模式
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 启动任务队列 Worker
taskiq worker brokers:broker
```

### 数据库迁移

```bash
alembic upgrade head
```

## API 接口

系统提供标准的 VIID 协议接口：

- `POST /VIID/System/Register` - 系统注册
- `POST /VIID/System/UnRegister` - 系统注销
- `POST /VIID/System/Keepalive` - 心跳检测
- `POST /VIID/Faces` - 人脸数据上报
- `POST /VIID/Subscribes` - 订阅管理

## 部署

### Kubernetes 部署

项目包含完整的 Kubernetes 部署配置：

```bash
# 应用部署
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f pvc.yaml
```

### 容器配置

- **Web 服务**: 处理 HTTP 请求 (`j-10000-runserver`)
- **任务队列**: 异步任务处理 (`j-10000-qcluster`)

## 项目结构

```txt
├── alembic/              # 数据库迁移
├── auth.py              # HTTP Digest 认证
├── brokers.py           # 任务队列 Broker
├── main.py              # FastAPI 应用入口
├── schemas.py           # 数据模型定义
├── tasks.py             # 异步任务定义
├── utils.py             # 工具函数
├── requirements.txt     # 依赖管理
└── deployment.yaml      # Kubernetes 部署配置
```

## 开发说明

### 数据格式

系统使用 VIID 标准 JSON 格式，时间格式为 `YYYYMMDDHHMMSS`。

### 认证方式

使用 HTTP Digest Authentication：

- Realm: `VIID API`
- Algorithm: `MD5`
- QoP: `auth`

### 异步任务

系统使用 Taskiq 处理异步任务，支持：

- 人脸数据处理
- 数据批量导入
- 通知推送

## 配置说明

主要配置文件：

- `alembic.ini` - 数据库迁移配置
- `deployment.yaml` - Kubernetes 部署配置
- `pvc.yaml` - 持久化存储配置

## 许可证

MIT License
