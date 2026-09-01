from sqlmodel import Field, SQLModel

from domain.common import enums

from .archive_query import ArchiveQuery


class ArchiveSubjectQuery(ArchiveQuery):
    ArchiveIDList: list[str] = Field(description="档案标识列表")
    ResultSubjectDetailDeclare: enums.ResultSubjectDetailDeclareEnum | None = Field(
        default=enums.ResultSubjectDetailDeclareEnum.EXCLUDE_DETAIL,
        description="返回结果轨迹详细信息约定",
    )


class ArchiveSubjectQuerySchema(SQLModel):
    ArchiveSubjectQueryObject: ArchiveSubjectQuery
