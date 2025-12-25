from typing import Annotated
from datetime import datetime

from sqlmodel import Field, SQLModel, Relationship  # type: ignore
from pydantic import BeforeValidator, PlainSerializer

import utils
import enums


class APS(SQLModel, table=True):
    # TODO 增加注释

    id: int | None = Field(default=None, primary_key=True)

    ApsID: str = Field(description="设备ID", max_length=20)
    Name: str = Field(description="名称", max_length=100)
    IPAddr: str = Field(description="IP地址", max_length=30)
    IPV6Addr: str | None = Field(default=None, description="IPv6地址", max_length=64)
    Port: int = Field(description="端口号")
    IsOnline: enums.StatusTypeEnum = Field(description="是否在线")


class APE(SQLModel, table=True):
    """GA/T 1400.3-2017 A.1 采集设备对象"""

    id: int | None = Field(default=None, primary_key=True)

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


class Subscribe(SQLModel, table=True):
    """GA/T 1400.3-2017 A.19 订阅对象"""

    id: int | None = Field(default=None, primary_key=True)

    SubscribeID: str = Field(description="订阅标识符", max_length=33)
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


class FeatureInfo(SQLModel, table=True):
    """视图库对接技术要求 A.7 特征值对象"""

    id: int | None = Field(default=None, primary_key=True)
    sub_image_info_id: str | None = Field(
        default=None, foreign_key="subimageinfo.ImageID"
    )

    Vendor: str = Field(description="厂商", max_length=100)
    AlgorithmVersion: str = Field(description="算法版本", max_length=100)
    FeatureData: str = Field(description="特征值数据")


class SubImageInfo(SQLModel, table=True):
    """GA/T 1400.3-2017 C.6 图像子对象"""

    id: int | None = Field(default=None, primary_key=True)
    archive_id: str | None = Field(default=None, foreign_key="archive.ArchiveID")

    ImageID: str | None = Field(
        default=None, description="图像标识", max_length=41, unique=True
    )
    EventSort: int | None = Field(default=None, description="事件分类")
    DeviceID: str | None = Field(default=None, description="设备编码", max_length=20)
    StoragePath: str | None = Field(
        default=None, description="存储路径", max_length=256
    )
    Type: enums.ImageTypeEnum = Field(description="图片类型")
    FileFormat: enums.ImageFormatEnum = Field(description="图像文件格式")
    ShotTime: str | None = Field(default=None, description="拍摄时间")
    Width: int | None = Field(description="水平像素值")
    Height: int | None = Field(description="垂直像素值")
    Data: str | None = Field(description="图像数据")


class Archive(SQLModel, table=True):
    """GA/T 2350.5-2025 B.3 人员档案基础信息对象"""

    id: int | None = Field(default=None, primary_key=True)

    ArchiveID: str = Field(max_length=48, description="档案标识", unique=True)
    ArchiveLibraryID: str | None = Field(max_length=48, description="所属目标档案库")
    IDType: str | None = Field(max_length=3, description="证件类型")
    IDNumber: str | None = Field(max_length=30, description="证件编号")
    Name: str | None = Field(max_length=50, description="姓名")
    BirthTime: enums.VIIDDateTime | None = Field(description="出生日期")
    CreateTime: enums.VIIDDateTime = Field(description="档案创建时间")
    UpdateTime: enums.VIIDDateTime = Field(description="档案更新时间")
