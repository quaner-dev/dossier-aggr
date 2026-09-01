from sqlmodel import Field, SQLModel


class UnRegister(SQLModel):
    """GA/T 1400.3-2017 C.28 注销对象"""

    DeviceID: str = Field(description="设备编码", max_length=20)

