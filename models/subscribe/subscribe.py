from sqlalchemy import UniqueConstraint
from sqlmodel import Field

from domain.subscribe.subscribe import Subscribe as SubscribeDomain


class Subscribe(SubscribeDomain, table=True):
    __table_args__ = (UniqueConstraint("SubscribeID"),)

    id: int | None = Field(default=None, primary_key=True, exclude=True)
