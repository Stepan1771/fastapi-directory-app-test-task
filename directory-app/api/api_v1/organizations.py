from typing import Annotated, List, Sequence

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import db_helper

from api.dependencies.api_key import verify_api_key

import crud.organizations as crud_organizations
from core.schemas.organization import Organization

from core.schemas.search_radius import SearchRadius

router = APIRouter(
    prefix=settings.api.v1.organizations,
    tags=["Organizations"],
)


@router.get(
    "/get-organizations-in-building",
    response_model=List[Organization],
)
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


@router.get(
    "/get-organizations-by-activity",
    response_model=List[Organization],
)
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


@router.post("/get-organizations-in-radius")
async def get_organizations_in_radius(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
        api_key: Annotated[
            str,
            Depends(verify_api_key),
        ],
        search_radius: SearchRadius,
):
    result = await crud_organizations.get_all_organizations_in_radius(
        session=session,
        api_key=api_key,
        search_radius=search_radius,
    )
    return result


@router.get(
    "/get-organizations-by-id",
    response_model=Organization,
)
async def get_organizations_by_id(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
        api_key: Annotated[
            str,
            Depends(verify_api_key),
        ],
        organization_id: int,
):
    result = await crud_organizations.get_organization_by_id(
        session=session,
        api_key=api_key,
        organization_id=organization_id,
    )
    return result


@router.get(
    "/get-organizations-by-activity-type",
    response_model=List[Organization],
)
async def get_organizations_by_activity_type(
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
    result = await crud_organizations.search_organizations_by_activity_type(
        session=session,
        api_key=api_key,
        activity_id=activity_id,
    )
    return result


@router.get(
    "/get-organizations-by-name",
    response_model=List[Organization],
)
async def get_organizations_by_name(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
        api_key: Annotated[
            str,
            Depends(verify_api_key),
        ],
        organization_name: str,
):
    result = await crud_organizations.search_organizations_by_name(
        session=session,
        api_key=api_key,
        organization_name=organization_name,
    )
    return result