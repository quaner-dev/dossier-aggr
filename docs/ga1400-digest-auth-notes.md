# GA/T 1400 Digest 认证待核对事项

本文记录当前代码审查得到的实现问题和后续协议核对清单。本文不替代本地 `.protocol/` 原始资料；若实现结论与原始协议冲突，以原始协议为准。

## 当前设计边界

- 当前凭据来源按数据库考虑，暂不新增数据库模型、迁移或其他持久化设计。
- Redis 暂不进入本阶段实现。后续如需要多节点共享 nonce、重放记录或运行时缓存，再单独讨论。
- `RegisterSchema` 暂时不加入用户名、密码等字段。Digest 认证信息属于 HTTP `Authorization` Header，注册请求体是否包含额外凭据字段需要先核对原始协议。
- FastAPI 的 `HTTPDigest` 只提供 OpenAPI 和依赖注入占位能力，不实现完整 Digest 协议；`core/auth.py` 需要自行完成服务端校验。

## `HTTPDigest1400` 当前问题

对应代码：[`core/auth.py`](../core/auth.py)

### 凭据来源

- 当前密码固定为 `admin`，没有按 `username` 查询数据库凭据。
- 当前没有账号启用/禁用状态，也没有把认证账号与注册请求中的 `DeviceID` 绑定。
- 认证成功后返回的是原始 `HTTPAuthorizationCredentials`，没有向业务层传递经过验证的下级身份。

### Digest 参数校验

- `Authorization` 参数通过 `split(", ")` 和 `split("=", 1)` 解析，无法可靠处理空白、引号、转义字符或逗号。
- 缺少 `username`、`uri`、`nonce`、`response`、`qop`、`nc` 或 `cnonce` 时可能抛出 `ValueError`/`KeyError`，应统一返回认证失败，而不是 500。
- 没有校验请求中的 `realm`、`nonce`、`algorithm`、`qop` 和 `opaque` 是否符合服务端挑战。
- 摘要计算使用服务端固定 `self.nonce` 和 `self.qop`，没有先验证并使用请求中的对应参数。
- 没有确认请求中的 `uri` 与当前 HTTP 请求目标一致，认证结果没有完整绑定到实际请求。
- response 使用普通字符串比较，后续应改为常量时间比较。

### HTTP 语义和路由范围

- 缺少认证、认证方案错误、Digest 参数错误和 response 错误的状态码/`WWW-Authenticate` 行为需要统一核对；当前错误方案返回 403，通常应区分认证失败（401）和认证后无权限（403）。
- 当前只有 `/VIID/System/Register` 通过 `Depends(security)` 使用认证；注销、保活和其他业务路由是否也必须认证，需要以 GA/T 1400 原文和部署边界为准。
- 当前注册路由使用路由级依赖但不接收认证结果，后续无法在服务层校验 `username` 与 `RegisterObject.DeviceID` 的关系。

## 协议核对清单

在修改认证实现前，需要从 GA/T 1400 原文确认：

- 使用 RFC 2617、RFC 7616，还是标准自定义的 Digest 变体。
- 允许的 `algorithm` 是否只有 MD5，是否要求 `qop=auth`，是否允许不带 qop 的旧格式。
- `username`、密码及其与下级系统/`DeviceID` 的对应关系来自预配置还是协议报文。
- 注册请求体是否只包含 `DeviceID`，还是另有账号字段。
- Digest 是否只用于 Register，还是也用于 UnRegister、Keepalive 及其他接口。
- nonce、opaque、realm 的格式、有效期、刷新和失效语义。
- nonce 失效时是否要求 `stale=true`。
- 首次请求是否允许无 Authorization 并通过 401 challenge 后重试。
- 注册成功后是否建立会话，还是后续每个 HTTP 请求都独立执行 Digest。
- 保活超时、注销和 APS 在线状态之间的协议关系。

## 后续实现边界

协议确认后，认证层的最小职责应为：

1. 解析并校验 Digest Header。
2. 按 `username` 从数据库读取凭据。
3. 校验 challenge 参数和当前请求目标。
4. 计算并以常量时间比较 response。
5. 返回已验证的下级身份（至少包含 `username` 和允许的 `DeviceID`）。

注册、保活和注销的状态更新应留在服务层。Redis 未来可以用于 nonce TTL、重放控制和多节点共享，但不属于上述 Digest 基本校验的前置条件。

## 当前测试缺口

现有系统测试主要直接调用 `register()`，没有经过 FastAPI 的认证依赖，因此不能证明 Digest 校验正确。需要补充真实 HTTP 层面的测试：

- 缺少 Authorization 时返回 401 和 Digest challenge。
- 错误方案、格式错误、缺少参数和错误 response 均返回认证失败而不是 500。
- 正确摘要可以通过，错误 username/凭据不能通过。
- URI、realm、nonce、qop、algorithm 不匹配时不能通过。
- 认证主体与请求 `DeviceID` 不匹配时不能执行注册业务。
