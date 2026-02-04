import pytest

from app.core.config import settings


@pytest.mark.asyncio
async def test_get_organizations_by_activity(client):
    """Проверка получения организаций по ID деятельности"""
    response = await client.get(
        "/organizations/activity/2",
        headers={settings.API_KEY_HEADER_NAME: settings.API_KEY},
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data

    first = data[0]
    assert {"id", "name", "activities"} <= set(first.keys())


@pytest.mark.asyncio
async def test_get_organizations_by_nonexistent_activity(client):
    """Тест получения организаций для несуществующей деятельности"""
    response = await client.get(
        "/organizations/activity/999999",
        headers={settings.API_KEY_HEADER_NAME: settings.API_KEY},
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_get_organizations_by_activity_with_invalid_id(client):
    """Тест получения организаций с недопустимым форматом ID деятельности"""
    response = await client.get(
        "/organizations/activity/invalid_id",
        headers={settings.API_KEY_HEADER_NAME: settings.API_KEY},
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_organizations_by_activity_negative_id(client):
    """Тест получения организаций с отрицательным ID деятельности"""
    response = await client.get(
        "/organizations/activity/-1",
        headers={settings.API_KEY_HEADER_NAME: settings.API_KEY},
    )

    assert response.status_code in [404, 422, 200]


@pytest.mark.asyncio
async def test_get_organizations_by_activity_response_structure(client):
    """Тест структуры ответа при получении организаций по ID деятельности"""
    response = await client.get(
        "/organizations/activity/1",
        headers={settings.API_KEY_HEADER_NAME: settings.API_KEY},
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

    for org in data:
        assert "id" in org
        assert "name" in org
        assert "building" in org
        assert "phones" in org
        assert "activities" in org

        assert isinstance(org["id"], int)
        assert isinstance(org["name"], str)
        assert isinstance(org["building"], dict)
        assert isinstance(org["phones"], list)
        assert isinstance(org["activities"], list)
