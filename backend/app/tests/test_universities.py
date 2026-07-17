import pytest


@pytest.mark.asyncio
async def test_list_universities(client):
    res = await client.get("/api/v1/universities")
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 1


@pytest.mark.asyncio
async def test_get_university_found(client):
    res = await client.get("/api/v1/universities/herat-university")
    assert res.status_code == 200
    assert res.json()["slug"] == "herat-university"


@pytest.mark.asyncio
async def test_get_university_not_found(client):
    res = await client.get("/api/v1/universities/nonexistent")
    assert res.status_code == 404
