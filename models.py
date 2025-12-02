from sqlmodel import Field, SQLModel  # type: ignore
from enum import IntEnum, StrEnum
from pydantic import BeforeValidator
from datetime import datetime
from typing import Annotated

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
