from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.activities import Activity
    from app.models.buildings import Building
    from app.models.phones import Phone


class Organisation(Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    building_id: Mapped[int] = mapped_column(ForeignKey("buildings.id"), nullable=False)

    building: Mapped["Building"] = relationship(
        "Building", back_populates="organizations"
    )

    phones: Mapped[list["Phone"]] = relationship(
        back_populates="organization", cascade="all, delete-orphan"
    )

    activities: Mapped[list["Activity"]] = relationship(
        "Activity",
        secondary="organisation_activities",
        back_populates="organizations",
        passive_deletes=True,
    )
