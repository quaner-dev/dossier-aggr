from pydantic import Field


from .archive_query_result import ArchiveQueryResultBase
from .archive_subject import ArchiveSubjectSchema


class ArchiveSubjectQueryResult(ArchiveQueryResultBase):
    """GA/T 2350.5-2025 B.10 档案明细查询结果对象"""

    ArchiveSubjectInfoList: ArchiveSubjectSchema = Field(
        description="结果档案明细对象列表"
    )
