import pytest


@pytest.mark.asyncio
async def test_list_faqs(client):
    res = await client.get("/api/v1/faqs")
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 1
