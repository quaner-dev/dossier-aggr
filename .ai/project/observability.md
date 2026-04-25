# Observability

指标协议：Prometheus。

指标端点：

- `/metrics`

指标分层：

- HTTP：请求总量、请求时延、请求/响应体大小、进行中请求数。
- ORM：SQL 次数、SQL 时延、影响行数。
- Layer：`service/task/repository` 执行时长。
- Task enqueue：`.kiq` 入队次数与入队耗时。

Grafana 可通过 Prometheus 抓取以上指标后配置请求频率、响应时间、ORM 与分层耗时看板。

相关代码：

- `observability/http.py`
- `observability/sqlalchemy.py`
- `observability/layers.py`
- `observability/metrics.py`
- `observability/setup.py`
