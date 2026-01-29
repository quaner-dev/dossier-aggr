from sqlmodel import SQLModel, Field

from models import enums
from .archive_query import ArchiveQuery


class ArchiveSubjectQuery(ArchiveQuery):
    """GA/T 2350.5-2025 B.9 档案明细查询对象"""

    ArchiveIDList: list[str] = Field(description="档案标识列表")
    ResultSubjectDetailDeclare: enums.ResultSubjectDetailDeclareEnum | None = Field(
        default=enums.ResultSubjectDetailDeclareEnum.EXCLUDE_DETAIL,
        description="返回结果轨迹详细信息约定",
    )


# 档案明细查询对象结构
class ArchiveSubjectQuerySchema(SQLModel):
    ArchiveSubjectQueryObject: ArchiveSubjectQuery
