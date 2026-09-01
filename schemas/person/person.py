from sqlmodel import Field, SQLModel

from domain.person import Person as PersonDomain

from ..common.sub_image_info import SubImageInfoList


class Person(PersonDomain):
    SubImageList: SubImageInfoList | None = Field(default=None, description="图像列表")


class PersonList(SQLModel):
    PersonObject: list[Person]


class PersonListObjectSchema(SQLModel):
    PersonListObject: PersonList
