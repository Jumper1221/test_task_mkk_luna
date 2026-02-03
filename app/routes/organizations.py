from typing import List, Optional

from fastapi import APIRouter, Depends, Path, Query

from app.routes.dependencies import get_org_service
from app.schemas.responses import OrganizationResponse
from app.services.organization_service import OrganizationService

router = APIRouter(prefix="/organizations", tags=["Организации"])


@router.get(
    "/{org_id}",
    response_model=OrganizationResponse,
    summary="Получить информацию об организации по ID",
    description=(
        "Возвращает полную информацию об организации по её уникальному идентификатору"
    ),
)
async def get_organization_by_id(
    org_id: int = Path(..., description="ID организации"),
    service: OrganizationService = Depends(get_org_service),
) -> OrganizationResponse:
    """Вывод информации об организации по её идентификатору"""
    organization = await service.get_by_id(org_id)
    return OrganizationResponse.model_validate(organization)


@router.get(
    "/building/{building_id}",
    response_model=List[OrganizationResponse],
    summary="Получить организации по ID здания",
    description="Возвращает список всех организаций, находящихся в конкретном здании",
)
async def get_organizations_by_building(
    building_id: int = Path(..., description="ID здания"),
    service: OrganizationService = Depends(get_org_service),
) -> List[OrganizationResponse]:
    """Список всех организаций, находящихся в конкретном здании"""
    organizations = await service.search_by_building_id(building_id)
    return [OrganizationResponse.model_validate(org) for org in organizations]


@router.get(
    "/activity/{activity_id}",
    response_model=List[OrganizationResponse],
    summary="Получить организации по виду деятельности",
    description=(
        "Возвращает список всех организаций,"
        " которые относятся к указанному виду деятельности или его подкатегориям"
    ),
)
async def get_organizations_by_activity(
    activity_id: int = Path(..., description="ID вида деятельности"),
    service: OrganizationService = Depends(get_org_service),
) -> List[OrganizationResponse]:
    """Список всех организаций, которые относятся к указанному виду деятельности"""
    organizations = await service.search_by_activity(activity_id)
    return [OrganizationResponse.model_validate(org) for org in organizations]


@router.get(
    "/search/by-name",
    response_model=List[OrganizationResponse],
    summary="Поиск организаций по названию",
    description="Поиск организаций по частичному совпадению с названием",
)
async def search_organizations_by_name(
    q: str = Query(..., description="Часть названия организации для поиска"),
    service: OrganizationService = Depends(get_org_service),
) -> List[OrganizationResponse]:
    """Поиск организации по названию"""
    organizations = await service.search_by_name(q)
    return [OrganizationResponse.model_validate(org) for org in organizations]


@router.get(
    "/search/by-location",
    response_model=List[OrganizationResponse],
    summary="Поиск организаций по географическому расположению",
    description="Поиск организаций в заданном радиусе от указанных координат",
)
async def search_organizations_by_location(
    lat: float = Query(..., description="Широта в градусах (от -90 до 90)"),
    lon: float = Query(..., description="Долгота в градусах (от -180 до 180)"),
    radius: Optional[float] = Query(
        5.0, description="Радиус поиска в километрах (по умолчанию 5 км)"
    ),
    service: OrganizationService = Depends(get_org_service),
) -> List[OrganizationResponse]:
    """Список организаций, которые находятся в заданном радиусе области"""
    radius = radius or 5.0
    organizations = await service.search_by_location(lat, lon, radius)
    return [OrganizationResponse.model_validate(org) for org in organizations]
