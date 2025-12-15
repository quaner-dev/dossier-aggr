import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from taskiq_aio_pika import AioPikaBroker

import settings


broker = AioPikaBroker(
    f"amqp://{settings.RABBITMQ_USERNAME}:{settings.RABBITMQ_PASSWORD}@{settings.RABBITMQ_IP}:{settings.RABBITMQ_PORT}"
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not broker.is_worker_process:
        logging.info("Starting broker")
        await broker.startup()
    yield
    if not broker.is_worker_process:
        logging.info("Shutting down broker")
        await broker.shutdown()
