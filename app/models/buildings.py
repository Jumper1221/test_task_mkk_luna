from typing import TYPE_CHECKING

from geoalchemy2 import Geometry
from geoalchemy2.elements import WKBElement
from geoalchemy2.shape import to_shape
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.organizations import Organization


class Building(Base):
    __tablename__ = "buildings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    address: Mapped[str] = mapped_column(unique=True, nullable=False)
    location: Mapped[WKBElement] = mapped_column(Geometry("POINT", srid=4326))

    organizations: Mapped[list["Organization"]] = relationship(
        "Organization", back_populates="building"
    )

    @property
    def latitude(self) -> float:
        return to_shape(self.location).y  # type: ignore

    @property
    def longitude(self) -> float:
        return to_shape(self.location).x  # type: ignore
