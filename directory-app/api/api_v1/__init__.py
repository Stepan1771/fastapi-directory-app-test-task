from fastapi import APIRouter

from core.config import settings

from .test import router as test_router



router = APIRouter(
    prefix=settings.api.v1.prefix,
)

router.include_router(test_router)
