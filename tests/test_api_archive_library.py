import asyncio

from api.library.archive_library import (
    archive_library_query_sync_read,
    archive_library_create,
    archive_library_update,
    archive_library_delete,
)
from models import (
    ArchiveLibrary,
    ArchiveLibraryList,
    ArchiveLibraryListSchema,
)
from tests.type_helpers import as_service, as_status_list, dt


class _FakeArchiveLibraryService:
    def __init__(self, libraries: list[ArchiveLibrary]):
        self._libraries = libraries
        self.created_with: list[ArchiveLibrary] | None = None
        self.updated_with: list[ArchiveLibrary] | None = None
        self.deleted_with: list[str] | None = None

    async def list_archive_libraries(self):
        return self._libraries

    async def create_archive_libraries(self, libraries: list[ArchiveLibrary]):
        self.created_with = libraries
        return libraries

    async def update_archive_libraries(self, libraries: list[ArchiveLibrary]):
        self.updated_with = libraries
        return libraries

    async def delete_archive_libraries(self, library_ids: list[str]):
        self.deleted_with = library_ids
        return library_ids


def _sample_libraries() -> list[ArchiveLibrary]:
    return [
        ArchiveLibrary(
            ArchiveLibraryID="LIB-001",
            Name="Lib-1",
            CreateTime=dt("20260101120000"),
            Memo="primary",
        ),
        ArchiveLibrary(
            ArchiveLibraryID="LIB-002",
            Name="Lib-2",
            CreateTime=dt("20260102120000"),
            Memo=None,
        ),
    ]


def test_archive_library_query_sync_read_returns_list_schema():
    async def _run():
        libraries = _sample_libraries()
        fake = _FakeArchiveLibraryService(libraries)

        res = await archive_library_query_sync_read(service=as_service(fake))

        assert res.ArchiveLibraryListObject.ArchiveLibraryObject[0].ArchiveLibraryID == "LIB-001"
        assert len(res.ArchiveLibraryListObject.ArchiveLibraryObject) == 2

    asyncio.run(_run())


def test_archive_library_create_update_delete_return_status_list():
    async def _run():
        libraries = _sample_libraries()
        fake = _FakeArchiveLibraryService(libraries)
        payload = ArchiveLibraryListSchema(
            ArchiveLibraryListObject=ArchiveLibraryList(ArchiveLibraryObject=libraries)
        )

        create_res = await archive_library_create(data=payload, service=as_service(fake))
        update_res = await archive_library_update(data=payload, service=as_service(fake))
        delete_res = await archive_library_delete(
            id_list=["LIB-001", "LIB-002"], service=as_service(fake)
        )

        create_status = as_status_list(
            create_res.ResponseStatusListObject.ResponseStatusObject
        )
        update_status = as_status_list(
            update_res.ResponseStatusListObject.ResponseStatusObject
        )
        delete_status = as_status_list(
            delete_res.ResponseStatusListObject.ResponseStatusObject
        )

        assert len(create_status) == 2
        assert create_status[0].StatusCode == "0"
        assert create_status[0].Id == "LIB-001"
        assert len(update_status) == 2
        assert update_status[1].Id == "LIB-002"
        assert len(delete_status) == 2
        assert delete_status[0].Id == "LIB-001"

        assert fake.created_with is not None
        assert len(fake.created_with) == 2
        assert fake.updated_with is not None
        assert len(fake.updated_with) == 2
        assert fake.deleted_with == ["LIB-001", "LIB-002"]

    asyncio.run(_run())
