import asyncio

from models import Face, FaceQueryParams, Person
from models.common import enums
from services.face.face import FaceService
from services.person.person import PersonService
import services.face.face as face_service_module
import services.person.person as person_service_module
import tasks.face.face as face_task_module
import tasks.person.person as person_task_module



def _sample_person() -> Person:
    return Person(
        PersonID="P-LAYER-001",
        InfoKind=enums.InfoKindEnum.AutoCollect,
        SourceID="SRC-P-LAYER-001",
        DeviceID="DEV-P-LAYER-001",
        LeftTopX=10,
        LeftTopY=20,
        RightBtmX=100,
        RightBtmY=200,
        SubImageList=None,
    )



def _sample_face() -> Face:
    return Face(
        FaceID="F-LAYER-001",
        InfoKind=enums.InfoKindEnum.AutoCollect,
        SourceID="SRC-F-LAYER-001",
        DeviceID="DEV-F-LAYER-001",
        LeftTopX=10,
        LeftTopY=20,
        RightBtmX=100,
        RightBtmY=200,
        SubImageList=None,
    )



def test_person_service_sync_reads_use_repository(monkeypatch):
    async def _run():
        person = _sample_person()
        called = {"list_repo": False, "get_repo": False}

        async def fake_list_repo():
            called["list_repo"] = True
            return [person]

        async def fake_get_repo(person_id: str):
            called["get_repo"] = True
            assert person_id == "P-LAYER-001"
            return person

        monkeypatch.setattr(
            person_service_module,
            "list_persons_repo",
            fake_list_repo,
            raising=False,
        )
        monkeypatch.setattr(
            person_service_module,
            "get_person_repo",
            fake_get_repo,
            raising=False,
        )
        monkeypatch.setattr(
            person_service_module,
            "list_persons_task",
            lambda *args, **kwargs: (_ for _ in ()).throw(
                AssertionError("list_persons_task should not be called")
            ),
            raising=False,
        )
        monkeypatch.setattr(
            person_service_module,
            "get_person_task",
            lambda *args, **kwargs: (_ for _ in ()).throw(
                AssertionError("get_person_task should not be called")
            ),
            raising=False,
        )

        service = PersonService()
        list_res = await asyncio.wait_for(service.list_persons(), timeout=1)
        get_res = await asyncio.wait_for(service.get_person("P-LAYER-001"), timeout=1)

        assert called["list_repo"] is True
        assert called["get_repo"] is True
        assert list_res[0].PersonID == "P-LAYER-001"
        assert get_res.PersonID == "P-LAYER-001"

    asyncio.run(_run())



def test_face_service_sync_reads_use_repository(monkeypatch):
    async def _run():
        face = _sample_face()
        called = {"list_repo": False, "get_repo": False}

        query = FaceQueryParams(RecordStartNo=1, PageRecordNum=1)

        async def fake_list_repo(query: FaceQueryParams):
            called["list_repo"] = True
            assert query == FaceQueryParams(RecordStartNo=1, PageRecordNum=1)
            return [face]

        async def fake_get_repo(face_id: str):
            called["get_repo"] = True
            assert face_id == "F-LAYER-001"
            return face

        monkeypatch.setattr(
            face_service_module,
            "list_faces_repo",
            fake_list_repo,
            raising=False,
        )
        monkeypatch.setattr(
            face_service_module,
            "get_face_repo",
            fake_get_repo,
            raising=False,
        )
        service = FaceService()
        list_res = await asyncio.wait_for(
            service.list_faces(query=query),
            timeout=1,
        )
        get_res = await asyncio.wait_for(service.get_face("F-LAYER-001"), timeout=1)

        assert called["list_repo"] is True
        assert called["get_repo"] is True
        assert list_res[0].FaceID == "F-LAYER-001"
        assert get_res.FaceID == "F-LAYER-001"

    asyncio.run(_run())



def test_person_face_tasks_delegate_to_repositories(monkeypatch):
    async def _run():
        person = _sample_person()
        face = _sample_face()
        called = {
            "list_person_repo": False,
            "get_person_repo": False,
            "delete_person_repo": False,
            "get_face_repo": False,
            "delete_face_repo": False,
        }

        async def fake_list_person_repo():
            called["list_person_repo"] = True
            return [person]

        async def fake_get_person_repo(person_id: str):
            called["get_person_repo"] = True
            assert person_id == "P-LAYER-001"
            return person

        async def fake_delete_person_repo(person_id: str):
            called["delete_person_repo"] = True
            assert person_id == "P-LAYER-001"
            return person_id

        async def fake_get_face_repo(face_id: str):
            called["get_face_repo"] = True
            assert face_id == "F-LAYER-001"
            return face

        async def fake_delete_face_repo(face_id: str):
            called["delete_face_repo"] = True
            assert face_id == "F-LAYER-001"
            return face_id

        monkeypatch.setattr(
            person_task_module,
            "list_persons_repo",
            fake_list_person_repo,
            raising=False,
        )
        monkeypatch.setattr(
            person_task_module,
            "get_person_repo",
            fake_get_person_repo,
            raising=False,
        )
        monkeypatch.setattr(
            person_task_module,
            "delete_person_repo",
            fake_delete_person_repo,
            raising=False,
        )
        monkeypatch.setattr(
            face_task_module,
            "get_face_repo",
            fake_get_face_repo,
            raising=False,
        )
        monkeypatch.setattr(
            face_task_module,
            "delete_face_repo",
            fake_delete_face_repo,
            raising=False,
        )
        monkeypatch.setattr(
            person_task_module,
            "AsyncSession",
            lambda *args, **kwargs: (_ for _ in ()).throw(
                AssertionError("AsyncSession should not be used in person tasks")
            ),
            raising=False,
        )
        monkeypatch.setattr(
            face_task_module,
            "AsyncSession",
            lambda *args, **kwargs: (_ for _ in ()).throw(
                AssertionError("AsyncSession should not be used in face tasks")
            ),
            raising=False,
        )

        person_list_res = await asyncio.wait_for(
            person_task_module.list_persons_task(), timeout=1
        )
        person_get_res = await asyncio.wait_for(
            person_task_module.get_person_task("P-LAYER-001"), timeout=1
        )
        person_delete_res = await asyncio.wait_for(
            person_task_module.delete_person_task.original_func("P-LAYER-001"), timeout=1
        )

        face_get_res = await asyncio.wait_for(
            face_task_module.get_face_task("F-LAYER-001"), timeout=1
        )
        face_delete_res = await asyncio.wait_for(
            face_task_module.delete_face_task.original_func("F-LAYER-001"), timeout=1
        )

        assert person_list_res[0].PersonID == "P-LAYER-001"
        assert person_get_res.PersonID == "P-LAYER-001"
        assert person_delete_res == "P-LAYER-001"
        assert face_get_res.FaceID == "F-LAYER-001"
        assert face_delete_res == "F-LAYER-001"
        assert all(called.values())

    asyncio.run(_run())
