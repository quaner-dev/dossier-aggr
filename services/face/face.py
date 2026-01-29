from sqlmodel import select

from models import Face
from tasks import create_face, create_faces
import exceptions
from services.common.common import BaseService
from collections.abc import Sequence


class FaceService(BaseService):
    async def create_face(self, face: Face):
        _ = await create_face.kiq(face)

    async def create_faces(self, faces: list[Face]):
        _ = await create_faces.kiq(faces=faces)

    async def get_face(self, face_id: str) -> Face:
        """根据FaceID查询人脸信息"""
        statement = select(Face).where(Face.FaceID == face_id)
        face = (await self.session.exec(statement)).first()
        if not face:
            raise exceptions.DataNotFoundError(detail=f"{face_id} not exist")
        return face

    async def list_faces(self) -> Sequence[Face]:
        """查询所有人脸信息"""
        statement = select(Face)
        faces = (await self.session.exec(statement)).all()
        if not faces:
            raise exceptions.DataNotFoundError(detail="No Face data exist")
        return faces

    async def update_face(self, face_id: str, face: Face) -> None:
        """更新人脸信息"""
        statement = select(Face).where(Face.FaceID == face_id)
        db_face = (await self.session.exec(statement)).first()
        if not db_face:
            raise exceptions.DataNotFoundError(detail=f"{face_id} not exist")

        # 更新基础字段
        for key, value in face.model_dump(exclude={"id"}).items():
            setattr(db_face, key, value)

        self.session.add(db_face)
        await self.session.commit()

    async def delete_face(self, face_id: str) -> None:
        """删除人脸信息"""
        statement = select(Face).where(Face.FaceID == face_id)
        db_face = (await self.session.exec(statement)).first()
        if not db_face:
            raise exceptions.DataNotFoundError(detail=f"{face_id} not exist")

        await self.session.delete(db_face)
        await self.session.commit()
