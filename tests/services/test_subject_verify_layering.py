import asyncio

from models import (
    Archive,
    ArchiveSubject,
    ArchiveSubjectQuery,
    VehicleArchive,
    VehicleArchiveSubject,
)
from services.archive.archive_subject import ArchiveSubjectService
from services.vehicle.vehicle_archive_subject import VehicleArchiveSubjectService
from services.verify.archive_confidence import ArchiveConfidenceService
from services.verify.vehicle_archive_confidence import VehicleArchiveConfidenceService
import services.archive.archive_subject as archive_subject_service_module
import services.vehicle.vehicle_archive_subject as vehicle_subject_service_module
import services.verify.archive_confidence as archive_verify_service_module
import services.verify.vehicle_archive_confidence as vehicle_verify_service_module
import tasks.archive.archive_subject as archive_subject_task_module
import tasks.vehicle.vehicle_archive_subject as vehicle_subject_task_module
import tasks.verify.archive_confidence as archive_verify_task_module
import tasks.verify.vehicle_archive_confidence as vehicle_verify_task_module
from models.common import enums
from tests.type_helpers import dt, sample_feature_info_list, sample_sub_image_list


def _sample_archive_subject() -> ArchiveSubject:
    return ArchiveSubject(
        ArchiveID="AS-LAYER-001",
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
    )


def _sample_vehicle_archive_subject() -> VehicleArchiveSubject:
    return VehicleArchiveSubject(
        ArchiveID="VAS-LAYER-001",
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
    )


def _sample_archive() -> Archive:
    return Archive(
        ArchiveID="A-LAYER-001",
        ArchiveLibraryID="LIB-LAYER-001",
        CreateTime=dt("20260101120000"),
        UpdateTime=dt("20260101120000"),
        SourceIDList=["PERSON-LAYER-001", "FACE-LAYER-001"],
        CenterFeatureList=sample_feature_info_list("archive-verify-layer"),
        Similaritydegree=0.91,
        Confidence=0.82,
        SubImageList=sample_sub_image_list(
            "IMG-LAYER-001",
            enums.ImageTypeEnum.PersonImage,
            "archive-verify-layer",
        ),
    )


def _sample_vehicle_archive() -> VehicleArchive:
    return VehicleArchive(
        ArchiveID="VA-LAYER-001",
        ArchiveLibraryID="LIB-LAYER-001",
        PlateNo="A12345",
        PlateColor=enums.ColorTypeEnum.Blue,
        VehicleClass="K11",
        CreateTime=dt("20260101120000"),
        UpdateTime=dt("20260101120000"),
        SourceIDList=["MV-LAYER-001"],
        SubImageList=sample_sub_image_list(
            "IMG-VA-LAYER-001",
            enums.ImageTypeEnum.VehicleLargeImage,
            "vehicle-verify-layer",
        ),
    )


def test_subject_services_sync_reads_use_repositories(monkeypatch):
    async def _run():
        archive_subject = _sample_archive_subject()
        vehicle_subject = _sample_vehicle_archive_subject()
        called = {"archive_query_repo": False, "vehicle_query_repo": False}
        archive_query = ArchiveSubjectQuery(
            QueryID="Q-AS-LAYER-001",
            ArchiveIDList=["AS-LAYER-001"],
        )
        vehicle_query = ArchiveSubjectQuery(
            QueryID="Q-VAS-LAYER-001",
            ArchiveIDList=["VAS-LAYER-001"],
        )

        async def fake_query_archive_subjects_repo(query: ArchiveSubjectQuery | None = None):
            called["archive_query_repo"] = True
            assert query is not None
            assert query.QueryID == "Q-AS-LAYER-001"
            return [archive_subject]

        async def fake_query_vehicle_archive_subjects_repo(
            query: ArchiveSubjectQuery | None = None,
        ):
            called["vehicle_query_repo"] = True
            assert query is not None
            assert query.QueryID == "Q-VAS-LAYER-001"
            return [vehicle_subject]

        monkeypatch.setattr(
            archive_subject_service_module,
            "query_archive_subjects_repo",
            fake_query_archive_subjects_repo,
            raising=False,
        )
        monkeypatch.setattr(
            vehicle_subject_service_module,
            "query_vehicle_archive_subjects_repo",
            fake_query_vehicle_archive_subjects_repo,
            raising=False,
        )
        monkeypatch.setattr(
            archive_subject_service_module,
            "query_archive_subjects_task",
            lambda *args, **kwargs: (_ for _ in ()).throw(
                AssertionError("query_archive_subjects_task should not be called")
            ),
            raising=False,
        )
        monkeypatch.setattr(
            vehicle_subject_service_module,
            "query_vehicle_archive_subjects_task",
            lambda *args, **kwargs: (_ for _ in ()).throw(
                AssertionError("query_vehicle_archive_subjects_task should not be called")
            ),
            raising=False,
        )

        archive_res = await ArchiveSubjectService().query_archive_subjects(archive_query)
        vehicle_res = await VehicleArchiveSubjectService().query_vehicle_archive_subjects(
            vehicle_query
        )

        assert archive_res[0].ArchiveID == "AS-LAYER-001"
        assert vehicle_res[0].ArchiveID == "VAS-LAYER-001"
        assert all(called.values())

    asyncio.run(_run())


def test_verify_services_sync_reads_use_repositories(monkeypatch):
    async def _run():
        archive = _sample_archive()
        vehicle_archive = _sample_vehicle_archive()
        called = {"archive_verify_repo": False, "vehicle_verify_repo": False}

        async def fake_verify_archive_confidence_repo(archives: list[Archive]):
            called["archive_verify_repo"] = True
            assert [archive.ArchiveID for archive in archives] == ["A-LAYER-001"]
            return archives

        async def fake_verify_vehicle_archive_confidence_repo(
            archives: list[VehicleArchive],
        ):
            called["vehicle_verify_repo"] = True
            assert [archive.ArchiveID for archive in archives] == ["VA-LAYER-001"]
            return archives

        monkeypatch.setattr(
            archive_verify_service_module,
            "verify_archive_confidence_repo",
            fake_verify_archive_confidence_repo,
            raising=False,
        )
        monkeypatch.setattr(
            vehicle_verify_service_module,
            "verify_vehicle_archive_confidence_repo",
            fake_verify_vehicle_archive_confidence_repo,
            raising=False,
        )
        monkeypatch.setattr(
            archive_verify_service_module,
            "verify_archive_confidence_task",
            lambda *args, **kwargs: (_ for _ in ()).throw(
                AssertionError("verify_archive_confidence_task should not be called")
            ),
            raising=False,
        )
        monkeypatch.setattr(
            vehicle_verify_service_module,
            "verify_vehicle_archive_confidence_task",
            lambda *args, **kwargs: (_ for _ in ()).throw(
                AssertionError("verify_vehicle_archive_confidence_task should not be called")
            ),
            raising=False,
        )

        archive_res = await ArchiveConfidenceService().verify_archive_confidence([archive])
        vehicle_res = await VehicleArchiveConfidenceService().verify_vehicle_archive_confidence(
            [vehicle_archive]
        )

        assert archive_res[0].ArchiveID == "A-LAYER-001"
        assert vehicle_res[0].ArchiveID == "VA-LAYER-001"
        assert all(called.values())

    asyncio.run(_run())


def test_subject_verify_tasks_delegate_to_repositories(monkeypatch):
    async def _run():
        archive_subject = _sample_archive_subject()
        vehicle_subject = _sample_vehicle_archive_subject()
        archive = _sample_archive()
        vehicle_archive = _sample_vehicle_archive()
        called = {
            "archive_query_repo": False,
            "archive_create_repo": False,
            "archive_update_repo": False,
            "archive_delete_repo": False,
            "vehicle_query_repo": False,
            "vehicle_create_repo": False,
            "vehicle_update_repo": False,
            "vehicle_delete_repo": False,
            "archive_verify_repo": False,
            "vehicle_verify_repo": False,
        }

        async def fake_query_archive_subjects_repo():
            called["archive_query_repo"] = True
            return [archive_subject]

        async def fake_create_archive_subjects_repo(subjects: list[ArchiveSubject]):
            called["archive_create_repo"] = True
            assert len(subjects) == 1
            return subjects

        async def fake_update_archive_subjects_repo(subjects: list[ArchiveSubject]):
            called["archive_update_repo"] = True
            assert len(subjects) == 1
            return subjects

        async def fake_delete_archive_subjects_repo(
            archive_id: str | None = None,
            face_id_list: list[str] | None = None,
            person_id_list: list[str] | None = None,
            motor_vehicle_id_list: list[str] | None = None,
            non_motor_vehicle_id_list: list[str] | None = None,
        ):
            called["archive_delete_repo"] = True
            assert face_id_list == ["F-001"]
            assert archive_id is None
            assert person_id_list is None
            assert motor_vehicle_id_list is None
            assert non_motor_vehicle_id_list is None
            return ["AS-LAYER-001"]

        async def fake_query_vehicle_archive_subjects_repo():
            called["vehicle_query_repo"] = True
            return [vehicle_subject]

        async def fake_create_vehicle_archive_subjects_repo(
            subjects: list[VehicleArchiveSubject],
        ):
            called["vehicle_create_repo"] = True
            assert len(subjects) == 1
            return subjects

        async def fake_update_vehicle_archive_subjects_repo(
            subjects: list[VehicleArchiveSubject],
        ):
            called["vehicle_update_repo"] = True
            assert len(subjects) == 1
            return subjects

        async def fake_delete_vehicle_archive_subjects_repo(
            archive_id: str | None = None,
            face_id_list: list[str] | None = None,
            person_id_list: list[str] | None = None,
            motor_vehicle_id_list: list[str] | None = None,
            non_motor_vehicle_id_list: list[str] | None = None,
        ):
            called["vehicle_delete_repo"] = True
            assert motor_vehicle_id_list == ["MV-001"]
            assert archive_id is None
            assert face_id_list is None
            assert person_id_list is None
            assert non_motor_vehicle_id_list is None
            return ["VAS-LAYER-001"]

        async def fake_verify_archive_confidence_repo(archives: list[Archive]):
            called["archive_verify_repo"] = True
            assert [archive.ArchiveID for archive in archives] == ["A-LAYER-001"]
            return archives

        async def fake_verify_vehicle_archive_confidence_repo(
            archives: list[VehicleArchive],
        ):
            called["vehicle_verify_repo"] = True
            assert [archive.ArchiveID for archive in archives] == ["VA-LAYER-001"]
            return archives

        monkeypatch.setattr(
            archive_subject_task_module,
            "query_archive_subjects_repo",
            fake_query_archive_subjects_repo,
            raising=False,
        )
        monkeypatch.setattr(
            archive_subject_task_module,
            "create_archive_subjects_repo",
            fake_create_archive_subjects_repo,
            raising=False,
        )
        monkeypatch.setattr(
            archive_subject_task_module,
            "update_archive_subjects_repo",
            fake_update_archive_subjects_repo,
            raising=False,
        )
        monkeypatch.setattr(
            archive_subject_task_module,
            "delete_archive_subjects_repo",
            fake_delete_archive_subjects_repo,
            raising=False,
        )
        monkeypatch.setattr(
            vehicle_subject_task_module,
            "query_vehicle_archive_subjects_repo",
            fake_query_vehicle_archive_subjects_repo,
            raising=False,
        )
        monkeypatch.setattr(
            vehicle_subject_task_module,
            "create_vehicle_archive_subjects_repo",
            fake_create_vehicle_archive_subjects_repo,
            raising=False,
        )
        monkeypatch.setattr(
            vehicle_subject_task_module,
            "update_vehicle_archive_subjects_repo",
            fake_update_vehicle_archive_subjects_repo,
            raising=False,
        )
        monkeypatch.setattr(
            vehicle_subject_task_module,
            "delete_vehicle_archive_subjects_repo",
            fake_delete_vehicle_archive_subjects_repo,
            raising=False,
        )
        monkeypatch.setattr(
            archive_verify_task_module,
            "verify_archive_confidence_repo",
            fake_verify_archive_confidence_repo,
            raising=False,
        )
        monkeypatch.setattr(
            vehicle_verify_task_module,
            "verify_vehicle_archive_confidence_repo",
            fake_verify_vehicle_archive_confidence_repo,
            raising=False,
        )

        archive_query_res = await archive_subject_task_module.query_archive_subjects_task()
        archive_create_res = await archive_subject_task_module.create_archive_subjects_task.original_func(
            [archive_subject]
        )
        archive_update_res = await archive_subject_task_module.update_archive_subjects_task.original_func(
            [archive_subject]
        )
        archive_delete_res = await archive_subject_task_module.delete_archive_subjects_task.original_func(
            face_id_list=["F-001"],
        )

        vehicle_query_res = await vehicle_subject_task_module.query_vehicle_archive_subjects_task()
        vehicle_create_res = await vehicle_subject_task_module.create_vehicle_archive_subjects_task.original_func(
            [vehicle_subject]
        )
        vehicle_update_res = await vehicle_subject_task_module.update_vehicle_archive_subjects_task.original_func(
            [vehicle_subject]
        )
        vehicle_delete_res = await vehicle_subject_task_module.delete_vehicle_archive_subjects_task.original_func(
            motor_vehicle_id_list=["MV-001"]
        )

        archive_verify_res = await archive_verify_task_module.verify_archive_confidence_task(
            archives=[archive]
        )
        vehicle_verify_res = await vehicle_verify_task_module.verify_vehicle_archive_confidence_task(
            archives=[vehicle_archive]
        )

        assert archive_query_res[0].ArchiveID == "AS-LAYER-001"
        assert archive_create_res[0].ArchiveID == "AS-LAYER-001"
        assert archive_update_res[0].ArchiveID == "AS-LAYER-001"
        assert archive_delete_res == ["AS-LAYER-001"]
        assert vehicle_query_res[0].ArchiveID == "VAS-LAYER-001"
        assert vehicle_create_res[0].ArchiveID == "VAS-LAYER-001"
        assert vehicle_update_res[0].ArchiveID == "VAS-LAYER-001"
        assert vehicle_delete_res == ["VAS-LAYER-001"]
        assert archive_verify_res[0].ArchiveID == "A-LAYER-001"
        assert vehicle_verify_res[0].ArchiveID == "VA-LAYER-001"
        assert all(called.values())

    asyncio.run(_run())
