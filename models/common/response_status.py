from sqlmodel import SQLModel, Field
from ..common import enums


class ResponseStatus(SQLModel):
    """GA/T 1400.3-2017 A.26 应答状态对象"""

    RequestURL: str = Field(description="资源定位符")
    StatusCode: str = Field(description="状态码")
    StatusString: str = Field(description="状态描述")
    Id: str | None = Field(default=None, description="资源ID")
    LocalTime: enums.VIIDDateTime | None = Field(description="日期时间")


class ResponseStatusList(SQLModel):
    """GA/T 1400.3-2017 C.25 应答状态对象列表"""

    ResponseStatusObject: list[ResponseStatus]


# 应答状态对象列表结构
class ResponseStatusListSchema(SQLModel):
    ResponseStatusListObject: ResponseStatusList
