import uuid

import pytest


async def _first_dept_slug(client) -> str:
    depts = (await client.get("/api/v1/departments")).json()
    return depts[0]["slug"]


@pytest.mark.asyncio
async def test_add_video_requires_admin(client):
    slug = await _first_dept_slug(client)
    res = await client.post(f"/api/v1/departments/{slug}/videos", json={
        "title_fa": "درس تستی", "video_url": "https://youtube.com/watch?v=x",
    })
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_video_crud_flow(client, auth_headers):
    slug = await _first_dept_slug(client)

    res = await client.post(f"/api/v1/departments/{slug}/videos", json={
        "title_fa": "درس تستی pytest",
        "video_url": "https://youtube.com/watch?v=abc123",
        "subject": "ریاضی",
        "semester": 1,
        "lecturer_name": "پوهنیار تست",
    }, headers=auth_headers)
    assert res.status_code == 201
    video_id = res.json()["id"]

    # Video appears in the public department detail
    dept = (await client.get(f"/api/v1/departments/{slug}")).json()
    assert any(v["id"] == video_id for v in dept.get("lecture_videos", []))

    # Delete (cleanup) — this exercises the fixed delete_video path
    res = await client.delete(f"/api/v1/departments/{slug}/videos/{video_id}", headers=auth_headers)
    assert res.status_code == 200

    dept = (await client.get(f"/api/v1/departments/{slug}")).json()
    assert not any(v["id"] == video_id for v in dept.get("lecture_videos", []))


@pytest.mark.asyncio
async def test_delete_missing_video_404(client, auth_headers):
    slug = await _first_dept_slug(client)
    res = await client.delete(f"/api/v1/departments/{slug}/videos/{uuid.uuid4()}", headers=auth_headers)
    assert res.status_code == 404
