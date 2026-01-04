from typing import List

from pydantic import BaseModel, Field

import base
from .sub_image_info import SubImageInfo


class Person(base.person.PersonBase):
    """GA/T 1400.3-2017 A.8 人员对象"""

    SubImageList: List[SubImageInfo] | None = Field(description="图像列表")


class PersonList(BaseModel):
    """GA/T 1400.3-2017 C.8 人员对象列表"""

    PersonObject: List[Person]


# 人员对象列表结构
class PersonListObjectSchema(BaseModel):
    PersonListObject: PersonList
