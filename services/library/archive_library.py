from collections.abc import Sequence

from domain import ArchiveLibrary as ArchiveLibraryData
from models import ArchiveLibrary
from repo.library.archive_library import (
    create_archive_libraries_repo,
    delete_archive_libraries_repo,
    list_archive_libraries_repo,
    update_archive_libraries_repo,
)
from services.model_conversion import to_table_models


class ArchiveLibraryService:
    """编排 GA/T 2350 目标档案库业务链路。

    档案库是低频控制数据，查询和写入均直接委托 repo。
    """

    async def list_archive_libraries(
        self, filters: dict[str, str] | None = None
    ) -> list[ArchiveLibrary]:
        return list(await list_archive_libraries_repo(filters=filters))

    async def create_archive_libraries(
        self, libraries: Sequence[ArchiveLibraryData]
    ) -> list[ArchiveLibrary]:
        return list(await create_archive_libraries_repo(libraries=to_table_models(ArchiveLibrary, libraries)))

    async def update_archive_libraries(
        self, libraries: Sequence[ArchiveLibraryData]
    ) -> list[ArchiveLibrary]:
        return list(await update_archive_libraries_repo(libraries=to_table_models(ArchiveLibrary, libraries)))

    async def delete_archive_libraries(self, library_ids: list[str]) -> list[str]:
        return await delete_archive_libraries_repo(library_ids=library_ids)
