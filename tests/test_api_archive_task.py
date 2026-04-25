import asyncio
from types import SimpleNamespace

from api.task.archive_task import (
    archive_tasks_create,
    archive_tasks_delete,
    archive_tasks_query,
    archive_tasks_update,
)
from models import ArchiveTask, ArchiveTaskList, ArchiveTaskListSchema
from tests.type_helpers import as_service, as_status_list, dt


class _FakeArchiveTaskService:
    def __init__(self, tasks: list[ArchiveTask]):
        self._tasks = tasks
        self.created_with: list[ArchiveTask] | None = None
        self.updated_with: list[ArchiveTask] | None = None
        self.deleted_with: list[str] | None = None
        self.query_filters: dict[str, str] | None = None

    async def list_archive_tasks(self, filters: dict[str, str] | None = None):
        self.query_filters = filters or {}
        if not filters:
            return self._tasks
        return [
            task
            for task in self._tasks
            if all(str(getattr(task, field)) == value for field, value in filters.items())
        ]

    async def create_archive_tasks(self, tasks: list[ArchiveTask]):
        self.created_with = tasks
        return tasks

    async def update_archive_tasks(self, tasks: list[ArchiveTask]):
        self.updated_with = tasks
        return tasks

    async def delete_archive_tasks(self, task_ids: list[str]):
        self.deleted_with = task_ids
        return task_ids


def _sample_tasks() -> list[ArchiveTask]:
    return [
        ArchiveTask(
            TaskID="TASK-001",
            TaskName="Task 1",
            ArchiveLibraryID="LIB-001",
            EventType="1",
            Status="created",
            CreateTime=dt("20260101120000"),
            UpdateTime=dt("20260101120000"),
        ),
        ArchiveTask(
            TaskID="TASK-002",
            TaskName="Task 2",
            ArchiveLibraryID="LIB-002",
            EventType="2",
            Status="running",
            CreateTime=dt("20260102120000"),
            UpdateTime=dt("20260102120000"),
        ),
    ]


def test_archive_tasks_query_returns_list_schema():
    async def _run():
        tasks = _sample_tasks()
        fake = _FakeArchiveTaskService(tasks)
        request = SimpleNamespace(query_params={"TaskID": "TASK-001"})

        res = await archive_tasks_query(request=request, service=as_service(fake))

        assert res.ArchiveTaskListObject.ArchiveTaskObject[0].TaskID == "TASK-001"
        assert len(res.ArchiveTaskListObject.ArchiveTaskObject) == 1
        assert fake.query_filters == {"TaskID": "TASK-001"}

    asyncio.run(_run())


def test_archive_tasks_create_update_delete_return_status_list():
    async def _run():
        tasks = _sample_tasks()
        fake = _FakeArchiveTaskService(tasks)
        payload = ArchiveTaskListSchema(
            ArchiveTaskListObject=ArchiveTaskList(ArchiveTaskObject=tasks)
        )

        create_res = await archive_tasks_create(data=payload, service=as_service(fake))
        update_res = await archive_tasks_update(data=payload, service=as_service(fake))
        delete_res = await archive_tasks_delete(
            task_ids=["TASK-001", "TASK-002"],
            service=as_service(fake),
        )

        create_status = as_status_list(
            create_res.ResponseStatusListObject.ResponseStatusObject
        )
        update_status = as_status_list(
            update_res.ResponseStatusListObject.ResponseStatusObject
        )
        delete_status = as_status_list(
            delete_res.ResponseStatusListObject.ResponseStatusObject
        )

        assert len(create_status) == 2
        assert create_status[0].StatusCode == "0"
        assert create_status[0].Id == "TASK-001"
        assert len(update_status) == 2
        assert update_status[1].Id == "TASK-002"
        assert len(delete_status) == 2
        assert delete_status[0].Id == "TASK-001"

        assert fake.created_with is not None
        assert len(fake.created_with) == 2
        assert fake.updated_with is not None
        assert len(fake.updated_with) == 2
        assert fake.deleted_with == ["TASK-001", "TASK-002"]

    asyncio.run(_run())
