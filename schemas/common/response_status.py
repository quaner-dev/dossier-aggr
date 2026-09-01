from sqlmodel import SQLModel

from domain.common import ResponseStatus


class ResponseStatusList(SQLModel):
    ResponseStatusObject: list[ResponseStatus]


class ResponseStatusListSchema(SQLModel):
    ResponseStatusListObject: ResponseStatusList
