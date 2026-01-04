from datetime import datetime

from fastapi import APIRouter, Depends

import schemas
import constants
from services import FaceService

router = APIRouter()


@router.post(
    path=constants.FACES_URL,
    response_model=schemas.ResponseStatusListSchema,
    description="GA/T 1400.4-2017 7.2.12.1 批量人脸增加",
)
async def faces_create(
    data: schemas.FaceListObjectSchema, service: FaceService = Depends(FaceService)
):
    """批量人脸增加接口"""
    faces = data.FaceListObject.FaceObject
    await service.batch_create_faces(faces)

    response_status_objects = [
        schemas.ResponseStatus(
            RequestURL=constants.FACES_URL,
            StatusCode="0",
            StatusString="上传成功",
            Id=face.FaceID,
            LocalTime=datetime.now(),
        )
        for face in faces
    ]

    return schemas.ResponseStatusListSchema(
        ResponseStatusListObject=schemas.ResponseStatusList(
            ResponseStatusObject=response_status_objects
        )
    )
