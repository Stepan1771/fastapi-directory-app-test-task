from typing import List

from pydantic import BaseModel

from core.schemas.activity import Activity
from core.schemas.building import Building


class Organization(BaseModel):
    id: int
    name: str
    phone_numbers: List[str]
    building: Building
    activities: List[Activity]

    class Config:
        from_attributes = True


class OrganizationDistance(Organization):
    distance: float | None = None