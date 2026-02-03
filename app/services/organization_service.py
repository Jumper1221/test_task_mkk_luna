from typing import List

from fastapi import HTTPException

from app.models.organizations import Organization
from app.repositories.activity_repo import ActivityRepository
from app.repositories.organization_repo import OrganizationRepository


class OrganizationService:
    def __init__(
        self, org_repo: OrganizationRepository, activity_repo: ActivityRepository
    ):
        self.org_repo = org_repo
        self.activity_repo = activity_repo

    async def get_by_id(self, org_id: int) -> Organization:
        """Поиск по id организации"""
        org = await self.org_repo.get_by_id(org_id)

        if not org:
            raise HTTPException(status_code=404, detail="Организация не найдена")

        return org

    async def search_by_activity(self, activity_id: int) -> List[Organization]:
        """Поиск по дереву категорий"""
        all_ids = await self.activity_repo.get_all_child_ids(activity_id)

        if not all_ids:
            return []

        organizations = await self.org_repo.get_by_activity_ids(all_ids)
        return organizations

    async def search_by_name(self, name: str) -> List[Organization]:
        """Поиск по названию"""
        result = await self.org_repo.get_by_name(name)
        return result

    async def search_by_building_id(self, building_id: int) -> List[Organization]:
        """Все организации в конкретном здании"""
        result = await self.org_repo.get_by_building(building_id)
        return result

    async def search_by_location(
        self, lat: float, lon: float, radius_km: float
    ) -> List[Organization]:
        """Поиск в радиусе"""
        result = await self.org_repo.get_in_radius(lat, lon, radius_km)
        return result
