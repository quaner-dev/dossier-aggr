# Runtime Chain

本文件说明一个协议接口从 HTTP 入口到数据库的运行链路。分层职责以 `.ai/project/layers.md` 为准。

## 标准链路

```mermaid
flowchart TD
    Client[Client or Upstream System] --> API[api/ FastAPI route]
    API --> Service[services/ business orchestration]
    Service -->|sync read| Repo[repo/ data access]
    Service -->|async write| Task[tasks/ Taskiq task]
    Task --> Repo
    Repo --> Models[models/ protocol and SQLModel objects]
    Repo --> DB[(Database)]
```

## 读取路径

```mermaid
flowchart LR
    API[api/] --> Service[services/]
    Service --> Repo[repo/]
    Repo --> Models[models/]
    Repo --> DB[(Database)]
```

读取接口通常不需要 Taskiq。`services/` 可以直接调用 `repo/`，由 `repo/` 负责过滤、排序、分页和空结果语义。

## 写入路径

```mermaid
flowchart LR
    API[api/] --> Service[services/]
    Service --> Dispatch[dispatch_and_wait]
    Dispatch --> Task[tasks/]
    Task --> Repo[repo/]
    Repo --> Models[models/]
    Repo --> DB[(Database)]
```

写入接口通过 `dispatch_and_wait` 进入 Taskiq 任务。`tasks/` 只作为异步任务入口，不直接承载数据库细节。

## A.6 `/VIAS/Tasks` 链路示例

```mermaid
flowchart TD
    Route["api/task/archive_task.py<br/>archive_tasks_*"] --> Service["ArchiveTaskService"]
    Service -->|GET| Repo["repo/task/archive_task.py"]
    Service -->|POST/PUT/DELETE| Task["tasks/task/archive_task.py"]
    Task --> Repo
    Repo --> Model["models/task/archive_task.py<br/>ArchiveTask"]
    Repo --> DB[(archive_task table)]
```
