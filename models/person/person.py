from sqlalchemy import JSON, Column, UniqueConstraint
from sqlmodel import Field

from domain.person.person import Person as PersonDomain
from schemas import SubImageInfoList


class Person(PersonDomain, table=True):
    __table_args__ = (UniqueConstraint("PersonID"),)

    id: int | None = Field(default=None, primary_key=True, exclude=True)
    SubImageList: SubImageInfoList | None = Field(
        default=None, description="图像列表", sa_column=Column(JSON)
    )
