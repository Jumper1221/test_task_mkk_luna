import pytest

from app.core.config import settings


@pytest.mark.asyncio
async def test_get_building_by_id(client):
    """Тест получения здания по ID"""
    response = await client.get(
        "/buildings/1",
        headers={settings.API_KEY_HEADER_NAME: settings.API_KEY},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "address" in data
    assert -90 <= data["latitude"] <= 90
    assert -180 <= data["longitude"] <= 180


@pytest.mark.asyncio
async def test_get_nonexistent_building(client):
    """Тест получения здания, которое не существует"""
    response = await client.get(
        "/buildings/999999",
        headers={settings.API_KEY_HEADER_NAME: settings.API_KEY},
    )

    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Здание не найдено"


@pytest.mark.asyncio
async def test_get_building_with_invalid_id(client):
    """Тест получения здания с недопустимым форматом ID"""
    response = await client.get(
        "/buildings/invalid_id",
        headers={settings.API_KEY_HEADER_NAME: settings.API_KEY},
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_building_negative_id(client):
    """Тест получения здания с отрицательным ID"""
    response = await client.get(
        "/buildings/-1",
        headers={settings.API_KEY_HEADER_NAME: settings.API_KEY},
    )
    assert response.status_code in [404, 422]
