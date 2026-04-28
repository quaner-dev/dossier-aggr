# JMeter 性能测试设计

## 背景

当前项目已经通过 pytest、协议路由检查、Helm 渲染测试和指标端点测试来验证 API 行为，但还没有提供一套可复用的方式，对已部署运行时执行接口压测。

下一步需要加入基于 JMeter 的性能测试资产。等专用机器和部署拓扑准备好后，可以直接使用这些资产执行压测。相关资产不能影响默认 `pytest -q` 工作流，也不能要求普通开发环境必须安装 JMeter。

## 目标

- 提供标准的 JMeter 入口，用于 API 吞吐量和时延测试。
- 第一阶段先覆盖少量低风险接口，后续可以逐步追加新场景。
- 压测参数可配置，不需要直接修改 JMeter 测试计划。
- 生成可复现的 `.jtl` 和 HTML 报告，报告文件不纳入源码跟踪。
- 文档中明确：只有在相同环境、相同部署方式、相同数据库、相同任务进程数量和相同测试参数下，压测结果才有可比性。

## 非目标

- 不替代 pytest 的功能测试和协议测试。
- 不把 JMeter 或 Java 加入 Python 依赖。
- 不提交生成的性能测试报告。
- 在测试机器准备好之前，不宣称最终生产容量。
- 第一阶段默认压测计划不包含重写入场景。

## 建议目录结构

```text
tests/performance/
  README.md
  jmeter/
    dossier-aggr-api.jmx
    data/
      README.md
      sample-subscribe.csv
    reports/
      .gitkeep
```

`.ai/testing/` 需要增加一段性能测试说明，指向 JMeter 资产，并明确性能测试是手动执行、强依赖环境的专项检查。

## 第一阶段场景

第一版 JMeter 计划默认启用以下 HTTP 采样器：

- `GET /live`
- `GET /ready`
- `GET /metrics`
- `GET /VIID/System/Time`

计划中可以包含一个默认禁用或单独说明的写入场景：

- `POST /VIID/Subscribes`

订阅写入场景需要通过 CSV 提供唯一 ID，并且默认不启用。原因是该场景会写入数据，可能需要数据库清理策略。

## 运行时模型

JMeter 应该测试已部署的 HTTP 运行时，而不是进程内 FastAPI 应用：

```text
JMeter
  -> HTTP 端点或入口网关
  -> FastAPI 中间件
  -> api/
  -> services/
  -> repo/ 或 tasks/
  -> 相关数据库和消息代理
```

这样得到的性能结果比进程内 Python 基准测试更接近真实部署行为。

## JMeter 计划要求

`.jmx` 计划需要使用 JMeter 属性做运行时配置：

- `BASE_URL`，默认值 `http://127.0.0.1:8000`
- `THREADS`，默认值 `10`
- `RAMP_UP`，默认值 `10`
- `DURATION`，默认值 `60`
- `CONNECT_TIMEOUT_MS`，默认值 `5000`
- `RESPONSE_TIMEOUT_MS`，默认值 `10000`

测试计划需要包含：

- HTTP 请求默认值。
- 线程组，并使用可配置的线程数、升压时间和持续时间。
- 用于校验 HTTP 成功状态码的响应断言。
- 只在响应内容稳定的接口上增加 JSON 或文本断言。
- 聚合报告和汇总报告监听器，方便本地交互式运行时观察结果。

文档中的命令行运行方式应使用非 GUI 模式，并将报告写入 `reports/performance/` 或 `tests/performance/jmeter/reports/`。除 `.gitkeep` 外，生成文件不应纳入源码管理。

## 报告

README 中应记录类似下面的基准命令：

```bash
jmeter -n \
  -t tests/performance/jmeter/dossier-aggr-api.jmx \
  -JBASE_URL=http://127.0.0.1:8000 \
  -JTHREADS=50 \
  -JRAMP_UP=30 \
  -JDURATION=300 \
  -l reports/performance/result.jtl \
  -e -o reports/performance/html
```

报告解读说明应重点关注：

- 每秒请求数。
- 错误率。
- 平均时延。
- P50、P90、P95 和 P99 时延。
- HTTP 状态码分布。
- 测试环境和部署元数据。

## 安全与清理

- 只读场景可以重复运行。
- 写入场景必须使用唯一 ID，并文档化清理步骤。
- 生成的 `.jtl`、HTML 报告和临时 CSV 输出不能提交。
- 性能结论必须附带完整上下文，包括执行命令、JMeter 版本、服务版本、机器规格、数据库后端、任务进程数量和部署方式。

## 测试策略

默认验证流程保持不变：

```bash
ruff check .
pyright
pytest -q
```

JMeter 执行是手动操作，并通过文档说明。仓库可以包含一个最小 pytest 冒烟测试，但前提是该测试只校验静态资产，不要求安装 JMeter。例如检查 `.jmx` 文件存在，并包含预期的可配置属性。

## 落地步骤

1. 增加 JMeter 目录结构和初始 `.jmx` 计划。
2. 增加 README 执行说明和示例 CSV 数据。
3. 更新 `.ai/testing/` 文档，补充性能测试说明。
4. 如果当前 `.gitignore` 尚未排除生成的性能报告，则补充对应规则。
5. 后续继续增加更多协议场景，例如 SubscribeNotification、Faces、Persons、Archive 查询，以及带清理策略的写路径测试。
