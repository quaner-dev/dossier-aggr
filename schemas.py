from pydantic import BaseModel, Field, BeforeValidator
from typing import Annotated, List
from models import Subscribe, APE
from enum import IntEnum, StrEnum
from datetime import datetime


class ExecuteOperationEnum(IntEnum):
    Add = 1  # 添加
    Update = 2  # 修改
    Delete = 3  # 删除


class ImageTypeEnum(StrEnum):
    VehicleLargeImage = "01"  # 车辆大图
    LicensePlateColorSmallImage = "02"  # 车牌彩色小图
    LicensePlateBinaryImage = "03"  # 车牌二值化图
    DriverFaceFeature = "04"  # 驾驶员面部特征图
    CoDriverFaceFeature = "05"  # 副驾驶面部特征图
    VehicleLogo = "06"  # 车标
    ViolationCompositeImage = "07"  # 违章合成图
    PassingCompositeImage = "08"  # 过车合成图
    VehicleCloseUpImage = "09"  # 车辆特写图
    PersonImage = "10"  # 人员图
    FaceImage = "11"  # 人脸图
    NonMotorVehicleImage = "12"  # 非机动车图
    ObjectImage = "13"  # 物品图
    SceneImage = "14"  # 场景图
    GeneralImage = "100"  # 一般图片


class ImageFormatEnum(StrEnum):
    BMP = "Bmp"  # BMP
    GIF = "Gif"  # GIF
    JPEG = "Jpeg"  # JPEG
    PNG = "Png"  # PNG


class InfoKindEnum(IntEnum):
    Other = 0  # 其他
    AutoCollect = 1  # 自动采集
    ManualCollect = 2  # 人工采集


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


class VIIDHeaders(BaseModel):
    content_type: str = "application/VIID+JSON"


class ResponseStatusObject(BaseModel):
    RequestURL: str
    StatusCode: str
    StatusString: str
    LocalTime: str


class SubscribeObject(BaseModel):
    SubscribeObject: List[Subscribe]


class SubscribeListObject(BaseModel):
    SubscribeListObject: SubscribeObject


class APEObject(BaseModel):
    APEObject: List[APE]


class APEListObject(BaseModel):
    APEListObject: APEObject


CompactDateTime = Annotated[
    datetime, BeforeValidator(lambda v: datetime.strptime(v, "%Y%m%d%H%M%S"))
]


class SubscribeNotification(BaseModel):
    NotificationID: str = Field(description="通知标识", max_length=33)
    SubscribeID: str = Field(description="订阅标识", max_length=33)
    Title: str = Field(description="订阅标题", max_length=256)
    TriggerTime: str = Field(description="触发时间")
    InfoIDs: str = Field(description="信息标识", max_length=1024)
    DeviceList: str | None = Field(default=None, description="设备")
    PersonObjectList: str | None = Field(default=None, description="人员信息")
    FaceObjectList: str | None = Field(default=None, description="人脸信息")
    MotorVehicleObjectList: str | None = Field(default=None, description="机动车信息")
    NonMotorVehicleObjectList: str | None = Field(
        default=None, description="非机动车信息"
    )
    DataClassTabObjectList: str | None = Field(default=None, description="数据分类标签")
    ExecuteOperation: ExecuteOperationEnum | None = Field(
        default=None, description="更新项目"
    )


class FeatureInfo(BaseModel):
    Vendor: str = Field(description="厂商", max_length=100)
    AlgorithmVersion: str = Field(description="算法版本", max_length=100)
    FeatureData: str = Field(description="特征值数据")


class SubImageInfo(BaseModel):
    ImageID: str | None = Field(default=None, description="图像标识", max_length=41)
    EventSort: int | None = Field(default=None, description="事件分类")
    DeviceID: str | None = Field(default=None, description="设备编码", max_length=20)
    StoragePath: str | None = Field(
        default=None, description="存储路径", max_length=256
    )
    Type: ImageTypeEnum = Field(description="图片类型")
    FileFormat: ImageFormatEnum = Field(description="图像文件格式")
    ShotTime: CompactDateTime | None = Field(default=None, description="拍摄时间")
    Width: int = Field(description="水平像素值")
    Height: int = Field(description="垂直像素值")
    Data: str = Field(description="图像数据")
    FeatureInfoObject: FeatureInfo = Field(description="特征值属性")


class Face(BaseModel):
    FaceID: str = Field(description="人脸标识", max_length=33)
    InfoKind: InfoKindEnum = Field(default=InfoKindEnum.Other, description="信息分类")
    SourceID: str = Field(description="来源标识", max_length=41)
    DeviceID: str = Field(description="设备编码", max_length=20)
    LeftTopX: int = Field(description="左上角X坐标")
    LeftTopY: int = Field(description="左上角Y坐标")
    RightBtmX: int = Field(description="右下角X坐标")
    RightBtmY: int = Field(description="右下角Y坐标")
    SubImageList: List[SubImageInfo] = Field(description="图像列表")
