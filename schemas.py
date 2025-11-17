from pydantic import BaseModel
from typing import List
from pydantic import BeforeValidator
from datetime import datetime
from typing import Annotated
from models import Subscribe

CompactDateTime = Annotated[
    datetime, BeforeValidator(lambda v: datetime.strptime(v, "%Y%m%d%H%M%S"))
]


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
