# TESTING

更新时间：2026-03-05  
范围：当前仓库代码（`api/`、`services/`、`tasks/`、`models/`）

## 1. 目标

本文用于统一两类测试：

- 接口测试：验证各 API 的可用性、输入输出、错误语义。
- 协议符合性测试：验证请求/响应结构、字段格式、枚举与 URL 是否符合 GA/T 1400 与 GA/T 2350.5 的当前实现约定。

## 2. 测试环境准备

### 2.1 依赖与启动

```bash
pip install -r requirements.txt
alembic upgrade head
uvicorn main:app --host 0.0.0.0 --port 8000
taskiq worker brokers:broker
```

说明：

- 写接口通过 `dispatch_and_wait` 触发 `.kiq(...)` 并等待任务结果；真实 broker 场景需启动 worker。
- 默认 `ENV=dev` 使用 `InMemoryBroker`；非 `dev` 需要 RabbitMQ 配置。

### 2.2 必要环境变量

- `ENV`
- `DATABASE_URL`
- （非 dev）`RABBITMQ_USERNAME`、`RABBITMQ_PASSWORD`、`RABBITMQ_IP`、`RABBITMQ_PORT`

### 2.3 建议测试数据策略

- 使用独立测试库（例如临时 sqlite 文件）避免污染开发数据。
- 每个测试用例执行前后清理表数据，保证可重复执行。

## 3. 测试分层

### 3.1 健康与可用性

- `GET /startup`：启动探针返回。
- `GET /live`：进程存活返回。
- `GET /ready`：数据库可用性检查（`SELECT 1`）。

### 3.2 接口功能测试

- 按资源域覆盖 CRUD/查询能力。
- 对批量接口验证“输入条数 == 返回状态条数”。
- 对查询接口验证列表包装对象名与字段完整性。

### 3.3 协议符合性测试

- URL 与方法是否匹配 `constants.py`。
- 顶层包装对象命名是否正确（如 `PersonListObject`、`ResponseStatusListObject`）。
- 时间字段是否为 `YYYYMMDDHHMMSS`。
- 枚举字段编码类型是否符合模型定义（`IntEnum`/`StrEnum`）。
- 错误场景返回体是否为约定协议对象。

### 3.4 异步一致性测试

- 写接口调用后，轮询查询接口确认最终一致性。
- 校验未启动 worker 时的行为是否符合预期（作为负向用例保留）。

### 3.5 分层边界测试

- 对 `services -> repositories -> tasks` 的职责边界增加约束测试。
- 典型规则：
  - `services` 同步读取路径不直接调用 `tasks`
  - `tasks` 作为异步入口层，不直接内联数据库访问
  - `collection`、`archive`、`archive_subject`、`task`、`vehicle`、`vehicle_archive_subject`、`person`、`face`、`subscribe`、`verify` 域均保留分层约束回归用例

### 3.6 监控指标测试

- `/metrics` 必须可访问且返回 Prometheus 文本格式。
- 至少覆盖以下关键指标族：
  - `dossier_aggr_http_requests_total`
  - `dossier_aggr_http_request_duration_seconds`
  - `dossier_aggr_orm_queries_total`
- 建议通过一次健康探针与一次数据库探针请求触发样本后再断言指标文本。

## 4. 接口测试矩阵（当前代码状态）

| 域 | 方法 | 路径 | 主要校验点 | 实现状态 |
| --- | --- | --- | --- | --- |
| System Register | POST | `/VIID/System/Register` | Digest 鉴权、`RegisterSchema` 入参、`ResponseStatusList` 返回 | 已实现 |
| System UnRegister | POST | `/VIID/System/UnRegister` | `UnRegisterSchema` 入参、状态返回 | 已实现 |
| System Keepalive | POST | `/VIID/System/Keepalive` | `KeepaliveSchema` 入参、状态返回 | 已实现 |
| System Time | GET | `/VIID/System/Time` | `SystemTime` 返回与时间格式校验 | 已实现 |
| APS 查询 | GET | `/VIID/APSs` | `APSListSchema` 包装 | 已实现 |
| APE 查询 | GET | `/VIID/APEs` | `APEListSchema` 包装 | 已实现 |
| APE 更新 | PUT | `/VIID/APEs` | 批量输入与返回状态逐条对齐 | 已实现 |
| Face 查询（批量） | GET | `/VIID/Faces` | 返回默认 `TOP100` 列表 | 已实现 |
| Face 查询（单条） | GET | `/VIID/Faces/{face_id}` | 路径参数单查，返回 `Face` 对象 | 已实现 |
| Face 修改（单条） | PUT | `/VIID/Faces/{face_id}` | 路径参数单条修改，返回 `ResponseStatus` | 已实现 |
| Face 删除（单条） | DELETE | `/VIID/Faces/{face_id}` | 路径参数单条删除，返回 `ResponseStatus` | 已实现 |
| Face 增删改 | POST/PUT/DELETE | `/VIID/Faces` | 写后可查、响应 `ResponseStatusListSchema` | 已实现 |
| Person 查询 | GET | `/VIID/Persons` | 返回默认 `TOP100` 列表 | 已实现 |
| Person 单查 | GET | `/VIID/Persons/{person_id}` | 单对象返回 | 已实现 |
| Person 修改（单条） | PUT | `/VIID/Persons/{person_id}` | 路径参数单条修改，返回 `ResponseStatus` | 已实现 |
| Person 删除（单条） | DELETE | `/VIID/Persons/{person_id}` | 路径参数单条删除，返回 `ResponseStatus` | 已实现 |
| Person 增删改 | POST/PUT/DELETE | `/VIID/Persons` | 批量状态回包、删除参数解析 | 已实现 |
| Subscribe 增删改查 | GET/POST/PUT/DELETE | `/VIID/Subscribes` | 时间格式、唯一约束、状态回包 | 已实现 |
| Subscribe 单条取消 | PUT | `/VIID/Subscribes/{subscribe_id}` | 路径参数与 `Subscribe` 负载一致性、`ResponseStatus` 回包 | 已实现 |
| SubscribeNotification 新增 | POST | `/VIID/SubscribeNotifications` | 通知对象批量写入与状态回包 | 已实现 |
| SubscribeNotification 查询 | GET | `/VIID/SubscribeNotifications` | 通知对象批量查询与列表包装 | 已实现 |
| SubscribeNotification 删除 | DELETE | `/VIID/SubscribeNotifications` | `IDList` 批量删除与状态回包 | 已实现 |
| ArchiveLibrary | GET/POST/PUT/DELETE | `/VIID/ArchiveLibraries` | 批量查询/增改删与状态回包；GET 支持 `ArchiveLibrary` 属性键值对查询，DELETE 使用 `IDList` | 已实现（A.5 主链路） |
| ArchiveTask | - | `/VIAS/Tasks` | 按当前交付范围省略，不在 OpenAPI 中暴露，也不纳入回归测试 | 未实现 |
| Archive | GET/POST/PUT/DELETE | `/VIID/ArchivesQuerySync`、`/VIID/Archives` | 查询结果包装、批量增改删状态回包 | 已实现（A.9/A.10 主链路） |
| VehicleArchive | POST/POST/PUT/DELETE | `/VIID/VehicleArchivesQuerySync`、`/VIID/VehicleArchives` | `POST /VIID/VehicleArchivesQuerySync` 使用 `ArchiveQuery` 查询并返回 `ArchiveQueryResult`；`DELETE /VIID/VehicleArchives` 使用 `IDList` | 已实现（A.11/A.12 主链路） |
| ArchiveSubject | POST/PUT/DELETE | `/VIID/ArchiveSubjectQuerySync`、`/VIID/ArchiveSubjects` | 明细查询与批量增改删状态回包；删除仅按 `ArchiveID` | 已实现（A.13/A.14 主链路） |
| VehicleArchiveSubject | POST/PUT/DELETE | `/VIID/VehicleArchiveSubjectQuerySync`、`/VIID/VehicleArchiveSubjects` | 车辆明细查询与批量增改删状态回包 | 已实现（A.15/A.16 主链路） |
| ArchiveConfidence | POST | `/VIID/ArchiveConfidence` | 人员档案核验状态回包 | 已实现（A.17 主链路） |
| VehicleArchiveConfidence | POST | `/VIID/VehicleArchiveConfidence` | 车辆档案核验状态回包 | 已实现（A.18 主链路） |

## 5. 协议符合性检查清单

### 5.1 URL 与资源命名

- 路径必须使用 `constants.py` 中定义值，不允许自由拼写。
- 资源命名保持复数（如 `APEs`、`Persons`、`Subscribes`）。

### 5.2 消息包装结构

- 批量对象必须使用 `<Domain>ListObject` 包装。
- 状态返回优先使用 `ResponseStatusListSchema`。
- 字段名保持协议风格（驼峰命名，大小写敏感）。

### 5.3 日期时间格式

- 协议时间按 `YYYYMMDDHHMMSS` 处理。
- 重点字段：`BeginTime`、`EndTime`、`LocalTime`、`CreateTime`、`UpdateTime`。

### 5.4 枚举值校验

- `IntEnum` 字段应为整数语义值。
- `StrEnum` 字段应为协议约定字符串值（如图片类型、格式等）。

### 5.5 错误语义

- `DataNotFoundError`：HTTP 404 + 协议状态对象。
- `DataAlreadyExistsError`：HTTP 409 + 协议状态对象。
- `InvalidParameterError` / 请求校验错误：HTTP 400 + 协议状态对象。
- `TaskExecutionError`：HTTP 503 + 协议状态对象。
- 协议测试应同时断言：
  - HTTP 状态码
  - `StatusCode`/`StatusString`
  - 响应包装对象形状

## 6. 基线用例（建议最小集合）

### 6.1 健康检查

```bash
curl -s http://127.0.0.1:8000/startup
curl -s http://127.0.0.1:8000/live
curl -s http://127.0.0.1:8000/ready
```

### 6.2 Register（Digest）

```bash
curl --digest -u tester:admin \
  -H 'Content-Type: application/json' \
  -X POST http://127.0.0.1:8000/VIID/System/Register \
  -d '{"RegisterObject":{"DeviceID":"APS-001"}}'
```

### 6.3 APE 批量更新 + 查询回读

```bash
curl -H 'Content-Type: application/json' \
  -X PUT http://127.0.0.1:8000/VIID/APEs \
  -d '{"APEListObject":{"APEObject":[{"ApeID":"APE-001","Name":"Cam-1","Model":"M1","IPAddr":"192.168.1.10","IPV6Addr":null,"Port":8001,"Longitude":116.39,"Latitude":39.90,"PlaceCode":"110000","Place":"BJ","OrgCode":"110101","CapDirection":0,"MonitorDirection":1,"MonitorAreaDesc":"Gate","IsOnline":1,"OwnerApsID":"APS-001","UserId":"admin","Password":"pass","FunctionType":"Capture","PositionType":"Fixed"}]}}'

curl -s http://127.0.0.1:8000/VIID/APEs
```

### 6.4 Subscribe 重复创建（负向）

- 首次创建应成功。
- 使用同一 `SubscribeID` 再次创建，应返回“已存在”语义（当前实现由业务异常给出）。

### 6.5 异步最终一致性（Taskiq）

- 对 `.kiq` 写路径，断言接口返回与任务执行结果一致（`dispatch_and_wait` 语义）。
- 对 InMemoryBroker 场景，保留轮询+超时验证最终可见性的 e2e 用例。
- 至少覆盖一个异步写资源域（当前基线：`ArchiveSubject`）。

## 7. 自动化落地建议（`pytest`）

- 目录建议：
  - `tests/api/`：接口行为测试
  - `tests/protocol/`：协议结构与格式测试
  - `tests/e2e/`：含 worker 的最终一致性测试
- 每个接口至少覆盖：
  - `happy path`
  - 参数缺失/格式错误
  - 资源不存在
  - 重复写入（如唯一键）
- 协议测试建议使用 `model_validate` 对响应进行结构校验，避免只做字符串断言。
- 分层重构时增加边界回归测试（参考 `tests/services/test_subscribe_layering.py`、`tests/services/test_person_face_layering.py`、`tests/services/test_collection_archive_layering.py`、`tests/services/test_subject_verify_layering.py`）。
- 监控指标建议增加端点回归测试（参考 `tests/test_api_metrics.py`）。
- 2350 A.7/A.8 建议维持复用路由与字段约束测试（参考 `tests/protocol/test_2350_routes.py`、`tests/protocol/test_2350_subscribe_contract.py`）。

## 8. 测试报告模板

- 测试时间：
- 代码版本（commit）：
- 环境（ENV/DATABASE_URL/Broker）：
- 用例总数/通过/失败：
- 协议不符合项：
- 接口缺陷与复现步骤：
- 结论（是否可发布）：

## 9. 当前限制与注意事项

- 2350 接口主链路已覆盖 A.5-A.18；A.13/A.14 与 A.15/A.16 明细链路已切换为持久化仓储实现。
- 写操作依赖任务执行；真实 broker 场景未启动 worker 通常会在 `dispatch_and_wait` 超时后返回 `TaskExecutionError`（HTTP 503）。
- 错误语义采用“HTTP 状态码 + 协议状态对象”组合，联调时需同时判断两者。
