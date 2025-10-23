from sqlalchemy import String, ForeignKey, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .organization_activity import OrganizationActivity


class Organization(Base):
    __tablename__ = 'organizations'

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        index=True,
    )
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )
    phone_numbers: Mapped[int] = mapped_column(
        ARRAY(String(20)),
        nullable=False,
        default=[],
    )
    building_id: Mapped[int] = mapped_column(
        ForeignKey('buildings.id'),
        nullable=False,
    )

    building = relationship("Building", back_populates="organizations")
    activities = relationship(
        "Activity",
        secondary=OrganizationActivity.__table__,
        back_populates="organizations"
    )