import asyncio
from typing import get_overloads, get_type_hints

import pytest
from taskiq import AsyncBroker, AsyncTaskiqDecoratedTask
from taskiq.result import TaskiqResult

from services.task_dispatch import dispatch_and_wait


class _Broker(AsyncBroker):
    async def kick(self, message):
        return None

    async def listen(self):
        if False:
            yield b""


def test_dispatch_and_wait_rejects_non_taskiq_task():
    async def _run():
        class _FakeTask:
            task_name = "fake-task"

            async def kiq(self, **kwargs):
                return {"kwargs": kwargs}

        with pytest.raises(TypeError, match="AsyncTaskiqDecoratedTask"):
            await dispatch_and_wait(_FakeTask(), face_id="F-001")

    asyncio.run(_run())


def test_dispatch_and_wait_exposes_coroutine_unwrapping_overload():
    overloads = get_overloads(dispatch_and_wait)

    assert overloads, "dispatch_and_wait should expose typing overloads"

    overload_hints = [get_type_hints(overload) for overload in overloads]
    assert any(
        "Coroutine" in repr(hints["task"]) and "Coroutine" not in repr(hints["return"])
        for hints in overload_hints
    ), "dispatch_and_wait should unwrap coroutine task return types"


def test_dispatch_and_wait_requires_standard_submitted_task():
    async def _run():
        async def _sample_task(face_id: str):
            return face_id

        task = AsyncTaskiqDecoratedTask(
            broker=_Broker(),
            task_name="sample-task",
            original_func=_sample_task,
            labels={},
            return_type=str,
        )

        class _SubmittedWithoutWaitResult:
            pass

        async def fake_kiq(**kwargs):
            return _SubmittedWithoutWaitResult()

        task.kiq = fake_kiq  # type: ignore[method-assign]

        with pytest.raises(AttributeError, match="wait_result"):
            await dispatch_and_wait(task, face_id="F-001")

    asyncio.run(_run())


def test_dispatch_and_wait_returns_task_return_value():
    async def _run():
        async def _sample_task(face_id: str):
            return face_id

        task = AsyncTaskiqDecoratedTask(
            broker=_Broker(),
            task_name="sample-task",
            original_func=_sample_task,
            labels={},
            return_type=str,
        )

        class _SubmittedTask:
            async def wait_result(self, timeout: float):
                assert timeout > 0
                return TaskiqResult(
                    is_err=False,
                    return_value="F-001",
                    execution_time=0.01,
                )

        async def fake_kiq(**kwargs):
            assert kwargs == {"face_id": "F-001"}
            return _SubmittedTask()

        task.kiq = fake_kiq  # type: ignore[method-assign]

        result = await dispatch_and_wait(task, face_id="F-001")

        assert result == "F-001"

    asyncio.run(_run())


def test_dispatch_and_wait_rejects_sync_wait_result():
    async def _run():
        async def _sample_task(face_id: str):
            return face_id

        task = AsyncTaskiqDecoratedTask(
            broker=_Broker(),
            task_name="sample-task",
            original_func=_sample_task,
            labels={},
            return_type=str,
        )

        class _SubmittedTask:
            def wait_result(self, timeout: float):
                assert timeout > 0
                return TaskiqResult(
                    is_err=False,
                    return_value="F-001",
                    execution_time=0.01,
                )

        async def fake_kiq(**kwargs):
            assert kwargs == {"face_id": "F-001"}
            return _SubmittedTask()

        task.kiq = fake_kiq  # type: ignore[method-assign]

        with pytest.raises(TypeError, match="await"):
            await dispatch_and_wait(task, face_id="F-001")

    asyncio.run(_run())
