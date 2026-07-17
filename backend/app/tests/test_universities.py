import pytest


@pytest.mark.asyncio
async def test_list_universities_empty(client):
    res = await client.get("/api/v1/universities")
    assert res.status_code == 200
    assert res.json() == []


@pytest.mark.asyncio
async def test_create_university(client):
    payload = {
        "slug": "test-uni",
        "name_fa": "پوهنتون آزمایشی",
        "description_fa": "توضیحات آزمایشی",
    }
    res = await client.post("/api/v1/universities", json=payload)
    assert res.status_code == 201
    data = res.json()
    assert data["slug"] == "test-uni"
    assert data["name_fa"] == "پوهنتون آزمایشی"


@pytest.mark.asyncio
async def test_get_university_found(client):
    # Create first
    await client.post("/api/v1/universities", json={
        "slug": "get-test",
        "name_fa": "test",
        "description_fa": "test desc",
    })
    res = await client.get("/api/v1/universities/get-test")
    assert res.status_code == 200
    assert res.json()["slug"] == "get-test"


@pytest.mark.asyncio
async def test_get_university_not_found(client):
    res = await client.get("/api/v1/universities/nonexistent")
    assert res.status_code == 404
