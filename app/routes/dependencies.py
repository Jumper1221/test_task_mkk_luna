from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_session
from app.repositories.activity_repo import ActivityRepository
from app.repositories.building_repo import BuildingRepository
from app.repositories.organization_repo import OrganizationRepository
from app.services.activity_service import ActivityService
from app.services.building_service import BuildingService
from app.services.organization_service import OrganizationService


async def get_org_service(
    session: AsyncSession = Depends(get_async_session),
) -> OrganizationService:
    org_repo = OrganizationRepository(session)
    act_repo = ActivityRepository(session)
    return OrganizationService(org_repo, act_repo)


async def get_building_service(
    session: AsyncSession = Depends(get_async_session),
) -> BuildingService:
    building_repo = BuildingRepository(session)
    return BuildingService(building_repo)


async def get_activity_service(
    session: AsyncSession = Depends(get_async_session),
) -> ActivityService:
    activity_repo = ActivityRepository(session)
    return ActivityService(activity_repo)
