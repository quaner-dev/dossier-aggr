from sqlmodel import Field, SQLModel  # type: ignore

import base.enums as enums


class ArchiveBase(SQLModel):
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
