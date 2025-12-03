from pydantic import BaseModel
from typing import List
from models import Subscribe, APE


class VIIDHeaders(BaseModel):
    content_type: str = "application/VIID+JSON"


class ResponseStatusObject(BaseModel):
    RequestURL: str
    StatusCode: str
    StatusString: str
    LocalTime: str


class SubscribeObject(BaseModel):
    SubscribeObject: List[Subscribe]


class SubscribeListObject(BaseModel):
    SubscribeListObject: SubscribeObject


class APEObject(BaseModel):
    APEObject: List[APE]


class APEListObject(BaseModel):
    APEListObject: APEObject
