from sqlmodel import Field, SQLModel

from . import enums


class ResponseStatus(SQLModel):
    """GA/T 1400.3-2017 A.26 应答状态对象"""

    RequestURL: str = Field(description="资源定位符")
    StatusCode: str = Field(description="状态码")
    StatusString: str = Field(description="状态描述")
    Id: str | None = Field(default=None, description="资源ID")
    LocalTime: enums.VIIDDateTime | None = Field(description="日期时间")
