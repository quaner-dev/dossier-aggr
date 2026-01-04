from typing import AsyncGenerator

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

import settings

engine = create_async_engine(settings.DATABASE_URL)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """异步获取数据库会话"""
    async with AsyncSession(engine) as session:
        yield session
