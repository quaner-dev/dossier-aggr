from models import Person
from tasks import (
    get_person_task,
    list_persons_task,
    create_person_task,
    create_persons_task,
    update_person_task,
    update_persons_task,
    delete_person_task,
    delete_persons_task,
)
from collections.abc import Sequence


class PersonService():
    async def get_person(self, person_id: str) -> Person:
        """根据PersonID查询人员信息"""
        person = await get_person_task(person_id=person_id)
        return person

    async def list_persons(self) -> Sequence[Person]:
        """查询所有人员信息"""
        persons = await list_persons_task()
        return persons

    async def create_person(self, person: Person):
        """创建人员信息"""
        _ = await create_person_task.kiq(person=person)

    async def create_persons(self, persons: list[Person]):
        """创建多个人员信息"""
        _ = await create_persons_task.kiq(persons=persons)

    async def update_person(self, person: Person) -> None:
        """更新人员信息"""
        _ = await update_person_task.kiq(person=person)

    async def update_persons(self, persons: list[Person]) -> None:
        """批量更新人员信息"""
        _ = await update_persons_task.kiq(persons=persons)

    async def delete_person(self, person_id: str) -> None:
        """删除人员信息"""
        _ = await delete_person_task.kiq(person_id=person_id)

    async def delete_persons(self, person_ids: list[str]) -> None:
        """批量删除人员信息"""
        _ = await delete_persons_task.kiq(person_ids=person_ids)
