from sqlmodel import Field, SQLModel


class Keepalive(SQLModel):
    """GA/T 1400.3-2017 C.27 保活对象"""

    DeviceID: str = Field(description="设备编码", max_length=20)

