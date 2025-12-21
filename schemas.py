from typing import Union, List, Annotated
from datetime import datetime

from pydantic import BaseModel, Field, BeforeValidator, PlainSerializer

import enums
import models
import utils


VIIDDateTime = Annotated[
    datetime,
    BeforeValidator(utils.parse_datetime),
    PlainSerializer(utils.serialize_datetime),
]


class APEList(BaseModel):
    """GA/T 1400.3-2017 C.1 采集设备对象列表"""

    APEObject: List[models.APE]


# 采集设备对象列表结构
class APEListSchema(BaseModel):
    APEListObject: APEList


class FeatureInfo(BaseModel):
    """视图库对接技术要求 A.7 特征值对象"""

    Vendor: str = Field(description="厂商", max_length=100)
    AlgorithmVersion: str = Field(description="算法版本", max_length=100)
    FeatureData: str = Field(description="特征值数据")


class SubImageInfo(BaseModel):
    """GA/T 1400.3-2017 C.6 图像子对象"""

    ImageID: str | None = Field(default=None, description="图像标识", max_length=41)
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
    FeatureInfoObject: FeatureInfo = Field(description="特征值属性")


class SubImageInfoList(BaseModel):
    """GA/T 1400.3-2017 C.6 子图像对象列表"""

    SubImageInfoObject: List[SubImageInfo]


class Person(BaseModel):
    """GA/T 1400.3-2017 A.8 人员对象"""

    PersonID: str = Field(description="人员标识", max_length=33)
    InfoKind: enums.InfoKindEnum = Field(
        default=enums.InfoKindEnum.Other, description="信息分类"
    )
    SourceID: str = Field(description="来源标识", max_length=41)
    DeviceID: str = Field(description="设备编码", max_length=20)
    LeftTopX: int | None = Field(description="左上角X坐标")
    LeftTopY: int | None = Field(description="左上角Y坐标")
    RightBtmX: int | None = Field(description="右下角X坐标")
    RightBtmY: int | None = Field(description="右下角Y坐标")
    SubImageList: List[SubImageInfo] | None = Field(description="图像列表")


class PersonList(BaseModel):
    """GA/T 1400.3-2017 C.8 人员对象列表"""

    PersonObject: List[Person]


# 人员对象列表结构
class PersonListObjectSchema(BaseModel):
    PersonListObject: PersonList


class Face(BaseModel):
    """GA/T 1400.3-2017 A.9 人脸对象"""

    FaceID: str = Field(description="人脸标识", max_length=33)
    InfoKind: enums.InfoKindEnum = Field(
        default=enums.InfoKindEnum.Other, description="信息分类"
    )
    SourceID: str = Field(description="来源标识", max_length=41)
    DeviceID: str = Field(description="设备编码", max_length=20)
    LeftTopX: int | None = Field(description="左上角X坐标")
    LeftTopY: int | None = Field(description="左上角Y坐标")
    RightBtmX: int | None = Field(description="右下角X坐标")
    RightBtmY: int | None = Field(description="右下角Y坐标")
    SubImageList: List[SubImageInfo] | None = Field(description="图像列表")


class FaceList(BaseModel):
    """GA/T 1400.3-2017 C.9 人脸对象列表"""

    FaceObject: List[Face]


# 人脸对象列表结构
class FaceListObjectSchema(BaseModel):
    FaceListObject: FaceList


# 订阅对象列表
class SubscribeList(BaseModel):
    """GA/T 1400.3-2017 C.19 订阅对象列表"""

    SubscribeObject: List[models.SubscribeBase]


# 订阅对象列表结构
class SubscribeListSchema(BaseModel):
    SubscribeListObject: SubscribeList


class SubscribeNotification(BaseModel):
    """GA/T 1400.3-2017 A.20 通知对象"""

    NotificationID: str = Field(description="通知标识", max_length=33)
    SubscribeID: str = Field(description="订阅标识", max_length=33)
    Title: str = Field(description="订阅标题", max_length=256)
    TriggerTime: str = Field(description="触发时间")
    InfoIDs: str = Field(description="信息标识", max_length=1024)
    DeviceList: str | None = Field(default=None, description="设备")
    PersonObjectList: PersonList | None = Field(default=None, description="人员信息")
    FaceObjectList: FaceList | None = Field(default=None, description="人脸信息")
    DataClassTabObjectList: str | None = Field(default=None, description="数据分类标签")
    ExecuteOperation: enums.ExecuteOperationEnum | None = Field(
        default=None, description="更新项目"
    )


class SubscribeNotificationList(BaseModel):
    """GA/T 1400.3-2017 C.20 通知对象列表"""

    SubscribeNotificationObject: List[SubscribeNotification]


# 通知对象列表结构
class SubscribeNotificationListSchema(BaseModel):
    SubscribeNotificationListObject: SubscribeNotificationList


class ResponseStatus(BaseModel):
    """GA/T 1400.3-2017 A.26 应答状态对象"""

    RequestURL: str = Field(description="资源定位符")
    StatusCode: str = Field(description="状态码")
    StatusString: str = Field(description="状态描述")
    Id: str | None = Field(default=None, description="资源ID")
    LocalTime: VIIDDateTime | None = Field(description="日期时间")


class ResponseStatusList(BaseModel):
    """GA/T 1400.3-2017 C.25 应答状态对象列表"""

    ResponseStatusObject: Union[ResponseStatus, List[ResponseStatus]]


# 应答状态对象列表结构
class ResponseStatusListSchema(BaseModel):
    ResponseStatusListObject: ResponseStatusList


class PictureQueryCondition(BaseModel):
    """GA/T 2350.5-2025 B.7 以图像搜图查询条件对象"""

    SubImage: SubImageInfo | None = Field(description="对象小图")
    Threshold: float | None = Field(description="相似度分数线")
    SubjectID: str | None = Field(description="数据标识", max_length=48)


class GeoRectangleType(BaseModel):
    """GA/T 2350.5-2025 B.12 检索区域对象"""

    LeftTopLongitude: float = Field(description="西北经度", decimal_places=6)
    LeftTopLatitude: float = Field(description="西北纬度", decimal_places=6)
    RightBtmLongitude: float = Field(description="东南经度", decimal_places=6)
    RightBtmLatitude: float = Field(description="东南纬度", decimal_places=6)


class DeviceSelector(BaseModel):
    """GA/T 2350.5-2025 B.13 检索设备范围对象"""

    # TODO 这里是个List，但是里面的device其实是个str，不是具有字段类型的model，所以这里直接使用List str来处理
    DeviceIDs: List[str] | None = Field(description="设备ID列表")
    DevicePlaceCode: str | None = Field(max_length=6, description="设备行政区划")


# 以图像搜图查询条件对象列表
class PictureQueryConditionList(BaseModel):
    PictureQueryConditionObject: List[PictureQueryCondition]


class Archive(BaseModel):
    """GA/T 2350.5-2025 B.3 人员档案基础信息对象"""

    ArchiveID: str = Field(max_length=48, description="档案标识")
    ArchiveLibraryID: str | None = Field(max_length=48, description="所属目标档案库")
    IDType: str | None = Field(max_length=3, description="证件类型")
    IDNumber: str | None = Field(max_length=30, description="证件编号")
    Name: str | None = Field(max_length=50, description="姓名")
    BirthTime: VIIDDateTime | None = Field(description="出生日期")
    CreateTime: VIIDDateTime = Field(description="档案创建时间")
    UpdateTime: VIIDDateTime = Field(description="档案更新时间")
    SubImageList: SubImageInfoList = Field(description="图片信息列表")


# 人员档案基础信息对象列表
class ArchiveList(BaseModel):
    ArchiveObject: List[Archive]


# 人员档案基础信息对象列表结构
class ArchiveListSchema(BaseModel):
    ArchiveListObject: ArchiveList


class ArchiveSubject(BaseModel):
    """GA/T 2350.5-2025 B.5 档案明细信息对象"""

    ArchiveID: str = Field(max_length=48, description="档案标识")
    PersonIDList: List[str] | None = Field(description="人员信息标识列表")
    FaceIDList: List[str] | None = Field(description="人脸信息标识列表")
    PersonObjectList: PersonList | None = Field(description="人员完整信息列表")
    FaceObjectList: FaceList | None = Field(description="人脸完整信息列表")


# 档案明细列表
class ArchiveSubjectList(BaseModel):
    ArchiveSubjectObject: List[ArchiveSubject]


# 档案明细列表结构
class ArchiveSubjectSchema(BaseModel):
    ArchiveSubjectListObject: ArchiveSubjectList


# TODO
class ArchiveQueryBase(BaseModel):
    QueryID: str = Field(max_length=48, description="查询标识")
    MaxNumRecordReturn: int | None = Field(description="最多返回记录数")
    PageRecordNum: int | None = Field(description="每页记录数")
    RecordStartNo: int | None = Field(description="起始记录号")
    BeginTime: VIIDDateTime | None = Field(description="开始时间")
    EndTime: VIIDDateTime | None = Field(description="结束时间")
    GeoRectangle: GeoRectangleType | None = Field(description="检索的区域范围")
    DeviceSelected: DeviceSelector = Field(description="检索的设备范围")
    Sort: str | None = Field(description="排序依据")


class ArchiveQuery(ArchiveQueryBase):
    """GA/T 2350.5-2025 B.6 档案查询对象"""

    PictureQueryCondition: PictureQueryConditionList | None = Field(
        description="以图像搜图查询"
    )


# 档案查询请求结构
class ArchiveQuerySchema(BaseModel):
    ArchiveQueryObject: ArchiveQuery


# TODO
class ArchiveQueryResultBase(BaseModel):
    QueryID: str = Field(max_length=48, description="查询标识")
    RecordStartNo: int | None = Field(description="起始记录号")
    PageRecordNum: int = Field(description="本页返回记录数")
    TotalNum: int = Field(description="符合条件记录总数")


class ArchiveQueryResult(ArchiveQueryResultBase):
    """GA/T 2350.5-2025 B.8 档案查询结果对象"""

    ArchiveListObject: ArchiveList = Field(description="人员结果档案对象列表")


# 档案查询结果对象结构
class ArchiveQueryResultSchema(BaseModel):
    ArchiveQueryResultObject: ArchiveQueryResult


class ArchiveSubjectQuery(ArchiveQueryBase):
    """GA/T 2350.5-2025 B.9 档案明细查询对象"""

    # TODO 这里需要限制profileid的长度
    ArchiveIDList: List[str] = Field(description="档案标识列表")
    ResultSubjectDetailDeclare: enums.ResultSubjectDetailDeclareEnum | None = Field(
        default=enums.ResultSubjectDetailDeclareEnum.EXCLUDE_DETAIL,
        description="返回结果轨迹详细信息约定",
    )


# 档案明细查询对象结构
class ArchiveSubjectQuerySchema(BaseModel):
    ArchiveSubjectQueryObject: ArchiveSubjectQuery


class ArchiveSubjectQueryResult(ArchiveQueryResultBase):
    """GA/T 2350.5-2025 B.10 档案明细查询结果对象"""

    ArchiveSubjectInfoList: ArchiveSubjectSchema = Field(
        description="结果档案明细对象列表"
    )
