# Observability

指标协议：Prometheus。

指标端点：

- `/metrics`

指标分层：

- HTTP：请求总量、请求时延、请求/响应体大小、进行中请求数；Grafana
  Dashboard 按 `method + route` 展示接口级 QPS、5xx 比例和 P95 延迟。
- ORM：SQL 次数、SQL 时延、影响行数。
- Layer：`service/task/repository` 执行时长。
- Task enqueue：`.kiq` 入队次数与入队耗时。

Grafana 可通过 Prometheus 抓取以上指标后配置请求频率、响应时间、ORM 与分层耗时看板。
Helm `monitoring.prometheusRule.routeAlerts` 可为关键接口渲染按路由的
5xx 比例和 P95 延迟告警规则；默认列表覆盖已实现的 GA/T 协议业务接口，
不包含健康检查和 `/metrics` 等运维端点。新增协议接口时应同步补充
`routeAlerts.routes`，确保接口维度告警覆盖不退化为仅看整体指标。

相关代码：

- `observability/http.py`
- `observability/sqlalchemy.py`
- `observability/layers.py`
- `observability/metrics.py`
- `observability/setup.py`
