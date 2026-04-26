from models import Archive, ArchiveQuery
from repo.archive.archives import list_archives_repo, query_archives_repo
from tasks.archive.archives import (
    create_archives_task,
    update_archives_task,
    delete_archives_task,
)
from services.task_dispatch import dispatch_and_wait


class ArchiveService:
    """编排 GA/T 2350.5 A.9/A.10 人员档案业务链路。

    同步查询直接委托 repo 保留查询语义；新增、更新和删除通过
    Taskiq task 写入，保持 `api -> services -> tasks -> repo` 的写路径边界。
    """

    async def list_archives(self) -> list[Archive]:
        return list(await list_archives_repo())

    async def query_archives(self, query: ArchiveQuery) -> list[Archive]:
        return list(await query_archives_repo(query=query))

    async def create_archives(self, archives: list[Archive]) -> list[Archive]:
        return list(await dispatch_and_wait(create_archives_task, archives=archives))

    async def update_archives(self, archives: list[Archive]) -> list[Archive]:
        return list(await dispatch_and_wait(update_archives_task, archives=archives))

    async def delete_archives(self, archive_ids: list[str]) -> list[str]:
        return await dispatch_and_wait(delete_archives_task, archive_ids=archive_ids)
