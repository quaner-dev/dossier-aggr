from time import perf_counter

from sqlalchemy import event
from sqlalchemy.engine import Engine

from .metrics import ORM_QUERIES_TOTAL, ORM_QUERY_DURATION_SECONDS, ORM_ROWS_AFFECTED

_ORM_HOOK_INSTALLED_ATTR = "_dossier_orm_metrics_installed"
_QUERY_TIMER_STACK_KEY = "_dossier_query_timer_stack"


def _sql_operation(statement: str | None) -> str:
    if not statement:
        return "UNKNOWN"
    token = statement.strip().split(maxsplit=1)
    if not token:
        return "UNKNOWN"
    operation = token[0].upper()
    if operation in {"SELECT", "INSERT", "UPDATE", "DELETE"}:
        return operation
    return "OTHER"


def instrument_sqlalchemy(sync_engine: Engine) -> None:
    if getattr(sync_engine, _ORM_HOOK_INSTALLED_ATTR, False):
        return

    @event.listens_for(sync_engine, "before_cursor_execute")
    def before_cursor_execute(  # type: ignore[no-untyped-def]
        conn,
        cursor,
        statement,
        parameters,
        context,
        executemany,
    ):
        stack = conn.info.setdefault(_QUERY_TIMER_STACK_KEY, [])
        stack.append((perf_counter(), _sql_operation(statement)))

    @event.listens_for(sync_engine, "after_cursor_execute")
    def after_cursor_execute(  # type: ignore[no-untyped-def]
        conn,
        cursor,
        statement,
        parameters,
        context,
        executemany,
    ):
        stack = conn.info.get(_QUERY_TIMER_STACK_KEY, [])
        if stack:
            start, operation = stack.pop()
        else:
            start, operation = perf_counter(), _sql_operation(statement)

        duration = perf_counter() - start
        ORM_QUERIES_TOTAL.labels(operation=operation, status="ok").inc()
        ORM_QUERY_DURATION_SECONDS.labels(operation=operation, status="ok").observe(
            duration
        )

        rowcount = getattr(cursor, "rowcount", None)
        if isinstance(rowcount, int) and rowcount >= 0:
            ORM_ROWS_AFFECTED.labels(operation=operation).observe(float(rowcount))

    @event.listens_for(sync_engine, "handle_error")
    def handle_error(exception_context):  # type: ignore[no-untyped-def]
        operation = _sql_operation(exception_context.statement)
        ORM_QUERIES_TOTAL.labels(operation=operation, status="error").inc()

    setattr(sync_engine, _ORM_HOOK_INSTALLED_ATTR, True)
