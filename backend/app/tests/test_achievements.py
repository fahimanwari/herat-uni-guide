import uuid

import pytest


@pytest.mark.asyncio
async def test_achievements_empty_for_new_session(client):
    res = await client.get(f"/api/v1/achievements?session_id=pytest-{uuid.uuid4().hex[:8]}")
    assert res.status_code == 200
    assert res.json() == []


@pytest.mark.asyncio
async def test_leaderboard_shape_and_anonymity(client):
    res = await client.get("/api/v1/achievements/leaderboard")
    assert res.status_code == 200
    rows = res.json()
    assert isinstance(rows, list)
    # هیچ session_id واقعی نباید به بیرون داده شود
    for row in rows:
        assert "session_id" not in row


@pytest.mark.asyncio
async def test_first_exam_awards_badge(client, auth_headers):
    subject = f"نشان-تست-{uuid.uuid4().hex[:6]}"
    q = await client.post("/api/v1/question-bank/questions", json={
        "subject": subject,
        "question_fa": "سوال نشان",
        "options": [{"text": "الف", "is_correct": True}, {"text": "ب"}],
        "is_verified": True,
    }, headers=auth_headers)
    qid = q.json()["id"]
    session_id = f"pytest-badge-{uuid.uuid4().hex[:8]}"

    start = await client.post("/api/v1/mock-kankor/start", json={
        "session_id": session_id, "subject": subject, "num_questions": 1,
    })
    assert start.status_code == 200
    question = start.json()["questions"][0]

    submit = await client.post(f"/api/v1/mock-kankor/{session_id}/submit", json={
        "answers": {question["id"]: question["options"][0]["id"]},
    })
    assert submit.status_code == 200
    assert "new_badges" in submit.json()

    earned = (await client.get(f"/api/v1/achievements?session_id={session_id}")).json()
    assert any(a["badge_key"] == "first_exam" for a in earned)

    # Cleanup
    await client.delete(f"/api/v1/question-bank/questions/{qid}", headers=auth_headers)
