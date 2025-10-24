from pydantic import BaseModel


class GeoPoint(BaseModel):
    latitude: float
    longitude: float


class SearchRadius(BaseModel):
    center: GeoPoint
    radius_km: float