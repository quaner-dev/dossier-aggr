from sqlmodel import Field, SQLModel

from models.common import enums

from .archive_query import ArchiveQuery


class ArchiveSubjectQuery(ArchiveQuery):
    """GA/T 2350.5-2025 B.9 档案明细查询对象"""

    ArchiveIDList: list[str] = Field(description="档案标识列表")
    ResultSubjectDetailDeclare: enums.ResultSubjectDetailDeclareEnum | None = Field(
        default=enums.ResultSubjectDetailDeclareEnum.EXCLUDE_DETAIL,
        description="返回结果轨迹详细信息约定",
    )


class ArchiveSubjectQuerySchema(SQLModel):
    """GA/T 2350.5-2025 A.13/A.15 `ArchiveSubjectQueryObject` 查询请求包装"""

    ArchiveSubjectQueryObject: ArchiveSubjectQuery
