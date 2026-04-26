from sqlmodel import SQLModel, Field

from ..common import enums
from ..common.common import (
    GeoRectangleType,
    DeviceSelector,
    FieldsType,
    PictureQueryConditionList,
)


class ArchiveQuery(SQLModel):
    """GA/T 2350.5-2025 B.6 档案查询对象"""

    QueryID: str = Field(max_length=48, description="查询标识")
    MaxNumRecordReturn: int | None = Field(default=None, description="最多返回记录数")
    PageRecordNum: int | None = Field(default=None, description="每页记录数")
    RecordStartNo: int | None = Field(default=None, description="起始记录号")
    PictureQueryCondition: PictureQueryConditionList | None = Field(
        default=None, description="以图像搜图查询条件"
    )
    BeginTime: enums.VIIDDateTime | None = Field(default=None, description="开始时间")
    EndTime: enums.VIIDDateTime | None = Field(default=None, description="结束时间")
    GeoRectangle: GeoRectangleType | None = Field(
        default=None, description="检索的区域范围"
    )
    DeviceSelected: DeviceSelector | None = Field(
        default=None, description="检索的设备范围"
    )
    Sort: str | None = Field(default=None, description="排序依据")
    Fields: FieldsType | None = Field(default=None, description="其他结构化筛查条件")


class ArchiveQuerySchema(SQLModel):
    """GA/T 2350.5-2025 A.9/A.11 `ArchiveQueryObject` 查询请求包装"""

    ArchiveQueryObject: ArchiveQuery
