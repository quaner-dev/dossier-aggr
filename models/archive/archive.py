from sqlmodel import SQLModel, Field

from ..common import enums


class Archive(SQLModel, table=True):
    """GA/T 2350.5-2025 B.3 人员档案基础信息对象"""

    id: int | None = Field(default=None, primary_key=True, exclude=True)

    ArchiveID: str = Field(max_length=48, description="档案标识", unique=True)
    ArchiveLibraryID: str | None = Field(max_length=48, description="所属目标档案库")
    IDType: str | None = Field(max_length=3, description="证件类型")
    IDNumber: str | None = Field(max_length=30, description="证件编号")
    Name: str | None = Field(max_length=50, description="姓名")
    BirthTime: enums.VIIDDateTime | None = Field(description="出生日期")
    CreateTime: enums.VIIDDateTime = Field(description="档案创建时间")
    UpdateTime: enums.VIIDDateTime = Field(description="档案更新时间")

    ImageID: str | None = Field(description="图像标识", max_length=41)


# 人员档案基础信息对象列表
class ArchiveList(SQLModel):
    ArchiveObject: list[Archive]


# 人员档案基础信息对象列表结构
class ArchiveListSchema(SQLModel):
    ArchiveListObject: ArchiveList
