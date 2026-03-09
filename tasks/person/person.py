import brokers
from collections.abc import Sequence

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


async def get_person_task(person_id: str) -> Person:
    return await get_person_repo(person_id=person_id)


async def list_persons_task() -> Sequence[Person]:
    return await list_persons_repo()


@brokers.broker.task
async def create_person_task(person: Person) -> Person:
    return await create_person_repo(person=person)


@brokers.broker.task
async def create_persons_task(persons: list[Person]) -> list[Person]:
    return await create_persons_repo(persons=persons)


@brokers.broker.task
async def update_person_task(person: Person):
    return await update_person_repo(person=person)


@brokers.broker.task
async def update_persons_task(persons: list[Person]):
    return await update_persons_repo(persons=persons)


@brokers.broker.task
async def delete_person_task(person_id: str):
    return await delete_person_repo(person_id=person_id)


@brokers.broker.task
async def delete_persons_task(person_ids: list[str]):
    return await delete_persons_repo(person_ids=person_ids)
