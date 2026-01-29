from fastapi import APIRouter

# 从功能模块导入所有路由
from .system.register import router as register_router
from .system.unregister import router as unregister_router
from .system.keepalive import router as keepalive_router
from .collection.aps import router as aps_router
from .collection.ape import router as ape_router
from .face.face import router as face_router
from .person.person import router as person_router
from .subscribe.subscrbe import router as subscrbe_router
from .subscribe.subscribe_notification import router as subscribe_notification_router
from .library.archive_library import router as archive_library_router
from .archive.archives import router as archives_router
from .archive.archive_subject import router as archive_subject_router

router = APIRouter()

router.include_router(register_router)
router.include_router(unregister_router)
router.include_router(keepalive_router)
router.include_router(aps_router)
router.include_router(ape_router)
router.include_router(face_router)
router.include_router(person_router)
router.include_router(subscrbe_router)
router.include_router(subscribe_notification_router)
router.include_router(archive_library_router)
router.include_router(archives_router)
router.include_router(archive_subject_router)

__all__ = ["router"]
