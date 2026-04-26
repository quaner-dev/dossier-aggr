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
    """编排 GA/T 2350 聚档任务业务链路。

    任务列表过滤由 repo 解释；任务创建、更新和删除经 Taskiq task
    写入，避免 service 层直接依赖数据库会话。
    """

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
