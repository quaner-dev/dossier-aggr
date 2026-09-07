import httpx
import pytest

from main import app
from message.manager import MessageUnavailableError, get_message_manager
from schemas import FaceList, FaceListObjectSchema
from tests.test_api_face import _sample_faces
from tests.type_helpers import FakeMessageManager


@pytest.mark.asyncio
async def test_faces_post_enqueues_and_returns_success():
    manager = FakeMessageManager()

    async def manager_dependency():
        return manager

    payload = FaceListObjectSchema(
        FaceListObject=FaceList(FaceObject=_sample_faces())
    ).model_dump(mode="json")
    app.dependency_overrides[get_message_manager] = manager_dependency
    try:
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(
            transport=transport, base_url="http://test"
        ) as client:
            response = await client.post("/VIID/Faces", json=payload)
    finally:
        app.dependency_overrides.pop(get_message_manager, None)

    assert response.status_code == 200
    assert manager.enqueued[0]["payload"] == payload
    assert manager.enqueued[0]["topic"] == "viid.faces.v1"


@pytest.mark.asyncio
async def test_faces_post_returns_protocol_503_when_queue_rejects():
    class RejectingManager:
        def enqueue(self, **kwargs):
            raise MessageUnavailableError("消息接入队列已满，请稍后重试")

    payload = FaceListObjectSchema(
        FaceListObject=FaceList(FaceObject=_sample_faces())
    ).model_dump(mode="json")

    async def manager_dependency():
        return RejectingManager()

    app.dependency_overrides[get_message_manager] = manager_dependency
    try:
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(
            transport=transport, base_url="http://test"
        ) as client:
            response = await client.post("/VIID/Faces", json=payload)
    finally:
        app.dependency_overrides.pop(get_message_manager, None)

    assert response.status_code == 503
    status = response.json()["ResponseStatusListObject"]["ResponseStatusObject"][0]
    assert status["StatusCode"] == "503"
    assert status["StatusString"] == "消息接入队列已满，请稍后重试"


@pytest.mark.asyncio
async def test_invalid_faces_payload_does_not_enqueue():
    manager = FakeMessageManager()

    async def manager_dependency():
        return manager

    app.dependency_overrides[get_message_manager] = manager_dependency
    try:
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(
            transport=transport, base_url="http://test"
        ) as client:
            response = await client.post("/VIID/Faces", json={})
    finally:
        app.dependency_overrides.pop(get_message_manager, None)

    assert response.status_code == 400
    assert manager.enqueued == []
