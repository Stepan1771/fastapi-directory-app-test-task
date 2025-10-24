from typing import Annotated, List, Sequence

from fastapi import Depends, HTTPException
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from api.dependencies.api_key import verify_api_key
from core.models import Organization, Building, Activity, OrganizationActivity
from core.schemas.organization import OrganizationWithDistance

from core.schemas.search_radius import SearchRadius
from utils.calculate_radius import calculate_distance


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


async def get_all_organizations_in_radius(
        session: AsyncSession,
        api_key: Depends(verify_api_key),
        search_radius: SearchRadius,
):
    organizations_with_distance = []

    stmt = await session.execute(
        select(Organization)
        .options(joinedload(Organization.building),
                 joinedload(Organization.activities))
    )
    organizations = stmt.unique().scalars().all()

    if not organizations:
        raise HTTPException(status_code=404, detail="Organization not found")

    for org in organizations:
        distance = calculate_distance(
            search_radius.center.latitude, search_radius.center.longitude,
            org.building.latitude, org.building.longitude
        )

        if distance <= search_radius.radius_km:
            org_dict = OrganizationWithDistance.from_orm(org)
            org_dict.distance = round(distance, 2)
            organizations_with_distance.append(org_dict)

        # Сортируем по расстоянию
    organizations_with_distance.sort(key=lambda x: x.distance)

    return organizations_with_distance


async def get_organization_by_id(
        session: AsyncSession,
        api_key: Depends(verify_api_key),
        organization_id: int,
):
    stmt = await session.execute(
        select(Organization)
        .options(joinedload(Organization.building),
                 joinedload(Organization.activities))
        .filter(Organization.id == organization_id)
    )
    organization = stmt.scalars().first()
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")

    return organization


async def search_organizations_by_activity_type(
        session: AsyncSession,
        api_key: Depends(verify_api_key),
        activity_id: int,
):
    async def get_child_activity_ids(parent_id: int, current_level: int = 1) -> List[int]:
        """Рекурсивно получаем ID всех дочерних видов деятельности (до 3 уровня)"""
        if current_level > 3:  # Ограничение уровня вложенности
            return []

        stmt = await session.execute(
            select(Activity.id)
            .filter(Activity.parent_id == parent_id)
        )


        children_ids = stmt.scalars().all()
        child_ids = list(children_ids)

        for child_id in children_ids:
            grandchild_ids = await get_child_activity_ids(child_id, current_level + 1)
            child_ids.extend(grandchild_ids)

        return child_ids

        # Получаем все ID видов деятельности в поддереве
    all_activity_ids = [activity_id] + await get_child_activity_ids(activity_id)
    stmt = await session.execute(
        select(Organization)
        .options(joinedload(Organization.building),
                 joinedload(Organization.activities))
        .join(Organization.activities)
        .filter(Activity.id.in_(all_activity_ids))
        .distinct()
    )
    organizations = stmt.unique().scalars().all()

    return organizations


async def search_organizations_by_name(
        session: AsyncSession,
        api_key: Depends(verify_api_key),
        organization_name: str,
):
    stmt = await session.execute(
        select(Organization)
        .options(joinedload(Organization.building),
                 joinedload(Organization.activities))
        .filter(Organization.name.ilike(f"%{organization_name}%"))
    )
    organization = stmt.unique().scalars().all()
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")

    return organization