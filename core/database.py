from collections.abc import AsyncGenerator
from typing import Any

from sqlalchemy.engine import make_url
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from core import settings


def _engine_kwargs(database_url: str) -> dict[str, Any]:
    if make_url(database_url).drivername.startswith("sqlite"):
        return {}

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


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """异步获取数据库会话"""
    async with AsyncSession(engine) as session:
        yield session
