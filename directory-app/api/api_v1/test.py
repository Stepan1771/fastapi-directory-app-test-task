from fastapi import APIRouter

from core.config import settings

from crud import test as crud_test


router = APIRouter(
    prefix=settings.api.v1.test,
    tags=["Test"],
)


@router.get("/test")
async def test():
    result = await crud_test.test()
    return result