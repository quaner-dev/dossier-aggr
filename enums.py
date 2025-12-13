from enum import IntEnum, StrEnum
from pydantic import BeforeValidator
from typing import Annotated
from datetime import datetime

CompactDateTime = Annotated[
    datetime, BeforeValidator(lambda v: datetime.strptime(v, "%Y%m%d%H%M%S"))
]


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


class StatusTypeEnum(IntEnum):
    Online = 1  # 在线
    Offline = 2  # 离线
    Other = 9  # 其他


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


class SortTypeEnum(StrEnum):
    Desc = "desc"  # 降序
    Asc = "Asc"  # 升序
