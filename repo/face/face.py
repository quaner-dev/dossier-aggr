from collections.abc import Sequence

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from core import exceptions
from core.database import engine
from models import Face, FaceQueryParams


async def get_face_repo(face_id: str) -> Face:
    async with AsyncSession(engine) as session:
        statement = select(Face).where(Face.FaceID == face_id)
        face = (await session.exec(statement)).first()
        if not face:
            raise exceptions.DataNotFoundError(detail=f"{face_id} not exist")
        return face


async def list_faces_repo(query: FaceQueryParams) -> Sequence[Face]:
    async with AsyncSession(engine) as session:
        statement = select(Face).order_by(Face.FaceID)
        if query.RecordStartNo:
            statement = statement.offset(query.RecordStartNo)
        if query.PageRecordNum is not None:
            statement = statement.limit(query.PageRecordNum)
        faces = (await session.exec(statement)).all()
        return faces


async def create_face_repo(face: Face) -> Face:
    async with AsyncSession(engine) as session:
        session.add(face)
        await session.commit()
        await session.refresh(face)
        return face


async def create_faces_repo(faces: list[Face]) -> list[Face]:
    async with AsyncSession(engine) as session:
        session.add_all(faces)
        await session.commit()
        for face in faces:
            await session.refresh(face)
        return faces


async def update_face_repo(face: Face) -> Face:
    async with AsyncSession(engine) as session:
        statement = select(Face).where(Face.FaceID == face.FaceID)
        if not (await session.exec(statement)).first():
            raise exceptions.DataNotFoundError(detail=f"{face.FaceID} not exist")
        session.add(face)
        await session.commit()
        await session.refresh(face)
        return face


async def update_faces_repo(faces: list[Face]) -> list[Face]:
    async with AsyncSession(engine) as session:
        for face in faces:
            statement = select(Face).where(Face.FaceID == face.FaceID)
            if not (await session.exec(statement)).first():
                raise exceptions.DataNotFoundError(detail=f"{face.FaceID} not exist")
            session.add(face)

        await session.commit()
        for face in faces:
            await session.refresh(face)
        return faces


async def delete_face_repo(face_id: str) -> str:
    async with AsyncSession(engine) as session:
        statement = select(Face).where(Face.FaceID == face_id)
        face = (await session.exec(statement)).first()
        if not face:
            raise exceptions.DataNotFoundError(detail=f"{face_id} not exist")
        await session.delete(face)
        await session.commit()
        return face_id


async def delete_faces_repo(face_ids: list[str]) -> list[str]:
    async with AsyncSession(engine) as session:
        for face_id in face_ids:
            statement = select(Face).where(Face.FaceID == face_id)
            face = (await session.exec(statement)).first()
            if not face:
                raise exceptions.DataNotFoundError(detail=f"{face_id} not exist")
            await session.delete(face)
        await session.commit()
        return face_ids
