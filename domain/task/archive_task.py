from sqlmodel import Field, SQLModel

from ..common import enums


class ArchiveTask(SQLModel):
    """GA/T 2350.5-2025 A.6 聚档任务对象"""

    TaskID: str = Field(max_length=48, description="任务标识")
    TaskName: str | None = Field(default=None, max_length=128, description="任务名称")
    ArchiveLibraryID: str | None = Field(
        default=None, max_length=48, description="目标档案库标识"
    )
    EventType: str | None = Field(default=None, max_length=8, description="事件类型")
    Status: str | None = Field(default=None, max_length=32, description="任务状态")
    CreateTime: enums.VIIDDateTime = Field(description="任务创建时间")
    UpdateTime: enums.VIIDDateTime = Field(description="任务更新时间")
