from typing import Optional

from pydantic import BaseModel


class Activity(BaseModel):
    id: int
    name: str
    parent_id: Optional[int]
    level: int

    class Config:
        from_attributes = True