from collections.abc import Mapping, Sequence

from domain import ArchiveTask as ArchiveTaskData
from models import ArchiveTask
from repo.task.archive_task import (
    create_archive_tasks_repo,
    delete_archive_tasks_repo,
    list_archive_tasks_repo,
    update_archive_tasks_repo,
)
from services.model_conversion import to_table_models


class ArchiveTaskService:
    """编排 GA/T 2350 聚档任务业务链路。

    聚档任务属于低频控制数据，读写直接委托 repo。
    """

    async def list_archive_tasks(
        self,
        filters: Mapping[str, str] | None = None,
    ) -> list[ArchiveTask]:
        return list(await list_archive_tasks_repo(filters=filters))

    async def create_archive_tasks(
        self,
        tasks: Sequence[ArchiveTaskData],
    ) -> list[ArchiveTask]:
        return list(await create_archive_tasks_repo(tasks=to_table_models(ArchiveTask, tasks)))

    async def update_archive_tasks(
        self,
        tasks: Sequence[ArchiveTaskData],
    ) -> list[ArchiveTask]:
        return list(await update_archive_tasks_repo(tasks=to_table_models(ArchiveTask, tasks)))

    async def delete_archive_tasks(self, task_ids: list[str]) -> list[str]:
        return await delete_archive_tasks_repo(task_ids=task_ids)
