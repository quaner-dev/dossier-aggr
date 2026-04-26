from collections.abc import Coroutine
from typing import TYPE_CHECKING, Any, ParamSpec, TypeVar, overload

from taskiq import AsyncTaskiqDecoratedTask
from taskiq.exceptions import TaskiqResultTimeoutError
from taskiq.result import TaskiqResult

if TYPE_CHECKING:
    from types import CoroutineType
else:
    # types.CoroutineType 只服务类型检查；运行时保持 collections.abc.Coroutine。
    CoroutineType = Coroutine


from core import exceptions
from core import settings

_FuncParams = ParamSpec("_FuncParams")
_ReturnType = TypeVar("_ReturnType")
_AwaitedReturnType = TypeVar("_AwaitedReturnType")


@overload
async def dispatch_and_wait(
    task: AsyncTaskiqDecoratedTask[
        _FuncParams,
        CoroutineType[Any, Any, _AwaitedReturnType],
    ],
    **kwargs: Any,
) -> _AwaitedReturnType: ...


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
    """投递 Taskiq 任务并等待任务返回值。

    Service 写路径统一通过该函数跨到 task 层，避免业务层绕过
    Taskiq 边界直接执行持久化写入。Taskiq 返回的错误和超时在这里
    转换为项目统一异常，路由层只处理协议响应包装。

    Args:
        task: 使用 broker 装饰的 Taskiq 任务函数。
        **kwargs: 传递给任务的关键字参数。

    Raises:
        TypeError: 传入对象不是 Taskiq 装饰任务。
        exceptions.TaskExecutionError: 任务等待结果超时。

    Returns:
        Taskiq 任务的原始返回值。
    """
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
