from collections.abc import Coroutine
from typing import Any, ParamSpec, TypeVar, overload

from taskiq import AsyncTaskiqDecoratedTask
from taskiq.exceptions import TaskiqResultTimeoutError
from taskiq.result import TaskiqResult


from core import exceptions
from core import settings

_FuncParams = ParamSpec("_FuncParams")
_ReturnType = TypeVar("_ReturnType")
_AwaitedReturnType = TypeVar("_AwaitedReturnType")


@overload
async def dispatch_and_wait(
    task: AsyncTaskiqDecoratedTask[
        _FuncParams,
        Coroutine[Any, Any, _AwaitedReturnType],
    ],
    **kwargs: Any,
) -> _AwaitedReturnType: ...


@overload
async def dispatch_and_wait(
    task: AsyncTaskiqDecoratedTask[_FuncParams, _ReturnType],
    **kwargs: Any,
) -> _ReturnType: ...


async def dispatch_and_wait(
    task: AsyncTaskiqDecoratedTask[Any, Any],
    **kwargs: Any,
) -> Any:
    if not isinstance(task, AsyncTaskiqDecoratedTask):
        raise TypeError("dispatch_and_wait expects an AsyncTaskiqDecoratedTask")

    submitted = await task.kiq(**kwargs)

    try:
        task_result: TaskiqResult[Any] = await submitted.wait_result(
            timeout=settings.TASK_RESULT_TIMEOUT_SECONDS
        )
    except TaskiqResultTimeoutError as exc:
        raise exceptions.TaskExecutionError(
            detail=(
                f"Task {task.task_name} timed out after "
                f"{settings.TASK_RESULT_TIMEOUT_SECONDS}s"
            )
        ) from exc

    task_result.raise_for_error()
    return task_result.return_value
