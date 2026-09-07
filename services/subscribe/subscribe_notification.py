from collections.abc import Sequence
from typing import Any
from fastapi import Request
from core import settings
from message.kafka import publish_message
from message.dispatch import MessageUnavailableError
from services.image_upload import transform_images

from domain import SubscribeNotification as SubscribeNotificationData
from models import SubscribeNotification
from repo.subscribe.subscribe_notification import (
    create_subscribe_notifications_repo,
    delete_subscribe_notifications_repo,
    list_subscribe_notifications_repo,
)
from services.model_conversion import to_table_models


class SubscribeNotificationService:
    """编排 GA/T 1400 订阅通知业务链路。

    通知查询、创建和删除统一委托 repo。
    """

    async def list_subscribe_notifications(
        self, filters: dict[str, str] | None = None
    ) -> list[SubscribeNotification]:
        return list(await list_subscribe_notifications_repo(filters=filters))

    async def create_subscribe_notifications(
        self,
        subscribe_notifications: Sequence[SubscribeNotificationData],
        *,
        request: Request | None = None,
        payload: dict[str, Any] | None = None,
    ) -> list[SubscribeNotification]:
        if request is not None:
            storage = getattr(request.app.state, "object_storage", None)
            producer = getattr(request.app.state, "kafka_producer", None)
            bucket = getattr(request.app.state, "object_storage_bucket_prefix", settings.OBJECT_STORAGE_BUCKET_PREFIX)
            if storage is None or producer is None or not bucket:
                raise MessageUnavailableError()
            if payload is None:
                payload = await request.json()
            await transform_images(payload, storage=storage, bucket=bucket)
            await publish_message(producer=producer, topic="viid.subscribe-notifications.v1", payload=payload)
            return []
        return list(
            await create_subscribe_notifications_repo(
                subscribe_notifications=to_table_models(
                    SubscribeNotification, subscribe_notifications
                )
            )
        )

    async def delete_subscribe_notifications(
        self, notification_ids: list[str]
    ) -> list[str]:
        return await delete_subscribe_notifications_repo(
            notification_ids=notification_ids
        )
