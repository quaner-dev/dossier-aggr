from models import Face, FaceQueryParams
from repo.face.face import (
    create_face_repo,
    create_faces_repo,
    delete_face_repo,
    delete_faces_repo,
    get_face_repo,
    list_faces_repo,
    update_face_repo,
    update_faces_repo,
)


class FaceService:
    """编排 GA/T 1400 人脸资源业务链路。

    读写请求统一委托 repo，保证请求完成时数据已经持久化。
    """

    async def get_face(self, face_id: str) -> Face:
        """根据FaceID查询人脸信息"""
        return await get_face_repo(face_id=face_id)

    async def list_faces(self, query: FaceQueryParams) -> list[Face]:
        return list(await list_faces_repo(query=query))

    async def create_face(self, face: Face) -> Face:
        return await create_face_repo(face=face)

    async def create_faces(self, faces: list[Face]) -> list[Face]:
        return await create_faces_repo(faces=faces)

    async def update_face(self, face: Face) -> Face:
        return await update_face_repo(face=face)

    async def update_faces(self, faces: list[Face]) -> list[Face]:
        return await update_faces_repo(faces=faces)

    async def delete_face(self, face_id: str) -> str:
        return await delete_face_repo(face_id=face_id)

    async def delete_faces(self, face_ids: list[str]) -> list[str]:
        return await delete_faces_repo(face_ids=face_ids)
