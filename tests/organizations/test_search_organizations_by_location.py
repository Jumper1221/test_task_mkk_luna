import pytest

from app.core.config import settings


@pytest.mark.asyncio
async def test_search_organizations_by_location(client):
    """Тест поиска организаций по местоположению с заданным радиусом"""
    response = await client.get(
        "/organizations/search/by-location",
        params={"lat": 55.7558, "lon": 37.6173, "radius": 5},
        headers={settings.API_KEY_HEADER_NAME: settings.API_KEY},
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data


@pytest.mark.asyncio
async def test_search_organizations_by_location_without_radius(client):
    """
    Тест поиска организаций по местоположению
    без указания радиуса (значение по умолчанию)
    """
    response = await client.get(
        "/organizations/search/by-location",
        params={"lat": 55.7558, "lon": 37.6176},
        headers={settings.API_KEY_HEADER_NAME: settings.API_KEY},
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_search_organizations_by_location_invalid_coordinates(client):
    """Тест поиска организаций с недопустимыми координатами"""
    response = await client.get(
        "/organizations/search/by-location",
        params={"lat": 100.0, "lon": 37.6176},  # 100 > 90
        headers={settings.API_KEY_HEADER_NAME: settings.API_KEY},
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_search_organizations_by_location_negative_radius(client):
    """Тест поиска организаций с отрицательным радиусом"""
    response = await client.get(
        "/organizations/search/by-location",
        params={"lat": 55.7558, "lon": 37.6176, "radius": -5.0},
        headers={settings.API_KEY_HEADER_NAME: settings.API_KEY},
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_search_organizations_by_location_boundary_coordinates(client):
    """Тест поиска организаций с граничными значениями координат"""
    response_max_lat = await client.get(
        "/organizations/search/by-location",
        params={"lat": 90.0, "lon": 0.0},
        headers={settings.API_KEY_HEADER_NAME: settings.API_KEY},
    )
    assert response_max_lat.status_code in [
        200,
        404,
    ]

    response_min_lat = await client.get(
        "/organizations/search/by-location",
        params={"lat": -90.0, "lon": 0.0},
        headers={settings.API_KEY_HEADER_NAME: settings.API_KEY},
    )
    assert response_min_lat.status_code in [200, 404]

    response_max_lon = await client.get(
        "/organizations/search/by-location",
        params={"lat": 0.0, "lon": 180.0},
        headers={settings.API_KEY_HEADER_NAME: settings.API_KEY},
    )
    assert response_max_lon.status_code in [200, 404]

    response_min_lon = await client.get(
        "/organizations/search/by-location",
        params={"lat": 0.0, "lon": -180.0},
        headers={settings.API_KEY_HEADER_NAME: settings.API_KEY},
    )
    assert response_min_lon.status_code in [200, 404]
