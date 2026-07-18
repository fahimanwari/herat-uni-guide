import uuid

import pytest


@pytest.mark.asyncio
async def test_list_users_requires_admin(client):
    res = await client.get("/api/v1/users/admin/list")
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_list_and_toggle_user(client, auth_headers):
    email = f"pytest-{uuid.uuid4().hex[:8]}@example.com"
    res = await client.post("/api/v1/users/register", json={
        "email": email,
        "password": "testpass123",
        "full_name": "کاربر تستی",
    })
    assert res.status_code == 200
    user_id = res.json()["user"]["id"]

    res = await client.get("/api/v1/users/admin/list", headers=auth_headers)
    assert res.status_code == 200
    assert any(u["id"] == user_id for u in res.json())

    res = await client.patch(f"/api/v1/users/admin/{user_id}", json={"is_active": False}, headers=auth_headers)
    assert res.status_code == 200
    assert res.json()["is_active"] is False


@pytest.mark.asyncio
async def test_toggle_nonexistent_user_requires_admin(client):
    res = await client.patch(f"/api/v1/users/admin/{uuid.uuid4()}", json={"is_active": False})
    assert res.status_code == 401
