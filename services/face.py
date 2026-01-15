from typing import List

from sqlmodel import select

from schemas import Face
from tasks import create_face
from models import Face as FaceModel
from base import FaceBase
import exceptions
from .common import BaseService


class FaceService(BaseService):
    async def create_face(self, face: Face):
        await create_face.kiq(face)

    async def batch_create_faces(self, faces: List[Face]):
        for face in faces:
            await create_face.kiq(face)

    async def get_face(self, face_id: str) -> FaceBase:
        """根据FaceID查询人脸信息"""
        statement = select(FaceModel).where(FaceModel.FaceID == face_id)
        face = (await self.session.exec(statement)).first()
        if not face:
            raise exceptions.DataNotFoundError(detail=f"{face_id} not exist")
        return FaceBase.model_validate(face)

    async def list_faces(self) -> List[FaceBase]:
        """查询所有人脸信息"""
        statement = select(FaceModel)
        faces = (await self.session.exec(statement)).all()
        if not faces:
            raise exceptions.DataNotFoundError(detail="No Face data exist")
        return [FaceBase.model_validate(face) for face in faces]

    async def update_face(self, face_id: str, face: Face) -> FaceModel:
        """更新人脸信息"""
        statement = select(FaceModel).where(FaceModel.FaceID == face_id)
        db_face = (await self.session.exec(statement)).first()
        if not db_face:
            raise exceptions.DataNotFoundError(detail=f"{face_id} not exist")
        
        # 更新基础字段
        face_base = FaceBase.model_validate(face)
        for key, value in face_base.model_dump(exclude={"id"}).items():
            setattr(db_face, key, value)
        
        self.session.add(db_face)
        await self.session.commit()
        await self.session.refresh(db_face)
        return db_face

    async def delete_face(self, face_id: str) -> None:
        """删除人脸信息"""
        statement = select(FaceModel).where(FaceModel.FaceID == face_id)
        db_face = (await self.session.exec(statement)).first()
        if not db_face:
            raise exceptions.DataNotFoundError(detail=f"{face_id} not exist")
        
        await self.session.delete(db_face)
        await self.session.commit()
