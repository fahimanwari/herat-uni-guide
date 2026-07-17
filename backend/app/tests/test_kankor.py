import pytest


@pytest.mark.asyncio
async def test_chances(client):
    res = await client.get("/api/v1/kankor/chances?score=250")
    assert res.status_code == 200
    data = res.json()
    assert len(data) > 0
    assert all(r["chance"] in ("high", "medium", "low") for r in data)


@pytest.mark.asyncio
async def test_chances_sorted(client):
    res = await client.get("/api/v1/kankor/chances?score=250")
    data = res.json()
    order = {"high": 0, "medium": 1, "low": 2}
    chances = [order[r["chance"]] for r in data]
    assert chances == sorted(chances)


@pytest.mark.asyncio
async def test_chances_high_score(client):
    res = await client.get("/api/v1/kankor/chances?score=300")
    data = res.json()
    assert any(r["chance"] == "high" for r in data)


@pytest.mark.asyncio
async def test_chances_low_score(client):
    res = await client.get("/api/v1/kankor/chances?score=100")
    data = res.json()
    assert any(r["chance"] == "low" for r in data)
