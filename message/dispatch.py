"""Kafka message transport primitives.

This module deliberately contains no object-storage imports or configuration.
The request-level composition of image uploads and Kafka delivery belongs to
``services.message_dispatch``.
"""

from typing import Any

from fastapi import HTTPException

from .kafka import AiokafkaProducer

FACES_TOPIC = "viid.faces.v1"
PERSONS_TOPIC = "viid.persons.v1"
SUBSCRIBE_NOTIFICATIONS_TOPIC = "viid.subscribe-notifications.v1"
MOTOR_VEHICLES_TOPIC = "viid.motor-vehicles.v1"
NON_MOTOR_VEHICLES_TOPIC = "viid.non-motor-vehicles.v1"


class MessageUnavailableError(HTTPException):
    """Raised when the message transport is not available."""

    def __init__(self, detail: str = "消息接入服务暂不可用") -> None:
        super().__init__(status_code=503, detail=detail)


async def publish_message(
    *, producer: AiokafkaProducer, topic: str, payload: dict[str, Any]
) -> None:
    """Publish one already-prepared payload to Kafka."""

    await producer.send(topic=topic, payload=payload)


__all__ = [
    "FACES_TOPIC",
    "PERSONS_TOPIC",
    "SUBSCRIBE_NOTIFICATIONS_TOPIC",
    "MOTOR_VEHICLES_TOPIC",
    "NON_MOTOR_VEHICLES_TOPIC",
    "MessageUnavailableError",
    "publish_message",
]
