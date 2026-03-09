from collections.abc import Sequence

import brokers
from models import Archive
from repo.archive.archives import (
    create_archives_repo,
    delete_archives_repo,
    list_archives_repo,
    update_archives_repo,
)


async def list_archives_task() -> Sequence[Archive]:
    return await list_archives_repo()


@brokers.broker.task
async def create_archives_task(archives: list[Archive]) -> Sequence[Archive]:
    return await create_archives_repo(archives=archives)


@brokers.broker.task
async def update_archives_task(archives: list[Archive]) -> Sequence[Archive]:
    return await update_archives_repo(archives=archives)


@brokers.broker.task
async def delete_archives_task(archive_ids: list[str]) -> list[str]:
    return await delete_archives_repo(archive_ids=archive_ids)
