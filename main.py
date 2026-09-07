from contextlib import AsyncExitStack, asynccontextmanager

from fastapi import FastAPI

import api
from api.error_handlers import register_exception_handlers
from core import settings
from message.kafka import AiokafkaProducer
from s3.storage import S3CompatibleStorage


@asynccontextmanager
async def lifespan(app: FastAPI):
    runtime_settings = settings.AppSettings()
    storage = S3CompatibleStorage(
        endpoint_url=runtime_settings.object_storage_endpoint_url,
        public_base_url=runtime_settings.object_storage_public_base_url,
        access_key=runtime_settings.object_storage_access_key_id,
        secret_key=runtime_settings.object_storage_secret_access_key,
        region=runtime_settings.object_storage_region,
    )
    producer = AiokafkaProducer(
        bootstrap_servers=runtime_settings.kafka_bootstrap_servers,
        client_id=runtime_settings.kafka_client_id,
        send_timeout_seconds=runtime_settings.kafka_send_timeout_seconds,
    )
    async with AsyncExitStack() as stack:
        await storage.start()
        stack.push_async_callback(storage.close)

        await producer.start()
        stack.push_async_callback(producer.stop)

        app.state.object_storage = storage
        app.state.object_storage_bucket_prefix = (
            runtime_settings.object_storage_bucket_prefix
        )
        app.state.kafka_producer = producer

        yield


app = FastAPI(lifespan=lifespan)
app.include_router(api.router)
register_exception_handlers(app)
