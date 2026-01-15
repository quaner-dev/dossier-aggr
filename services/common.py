from fastapi import Depends
from database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession


class BaseService:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session
