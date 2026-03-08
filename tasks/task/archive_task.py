from collections.abc import Sequence

import brokers
from models.task.archive_task import ArchiveTask
from repositories.task.archive_task import (
    create_archive_tasks_repo,
    delete_archive_tasks_repo,
    list_archive_tasks_repo,
    update_archive_tasks_repo,
)


async def list_archive_tasks_task() -> Sequence[ArchiveTask]:
    return await list_archive_tasks_repo()


@brokers.broker.task
async def create_archive_tasks_task(tasks: list[ArchiveTask]) -> Sequence[ArchiveTask]:
    return await create_archive_tasks_repo(tasks=tasks)


@brokers.broker.task
async def update_archive_tasks_task(tasks: list[ArchiveTask]) -> Sequence[ArchiveTask]:
    return await update_archive_tasks_repo(tasks=tasks)


@brokers.broker.task
async def delete_archive_tasks_task(task_ids: list[str]) -> list[str]:
    return await delete_archive_tasks_repo(task_ids=task_ids)
