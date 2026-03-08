import asyncio

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
