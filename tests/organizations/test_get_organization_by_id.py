import pytest

from app.core.config import settings


@pytest.mark.asyncio
async def test_get_organization_by_id(client):
    """Тест получения организации по ID"""
    response = await client.get(
        "/organizations/1",
        headers={settings.API_KEY_HEADER_NAME: settings.API_KEY},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "name" in data
    assert "building" in data
    assert {"id", "address", "latitude", "longitude"} <= set(data["building"].keys())
    assert isinstance(data.get("phones", []), list)
    assert isinstance(data.get("activities", []), list)


@pytest.mark.asyncio
async def test_get_nonexistent_organization(client):
    """Тест получения организации, которая не существует"""
    response = await client.get(
        "/organizations/999999",
        headers={settings.API_KEY_HEADER_NAME: settings.API_KEY},
    )

    assert response.status_code == 404
    data = response.json()
    assert "detail" in data


@pytest.mark.asyncio
async def test_get_organization_with_invalid_id(client):
    """Тест получения организации с недопустимым форматом ID"""
    response = await client.get(
        "/organizations/invalid_id",
        headers={settings.API_KEY_HEADER_NAME: settings.API_KEY},
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_organization_negative_id(client):
    """Тест получения организации с отрицательным ID"""
    response = await client.get(
        "/organizations/-1",
        headers={settings.API_KEY_HEADER_NAME: settings.API_KEY},
    )
    assert response.status_code in [404, 422]


@pytest.mark.asyncio
async def test_organization_structure_validation(client):
    """Тест валидации структуры данных организации"""
    response = await client.get(
        "/organizations/1",
        headers={settings.API_KEY_HEADER_NAME: settings.API_KEY},
    )

    assert response.status_code == 200
    data = response.json()

    assert "id" in data
    assert "name" in data
    assert "building" in data
    assert "phones" in data
    assert "activities" in data

    assert isinstance(data["id"], int)
    assert isinstance(data["name"], str)
    assert isinstance(data["building"], dict)
    assert isinstance(data["phones"], list)
    assert isinstance(data["activities"], list)

    building = data["building"]
    assert "id" in building
    assert "address" in building
    assert "latitude" in building
    assert "longitude" in building
