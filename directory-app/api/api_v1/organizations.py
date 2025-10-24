from typing import Annotated, List, Sequence

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import db_helper

from api.dependencies.api_key import verify_api_key
from core.schemas.organization import Organization

import crud.organizations as crud_organizations

router = APIRouter(
    prefix=settings.api.v1.organizations,
    tags=["Organizations"],
)


@router.get("/get-organizations-in-building")
async def get_organizations_in_building(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
        api_key: Annotated[
            str,
            Depends(verify_api_key),
        ],
        building_id: int,
):
    result = await crud_organizations.get_all_organizations_in_building(
        session=session,
        api_key=api_key,
        building_id=building_id,
    )
    return result


@router.get("/get-organizations-by-activity")
async def get_organizations_by_activity(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
        api_key: Annotated[
            str,
            Depends(verify_api_key),
        ],
        activity_id: int,
):
    result = await crud_organizations.get_all_organizations_by_activity(
        session=session,
        api_key=api_key,
        activity_id=activity_id,
    )
    return result
