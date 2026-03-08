from collections.abc import Sequence

import exceptions
from database import engine
from models import Person
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession


async def get_person_repo(person_id: str) -> Person:
    async with AsyncSession(engine) as session:
        statement = select(Person).where(Person.PersonID == person_id)
        person = (await session.exec(statement)).first()
        if not person:
            raise exceptions.DataNotFoundError(detail=f"{person_id} not exist")
    return person


async def list_persons_repo() -> Sequence[Person]:
    async with AsyncSession(engine) as session:
        persons = (await session.exec(select(Person))).all()
        if not persons:
            raise exceptions.DataNotFoundError(detail="No Person data exist")
        return persons


async def create_person_repo(person: Person) -> Person:
    async with AsyncSession(engine) as session:
        session.add(person)
        await session.commit()
        await session.refresh(person)
        return person


async def create_persons_repo(persons: list[Person]) -> list[Person]:
    async with AsyncSession(engine) as session:
        session.add_all(persons)
        await session.commit()
        for person in persons:
            await session.refresh(person)
        return persons


async def update_person_repo(person: Person) -> Person:
    async with AsyncSession(engine) as session:
        statement = select(Person).where(Person.PersonID == person.PersonID)
        if not (await session.exec(statement)).first():
            raise exceptions.DataNotFoundError(detail=f"{person.PersonID} not exist")
        session.add(person)
        await session.commit()
        await session.refresh(person)
        return person


async def update_persons_repo(persons: list[Person]) -> list[Person]:
    async with AsyncSession(engine) as session:
        for person in persons:
            statement = select(Person).where(Person.PersonID == person.PersonID)
            if not (await session.exec(statement)).first():
                raise exceptions.DataNotFoundError(detail=f"{person.PersonID} not exist")
            session.add(person)

        await session.commit()
        for person in persons:
            await session.refresh(person)
        return persons


async def delete_person_repo(person_id: str) -> str:
    async with AsyncSession(engine) as session:
        statement = select(Person).where(Person.PersonID == person_id)
        person = (await session.exec(statement)).first()
        if not person:
            raise exceptions.DataNotFoundError(detail=f"{person_id} not exist")
        await session.delete(person)
        await session.commit()
        return person_id


async def delete_persons_repo(person_ids: list[str]) -> list[str]:
    async with AsyncSession(engine) as session:
        for person_id in person_ids:
            statement = select(Person).where(Person.PersonID == person_id)
            person = (await session.exec(statement)).first()
            if not person:
                raise exceptions.DataNotFoundError(detail=f"{person_id} not exist")
            await session.delete(person)
        await session.commit()
        return person_ids
