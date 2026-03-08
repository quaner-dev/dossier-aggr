import asyncio

from models import ArchiveSubject, VehicleArchiveSubject
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


def _sample_archive_subject() -> ArchiveSubject:
    return ArchiveSubject(
        ArchiveID="AS-LAYER-001",
        PersonIDList=["P-001"],
        FaceIDList=["F-001"],
        PersonObjectList=None,
        FaceObjectList=None,
        ImageID="IMG-AS-LAYER-001",
    )


def _sample_vehicle_archive_subject() -> VehicleArchiveSubject:
    return VehicleArchiveSubject(
        ArchiveID="VAS-LAYER-001",
        MotorVehicleIDList=["MV-001"],
        NonMotorVehicleIDList=["NMV-001"],
        ImageID="IMG-VAS-LAYER-001",
    )


def test_subject_services_sync_reads_use_repositories(monkeypatch):
    async def _run():
        archive_subject = _sample_archive_subject()
        vehicle_subject = _sample_vehicle_archive_subject()
        called = {"archive_query_repo": False, "vehicle_query_repo": False}

        async def fake_query_archive_subjects_repo():
            called["archive_query_repo"] = True
            return [archive_subject]

        async def fake_query_vehicle_archive_subjects_repo():
            called["vehicle_query_repo"] = True
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

        archive_res = await ArchiveSubjectService().query_archive_subjects()
        vehicle_res = await VehicleArchiveSubjectService().query_vehicle_archive_subjects()

        assert archive_res[0].ArchiveID == "AS-LAYER-001"
        assert vehicle_res[0].ArchiveID == "VAS-LAYER-001"
        assert all(called.values())

    asyncio.run(_run())


def test_verify_services_sync_reads_use_repositories(monkeypatch):
    async def _run():
        called = {"archive_verify_repo": False, "vehicle_verify_repo": False}

        async def fake_verify_archive_confidence_repo(archive_ids: list[str]):
            called["archive_verify_repo"] = True
            assert archive_ids == ["A-LAYER-001", "A-LAYER-002"]
            return archive_ids

        async def fake_verify_vehicle_archive_confidence_repo(archive_ids: list[str]):
            called["vehicle_verify_repo"] = True
            assert archive_ids == ["VA-LAYER-001", "VA-LAYER-002"]
            return archive_ids

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

        archive_res = await ArchiveConfidenceService().verify_archive_confidence(
            archive_ids=["A-LAYER-001", "A-LAYER-002"]
        )
        vehicle_res = await VehicleArchiveConfidenceService().verify_vehicle_archive_confidence(
            archive_ids=["VA-LAYER-001", "VA-LAYER-002"]
        )

        assert archive_res == ["A-LAYER-001", "A-LAYER-002"]
        assert vehicle_res == ["VA-LAYER-001", "VA-LAYER-002"]
        assert all(called.values())

    asyncio.run(_run())


def test_subject_verify_tasks_delegate_to_repositories(monkeypatch):
    async def _run():
        archive_subject = _sample_archive_subject()
        vehicle_subject = _sample_vehicle_archive_subject()
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
            archive_id: str | None,
            face_id_list: list[str] | None,
            person_id_list: list[str] | None,
            motor_vehicle_id_list: list[str] | None,
            non_motor_vehicle_id_list: list[str] | None,
        ):
            called["archive_delete_repo"] = True
            assert archive_id == "AS-LAYER-001"
            assert face_id_list == ["F-001"]
            assert person_id_list == ["P-001"]
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

        async def fake_delete_vehicle_archive_subjects_repo(archive_ids: list[str]):
            called["vehicle_delete_repo"] = True
            assert archive_ids == ["VAS-LAYER-001"]
            return archive_ids

        async def fake_verify_archive_confidence_repo(archive_ids: list[str]):
            called["archive_verify_repo"] = True
            assert archive_ids == ["A-LAYER-001"]
            return archive_ids

        async def fake_verify_vehicle_archive_confidence_repo(archive_ids: list[str]):
            called["vehicle_verify_repo"] = True
            assert archive_ids == ["VA-LAYER-001"]
            return archive_ids

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
            archive_id="AS-LAYER-001",
            face_id_list=["F-001"],
            person_id_list=["P-001"],
            motor_vehicle_id_list=None,
            non_motor_vehicle_id_list=None,
        )

        vehicle_query_res = await vehicle_subject_task_module.query_vehicle_archive_subjects_task()
        vehicle_create_res = await vehicle_subject_task_module.create_vehicle_archive_subjects_task.original_func(
            [vehicle_subject]
        )
        vehicle_update_res = await vehicle_subject_task_module.update_vehicle_archive_subjects_task.original_func(
            [vehicle_subject]
        )
        vehicle_delete_res = await vehicle_subject_task_module.delete_vehicle_archive_subjects_task.original_func(
            archive_ids=["VAS-LAYER-001"]
        )

        archive_verify_res = await archive_verify_task_module.verify_archive_confidence_task(
            archive_ids=["A-LAYER-001"]
        )
        vehicle_verify_res = await vehicle_verify_task_module.verify_vehicle_archive_confidence_task(
            archive_ids=["VA-LAYER-001"]
        )

        assert archive_query_res[0].ArchiveID == "AS-LAYER-001"
        assert archive_create_res[0].ArchiveID == "AS-LAYER-001"
        assert archive_update_res[0].ArchiveID == "AS-LAYER-001"
        assert archive_delete_res == ["AS-LAYER-001"]
        assert vehicle_query_res[0].ArchiveID == "VAS-LAYER-001"
        assert vehicle_create_res[0].ArchiveID == "VAS-LAYER-001"
        assert vehicle_update_res[0].ArchiveID == "VAS-LAYER-001"
        assert vehicle_delete_res == ["VAS-LAYER-001"]
        assert archive_verify_res == ["A-LAYER-001"]
        assert vehicle_verify_res == ["VA-LAYER-001"]
        assert all(called.values())

    asyncio.run(_run())
