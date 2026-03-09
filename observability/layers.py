import functools
import inspect
import sys
from time import perf_counter
from types import ModuleType
from typing import Any, Callable

from taskiq import AsyncTaskiqDecoratedTask

from .metrics import LAYER_DURATION_SECONDS, TASK_ENQUEUE_DURATION_SECONDS, TASK_ENQUEUED_TOTAL

_INSTRUMENTED_ATTR = "_dossier_layer_instrumented"
_TASK_KIQ_INSTRUMENTED = False
_LAYER_INSTRUMENTED = False


def _component_from_module(module_name: str) -> str:
    return module_name.split(".", maxsplit=1)[-1]


def _replace_references(old_obj: Any, new_obj: Any) -> None:
    target_prefixes = ("services.", "tasks.", "repo.")
    for module_name, module in list(sys.modules.items()):
        if not module_name.startswith(target_prefixes):
            continue
        if not isinstance(module, ModuleType):
            continue
        for key, value in list(vars(module).items()):
            if value is old_obj:
                setattr(module, key, new_obj)


def _wrap_function(
    func: Callable[..., Any],
    layer: str,
    component: str,
    operation: str,
) -> Callable[..., Any]:
    if getattr(func, _INSTRUMENTED_ATTR, False):
        return func

    if inspect.iscoroutinefunction(func):

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            start = perf_counter()
            status = "ok"
            try:
                return await func(*args, **kwargs)
            except Exception:
                status = "error"
                raise
            finally:
                LAYER_DURATION_SECONDS.labels(
                    layer=layer,
                    component=component,
                    operation=operation,
                    status=status,
                ).observe(perf_counter() - start)

        setattr(async_wrapper, _INSTRUMENTED_ATTR, True)
        return async_wrapper

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = perf_counter()
        status = "ok"
        try:
            return func(*args, **kwargs)
        except Exception:
            status = "error"
            raise
        finally:
            LAYER_DURATION_SECONDS.labels(
                layer=layer,
                component=component,
                operation=operation,
                status=status,
            ).observe(perf_counter() - start)

    setattr(wrapper, _INSTRUMENTED_ATTR, True)
    return wrapper


def _instrument_service_layer() -> None:
    import services

    for export_name in getattr(services, "__all__", []):
        obj = getattr(services, export_name, None)
        if not inspect.isclass(obj):
            continue
        for method_name, method in list(vars(obj).items()):
            if method_name.startswith("_"):
                continue
            if not inspect.iscoroutinefunction(method):
                continue
            wrapped = _wrap_function(
                method,
                layer="service",
                component=export_name,
                operation=method_name,
            )
            setattr(obj, method_name, wrapped)


def _instrument_repository_layer() -> None:
    for module_name, module in list(sys.modules.items()):
        if not module_name.startswith("repo."):
            continue
        if not isinstance(module, ModuleType):
            continue

        component = _component_from_module(module_name)
        for attr_name, attr_value in list(vars(module).items()):
            if attr_name.startswith("_"):
                continue
            if not inspect.iscoroutinefunction(attr_value):
                continue

            wrapped = _wrap_function(
                attr_value,
                layer="repository",
                component=component,
                operation=attr_name,
            )
            setattr(module, attr_name, wrapped)
            _replace_references(old_obj=attr_value, new_obj=wrapped)


def _instrument_task_layer() -> None:
    for module_name, module in list(sys.modules.items()):
        if not module_name.startswith("tasks."):
            continue
        if not isinstance(module, ModuleType):
            continue

        component = _component_from_module(module_name)
        for attr_name, attr_value in list(vars(module).items()):
            if attr_name.startswith("_"):
                continue

            if isinstance(attr_value, AsyncTaskiqDecoratedTask):
                wrapped = _wrap_function(
                    attr_value.original_func,
                    layer="task",
                    component=component,
                    operation=attr_name,
                )
                attr_value.original_func = wrapped
                continue

            if inspect.iscoroutinefunction(attr_value):
                wrapped = _wrap_function(
                    attr_value,
                    layer="task",
                    component=component,
                    operation=attr_name,
                )
                setattr(module, attr_name, wrapped)
                _replace_references(old_obj=attr_value, new_obj=wrapped)


def _instrument_task_enqueue() -> None:
    global _TASK_KIQ_INSTRUMENTED
    if _TASK_KIQ_INSTRUMENTED:
        return

    original_kiq = AsyncTaskiqDecoratedTask.kiq

    @functools.wraps(original_kiq)
    async def kiq_wrapper(self, *args, **kwargs):  # type: ignore[no-untyped-def]
        start = perf_counter()
        status = "ok"
        try:
            return await original_kiq(self, *args, **kwargs)
        except Exception:
            status = "error"
            raise
        finally:
            TASK_ENQUEUED_TOTAL.labels(task_name=self.task_name, status=status).inc()
            TASK_ENQUEUE_DURATION_SECONDS.labels(
                task_name=self.task_name,
                status=status,
            ).observe(perf_counter() - start)

    AsyncTaskiqDecoratedTask.kiq = kiq_wrapper  # type: ignore[assignment]
    _TASK_KIQ_INSTRUMENTED = True


def instrument_layers() -> None:
    global _LAYER_INSTRUMENTED
    if _LAYER_INSTRUMENTED:
        return

    _instrument_service_layer()
    _instrument_repository_layer()
    _instrument_task_layer()
    _instrument_task_enqueue()
    _LAYER_INSTRUMENTED = True
