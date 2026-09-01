from sqlmodel import SQLModel

from domain.common import FeatureInfo


class FeatureInfoList(SQLModel):
    FeatureInfoObject: list[FeatureInfo]
