import brokers
from models import Person
from collections.abc import Sequence
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
import exceptions
from database import engine


async def get_person_task(person_id: str) -> Person:
    async with AsyncSession(engine) as session:
        statement = select(Person).where(Person.PersonID == person_id)
        person = (await session.exec(statement)).first()
        if not person:
            raise exceptions.DataNotFoundError(detail=f"{person_id} not exist")
    return person


async def list_persons_task() -> Sequence[Person]:
    async with AsyncSession(engine) as session:
        persons = (await session.exec(select(Person))).all()
        if not persons:
            raise exceptions.DataNotFoundError(detail="No Person data exist")
        return persons


@brokers.broker.task
async def create_person_task(person: Person) -> Person:
    async with AsyncSession(engine) as session:
        session.add(person)
        await session.commit()
        await session.refresh(person)
        return person


@brokers.broker.task
async def create_persons_task(persons: list[Person]) -> list[Person]:
    async with AsyncSession(engine) as session:
        session.add_all(persons)
        await session.commit()
        await session.refresh(persons)
        return persons


@brokers.broker.task
async def update_person_task(person: Person):
    async with AsyncSession(engine) as session:
        session.add(person)
        await session.commit()
        await session.refresh(person)
        return person


@brokers.broker.task
async def update_persons_task(persons: list[Person]):
    async with AsyncSession(engine) as session:
        session.add_all(persons)
        await session.commit()
        await session.refresh(persons)
        return persons


@brokers.broker.task
async def delete_person_task(person_id: str):
    async with AsyncSession(engine) as session:
        await session.delete(Person.model_validate(person_id))
        await session.commit()
        return person_id


@brokers.broker.task
async def delete_persons_task(person_ids: list[str]):
    async with AsyncSession(engine) as session:
        for person_id in person_ids:
            await session.delete(Person.model_validate(person_id))
        await session.commit()
        return person_ids
