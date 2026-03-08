import asyncio

from api.person.person import (
    list_persons,
    create_persons,
    update_persons,
    delete_persons,
    get_person,
)
from models import Person, PersonList, PersonListObjectSchema
from models.common import enums
from tests.type_helpers import as_service, as_status_list


class _FakePersonService:
    def __init__(self, persons: list[Person]):
        self._persons = persons
        self.created_with: list[Person] | None = None
        self.updated_with: list[Person] | None = None
        self.deleted_with: list[str] | None = None

    async def list_persons(self):
        return self._persons

    async def get_person(self, person_id: str):
        return next(person for person in self._persons if person.PersonID == person_id)

    async def create_persons(self, persons: list[Person]):
        self.created_with = persons
        return persons

    async def update_persons(self, persons: list[Person]):
        self.updated_with = persons
        return persons

    async def delete_persons(self, person_ids: list[str]):
        self.deleted_with = person_ids
        return person_ids


def _sample_persons() -> list[Person]:
    return [
        Person(
            PersonID="P-001",
            InfoKind=enums.InfoKindEnum.AutoCollect,
            SourceID="SRC-P-001",
            DeviceID="DEV-P-001",
            LeftTopX=10,
            LeftTopY=20,
            RightBtmX=100,
            RightBtmY=200,
            SubImageList=None,
        ),
        Person(
            PersonID="P-002",
            InfoKind=enums.InfoKindEnum.ManualCollect,
            SourceID="SRC-P-002",
            DeviceID="DEV-P-002",
            LeftTopX=11,
            LeftTopY=21,
            RightBtmX=101,
            RightBtmY=201,
            SubImageList=None,
        ),
    ]


def test_persons_query_and_get_return_expected_schema():
    async def _run():
        persons = _sample_persons()
        fake = _FakePersonService(persons)

        list_res = await list_persons(service=as_service(fake))
        one_res = await get_person(person_id="P-001", service=as_service(fake))

        assert len(list_res.PersonListObject.PersonObject) == 2
        assert list_res.PersonListObject.PersonObject[0].PersonID == "P-001"
        assert one_res.PersonID == "P-001"

    asyncio.run(_run())


def test_persons_create_update_delete_return_status_list():
    async def _run():
        persons = _sample_persons()
        fake = _FakePersonService(persons)
        payload = PersonListObjectSchema(PersonListObject=PersonList(PersonObject=persons))

        create_res = await create_persons(data=payload, service=as_service(fake))
        update_res = await update_persons(data=payload, service=as_service(fake))
        delete_res = await delete_persons(
            service=as_service(fake), person_ids=["P-001", "P-002"]
        )

        create_status = as_status_list(
            create_res.ResponseStatusListObject.ResponseStatusObject
        )
        update_status = as_status_list(
            update_res.ResponseStatusListObject.ResponseStatusObject
        )
        delete_status = as_status_list(
            delete_res.ResponseStatusListObject.ResponseStatusObject
        )

        assert len(create_status) == 2
        assert create_status[0].StatusCode == "0"
        assert create_status[0].Id == "P-001"
        assert len(update_status) == 2
        assert update_status[1].Id == "P-002"
        assert len(delete_status) == 2
        assert delete_status[0].Id == "P-001"

        assert fake.created_with is not None
        assert len(fake.created_with) == 2
        assert fake.updated_with is not None
        assert len(fake.updated_with) == 2
        assert fake.deleted_with == ["P-001", "P-002"]

    asyncio.run(_run())
