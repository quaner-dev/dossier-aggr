from sqlmodel import Field, SQLModel

from .archive import ArchiveList
from .vehicle_archive import VehicleArchiveList


class ArchiveQueryResult(SQLModel):
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
    ArchiveQueryResultObject: ArchiveQueryResult
