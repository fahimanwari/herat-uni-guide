import pytest


@pytest.mark.asyncio
async def test_health(client):
    res = await client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_universities(client):
    res = await client.get("/api/v1/universities")
    assert res.status_code == 200
    assert len(res.json()) >= 1


@pytest.mark.asyncio
async def test_university_detail(client):
    res = await client.get("/api/v1/universities/herat-university")
    assert res.status_code == 200
    assert res.json()["slug"] == "herat-university"


@pytest.mark.asyncio
async def test_university_not_found(client):
    res = await client.get("/api/v1/universities/nonexistent")
    assert res.status_code == 404


@pytest.mark.asyncio
async def test_faculties(client):
    res = await client.get("/api/v1/faculties")
    assert res.status_code == 200
    assert len(res.json()) >= 16


@pytest.mark.asyncio
async def test_faculty_detail(client):
    res = await client.get("/api/v1/faculties/computer-science")
    assert res.status_code == 200
    assert res.json()["slug"] == "computer-science"


@pytest.mark.asyncio
async def test_faculty_not_found(client):
    res = await client.get("/api/v1/faculties/nonexistent")
    assert res.status_code == 404


@pytest.mark.asyncio
async def test_departments(client):
    res = await client.get("/api/v1/departments")
    assert res.status_code == 200
    assert len(res.json()) >= 4


@pytest.mark.asyncio
async def test_department_detail(client):
    res = await client.get("/api/v1/departments/software-engineering")
    assert res.status_code == 200
    assert res.json()["slug"] == "software-engineering"


@pytest.mark.asyncio
async def test_department_not_found(client):
    res = await client.get("/api/v1/departments/nonexistent")
    assert res.status_code == 404


@pytest.mark.asyncio
async def test_news(client):
    res = await client.get("/api/v1/news")
    assert res.status_code == 200
    assert len(res.json()) >= 1


@pytest.mark.asyncio
async def test_faqs(client):
    res = await client.get("/api/v1/faqs")
    assert res.status_code == 200
    assert len(res.json()) >= 1


@pytest.mark.asyncio
async def test_kankor_chances(client):
    res = await client.get("/api/v1/kankor/chances?score=250")
    assert res.status_code == 200
    data = res.json()
    assert len(data) > 0
    assert all(r["chance"] in ("high", "medium", "low") for r in data)


@pytest.mark.asyncio
async def test_kankor_chances_sorted(client):
    res = await client.get("/api/v1/kankor/chances?score=250")
    data = res.json()
    order = {"high": 0, "medium": 1, "low": 2}
    chances = [order[r["chance"]] for r in data]
    assert chances == sorted(chances)


@pytest.mark.asyncio
async def test_quiz_questions(client):
    res = await client.get("/api/v1/quiz/questions")
    assert res.status_code == 200
    data = res.json()
    assert len(data) > 0
    assert all("options" in q for q in data)


@pytest.mark.asyncio
async def test_notifications(client):
    res = await client.get("/api/v1/notifications/events")
    assert res.status_code == 200
    assert len(res.json()) > 0


@pytest.mark.asyncio
async def test_swagger(client):
    res = await client.get("/docs")
    assert res.status_code == 200
