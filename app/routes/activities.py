from typing import List

from fastapi import APIRouter, Depends, Path

from app.routes.dependencies import get_activity_service
from app.schemas.responses import ActivityResponse
from app.services.activity_service import ActivityService

router = APIRouter(
    prefix="/activities",
    tags=["Деятельности"],
)


@router.get(
    "/{activity_id}",
    response_model=ActivityResponse,
    summary="Получить информацию о виде деятельности по ID",
    description=(
        "Возвращает информацию о конкретном виде деятельности по его идентификатору"
    ),
)
async def get_activity_by_id(
    activity_id: int = Path(..., description="ID вида деятельности"),
    service: ActivityService = Depends(get_activity_service),
) -> ActivityResponse:
    """Получить информацию о виде деятельности по ID"""
    activity = await service.get_by_id(activity_id)
    return ActivityResponse.model_validate(activity)


@router.get(
    "",
    response_model=List[ActivityResponse],
    summary="Получить все виды деятельности",
    description="Возвращает список всех доступных видов деятельности",
)
async def get_all_activities(
    service: ActivityService = Depends(get_activity_service),
) -> List[ActivityResponse]:
    """Получить все виды деятельности"""
    activities = await service.get_all()
    return [ActivityResponse.model_validate(activity) for activity in activities]
