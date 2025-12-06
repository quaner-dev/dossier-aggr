from pydantic import BaseModel, Field
from typing import List, Optional, Annotated
from pydantic import BeforeValidator, PlainSerializer
from datetime import datetime
import enums
import models
import utils


class VIIDHeaders(BaseModel):
    content_type: str = "application/VIID+JSON"


# 采集设备对象
class APEObject(BaseModel):
    APEObject: List[models.APE]


# 采集设备对象列表
class APEListObject(BaseModel):
    APEListObject: APEObject


# 订阅对象
class SubscribeObject(BaseModel):
    SubscribeObject: List[models.SubscribeBase]


# 订阅对象列表
class SubscribeListObject(BaseModel):
    SubscribeListObject: SubscribeObject


# 通知对象
class SubscribeNotification(BaseModel):
    NotificationID: str = Field(description="通知标识", max_length=33)
    SubscribeID: str = Field(description="订阅标识", max_length=33)
    Title: str = Field(description="订阅标题", max_length=256)
    TriggerTime: str = Field(description="触发时间")
    InfoIDs: str = Field(description="信息标识", max_length=1024)
    DeviceList: Optional[str] = Field(default=None, description="设备")
    PersonObjectList: Optional[str] = Field(default=None, description="人员信息")
    FaceObjectList: Optional[str] = Field(default=None, description="人脸信息")
    MotorVehicleObjectList: Optional[str] = Field(
        default=None, description="机动车信息"
    )
    NonMotorVehicleObjectList: Optional[str] = Field(
        default=None, description="非机动车信息"
    )
    DataClassTabObjectList: Optional[str] = Field(
        default=None, description="数据分类标签"
    )
    ExecuteOperation: Optional[enums.ExecuteOperationEnum] = Field(
        default=None, description="更新项目"
    )


# 通知对象列表
class SubscribeNotificationListObject(BaseModel):
    SubscribeNotificationList: List[SubscribeNotification]


# 特征值对象
class FeatureInfo(BaseModel):
    Vendor: str = Field(description="厂商", max_length=100)
    AlgorithmVersion: str = Field(description="算法版本", max_length=100)
    FeatureData: str = Field(description="特征值数据")


# 子图像对象
class SubImageInfo(BaseModel):
    ImageID: Optional[str] = Field(default=None, description="图像标识", max_length=41)
    EventSort: Optional[int] = Field(default=None, description="事件分类")
    DeviceID: Optional[str] = Field(default=None, description="设备编码", max_length=20)
    StoragePath: Optional[str] = Field(
        default=None, description="存储路径", max_length=256
    )
    Type: enums.ImageTypeEnum = Field(description="图片类型")
    FileFormat: enums.ImageFormatEnum = Field(description="图像文件格式")
    ShotTime: Optional[str] = Field(default=None, description="拍摄时间")
    Width: int = Field(description="水平像素值")
    Height: int = Field(description="垂直像素值")
    Data: str = Field(description="图像数据")
    FeatureInfoObject: FeatureInfo = Field(description="特征值属性")


# 人脸对象
class Face(BaseModel):
    FaceID: str = Field(description="人脸标识", max_length=33)
    InfoKind: enums.InfoKindEnum = Field(
        default=enums.InfoKindEnum.Other, description="信息分类"
    )
    SourceID: str = Field(description="来源标识", max_length=41)
    DeviceID: str = Field(description="设备编码", max_length=20)
    LeftTopX: int = Field(description="左上角X坐标")
    LeftTopY: int = Field(description="左上角Y坐标")
    RightBtmX: int = Field(description="右下角X坐标")
    RightBtmY: int = Field(description="右下角Y坐标")
    SubImageList: List[SubImageInfo] = Field(description="图像列表")


# 人脸对象列表
class FaceListObject(BaseModel):
    FaceList: List[Face]


# 应答状态对象
class ResponseStatusObject(BaseModel):
    RequestURL: str = Field(description="资源定位符")
    StatusCode: str = Field(description="状态码")
    StatusString: str = Field(description="状态描述")
    Id: str = Field(description="资源ID")
    LocalTime: Annotated[
        datetime,
        BeforeValidator(utils.parse_datetime),
        PlainSerializer(utils.serialize_datetime),
    ] = Field(description="日期时间")


# 应答状态对象列表
class ResponseStatusListObject(BaseModel):
    ResponseStatusList: List[ResponseStatusObject]
