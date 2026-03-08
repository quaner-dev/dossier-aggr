from models import Archive
from repositories.archive.archives import list_archives_repo
from tasks.archive.archives import (
    create_archives_task,
    update_archives_task,
    delete_archives_task,
)
from services.task_dispatch import dispatch_and_wait


class ArchiveService:
    async def list_archives(self) -> list[Archive]:
        return list(await list_archives_repo())

    async def create_archives(self, archives: list[Archive]) -> list[Archive]:
        return await dispatch_and_wait(create_archives_task, archives=archives)

    async def update_archives(self, archives: list[Archive]) -> list[Archive]:
        return await dispatch_and_wait(update_archives_task, archives=archives)

    async def delete_archives(self, archive_ids: list[str]) -> list[str]:
        return await dispatch_and_wait(delete_archives_task, archive_ids=archive_ids)
