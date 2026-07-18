import uuid

import pytest


@pytest.mark.asyncio
async def test_create_exam_requires_admin(client):
    res = await client.post("/api/v1/exam", json={"title_fa": "امتحان تستی"})
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_exam_crud_flow(client, auth_headers):
    # Create
    res = await client.post("/api/v1/exam", json={
        "title_fa": "امتحان تستی pytest",
        "category": "kankor",
        "duration_minutes": 30,
        "total_questions": 2,
        "passing_score": 50.0,
    }, headers=auth_headers)
    assert res.status_code == 200
    exam = res.json()
    exam_id = exam["id"]
    assert exam["title_fa"] == "امتحان تستی pytest"

    # Add a question with options
    res = await client.post(f"/api/v1/exam/{exam_id}/questions", json={
        "question_fa": "۱+۱=?",
        "sort_order": 0,
        "points": 1,
        "subject": "ریاضی",
        "options": [
            {"id": str(uuid.uuid4()), "text_fa": "۲", "text_en": None, "is_correct": True},
            {"id": str(uuid.uuid4()), "text_fa": "۳", "text_en": None, "is_correct": False},
        ],
    }, headers=auth_headers)
    assert res.status_code == 200

    # Update
    res = await client.patch(f"/api/v1/exam/{exam_id}", json={
        "id": exam_id,
        "title_fa": "امتحان تستی pytest — ویرایش‌شده",
        "title_en": None,
        "category": "kankor",
        "year": None,
        "duration_minutes": 30,
        "total_questions": 2,
        "passing_score": 50.0,
    }, headers=auth_headers)
    assert res.status_code == 200
    assert res.json()["title_fa"] == "امتحان تستی pytest — ویرایش‌شده"

    # Delete (cleanup)
    res = await client.delete(f"/api/v1/exam/{exam_id}", headers=auth_headers)
    assert res.status_code == 200

    res = await client.get(f"/api/v1/exam/{exam_id}")
    assert res.status_code == 404


@pytest.mark.asyncio
async def test_delete_question_requires_admin(client):
    res = await client.delete(f"/api/v1/exam/questions/{uuid.uuid4()}")
    assert res.status_code == 401
