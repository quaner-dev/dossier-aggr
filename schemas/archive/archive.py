from sqlmodel import Field, SQLModel

from domain.archive import Archive as ArchiveDomain

from ..common import FeatureInfoList, SubImageInfoList


class Archive(ArchiveDomain):
    SourceIDList: list[str] | None = Field(default=None, description="档案数据来源列表")
    CenterFeatureList: FeatureInfoList | None = Field(
        default=None, description="档案中心特征列表"
    )
    SubImageList: SubImageInfoList = Field(description="图片信息列表")


class ArchiveList(SQLModel):
    ArchiveObject: list[Archive]


class ArchiveListSchema(SQLModel):
    ArchiveListObject: ArchiveList
