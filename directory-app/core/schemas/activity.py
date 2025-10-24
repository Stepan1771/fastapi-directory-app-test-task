from pydantic import BaseModel


class Activity(BaseModel):
    id: int
    name: str
    parent_id: int | None
    level: int

    class Config:
        from_attributes = True