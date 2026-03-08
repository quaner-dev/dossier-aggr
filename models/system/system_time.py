from sqlmodel import SQLModel, Field

from ..common import enums


class SystemTime(SQLModel):
    """GA/T 1400.3-2017 系统时间对象"""

    LocalTime: enums.VIIDDateTime = Field(description="系统时间")
