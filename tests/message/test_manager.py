import asyncio

import pytest
from message.manager import MessageManager, MessageUnavailableError


class FakeStorage:
    async def start(self):
        pass

    async def upload(self, *, bucket, content, content_type):
        return "path"

    async def close(self):
        pass


class FakeProducer:
    def __init__(self, fail=False):
        self.sent = []
        self.fail = fail

    async def start(self):
        pass

    async def send(self, *, topic, payload):
        if self.fail:
            raise RuntimeError("down")
        self.sent.append((topic, payload))

    async def stop(self):
        pass


@pytest.mark.asyncio
async def test_enqueue_and_workers_send_once():
    producer = FakeProducer()
    manager = MessageManager(
        storage=FakeStorage(), producer=producer, storage_workers=1, kafka_workers=1
    )
    await manager.start()
    payload = {"A": 1}
    manager.enqueue(
        topic="viid.faces.v1",
        request_path="/VIID/Faces",
        business_ids=["x"],
        payload=payload,
    )
    await manager.stop()
    assert producer.sent == [("viid.faces.v1", payload)]


def test_full_queue_returns_503():
    manager = MessageManager(
        storage=FakeStorage(), producer=FakeProducer(), input_queue_max_items=1
    )
    manager.accepting = True
    manager.enqueue(topic="t", request_path="p", business_ids=[], payload={})
    with pytest.raises(MessageUnavailableError) as exc:
        manager.enqueue(topic="t", request_path="p", business_ids=[], payload={})
    assert exc.value.status_code == 503


@pytest.mark.asyncio
async def test_kafka_failure_is_dropped():
    manager = MessageManager(
        storage=FakeStorage(),
        producer=FakeProducer(fail=True),
        storage_workers=1,
        kafka_workers=1,
    )
    await manager.start()
    manager.enqueue(topic="t", request_path="p", business_ids=[], payload={})
    await asyncio.wait_for(manager.stop(timeout=1), timeout=2)
