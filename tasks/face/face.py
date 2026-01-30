import brokers
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from models import Face
from database import engine
import exceptions
from collections.abc import Sequence


async def get_face_task(face_id: str) -> Face:
    async with AsyncSession(engine) as session:
        statement = select(Face).where(Face.FaceID == face_id)
        face = (await session.exec(statement)).first()
        if not face:
            raise exceptions.DataNotFoundError(detail=f"{face_id} not exist")
        return face


async def list_faces_task() -> Sequence[Face]:
    async with AsyncSession(engine) as session:
        statement = select(Face)
        faces = (await session.exec(statement)).all()
        if not faces:
            raise exceptions.DataNotFoundError(detail="No Face data exist")
        return faces


@brokers.broker.task
async def create_face_task(face: Face):
    async with AsyncSession(engine) as session:
        session.add(face)
        await session.commit()
        await session.refresh(face)
        return face


@brokers.broker.task
async def create_faces_task(faces: list[Face]):
    async with AsyncSession(engine) as session:
        session.add_all(faces)
        await session.commit()
        await session.refresh(faces)
        return faces


@brokers.broker.task
async def update_face_task(face: Face):
    async with AsyncSession(engine) as session:
        session.add(face)
        await session.commit()
        await session.refresh(face)
        return face


@brokers.broker.task
async def delete_face_task(face: Face):
    async with AsyncSession(engine) as session:
        await session.delete(face)
        await session.commit()
        return face
