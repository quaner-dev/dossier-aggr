# Kafka 高并发接入实现文档

本文是 [`docs/data-push-architecture.md`](./data-push-architecture.md) 的编码指南。
架构文档已经确定业务边界，本文只把它翻译成一组简单、可逐步执行的代码任务。

当前只做一件事：指定的高并发 `POST` 先进入 FastAPI 进程内存队列，后台上传图片并
发送一条 Kafka 消息。当前不做 Kafka consumer、不做 PostgreSQL 批量物化、不做出站
推送。

## 1. 先记住这条主流程

```text
指定 POST
  -> FastAPI 协议校验
  -> 读取调用方原始 JSON
  -> message 接入队列 put_nowait
  -> 立即返回 HTTP 200

后台：接入队列
  -> 上传 Base64 图片
  -> StoragePath = 上传返回值，Data = null
  -> Kafka 队列
  -> Kafka producer 发送一条 record
```

同一个请求必须先完成图片上传和 JSON 替换，再发送 Kafka；不同请求可以并行。HTTP
响应不等待图片上传、Kafka 发送或 broker ACK。

HTTP 200 的含义只有：协议校验通过，并且请求已经进入当前 FastAPI 进程的有界内存
队列。进程崩溃、重启或强制退出时，尚未处理的内存队列数据可能丢失，这是当前业务
已经接受的风险。

## 2. 接口范围

### 2.1 当前接入 Kafka 的 POST

| HTTP 路径 | Kafka topic | 实施顺序 |
| --- | --- | --- |
| `POST /VIID/Faces` | `viid.faces.v1` | 第一个纵向切片 |
| `POST /VIID/Persons` | `viid.persons.v1` | Faces 完成后 |
| `POST /VIID/SubscribeNotifications` | `viid.subscribe-notifications.v1` | Persons 完成后 |

后续协议和模型准备好后，再增加：

| HTTP 路径 | Kafka topic |
| --- | --- |
| `POST /VIID/MotorVehicles` | `viid.motor-vehicles.v1` |
| `POST /VIID/NonMotorVehicles` | `viid.non-motor-vehicles.v1` |

机动车和非机动车目前没有完整协议模型。没有 `.protocol/` 原文和契约测试时，不要
用 `dict[str, Any]` 占位实现它们。

### 2.2 保持 PostgreSQL 同步的接口

以下接口完全保持现有 Service/Repository/事务路径：

- 所有 GET、PUT、DELETE。
- `POST /VIID/Archives`。
- `POST /VIID/ArchiveSubjects`。
- 车辆档案、车辆档案明细和其他未列出的 POST。
- 订阅创建、修改、取消等控制面接口。

这些接口不调用 `message` 队列，不依赖 Kafka 或对象存储，也不等待 Kafka 物化。

### 2.3 明确不做的内容

不要在本次实现中增加：

- Kafka consumer、批量写 PostgreSQL、物化进程、物化状态查询。
- 台账表、`event_id`、`batch_id`、`operation` 或新增追踪字段。
- DLQ、自动重试、补偿、consumer lag 监控或出站推送。
- Kafka record key。
- 每请求一个 `BackgroundTasks` 或无界 `create_task`。
- SHA-256、图片去重或业务层 object key 规则。
- 为了接入 Kafka 而修改协议字段、数据库表模型或历史迁移。

## 3. 目标目录：所有接入代码集中在 `message/`

新增一个独立的根目录包 `message/`，专门表示消息接入和 Kafka/对象存储适配。不要把
这些文件放入现有的 `core/`、`services/`、`repo/` 或 `api/` 业务目录，也不要创建
根目录 `ingest/` 或 `consumers/`。

```text
message/
  __init__.py       # 对外导出 topic 和 MessageManager
  config.py         # Kafka/对象存储/队列环境变量
  storage.py        # 对象存储接口、首个 adapter 和图片递归转换
  kafka.py          # KafkaProducer Protocol 和 aiokafka 实现
  manager.py        # 入队、两个有界队列、固定 Worker、启动和停止
```

说明：

- 选择 `message` 而不是 `consumer`，因为当前只写入 Kafka，还没有消费 Kafka。
- `message/` 是接入基础设施边界；API 不直接导入 Kafka SDK 或对象存储 SDK。
- `core/settings.py` 继续保留 PostgreSQL 配置。Kafka/对象存储配置放到
  `message/config.py`，避免继续扩大现有 `core` 配置文件。
- API 路由只依赖 `MessageManager.enqueue()`；dependency 也放在 `message/manager.py`。
- 不新增 `services/ingestion.py`、`core/ingestion/`、`api/dependencies.py`、Factory 或
  Runtime 包装层。

测试集中放在独立目录：

```text
tests/message/test_storage.py
tests/message/test_kafka.py
tests/message/test_manager.py
tests/test_message_lifespan.py
tests/test_api_kafka_ingestion.py
```

## 4. Sol Light 的执行方式

后续使用 `gpt-5.6-sol` Light；CLI 中对应 Low。每次只执行一个小阶段，不要求代理
一次完成全部改造。

给代理的任务固定写成：

```text
只执行 docs/kafka-ingestion-implementation.md 的“阶段 N”。
先检查前置条件，只修改该阶段列出的文件，先补测试再写代码。
执行该阶段的定向命令。遇到停止条件时不要猜测、换依赖或扩大范围。
不要开始阶段 N+1。
```

每一阶段都要：

1. 先读取本文、架构文档、`AGENTS.md` 和涉及的现有代码。
2. 只修改允许修改的文件；需要额外文件时先停止并说明原因。
3. 先补最小测试，再写实现。
4. 通过定向测试、`ruff check`、`pyright` 和 `git diff --check` 后再进入下一阶段。

## 5. 编码前置条件

当前工作树正在进行 Domain/Schema 分离。开始 Kafka 编码前，必须先确认该重构已经
结束，并运行：

```bash
git diff --check
ruff check .
pyright
pytest -q
```

如果基线失败、相关文件仍在被其他任务修改，或者协议字段需要修改但本地原文不可用，
停止 Kafka 实现。不要在 Kafka 任务中修复或回退无关重构。

还需要部署方确认：Kafka broker 地址和认证方式、对象存储平台和稳定地址格式、真实
Base64 大小、10,000 指标的准确单位、容器内存和 Uvicorn 进程数。

## 6. 数据契约

### 6.1 内部队列对象

`message/manager.py` 直接使用下列简单 dataclass；这些字段只用于进程内编排和
日志，不得写入 Kafka value：

```python
@dataclass(slots=True)
class MessageItem:
    topic: str
    request_path: str
    business_ids: tuple[str, ...]
    bucket: str
    payload: dict[str, Any]
```

只需要一种对象。图片转换完成后，直接把同一个 item 的 `payload` 交给 Kafka 队列，
不必再创建 `IngressItem`/`KafkaItem` 两套重复类型。队列本身已经代表处理阶段。

`topic`、`request_path`、`business_ids`、`bucket` 不能合并到 `payload`。不生成任何
额外 ID；响应和日志使用协议已有的 `FaceID`、`PersonID` 或 `NotificationID`。

### 6.2 Kafka value

一次 HTTP POST 对应一条 Kafka record。value 是图片处理后的原始请求 JSON：

- 保留外层对象、字段名称和大小写、列表/对象层级、调用方提交的字段和值。
- 不增加 envelope、资源类型、事件 ID、批次 ID、操作类型或技术字段。
- 不拆分 `FaceObject`、`PersonObject` 或通知内的对象。
- 只修改图片节点的 `StoragePath` 和 `Data`。
- 不使用 Pydantic `model_dump()` 作为 Kafka value 来源。

JSON 的空白、缩进和原始字节顺序不承诺逐字节一致；结构和字段语义必须一致。

### 6.3 Kafka key/header/topic

- record key 为 `None`（空 key）。
- 自定义 header 只有：`content-type=application/json`。
- topic 固定为第 2 节的接口 topic；不增加环境前缀。
- 五个 topic 预建为每个 12 个分区。API 启动时不自动创建 topic。

不同请求不承诺顺序。调用方重复 POST 可能产生重复 record；当前不增加业务幂等层。

## 7. 原始 JSON 的取得

路由保留类型化 body 参数用于 FastAPI/Pydantic 校验，同时接收 `Request`：

```python
async def faces_create(
    request: Request,
    data: FaceListObjectSchema,
    message_manager: Annotated[
        MessageManager, Depends(get_message_manager)
    ],
) -> ResponseStatusListSchema:
    raw_payload = await request.json()
    message_manager.enqueue(
        topic=FACES_TOPIC,
        request_path=constants.FACES_URL,
        business_ids=[face.FaceID for face in data.FaceListObject.FaceObject],
        payload=raw_payload,
    )
    ...
```

实现规则：

1. `data` 只用于校验、读取业务 ID 和构造现有成功响应。
2. `raw_payload = await request.json()` 是 Kafka payload 来源；顶层必须是 JSON object。
3. `MessageManager.enqueue()` 对 payload 做一次 `copy.deepcopy` 后调用队列
   `put_nowait`，从此由后台拥有该对象。
4. HTTP body 中未提交的可选字段不能因为模型默认值而出现在 Kafka value 中。
5. 入队成功后直接返回现有 `ResponseStatusListObject`，状态码和状态文字不变。

如果协议校验失败，FastAPI 返回 400，且不能调用 `message_manager`。如果队列满或
manager 没有接收，返回协议包装的 503。

## 8. Base64 图片处理

`message/storage.py` 同时放图片转换函数和 `ObjectStorage` Protocol，避免为一个简单
转换过程再增加额外 service 层。

### 8.1 识别和替换

递归遍历所有 `dict` 和 `list`。mapping 同时包含大小写完全一致的 `Data` 和
`StoragePath` 时，视为图片节点：

1. `Data` 为 `None` 或空字符串：不上传、不修改。
2. `Data` 为非空字符串：严格按纯 Base64 解码。
3. 按节点的 `FileFormat` 选择 `content_type`。
4. 调用 `await storage.upload(bucket=bucket, content=bytes, content_type=...)`。
5. 成功后设置 `StoragePath` 为返回值，设置 `Data` 为 `None`。
6. 其他字段不修改，不增加 key，不删除 key。

当前只接受纯 Base64，不接受 `data:image/jpeg;base64,...` Data URI。协议以后确认允许
Data URI 时，另开任务修改规则和测试，不在实现中自行兼容。

### 8.2 格式映射

| `FileFormat` | MIME 类型 |
| --- | --- |
| `Bmp` | `image/bmp` |
| `Gif` | `image/gif` |
| `Jpeg` | `image/jpeg` |
| `Png` | `image/png` |

缺少或不支持 `FileFormat`、Base64 解码失败、上传返回空地址或地址超过当前协议的
256 字符限制，都视为该请求的后台失败。不能猜 MIME、截断地址或把原始 Base64 发到
Kafka。

单个请求内按遍历顺序逐张上传，不对图片创建无界并发任务。第 N 张失败时整条 Kafka
消息丢弃；已经上传的对象暂不删除，也不做补偿。

### 8.3 日期 bucket

接收请求时按 `CHINA_TZ` 计算并写入 item，格式固定为：

```text
viid-{YYYYMMDD}
```

例如 `20260901` 对应 `viid-20260901`。不能由后台处理时间重新计算，避免跨午夜积压
进入错误日期。

## 9. 对象存储接口

`message/storage.py` 定义平台无关接口：

```python
class ObjectStorage(Protocol):
    async def start(self) -> None: ...

    async def upload(
        self,
        *,
        bucket: str,
        content: bytes,
        content_type: str,
    ) -> str: ...

    async def close(self) -> None: ...
```

业务层只把返回值写入 `StoragePath`，将其当作不透明字符串。业务层不判断 AWS、
MinIO、Ceph、OSS 或 OBS，也不生成 object key。

如果确认首个平台是 S3-compatible，首个具体类也直接放在 `message/storage.py`，使用
一个长生命周期异步 client。adapter 内部负责：

- 根据 content type 生成随机 object key；不使用业务 ID，不计算 SHA-256。
- 按日期 bucket 做一次存在性检查/创建并缓存结果；不能每张图片重复检查。
- 设置上传 `ContentType`。
- 返回平台提供的稳定地址；平台没有稳定地址时，使用部署方确认的长期地址格式。
- 不返回会过期的预签名 URL。

如果目标平台不是可靠的 S3-compatible，新增对应 adapter，不在业务代码中写平台分支。
如果部署方尚未确认 `StoragePath` 的长期格式，停在 adapter 阶段，不猜测地址。

## 10. Kafka producer

`message/kafka.py` 定义：

```python
class KafkaProducer(Protocol):
    async def start(self) -> None: ...

    async def send_json(self, *, topic: str, payload: dict[str, Any]) -> None: ...

    async def stop(self) -> None: ...
```

首个实现使用 `aiokafka`，每个 FastAPI 进程只创建一个长生命周期 producer：

```text
acks=all
enable_idempotence=True
compression_type=配置值，初始 lz4
key=None
headers=[("content-type", b"application/json")]
```

producer 的 `send_and_wait` 只在 Kafka Worker 中执行。HTTP 路由不等待 broker ACK。

value 使用：

```python
json.dumps(
    payload,
    ensure_ascii=False,
    separators=(",", ":"),
    allow_nan=False,
).encode("utf-8")
```

不要排序 key、不要套 envelope、不要序列化 Pydantic 模型。超时、消息过大、序列化或
broker 错误由 Worker 记录并丢弃；不向已返回 200 的调用方补发错误。

## 11. MessageManager 和生命周期

`message/manager.py` 集中管理入队、两个队列、Worker 以及 client 生命周期，不再拆分
Pipeline、Runtime 和 Service。

只保留两个 `asyncio.Queue`：

```text
input_queue: asyncio.Queue[MessageItem]   # HTTP 入队
kafka_queue: asyncio.Queue[MessageItem]   # 图片处理完成后待发送
```

固定数量的 storage worker：

1. 从 `input_queue` 取 item。
2. 递归处理图片。
3. 使用 `kafka_queue.put_nowait(item)`。
4. 在 `finally` 调用 `input_queue.task_done()`。

固定数量的 Kafka worker：

1. 从 `kafka_queue` 取 item。
2. 调用 `producer.send_json()`。
3. 在 `finally` 调用 `kafka_queue.task_done()`。

后台 worker 只捕获普通 `Exception` 并记录安全日志；`CancelledError` 必须继续抛出。
不重试、不重新入队、不写 DLQ。

同一个 manager 的 `enqueue()` 只做三件事：计算日期 bucket、深拷贝 payload、调用
`input_queue.put_nowait`。建议接口：

```python
class MessageManager:
    def enqueue(
        self,
        *,
        topic: str,
        request_path: str,
        business_ids: Sequence[str],
        payload: dict[str, Any],
    ) -> None: ...
```

`get_message_manager(request: Request)` 从 `request.app.state.message_manager` 直接返回
manager。测试通过 `app.dependency_overrides` 注入 fake，不连接外部服务。

启动顺序：

1. 读取并校验 `message/config.py` 配置。
2. 启动 storage。
3. 启动 producer。
4. 创建固定数量的两个 Worker。
5. 设置 `accepting=True`。

如果启动失败，已启动的 client 必须关闭，FastAPI 不进入 serving 状态。

`main.py` 使用 lifespan：

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    manager = MessageManager.from_config()
    await manager.start()
    app.state.message_manager = manager
    try:
        yield
    finally:
        await manager.stop(timeout=INGEST_SHUTDOWN_TIMEOUT_SECONDS)
        app.state.message_manager = None
```

停止时先禁止新入队，再在一个总超时内等待两个队列完成，取消剩余 Worker，最后关闭
producer 和 storage。超时的剩余数量写日志，不写消息内容。关闭方法可以重复调用。

## 12. 配置和依赖

配置放在 `message/config.py`，默认值只用于功能联调，不代表生产容量：

```text
INGEST_INPUT_QUEUE_MAX_ITEMS=256
INGEST_KAFKA_QUEUE_MAX_ITEMS=4096
INGEST_STORAGE_WORKERS=4
INGEST_KAFKA_WORKERS=2
INGEST_SHUTDOWN_TIMEOUT_SECONDS=10

KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_CLIENT_ID=dossier-aggr-api
KAFKA_SEND_TIMEOUT_SECONDS=5
KAFKA_COMPRESSION_TYPE=lz4

OBJECT_STORAGE_PROVIDER=s3-compatible
OBJECT_STORAGE_BUCKET_PREFIX=viid
OBJECT_STORAGE_ENDPOINT_URL=
OBJECT_STORAGE_REGION=
OBJECT_STORAGE_ACCESS_KEY_ID=
OBJECT_STORAGE_SECRET_ACCESS_KEY=
```

要求：

- 队列容量、worker 数、超时必须大于零；配置错误在启动时失败。
- 不提供默认密码、access key 或 secret key；允许使用部署环境默认凭证链。
- access key 和 secret key 必须同时设置或同时留空。
- 当前不区分 dev/test/prod，不在 topic 前加环境名。
- `OBJECT_STORAGE_PROVIDER` 不是 `s3-compatible` 时先停止，不自动回退本地文件。
- 每个 Uvicorn 进程拥有独立队列和 client，多进程会按进程数放大内存与连接数。
- Base64 保留在 input queue 时按请求体大小占用内存；不能只看队列条数调大容量。

候选运行依赖为 `aiokafka`、`aioboto3`、`lz4`。加入 `pyproject.toml` 前，必须在 Python
3.14 和当前 Alpine Dockerfile 中完成 import、client 生命周期和最小 smoke。兼容失败时
停止并报告，不能自行改用同步库、线程池、其他 Python 版本或其他基础镜像。

## 13. 现有路由的最小修改

### 13.1 Faces

只修改 `api/face/face.py` 的批量 POST：

- 增加 `Request` 参数和 `get_message_manager` dependency。
- 读取 raw JSON，提取已校验的 `FaceID` 列表。
- 调用 `MessageManager.enqueue(topic=FACES_TOPIC, ...)`。
- 删除该 POST 对 `FaceService.create_faces` 的调用。
- 保留现有响应对象、每个 ID 一个状态、`StatusCode="0"`、`StatusString="已接收"`。

同文件 GET/PUT/DELETE 和单对象接口不改。

### 13.2 Persons

Faces 完成后，只修改 `api/person/person.py` 的批量 POST：使用 `PERSONS_TOPIC` 和
`PersonID`，不调用 `PersonService.create_persons`；其他方法不改。

### 13.3 SubscribeNotifications

Persons 完成后，只修改 `api/subscribe/subscribe_notification.py` 的 POST：使用
`SUBSCRIBE_NOTIFICATIONS_TOPIC` 和 `NotificationID`，不调用通知 create Service；
GET/DELETE 仍同步查删 PostgreSQL。增加包含多层人脸、人员、档案图片的 raw JSON 测试，
证明通知仍只产生一条 Kafka record。

现有直接调用 POST 路由函数的测试改为 `httpx.ASGITransport`，因为路由新增了
`Request` 和 dependency；GET/PUT/DELETE 的直接测试可以继续使用。

## 14. 错误和日志

在 `message/manager.py` 定义一个 HTTP 503 的 `MessageUnavailableError`，复用现有
通用 `HTTPException` handler，错误仍包装为 `ResponseStatusListObject`。队列满或 manager
停止接收时抛出该异常，不能返回 200。

后台失败只记录以下元数据：

```text
stage=storage_upload | kafka_enqueue | kafka_send
request_path
topic
business_ids
异常类型和截断后的错误摘要
相关队列长度
```

日志禁止包含完整 payload、Base64、Kafka value、请求对象、认证 header、密码、access
key、secret key、session token 或连接签名。异常摘要去掉换行并限制长度。成功请求不
逐条打印 INFO，避免日志 I/O 反过来限制吞吐。

后台失败在 HTTP 200 之后发生，只记录并丢弃；第一阶段没有重试、补偿或状态查询。

## 15. 测试要求

### 15.1 `tests/message/test_storage.py`

- 递归处理 dict/list 中的所有图片节点。
- Base64 成功上传后只改变 `StoragePath` 和 `Data`。
- `Data=None`、空字符串不上传。
- 四种 `FileFormat` 的 MIME 映射正确。
- 非法 Base64、Data URI、缺少/未知格式、空地址、超过 256 字符均失败。
- 多层通知处理后仍保持原始字段和层级，不生成额外字段。
- fake 上传失败时整条消息不进入 Kafka。

### 15.2 `tests/message/test_manager.py`

- start/stop 调用 storage 和 producer 的生命周期各一次。
- input queue 满或停止接收抛 `MessageUnavailableError`。
- 图片处理完成后才进入 Kafka queue。
- storage、kafka enqueue、kafka send 三类失败日志 stage 正确。
- 每个成功 item 最多调用一次 `send_json`，不重试不重新入队。
- Worker 取消时执行 `task_done()`；stop 在总超时内结束并关闭 client。
- 日志哨兵断言不包含 Base64 和 secret。

### 15.3 `tests/message/test_kafka.py`

- topic、value、key、header 与第 6 节完全一致。
- value 没有 envelope、event/batch/operation 字段。
- 中文按 UTF-8 发送，`allow_nan=False`。
- producer 生命周期和超时错误正确传递。

### 15.4 API/lifespan 测试

`tests/test_api_kafka_ingestion.py` 覆盖：

- Faces、Persons、通知合法 POST 返回 200 并只 enqueue 一次。
- raw JSON 的省略字段不会变成模型默认字段。
- POST 不调用数据库 create Service。
- 队列满返回 503 协议错误；协议校验失败返回 400 且不 enqueue。
- GET/PUT/DELETE 仍调用同步数据库 fake，不调用 message fake。
- 通知多层图片仍只有一条 Kafka payload。

`tests/test_message_lifespan.py` 覆盖：

- manager 在 lifespan 进入前启动、退出时停止。
- 启动失败会清理已启动 client。
- 关闭后清理 `app.state.message_manager`。
- fake storage/Kafka 被阻塞时，HTTP 入队响应仍不等待后台完成。

## 16. 分阶段执行清单

### 阶段 0：确认基线

只读检查当前 Domain/Schema 重构和协议资料：

```bash
git diff --check
ruff check .
pyright
pytest -q
```

失败或相关文件仍在并发修改时停止，不修改 Kafka 代码。

### 阶段 1：创建独立 `message/` 基础包

允许修改：

```text
message/__init__.py
message/config.py
message/storage.py
message/kafka.py
message/manager.py
tests/message/test_storage.py
tests/message/test_manager.py
```

先实现 dataclass、topic 常量、配置解析、图片纯转换、两个有界队列和 fake adapter；不
连接真实 Kafka/对象存储，不修改 API 路由。

定向命令：

```bash
pytest -q tests/message/test_storage.py tests/message/test_manager.py
ruff check message tests/message
pyright
git diff --check
```

### 阶段 2：加入 producer 和对象存储 adapter

允许修改：

```text
message/kafka.py
message/storage.py
tests/message/test_kafka.py
tests/message/test_storage.py
pyproject.toml
tests/test_project_layout.py
Dockerfile
```

先验证 Python 3.14/Alpine 兼容性，再加入依赖。完成 fake SDK 测试和受控环境 smoke。
兼容性或认证方式不明确时停止，不替换库。

### 阶段 3：接入 lifespan 和错误响应

允许修改：

```text
message/manager.py
main.py
tests/test_message_lifespan.py
tests/message/test_manager.py
```

把 manager 接入 FastAPI lifespan，实现 `get_message_manager` 和 503。不要再增加
Runtime、Service 或 Factory，也不修改 Faces/Persons/通知路由。

定向命令：

```bash
pytest -q tests/message tests/test_message_lifespan.py
ruff check message main.py tests/message tests/test_message_lifespan.py
pyright
git diff --check
```

### 阶段 4：Faces 纵向切片

允许修改：

```text
api/face/face.py
tests/test_api_face.py
tests/test_api_kafka_ingestion.py
```

只改 Faces 批量 POST，完成第 13.1 节测试。GET/PUT/DELETE 回归通过后才继续。

### 阶段 5：Persons 迁移

允许修改：

```text
api/person/person.py
tests/test_api_person.py
tests/test_api_kafka_ingestion.py
```

只改 Persons 批量 POST；Faces 和 Persons 的 GET/PUT/DELETE 仍走 PostgreSQL。

### 阶段 6：SubscribeNotifications 迁移

允许修改：

```text
api/subscribe/subscribe_notification.py
tests/test_api_subscribe_notification.py
tests/test_api_kafka_ingestion.py
tests/protocol/test_2350_subscribe_contract.py
```

只改通知 POST，增加真实嵌套图片测试；通知 GET/DELETE 保持同步。

### 阶段 7：容器和全量回归

允许修改：

```text
README.md
AGENTS.md
Dockerfile
docs/kafka-ingestion-implementation.md
```

执行：

```bash
git diff --check
ruff check .
pyright
pytest -q
docker build -t dossier-aggr:kafka-message .
```

再由部署方确认五个 topic 均为 12 分区，并用无图、单图、多图和嵌套通知样本做实际
Kafka/对象存储 smoke。

## 17. 完成标准

- [ ] 所有 Kafka/对象存储/队列代码都在独立根目录 `message/`，没有新增 `core/ingestion`、
      `services/ingestion`、`api/dependencies`、Pipeline、Runtime、Service 或 Factory 包装层。
- [ ] Faces、Persons、SubscribeNotifications POST 入队成功后立即返回 200。
- [ ] 队列满或 manager 停止接收返回协议包装的 503。
- [ ] 一次 POST 只产生一条 Kafka record，key 为空，header 只有 content-type。
- [ ] Kafka value 保留 raw JSON，不增加字段，只把图片 `StoragePath` 换成上传返回值、
      `Data` 换成 JSON `null`。
- [ ] Base64 不进入 Kafka，不计算 SHA-256，不在业务层生成 object key。
- [ ] bucket 为接收日期的 `viid-{YYYYMMDD}`。
- [ ] 对象存储和 Kafka producer 每进程长生命周期复用。
- [ ] 后台失败只记录安全日志并丢弃，不重试、不写 DLQ、不建台账。
- [ ] GET/PUT/DELETE、Archives、ArchiveSubjects 仍同步访问 PostgreSQL。
- [ ] 五个 topic 由部署预建，每个 12 分区，API 不自动创建。
- [ ] Python 3.14、本机工具、Docker 镜像和全量测试均通过。

## 18. 暂不自行决定的问题

以下答案必须由部署/协议负责人确认；没有答案时可以完成 fake manager，但不能上线
具体 adapter：

1. “均值 10,000”是 requests/s、业务对象/s 还是并发连接数。
2. Base64 最大单图/单请求大小，是否永远是纯 Base64。
3. 首个对象存储平台及 `StoragePath` 的稳定长期格式。
4. bucket 自动创建权限和生命周期策略。
5. Kafka broker、认证/TLS、单 record 上限、保留时间和复制因子。
6. Uvicorn 进程数、容器内存和 termination grace period。
7. 机动车、非机动车协议原文和完整模型。

这些问题若要求改变“入队即成功”、Kafka value 结构、图片字段规则或持久化保证，必须
先修改并重新评审架构文档，不能由 Light 实现代理自行决定。
