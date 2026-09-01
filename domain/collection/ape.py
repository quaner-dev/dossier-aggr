from sqlmodel import Field, SQLModel

from ..common import enums


class APE(SQLModel):
    """GA/T 1400.3-2017 A.1 采集设备对象"""

    ApeID: str = Field(description="设备ID", max_length=20)
    Name: str = Field(description="名称", max_length=100)
    Model: str = Field(description="型号", max_length=100)
    IPAddr: str = Field(description="IP地址", max_length=30)
    IPV6Addr: str | None = Field(default=None, description="IPv6地址", max_length=64)
    Port: int = Field(description="端口号")
    Longitude: float = Field(description="经度")
    Latitude: float = Field(description="纬度")
    PlaceCode: str = Field(description="安装地点行政区划代码", max_length=6)
    Place: str | None = Field(default=None, description="位置名", max_length=256)
    OrgCode: str | None = Field(default=None, description="管辖单位代码", max_length=12)
    CapDirection: enums.CapDirectionEnum | None = Field(
        default=None, description="车辆抓拍方向"
    )
    MonitorDirection: enums.MonitorDirectionEnum | None = Field(
        default=None, description="监测方向"
    )
    MonitorAreaDesc: str | None = Field(
        default=None, description="监视区域说明", max_length=256
    )
    IsOnline: enums.StatusTypeEnum = Field(description="是否在线")
    OwnerApsID: str | None = Field(
        default=None, description="所属采集系统", max_length=20
    )
    UserId: str | None = Field(default=None, description="用户帐号", max_length=64)
    Password: str | None = Field(default=None, description="口令", max_length=32)
    FunctionType: str = Field(description="功能类型", max_length=30)
    PositionType: str | None = Field(
        default=None, description="位置类型", max_length=50
    )
