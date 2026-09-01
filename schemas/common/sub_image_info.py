from sqlmodel import SQLModel

from domain.common import SubImageInfo


class SubImageInfoList(SQLModel):
    SubImageInfoObject: list[SubImageInfo]
