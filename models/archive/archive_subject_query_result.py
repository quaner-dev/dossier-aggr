from sqlmodel import SQLModel, Field

from .archive_query_result import ArchiveQueryResult
from .archive_subject import ArchiveSubjectList


class ArchiveSubjectQueryResult(ArchiveQueryResult):
    """GA/T 2350.5-2025 B.10 档案明细查询结果对象"""

    ArchiveSubjectInfoList: ArchiveSubjectList = Field(
        description="结果档案明细对象列表"
    )


# 档案明细查询结果对象结构
class ArchiveSubjectQueryResultSchema(SQLModel):
    ArchiveSubjectQueryResultObject: ArchiveSubjectQueryResult
