from sqlalchemy import UniqueConstraint
from sqlmodel import Field

from domain.collection.aps import APS as APSDomain


class APS(APSDomain, table=True):
    __table_args__ = (UniqueConstraint("ApsID"),)

    id: int | None = Field(default=None, primary_key=True, exclude=True)
