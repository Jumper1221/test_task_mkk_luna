from sqlalchemy import select

from app.models.activities import Activity
from app.repositories.base_repo import BaseRepository


class ActivityRepository(BaseRepository):
    async def get_all_child_ids(self, activity_id: int) -> list[int]:
        """
        Возвращает ID самой категории и всех её потомков (CTE).
        """
        cte = (
            select(Activity.id)
            .where(Activity.id == activity_id)
            .cte("activity_cte", recursive=True)
        )

        cte = cte.union_all(
            select(Activity.id).join(cte, Activity.parent_id == cte.c.id)
        )

        stmt = select(cte)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_activity_by_id(self, activity_id: int) -> Activity | None:
        """
        Получить вид деятельности по ID
        """
        stmt = select(Activity).where(Activity.id == activity_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all_activities(self) -> list[Activity]:
        """
        Получить все виды деятельности
        """
        stmt = select(Activity)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
