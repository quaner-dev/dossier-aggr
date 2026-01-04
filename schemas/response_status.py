from typing import Union, List

from pydantic import BaseModel, Field

import base


class ResponseStatus(BaseModel):
    """GA/T 1400.3-2017 A.26 应答状态对象"""

    RequestURL: str = Field(description="资源定位符")
    StatusCode: str = Field(description="状态码")
    StatusString: str = Field(description="状态描述")
    Id: str | None = Field(default=None, description="资源ID")
    LocalTime: base.enums.VIIDDateTime | None = Field(description="日期时间")


class ResponseStatusList(BaseModel):
    """GA/T 1400.3-2017 C.25 应答状态对象列表"""

    ResponseStatusObject: Union[ResponseStatus, List[ResponseStatus]]


# 应答状态对象列表结构
class ResponseStatusListSchema(BaseModel):
    ResponseStatusListObject: ResponseStatusList
