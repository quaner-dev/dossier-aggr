from sqlmodel import SQLModel, Field

from ..person.person import PersonList
from ..face.face import FaceList


class ArchiveSubject(SQLModel):
    """GA/T 2350.5-2025 B.5 档案明细信息对象"""

    ArchiveID: str = Field(max_length=48, description="档案标识")
    PersonIDList: list[str] | None = Field(description="人员信息标识列表")
    FaceIDList: list[str] | None = Field(description="人脸信息标识列表")
    PersonObjectList: PersonList | None = Field(description="人员完整信息列表")
    FaceObjectList: FaceList | None = Field(description="人脸完整信息列表")

    ImageID: str | None = Field(description="图像标识", max_length=41)


# 档案明细列表
class ArchiveSubjectList(SQLModel):
    ArchiveSubjectObject: list[ArchiveSubject]


# 档案明细列表结构
class ArchiveSubjectSchema(SQLModel):
    ArchiveSubjectListObject: ArchiveSubjectList
