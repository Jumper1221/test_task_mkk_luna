from typing import List

from fastapi import APIRouter, Depends, Path

from app.routes.dependencies import get_building_service
from app.schemas.responses import BuildingResponse
from app.services.building_service import BuildingService

router = APIRouter(prefix="/buildings", tags=["Здания"])


@router.get(
    "/{building_id}",
    response_model=BuildingResponse,
    summary="Получить информацию о здании по ID",
    description="Возвращает информацию о конкретном здании по его идентификатору",
)
async def get_building_by_id(
    building_id: int = Path(..., description="ID здания"),
    service: BuildingService = Depends(get_building_service),
) -> BuildingResponse:
    """Получить информацию о здании по ID"""
    building = await service.get_by_id(building_id)
    return BuildingResponse.model_validate(building)


@router.get(
    "",
    response_model=List[BuildingResponse],
    summary="Получить все здания",
    description="Возвращает список всех доступных зданий",
)
async def get_all_buildings(
    service: BuildingService = Depends(get_building_service),
) -> List[BuildingResponse]:
    """Получить все здания"""
    buildings = await service.get_all()
    return [BuildingResponse.model_validate(building) for building in buildings]
