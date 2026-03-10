from typing import Annotated
from datetime import datetime
from enum import IntEnum, StrEnum

from pydantic import BeforeValidator, PlainSerializer

from core import utils


CompactDateTime = Annotated[
    datetime, BeforeValidator(lambda v: datetime.strptime(v, "%Y%m%d%H%M%S"))
]

VIIDDateTime = Annotated[
    datetime,
    BeforeValidator(utils.parse_datetime),
    PlainSerializer(utils.serialize_datetime),
]


class CapDirectionEnum(IntEnum):
    """车辆抓拍方向"""

    Front = 0  # 拍车头
    Rear = 1  # 拍车尾


class MonitorDirectionEnum(IntEnum):
    """监视方向"""

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
    """视频设备工作状态"""

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


class ResultSubjectDetailDeclareEnum(IntEnum):
    EXCLUDE_DETAIL = -1  # 不需要轨迹详细信息
    INCLUDE_DETAIL = 1  # 需要返回轨迹详细信息


class OnlyRealNameArchiveEnum(IntEnum):
    AllArchive = 0  # 返回全部档案，默认值
    OnlyRealNameArchive = 1  # 仅返回实名档案
    OnlyNonRealNameArchive = 2  # 仅返回非实名档案


class GenderTypeEnum(IntEnum):
    Unknown = 0  # 未知的性别
    Male = 1  # 男性
    Female = 2  # 女性
    NotSpecified = 9  # 未说明的性别


class ColorTypeEnum(StrEnum):
    Black = "1"  # 黑
    White = "2"  # 白
    Gray = "3"  # 灰
    Red = "4"  # 红
    Blue = "5"  # 蓝
    Yellow = "6"  # 黄
    Orange = "7"  # 橙
    Brown = "8"  # 棕
    Green = "9"  # 绿
    Purple = "10"  # 紫
    Cyan = "11"  # 青
    Pink = "12"  # 粉
    Transparent = "13"  # 透明
    Other = "99"  # 其他


class VehicleBrandTypeEnum(StrEnum):
    other = "0"  # 其他
    volkswagen = "1"  # 大众
    buick = "2"  # 别克
    bmw = "3"  # 宝马
    honda = "4"  # 本田
    peugeot = "5"  # 标致
    toyota = "6"  # 丰田
    ford = "7"  # 福特
    nissan = "8"  # 日产
    audi = "9"  # 奥迪
    mazda = "10"  # 马自达
    chevrolet = "11"  # 雪佛兰
    citroen = "12"  # 雪铁龙
    hyundai = "13"  # 现代
    chery = "14"  # 奇瑞
    kia = "15"  # 起亚
    roewe = "16"  # 荣威
    mitsubishi = "17"  # 三菱
    skoda = "18"  # 斯柯达
    geely = "19"  # 吉利
    zhonghua = "20"  # 中华
    volvo = "21"  # 沃尔沃
    lexus = "22"  # 雷克萨斯
    fiat = "23"  # 菲亚特
    geely_emgrand = "24"  # 吉利帝豪
    dongfeng = "25"  # 东风
    byd = "26"  # 比亚迪
    suzuki = "27"  # 铃木
    jinbei = "28"  # 金杯
    haima = "29"  # 海马
    wuling = "30"  # 五菱
    jac = "31"  # 江淮
    subaru = "32"  # 斯巴鲁
    londinium = "33"  # 英伦
    greatwall = "34"  # 长城
    hafei = "35"  # 哈飞
    qingling_isuzu = "36"  # 庆铃（五十铃）
    southeast = "37"  # 东南
    changan = "38"  # 长安
    foton = "39"  # 福田
    xiali = "40"  # 夏利
    benz = "41"  # 奔驰
    faw = "42"  # 一汽
    iveco = "43"  # 依维柯
    lifan = "44"  # 力帆
    faw_besturn = "45"  # 一汽奔腾
    crown = "46"  # 皇冠
    renault = "47"  # 雷诺
    jmc = "48"  # JMC
    mg = "49"  # MG名爵
    kema = "50"  # 凯马
    zotye = "51"  # 众泰
    changhe = "52"  # 昌河
    kinglong = "53"  # 厦门金龙
    shanghai_huijong = "54"  # 上海汇众
    kinglong_suzhou = "55"  # 苏州金龙
    haige = "56"  # 海格
    yutong = "57"  # 宇通
    sinotruk = "58"  # 中国重汽
    north_ben_twin = "59"  # 北奔重卡
    camc = "60"  # 华菱星马汽车
    yuejin = "61"  # 跃进汽车
    huanghai = "62"  # 黄海汽车
    porsche = "65"  # 保时捷
    cadillac = "66"  # 凯迪拉克
    infiniti = "67"  # 英菲尼迪
    geely_gleagle = "68"  # 吉利全球鹰
    jeep = "69"  # 吉普
    land_rover = "70"  # 路虎
    changfeng_hunter = "71"  # 长丰猎豹
    shidai = "73"  # 时代汽车
    changan_car = "75"  # 长安轿车
    shaanxi_heavy_truck = "76"  # 陕汽重卡
    ankai = "81"  # 安凯
    shenlong = "82"  # 申龙
    daewoo = "83"  # 大宇
    zhongtong = "86"  # 中通
    baojun = "87"  # 宝骏
    baic_weiwang = "88"  # 北汽威旺
    gac_trumpchi = "89"  # 广汽传祺
    lufeng = "90"  # 陆风
    baic = "92"  # 北京
    weilin = "94"  # 威麟
    opel = "95"  # 欧宝
    karry = "96"  # 开瑞
    huapu = "97"  # 华普
    acura = "103"  # 讴歌
    qichen = "104"  # 启辰
    baic_making = "107"  # 北汽制造
    luxgen = "108"  # 纳智捷
    yema = "109"  # 野马
    zhongxing = "110"  # 中兴
    chrysler = "112"  # 克莱斯勒
    gac_geomobile = "113"  # 广汽吉奥
    ruilin = "115"  # 瑞麟
    jaguar = "117"  # 捷豹
    tata_daewoo = "119"  # 唐骏欧铃
    fudi = "121"  # 福迪
    lotus = "122"  # 莲花
    dualis = "124"  # 双环
    yongyuan = "128"  # 永源
    jiangnan = "136"  # 江南
    dodge = "144"  # 道奇
    daton_auto = "155"  # 大运汽车
    northern_bus = "167"  # 北方客车
    klt = "176"  # 九龙
    bentley = "191"  # 宾利
    shuchibust = "201"  # 舒驰客车
    red_flag = "230"  # 红旗
