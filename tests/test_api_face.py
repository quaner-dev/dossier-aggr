import asyncio

from api.face.face import (
    face_delete,
    face_query,
    face_update,
    faces_create,
    faces_delete,
    faces_query,
    faces_update,
)
import exceptions
from models import Face, FaceList, FaceListObjectSchema
from models.common import enums
from tests.type_helpers import as_service, as_status_list


class _FakeFaceService:
    def __init__(self, faces: list[Face]):
        self._faces = faces
        self.created_with: list[Face] | None = None
        self.updated_with: list[Face] = []
        self.deleted_with: list[str] = []
        self.get_calls: list[str] = []
        self.list_calls: int = 0
        self.update_face_calls: list[str] = []
        self.update_faces_calls: list[list[str]] = []
        self.delete_face_calls: list[str] = []
        self.delete_faces_calls: list[list[str]] = []

    async def get_face(self, face_id: str) -> Face:
        self.get_calls.append(face_id)
        for face in self._faces:
            if face.FaceID == face_id:
                return face
        raise exceptions.DataNotFoundError(detail=f"{face_id} not exist")

    async def list_faces(self) -> list[Face]:
        self.list_calls += 1
        return self._faces[:100]

    async def create_faces(self, faces: list[Face]):
        self.created_with = faces
        return faces

    async def update_face(self, face: Face):
        self.update_face_calls.append(face.FaceID)
        self.updated_with.append(face)
        return face

    async def update_faces(self, faces: list[Face]):
        self.update_faces_calls.append([face.FaceID for face in faces])
        self.updated_with.extend(faces)
        return faces

    async def delete_face(self, face_id: str):
        self.delete_face_calls.append(face_id)
        self.deleted_with.append(face_id)
        return face_id

    async def delete_faces(self, face_ids: list[str]):
        self.delete_faces_calls.append(face_ids)
        self.deleted_with.extend(face_ids)
        return face_ids


def _sample_faces() -> list[Face]:
    return [
        Face(
            FaceID="F-001",
            InfoKind=enums.InfoKindEnum.AutoCollect,
            SourceID="SRC-001",
            DeviceID="DEV-001",
            LeftTopX=10,
            LeftTopY=20,
            RightBtmX=100,
            RightBtmY=200,
            SubImageList=None,
        ),
        Face(
            FaceID="F-002",
            InfoKind=enums.InfoKindEnum.ManualCollect,
            SourceID="SRC-002",
            DeviceID="DEV-002",
            LeftTopX=11,
            LeftTopY=21,
            RightBtmX=101,
            RightBtmY=201,
            SubImageList=None,
        ),
    ]


def test_face_query_uses_path_id_for_single_lookup():
    async def _run():
        fake = _FakeFaceService(_sample_faces())

        result = await face_query(
            service=as_service(fake),
            face_id="F-002",
        )

        assert result.FaceID == "F-002"
        assert fake.get_calls == ["F-002"]
        assert fake.list_calls == 0

    asyncio.run(_run())


def test_faces_query_lists_faces_with_default_pagination():
    async def _run():
        fake = _FakeFaceService(_sample_faces())

        result = await faces_query(service=as_service(fake))

        items = result.FaceListObject.FaceObject
        assert len(items) == 2
        assert fake.get_calls == []
        assert fake.list_calls == 1

    asyncio.run(_run())


def test_faces_create_update_delete_return_status_list():
    async def _run():
        faces = _sample_faces()
        fake = _FakeFaceService(faces)
        payload = FaceListObjectSchema(FaceListObject=FaceList(FaceObject=faces))

        create_res = await faces_create(data=payload, service=as_service(fake))
        update_res = await faces_update(data=payload, service=as_service(fake))
        delete_res = await faces_delete(
            id_list="F-001, F-002", service=as_service(fake)
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
        assert create_status[0].Id == "F-001"
        assert len(update_status) == 2
        assert update_status[1].Id == "F-002"
        assert len(delete_status) == 2
        assert delete_status[0].Id == "F-001"

        assert fake.created_with is not None
        assert len(fake.created_with) == 2
        assert len(fake.updated_with) == 2
        assert fake.deleted_with == ["F-001", "F-002"]
        assert fake.update_faces_calls == [["F-001", "F-002"]]
        assert fake.update_face_calls == []
        assert fake.delete_faces_calls == [["F-001", "F-002"]]
        assert fake.delete_face_calls == []

    asyncio.run(_run())


def test_face_update_delete_by_id_return_status():
    async def _run():
        fake = _FakeFaceService(_sample_faces())
        payload = _sample_faces()[0]

        update_res = await face_update(
            face_id="F-001",
            data=payload,
            service=as_service(fake),
        )
        delete_res = await face_delete(
            face_id="F-001",
            service=as_service(fake),
        )

        assert update_res.StatusCode == "0"
        assert update_res.Id == "F-001"
        assert update_res.RequestURL.endswith("/VIID/Faces/F-001")
        assert delete_res.StatusCode == "0"
        assert delete_res.Id == "F-001"
        assert delete_res.RequestURL.endswith("/VIID/Faces/F-001")
        assert len(fake.updated_with) == 1
        assert fake.updated_with[0].FaceID == "F-001"
        assert fake.deleted_with == ["F-001"]
        assert fake.update_face_calls == ["F-001"]
        assert fake.update_faces_calls == []
        assert fake.delete_face_calls == ["F-001"]
        assert fake.delete_faces_calls == []

    asyncio.run(_run())
