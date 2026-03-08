from models import ArchiveLibrary
from repositories.library.archive_library import list_archive_libraries_repo
from tasks.library.archive_library import (
    create_archive_libraries_task,
    update_archive_libraries_task,
    delete_archive_libraries_task,
)
from services.task_dispatch import dispatch_and_wait


class ArchiveLibraryService:
    async def list_archive_libraries(self) -> list[ArchiveLibrary]:
        return list(await list_archive_libraries_repo())

    async def create_archive_libraries(
        self, libraries: list[ArchiveLibrary]
    ) -> list[ArchiveLibrary]:
        return await dispatch_and_wait(
            create_archive_libraries_task,
            libraries=libraries,
        )

    async def update_archive_libraries(
        self, libraries: list[ArchiveLibrary]
    ) -> list[ArchiveLibrary]:
        return await dispatch_and_wait(
            update_archive_libraries_task,
            libraries=libraries,
        )

    async def delete_archive_libraries(self, library_ids: list[str]) -> list[str]:
        return await dispatch_and_wait(
            delete_archive_libraries_task,
            library_ids=library_ids,
        )
