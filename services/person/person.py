from models import Person
from repo.person.person import get_person_repo, list_persons_repo
from tasks import (
    create_person_task,
    create_persons_task,
    update_person_task,
    update_persons_task,
    delete_person_task,
    delete_persons_task,
)
from collections.abc import Sequence
from services.task_dispatch import dispatch_and_wait


class PersonService():
    """编排 GA/T 1400 人员资源业务链路。

    单查和列表读取直接委托 repo；创建、更新和删除通过 Taskiq task
    写入，兼容单资源与批量接口共用同一 service。
    """

    async def get_person(self, person_id: str) -> Person:
        """根据PersonID查询人员信息"""
        person = await get_person_repo(person_id=person_id)
        return person

    async def list_persons(self) -> Sequence[Person]:
        """查询所有人员信息"""
        persons = await list_persons_repo()
        return persons

    async def create_person(self, person: Person):
        """创建人员信息"""
        _ = await dispatch_and_wait(create_person_task, person=person)

    async def create_persons(self, persons: list[Person]):
        """创建多个人员信息"""
        _ = await dispatch_and_wait(create_persons_task, persons=persons)

    async def update_person(self, person: Person) -> None:
        """更新人员信息"""
        _ = await dispatch_and_wait(update_person_task, person=person)

    async def update_persons(self, persons: list[Person]) -> None:
        """批量更新人员信息"""
        _ = await dispatch_and_wait(update_persons_task, persons=persons)

    async def delete_person(self, person_id: str) -> None:
        """删除人员信息"""
        _ = await dispatch_and_wait(delete_person_task, person_id=person_id)

    async def delete_persons(self, person_ids: list[str]) -> None:
        """批量删除人员信息"""
        _ = await dispatch_and_wait(delete_persons_task, person_ids=person_ids)
