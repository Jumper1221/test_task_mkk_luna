from typing import List

from app.models.activities import Activity
from app.repositories.activity_repo import ActivityRepository


class ActivityService:
    def __init__(self, activity_repo: ActivityRepository):
        self.activity_repo: ActivityRepository = activity_repo

    async def get_by_id(self, activity_id: int) -> Activity:
        """
        Получить вид деятельности по ID
        """
        activity = await self.activity_repo.get_activity_by_id(activity_id)
        if not activity:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Activity not found")
        return activity

    async def get_all(self) -> List[Activity]:
        """
        Получить все виды деятельности
        """
        return await self.activity_repo.get_all_activities()