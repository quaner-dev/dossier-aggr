import math

import pytest

import message.kafka as kafka_module


class FakeAIOKafkaProducer:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.sent = []

    async def start(self):
        pass

    async def send_and_wait(self, topic, **kwargs):
        self.sent.append((topic, kwargs))

    async def stop(self):
        pass


@pytest.mark.asyncio
async def test_producer_uses_required_delivery_and_record_contract(monkeypatch):
    monkeypatch.setattr(kafka_module, "AIOKafkaProducer", FakeAIOKafkaProducer)
    producer = kafka_module.AiokafkaProducer(
        bootstrap_servers="kafka:9092",
        client_id="test",
    )

    assert producer._producer.kwargs == {
        "bootstrap_servers": "kafka:9092",
        "client_id": "test",
        "acks": "all",
        "enable_idempotence": True,
    }

    await producer.send(topic="viid.faces.v1", payload={"名称": "张三"})
    topic, record = producer._producer.sent[0]
    assert topic == "viid.faces.v1"
    assert record == {
        "value": '{"名称":"张三"}'.encode(),
        "headers": [("content-type", b"application/json")],
    }


@pytest.mark.asyncio
async def test_producer_rejects_non_standard_nan(monkeypatch):
    monkeypatch.setattr(kafka_module, "AIOKafkaProducer", FakeAIOKafkaProducer)
    producer = kafka_module.AiokafkaProducer(
        bootstrap_servers="kafka:9092",
        client_id="test",
    )

    with pytest.raises(ValueError):
        await producer.send(topic="test", payload={"value": math.nan})
