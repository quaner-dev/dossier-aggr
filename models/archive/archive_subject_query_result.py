from sqlmodel import Field, SQLModel

from .archive_query_result import ArchiveQueryResult
from .archive_subject import ArchiveSubjectList
from .vehicle_archive_subject import VehicleArchiveSubjectList


class ArchiveSubjectQueryResult(ArchiveQueryResult):
    """GA/T 2350.5-2025 B.10 档案明细查询结果对象"""

    ArchiveSubjectInfoList: ArchiveSubjectList | VehicleArchiveSubjectList = Field(
        description="结果档案明细对象列表"
    )


class ArchiveSubjectQueryResultSchema(SQLModel):
    """GA/T 2350.5-2025 A.13/A.15 `ArchiveSubjectQueryResultObject` 响应包装"""

    ArchiveSubjectQueryResultObject: ArchiveSubjectQueryResult
