# Architecture

本文件只说明系统组件关系和总体拓扑。分层职责和禁止事项以 `.ai/project/layers.md` 为准；具体接口运行链路以 `.ai/project/runtime-chain.md` 为准。

## 系统拓扑

```text
Client
  -> main.py
      -> api/*
          -> services/*
              -> repo/*
              -> tasks/* -> repo/*
                  -> models/*
                  -> core/database.py
```

## 组件职责

- `main.py`：创建 FastAPI 应用，注册 lifespan、middleware 和 router。
- `api/`：HTTP 协议边界，负责路由、参数接收和响应包装。
- `services/`：业务编排层，协调同步读取和异步写入。
- `repo/`：数据访问层，负责查询、过滤、排序、分页和持久化语义。
- `tasks/`：Taskiq 任务入口，承接需要异步执行的写路径。
- `models/`：协议模型、SQLModel 表模型和跨层数据对象。
- `core/`：配置、数据库、异常、常量、认证、broker 和共享工具。

## 运行原则

- 读取路径通常由 `services/` 直接调用 `repo/`。
- 写入路径通常由 `services/` 通过 `dispatch_and_wait` 进入 `tasks/`。
- 每个协议接口是否走 Taskiq，以 `.ai/project/runtime-chain.md` 和现有实现映射为准。
