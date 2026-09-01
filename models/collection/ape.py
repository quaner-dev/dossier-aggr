from sqlalchemy import UniqueConstraint
from sqlmodel import Field

from domain.collection.ape import APE as APEDomain


class APE(APEDomain, table=True):
    __table_args__ = (UniqueConstraint("ApeID"),)

    id: int | None = Field(default=None, primary_key=True, exclude=True)
