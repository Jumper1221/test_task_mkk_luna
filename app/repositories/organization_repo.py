from geoalchemy2 import Geography
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from app.models.buildings import Building
from app.models.organization_activities import OrganizationActivity
from app.models.organizations import Organization
from app.repositories.base_repo import BaseRepository


class OrganizationRepository(BaseRepository):
    def _base_query(self):
        return select(Organization).options(
            selectinload(Organization.building),
            selectinload(Organization.phones),
            selectinload(Organization.activities),
        )

    async def get_by_id(self, org_id: int) -> Organization | None:
        """Поиск организации по её идентификатору"""
        stmt = self._base_query().where(Organization.id == org_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_in_radius(
        self, lat: float, lon: float, radius_km: float
    ) -> list[Organization]:
        """
        Поиск организаций, которые находятся в заданном радиусе
        относительно указанной точки на карте
        """
        user_point = func.ST_SetSRID(func.ST_MakePoint(lon, lat), 4326)

        stmt = (
            self._base_query()
            .join(Organization.building)
            .where(
                func.ST_DWithin(
                    Building.location.cast(Geography(srid=4326)),
                    user_point.cast(Geography(srid=4326)),
                    radius_km * 1000,
                )
            )
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_building(self, building_id: int) -> list[Organization]:
        """список всех организаций находящихся в конкретном здании"""
        stmt = self._base_query().where(Organization.building_id == building_id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_activity_ids(self, activity_ids: list[int]) -> list[Organization]:
        """Ищет организации, у которых есть ХОТЯ БЫ ОДНА деятельность из списка ids"""
        stmt = (
            self._base_query()
            .join(
                OrganizationActivity,
                OrganizationActivity.organization_id == Organization.id,
            )
            .where(OrganizationActivity.activity_id.in_(activity_ids))
            .distinct()
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_name(self, name_part: str) -> list[Organization]:
        """Поиск организации по названию"""
        stmt = self._base_query().where(Organization.name.ilike(f"%{name_part}%"))
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
