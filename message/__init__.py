"""消息接入基础设施。"""

from .dispatch import (
    FACES_TOPIC,
    MOTOR_VEHICLES_TOPIC,
    NON_MOTOR_VEHICLES_TOPIC,
    PERSONS_TOPIC,
    SUBSCRIBE_NOTIFICATIONS_TOPIC,
    MessageUnavailableError,
    publish_message,
)
from .kafka import AiokafkaProducer

__all__ = [
    "FACES_TOPIC",
    "MOTOR_VEHICLES_TOPIC",
    "NON_MOTOR_VEHICLES_TOPIC",
    "PERSONS_TOPIC",
    "SUBSCRIBE_NOTIFICATIONS_TOPIC",
    "MessageUnavailableError",
    "publish_message",
    "AiokafkaProducer",
]
