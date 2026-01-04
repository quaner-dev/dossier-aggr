from typing import List

from pydantic import BaseModel, Field

import base
from .person import PersonList
from .face import FaceList


class SubscribeNotification(base.subscribe_notification.SubscribeNotificationBase):
    """GA/T 1400.3-2017 A.20 通知对象"""

    PersonObjectList: PersonList | None = Field(default=None, description="人员信息")
    FaceObjectList: FaceList | None = Field(default=None, description="人脸信息")


class SubscribeNotificationList(BaseModel):
    """GA/T 1400.3-2017 C.20 通知对象列表"""

    SubscribeNotificationObject: List[SubscribeNotification]


# 通知对象列表结构
class SubscribeNotificationListSchema(BaseModel):
    SubscribeNotificationListObject: SubscribeNotificationList
