from typing import Annotated, List, Sequence

from fastapi import Depends, HTTPException
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from api.dependencies.api_key import verify_api_key
from core.models import Organization, Building, Activity, OrganizationActivity



async def get_all_organizations_in_building(
        session: AsyncSession,
        api_key: Depends(verify_api_key),
        building_id: int,
) -> Sequence[Organization]:
    stmt = await session.execute(
        select(Organization)
        .options(joinedload(Organization.building),
                 joinedload(Organization.activities))
        .filter(Organization.building_id == building_id)
    )
    organizations = stmt.unique().scalars().all()

    if not organizations:
        raise HTTPException(status_code=404, detail="Organization not found")

    return organizations


async def get_all_organizations_by_activity(
        session: AsyncSession,
        api_key: Depends(verify_api_key),
        activity_id: int,
):
    stmt = await session.execute(
        select(Activity)
        .filter(Activity.id == activity_id)
    )
    activity = stmt.scalars().first()

    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    stmt = await session.execute(
        select(Organization)
        .options(
            selectinload(Organization.building),
            selectinload(Organization.activities)
        )
        .filter(Organization.activities.any(Activity.id == activity_id))
    )
    organizations = stmt.unique().scalars().all()

    return organizations


async def get_all_organizations_in_area():
    pass


async def get_organization_by_id():
    pass


async def search_organizations_by_type_activity():
    pass


async def search_organizations_by_name():
    pass