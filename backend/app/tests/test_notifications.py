import pytest


@pytest.mark.asyncio
async def test_list_events(client):
    res = await client.get("/api/v1/notifications/events")
    assert res.status_code == 200
    data = res.json()
    assert len(data) > 0
    assert all("title_fa" in e for e in data)
