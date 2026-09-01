from collections.abc import Iterable

from pydantic import BaseModel
from sqlmodel import SQLModel


def to_table_model[TableModel: SQLModel](
    model_type: type[TableModel], value: BaseModel
) -> TableModel:
    if isinstance(value, model_type):
        return value
    return model_type.model_validate(value.model_dump())


def to_table_models[TableModel: SQLModel](
    model_type: type[TableModel], values: Iterable[BaseModel]
) -> list[TableModel]:
    return [to_table_model(model_type, value) for value in values]
