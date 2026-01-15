from fastapi import APIRouter

from .register import router as register_router
from .unregister import router as unregister_router
from .keepalive import router as keepalive_router
from .aps import router as aps_router
from .ape import router as ape_router
from .face import router as face_router
from .person import router as person_router
from .motor_vehicle import router as motor_vehicle_router
from .non_motor_vehicle import router as non_motor_vehicle_router
from .subscribe_notification import router as subscribe_notification_router
from .subscrbe import router as subscrbe_router
from .archives import router as archives_router
from .archive_subject import router as archive_subject_router

router = APIRouter()

router.include_router(register_router)
router.include_router(unregister_router)
router.include_router(keepalive_router)
router.include_router(aps_router)
router.include_router(ape_router)
router.include_router(face_router)
router.include_router(person_router)
router.include_router(motor_vehicle_router)
router.include_router(non_motor_vehicle_router)
router.include_router(subscrbe_router)
router.include_router(subscribe_notification_router)
router.include_router(archives_router)
router.include_router(archive_subject_router)

__all__ = ["router"]
