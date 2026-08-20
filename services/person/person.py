from models import Person
from repo.person.person import (
    create_person_repo,
    create_persons_repo,
    delete_person_repo,
    delete_persons_repo,
    get_person_repo,
    list_persons_repo,
    update_person_repo,
    update_persons_repo,
)


class PersonService:
    """编排 GA/T 1400 人员资源业务链路。

    读写请求统一委托 repo，保证请求完成时数据已经持久化。
    """

    async def get_person(self, person_id: str) -> Person:
        """根据PersonID查询人员信息"""
        return await get_person_repo(person_id=person_id)

    async def list_persons(self) -> list[Person]:
        """查询所有人员信息"""
        return list(await list_persons_repo())

    async def create_person(self, person: Person) -> Person:
        """创建人员信息"""
        return await create_person_repo(person=person)

    async def create_persons(self, persons: list[Person]) -> list[Person]:
        """创建多个人员信息"""
        return await create_persons_repo(persons=persons)

    async def update_person(self, person: Person) -> Person:
        """更新人员信息"""
        return await update_person_repo(person=person)

    async def update_persons(self, persons: list[Person]) -> list[Person]:
        """批量更新人员信息"""
        return await update_persons_repo(persons=persons)

    async def delete_person(self, person_id: str) -> str:
        """删除人员信息"""
        return await delete_person_repo(person_id=person_id)

    async def delete_persons(self, person_ids: list[str]) -> list[str]:
        """批量删除人员信息"""
        return await delete_persons_repo(person_ids=person_ids)
