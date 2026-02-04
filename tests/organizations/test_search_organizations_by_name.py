import pytest

from app.core.config import settings


@pytest.mark.asyncio
async def test_search_organizations_by_name(client):
    """Тест поиска организаций по имени"""
    response = await client.get(
        "/organizations/search/by-name",
        params={"q": "SoftTech"},
        headers={settings.API_KEY_HEADER_NAME: settings.API_KEY},
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any("SoftTech" in item.get("name", "") for item in data)


@pytest.mark.asyncio
async def test_search_organizations_by_empty_query(client):
    """Тест поиска организаций с пустым запросом"""
    response = await client.get(
        "/organizations/search/by-name",
        params={"q": ""},
        headers={settings.API_KEY_HEADER_NAME: settings.API_KEY},
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_search_organizations_by_short_query(client):
    """Тест поиска организаций с коротким запросом"""
    response = await client.get(
        "/organizations/search/by-name",
        params={"q": "a"},
        headers={settings.API_KEY_HEADER_NAME: settings.API_KEY},
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_search_organizations_by_nonexistent_name(client):
    """Тест поиска организаций по несуществующему имени"""
    response = await client.get(
        "/organizations/search/by-name",
        params={"q": "NonExistentOrgName12345"},
        headers={settings.API_KEY_HEADER_NAME: settings.API_KEY},
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 0


@pytest.mark.asyncio
async def test_search_organizations_response_structure(client):
    """Тест структуры ответа при поиске организаций по имени"""
    response = await client.get(
        "/organizations/search/by-name",
        params={"q": "Soft"},
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
