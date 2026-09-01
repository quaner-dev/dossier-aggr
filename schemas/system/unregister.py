from sqlmodel import SQLModel

from domain.system import UnRegister


class UnRegisterSchema(SQLModel):
    UnRegisterObject: UnRegister
