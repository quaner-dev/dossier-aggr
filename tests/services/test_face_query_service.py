import asyncio

import pytest
from models import Face
from models.common import enums
from services.face.face import FaceService
import services.face.face as face_service_module


def _sample_face() -> Face:
    return Face(
        FaceID="F-SVC-001",
        InfoKind=enums.InfoKindEnum.AutoCollect,
        SourceID="SRC-SVC-001",
        DeviceID="DEV-SVC-001",
        LeftTopX=10,
        LeftTopY=20,
        RightBtmX=100,
        RightBtmY=200,
        SubImageList=None,
    )


def test_list_faces_reads_from_repository(monkeypatch: pytest.MonkeyPatch):
    async def _run():
        called = {"list_repo": False}

        async def fake_list_repo():
            called["list_repo"] = True
            return [_sample_face()]

        monkeypatch.setattr(
            face_service_module,
            "list_faces_repo",
            fake_list_repo,
            raising=False,
        )
        service = FaceService()
        result = await service.list_faces()

        assert len(result) == 1
        assert called["list_repo"] is True

    asyncio.run(_run())


def test_face_service_write_dispatch_routes_single_and_batch(monkeypatch: pytest.MonkeyPatch):
    async def _run():
        face = _sample_face()
        called: list[tuple[str, dict]] = []

        class _Task:
            def __init__(self, name: str):
                self.task_name = name

        async def fake_dispatch(task, **kwargs):
            called.append((task.task_name, kwargs))
            return None

        monkeypatch.setattr(
            face_service_module,
            "dispatch_and_wait",
            fake_dispatch,
            raising=False,
        )
        monkeypatch.setattr(
            face_service_module,
            "update_face_task",
            _Task("update_face_task"),
            raising=False,
        )
        monkeypatch.setattr(
            face_service_module,
            "update_faces_task",
            _Task("update_faces_task"),
            raising=False,
        )
        monkeypatch.setattr(
            face_service_module,
            "delete_face_task",
            _Task("delete_face_task"),
            raising=False,
        )
        monkeypatch.setattr(
            face_service_module,
            "delete_faces_task",
            _Task("delete_faces_task"),
            raising=False,
        )

        service = FaceService()
        await service.update_face(face)
        await service.update_faces([face])
        await service.delete_face("F-SVC-001")
        await service.delete_faces(["F-SVC-001"])

        assert called == [
            ("update_face_task", {"face": face}),
            ("update_faces_task", {"faces": [face]}),
            ("delete_face_task", {"face_id": "F-SVC-001"}),
            ("delete_faces_task", {"face_ids": ["F-SVC-001"]}),
        ]

    asyncio.run(_run())
