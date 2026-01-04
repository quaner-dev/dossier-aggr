from pydantic import BaseModel, Field

from .archive import ArchiveList
from .common import ArchiveQueryResultBase


class ArchiveQueryResult(ArchiveQueryResultBase):
    """GA/T 2350.5-2025 B.8 档案查询结果对象"""

    ArchiveListObject: ArchiveList = Field(description="人员结果档案对象列表")


# 档案查询结果对象结构
class ArchiveQueryResultSchema(BaseModel):
    ArchiveQueryResultObject: ArchiveQueryResult
