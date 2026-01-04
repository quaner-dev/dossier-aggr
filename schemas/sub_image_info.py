from typing import List

from pydantic import BaseModel, Field

import base


class SubImageInfo(base.SubImageInfoBase):
    """GA/T 1400.3-2017 C.6 图像子对象"""

    FeatureInfoObject: base.feature_info.FeatureInfoBase = Field(
        description="特征值属性"
    )


class SubImageInfoList(BaseModel):
    """GA/T 1400.3-2017 C.6 子图像对象列表"""

    SubImageInfoObject: List[base.sub_image_info.SubImageInfoBase]
