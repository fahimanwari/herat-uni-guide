import uuid

import pytest


@pytest.mark.asyncio
async def test_create_question_requires_admin(client):
    res = await client.post("/api/v1/question-bank/questions", json={
        "subject": "ریاضی",
        "question_fa": "تست",
        "options": [{"text": "الف", "is_correct": True}, {"text": "ب"}],
    })
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_question_crud_flow(client, auth_headers):
    # Create
    res = await client.post("/api/v1/question-bank/questions", json={
        "subject": "ریاضی-تست",
        "difficulty": "easy",
        "question_fa": "۱+۱=?",
        "options": [{"text": "۲", "is_correct": True}, {"text": "۳"}],
        "is_verified": True,
        "year": 1404,
    }, headers=auth_headers)
    assert res.status_code == 200
    question = res.json()
    qid = question["id"]
    assert question["is_verified"] is True

    # Update
    res = await client.patch(f"/api/v1/question-bank/questions/{qid}", json={
        "id": qid,
        "subject": "ریاضی-تست",
        "difficulty": "medium",
        "question_fa": "۱+۱=? (ویرایش‌شده)",
        "options": [{"text": "۲", "is_correct": True}, {"text": "۳"}],
    }, headers=auth_headers)
    assert res.status_code == 200
    assert res.json()["difficulty"] == "medium"

    # Delete (cleanup)
    res = await client.delete(f"/api/v1/question-bank/questions/{qid}", headers=auth_headers)
    assert res.status_code == 200


@pytest.mark.asyncio
async def test_create_question_rejects_missing_correct_answer(client, auth_headers):
    res = await client.post("/api/v1/question-bank/questions", json={
        "subject": "ریاضی-تست",
        "question_fa": "سوال بی‌جواب",
        "options": [{"text": "الف"}, {"text": "ب"}],
    }, headers=auth_headers)
    assert res.status_code == 422


@pytest.mark.asyncio
async def test_import_requires_admin(client):
    res = await client.post("/api/v1/question-bank/import", json=[
        {"subject": "ریاضی", "question_fa": "تست", "options": [{"text": "الف", "is_correct": True}, {"text": "ب"}]},
    ])
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_import_is_all_or_nothing(client, auth_headers):
    subject = f"وارداتی-{uuid.uuid4().hex[:8]}"

    # One valid row, one invalid (no correct answer marked) — nothing should be saved.
    res = await client.post("/api/v1/question-bank/import", json=[
        {"subject": subject, "question_fa": "معتبر", "options": [{"text": "الف", "is_correct": True}, {"text": "ب"}]},
        {"subject": subject, "question_fa": "نامعتبر", "options": [{"text": "الف"}, {"text": "ب"}]},
    ], headers=auth_headers)
    assert res.status_code == 200
    body = res.json()
    assert body["imported"] == 0
    assert len(body["errors"]) == 1
    assert body["errors"][0]["row"] == 2

    listed = await client.get(f"/api/v1/question-bank/questions?subject={subject}", headers=auth_headers)
    assert listed.json() == []

    # Fully valid batch — both rows should be saved atomically.
    res = await client.post("/api/v1/question-bank/import", json=[
        {"subject": subject, "question_fa": "معتبر یک", "options": [{"text": "الف", "is_correct": True}, {"text": "ب"}]},
        {"subject": subject, "question_fa": "معتبر دو", "options": [{"text": "الف", "is_correct": True}, {"text": "ب"}]},
    ], headers=auth_headers)
    assert res.status_code == 200
    body = res.json()
    assert body["imported"] == 2
    assert body["errors"] == []

    # Cleanup
    listed = await client.get(f"/api/v1/question-bank/questions?subject={subject}", headers=auth_headers)
    for q in listed.json():
        await client.delete(f"/api/v1/question-bank/questions/{q['id']}", headers=auth_headers)
