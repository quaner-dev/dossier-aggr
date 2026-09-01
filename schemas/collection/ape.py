from sqlmodel import SQLModel

from domain.collection import APE


class APEList(SQLModel):
    APEObject: list[APE]


class APEListSchema(SQLModel):
    APEListObject: APEList
