import asyncio

from models import Face
from models.common import enums
from tasks.face import face as face_tasks
from tasks.person import person as person_tasks


def test_delete_person_task_delegates_to_repository(monkeypatch):
    async def _run():
        called = {"delete_person_repo": False}

        async def fake_delete_person_repo(person_id: str):
            called["delete_person_repo"] = True
            assert person_id == "P-001"
            return person_id

        monkeypatch.setattr(
            person_tasks,
            "delete_person_repo",
            fake_delete_person_repo,
            raising=False,
        )

        result = await person_tasks.delete_person_task.original_func(person_id="P-001")
        assert result == "P-001"
        assert called["delete_person_repo"] is True

    asyncio.run(_run())


def test_update_faces_task_delegates_to_repository(monkeypatch):
    async def _run():
        called = {"update_faces_repo": False}
        faces = [
            Face(
                FaceID="F-001",
                InfoKind=enums.InfoKindEnum.AutoCollect,
                SourceID="SRC-001",
                DeviceID="DEV-001",
                LeftTopX=10,
                LeftTopY=20,
                RightBtmX=100,
                RightBtmY=200,
                SubImageList=None,
            )
        ]

        async def fake_update_faces_repo(faces: list[Face]):
            called["update_faces_repo"] = True
            assert len(faces) == 1
            assert faces[0].FaceID == "F-001"
            return faces

        monkeypatch.setattr(
            face_tasks,
            "update_faces_repo",
            fake_update_faces_repo,
            raising=False,
        )

        result = await face_tasks.update_faces_task.original_func(faces=faces)
        assert len(result) == 1
        assert result[0].FaceID == "F-001"
        assert called["update_faces_repo"] is True

    asyncio.run(_run())


def test_delete_face_task_delegates_to_repository(monkeypatch):
    async def _run():
        called = {"delete_face_repo": False}

        async def fake_delete_face_repo(face_id: str):
            called["delete_face_repo"] = True
            assert face_id == "F-001"
            return face_id

        monkeypatch.setattr(
            face_tasks,
            "delete_face_repo",
            fake_delete_face_repo,
            raising=False,
        )

        result = await face_tasks.delete_face_task.original_func(face_id="F-001")
        assert result == "F-001"
        assert called["delete_face_repo"] is True

    asyncio.run(_run())


def test_delete_faces_task_delegates_to_repository(monkeypatch):
    async def _run():
        called = {"delete_faces_repo": False}

        async def fake_delete_faces_repo(face_ids: list[str]):
            called["delete_faces_repo"] = True
            assert face_ids == ["F-001", "F-002"]
            return face_ids

        monkeypatch.setattr(
            face_tasks,
            "delete_faces_repo",
            fake_delete_faces_repo,
            raising=False,
        )

        result = await face_tasks.delete_faces_task.original_func(
            face_ids=["F-001", "F-002"]
        )
        assert result == ["F-001", "F-002"]
        assert called["delete_faces_repo"] is True

    asyncio.run(_run())
