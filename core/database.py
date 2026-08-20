from typing import Any

from sqlalchemy.ext.asyncio import create_async_engine

from core import settings


def _engine_kwargs(database_url: str) -> dict[str, Any]:
    kwargs: dict[str, Any] = {}
    if settings.DB_POOL_SIZE is not None:
        kwargs["pool_size"] = settings.DB_POOL_SIZE
    if settings.DB_MAX_OVERFLOW is not None:
        kwargs["max_overflow"] = settings.DB_MAX_OVERFLOW
    if settings.DB_POOL_TIMEOUT_SECONDS is not None:
        kwargs["pool_timeout"] = settings.DB_POOL_TIMEOUT_SECONDS
    if settings.DB_POOL_RECYCLE_SECONDS is not None:
        kwargs["pool_recycle"] = settings.DB_POOL_RECYCLE_SECONDS
    if settings.DB_POOL_PRE_PING is not None:
        kwargs["pool_pre_ping"] = settings.DB_POOL_PRE_PING
    return kwargs


engine = create_async_engine(settings.DATABASE_URL, **_engine_kwargs(settings.DATABASE_URL))
