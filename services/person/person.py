from models import Person
from tasks import (
    get_person,
    list_persons,
    create_person,
    create_persons,
    update_person,
    update_persons,
    delete_person,
)
from services.common.common import BaseService
from collections.abc import Sequence


class PersonService(BaseService):
    async def get_person(self, person_id: str) -> Person:
        """根据PersonID查询人员信息"""
        person = await get_person(person_id=person_id)
        return person

    async def list_persons(self) -> Sequence[Person]:
        """查询所有人员信息"""
        persons = await list_persons()
        return persons

    async def create_person(self, person: Person):
        """创建人员信息"""
        _ = await create_person.kiq(person=person)

    async def create_persons(self, persons: list[Person]):
        """创建多个人员信息"""
        _ = await create_persons.kiq(persons=persons)

    async def update_person(self, person: Person) -> None:
        """更新人员信息"""
        _ = await update_person.kiq(person=person)
        await self.session.commit()

    async def update_persons(self, persons: list[Person]) -> None:
        """批量更新人员信息"""
        _ = await update_persons.kiq(persons=persons)

    async def delete_person(self, person_id: str) -> None:
        """删除人员信息"""
        _ = await delete_person.kiq(person_id=person_id)
        await self.session.commit()
