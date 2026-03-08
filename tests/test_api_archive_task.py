import asyncio

from api.task.archive_task import (
    archive_tasks_query,
    archive_tasks_create,
    archive_tasks_update,
    archive_tasks_delete,
)
from models.task.archive_task import ArchiveTask, ArchiveTaskList, ArchiveTaskListSchema
from tests.type_helpers import as_service, as_status_list, dt


class _FakeArchiveTaskService:
    def __init__(self, tasks: list[ArchiveTask]):
        self._tasks = tasks
        self.created_with: list[ArchiveTask] | None = None
        self.updated_with: list[ArchiveTask] | None = None
        self.deleted_with: list[str] | None = None

    async def list_archive_tasks(self):
        return self._tasks

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
            TaskID="T-001",
            TaskName="collect-1",
            ArchiveLibraryID="LIB-001",
            EventType="1",
            Status="Active",
            CreateTime=dt("20260101120000"),
            UpdateTime=dt("20260101120000"),
        ),
        ArchiveTask(
            TaskID="T-002",
            TaskName="collect-2",
            ArchiveLibraryID="LIB-001",
            EventType="2",
            Status="Inactive",
            CreateTime=dt("20260102120000"),
            UpdateTime=dt("20260102120000"),
        ),
    ]


def test_archive_task_query_returns_list_schema():
    async def _run():
        tasks = _sample_tasks()
        fake = _FakeArchiveTaskService(tasks)

        res = await archive_tasks_query(service=as_service(fake))
        assert res.ArchiveTaskListObject.ArchiveTaskObject[0].TaskID == "T-001"
        assert len(res.ArchiveTaskListObject.ArchiveTaskObject) == 2

    asyncio.run(_run())


def test_archive_task_create_update_delete_return_status_list():
    async def _run():
        tasks = _sample_tasks()
        fake = _FakeArchiveTaskService(tasks)
        payload = ArchiveTaskListSchema(
            ArchiveTaskListObject=ArchiveTaskList(ArchiveTaskObject=tasks)
        )

        create_res = await archive_tasks_create(data=payload, service=as_service(fake))
        update_res = await archive_tasks_update(data=payload, service=as_service(fake))
        delete_res = await archive_tasks_delete(
            task_ids=["T-001", "T-002"], service=as_service(fake)
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
        assert create_status[0].Id == "T-001"
        assert len(update_status) == 2
        assert update_status[1].Id == "T-002"
        assert len(delete_status) == 2
        assert delete_status[0].Id == "T-001"

        assert fake.created_with is not None
        assert len(fake.created_with) == 2
        assert fake.updated_with is not None
        assert len(fake.updated_with) == 2
        assert fake.deleted_with == ["T-001", "T-002"]

    asyncio.run(_run())
