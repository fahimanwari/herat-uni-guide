import pytest


@pytest.mark.asyncio
async def test_list_faculties(client):
    res = await client.get("/api/v1/faculties")
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 16


@pytest.mark.asyncio
async def test_get_faculty_found(client):
    res = await client.get("/api/v1/faculties/computer-science")
    assert res.status_code == 200
    assert res.json()["slug"] == "computer-science"


@pytest.mark.asyncio
async def test_get_faculty_not_found(client):
    res = await client.get("/api/v1/faculties/nonexistent")
    assert res.status_code == 404
