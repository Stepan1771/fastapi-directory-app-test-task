from pydantic import BaseModel


class OrganizationActivity(BaseModel):
    organization_id: int
    activity_id: int

    class Config:
        from_attributes = True