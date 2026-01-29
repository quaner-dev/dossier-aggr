from sqlmodel import SQLModel, Field

from .sub_image_info import SubImageInfo
from .enums import (
    OnlyRealNameArchiveEnum,
    GenderTypeEnum,
    ColorTypeEnum,
    VehicleBrandTypeEnum,
)


class PictureQueryCondition(SQLModel):
    """GA/T 2350.5-2025 B.7 以图像搜图查询条件对象"""

    SubImage: SubImageInfo | None = Field(description="对象小图")
    Threshold: float | None = Field(description="相似度分数线")
    SubjectID: str | None = Field(description="数据标识", max_length=48)


# 以图像搜图查询条件对象列表
class PictureQueryConditionList(SQLModel):
    PictureQueryConditionObject: list[PictureQueryCondition]


class GeoRectangleType(SQLModel):
    """GA/T 2350.5-2025 B.12 检索区域对象"""

    LeftTopLongitude: float = Field(description="西北经度", decimal_places=6)
    LeftTopLatitude: float = Field(description="西北纬度", decimal_places=6)
    RightBtmLongitude: float = Field(description="东南经度", decimal_places=6)
    RightBtmLatitude: float = Field(description="东南纬度", decimal_places=6)


class DeviceSelector(SQLModel):
    """GA/T 2350.5-2025 B.13 检索设备范围对象"""

    # TODO 这里是个List，但是里面的device其实是个str，不是具有字段类型的model，所以这里直接使用List str来处理
    DeviceIDs: list[str] | None = Field(description="设备ID列表")
    DevicePlaceCode: str | None = Field(max_length=6, description="设备行政区划")


class FieldsType(SQLModel):
    ArchiveLibraryID: str | None = Field(description="目标档案库标识", max_length=48)
    IDNumbers: str | None = Field(description="证件编号列表", max_length=1024)
    Names: str | None = Field(description="姓名列表", max_length=1024)
    ArchiveIDList: list[str] | None = Field(description="档案标识列表")
    OnlyRealNameArchive: OnlyRealNameArchiveEnum | None = Field(
        description="档案类型过滤"
    )
    PlaceCode: str | None = Field(description="行政区划范围", max_length=6)
    GenderCode: GenderTypeEnum | None = Field(description="性别代码")
    AgeUpLimit: int | None = Field(description="年龄上限")
    AgeLowerLimit: int | None = Field(description="年龄下限")
    PlateNos: str | None = Field(description="车牌号", max_length=1024)
    PlateColor: ColorTypeEnum | None = Field(description="车牌颜色")
    VehicleClass: str | None = Field(description="车辆类型", max_length=3)
    VehicleBrand: VehicleBrandTypeEnum | None = Field(
        description="车辆品牌", max_length=3
    )
    VehicleModel: str | None = Field(description="车辆型号", max_length=32)
    VehicleColor: ColorTypeEnum | None = Field(description="车辆颜色")
    VehicleStyles: str | None = Field(description="车辆年款", max_length=16)
