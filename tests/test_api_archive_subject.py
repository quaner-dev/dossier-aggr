import asyncio

from api.archive.archive_subject import (
    archive_subject_query_sync,
    archive_subjects_create,
    archive_subjects_delete,
    archive_subjects_update,
)
from models import (
    ArchiveSubject,
    ArchiveSubjectList,
    ArchiveSubjectQuery,
    ArchiveSubjectQuerySchema,
    ArchiveSubjectSchema,
)
from tests.type_helpers import as_service, as_status_list


class _FakeArchiveSubjectService:
    def __init__(self, subjects: list[ArchiveSubject]):
        self._subjects = subjects
        self.queried_with: ArchiveSubjectQuery | None = None
        self.created_with: list[ArchiveSubject] | None = None
        self.updated_with: list[ArchiveSubject] | None = None
        self.deleted_with: dict[str, object] | None = None

    async def query_archive_subjects(self, query: ArchiveSubjectQuery):
        self.queried_with = query
        return self._subjects

    async def create_archive_subjects(self, subjects: list[ArchiveSubject]):
        self.created_with = subjects
        return subjects

    async def update_archive_subjects(self, subjects: list[ArchiveSubject]):
        self.updated_with = subjects
        return subjects

    async def delete_archive_subjects(
        self,
        archive_id: str | None = None,
        face_id_list: list[str] | None = None,
        person_id_list: list[str] | None = None,
        motor_vehicle_id_list: list[str] | None = None,
        non_motor_vehicle_id_list: list[str] | None = None,
    ):
        self.deleted_with = {
            "archive_id": archive_id,
            "face_id_list": face_id_list,
            "person_id_list": person_id_list,
            "motor_vehicle_id_list": motor_vehicle_id_list,
            "non_motor_vehicle_id_list": non_motor_vehicle_id_list,
        }
        return ["AS-001"]


def _sample_subjects() -> list[ArchiveSubject]:
    return [
        ArchiveSubject(
            ArchiveID="AS-001",
            PersonIDList=["P-001"],
            FaceIDList=["F-001"],
            GaitIDList=["G-001"],
            MotorVehicleIDList=["MV-001"],
            NonMotorVehicleIDList=["NMV-001"],
            PersonObjectList=None,
            FaceObjectList=None,
            GaitObjectList=None,
            MotorVehicleObjectList=None,
            NonMotorVehicleObjectList=None,
        ),
        ArchiveSubject(
            ArchiveID="AS-002",
            PersonIDList=["P-002"],
            FaceIDList=["F-002"],
            GaitIDList=["G-002"],
            MotorVehicleIDList=["MV-002"],
            NonMotorVehicleIDList=["NMV-002"],
            PersonObjectList=None,
            FaceObjectList=None,
            GaitObjectList=None,
            MotorVehicleObjectList=None,
            NonMotorVehicleObjectList=None,
        ),
    ]


def test_archive_subject_query_sync_returns_query_result_schema():
    async def _run():
        subjects = _sample_subjects()
        fake = _FakeArchiveSubjectService(subjects)
        payload = ArchiveSubjectQuerySchema(
            ArchiveSubjectQueryObject=ArchiveSubjectQuery(
                QueryID="Q-AS-001",
                RecordStartNo=0,
                PageRecordNum=10,
                ArchiveIDList=["AS-001", "AS-002"],
            )
        )

        res = await archive_subject_query_sync(data=payload, service=as_service(fake))

        assert res.ArchiveSubjectQueryResultObject.QueryID == "Q-AS-001"
        assert res.ArchiveSubjectQueryResultObject.TotalNum == 2
        assert (
            res.ArchiveSubjectQueryResultObject.ArchiveSubjectInfoList.ArchiveSubjectObject[
                0
            ].ArchiveID
            == "AS-001"
        )
        assert (
            res.ArchiveSubjectQueryResultObject.ArchiveSubjectInfoList.ArchiveSubjectObject[
                0
            ].GaitIDList
            == ["G-001"]
        )
        assert fake.queried_with is not None
        assert fake.queried_with.QueryID == "Q-AS-001"

    asyncio.run(_run())


def test_archive_subject_create_update_delete_return_status_list():
    async def _run():
        subjects = _sample_subjects()
        fake = _FakeArchiveSubjectService(subjects)
        payload = ArchiveSubjectSchema(
            ArchiveSubjectListObject=ArchiveSubjectList(ArchiveSubjectObject=subjects)
        )

        create_res = await archive_subjects_create(data=payload, service=as_service(fake))
        update_res = await archive_subjects_update(data=payload, service=as_service(fake))
        delete_res = await archive_subjects_delete(
            face_id_list="F-001",
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
        assert create_status[0].Id == "AS-001"
        assert len(update_status) == 2
        assert update_status[1].Id == "AS-002"
        assert len(delete_status) == 1
        assert delete_status[0].Id == "AS-001"

        assert fake.created_with is not None
        assert len(fake.created_with) == 2
        assert fake.updated_with is not None
        assert len(fake.updated_with) == 2
        assert fake.deleted_with == {
            "archive_id": None,
            "face_id_list": ["F-001"],
            "person_id_list": None,
            "motor_vehicle_id_list": None,
            "non_motor_vehicle_id_list": None,
        }

    asyncio.run(_run())


def test_archive_subject_delete_accepts_motor_vehicle_id_list():
    async def _run():
        fake = _FakeArchiveSubjectService(_sample_subjects())

        _ = await archive_subjects_delete(
            motor_vehicle_id_list="MV-001",
            service=as_service(fake),
        )

        assert fake.deleted_with == {
            "archive_id": None,
            "face_id_list": None,
            "person_id_list": None,
            "motor_vehicle_id_list": ["MV-001"],
            "non_motor_vehicle_id_list": None,
        }

    asyncio.run(_run())
