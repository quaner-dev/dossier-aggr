from pydantic import BaseModel, Field

import base
from .common import PictureQueryConditionList, GeoRectangleType, DeviceSelector


# TODO
class ArchiveQueryBase(BaseModel):
    QueryID: str = Field(max_length=48, description="查询标识")
    MaxNumRecordReturn: int | None = Field(description="最多返回记录数")
    PageRecordNum: int | None = Field(description="每页记录数")
    RecordStartNo: int | None = Field(description="起始记录号")
    BeginTime: base.enums.VIIDDateTime | None = Field(description="开始时间")
    EndTime: base.enums.VIIDDateTime | None = Field(description="结束时间")
    GeoRectangle: GeoRectangleType | None = Field(description="检索的区域范围")
    DeviceSelected: DeviceSelector = Field(description="检索的设备范围")
    Sort: str | None = Field(description="排序依据")


class ArchiveQuery(ArchiveQueryBase):
    """GA/T 2350.5-2025 B.6 档案查询对象"""

    PictureQueryCondition: PictureQueryConditionList | None = Field(
        description="以图像搜图查询"
    )


# 档案查询请求结构
class ArchiveQuerySchema(BaseModel):
    ArchiveQueryObject: ArchiveQuery
