from typing import List

from fastapi import HTTPException

from app.models.buildings import Building
from app.repositories.building_repo import BuildingRepository


class BuildingService:
    def __init__(self, building_repo: BuildingRepository):
        self.building_repo = building_repo

    async def get_by_id(self, building_id: int) -> Building:
        """Получить здание по его идентификатору"""
        building = await self.building_repo.get_by_id(building_id)

        if not building:
            raise HTTPException(status_code=404, detail="Здание не найдено")

        return building

    async def get_all(self) -> List[Building]:
        """Получить все здания"""
        return await self.building_repo.get_all()
