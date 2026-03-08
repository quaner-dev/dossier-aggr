from sqlalchemy import Column, JSON
from sqlmodel import SQLModel, Field

from ..person.person import PersonList
from ..face.face import FaceList


class ArchiveSubject(SQLModel, table=True):
    """GA/T 2350.5-2025 B.5 档案明细信息对象"""

    id: int | None = Field(default=None, primary_key=True, exclude=True)

    ArchiveID: str = Field(max_length=48, description="档案标识", unique=True)
    PersonIDList: list[str] | None = Field(
        default=None,
        description="人员信息标识列表",
        sa_column=Column(JSON),
    )
    FaceIDList: list[str] | None = Field(
        default=None,
        description="人脸信息标识列表",
        sa_column=Column(JSON),
    )
    PersonObjectList: PersonList | None = Field(
        default=None,
        description="人员完整信息列表",
        sa_column=Column(JSON),
    )
    FaceObjectList: FaceList | None = Field(
        default=None,
        description="人脸完整信息列表",
        sa_column=Column(JSON),
    )

    ImageID: str | None = Field(default=None, description="图像标识", max_length=41)


# 档案明细列表
class ArchiveSubjectList(SQLModel):
    ArchiveSubjectObject: list[ArchiveSubject]


# 档案明细列表结构
class ArchiveSubjectSchema(SQLModel):
    ArchiveSubjectListObject: ArchiveSubjectList
