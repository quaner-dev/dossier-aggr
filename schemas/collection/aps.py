from sqlmodel import SQLModel

from domain.collection import APS


class APSList(SQLModel):
    APSObject: list[APS]


class APSListSchema(SQLModel):
    APSListObject: APSList
