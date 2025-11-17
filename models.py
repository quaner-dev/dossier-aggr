from sqlmodel import Field, SQLModel # type: ignore
from enum import IntEnum, StrEnum


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
    SubscribeID: str = Field(primary_key=True)
    Title: str
    SubscribeDetail: str
    ResourceClass: ResourceClassEnum
    ResourceURI: str
    ApplicantName: str
    ApplicantOrg: str
    BeginTime: str
    EndTime: str
    ReceiveAddr: str
    ReportInterval: int | None = 30
    Reason: str | None = None
    OperateType: OperateTypeEnum
    SubscribeStatus: SubscribeStatusEnum
    SubscribeCancelOrg: str | None = None
    SubscribeCancelPerson: str | None = None
    CancelTime: str | None = None
    CancelReason: str | None = None
    ResultImageDeclare: ResultImageDeclareEnum
    ResultFeatureDeclare: ResultFeatureDeclareEnum
    TabID: str | None = None
