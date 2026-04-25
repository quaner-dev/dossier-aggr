from sqlalchemy import Column, JSON
from sqlmodel import SQLModel, Field

from ..common import enums
from ..common.sub_image_info import SubImageInfoList


class VehicleArchive(SQLModel, table=True):
    """GA/T 2350.5-2025 B.4 车辆档案基础信息对象"""

    id: int | None = Field(default=None, primary_key=True, exclude=True)

    ArchiveID: str = Field(max_length=48, description="档案标识", unique=True)
    ArchiveLibraryID: str | None = Field(
        default=None, max_length=48, description="所属目标档案库"
    )
    PlateNo: str = Field(max_length=16, description="车牌号码")
    PlateColor: enums.ColorTypeEnum = Field(description="车牌颜色")
    VehicleClass: str | None = Field(default=None, max_length=3, description="车辆类型")
    VehicleBrand: enums.VehicleBrandTypeEnum | None = Field(
        default=None, description="车辆品牌"
    )
    VehicleModel: str | None = Field(default=None, max_length=32, description="车辆型号")
    VehicleColor: enums.ColorTypeEnum | None = Field(default=None, description="车辆颜色")
    VehicleStyles: str | None = Field(default=None, max_length=16, description="车辆年款")
    CreateTime: enums.VIIDDateTime = Field(description="档案创建时间")
    UpdateTime: enums.VIIDDateTime = Field(description="档案更新时间")
    SourceIDList: list[str] | None = Field(
        default=None,
        description="档案数据来源列表",
        sa_column=Column(JSON),
    )
    SubImageList: SubImageInfoList = Field(
        description="图片信息列表",
        sa_column=Column(JSON),
    )


class VehicleArchiveList(SQLModel):
    VehicleArchiveObject: list[VehicleArchive]


class VehicleArchiveListSchema(SQLModel):
    VehicleArchiveListObject: VehicleArchiveList
