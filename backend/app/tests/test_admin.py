import pytest


@pytest.mark.asyncio
async def test_admin_login_success(client):
    res = await client.post("/api/v1/admin/auth/login", json={
        "email": "admin@herat-uni.edu.af",
        "password": "admin123",
    })
    assert res.status_code == 200
    assert "access_token" in res.json()
    assert "refresh_token" in res.json()


@pytest.mark.asyncio
async def test_admin_login_wrong_password(client):
    res = await client.post("/api/v1/admin/auth/login", json={
        "email": "admin@herat-uni.edu.af",
        "password": "wrongpassword",
    })
    assert res.status_code == 404


@pytest.mark.asyncio
async def test_admin_login_nonexistent(client):
    res = await client.post("/api/v1/admin/auth/login", json={
        "email": "nonexistent@example.com",
        "password": "anything",
    })
    assert res.status_code == 404


@pytest.mark.asyncio
async def test_admin_refresh_token(client):
    login_res = await client.post("/api/v1/admin/auth/login", json={
        "email": "admin@herat-uni.edu.af",
        "password": "admin123",
    })
    refresh_token = login_res.json()["refresh_token"]
    res = await client.post("/api/v1/admin/auth/refresh", json={
        "refresh_token": refresh_token,
    })
    assert res.status_code == 200
    assert "access_token" in res.json()


@pytest.mark.asyncio
async def test_admin_refresh_invalid_token(client):
    res = await client.post("/api/v1/admin/auth/refresh", json={
        "refresh_token": "invalid-token",
    })
    assert res.status_code == 404
