from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class PhoneResponse(BaseModel):
    """
    Модель ответа для телефонного номера организации
    """

    number: str = Field(description="Телефонный номер организации")

    model_config = ConfigDict(from_attributes=True)


class BuildingResponse(BaseModel):
    """
    Модель ответа для информации о здании
    """

    id: int = Field(description="Уникальный идентификатор здания")
    address: str = Field(description="Адрес здания")
    latitude: float = Field(description="Широта координаты здания")
    longitude: float = Field(description="Долгота координаты здания")

    model_config = ConfigDict(from_attributes=True)


class ActivityResponse(BaseModel):
    """
    Модель ответа для информации о виде деятельности
    """

    id: int = Field(description="Уникальный идентификатор вида деятельности")
    name: str = Field(description="Название вида деятельности")
    parent_id: Optional[int] = Field(
        default=None, description="Идентификатор родительской категории (если есть)"
    )
    level: int = Field(description="Уровень вложенности категории")

    model_config = ConfigDict(from_attributes=True)


class OrganizationResponse(BaseModel):
    """
    Модель ответа для информации об организации
    """

    id: int = Field(description="Уникальный идентификатор организации")
    name: str = Field(description="Название организации")
    building: BuildingResponse = Field(
        description="Информация о здании, где находится организация"
    )
    phones: List[PhoneResponse] = Field(
        description="Список телефонных номеров организации"
    )
    activities: List[ActivityResponse] = Field(
        description="Список видов деятельности организации"
    )

    model_config = ConfigDict(from_attributes=True)
