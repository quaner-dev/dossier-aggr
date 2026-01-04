from typing import List

from pydantic import BaseModel, Field

import base
from .archive_query import ArchiveQueryBase


class ArchiveSubjectQuery(ArchiveQueryBase):
    """GA/T 2350.5-2025 B.9 档案明细查询对象"""

    # TODO 这里需要限制profileid的长度
    ArchiveIDList: List[str] = Field(description="档案标识列表")
    ResultSubjectDetailDeclare: base.enums.ResultSubjectDetailDeclareEnum | None = (
        Field(
            default=base.enums.ResultSubjectDetailDeclareEnum.EXCLUDE_DETAIL,
            description="返回结果轨迹详细信息约定",
        )
    )


# 档案明细查询对象结构
class ArchiveSubjectQuerySchema(BaseModel):
    ArchiveSubjectQueryObject: ArchiveSubjectQuery
