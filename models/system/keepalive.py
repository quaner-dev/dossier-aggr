from sqlmodel import SQLModel, Field


class Keepalive(SQLModel):
    """GA/T 1400.3-2017 C.27 保活对象"""

    DeviceID: str = Field(description="设备编码", max_length=20)


# 保活对象结构
class KeepaliveSchema(SQLModel):
    KeepaliveObject: Keepalive
