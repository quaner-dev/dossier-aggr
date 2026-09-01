import asyncio

from api.archive.archives import (
    archives_create,
    archives_delete,
    archives_query_sync,
    archives_update,
)
from domain.common import enums
from schemas import (
    Archive,
    ArchiveList,
    ArchiveListSchema,
    ArchiveQuery,
    ArchiveQuerySchema,
)
from tests.type_helpers import (
    as_service,
    as_status_list,
    dt,
    sample_feature_info_list,
    sample_sub_image_list,
)


class _FakeArchiveService:
    def __init__(self, archives: list[Archive]):
        self._archives = archives
        self.queried_with: ArchiveQuery | None = None
        self.created_with: list[Archive] | None = None
        self.updated_with: list[Archive] | None = None
        self.deleted_with: list[str] | None = None

    async def query_archives(self, query: ArchiveQuery):
        self.queried_with = query
        return self._archives

    async def create_archives(self, archives: list[Archive]):
        self.created_with = archives
        return archives

    async def update_archives(self, archives: list[Archive]):
        self.updated_with = archives
        return archives

    async def delete_archives(self, archive_ids: list[str]):
        self.deleted_with = archive_ids
        return archive_ids


def _sample_archives() -> list[Archive]:
    return [
        Archive(
            ArchiveID="A-001",
            ArchiveLibraryID="LIB-001",
            CreateTime=dt("20260101120000"),
            UpdateTime=dt("20260101120000"),
            SourceIDList=["PERSON-001", "FACE-001"],
            CenterFeatureList=sample_feature_info_list("a-001"),
            Similaritydegree=0.91,
            Confidence=0.82,
            SubImageList=sample_sub_image_list(
                "IMG-A-001", enums.ImageTypeEnum.PersonImage, "a-001"
            ),
        ),
        Archive(
            ArchiveID="A-002",
            ArchiveLibraryID="LIB-001",
            CreateTime=dt("20260102120000"),
            UpdateTime=dt("20260102120000"),
            SourceIDList=["PERSON-002"],
            CenterFeatureList=sample_feature_info_list("a-002"),
            Similaritydegree=0.92,
            Confidence=0.83,
            SubImageList=sample_sub_image_list(
                "IMG-A-002", enums.ImageTypeEnum.PersonImage, "a-002"
            ),
        ),
    ]


def test_archives_query_sync_returns_query_result_schema():
    async def _run():
        archives = _sample_archives()
        fake = _FakeArchiveService(archives)
        payload = ArchiveQuerySchema(
            ArchiveQueryObject=ArchiveQuery(
                QueryID="Q-A-001",
                RecordStartNo=0,
                PageRecordNum=10,
            )
        )

        res = await archives_query_sync(data=payload, service=as_service(fake))

        assert res.ArchiveQueryResultObject.QueryID == "Q-A-001"
        assert res.ArchiveQueryResultObject.TotalNum == 2
        assert (
            res.ArchiveQueryResultObject.ArchiveListObject.ArchiveObject[0].ArchiveID
            == "A-001"
        )
        assert (
            res.ArchiveQueryResultObject.ArchiveListObject.ArchiveObject[0]
            .SubImageList.SubImageInfoObject[0]
            .ImageID
            == "IMG-A-001"
        )
        assert fake.queried_with is not None
        assert fake.queried_with.QueryID == "Q-A-001"

    asyncio.run(_run())


def test_archives_create_update_delete_return_status_list():
    async def _run():
        archives = _sample_archives()
        fake = _FakeArchiveService(archives)
        payload = ArchiveListSchema(ArchiveListObject=ArchiveList(ArchiveObject=archives))

        create_res = await archives_create(data=payload, service=as_service(fake))
        update_res = await archives_update(data=payload, service=as_service(fake))
        delete_res = await archives_delete(
            archive_ids=["A-001", "A-002"], service=as_service(fake)
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
        assert create_status[0].StatusString == "已接收"
        assert create_status[0].Id == "A-001"
        assert len(update_status) == 2
        assert update_status[1].Id == "A-002"
        assert len(delete_status) == 2
        assert delete_status[0].Id == "A-001"

        assert fake.created_with is not None
        assert len(fake.created_with) == 2
        assert fake.updated_with is not None
        assert len(fake.updated_with) == 2
        assert fake.deleted_with == ["A-001", "A-002"]

    asyncio.run(_run())
