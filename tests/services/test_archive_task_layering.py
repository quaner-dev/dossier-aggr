import asyncio

from models import ArchiveTask
from services.task.archive_task import ArchiveTaskService
import services.task.archive_task as archive_task_service_module
import tasks.task.archive_task as archive_task_module
from tests.type_helpers import dt


def _sample_task() -> ArchiveTask:
    return ArchiveTask(
        TaskID="TASK-LAYER-001",
        TaskName="Layer Task",
        ArchiveLibraryID="LIB-LAYER-001",
        EventType="1",
        Status="created",
        CreateTime=dt("20260101120000"),
        UpdateTime=dt("20260101120000"),
    )


def test_archive_task_service_read_uses_repository(monkeypatch):
    async def _run():
        task = _sample_task()
        called = {"repo": False}

        async def fake_list_archive_tasks_repo(filters: dict[str, str] | None = None):
            called["repo"] = True
            assert filters == {"TaskID": "TASK-LAYER-001"}
            return [task]

        monkeypatch.setattr(
            archive_task_service_module,
            "list_archive_tasks_repo",
            fake_list_archive_tasks_repo,
            raising=False,
        )

        res = await ArchiveTaskService().list_archive_tasks(
            {"TaskID": "TASK-LAYER-001"}
        )

        assert res[0].TaskID == "TASK-LAYER-001"
        assert called["repo"] is True

    asyncio.run(_run())


def test_archive_task_service_writes_use_dispatch(monkeypatch):
    async def _run():
        task = _sample_task()
        called = {"dispatch": False}

        async def fake_dispatch(task_func, **kwargs):
            called["dispatch"] = True
            assert task_func is archive_task_service_module.create_archive_tasks_task
            assert kwargs == {"tasks": [task]}
            return [task]

        monkeypatch.setattr(
            archive_task_service_module,
            "dispatch_and_wait",
            fake_dispatch,
            raising=False,
        )

        res = await ArchiveTaskService().create_archive_tasks([task])

        assert res[0].TaskID == "TASK-LAYER-001"
        assert called["dispatch"] is True

    asyncio.run(_run())


def test_archive_task_tasks_delegate_to_repositories(monkeypatch):
    async def _run():
        task = _sample_task()
        called = {
            "list_repo": False,
            "create_repo": False,
            "update_repo": False,
            "delete_repo": False,
        }

        async def fake_list_archive_tasks_repo(filters: dict[str, str] | None = None):
            called["list_repo"] = True
            assert filters == {"TaskID": "TASK-LAYER-001"}
            return [task]

        async def fake_create_archive_tasks_repo(tasks: list[ArchiveTask]):
            called["create_repo"] = True
            assert tasks == [task]
            return tasks

        async def fake_update_archive_tasks_repo(tasks: list[ArchiveTask]):
            called["update_repo"] = True
            assert tasks == [task]
            return tasks

        async def fake_delete_archive_tasks_repo(task_ids: list[str]):
            called["delete_repo"] = True
            assert task_ids == ["TASK-LAYER-001"]
            return task_ids

        monkeypatch.setattr(
            archive_task_module,
            "list_archive_tasks_repo",
            fake_list_archive_tasks_repo,
            raising=False,
        )
        monkeypatch.setattr(
            archive_task_module,
            "create_archive_tasks_repo",
            fake_create_archive_tasks_repo,
            raising=False,
        )
        monkeypatch.setattr(
            archive_task_module,
            "update_archive_tasks_repo",
            fake_update_archive_tasks_repo,
            raising=False,
        )
        monkeypatch.setattr(
            archive_task_module,
            "delete_archive_tasks_repo",
            fake_delete_archive_tasks_repo,
            raising=False,
        )

        list_res = await archive_task_module.list_archive_tasks_task(
            {"TaskID": "TASK-LAYER-001"}
        )
        create_res = await archive_task_module.create_archive_tasks_task.original_func(
            [task]
        )
        update_res = await archive_task_module.update_archive_tasks_task.original_func(
            [task]
        )
        delete_res = await archive_task_module.delete_archive_tasks_task.original_func(
            ["TASK-LAYER-001"]
        )

        assert list_res[0].TaskID == "TASK-LAYER-001"
        assert create_res[0].TaskID == "TASK-LAYER-001"
        assert update_res[0].TaskID == "TASK-LAYER-001"
        assert delete_res == ["TASK-LAYER-001"]
        assert all(called.values())

    asyncio.run(_run())
