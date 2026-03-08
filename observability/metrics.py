from dataclasses import dataclass
from threading import Lock


def _escape_label(value: str) -> str:
    return (
        value.replace("\\", "\\\\")
        .replace("\n", "\\n")
        .replace('"', '\\"')
    )


def _render_labels(label_names: tuple[str, ...], key: tuple[str, ...]) -> str:
    if not label_names:
        return ""
    pairs = [
        f'{label_name}="{_escape_label(label_value)}"'
        for label_name, label_value in zip(label_names, key, strict=True)
    ]
    return "{" + ",".join(pairs) + "}"


class CounterChild:
    def __init__(self, parent: "Counter", key: tuple[str, ...]):
        self._parent = parent
        self._key = key

    def inc(self, amount: float = 1.0) -> None:
        self._parent._inc(self._key, amount)


class GaugeChild:
    def __init__(self, parent: "Gauge", key: tuple[str, ...]):
        self._parent = parent
        self._key = key

    def inc(self, amount: float = 1.0) -> None:
        self._parent._inc(self._key, amount)

    def dec(self, amount: float = 1.0) -> None:
        self._parent._inc(self._key, -amount)

    def set(self, value: float) -> None:
        self._parent._set(self._key, value)


class HistogramChild:
    def __init__(self, parent: "Histogram", key: tuple[str, ...]):
        self._parent = parent
        self._key = key

    def observe(self, value: float) -> None:
        self._parent._observe(self._key, value)


@dataclass
class HistogramState:
    buckets: list[int]
    count: int
    total: float


class Counter:
    def __init__(self, name: str, help_text: str, label_names: list[str] | None = None):
        self.name = name
        self.help_text = help_text
        self.label_names = tuple(label_names or [])
        self._values: dict[tuple[str, ...], float] = {}
        self._lock = Lock()

    def labels(self, **labels: str) -> CounterChild:
        key = tuple(labels[label] for label in self.label_names)
        return CounterChild(self, key)

    def inc(self, amount: float = 1.0) -> None:
        self._inc(tuple(), amount)

    def _inc(self, key: tuple[str, ...], amount: float) -> None:
        with self._lock:
            self._values[key] = self._values.get(key, 0.0) + amount

    def render(self) -> list[str]:
        lines = [f"# HELP {self.name} {self.help_text}", f"# TYPE {self.name} counter"]
        with self._lock:
            items = sorted(self._values.items())
        for key, value in items:
            lines.append(f"{self.name}{_render_labels(self.label_names, key)} {value}")
        return lines


class Gauge:
    def __init__(self, name: str, help_text: str, label_names: list[str] | None = None):
        self.name = name
        self.help_text = help_text
        self.label_names = tuple(label_names or [])
        self._values: dict[tuple[str, ...], float] = {}
        self._lock = Lock()

    def labels(self, **labels: str) -> GaugeChild:
        key = tuple(labels[label] for label in self.label_names)
        return GaugeChild(self, key)

    def inc(self, amount: float = 1.0) -> None:
        self._inc(tuple(), amount)

    def dec(self, amount: float = 1.0) -> None:
        self._inc(tuple(), -amount)

    def set(self, value: float) -> None:
        self._set(tuple(), value)

    def _inc(self, key: tuple[str, ...], amount: float) -> None:
        with self._lock:
            self._values[key] = self._values.get(key, 0.0) + amount

    def _set(self, key: tuple[str, ...], value: float) -> None:
        with self._lock:
            self._values[key] = value

    def render(self) -> list[str]:
        lines = [f"# HELP {self.name} {self.help_text}", f"# TYPE {self.name} gauge"]
        with self._lock:
            items = sorted(self._values.items())
        for key, value in items:
            lines.append(f"{self.name}{_render_labels(self.label_names, key)} {value}")
        return lines


class Histogram:
    def __init__(
        self,
        name: str,
        help_text: str,
        label_names: list[str] | None = None,
        buckets: tuple[float, ...] | None = None,
    ):
        self.name = name
        self.help_text = help_text
        self.label_names = tuple(label_names or [])
        self.buckets = list(buckets or (0.005, 0.01, 0.025, 0.05, 0.1, 0.5, 1, 5))
        self._values: dict[tuple[str, ...], HistogramState] = {}
        self._lock = Lock()

    def labels(self, **labels: str) -> HistogramChild:
        key = tuple(labels[label] for label in self.label_names)
        return HistogramChild(self, key)

    def observe(self, value: float) -> None:
        self._observe(tuple(), value)

    def _observe(self, key: tuple[str, ...], value: float) -> None:
        with self._lock:
            state = self._values.get(key)
            if state is None:
                state = HistogramState(
                    buckets=[0] * (len(self.buckets) + 1),
                    count=0,
                    total=0.0,
                )
                self._values[key] = state

            bucket_index = len(self.buckets)
            for index, upper_bound in enumerate(self.buckets):
                if value <= upper_bound:
                    bucket_index = index
                    break

            state.buckets[bucket_index] += 1
            state.count += 1
            state.total += value

    def render(self) -> list[str]:
        lines = [f"# HELP {self.name} {self.help_text}", f"# TYPE {self.name} histogram"]

        with self._lock:
            items = sorted(self._values.items())

        for key, state in items:
            cumulative = 0
            for upper_bound, bucket_count in zip(self.buckets, state.buckets[:-1], strict=True):
                cumulative += bucket_count
                label_names = self.label_names + ("le",)
                label_key = key + (str(upper_bound),)
                lines.append(
                    f"{self.name}_bucket{_render_labels(label_names, label_key)} {cumulative}"
                )

            cumulative += state.buckets[-1]
            inf_label_names = self.label_names + ("le",)
            inf_label_key = key + ("+Inf",)
            lines.append(
                f"{self.name}_bucket{_render_labels(inf_label_names, inf_label_key)} {cumulative}"
            )
            lines.append(
                f"{self.name}_count{_render_labels(self.label_names, key)} {state.count}"
            )
            lines.append(
                f"{self.name}_sum{_render_labels(self.label_names, key)} {state.total}"
            )

        return lines


HTTP_REQUESTS_TOTAL = Counter(
    "dossier_aggr_http_requests_total",
    "Total number of HTTP requests.",
    ["method", "route", "status_code"],
)

HTTP_REQUEST_DURATION_SECONDS = Histogram(
    "dossier_aggr_http_request_duration_seconds",
    "HTTP request latency in seconds.",
    ["method", "route", "status_code"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.3, 0.5, 1, 2, 5),
)

HTTP_REQUEST_SIZE_BYTES = Histogram(
    "dossier_aggr_http_request_size_bytes",
    "HTTP request payload size in bytes.",
    ["method", "route"],
    buckets=(128, 512, 1024, 4096, 16384, 65536, 262144, 1048576),
)

HTTP_RESPONSE_SIZE_BYTES = Histogram(
    "dossier_aggr_http_response_size_bytes",
    "HTTP response payload size in bytes.",
    ["method", "route", "status_code"],
    buckets=(128, 512, 1024, 4096, 16384, 65536, 262144, 1048576),
)

HTTP_IN_PROGRESS = Gauge(
    "dossier_aggr_http_in_progress_requests",
    "Current in-progress HTTP requests.",
)

ORM_QUERIES_TOTAL = Counter(
    "dossier_aggr_orm_queries_total",
    "Total ORM/SQL queries.",
    ["operation", "status"],
)

ORM_QUERY_DURATION_SECONDS = Histogram(
    "dossier_aggr_orm_query_duration_seconds",
    "ORM/SQL query duration in seconds.",
    ["operation", "status"],
    buckets=(0.0005, 0.001, 0.005, 0.01, 0.03, 0.05, 0.1, 0.3, 1),
)

ORM_ROWS_AFFECTED = Histogram(
    "dossier_aggr_orm_rows_affected",
    "Number of rows affected by ORM/SQL statements.",
    ["operation"],
    buckets=(0, 1, 2, 5, 10, 50, 100, 500, 1000),
)

LAYER_DURATION_SECONDS = Histogram(
    "dossier_aggr_layer_duration_seconds",
    "Execution duration by layer.",
    ["layer", "component", "operation", "status"],
    buckets=(0.0005, 0.001, 0.005, 0.01, 0.03, 0.05, 0.1, 0.3, 1, 3),
)

TASK_ENQUEUED_TOTAL = Counter(
    "dossier_aggr_task_enqueued_total",
    "Total task enqueue operations.",
    ["task_name", "status"],
)

TASK_ENQUEUE_DURATION_SECONDS = Histogram(
    "dossier_aggr_task_enqueue_duration_seconds",
    "Task enqueue latency in seconds.",
    ["task_name", "status"],
    buckets=(0.0005, 0.001, 0.005, 0.01, 0.03, 0.05, 0.1, 0.3, 1),
)

_METRICS = [
    HTTP_REQUESTS_TOTAL,
    HTTP_REQUEST_DURATION_SECONDS,
    HTTP_REQUEST_SIZE_BYTES,
    HTTP_RESPONSE_SIZE_BYTES,
    HTTP_IN_PROGRESS,
    ORM_QUERIES_TOTAL,
    ORM_QUERY_DURATION_SECONDS,
    ORM_ROWS_AFFECTED,
    LAYER_DURATION_SECONDS,
    TASK_ENQUEUED_TOTAL,
    TASK_ENQUEUE_DURATION_SECONDS,
]


def render_metrics() -> str:
    lines: list[str] = []
    for metric in _METRICS:
        lines.extend(metric.render())
    return "\n".join(lines) + "\n"
