import pytest

from app.core.config import settings


@pytest.mark.asyncio
async def test_get_all_buildings(client):
    """Проверка получения всех зданий"""
    response = await client.get(
        "/buildings",
        headers={settings.API_KEY_HEADER_NAME: settings.API_KEY},
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data

    first = data[0]
    assert {"id", "address", "latitude", "longitude"} <= set(first.keys())
    assert isinstance(first["latitude"], (int, float))
    assert isinstance(first["longitude"], (int, float))


@pytest.mark.asyncio
async def test_building_coordinates_validity(client):
    """Тест что координаты зданий находятся в допустимых диапазонах"""
    response = await client.get(
        "/buildings",
        headers={settings.API_KEY_HEADER_NAME: settings.API_KEY},
    )

    assert response.status_code == 200
    data = response.json()

    for building in data:
        assert -90 <= building["latitude"] <= 90
        assert -180 <= building["longitude"] <= 180


@pytest.mark.asyncio
async def test_building_address_not_empty(client):
    """Тест что адреса зданий не являются пустыми строками"""
    response = await client.get(
        "/buildings",
        headers={settings.API_KEY_HEADER_NAME: settings.API_KEY},
    )

    assert response.status_code == 200
    data = response.json()

    for building in data:
        assert "address" in building
        assert building["address"].strip() != ""


@pytest.mark.asyncio
async def test_building_unique_ids(client):
    """Тест что все ID зданий в ответе уникальны"""
    response = await client.get(
        "/buildings",
        headers={settings.API_KEY_HEADER_NAME: settings.API_KEY},
    )

    assert response.status_code == 200
    data = response.json()

    ids = [building["id"] for building in data]
    assert len(ids) == len(set(ids))
