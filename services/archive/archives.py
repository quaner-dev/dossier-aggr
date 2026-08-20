from models import Archive, ArchiveQuery
from repo.archive.archives import (
    create_archives_repo,
    delete_archives_repo,
    list_archives_repo,
    query_archives_repo,
    update_archives_repo,
)


class ArchiveService:
    """编排 GA/T 2350.5 A.9/A.10 人员档案业务链路。

    查询、创建、更新和删除统一委托 repo。
    """

    async def list_archives(self) -> list[Archive]:
        return list(await list_archives_repo())

    async def query_archives(self, query: ArchiveQuery) -> list[Archive]:
        return list(await query_archives_repo(query=query))

    async def create_archives(self, archives: list[Archive]) -> list[Archive]:
        return list(await create_archives_repo(archives=archives))

    async def update_archives(self, archives: list[Archive]) -> list[Archive]:
        return list(await update_archives_repo(archives=archives))

    async def delete_archives(self, archive_ids: list[str]) -> list[str]:
        return await delete_archives_repo(archive_ids=archive_ids)
