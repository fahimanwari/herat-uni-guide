import pytest


@pytest.mark.asyncio
async def test_list_faqs_empty(client):
    res = await client.get("/api/v1/faqs")
    assert res.status_code == 200
    assert res.json() == []


@pytest.mark.asyncio
async def test_create_faq(client):
    payload = {
        "question_fa": "آزمایشی؟",
        "answer_fa": "جواب آزمایشی",
    }
    res = await client.post("/api/v1/faqs", json=payload)
    assert res.status_code == 201
    assert res.json()["question_fa"] == "آزمایشی؟"


@pytest.mark.asyncio
async def test_get_faq_not_found(client):
    import uuid
    fake_id = str(uuid.uuid4())
    res = await client.get(f"/api/v1/faqs/{fake_id}")
    assert res.status_code == 404
