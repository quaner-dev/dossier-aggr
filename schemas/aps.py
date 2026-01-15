from typing import List

from pydantic import BaseModel

import base


# 采集系统对象列表
class APSList(BaseModel):
    APSObject: List[base.aps.APSBase]


# 采集系统对象列表结构
class APSListSchema(BaseModel):
    APSListObject: APSList
