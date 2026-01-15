from typing import List

from sqlmodel import select

import tasks
from schemas import Person
from models import Person as PersonModel
from base import PersonBase
import exceptions
from .common import BaseService


class PersonService(BaseService):
    async def create_person(self, person: Person):
        await tasks.create_person.kiq(person)

    async def batch_create_persons(self, persons: List[Person]):
        for person in persons:
            await tasks.create_person(person)

    async def get_person(self, person_id: str) -> PersonBase:
        """根据PersonID查询人员信息"""
        statement = select(PersonModel).where(PersonModel.PersonID == person_id)
        person = (await self.session.exec(statement)).first()
        if not person:
            raise exceptions.DataNotFoundError(detail=f"{person_id} not exist")
        return PersonBase.model_validate(person)

    async def list_persons(self) -> List[PersonBase]:
        """查询所有人员信息"""
        statement = select(PersonModel)
        persons = (await self.session.exec(statement)).all()
        if not persons:
            raise exceptions.DataNotFoundError(detail="No Person data exist")
        return [PersonBase.model_validate(person) for person in persons]

    async def update_person(self, person_id: str, person: Person) -> PersonModel:
        """更新人员信息"""
        statement = select(PersonModel).where(PersonModel.PersonID == person_id)
        db_person = (await self.session.exec(statement)).first()
        if not db_person:
            raise exceptions.DataNotFoundError(detail=f"{person_id} not exist")
        
        # 更新基础字段
        person_base = PersonBase.model_validate(person)
        for key, value in person_base.model_dump(exclude={"id"}).items():
            setattr(db_person, key, value)
        
        self.session.add(db_person)
        await self.session.commit()
        await self.session.refresh(db_person)
        return db_person

    async def delete_person(self, person_id: str) -> None:
        """删除人员信息"""
        statement = select(PersonModel).where(PersonModel.PersonID == person_id)
        db_person = (await self.session.exec(statement)).first()
        if not db_person:
            raise exceptions.DataNotFoundError(detail=f"{person_id} not exist")
        
        await self.session.delete(db_person)
        await self.session.commit()
