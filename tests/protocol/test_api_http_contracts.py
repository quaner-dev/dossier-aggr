import asyncio

import httpx

import exceptions
from main import app
from models import Face, Person
from models.common import enums
from services.face.face import FaceService
from services.person.person import PersonService


class _FakePersonService:
    def __init__(self, persons: list[Person]):
        self._persons = persons

    async def list_persons(self):
        return self._persons

    async def get_person(self, person_id: str):
        for person in self._persons:
            if person.PersonID == person_id:
                return person
        raise exceptions.DataNotFoundError(detail=f"{person_id} not exist")


class _FakeFaceService:
    def __init__(self, faces: list[Face]):
        self._faces = faces

    async def get_face(self, face_id: str):
        for face in self._faces:
            if face.FaceID == face_id:
                return face
        raise exceptions.DataNotFoundError(detail=f"{face_id} not exist")

    async def list_faces(self):
        return self._faces[:100]


def _sample_persons() -> list[Person]:
    return [
        Person(
            PersonID="P-HTTP-001",
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
            PersonID="P-HTTP-002",
            InfoKind=enums.InfoKindEnum.AutoCollect,
            SourceID="SRC-P-002",
            DeviceID="DEV-P-002",
            LeftTopX=11,
            LeftTopY=21,
            RightBtmX=101,
            RightBtmY=201,
            SubImageList=None,
        ),
    ]


def _sample_faces() -> list[Face]:
    return [
        Face(
            FaceID="F-HTTP-001",
            InfoKind=enums.InfoKindEnum.AutoCollect,
            SourceID="SRC-F-001",
            DeviceID="DEV-F-001",
            LeftTopX=10,
            LeftTopY=20,
            RightBtmX=100,
            RightBtmY=200,
            SubImageList=None,
        ),
        Face(
            FaceID="F-HTTP-002",
            InfoKind=enums.InfoKindEnum.ManualCollect,
            SourceID="SRC-F-002",
            DeviceID="DEV-F-002",
            LeftTopX=11,
            LeftTopY=21,
            RightBtmX=101,
            RightBtmY=201,
            SubImageList=None,
        ),
    ]


def test_person_detail_route_and_error_contract_via_http():
    async def _run():
        async def _person_dep() -> _FakePersonService:
            return _FakePersonService(_sample_persons())

        app.dependency_overrides[PersonService] = _person_dep
        try:
            transport = httpx.ASGITransport(app=app)
            async with httpx.AsyncClient(
                transport=transport,
                base_url="http://test",
            ) as client:
                ok = await client.get("/VIID/Persons/P-HTTP-001")
                assert ok.status_code == 200
                assert ok.json()["PersonID"] == "P-HTTP-001"

                not_found = await client.get("/VIID/Persons/P-HTTP-404")
                assert not_found.status_code == 404
                body = not_found.json()
                assert "ResponseStatusListObject" in body
                assert isinstance(
                    body["ResponseStatusListObject"]["ResponseStatusObject"],
                    list,
                )
                assert (
                    body["ResponseStatusListObject"]["ResponseStatusObject"][0][
                        "StatusCode"
                    ]
                    == "404"
                )
        finally:
            app.dependency_overrides.pop(PersonService, None)

    asyncio.run(_run())


def test_person_face_query_filters_via_http():
    async def _run():
        async def _person_dep() -> _FakePersonService:
            return _FakePersonService(_sample_persons())

        async def _face_dep() -> _FakeFaceService:
            return _FakeFaceService(_sample_faces())

        app.dependency_overrides[PersonService] = _person_dep
        app.dependency_overrides[FaceService] = _face_dep
        try:
            transport = httpx.ASGITransport(app=app)
            async with httpx.AsyncClient(
                transport=transport,
                base_url="http://test",
            ) as client:
                person_res = await client.get(
                    "/VIID/Persons",
                    params={"person_ids": "P-HTTP-002"},
                )
                assert person_res.status_code == 200
                person_items = person_res.json()["PersonListObject"]["PersonObject"]
                assert len(person_items) == 1
                assert person_items[0]["PersonID"] == "P-HTTP-002"

                face_list_res = await client.get("/VIID/Faces")
                assert face_list_res.status_code == 200
                face_items = face_list_res.json()["FaceListObject"]["FaceObject"]
                assert len(face_items) == 2
                assert face_items[0]["FaceID"] == "F-HTTP-001"

                face_get_res = await client.get(
                    "/VIID/Faces",
                    params={"FaceID": "F-HTTP-001"},
                )
                assert face_get_res.status_code == 200
                face_get_items = face_get_res.json()["FaceListObject"]["FaceObject"]
                assert len(face_get_items) == 1
                assert face_get_items[0]["FaceID"] == "F-HTTP-001"
        finally:
            app.dependency_overrides.pop(PersonService, None)
            app.dependency_overrides.pop(FaceService, None)

    asyncio.run(_run())
