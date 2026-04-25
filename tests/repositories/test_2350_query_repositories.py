import asyncio

import pytest

from core import exceptions
from models import (
    Archive,
    ArchiveQuery,
    ArchiveSubject,
    ArchiveSubjectQuery,
    VehicleArchive,
    VehicleArchiveSubject,
)
from models.common import enums
from repo.archive import archive_subject as archive_subject_repo
from repo.archive import archives as archive_repo
from repo.vehicle import vehicle_archive as vehicle_archive_repo
from repo.vehicle import vehicle_archive_subject as vehicle_subject_repo
from tests.type_helpers import dt, sample_feature_info_list, sample_sub_image_list


class _FakeResult:
    def __init__(self, rows):
        self._rows = rows

    def all(self):
        return self._rows


class _FakeAsyncSession:
    def __init__(self, rows):
        self._rows = rows
        self.statement = None

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    async def exec(self, statement):
        self.statement = statement
        return _FakeResult(self._rows)


def _query_with_subject(subject_id: str) -> ArchiveQuery:
    return ArchiveQuery.model_validate(
        {
            "QueryID": "Q-2350-SUBJECT-001",
            "PictureQueryCondition": {
                "PictureQueryConditionObject": [{"SubjectID": subject_id}]
            },
        }
    )


def _subject_query_with_subject(subject_id: str) -> ArchiveSubjectQuery:
    return ArchiveSubjectQuery.model_validate(
        {
            "QueryID": "Q-2350-SUBJECT-001",
            "ArchiveIDList": [],
            "PictureQueryCondition": {
                "PictureQueryConditionObject": [{"SubjectID": subject_id}]
            },
        }
    )


def _sample_archive(archive_id: str, source_ids: list[str]) -> Archive:
    return Archive(
        ArchiveID=archive_id,
        ArchiveLibraryID="LIB-001",
        CreateTime=dt("20260101120000"),
        UpdateTime=dt("20260101120000"),
        SourceIDList=source_ids,
        CenterFeatureList=sample_feature_info_list(archive_id.lower()),
        Similaritydegree=0.91,
        Confidence=0.82,
        SubImageList=sample_sub_image_list(
            f"IMG-{archive_id}", enums.ImageTypeEnum.PersonImage, archive_id.lower()
        ),
    )


def _sample_vehicle_archive(archive_id: str, source_ids: list[str]) -> VehicleArchive:
    return VehicleArchive(
        ArchiveID=archive_id,
        ArchiveLibraryID="LIB-001",
        PlateNo="A12345",
        PlateColor=enums.ColorTypeEnum.Blue,
        VehicleClass="K11",
        CreateTime=dt("20260101120000"),
        UpdateTime=dt("20260101120000"),
        SourceIDList=source_ids,
        SubImageList=sample_sub_image_list(
            f"IMG-{archive_id}",
            enums.ImageTypeEnum.VehicleLargeImage,
            archive_id.lower(),
        ),
    )


def _sample_archive_subject(archive_id: str, face_ids: list[str]) -> ArchiveSubject:
    return ArchiveSubject(
        ArchiveID=archive_id,
        PersonIDList=["P-001"],
        FaceIDList=face_ids,
        GaitIDList=["G-001"],
        MotorVehicleIDList=["MV-001"],
        NonMotorVehicleIDList=["NMV-001"],
        PersonObjectList=None,
        FaceObjectList=None,
        GaitObjectList=None,
        MotorVehicleObjectList=None,
        NonMotorVehicleObjectList=None,
    )


def _sample_vehicle_archive_subject(
    archive_id: str,
    person_ids: list[str],
) -> VehicleArchiveSubject:
    return VehicleArchiveSubject(
        ArchiveID=archive_id,
        PersonIDList=person_ids,
        FaceIDList=["F-001"],
        GaitIDList=["G-001"],
        MotorVehicleIDList=["MV-001"],
        NonMotorVehicleIDList=["NMV-001"],
        PersonObjectList=None,
        FaceObjectList=None,
        GaitObjectList=None,
        MotorVehicleObjectList=None,
        NonMotorVehicleObjectList=None,
    )


def test_query_archives_repo_filters_by_picture_query_condition_subject_id(monkeypatch):
    async def _run():
        rows = [
            _sample_archive("A-001", ["P-001", "FACE-001"]),
            _sample_archive("A-002", ["P-002", "FACE-002"]),
        ]
        fake_session = _FakeAsyncSession(rows)
        monkeypatch.setattr(archive_repo, "AsyncSession", lambda _engine: fake_session)

        result = await archive_repo.query_archives_repo(_query_with_subject("FACE-001"))

        assert [archive.ArchiveID for archive in result] == ["A-001"]

    asyncio.run(_run())


def test_query_vehicle_archives_repo_filters_by_picture_query_condition_subject_id(monkeypatch):
    async def _run():
        rows = [
            _sample_vehicle_archive("VA-001", ["MV-001"]),
            _sample_vehicle_archive("VA-002", ["MV-002"]),
        ]
        fake_session = _FakeAsyncSession(rows)
        monkeypatch.setattr(
            vehicle_archive_repo,
            "AsyncSession",
            lambda _engine: fake_session,
        )

        result = await vehicle_archive_repo.query_vehicle_archives_repo(
            _query_with_subject("MV-001")
        )

        assert [archive.ArchiveID for archive in result] == ["VA-001"]

    asyncio.run(_run())


def test_query_archive_subjects_repo_filters_by_picture_query_condition_subject_id(
    monkeypatch,
):
    async def _run():
        rows = [
            _sample_archive_subject("AS-001", ["F-001"]),
            _sample_archive_subject("AS-002", ["F-002"]),
        ]
        fake_session = _FakeAsyncSession(rows)
        monkeypatch.setattr(
            archive_subject_repo,
            "AsyncSession",
            lambda _engine: fake_session,
        )
        monkeypatch.setattr(archive_subject_repo, "_ensure_table", lambda: asyncio.sleep(0))

        result = await archive_subject_repo.query_archive_subjects_repo(
            _subject_query_with_subject("F-001")
        )

        assert [subject.ArchiveID for subject in result] == ["AS-001"]

    asyncio.run(_run())


def test_query_vehicle_archive_subjects_repo_filters_by_picture_query_condition_subject_id(
    monkeypatch,
):
    async def _run():
        rows = [
            _sample_vehicle_archive_subject("VAS-001", ["P-001"]),
            _sample_vehicle_archive_subject("VAS-002", ["P-002"]),
        ]
        fake_session = _FakeAsyncSession(rows)
        monkeypatch.setattr(
            vehicle_subject_repo,
            "AsyncSession",
            lambda _engine: fake_session,
        )
        monkeypatch.setattr(vehicle_subject_repo, "_ensure_table", lambda: asyncio.sleep(0))

        result = await vehicle_subject_repo.query_vehicle_archive_subjects_repo(
            _subject_query_with_subject("P-001")
        )

        assert [subject.ArchiveID for subject in result] == ["VAS-001"]

    asyncio.run(_run())


def test_query_archives_repo_raises_not_found_after_subject_filter(monkeypatch):
    async def _run():
        rows = [_sample_archive("A-001", ["P-001"])]
        fake_session = _FakeAsyncSession(rows)
        monkeypatch.setattr(archive_repo, "AsyncSession", lambda _engine: fake_session)

        with pytest.raises(exceptions.DataNotFoundError):
            await archive_repo.query_archives_repo(_query_with_subject("FACE-404"))

    asyncio.run(_run())
