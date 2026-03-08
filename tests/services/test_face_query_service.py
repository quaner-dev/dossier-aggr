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
