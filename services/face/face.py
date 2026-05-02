from collections.abc import Sequence

from models import Face, FaceQueryParams
from repo.face.face import get_face_repo, list_faces_repo
from services.task_dispatch import dispatch_and_wait
from tasks import (
    create_face_task,
    create_faces_task,
    update_face_task,
    update_faces_task,
    delete_face_task,
    delete_faces_task,
)


class FaceService:
    """编排 GA/T 1400 人脸资源业务链路。

    单查和列表读取直接委托 repo；创建、更新和删除通过 Taskiq task
    写入，兼容单资源与批量接口共用同一 service。
    """

    async def get_face(self, face_id: str) -> Face:
        """根据FaceID查询人脸信息"""
        face = await get_face_repo(face_id=face_id)
        return face

    async def list_faces(self, query: FaceQueryParams) -> Sequence[Face]:
        faces = await list_faces_repo(query=query)
        return faces

    async def create_face(self, face: Face):
        _ = await dispatch_and_wait(create_face_task, face=face)

    async def create_faces(self, faces: list[Face]):
        _ = await dispatch_and_wait(create_faces_task, faces=faces)

    async def update_face(self, face: Face) -> None:
        _ = await dispatch_and_wait(update_face_task, face=face)

    async def update_faces(self, faces: list[Face]) -> None:
        _ = await dispatch_and_wait(update_faces_task, faces=faces)

    async def delete_face(self, face_id: str) -> None:
        _ = await dispatch_and_wait(delete_face_task, face_id=face_id)

    async def delete_faces(self, face_ids: list[str]) -> None:
        _ = await dispatch_and_wait(delete_faces_task, face_ids=face_ids)
