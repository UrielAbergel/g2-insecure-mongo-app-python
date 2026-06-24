# tests/test_api.py

import pytest
import pytest_asyncio


@pytest_asyncio.fixture(scope="module", autouse=True)
async def setup_admin_and_users(client):
    token = await get_jwt(client, "admin", "admin")
    await register_user(client, token, "reader", "reader", "reader")
    await register_user(client, token, "writer", "writer", "writer")


async def get_jwt(client, username, password):
    r = await client.post(
        "/auth/token", json={"username": username, "password": password}
    )
    assert r.status_code == 200
    return r.json()["token"]


async def register_user(client, token, username, password, role=None):
    data = {"username": username, "password": password}
    if role:
        data["role"] = role
    return await client.post(
        "/auth/register", json=data, headers={"Authorization": f"Bearer {token}"}
    )


def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_get_items_without_id_returns_404(client):
    token = await get_jwt(client, "admin", "admin")
    r = await client.get("/items?id=", headers=auth_headers(token))
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_get_items_without_token_returns_401(client):
    r = await client.get("/items?id=someid")
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_get_items_with_reader_token_returns_404(client):
    token = await get_jwt(client, "reader", "reader")
    r = await client.get("/items?id=nonexistent", headers=auth_headers(token))
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_auth_token_with_valid_credentials_returns_token(client):
    r = await client.post(
        "/auth/token", json={"username": "admin", "password": "admin"}
    )
    assert r.status_code == 200
    assert "token" in r.json()


@pytest.mark.asyncio
async def test_auth_token_with_invalid_credentials_returns_unauthorized(client):
    r = await client.post(
        "/auth/token", json={"username": "admin", "password": "wrong"}
    )
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_register_new_user_as_admin_returns_ok(client):
    token = await get_jwt(client, "admin", "admin")
    r = await register_user(client, token, "testuser", "testpass")
    assert r.status_code in (200, 409)


@pytest.mark.asyncio
async def test_register_new_writer_user_as_admin_returns_ok(client):
    token = await get_jwt(client, "admin", "admin")
    r = await register_user(client, token, "writerX", "testpass", role="writer")
    assert r.status_code in (200, 409)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "username,password", [("reader", "reader"), ("writer", "writer")]
)
async def test_register_as_non_admin_returns_unauthorized(client, username, password):
    token = await get_jwt(client, username, password)
    r = await register_user(client, token, "unauthorizedUser", "test")
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_post_item_without_token_returns_401(client):
    r = await client.post("/items", json={"name": "insecure"})
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_post_item_with_writer_token_returns_201(client):
    token = await get_jwt(client, "writer", "writer")
    r = await client.post(
        "/items", json={"name": "test item"}, headers=auth_headers(token)
    )
    assert r.status_code == 201


@pytest.mark.asyncio
async def test_post_item_with_reader_token_returns_unauthorized(client):
    token = await get_jwt(client, "reader", "reader")
    r = await client.post(
        "/items", json={"name": "reader-should-not-post"}, headers=auth_headers(token)
    )
    assert r.status_code == 401
