import asyncio

from api.vehicle.vehicle_archive import (
    vehicle_archives_create,
    vehicle_archives_delete,
    vehicle_archives_query_sync,
    vehicle_archives_update,
)
from models import (
    ArchiveQuery,
    ArchiveQuerySchema,
    VehicleArchive,
    VehicleArchiveList,
    VehicleArchiveListSchema,
)
from models.common import enums
from tests.type_helpers import as_service, as_status_list, dt, sample_sub_image_list


class _FakeVehicleArchiveService:
    def __init__(self, archives: list[VehicleArchive]):
        self._archives = archives
        self.created_with: list[VehicleArchive] | None = None
        self.updated_with: list[VehicleArchive] | None = None
        self.deleted_with: list[str] | None = None
        self.queried_with: ArchiveQuery | None = None

    async def query_vehicle_archives(self, query: ArchiveQuery):
        self.queried_with = query
        return self._archives

    async def create_vehicle_archives(self, archives: list[VehicleArchive]):
        self.created_with = archives
        return archives

    async def update_vehicle_archives(self, archives: list[VehicleArchive]):
        self.updated_with = archives
        return archives

    async def delete_vehicle_archives(self, archive_ids: list[str]):
        self.deleted_with = archive_ids
        return archive_ids


def _sample_vehicle_archives() -> list[VehicleArchive]:
    return [
        VehicleArchive(
            ArchiveID="VA-001",
            ArchiveLibraryID="LIB-001",
            PlateNo="A12345",
            PlateColor=enums.ColorTypeEnum.Blue,
            VehicleClass="K11",
            CreateTime=dt("20260101120000"),
            UpdateTime=dt("20260101120000"),
            SourceIDList=["MV-001"],
            SubImageList=sample_sub_image_list(
                "IMG-VA-001", enums.ImageTypeEnum.VehicleLargeImage, "va-001"
            ),
        ),
        VehicleArchive(
            ArchiveID="VA-002",
            ArchiveLibraryID="LIB-001",
            PlateNo="B12345",
            PlateColor=enums.ColorTypeEnum.White,
            VehicleClass="K11",
            CreateTime=dt("20260102120000"),
            UpdateTime=dt("20260102120000"),
            SourceIDList=["MV-002"],
            SubImageList=sample_sub_image_list(
                "IMG-VA-002", enums.ImageTypeEnum.VehicleLargeImage, "va-002"
            ),
        ),
    ]


def test_vehicle_archive_query_returns_query_result_schema():
    async def _run():
        archives = _sample_vehicle_archives()
        fake = _FakeVehicleArchiveService(archives)
        payload = ArchiveQuerySchema(
            ArchiveQueryObject=ArchiveQuery(
                QueryID="Q-VA-001",
                RecordStartNo=0,
                PageRecordNum=10,
            )
        )

        res = await vehicle_archives_query_sync(data=payload, service=as_service(fake))
        assert res.ArchiveQueryResultObject.QueryID == "Q-VA-001"
        assert (
            res.ArchiveQueryResultObject.VehicleArchiveListObject.VehicleArchiveObject[0].ArchiveID
            == "VA-001"
        )
        assert (
            res.ArchiveQueryResultObject.VehicleArchiveListObject.VehicleArchiveObject[0]
            .SubImageList.SubImageInfoObject[0]
            .ImageID
            == "IMG-VA-001"
        )
        assert (
            len(res.ArchiveQueryResultObject.VehicleArchiveListObject.VehicleArchiveObject)
            == 2
        )
        assert fake.queried_with is not None
        assert fake.queried_with.QueryID == "Q-VA-001"

    asyncio.run(_run())


def test_vehicle_archive_create_update_delete_return_status_list():
    async def _run():
        archives = _sample_vehicle_archives()
        fake = _FakeVehicleArchiveService(archives)
        payload = VehicleArchiveListSchema(
            VehicleArchiveListObject=VehicleArchiveList(VehicleArchiveObject=archives)
        )

        create_res = await vehicle_archives_create(data=payload, service=as_service(fake))
        update_res = await vehicle_archives_update(data=payload, service=as_service(fake))
        delete_res = await vehicle_archives_delete(
            archive_ids=["VA-001", "VA-002"],
            service=as_service(fake),
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
        assert create_status[0].Id == "VA-001"
        assert len(update_status) == 2
        assert update_status[1].Id == "VA-002"
        assert len(delete_status) == 2
        assert delete_status[0].Id == "VA-001"

        assert fake.created_with is not None
        assert len(fake.created_with) == 2
        assert fake.updated_with is not None
        assert len(fake.updated_with) == 2
        assert fake.deleted_with == ["VA-001", "VA-002"]

    asyncio.run(_run())
