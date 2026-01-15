from typing import List

from pydantic import BaseModel, Field

import base
from .sub_image_info import SubImageInfo


class MotorVehicle(base.motor_vehicle.MotorVehicleBase):
    """GA/T 1400.3-2017 A.11 机动车对象"""

    SubImageList: List[SubImageInfo] | None = Field(description="图像列表")


class MotorVehicleList(BaseModel):
    """GA/T 1400.3-2017 C.11 机动车对象列表"""

    MotorVehicleObject: List[MotorVehicle]


# 机动车对象列表结构
class MotorVehicleListObjectSchema(BaseModel):
    MotorVehicleListObject: MotorVehicleList
