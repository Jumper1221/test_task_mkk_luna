from datetime import datetime

import pytest

from app.core.config import settings


@pytest.mark.asyncio
async def test_health_check(client):
    response = await client.get(
        "/",
        headers={settings.API_KEY_HEADER_NAME: settings.API_KEY},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    datetime.fromisoformat(data["timestamp"])
