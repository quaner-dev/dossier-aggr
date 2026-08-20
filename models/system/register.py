from sqlmodel import Field, SQLModel


class Register(SQLModel):
    """GA/T 1400.3-2017 C.26 注册对象"""

    DeviceID: str = Field(description="设备编码", max_length=20)


# 注册对象结构
class RegisterSchema(SQLModel):
    RegisterObject: Register
