from models import Face
from tasks import (
    get_face_task,
    list_faces_task,
    create_face_task,
    create_faces_task,
    update_face_task,
    delete_face_task,
)
from collections.abc import Sequence


class FaceService:
    async def get_face(self, face_id: str) -> Face:
        """根据FaceID查询人脸信息"""
        face = await get_face_task(face_id=face_id)
        return face

    async def list_faces(self) -> Sequence[Face]:
        """查询所有人脸信息"""
        faces = await list_faces_task()
        return faces

    async def create_face(self, face: Face):
        _ = await create_face_task.kiq(face)

    async def create_faces(self, faces: list[Face]):
        _ = await create_faces_task.kiq(faces=faces)

    async def update_face(self, face: Face) -> None:
        _ = await update_face_task.kiq(face=face)

    async def delete_face(self, face: Face) -> None:
        _ = await delete_face_task.kiq(face=face)
