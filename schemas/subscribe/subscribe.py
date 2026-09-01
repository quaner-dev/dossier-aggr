from sqlmodel import SQLModel

from domain.subscribe import Subscribe


class SubscribeList(SQLModel):
    SubscribeObject: list[Subscribe]


class SubscribeListSchema(SQLModel):
    SubscribeListObject: SubscribeList
