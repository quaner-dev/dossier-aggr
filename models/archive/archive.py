from sqlalchemy import JSON, Column, UniqueConstraint
from sqlmodel import Field

from domain.archive.archive import Archive as ArchiveDomain
from schemas import FeatureInfoList, SubImageInfoList


class Archive(ArchiveDomain, table=True):
    __table_args__ = (UniqueConstraint("ArchiveID"),)

    id: int | None = Field(default=None, primary_key=True, exclude=True)
    SourceIDList: list[str] | None = Field(
        default=None, description="档案数据来源列表", sa_column=Column(JSON)
    )
    CenterFeatureList: FeatureInfoList | None = Field(
        default=None, description="档案中心特征列表", sa_column=Column(JSON)
    )
    SubImageList: SubImageInfoList = Field(
        description="图片信息列表", sa_column=Column(JSON)
    )
