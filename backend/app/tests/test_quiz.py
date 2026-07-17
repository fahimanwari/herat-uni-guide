import pytest


@pytest.mark.asyncio
async def test_list_questions(client):
    res = await client.get("/api/v1/quiz/questions")
    assert res.status_code == 200
    data = res.json()
    assert len(data) > 0
    assert all("options" in q for q in data)


@pytest.mark.asyncio
async def test_question_has_options(client):
    res = await client.get("/api/v1/quiz/questions")
    data = res.json()
    for q in data:
        assert len(q["options"]) >= 2


@pytest.mark.asyncio
async def test_score_quiz(client):
    questions = (await client.get("/api/v1/quiz/questions")).json()
    option_ids = [q["options"][0]["id"] for q in questions]
    res = await client.post("/api/v1/quiz/score", json={"selected_option_ids": option_ids})
    assert res.status_code == 200
    assert len(res.json()) > 0
