from pydantic import BaseModel, Field


class GeoSearchParams(BaseModel):
    """
    Параметры для географического поиска организаций
    """

    lat: float = Field(
        ..., ge=-90, le=90, description="Широта в градусах (от -90 до 90)"
    )
    lon: float = Field(
        ..., ge=-180, le=180, description="Долгота в градусах (от -180 до 180)"
    )
    radius_km: float = Field(
        ..., gt=0, le=1000, description="Радиус поиска в километрах"
    )


class NameSearchParams(BaseModel):
    """
    Параметры для поиска по названию организации
    """

    q: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Часть названия организации (минимум 3 символа)",
    )


class BuildingParams(BaseModel):
    """
    Параметры для поиска по ID здания
    """

    building_id: int = Field(..., gt=0, description="ID здания")


class ActivityParams(BaseModel):
    """
    Параметры для поиска по ID вида деятельности
    """

    activity_id: int = Field(..., gt=0, description="ID вида деятельности")
