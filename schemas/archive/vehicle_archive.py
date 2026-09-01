from sqlmodel import Field, SQLModel

from domain.archive import VehicleArchive as VehicleArchiveDomain

from ..common import SubImageInfoList


class VehicleArchive(VehicleArchiveDomain):
    SourceIDList: list[str] | None = Field(default=None, description="档案数据来源列表")
    SubImageList: SubImageInfoList = Field(description="图片信息列表")


class VehicleArchiveList(SQLModel):
    VehicleArchiveObject: list[VehicleArchive]


class VehicleArchiveListSchema(SQLModel):
    VehicleArchiveListObject: VehicleArchiveList
