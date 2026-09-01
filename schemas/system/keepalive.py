from sqlmodel import SQLModel

from domain.system import Keepalive


class KeepaliveSchema(SQLModel):
    KeepaliveObject: Keepalive
