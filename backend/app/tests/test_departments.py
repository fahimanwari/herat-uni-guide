import pytest


@pytest.mark.asyncio
async def test_list_departments(client):
    res = await client.get("/api/v1/departments")
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 4


@pytest.mark.asyncio
async def test_get_department_found(client):
    res = await client.get("/api/v1/departments/software-engineering")
    assert res.status_code == 200
    assert res.json()["slug"] == "software-engineering"


@pytest.mark.asyncio
async def test_get_department_not_found(client):
    res = await client.get("/api/v1/departments/nonexistent")
    assert res.status_code == 404
