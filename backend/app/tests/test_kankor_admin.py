import pytest


@pytest.mark.asyncio
async def test_create_cutoff_requires_admin(client):
    depts = (await client.get("/api/v1/departments")).json()
    dept_id = depts[0]["id"]
    res = await client.post(f"/api/v1/kankor/cutoffs?department_id={dept_id}", json={
        "year": 1404, "min_score": 200, "capacity": 50,
    })
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_cutoff_crud_flow(client, auth_headers):
    depts = (await client.get("/api/v1/departments")).json()
    dept_id = depts[0]["id"]

    res = await client.post(f"/api/v1/kankor/cutoffs?department_id={dept_id}", json={
        "year": 1404, "min_score": 210.5, "capacity": 40,
    }, headers=auth_headers)
    assert res.status_code == 200
    cutoff = res.json()
    cutoff_id = cutoff["id"]

    res = await client.patch(f"/api/v1/kankor/cutoffs/{cutoff_id}", json={
        "year": 1404, "min_score": 220.0, "capacity": 45,
    }, headers=auth_headers)
    assert res.status_code == 200
    assert res.json()["min_score"] == 220.0

    res = await client.delete(f"/api/v1/kankor/cutoffs/{cutoff_id}", headers=auth_headers)
    assert res.status_code == 200


@pytest.mark.asyncio
async def test_create_guide_requires_admin(client):
    res = await client.post("/api/v1/kankor/guides", json={
        "title_fa": "راهنمای تستی", "body_fa": "متن راهنما",
    })
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_guide_crud_flow(client, auth_headers):
    res = await client.post("/api/v1/kankor/guides", json={
        "title_fa": "راهنمای تستی pytest", "body_fa": "متن راهنما", "category": "عمومی",
    }, headers=auth_headers)
    assert res.status_code == 201
    guide = res.json()
    guide_id = guide["id"]

    res = await client.get("/api/v1/kankor/guides")
    assert res.status_code == 200
    assert any(g["id"] == guide_id for g in res.json())

    res = await client.patch(f"/api/v1/kankor/guides/{guide_id}", json={
        "title_fa": "راهنمای تستی pytest — ویرایش‌شده",
    }, headers=auth_headers)
    assert res.status_code == 200
    assert res.json()["title_fa"] == "راهنمای تستی pytest — ویرایش‌شده"

    res = await client.delete(f"/api/v1/kankor/guides/{guide_id}", headers=auth_headers)
    assert res.status_code == 200
