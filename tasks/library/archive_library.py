from collections.abc import Sequence

from core import brokers
from models import ArchiveLibrary
from repo.library.archive_library import (
    create_archive_libraries_repo,
    delete_archive_libraries_repo,
    list_archive_libraries_repo,
    update_archive_libraries_repo,
)


async def list_archive_libraries_task() -> Sequence[ArchiveLibrary]:
    return await list_archive_libraries_repo()


@brokers.broker.task
async def create_archive_libraries_task(
    libraries: Sequence[ArchiveLibrary],
) -> Sequence[ArchiveLibrary]:
    return await create_archive_libraries_repo(libraries=libraries)


@brokers.broker.task
async def update_archive_libraries_task(
    libraries: Sequence[ArchiveLibrary],
) -> Sequence[ArchiveLibrary]:
    return await update_archive_libraries_repo(libraries=libraries)


@brokers.broker.task
async def delete_archive_libraries_task(library_ids: list[str]) -> list[str]:
    return await delete_archive_libraries_repo(library_ids=library_ids)
