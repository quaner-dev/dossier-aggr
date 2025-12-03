from sqlmodel import Field, SQLModel  # type: ignore
from enum import IntEnum, StrEnum
from pydantic import BeforeValidator
from datetime import datetime
from typing import Annotated, Optional

CompactDateTime = Annotated[
    datetime, BeforeValidator(lambda v: datetime.strptime(v, "%Y%m%d%H%M%S"))
]


class ResourceClassEnum(IntEnum):
    Tollgate = 0  # 卡口
    Ape = 1  # 设备
    CollectedData = 2  # 采集内容
    Case = 3  # 案件
    VIID = 4  # 视图库
    AdministrativeDivision = 5  # 行政区划


class OperateTypeEnum(IntEnum):
    Subscribe = 0  # 订阅
    Unsubscribe = 1  # 取消订阅


class SubscribeStatusEnum(IntEnum):
    Active = 0  # 订阅中
    Unsubscribed = 1  # 已取消订阅
    Expired = 2  # 订阅到期
    Not_Subscribe = 9  # 未订阅


class ResultImageDeclareEnum(StrEnum):
    Unknown = "-1"  # 不要图片
    PersonImage = "10"  # 人员图
    FaceImage = "11"  # 人脸图
    SceneImage = "14"  # 场景图


class ResultFeatureDeclareEnum(IntEnum):
    WithoutFeatures = -1  # 不要特征值
    WithFeatures = 1  # 需要返回特征值


class Subscribe(SQLModel, table=True):
    SubscribeID: str = Field(primary_key=True, description="订阅标识符")
    Title: str = Field(description="订阅标题")
    SubscribeDetail: str = Field(description="订阅类别")
    ResourceClass: ResourceClassEnum
    ResourceURI: str = Field(description="订阅资源路径")
    ApplicantName: str = Field(description="申请人")
    ApplicantOrg: str = Field(description="申请单位")
    BeginTime: CompactDateTime = Field(description="开始时间")
    EndTime: CompactDateTime = Field(description="结束时间")
    ReceiveAddr: str = Field(description="信息接收地址")
    ReportInterval: int | None = Field(default=30, description="信息上报间隔时间")
    Reason: str | None = Field(default=None, description="理由")
    OperateType: OperateTypeEnum = Field(description="操作类型")
    SubscribeStatus: SubscribeStatusEnum = Field(description="订阅执行状态")
    SubscribeCancelOrg: str | None = Field(default=None, description="订阅取消单位")
    SubscribeCancelPerson: str | None = Field(default=None, description="订阅取消人")
    CancelTime: str | None = Field(default=None, description="取消时间")
    CancelReason: str | None = Field(default=None, description="取消原因")
    ResultImageDeclare: ResultImageDeclareEnum = Field(description="返回结果图片约定")
    ResultFeatureDeclare: ResultFeatureDeclareEnum = Field(
        description="返回结果特征值约定"
    )
    TabID: str | None = Field(default=None, description="订阅分类标签标识")

    # @field_validator("BeginTime", "EndTime")
    # @classmethod
    # def parse_datetime(cls, v: Any) -> datetime:
    #     if isinstance(v, str):
    #         return datetime.strptime(v, "%Y%m%d%H%M%S")
    #     return v


class CapDirectionEnum(IntEnum):
    Front = 0  # 拍车头
    Rear = 1  # 拍车尾


class MonitorDirectionEnum(IntEnum):
    WestToEast = 1  # 西向东（东）
    EastToWest = 2  # 东向西（西）
    NorthToSouth = 3  # 北向南（南）
    SouthToNorth = 4  # 南向北（北）
    SouthwestToNortheast = 5  # 西南到东北（东北）
    NortheastToSouthwest = 6  # 东北到西南（西南）
    NorthwestToSoutheast = 7  # 西北到东南（东南）
    SoutheastToNorthwest = 8  # 东南到西北（西北）
    Other = 9  # 其他


class APE(SQLModel, table=True):
    ApeID: str = Field(primary_key=True, description="设备ID")
    Name: str = Field(description="名称")
    Model: str = Field(description="型号")
    IPAddr: str = Field(description="IP地址")
    IPV6Addr: Optional[str] = Field(description="IPv6地址")
    Port: int = Field(description="端口号")
    Longitude: float = Field(description="经度")
    Latitude: float = Field(description="纬度")
    PlaceCode: str = Field(description="安装地点行政区划代码")
    Place: Optional[str] = Field(description="位置名")
    OrgCode: Optional[str] = Field(description="管辖单位代码")
    CapDirection: Optional[CapDirectionEnum] = Field(description="车辆抓拍方向")
    MonitorDirection: Optional[MonitorDirectionEnum] = Field(description="监测方向")
    MonitorAreaDesc: Optional[str] = Field(description="监视区域说明")
    IsOnline: str = Field(description="是否在线")
    OwnerApsID: Optional[str] = Field(description="所属采集系统")
    UserId: Optional[str] = Field(description="用户帐号")
    Password: Optional[str] = Field(description="口令")
    FunctionType: str = Field(description="功能类型")
    PositionType: Optional[str] = Field(description="位置类型")
