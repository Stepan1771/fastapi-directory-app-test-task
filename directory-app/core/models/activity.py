from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, organization_activity


class Activity(Base):
    __tablename__ = 'activities'

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        index=True,
    )
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )
    parent_id: Mapped[int] = mapped_column(
        ForeignKey('activities.id'),
        nullable=True,
    )
    level: Mapped[int] = mapped_column(
        default=1,
    )

    parent = relationship(
        "Activity",
        remote_side=[id],
        backref="children",
    )

    organizations = relationship(
        "Organization",
        secondary=organization_activity,
        back_populates="activities"
    )