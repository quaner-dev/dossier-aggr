from collections.abc import Mapping, Sequence
from typing import Any, cast

from sqlmodel import delete, select
from sqlmodel.ext.asyncio.session import AsyncSession

from core import exceptions
from core.database import engine
from models import SubscribeNotification

_FILTERABLE_NOTIFICATION_FIELDS = {
    "NotificationID",
    "SubscribeID",
    "Title",
    "TriggerTime",
    "InfoIDs",
    "DeviceList",
    "DataClassTabObjectList",
    "ExecuteOperation",
}


def _normalize_filter_value(field: str, value: str) -> str | int:
    if field == "ExecuteOperation":
        try:
            return int(value)
        except ValueError as exc:
            raise exceptions.InvalidParameterError(
                detail=f"{field} must be an integer value"
            ) from exc
    return value


async def list_subscribe_notifications_repo(
    filters: Mapping[str, str] | None = None,
) -> Sequence[SubscribeNotification]:
    """根据过滤条件查询通知记录"""
    async with AsyncSession(engine) as session:
        statement = select(SubscribeNotification)
        for field, value in (filters or {}).items():
            if field not in _FILTERABLE_NOTIFICATION_FIELDS:
                raise exceptions.InvalidParameterError(
                    detail=f"{field} is not a supported query field"
                )
            statement = statement.where(
                getattr(SubscribeNotification, field)
                == _normalize_filter_value(field, value)
            )

        notifications = (await session.exec(statement)).all()
        if not notifications:
            raise exceptions.DataNotFoundError(
                detail="No SubscribeNotification data exist"
            )
        return notifications


async def create_subscribe_notifications_repo(
    subscribe_notifications: list[SubscribeNotification],
) -> list[SubscribeNotification]:
    """创建通知记录"""
    async with AsyncSession(engine) as session:
        session.add_all(subscribe_notifications)
        await session.commit()
        for notification in subscribe_notifications:
            await session.refresh(notification)
    return subscribe_notifications


async def delete_subscribe_notifications_repo(notification_ids: list[str]) -> list[str]:
    """批量删除通知记录"""
    async with AsyncSession(engine) as session:
        _ = await session.exec(
            delete(SubscribeNotification).where(
                cast(Any, SubscribeNotification.NotificationID).in_(notification_ids)
            )
        )
        await session.commit()
    return notification_ids
