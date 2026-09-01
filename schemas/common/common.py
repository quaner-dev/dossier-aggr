from sqlmodel import SQLModel

from domain.common import PictureQueryCondition


class PictureQueryConditionList(SQLModel):
    PictureQueryConditionObject: list[PictureQueryCondition]
