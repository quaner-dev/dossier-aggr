# Architecture

## 总体结构

```text
Client
  -> main.py
      -> api/*          # HTTP 路由、入参/出参组装
          -> services/* # 业务编排
              -> repo/* # 数据访问
              -> tasks/* -> repo/* -> models/* -> core/database.py
```

## 请求模式

同步查询链路：

```text
API -> Service -> Repository -> DB
```

典型接口：

- `GET /VIID/System/Time`
- `GET /VIID/Subscribes/{subscribe_id}`
- `GET /VIID/SubscribeNotifications`
- `GET /VIID/ArchiveLibraries`
- `POST /VIID/VehicleArchivesQuerySync`

异步写入链路：

```text
API -> Service(dispatch_and_wait) -> task_fn.kiq(...) -> Broker -> Worker -> Repository -> DB
```

典型接口：

- `PUT /VIID/APEs`
- `POST /VIID/Faces`
- `POST /VIID/Persons`
- `POST /VIID/Subscribes`

`services/task_dispatch.py` 统一执行 `.kiq(...)` 并等待任务结果。写请求返回成功表示任务执行成功，不只是完成入队。
