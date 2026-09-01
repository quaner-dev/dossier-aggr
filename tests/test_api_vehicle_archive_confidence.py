import asyncio

from api.verify.vehicle_archive_confidence import vehicle_archive_confidence_verify
from domain.common import enums
from schemas import (
    VehicleArchive,
    VehicleArchiveList,
    VehicleArchiveListSchema,
)
from tests.type_helpers import as_service, dt, sample_sub_image_list


class _FakeVehicleArchiveConfidenceService:
    def __init__(self):
        self.called_with: list[VehicleArchive] | None = None

    async def verify_vehicle_archive_confidence(self, archives: list[VehicleArchive]):
        self.called_with = archives
        return archives


def test_vehicle_archive_confidence_returns_archive_list():
    async def _run():
        fake = _FakeVehicleArchiveConfidenceService()
        archives = [
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
        payload = VehicleArchiveListSchema(
            VehicleArchiveListObject=VehicleArchiveList(VehicleArchiveObject=archives)
        )
        res = await vehicle_archive_confidence_verify(
            data=payload,
            service=as_service(fake),
        )

        returned_archives = res.VehicleArchiveListObject.VehicleArchiveObject
        assert len(returned_archives) == 2
        assert returned_archives[0].ArchiveID == "VA-001"
        assert returned_archives[0].SubImageList.SubImageInfoObject[0].ImageID == "IMG-VA-001"
        assert fake.called_with is not None
        assert fake.called_with[0].ArchiveID == "VA-001"

    asyncio.run(_run())
