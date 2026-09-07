# 各领域 Service 负责 S3/Kafka 接入实现方案

## 1. 背景与目标

当前通知、人脸、人员（人体）等 POST 接口需要将请求中的图片上传到 S3-compatible 对象存储，并将处理后的完整 payload 投递到 Kafka。该流程属于各领域接口的业务处理，不应由 API 路由或独立的通用 dispatch Service 负责。

本方案的目标是：

- 保留现有 API 路径、HTTP 方法、协议响应和 `create_*` 方法名称；
- 将 S3 图片处理和 Kafka 投递下沉到对应领域 Service；
- 由每个领域 Service 自己决定图片字段、topic 和 payload 处理规则；
- `s3/` 和 `message/` 仅提供现有基础设施客户端，不承载领域业务判断；
- 不引入后台任务、消息队列之外的异步编排，也不改变现有同步请求边界。

本次只调整现有领域 Service 和对应 POST 路由，不新增公共 Service、工具文件或配置项，
也不修改 S3、Kafka 客户端模块。

## 2. 当前实现

基础设施已经位于以下位置：

- `s3/storage.py`：S3-compatible 对象存储客户端；
- `message/kafka.py`：Kafka Producer；
- `main.py`：在应用 lifespan 中创建并启动 storage、producer，并放入 `app.state`；
- `app.state.object_storage_bucket_prefix`：当前应用已经提供的对象存储 bucket 配置。

当前代码还存在图片处理和 dispatch 中间层，部分 API 直接依赖 dispatch 逻辑。该结构无法体现人员、人脸、通知等领域的不同处理规则。本次不再扩展这些中间层；迁移完成后，若它们没有其他调用方，再单独清理。

## 3. 目标分层

```text
API 路由
  └── 对应领域 Service.create_*()
        ├── 读取并处理本领域 payload
        ├── 上传本领域需要的图片到 S3
        ├── 替换 StoragePath / Data 等字段
        └── 投递本领域 Kafka topic
              ├── app.state.object_storage
              └── app.state.kafka_producer
```

Service 负责业务编排，基础设施模块只负责客户端操作：

- Service 决定上传哪些图片、使用哪个 topic；
- 所有图片使用当前应用已经配置的同一个 bucket，不按日期、资源类型或 topic 拼接新的 bucket 名称；本次直接将现有 `object_storage_bucket_prefix` 配置值作为 bucket 名称使用，不重命名配置项；
- `S3CompatibleStorage.upload()` 只接收字节并返回存储地址；
- `AiokafkaProducer.send()` 只负责发送 topic 和 payload；
- 不在公共 dispatch 文件中维护人员、人脸、通知等业务 topic 或统一分支。

## 4. 各领域改造方案

### 4.1 `SubscribeNotificationService`

保持方法名 `create_subscribe_notifications` 不变，将其从“只写 Repository”调整为通知 POST 的完整接入流程。方法不接收 `storage`、`producer` 或 bucket 参数，而是通过当前请求访问 `request.app.state` 中已经初始化的客户端和单一 bucket 配置：

```python
async def create_subscribe_notifications(
    self,
    subscribe_notifications: Sequence[SubscribeNotificationData],
    *,
    request: Request,
    payload: dict[str, Any],
) -> list[SubscribeNotification]:
    ...
```

处理顺序：

1. 从 `request.app.state` 取得 `object_storage`、`kafka_producer` 和现有 bucket 配置；
2. 遍历通知 payload 中本领域支持的图片对象；
3. 上传图片并将 `StoragePath` 写回 payload，同时清空 `Data`；
4. 向 `viid.subscribe-notifications.v1` 投递处理后的 payload；
5. 按既有实现完成通知记录的 Repository 写入（如果该接口协议要求落库）；
6. 只有上述流程成功后，API 才返回成功状态。

如果通知 POST 当前仅承担 Kafka 接入、不要求写 PostgreSQL，则保留现有行为：不调用 Repository，只在投递成功后返回“已接收”。这一点需要以现有协议测试和接口约定为准，不能因重构改变语义。

### 4.2 `PersonService`

保持 `create_persons` 名称，由人员 Service 自己从 `request.app.state` 取得客户端，负责人员图片处理和 `viid.persons.v1` 投递。人员专有的图片字段、空值处理和 payload 结构不得依赖人脸或通知 Service 的通用判断。

### 4.3 `FaceService`

保持 `create_faces` 名称，由人脸 Service 自己从 `request.app.state` 取得客户端，负责图片处理和 `viid.faces.v1` 投递。人脸通常可能包含多张或嵌套图片，应由该 Service 决定遍历范围和字段规则。

### 4.4 后续人体、车辆等 Service

对人体、机动车、非机动车等 POST 接口采用相同原则：继续使用既有 `create_*` 方法名，在各自 Service 内从 `request.app.state` 取得客户端，并决定图片处理和 topic，不把所有资源重新集中到统一 dispatch 文件。

## 5. API 改造方式

API 不再注入 `MessageDispatchService`，而是注入对应领域 Service。路由只负责：

- 解析协议请求；
- 保留当前 `Request`，将请求 payload 和 request 上下文交给原有名称的 `create_*` 方法；
- 生成现有 `ResponseStatusListObject` 响应。

API 不应直接调用 `transform_images`、`producer.send` 或决定 Kafka topic。

Service 从 `request.app.state` 读取客户端；本次不新增客户端依赖函数，也不把客户端作为 `create_*` 的显式参数传递。

## 6. 模块调整

- 将 API 对公共 dispatch 的调用改为调用对应领域 Service 的原有 `create_*` 方法；
- 将各领域需要的图片遍历、S3 上传、payload 替换和 Kafka topic 调用直接写入对应 Service；
- 不新增 `MessageDispatchService`、新的图片工具或新的配置；
- `s3/storage.py`、`message/kafka.py` 保持不变，仅作为已有基础设施适配器使用；
- 现有图片/dispatch 文件只有在确认无调用方后再清理，本次不为清理而改动其他模块。

## 7. 错误、事务与响应

- S3 上传失败、图片格式非法、Kafka 发送失败时，接口不得返回协议成功；
- 投递流程保持当前请求内同步执行，不引入后台任务或额外消息队列；
- 如果同时存在数据库写入，则必须明确“投递”和“落库”的顺序，并保证成功响应只在要求的持久化操作完成后返回；
- 保持现有 `MessageUnavailableError` 及 HTTP 错误包装边界，除非协议测试明确要求变化；
- 批量请求中的图片或 Kafka 失败时，不应产生部分成功响应。

## 8. 测试计划

需要补充或调整以下测试：

- `tests/services/`：分别测试人员、人脸、通知 Service 从 `request.app.state` 取得客户端、S3 上传和 Kafka topic；
- `tests/test_api_person.py`、`tests/test_api_face.py`、`tests/test_api_subscribe_notification.py`：断言 API 调用对应 Service，而不是直接调用 dispatch；
- 协议测试：确认成功、图片参数错误、S3/Kafka 不可用时的响应外形和状态码；
- `tests/message/` 和 `tests/s3/`：继续只测试基础设施客户端行为；
- 迁移完成后运行 `git diff --check`、`ruff check .`、`pyright` 和 `pytest -q`。

## 9. 实施顺序

1. 确认通知 POST 是否需要同时写 Repository；
2. 将通知流程迁移到 `SubscribeNotificationService.create_subscribe_notifications`，客户端从 `request.app.state` 读取；
3. 将人员和人脸流程分别迁移到对应 `create_*` 方法；
4. 按同样方式处理人体、车辆等其他 POST 接口；
5. 更新 API、服务层和协议测试；
6. 仅在确认无调用方后清理旧中间层，并执行完整静态检查和测试。
