from pydantic import BaseModel, Field


class Keepalive(BaseModel):
    """GA/T 1400.3-2017 C.27 保活对象"""

    DeviceID: str = Field(description="设备编码", max_length=20)


# 保活对象结构
class KeepaliveSchema(BaseModel):
    KeepaliveObject: Keepalive
