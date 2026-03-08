from models.task.archive_task import ArchiveTask
from repositories.task.archive_task import list_archive_tasks_repo
from tasks.task.archive_task import (
    create_archive_tasks_task,
    update_archive_tasks_task,
    delete_archive_tasks_task,
)
from services.task_dispatch import dispatch_and_wait


class ArchiveTaskService:
    async def list_archive_tasks(self) -> list[ArchiveTask]:
        return list(await list_archive_tasks_repo())

    async def create_archive_tasks(self, tasks: list[ArchiveTask]) -> list[ArchiveTask]:
        return await dispatch_and_wait(create_archive_tasks_task, tasks=tasks)

    async def update_archive_tasks(self, tasks: list[ArchiveTask]) -> list[ArchiveTask]:
        return await dispatch_and_wait(update_archive_tasks_task, tasks=tasks)

    async def delete_archive_tasks(self, task_ids: list[str]) -> list[str]:
        return await dispatch_and_wait(delete_archive_tasks_task, task_ids=task_ids)
