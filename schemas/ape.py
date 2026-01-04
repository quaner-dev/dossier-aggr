from typing import List

from pydantic import BaseModel

import base


# 采集设备对象列表
class APEList(BaseModel):
    APEObject: List[base.ape.APEBase]


# 采集设备对象列表结构
class APEListSchema(BaseModel):
    APEListObject: APEList
