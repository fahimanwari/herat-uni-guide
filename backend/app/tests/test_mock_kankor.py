import uuid

import pytest


async def _create_verified_question(client, auth_headers, subject, question_fa, correct_text="درست"):
    res = await client.post("/api/v1/question-bank/questions", json={
        "subject": subject,
        "difficulty": "easy",
        "question_fa": question_fa,
        "options": [{"text": correct_text, "is_correct": True}, {"text": "نادرست"}],
        "is_verified": True,
    }, headers=auth_headers)
    assert res.status_code == 200
    return res.json()["id"]


@pytest.mark.asyncio
async def test_start_exam_no_questions_available(client):
    res = await client.post("/api/v1/mock-kankor/start", json={
        "session_id": f"pytest-{uuid.uuid4().hex[:8]}",
        "subject": f"موضوع-ناموجود-{uuid.uuid4().hex[:8]}",
        "num_questions": 5,
    })
    assert res.status_code == 404


@pytest.mark.asyncio
async def test_mock_exam_full_flow(client, auth_headers):
    subject = f"مضمون-تست-{uuid.uuid4().hex[:8]}"
    qid = await _create_verified_question(client, auth_headers, subject, "پرسش تستی")
    session_id = f"pytest-{uuid.uuid4().hex[:8]}"

    # Start
    res = await client.post("/api/v1/mock-kankor/start", json={
        "session_id": session_id,
        "subject": subject,
        "num_questions": 1,
    })
    assert res.status_code == 200
    data = res.json()
    assert data["total_questions"] == 1
    question = data["questions"][0]
    correct_option = next(o for o in question["options"] if o["text"] == "درست")

    # Submit — answer correctly
    res = await client.post(f"/api/v1/mock-kankor/{session_id}/submit", json={
        "answers": {question["id"]: correct_option["id"]},
    })
    assert res.status_code == 200
    result = res.json()
    assert result["score"] == 100.0
    assert result["correct_answers"] == 1

    # Review
    res = await client.get(f"/api/v1/mock-kankor/{session_id}/review")
    assert res.status_code == 200
    assert res.json()["questions"][0]["is_correct"] is True

    # History
    res = await client.get(f"/api/v1/mock-kankor/history?session_id={session_id}")
    assert res.status_code == 200
    assert len(res.json()) >= 1

    # Cleanup
    await client.delete(f"/api/v1/question-bank/questions/{qid}", headers=auth_headers)


@pytest.mark.asyncio
async def test_create_blueprint_requires_admin(client):
    res = await client.post("/api/v1/mock-kankor/blueprints", json={
        "name_fa": "تست",
        "sections": [{"subject": "ریاضی", "count": 5}],
    })
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_blueprint_drives_section_based_selection(client, auth_headers):
    subject_a = f"الف-{uuid.uuid4().hex[:6]}"
    subject_b = f"ب-{uuid.uuid4().hex[:6]}"
    qid_a = await _create_verified_question(client, auth_headers, subject_a, "سوال الف")
    qid_b = await _create_verified_question(client, auth_headers, subject_b, "سوال ب")

    res = await client.post("/api/v1/mock-kankor/blueprints", json={
        "name_fa": "الگوی تستی",
        "total_minutes": 20,
        "sections": [{"subject": subject_a, "count": 1}, {"subject": subject_b, "count": 1}],
    }, headers=auth_headers)
    assert res.status_code == 201
    blueprint = res.json()

    session_id = f"pytest-bp-{uuid.uuid4().hex[:8]}"
    res = await client.post("/api/v1/mock-kankor/start", json={
        "session_id": session_id,
        "blueprint_id": blueprint["id"],
    })
    assert res.status_code == 200
    data = res.json()
    assert data["total_questions"] == 2
    subjects = {q["subject"] for q in data["questions"]}
    assert subjects == {subject_a, subject_b}
    assert data["total_minutes"] == 20

    # Cleanup
    await client.delete(f"/api/v1/mock-kankor/blueprints/{blueprint['id']}", headers=auth_headers)
    await client.delete(f"/api/v1/question-bank/questions/{qid_a}", headers=auth_headers)
    await client.delete(f"/api/v1/question-bank/questions/{qid_b}", headers=auth_headers)
