import asyncio

from api.vehicle.vehicle_archive_subject import (
    vehicle_archive_subject_query_sync_read,
    vehicle_archive_subjects_create,
    vehicle_archive_subjects_update,
    vehicle_archive_subjects_delete,
)
from models import (
    VehicleArchiveSubject,
    VehicleArchiveSubjectList,
    VehicleArchiveSubjectSchema,
)
from tests.type_helpers import as_service, as_status_list


class _FakeVehicleArchiveSubjectService:
    def __init__(self, subjects: list[VehicleArchiveSubject]):
        self._subjects = subjects
        self.created_with: list[VehicleArchiveSubject] | None = None
        self.updated_with: list[VehicleArchiveSubject] | None = None
        self.deleted_with: list[str] | None = None

    async def query_vehicle_archive_subjects(self):
        return self._subjects

    async def create_vehicle_archive_subjects(self, subjects: list[VehicleArchiveSubject]):
        self.created_with = subjects
        return subjects

    async def update_vehicle_archive_subjects(self, subjects: list[VehicleArchiveSubject]):
        self.updated_with = subjects
        return subjects

    async def delete_vehicle_archive_subjects(self, archive_ids: list[str]):
        self.deleted_with = archive_ids
        return archive_ids


def _sample_vehicle_archive_subjects() -> list[VehicleArchiveSubject]:
    return [
        VehicleArchiveSubject(
            ArchiveID="VS-001",
            MotorVehicleIDList=["MV-001"],
            NonMotorVehicleIDList=None,
            ImageID="IMG-VS-001",
        ),
        VehicleArchiveSubject(
            ArchiveID="VS-002",
            MotorVehicleIDList=["MV-002"],
            NonMotorVehicleIDList=["NMV-002"],
            ImageID="IMG-VS-002",
        ),
    ]


def test_vehicle_archive_subject_query_returns_schema():
    async def _run():
        subjects = _sample_vehicle_archive_subjects()
        fake = _FakeVehicleArchiveSubjectService(subjects)

        res = await vehicle_archive_subject_query_sync_read(service=as_service(fake))
        assert (
            res.VehicleArchiveSubjectListObject.VehicleArchiveSubjectObject[0].ArchiveID
            == "VS-001"
        )
        assert len(res.VehicleArchiveSubjectListObject.VehicleArchiveSubjectObject) == 2

    asyncio.run(_run())


def test_vehicle_archive_subject_create_update_delete_return_status_list():
    async def _run():
        subjects = _sample_vehicle_archive_subjects()
        fake = _FakeVehicleArchiveSubjectService(subjects)
        payload = VehicleArchiveSubjectSchema(
            VehicleArchiveSubjectListObject=VehicleArchiveSubjectList(
                VehicleArchiveSubjectObject=subjects
            )
        )

        create_res = await vehicle_archive_subjects_create(
            data=payload, service=as_service(fake)
        )
        update_res = await vehicle_archive_subjects_update(
            data=payload, service=as_service(fake)
        )
        delete_res = await vehicle_archive_subjects_delete(
            archive_ids=["VS-001", "VS-002"], service=as_service(fake)
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
        assert create_status[0].Id == "VS-001"
        assert len(update_status) == 2
        assert update_status[1].Id == "VS-002"
        assert len(delete_status) == 2
        assert delete_status[0].Id == "VS-001"

        assert fake.created_with is not None
        assert len(fake.created_with) == 2
        assert fake.updated_with is not None
        assert len(fake.updated_with) == 2
        assert fake.deleted_with == ["VS-001", "VS-002"]

    asyncio.run(_run())
