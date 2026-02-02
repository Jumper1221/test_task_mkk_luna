from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.organizations import Organisation


class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("activities.id"), nullable=True
    )
    level: Mapped[int] = mapped_column(nullable=False, default=1)

    __table_args__ = (CheckConstraint("level BETWEEN 1 AND 3", name="check_max_depth"),)

    parent: Mapped["Activity | None"] = relationship(
        "Activity", remote_side=[id], back_populates="children"
    )
    children: Mapped[list["Activity"]] = relationship(
        "Activity", back_populates="parent", cascade="all, delete-orphan"
    )

    organizations: Mapped[list["Organisation"]] = relationship(
        "Organisation",
        secondary="organisation_activities",
        back_populates="activities",
        passive_deletes=True,
    )
