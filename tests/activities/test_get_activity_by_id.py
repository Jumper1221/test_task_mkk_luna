import pytest

from app.core.config import settings


@pytest.mark.asyncio
async def test_get_activity_by_id(client):
    response = await client.get(
        "/activities/1",
        headers={settings.API_KEY_HEADER_NAME: settings.API_KEY},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "name" in data
    assert isinstance(data["level"], int)


@pytest.mark.asyncio
async def test_get_nonexistent_activity(client):
    """Тест получения деятельности, которая не существует"""
    response = await client.get(
        "/activities/999999",
        headers={settings.API_KEY_HEADER_NAME: settings.API_KEY},
    )

    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Activity not found"


@pytest.mark.asyncio
async def test_get_activity_with_invalid_id(client):
    """Тест получения деятельности с недопустимым форматом ID"""
    response = await client.get(
        "/activities/invalid_id",
        headers={settings.API_KEY_HEADER_NAME: settings.API_KEY},
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_activity_negative_id(client):
    """Тест получения деятельности с отрицательным ID"""
    response = await client.get(
        "/activities/-1",
        headers={settings.API_KEY_HEADER_NAME: settings.API_KEY},
    )
    assert response.status_code in [404, 422]
