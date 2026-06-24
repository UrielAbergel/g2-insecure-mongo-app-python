# tests/test_api.py

import os

import pytest
import pytest_asyncio

CRED_FIELD = "password"
TEST_ADMIN_USER = os.getenv("TEST_ADMIN_USER", "admin")
TEST_ADMIN_PASS = os.getenv("TEST_ADMIN_PASS", "admin")
TEST_READER_USER = os.getenv("TEST_READER_USER", "reader")
TEST_READER_PASS = os.getenv("TEST_READER_PASS", "reader")
TEST_WRITER_USER = os.getenv("TEST_WRITER_USER", "writer")
TEST_WRITER_PASS = os.getenv("TEST_WRITER_PASS", "writer")


@pytest_asyncio.fixture(scope="module", autouse=True)
async def setup_admin_and_users(client):
    token = await get_jwt(client, TEST_ADMIN_USER, TEST_ADMIN_PASS)
    await register_user(client, token, TEST_READER_USER, TEST_READER_PASS, "reader")
    await register_user(client, token, TEST_WRITER_USER, TEST_WRITER_PASS, "writer")


async def get_jwt(client, username, credential):
    r = await client.post(
        "/auth/token", json={"username": username, CRED_FIELD: credential}
    )
    assert r.status_code == 200
    return r.json()["token"]


async def register_user(client, token, username, credential, role=None):
    data = {"username": username, CRED_FIELD: credential}
    if role:
        data["role"] = role
    return await client.post(
        "/auth/register", json=data, headers={"Authorization": f"Bearer {token}"}
    )


def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_get_items_without_id_returns_404(client):
    token = await get_jwt(client, TEST_ADMIN_USER, TEST_ADMIN_PASS)
    r = await client.get("/items?id=", headers=auth_headers(token))
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_get_items_without_token_returns_401(client):
    r = await client.get("/items?id=someid")
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_get_items_with_reader_token_returns_404(client):
    token = await get_jwt(client, TEST_READER_USER, TEST_READER_PASS)
    r = await client.get("/items?id=nonexistent", headers=auth_headers(token))
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_auth_token_with_valid_credentials_returns_token(client):
    r = await client.post(
        "/auth/token", json={"username": TEST_ADMIN_USER, CRED_FIELD: TEST_ADMIN_PASS}
    )
    assert r.status_code == 200
    assert "token" in r.json()


@pytest.mark.asyncio
async def test_auth_token_with_invalid_credentials_returns_unauthorized(client):
    r = await client.post(
        "/auth/token",
        json={"username": TEST_ADMIN_USER, CRED_FIELD: "wrong-credential"},
    )
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_register_new_user_as_admin_returns_ok(client):
    token = await get_jwt(client, TEST_ADMIN_USER, TEST_ADMIN_PASS)
    r = await register_user(client, token, "testuser", "testpass-val")
    assert r.status_code in (200, 409)


@pytest.mark.asyncio
async def test_register_new_writer_user_as_admin_returns_ok(client):
    token = await get_jwt(client, TEST_ADMIN_USER, TEST_ADMIN_PASS)
    r = await register_user(client, token, "writerX", "testpass-val", role="writer")
    assert r.status_code in (200, 409)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "username,credential",
    [(TEST_READER_USER, TEST_READER_PASS), (TEST_WRITER_USER, TEST_WRITER_PASS)],
)
async def test_register_as_non_admin_returns_unauthorized(client, username, credential):
    token = await get_jwt(client, username, credential)
    r = await register_user(client, token, "unauthorizedUser", "test-val")
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_post_item_without_token_returns_401(client):
    r = await client.post("/items", json={"name": "insecure"})
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_post_item_with_writer_token_returns_201(client):
    token = await get_jwt(client, TEST_WRITER_USER, TEST_WRITER_PASS)
    r = await client.post(
        "/items", json={"name": "test item"}, headers=auth_headers(token)
    )
    assert r.status_code == 201


@pytest.mark.asyncio
async def test_post_item_with_reader_token_returns_unauthorized(client):
    token = await get_jwt(client, TEST_READER_USER, TEST_READER_PASS)
    r = await client.post(
        "/items", json={"name": "reader-should-not-post"}, headers=auth_headers(token)
    )
    assert r.status_code == 401
