import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from taskiq import AsyncBroker, InMemoryBroker
from taskiq_aio_pika import AioPikaBroker
from taskiq_redis import RedisAsyncResultBackend

from core import settings


broker: AsyncBroker

if settings.ENV == "dev":
    broker = InMemoryBroker()
else:
    if not settings.TASKIQ_RESULT_BACKEND_URL:
        raise RuntimeError("TASKIQ_RESULT_BACKEND_URL is required when ENV is not dev")

    broker = AioPikaBroker(
        f"amqp://{settings.RABBITMQ_USERNAME}:{settings.RABBITMQ_PASSWORD}"
        f"@{settings.RABBITMQ_IP}:{settings.RABBITMQ_PORT}",
    ).with_result_backend(RedisAsyncResultBackend(settings.TASKIQ_RESULT_BACKEND_URL))


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not broker.is_worker_process:
        logging.info("Starting broker")
        await broker.startup()
    yield
    if not broker.is_worker_process:
        logging.info("Shutting down broker")
        await broker.shutdown()
