from collections.abc import Sequence

from models import ArchiveLibrary
from repo.library.archive_library import list_archive_libraries_repo
from tasks.library.archive_library import (
    create_archive_libraries_task,
    update_archive_libraries_task,
    delete_archive_libraries_task,
)
from services.task_dispatch import dispatch_and_wait


class ArchiveLibraryService:
    async def list_archive_libraries(
        self, filters: dict[str, str] | None = None
    ) -> Sequence[ArchiveLibrary]:
        return await list_archive_libraries_repo(filters=filters)

    async def create_archive_libraries(
        self, libraries: Sequence[ArchiveLibrary]
    ) -> Sequence[ArchiveLibrary]:
        return await dispatch_and_wait(
            create_archive_libraries_task,
            libraries=libraries,
        )

    async def update_archive_libraries(
        self, libraries: Sequence[ArchiveLibrary]
    ) -> Sequence[ArchiveLibrary]:
        return await dispatch_and_wait(
            update_archive_libraries_task,
            libraries=libraries,
        )

    async def delete_archive_libraries(self, library_ids: list[str]) -> list[str]:
        return await dispatch_and_wait(
            delete_archive_libraries_task,
            library_ids=library_ids,
        )
