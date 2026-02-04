import pytest

from app.core.config import settings


@pytest.mark.asyncio
async def test_get_all_activities(client):
    """Проверка получения всех видов деятельности"""
    response = await client.get(
        "/activities",
        headers={settings.API_KEY_HEADER_NAME: settings.API_KEY},
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data

    first = data[0]
    assert {"id", "name", "level", "parent_id"} <= set(first.keys())


@pytest.mark.asyncio
async def test_activity_name_not_empty(client):
    """Тест что названия деятельности не являются пустыми строками"""
    response = await client.get(
        "/activities",
        headers={settings.API_KEY_HEADER_NAME: settings.API_KEY},
    )

    assert response.status_code == 200
    data = response.json()

    for activity in data:
        assert "name" in activity
        assert activity["name"].strip() != ""


@pytest.mark.asyncio
async def test_activity_unique_ids(client):
    """Тест что все ID деятельности в ответе уникальны"""
    response = await client.get(
        "/activities",
        headers={settings.API_KEY_HEADER_NAME: settings.API_KEY},
    )

    assert response.status_code == 200
    data = response.json()

    ids = [activity["id"] for activity in data]
    assert len(ids) == len(set(ids)), "ID деятельности должны быть уникальными"


@pytest.mark.asyncio
async def test_activity_level_validity(client):
    """Тест что уровни деятельности являются неотрицательными целыми числами"""
    response = await client.get(
        "/activities",
        headers={settings.API_KEY_HEADER_NAME: settings.API_KEY},
    )

    assert response.status_code == 200
    data = response.json()

    for activity in data:
        assert isinstance(activity["level"], int)
        assert activity["level"] >= 0
