from typing import List

from pydantic import BaseModel, Field

import base
from .sub_image_info import SubImageInfoList


class Archive(base.ArchiveBase):
    """GA/T 2350.5-2025 B.3 人员档案基础信息对象"""

    SubImageList: SubImageInfoList = Field(description="图片信息列表")


# 人员档案基础信息对象列表
class ArchiveList(BaseModel):
    ArchiveObject: List[Archive]


# 人员档案基础信息对象列表结构
class ArchiveListSchema(BaseModel):
    ArchiveListObject: ArchiveList
