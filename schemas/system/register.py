from sqlmodel import SQLModel

from domain.system import Register


class RegisterSchema(SQLModel):
    RegisterObject: Register
