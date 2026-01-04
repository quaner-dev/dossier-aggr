from typing import Annotated
from datetime import datetime

from sqlmodel import Field, SQLModel  # type: ignore
from pydantic import BeforeValidator, PlainSerializer

import utils
import base.enums as enums


class SubscribeBase(SQLModel):
    """GA/T 1400.3-2017 A.19 订阅对象"""

    id: int | None = Field(default=None, primary_key=True, exclude=True)

    SubscribeID: str = Field(description="订阅标识符", max_length=33, unique=True)
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
