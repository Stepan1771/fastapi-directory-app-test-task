from pydantic import BaseModel


class BuildingBase(BaseModel):
    id: int
    address: str
    latitude: float
    longitude: float


class Building(BaseModel):
    pass

    class Config:
        from_attrs = True