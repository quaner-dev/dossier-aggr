from fastapi import APIRouter

from .register import router as register_router
from .ape import router as ape_router
from .archive_subject import router as archive_subject_router

router = APIRouter()

router.include_router(register_router)
router.include_router(ape_router)
router.include_router(archive_subject_router)
router.include_router(register_router)

__all__ = ["router"]
