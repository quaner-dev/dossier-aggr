from fastapi import APIRouter

# 从功能模块导入所有路由
from .system.register import router as register_router
from .system.unregister import router as unregister_router
from .system.keepalive import router as keepalive_router
from .system.time import router as time_router
from .health.probes import router as probes_router
from .collection.aps import router as aps_router
from .collection.ape import router as ape_router
from .face.face import router as face_router
from .person.person import router as person_router
from .subscribe.subscrbe import router as subscrbe_router
from .subscribe.subscribe_notification import router as subscribe_notification_router
from .library.archive_library import router as archive_library_router
from .archive.archives import router as archives_router
from .archive.archive_subject import router as archive_subject_router
from .task.archive_task import router as archive_task_router
from .vehicle.vehicle_archive import router as vehicle_archive_router
from .vehicle.vehicle_archive_subject import router as vehicle_archive_subject_router
from .verify.archive_confidence import router as archive_confidence_router
from .verify.vehicle_archive_confidence import (
    router as vehicle_archive_confidence_router,
)

router = APIRouter()

router.include_router(register_router)
router.include_router(unregister_router)
router.include_router(keepalive_router)
router.include_router(time_router)
router.include_router(probes_router)
router.include_router(aps_router)
router.include_router(ape_router)
router.include_router(face_router)
router.include_router(person_router)
router.include_router(subscrbe_router)
router.include_router(subscribe_notification_router)
router.include_router(archive_library_router)
router.include_router(archives_router)
router.include_router(archive_subject_router)
router.include_router(archive_task_router)
router.include_router(vehicle_archive_router)
router.include_router(vehicle_archive_subject_router)
router.include_router(archive_confidence_router)
router.include_router(vehicle_archive_confidence_router)

__all__ = ["router"]
