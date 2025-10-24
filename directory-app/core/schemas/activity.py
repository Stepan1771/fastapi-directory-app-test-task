from typing import List

from pydantic import BaseModel


class ActivityBase(BaseModel):
    id: int
    name: str
    level: int

    class Config:
        from_attributes = True

class Activity(ActivityBase):
    parent_id: int | None = None
    children: List['Activity'] = []

    class Config:
        from_attributes = True