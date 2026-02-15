# TESTING

更新时间：2026-02-14  
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

- 写接口大量通过 `.kiq(...)` 投递任务，测试写路径时必须启动 worker。
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

## 4. 接口测试矩阵（当前代码状态）

| 域 | 方法 | 路径 | 主要校验点 | 实现状态 |
| --- | --- | --- | --- | --- |
| System Register | POST | `/VIID/System/Register` | Digest 鉴权、`RegisterSchema` 入参、`ResponseStatusList` 返回 | 已实现 |
| System UnRegister | POST | `/VIID/System/UnRegister` | `UnRegisterSchema` 入参、状态返回 | 已实现 |
| System Keepalive | POST | `/VIID/System/Keepalive` | `KeepaliveSchema` 入参、状态返回 | 已实现 |
| APS 查询 | GET | `/VIID/APSs` | `APSListSchema` 包装 | 已实现 |
| APE 查询 | GET | `/VIID/APEs` | `APEListSchema` 包装 | 已实现 |
| APE 更新 | PUT | `/VIID/APEs` | 批量输入与返回状态逐条对齐 | 已实现 |
| Face 查询 | GET | `/VIID/Faces` | 全量/按 `face_id` 查询 | 已实现 |
| Face 增删改 | POST/PUT/DELETE | `/VIID/Faces` | 写后可查、响应 `ResponseStatusListSchema` | 已实现 |
| Person 查询 | GET | `/VIID/Persons` | 列表包装与字段完整性 | 已实现 |
| Person 单查 | GET | `/VIID/Persons/{person_id: str}` | 单对象返回 | 已实现 |
| Person 增删改 | POST/PUT/DELETE | `/VIID/Persons` | 批量状态回包、删除参数解析 | 已实现 |
| Subscribe 增删改查 | GET/POST/PUT/DELETE | `/VIID/Subscribes` | 时间格式、唯一约束、状态回包 | 已实现 |
| SubscribeNotification 新增 | POST | `/VIID/SubscribeNotifications` | 通知对象批量写入与状态回包 | 已实现 |
| ArchiveLibrary | GET/POST/PUT/DELETE | `/VIID/ArchiveLibraryQuerySync`、`/VIID/ArchiveLibraries` | 接口契约占位 | 占位 |
| Archive | GET/POST/PUT/DELETE | `/VIID/ArchivesQuerySync`、`/VIID/Archives` | 接口契约占位 | 占位 |
| ArchiveSubject | POST/PUT/DELETE | `/VIID/ArchiveSubjectQuerySync`、`/VIID/ArchiveSubjects` | 接口契约占位 | 占位 |

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

- `DataNotFoundError`、`DataAlreadyExistsError` 当前实现为 HTTP 200 + 业务状态对象。
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

## 8. 测试报告模板

- 测试时间：
- 代码版本（commit）：
- 环境（ENV/DATABASE_URL/Broker）：
- 用例总数/通过/失败：
- 协议不符合项：
- 接口缺陷与复现步骤：
- 结论（是否可发布）：

## 9. 当前限制与注意事项

- `Archive*` 相关接口当前多为占位实现，暂不作为“通过门槛”。
- 写操作依赖任务执行，未启动 worker 会导致写后不可见或不一致。
- 错误语义采用“HTTP 200 + 业务状态码”的场景较多，联调时需按协议字段判断业务成功与否。
