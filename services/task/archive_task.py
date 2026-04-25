from collections.abc import Mapping, Sequence

from models import ArchiveTask
from repo.task.archive_task import list_archive_tasks_repo
from services.task_dispatch import dispatch_and_wait
from tasks.task.archive_task import (
    create_archive_tasks_task,
    delete_archive_tasks_task,
    update_archive_tasks_task,
)


class ArchiveTaskService:
    async def list_archive_tasks(
        self,
        filters: Mapping[str, str] | None = None,
    ) -> Sequence[ArchiveTask]:
        return await list_archive_tasks_repo(filters=filters)

    async def create_archive_tasks(
        self,
        tasks: Sequence[ArchiveTask],
    ) -> Sequence[ArchiveTask]:
        return await dispatch_and_wait(create_archive_tasks_task, tasks=tasks)

    async def update_archive_tasks(
        self,
        tasks: Sequence[ArchiveTask],
    ) -> Sequence[ArchiveTask]:
        return await dispatch_and_wait(update_archive_tasks_task, tasks=tasks)

    async def delete_archive_tasks(self, task_ids: list[str]) -> list[str]:
        return await dispatch_and_wait(delete_archive_tasks_task, task_ids=task_ids)
