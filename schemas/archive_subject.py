from typing import List

from pydantic import BaseModel, Field

from .person import PersonList
from .face import FaceList


class ArchiveSubject(BaseModel):
    """GA/T 2350.5-2025 B.5 档案明细信息对象"""

    ArchiveID: str = Field(max_length=48, description="档案标识")
    PersonIDList: List[str] | None = Field(description="人员信息标识列表")
    FaceIDList: List[str] | None = Field(description="人脸信息标识列表")
    PersonObjectList: PersonList | None = Field(description="人员完整信息列表")
    FaceObjectList: FaceList | None = Field(description="人脸完整信息列表")


# 档案明细列表
class ArchiveSubjectList(BaseModel):
    ArchiveSubjectObject: List[ArchiveSubject]


# 档案明细列表结构
class ArchiveSubjectSchema(BaseModel):
    ArchiveSubjectListObject: ArchiveSubjectList
