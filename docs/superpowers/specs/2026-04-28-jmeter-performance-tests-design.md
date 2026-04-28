# JMeter Performance Tests Design

## Context

The project currently validates API behavior with pytest, protocol route checks, Helm rendering tests, and metrics endpoint checks. It does not yet provide a reusable way to run load tests against a deployed runtime.

The next step is to add JMeter-based performance test assets that can be run later when dedicated machines and deployment topology are ready. The assets must not affect the default `pytest -q` workflow and must not require JMeter to be installed for normal development.

## Goals

- Provide a standard JMeter entry point for API throughput and latency testing.
- Cover a small set of low-risk interfaces first, then allow new scenarios to be added incrementally.
- Make load parameters configurable without editing the JMeter plan.
- Produce repeatable `.jtl` and HTML reports outside tracked source files.
- Document how to compare results only under the same environment, deployment, database, worker count, and test parameters.

## Non-Goals

- Do not replace pytest functional or protocol tests.
- Do not add JMeter or Java to Python dependencies.
- Do not commit generated performance reports.
- Do not benchmark final production capacity before the test machines are prepared.
- Do not make write-heavy scenarios part of the first default load plan.

## Proposed Layout

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

`.ai/testing/` should be updated with a short performance testing section that points to the JMeter assets and states that performance tests are manually executed, environment-sensitive checks.

## Initial Scenarios

The first JMeter plan should include these enabled HTTP samplers:

- `GET /live`
- `GET /ready`
- `GET /metrics`
- `GET /VIID/System/Time`

The plan should include a disabled or separately documented write scenario for:

- `POST /VIID/Subscribes`

The subscribe write scenario should use CSV-driven unique IDs and should not be enabled by default, because it writes data and may require database cleanup.

## Runtime Model

JMeter should test the deployed HTTP runtime, not the in-process FastAPI app:

```text
JMeter
  -> HTTP endpoint or ingress
  -> FastAPI middleware
  -> api/
  -> services/
  -> repo/ or tasks/
  -> database and broker when relevant
```

This keeps performance results closer to real deployment behavior than an in-process Python benchmark.

## JMeter Plan Requirements

The `.jmx` plan should use JMeter properties for runtime configuration:

- `BASE_URL`, default `http://127.0.0.1:8000`
- `THREADS`, default `10`
- `RAMP_UP`, default `10`
- `DURATION`, default `60`
- `CONNECT_TIMEOUT_MS`, default `5000`
- `RESPONSE_TIMEOUT_MS`, default `10000`

The plan should include:

- HTTP Request Defaults.
- A Thread Group using the configurable thread count, ramp-up, and duration.
- Response assertions for successful HTTP status codes.
- JSON or text assertions only where stable response content exists.
- Aggregate Report and Summary Report listeners for local interactive runs.

The command-line documented path should use non-GUI mode and write reports under `reports/performance/` or `tests/performance/jmeter/reports/`, with generated files excluded from source control except `.gitkeep`.

## Reporting

The README should document a baseline command similar to:

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

The report interpretation guide should focus on:

- Requests per second.
- Error rate.
- Average latency.
- P50, P90, P95, and P99 latency.
- Status code distribution.
- Test environment and deployment metadata.

## Safety and Cleanup

- Read-only scenarios are safe to run repeatedly.
- Write scenarios must use unique IDs and document cleanup steps.
- Generated `.jtl`, HTML reports, and temporary CSV outputs must not be committed.
- Performance claims should cite the exact command, JMeter version, service version, machine spec, database backend, worker count, and deployment mode.

## Testing Strategy

Default verification remains:

```bash
ruff check .
pyright
pytest -q
```

JMeter execution is manual and documented. The repository can include a minimal pytest smoke test only if it validates static assets without requiring JMeter, such as checking that the `.jmx` file exists and contains the expected configurable properties.

## Rollout

1. Add the JMeter directory structure and initial `.jmx` plan.
2. Add README instructions and sample CSV data.
3. Update `.ai/testing/` documentation to include performance testing guidance.
4. Add `.gitignore` rules for generated performance reports if current rules do not already exclude them.
5. Later, add more protocol scenarios such as SubscribeNotification, Faces, Persons, Archive query, and write-path tests with cleanup.
