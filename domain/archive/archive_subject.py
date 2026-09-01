from sqlmodel import Field, SQLModel


class ArchiveSubject(SQLModel):
    """GA/T 2350.5-2025 B.5 档案明细信息对象"""

    ArchiveID: str = Field(max_length=48, description="档案标识")
