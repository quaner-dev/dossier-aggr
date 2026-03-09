import asyncio

from api.archive.archive_subject import (
    archive_subject_query_sync,
    archive_subjects_create,
    archive_subjects_update,
    archive_subjects_delete,
)
from models import ArchiveSubject, ArchiveSubjectList, ArchiveSubjectSchema
from tests.type_helpers import as_service, as_status_list


class _FakeArchiveSubjectService:
    def __init__(self, subjects: list[ArchiveSubject]):
        self._subjects = subjects
        self.created_with: list[ArchiveSubject] | None = None
        self.updated_with: list[ArchiveSubject] | None = None
        self.deleted_with: str | None = None

    async def query_archive_subjects(self):
        return self._subjects

    async def create_archive_subjects(self, subjects: list[ArchiveSubject]):
        self.created_with = subjects
        return subjects

    async def update_archive_subjects(self, subjects: list[ArchiveSubject]):
        self.updated_with = subjects
        return subjects

    async def delete_archive_subjects(self, archive_id: str):
        self.deleted_with = archive_id
        return [archive_id]


def _sample_subjects() -> list[ArchiveSubject]:
    return [
        ArchiveSubject(
            ArchiveID="AS-001",
            PersonIDList=["P-001"],
            FaceIDList=["F-001"],
            PersonObjectList=None,
            FaceObjectList=None,
            ImageID="IMG-S-001",
        ),
        ArchiveSubject(
            ArchiveID="AS-002",
            PersonIDList=["P-002"],
            FaceIDList=["F-002"],
            PersonObjectList=None,
            FaceObjectList=None,
            ImageID="IMG-S-002",
        ),
    ]


def test_archive_subject_query_sync_returns_query_result_schema():
    async def _run():
        subjects = _sample_subjects()
        fake = _FakeArchiveSubjectService(subjects)

        res = await archive_subject_query_sync(service=as_service(fake))

        assert res.ArchiveSubjectQueryResultObject.TotalNum == 2
        assert (
            res.ArchiveSubjectQueryResultObject.ArchiveSubjectInfoList.ArchiveSubjectObject[
                0
            ].ArchiveID
            == "AS-001"
        )

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
            archive_id="AS-001",
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
        assert create_status[0].Id == "AS-001"
        assert len(update_status) == 2
        assert update_status[1].Id == "AS-002"
        assert len(delete_status) == 1
        assert delete_status[0].Id == "AS-001"

        assert fake.created_with is not None
        assert len(fake.created_with) == 2
        assert fake.updated_with is not None
        assert len(fake.updated_with) == 2
        assert fake.deleted_with == "AS-001"

    asyncio.run(_run())
