from sqlmodel import Field, SQLModel  # type: ignore
from pydantic import BeforeValidator, PlainSerializer
from datetime import datetime
from typing import Annotated
import utils
import enums


class SubscribeBase(SQLModel):
    SubscribeID: str = Field(description="订阅标识符", max_length=33, primary_key=True)
    Title: str = Field(description="订阅标题", max_length=256)
    SubscribeDetail: str = Field(description="订阅类别")
    ResourceClass: enums.ResourceClassEnum = Field(description="订阅资源类别")
    ResourceURI: str = Field(description="订阅资源路径", max_length=256)
    ApplicantName: str = Field(description="申请人", max_length=50)
    ApplicantOrg: str = Field(description="申请单位", max_length=100)
    BeginTime: Annotated[
        datetime,
        BeforeValidator(utils.parse_datetime),
        PlainSerializer(utils.serialize_datetime),
    ] = Field(description="开始时间")
    EndTime: Annotated[
        datetime,
        BeforeValidator(utils.parse_datetime),
        PlainSerializer(utils.serialize_datetime),
    ] = Field(description="结束时间")
    ReceiveAddr: str = Field(description="信息接收地址", max_length=256)
    ReportInterval: int | None = Field(default=30, description="信息上报间隔时间")
    Reason: str | None = Field(default=None, description="理由", max_length=256)
    OperateType: enums.OperateTypeEnum = Field(description="操作类型")
    SubscribeStatus: enums.SubscribeStatusEnum = Field(description="订阅执行状态")
    SubscribeCancelOrg: str | None = Field(
        default=None, description="订阅取消单位", max_length=32
    )
    SubscribeCancelPerson: str | None = Field(
        default=None, description="订阅取消人", max_length=32
    )
    CancelTime: str | None = Field(default=None, description="取消时间")
    CancelReason: str | None = Field(
        default=None, description="取消原因", max_length=64
    )
    ResultImageDeclare: enums.ResultImageDeclareEnum = Field(
        description="返回结果图片约定", max_length=5
    )
    ResultFeatureDeclare: enums.ResultFeatureDeclareEnum = Field(
        description="返回结果特征值约定"
    )
    TabID: str | None = Field(
        default=None, description="订阅分类标签标识", max_length=41
    )


class Subscribe(SubscribeBase, table=True):
    pass


class APE(SQLModel, table=True):
    ApeID: str = Field(description="设备ID", max_length=20, primary_key=True)
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
