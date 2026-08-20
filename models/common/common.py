from sqlmodel import Field, SQLModel

from .enums import (
    ColorTypeEnum,
    VehicleBrandTypeEnum,
)
from .sub_image_info import SubImageInfo


class PictureQueryCondition(SQLModel):
    """GA/T 2350.5-2025 B.7 以图像搜图查询条件对象"""

    SubImage: SubImageInfo | None = Field(default=None, description="对象小图")
    Threshold: float | None = Field(default=None, description="相似度分数线")
    SubjectID: str | None = Field(default=None, description="数据标识", max_length=48)


class PictureQueryConditionList(SQLModel):
    """GA/T 2350.5-2025 B.7 以图像搜图查询条件对象列表"""

    PictureQueryConditionObject: list[PictureQueryCondition]


class GeoRectangleType(SQLModel):
    """GA/T 2350.5-2025 B.12 检索区域对象"""

    LeftTopLongitude: float = Field(description="西北经度", decimal_places=6)
    LeftTopLatitude: float = Field(description="西北纬度", decimal_places=6)
    RightBtmLongitude: float = Field(description="东南经度", decimal_places=6)
    RightBtmLatitude: float = Field(description="东南纬度", decimal_places=6)


class DeviceSelector(SQLModel):
    """GA/T 2350.5-2025 B.13 检索设备范围对象"""

    # 协议只定义设备标识字符串列表，没有嵌套设备对象字段。
    DeviceIDs: list[str] | None = Field(default=None, description="设备ID列表")
    DevicePlaceCode: str | None = Field(
        default=None, max_length=6, description="设备行政区划"
    )


class FieldsType(SQLModel):
    """GA/T 2350.5-2025 B.14 筛查条件对象"""

    ArchiveLibraryID: str | None = Field(
        default=None, description="目标档案库标识", max_length=48
    )
    ArchiveIDList: list[str] | None = Field(default=None, description="档案标识列表")
    PlaceCode: str | None = Field(default=None, description="行政区划范围", max_length=6)
    PlateNos: str | None = Field(default=None, description="车牌号", max_length=1024)
    PlateColor: ColorTypeEnum | None = Field(default=None, description="车牌颜色")
    VehicleClass: str | None = Field(default=None, description="车辆类型", max_length=3)
    VehicleBrand: VehicleBrandTypeEnum | None = Field(
        default=None, description="车辆品牌", max_length=3
    )
    VehicleModel: str | None = Field(default=None, description="车辆型号", max_length=32)
    VehicleColor: ColorTypeEnum | None = Field(default=None, description="车辆颜色")
    VehicleStyles: str | None = Field(default=None, description="车辆年款", max_length=16)
