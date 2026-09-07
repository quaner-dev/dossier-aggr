import pytest
from fastapi import FastAPI

import main


class FakeStorage:
    async def start(self):
        pass

    async def upload(self, *, bucket, content, content_type):
        return "path"

    async def close(self):
        pass


class FakeProducer:
    async def start(self):
        pass

    async def send(self, *, topic, payload):
        pass

    async def stop(self):
        pass


@pytest.mark.asyncio
async def test_lifespan_starts_and_stops_message_manager(monkeypatch):
    monkeypatch.setenv("OBJECT_STORAGE_PUBLIC_BASE_URL", "https://images.test")
    monkeypatch.setattr(main, "S3CompatibleStorage", lambda **kwargs: FakeStorage())
    monkeypatch.setattr(main, "AiokafkaProducer", lambda **kwargs: FakeProducer())
    app = FastAPI()

    async with main.lifespan(app):
        assert app.state.message_manager.accepting is True

    assert app.state.message_manager.accepting is False
