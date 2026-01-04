from typing import List

from schemas import Face
from tasks import create_face


class FaceService:
    async def create_face(self, face: Face):
        await create_face.kiq(face)

    async def batch_create_faces(self, faces: List[Face]):
        for face in faces:
            await create_face.kiq(face)
