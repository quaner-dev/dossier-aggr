from sqlalchemy import Column, JSON
from sqlmodel import SQLModel, Field

from ..common import enums
from ..common.feature_info import FeatureInfoList
from ..common.sub_image_info import SubImageInfoList


class Archive(SQLModel, table=True):
    """GA/T 2350.5-2025 B.3 人员档案基础信息对象"""

    id: int | None = Field(default=None, primary_key=True, exclude=True)

    ArchiveID: str = Field(max_length=48, description="档案标识", unique=True)
    ArchiveLibraryID: str | None = Field(
        default=None, max_length=48, description="所属目标档案库"
    )
    CreateTime: enums.VIIDDateTime = Field(description="档案创建时间")
    UpdateTime: enums.VIIDDateTime = Field(description="档案更新时间")
    SourceIDList: list[str] | None = Field(
        default=None,
        description="档案数据来源列表",
        sa_column=Column(JSON),
    )
    CenterFeatureList: FeatureInfoList | None = Field(
        default=None,
        description="档案中心特征列表",
        sa_column=Column(JSON),
    )
    Similaritydegree: float | None = Field(default=None, description="相似度")
    Confidence: float | None = Field(default=None, description="可信度")
    SubImageList: SubImageInfoList = Field(
        description="图片信息列表",
        sa_column=Column(JSON),
    )


class ArchiveList(SQLModel):
    """GA/T 2350.5-2025 B.3 人员档案基础信息对象列表"""

    ArchiveObject: list[Archive]


class ArchiveListSchema(SQLModel):
    """GA/T 2350.5-2025 A.10 `ArchiveListObject` 请求/响应包装"""

    ArchiveListObject: ArchiveList
