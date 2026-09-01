from sqlmodel import Field, SQLModel

from ..common import enums


class Archive(SQLModel):
    """GA/T 2350.5-2025 B.3 人员档案基础信息对象"""

    ArchiveID: str = Field(max_length=48, description="档案标识")
    ArchiveLibraryID: str | None = Field(
        default=None, max_length=48, description="所属目标档案库"
    )
    CreateTime: enums.VIIDDateTime = Field(description="档案创建时间")
    UpdateTime: enums.VIIDDateTime = Field(description="档案更新时间")
    Similaritydegree: float | None = Field(default=None, description="相似度")
    Confidence: float | None = Field(default=None, description="可信度")
