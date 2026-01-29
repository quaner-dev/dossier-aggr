from sqlmodel import SQLModel, Field

from ..common import enums


class APS(SQLModel, table=True):
    """GA/T 1400.3-2017 A.3 采集系统对象特征属性"""

    id: int | None = Field(default=None, primary_key=True, exclude=True)

    ApsID: str = Field(description="设备ID", max_length=20, unique=True)
    Name: str = Field(description="名称", max_length=100)
    IPAddr: str = Field(description="IP地址", max_length=30)
    IPV6Addr: str | None = Field(default=None, description="IPv6地址", max_length=64)
    Port: int = Field(description="端口号")
    IsOnline: enums.StatusTypeEnum = Field(description="是否在线")


# 采集系统对象列表
class APSList(SQLModel):
    APSObject: list[APS]


# 采集系统对象列表结构
class APSListSchema(SQLModel):
    APSListObject: APSList
