from typing import List

from pydantic import BaseModel, Field

import base
from .sub_image_info import SubImageInfo


class NonMotorVehicle(base.non_motor_vehicle.NonMotorVehicleBase):
    """GA/T 1400.3-2017 A.10 非机动车对象"""

    SubImageList: List[SubImageInfo] | None = Field(description="图像列表")


class NonMotorVehicleList(BaseModel):
    """GA/T 1400.3-2017 C.10 非机动车对象列表"""

    NonMotorVehicleObject: List[NonMotorVehicle]


# 非机动车对象列表结构
class NonMotorVehicleListObjectSchema(BaseModel):
    NonMotorVehicleListObject: NonMotorVehicleList
