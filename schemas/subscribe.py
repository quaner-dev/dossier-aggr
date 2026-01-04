from typing import List

from pydantic import BaseModel

import base


class SubscribeList(BaseModel):
    """GA/T 1400.3-2017 C.19 订阅对象列表"""

    SubscribeObject: List[base.subscribe.SubscribeBase]


# 订阅对象列表结构
class SubscribeListSchema(BaseModel):
    SubscribeListObject: SubscribeList
