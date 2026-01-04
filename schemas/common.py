from typing import List

from pydantic import BaseModel, Field

from .sub_image_info import SubImageInfo


class PictureQueryCondition(BaseModel):
    """GA/T 2350.5-2025 B.7 以图像搜图查询条件对象"""

    SubImage: SubImageInfo | None = Field(description="对象小图")
    Threshold: float | None = Field(description="相似度分数线")
    SubjectID: str | None = Field(description="数据标识", max_length=48)


# 以图像搜图查询条件对象列表
class PictureQueryConditionList(BaseModel):
    PictureQueryConditionObject: List[PictureQueryCondition]


class GeoRectangleType(BaseModel):
    """GA/T 2350.5-2025 B.12 检索区域对象"""

    LeftTopLongitude: float = Field(description="西北经度", decimal_places=6)
    LeftTopLatitude: float = Field(description="西北纬度", decimal_places=6)
    RightBtmLongitude: float = Field(description="东南经度", decimal_places=6)
    RightBtmLatitude: float = Field(description="东南纬度", decimal_places=6)


class DeviceSelector(BaseModel):
    """GA/T 2350.5-2025 B.13 检索设备范围对象"""

    # TODO 这里是个List，但是里面的device其实是个str，不是具有字段类型的model，所以这里直接使用List str来处理
    DeviceIDs: List[str] | None = Field(description="设备ID列表")
    DevicePlaceCode: str | None = Field(max_length=6, description="设备行政区划")


class ArchiveQueryResultBase(BaseModel):
    QueryID: str = Field(max_length=48, description="查询标识")
    RecordStartNo: int | None = Field(description="起始记录号")
    PageRecordNum: int = Field(description="本页返回记录数")
    TotalNum: int = Field(description="符合条件记录总数")
