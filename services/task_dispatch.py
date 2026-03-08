import inspect
from typing import Any, cast

from taskiq.exceptions import TaskiqResultTimeoutError

import exceptions
import settings

async def dispatch_and_wait(
    task: Any,
    **kwargs: Any,
) -> Any:
    submitted = await cast(Any, task).kiq(**kwargs)

    wait_result = getattr(submitted, "wait_result", None)
    if not callable(wait_result):
        # Unit tests may inject lightweight fake tasks that only validate `kiq` args.
        return submitted

    try:
        waited = wait_result(timeout=settings.TASK_RESULT_TIMEOUT_SECONDS)
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
