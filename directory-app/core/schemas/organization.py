from typing import List

from pydantic import BaseModel

from core.schemas.activity import Activity
from core.schemas.building import Building


class OrganizationBase(BaseModel):
    id: int
    name: str
    phone_numbers: List[str]


class Organization(BaseModel):
    building: Building
    activities: List[Activity]