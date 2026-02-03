from typing import List

from sqlalchemy import select

from app.models.buildings import Building
from app.repositories.base_repo import BaseRepository


class BuildingRepository(BaseRepository):
    async def get_by_id(self, building_id: int) -> Building | None:
        """Получить здание по его идентификатору"""
        stmt = select(Building).where(Building.id == building_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self) -> List[Building]:
        """Получить все здания"""
        stmt = select(Building)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
