from sqlmodel import Field, SQLModel  # type: ignore

import base


class PersonSubImageInfoLink(SQLModel, table=True):
    PersonID: str = Field(foreign_key="person.PersonID", primary_key=True)
    ImageID: str = Field(
        foreign_key="subimageinfo.ImageID", primary_key=True, unique=True
    )


class Person(base.person.PersonBase, table=True): ...
