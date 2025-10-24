from typing import List

from pydantic import BaseModel

from core.schemas.activity import Activity
from core.schemas.building import Building


class OrganizationBase(BaseModel):
    id: int
    name: str
    phone_numbers: List[str]

    class Config:
        from_attributes = True


class Organization(OrganizationBase):
    building: Building
    activities: List[Activity]

    class Config:
        from_attributes = True



class OrganizationWithDistance(Organization):
    distance: float | None = None

    class Config:
        from_attributes = True