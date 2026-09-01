from sqlmodel import Field, SQLModel

from ..common import enums


class ArchiveLibrary(SQLModel):
    """GA/T 2350.5-2025 B.2 目标档案库对象"""

    ArchiveLibraryID: str = Field(
        max_length=48, description="目标档案库标识"
    )
    Name: str = Field(max_length=32, description="名称")
    CreateTime: enums.VIIDDateTime = Field(description="档案库创建时间")
    Memo: str | None = Field(max_length=1024, description="备注")
