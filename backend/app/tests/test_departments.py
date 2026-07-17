import pytest


@pytest.mark.asyncio
async def test_list_departments_empty(client):
    res = await client.get("/api/v1/departments")
    assert res.status_code == 200
    assert res.json() == []


@pytest.mark.asyncio
async def test_create_and_get_department(client):
    # Create university and faculty first
    uni = await client.post("/api/v1/universities", json={
        "slug": "test-uni",
        "name_fa": "test",
        "description_fa": "test",
    })
    fac = await client.post("/api/v1/faculties", json={
        "university_id": uni.json()["id"],
        "slug": "test-fac",
        "name_fa": "test fac",
        "description_fa": "test",
    })
    # Create department
    dept = await client.post("/api/v1/departments", json={
        "faculty_id": fac.json()["id"],
        "slug": "test-dept",
        "name_fa": "رشته آزمایشی",
        "description_fa": "توضیحات",
    })
    assert dept.status_code == 201
    assert dept.json()["slug"] == "test-dept"


@pytest.mark.asyncio
async def test_get_department_not_found(client):
    res = await client.get("/api/v1/departments/nonexistent")
    assert res.status_code == 404
