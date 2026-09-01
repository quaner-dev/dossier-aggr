from sqlmodel import Field, SQLModel

from .archive_query_result import ArchiveQueryResult
from .archive_subject import ArchiveSubjectList
from .vehicle_archive_subject import VehicleArchiveSubjectList


class ArchiveSubjectQueryResult(ArchiveQueryResult):
    ArchiveSubjectInfoList: ArchiveSubjectList | VehicleArchiveSubjectList = Field(
        description="结果档案明细对象列表"
    )


class ArchiveSubjectQueryResultSchema(SQLModel):
    ArchiveSubjectQueryResultObject: ArchiveSubjectQueryResult
