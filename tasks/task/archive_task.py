from collections.abc import Mapping, Sequence

from core import brokers
from models import ArchiveTask
from repo.task.archive_task import (
    create_archive_tasks_repo,
    delete_archive_tasks_repo,
    list_archive_tasks_repo,
    update_archive_tasks_repo,
)


async def list_archive_tasks_task(
    filters: Mapping[str, str] | None = None,
) -> Sequence[ArchiveTask]:
    return await list_archive_tasks_repo(filters=filters)


@brokers.broker.task
async def create_archive_tasks_task(
    tasks: Sequence[ArchiveTask],
) -> Sequence[ArchiveTask]:
    return await create_archive_tasks_repo(tasks=tasks)


@brokers.broker.task
async def update_archive_tasks_task(
    tasks: Sequence[ArchiveTask],
) -> Sequence[ArchiveTask]:
    return await update_archive_tasks_repo(tasks=tasks)


@brokers.broker.task
async def delete_archive_tasks_task(task_ids: list[str]) -> list[str]:
    return await delete_archive_tasks_repo(task_ids=task_ids)
