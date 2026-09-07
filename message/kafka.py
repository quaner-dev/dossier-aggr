"""Kafka producer 客户端。"""

import asyncio
import json
from typing import Any

from aiokafka import AIOKafkaProducer


class AiokafkaProducer:
    def __init__(
        self,
        *,
        bootstrap_servers: str,
        client_id: str,
        send_timeout_seconds: float = 5,
    ) -> None:
        self._producer = AIOKafkaProducer(
            bootstrap_servers=bootstrap_servers,
            client_id=client_id,
            acks="all",
            enable_idempotence=True,
        )
        self._timeout = send_timeout_seconds

    async def start(self) -> None:
        await self._producer.start()

    async def send(self, *, topic: str, payload: dict[str, Any]) -> None:
        await asyncio.wait_for(
            self._producer.send_and_wait(
                topic,
                value=json.dumps(
                    payload,
                    ensure_ascii=False,
                    separators=(",", ":"),
                    allow_nan=False,
                ).encode("utf-8"),
                headers=[("content-type", b"application/json")],
            ),
            timeout=self._timeout,
        )

    async def stop(self) -> None:
        await self._producer.stop()
