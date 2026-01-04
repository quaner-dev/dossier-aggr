from typing import List

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

import base
import models

from database import get_session


class SubscribeService:
    async def batch_create(
        self,
        subscribes: List[base.subscribe.SubscribeBase],
        session: AsyncSession = Depends(get_session),
    ):
        for subscribe in subscribes:
            session.add(models.subscribe.Subscribe.model_validate(subscribe))

        await session.commit()
