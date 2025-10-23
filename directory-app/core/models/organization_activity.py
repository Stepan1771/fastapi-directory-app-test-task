from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class OrganizationActivity(Base):
    __tablename__ = 'organizations_activities'

    organization_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('organizations.id'),
        primary_key=True,
    )
    activity_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('activities.id'),
        primary_key=True,
    )

