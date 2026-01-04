from typing import List


import tasks
from schemas import Person

class PersonService:
    async def create_person(self, person: Person):
        await tasks.create_person.kiq(person)

    async def batch_create_persons(self, persons: List[Person]):
        for person in persons:
            await tasks.create_person(person)
