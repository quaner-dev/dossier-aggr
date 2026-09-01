from sqlalchemy import JSON, Column, UniqueConstraint
from sqlmodel import Field

from domain.archive.vehicle_archive import VehicleArchive as VehicleArchiveDomain
from schemas import SubImageInfoList


class VehicleArchive(VehicleArchiveDomain, table=True):
    __table_args__ = (UniqueConstraint("ArchiveID"),)

    id: int | None = Field(default=None, primary_key=True, exclude=True)
    SourceIDList: list[str] | None = Field(
        default=None, description="档案数据来源列表", sa_column=Column(JSON)
    )
    SubImageList: SubImageInfoList = Field(
        description="图片信息列表", sa_column=Column(JSON)
    )
