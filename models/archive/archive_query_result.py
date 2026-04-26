from sqlmodel import SQLModel, Field

from .archive import ArchiveList
from .vehicle_archive import VehicleArchiveList


class ArchiveQueryResult(SQLModel):
    """GA/T 2350.5-2025 B.8 档案查询结果对象"""

    QueryID: str = Field(max_length=48, description="查询标识")
    RecordStartNo: int | None = Field(description="起始记录号")
    PageRecordNum: int = Field(description="本页返回记录数")
    TotalNum: int = Field(description="符合条件记录总数")

    ArchiveListObject: ArchiveList | None = Field(
        default=None, description="人员结果档案对象列表"
    )
    VehicleArchiveListObject: VehicleArchiveList | None = Field(
        default=None, description="车辆结果档案对象列表"
    )


class ArchiveQueryResultSchema(SQLModel):
    """GA/T 2350.5-2025 A.9/A.11 `ArchiveQueryResultObject` 响应包装"""

    ArchiveQueryResultObject: ArchiveQueryResult
