from typing import Union, List

from pydantic import BaseModel, Field

import base
import enums

# TODO 如果要保证model和schema相互结合，就需要保证两个模块之间没有关联关系存在，也就是relation存在，当前的情况是model是基础类，schema来引用model中的类


# 采集设备对象列表
class APEList(BaseModel):
    APEObject: List[base.APEBase]


# 采集设备对象列表结构
class APEListSchema(BaseModel):
    APEListObject: APEList


class SubImageInfo(base.SubImageInfoBase):
    """GA/T 1400.3-2017 C.6 图像子对象"""

    FeatureInfoObject: base.FeatureInfoBase = Field(description="特征值属性")


class SubImageInfoList(BaseModel):
    """GA/T 1400.3-2017 C.6 子图像对象列表"""

    SubImageInfoObject: List[base.SubImageInfoBase]


class Person(base.PersonBase):
    """GA/T 1400.3-2017 A.8 人员对象"""

    SubImageList: List[SubImageInfo] | None = Field(description="图像列表")


class PersonList(BaseModel):
    """GA/T 1400.3-2017 C.8 人员对象列表"""

    PersonObject: List[Person]


# 人员对象列表结构
class PersonListObjectSchema(BaseModel):
    PersonListObject: PersonList


class Face(base.FaceBase):
    """GA/T 1400.3-2017 A.9 人脸对象"""

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

    SubscribeObject: List[base.SubscribeBase]


# 订阅对象列表结构
class SubscribeListSchema(BaseModel):
    SubscribeListObject: SubscribeList


class SubscribeNotification(base.SubscribeNotificationBase):
    """GA/T 1400.3-2017 A.20 通知对象"""

    PersonObjectList: PersonList | None = Field(default=None, description="人员信息")
    FaceObjectList: FaceList | None = Field(default=None, description="人脸信息")


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
    LocalTime: enums.VIIDDateTime | None = Field(description="日期时间")


class ResponseStatusList(BaseModel):
    """GA/T 1400.3-2017 C.25 应答状态对象列表"""

    ResponseStatusObject: Union[ResponseStatus, List[ResponseStatus]]


# 应答状态对象列表结构
class ResponseStatusListSchema(BaseModel):
    ResponseStatusListObject: ResponseStatusList


class Register(BaseModel):
    """GA/T 1400.3-2017 C.26 注册对象"""

    DeviceID: str = Field(description="设备编码", max_length=20)


# 注册对象结构
class RegisterSchema(BaseModel):
    RegisterObject: Register


class Keepalive(BaseModel):
    """GA/T 1400.3-2017 C.27 保活对象"""

    DeviceID: str = Field(description="设备编码", max_length=20)


# 保活对象结构
class KeepaliveSchema(BaseModel):
    KeepaliveObject: Keepalive


class UnRegister(BaseModel):
    """GA/T 1400.3-2017 C.28 注销对象"""

    DeviceID: str = Field(description="设备编码", max_length=20)


# 注销对象结构
class UnRegisterSchema(BaseModel):
    UnRegisterObject: UnRegister


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


class Archive(base.ArchiveBase):
    """GA/T 2350.5-2025 B.3 人员档案基础信息对象"""

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
    BeginTime: enums.VIIDDateTime | None = Field(description="开始时间")
    EndTime: enums.VIIDDateTime | None = Field(description="结束时间")
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
