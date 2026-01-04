from sqlmodel import Field, SQLModel  # type: ignore

import base.enums as enums


class APSBase(SQLModel):
    """GA/T 1400.3-2017 A.3 采集系统对象特征属性"""

    id: int | None = Field(default=None, primary_key=True, exclude=True)

    ApsID: str = Field(description="设备ID", max_length=20, unique=True)
    Name: str = Field(description="名称", max_length=100)
    IPAddr: str = Field(description="IP地址", max_length=30)
    IPV6Addr: str | None = Field(default=None, description="IPv6地址", max_length=64)
    Port: int = Field(description="端口号")
    IsOnline: enums.StatusTypeEnum = Field(description="是否在线")
