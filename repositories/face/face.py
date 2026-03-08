from collections.abc import Sequence

import exceptions
from database import engine
from models import Face
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

_DEFAULT_FACE_LIST_LIMIT = 100


async def get_face_repo(face_id: str) -> Face:
    async with AsyncSession(engine) as session:
        statement = select(Face).where(Face.FaceID == face_id)
        face = (await session.exec(statement)).first()
        if not face:
            raise exceptions.DataNotFoundError(detail=f"{face_id} not exist")
        return face


async def list_faces_repo() -> Sequence[Face]:
    async with AsyncSession(engine) as session:
        statement = (
            select(Face).order_by(Face.FaceID.asc()).limit(_DEFAULT_FACE_LIST_LIMIT)
        )
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


async def delete_face_repo(face_id: str) -> str:
    async with AsyncSession(engine) as session:
        statement = select(Face).where(Face.FaceID == face_id)
        face = (await session.exec(statement)).first()
        if not face:
            raise exceptions.DataNotFoundError(detail=f"{face_id} not exist")
        await session.delete(face)
        await session.commit()
        return face_id
