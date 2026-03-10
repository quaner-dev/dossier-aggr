import inspect
from typing import Any, cast

from taskiq import AsyncTaskiqDecoratedTask
from taskiq.exceptions import TaskiqResultTimeoutError

from core import exceptions
from core import settings


async def dispatch_and_wait(
    task: AsyncTaskiqDecoratedTask[Any, Any],
    **kwargs: Any,
) -> Any:
    if not isinstance(task, AsyncTaskiqDecoratedTask):
        raise TypeError("dispatch_and_wait expects an AsyncTaskiqDecoratedTask")

    submitted = await task.kiq(**kwargs)

    try:
        waited = submitted.wait_result(timeout=settings.TASK_RESULT_TIMEOUT_SECONDS)
        result = await waited if inspect.isawaitable(waited) else waited
    except TaskiqResultTimeoutError as exc:
        raise exceptions.TaskExecutionError(
            detail=(
                f"Task {task.task_name} timed out after "
                f"{settings.TASK_RESULT_TIMEOUT_SECONDS}s"
            )
        ) from exc

    result_obj = cast(Any, result)
    result_obj.raise_for_error()
    return result_obj.return_value
